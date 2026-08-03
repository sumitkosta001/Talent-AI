"""TalentAI API Gateway Main Application Entry Point.

Production-grade FastAPI instance instantiation, metadata, middleware setup,
exception handlers, router registration, lifespan manager, and /health check handler.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.core.lifespan import lifespan
from app.database.health import check_database_health
from app.exceptions.base import TalentAIException
from app.middleware.cors import setup_cors_middleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware
from app.api.v1.router import api_v1_router

logger = logging.getLogger("talentai.main")


def create_application() -> FastAPI:
    """Construct and configure production-ready FastAPI application instance.
    
    Returns:
        Fully configured FastAPI instance.
    """
    app = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        description="Production-Grade TalentAI Enterprise Modular Monolith API Gateway",
        docs_url=settings.app.docs_url if settings.app.debug else None,
        redoc_url=settings.app.redoc_url if settings.app.debug else None,
        openapi_url=settings.app.openapi_url if settings.app.debug else None,
        contact={
            "name": settings.app.contact_name,
            "email": settings.app.contact_email,
        },
        license_info={
            "name": settings.app.license_name,
        },
        lifespan=lifespan,
    )

    # --------------------------------------------------------------------------
    # MIDDLEWARE REGISTRATION PIPELINE
    # --------------------------------------------------------------------------
    setup_cors_middleware(app)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)

    # --------------------------------------------------------------------------
    # GLOBAL EXCEPTION HANDLERS
    # --------------------------------------------------------------------------
    @app.exception_handler(TalentAIException)
    async def talentai_exception_handler(request: Request, exc: TalentAIException) -> JSONResponse:
        """Handle custom domain TalentAI exceptions."""
        request_id = getattr(request.state, "request_id", "N/A")
        logger.warning(f"[{request_id}] Domain Exception ({exc.status_code}): {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.message,
                    "status_code": exc.status_code,
                    "details": exc.details,
                },
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle Pydantic request body & query validation errors."""
        request_id = getattr(request.state, "request_id", "N/A")
        logger.warning(f"[{request_id}] Request Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "message": "Input validation failed.",
                    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "details": jsonable_encoder(exc.errors()),
                },
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle standard HTTP exceptions."""
        request_id = getattr(request.state, "request_id", "N/A")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.detail,
                    "status_code": exc.status_code,
                },
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unhandled server exceptions safely without leaking stack traces."""
        request_id = getattr(request.state, "request_id", "N/A")
        logger.error(f"[{request_id}] Unhandled Server Error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "message": "An internal server error occurred.",
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    # --------------------------------------------------------------------------
    # API ROUTER REGISTRATION
    # --------------------------------------------------------------------------
    app.include_router(api_v1_router, prefix="/api")

    # --------------------------------------------------------------------------
    # HEALTH CHECK ENDPOINT (DATABASE INTEGRATION)
    # --------------------------------------------------------------------------
    @app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
    async def health_check() -> Dict[str, Any]:
        """System and database operational health check endpoint.
        
        Returns:
            Structured dictionary containing health status, database diagnostics,
            application metadata, and current UTC timestamp.
        """
        db_health = await check_database_health()
        
        is_healthy = db_health.get("connection") == "success"
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "database": {
                "status": db_health.get("status"),
                "driver": db_health.get("driver"),
                "host": db_health.get("host"),
                "database": db_health.get("database"),
                "user": db_health.get("user"),
                "version": db_health.get("version"),
                "latency_ms": db_health.get("latency_ms"),
            },
            "application": {
                "name": settings.app.name,
                "version": settings.app.version,
                "environment": settings.app.env,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    return app


app = create_application()
