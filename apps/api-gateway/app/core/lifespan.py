"""FastAPI Application Async Lifespan Context Handler.

Manages startup database connection verification, logging without password leakage,
and graceful engine disposal on shutdown.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.config.settings import settings
from app.config.logging import setup_logging
from app.database.engine import engine
from app.database.health import check_database_health
from app.utils.database import parse_database_url

logger = logging.getLogger("talentai.lifespan")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle resources.
    
    Args:
        app: Target FastAPI application instance.
    """
    # --------------------------------------------------------------------------
    # STARTUP ACTIONS
    # --------------------------------------------------------------------------
    setup_logging()
    logger.info(f"Starting {settings.app.name} v{settings.app.version} ({settings.app.env} mode)...")

    # Parse and log connection info (safely omitting passwords) using SQLAlchemy parser
    conn_info = parse_database_url(settings.database.url)
    logger.info(
        f"Database Configuration Loaded - Host: {conn_info['host']}, "
        f"Database: {conn_info['database']}, Driver: {conn_info['driver']}, "
        f"Environment: {settings.app.env}, Pool Size: {settings.database.pool_size}"
    )

    # Verify Database Connection
    db_health = await check_database_health()
    if db_health.get("connection") == "success":
        logger.info(
            f"Database Connected - Host: {db_health.get('host')}, DB: {db_health.get('database')}, "
            f"User: {db_health.get('user')}, Latency: {db_health.get('latency_ms')}ms"
        )
    else:
        logger.error(
            f"Database Connection Failed - Host: {conn_info['host']}, DB: {conn_info['database']}. "
            f"Error: {db_health.get('error')}"
        )

    logger.info("Initializing Redis connection pool placeholder...")
    logger.info("Initializing Redis connection pool placeholder...")
    logger.info("Initializing AI SDK client wrappers placeholder...")
    logger.info("Initializing scheduler placeholder...")

    yield

    # --------------------------------------------------------------------------
    # SHUTDOWN ACTIONS
    # --------------------------------------------------------------------------
    logger.info(f"Stopping {settings.app.name}...")

    # Dispose SQLAlchemy AsyncEngine pool
    try:
        await engine.dispose()
        logger.info("Database Disconnected - AsyncEngine connection pool disposed.")
    except Exception as exc:
        logger.error(f"Error disposing database engine on shutdown: {exc}")

    logger.info("Closing Redis connections placeholder...")
    logger.info("Shutdown sequence complete.")
