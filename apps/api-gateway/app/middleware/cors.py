"""CORS (Cross-Origin Resource Sharing) Middleware Setup.

Configures allowed origins, credentials, methods, and headers for client app security.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings


def setup_cors_middleware(app: FastAPI) -> None:
    """Register CORSMiddleware on the FastAPI application instance.
    
    Args:
        app: FastAPI application target.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.allowed_hosts,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time-MS"],
    )
