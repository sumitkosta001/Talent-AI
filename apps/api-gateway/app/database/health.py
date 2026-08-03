"""Database Health Check Diagnostic Service.

Provides async database connectivity, latency measurement, version inspection,
and status diagnostics for application endpoints and health monitoring.
"""

import time
import logging
import traceback
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.engine import make_url
from app.config.settings import settings
from app.database.engine import engine

logger = logging.getLogger("talentai.database.health")


async def check_database_health() -> Dict[str, Any]:
    """Inspect PostgreSQL database connectivity, latency, version, database name, and user.

    Creates a single async connection from the engine pool, executes version inspection,
    measures latency, and closes the connection cleanly via context manager.

    Returns:
        Structured dictionary containing health metrics and database metadata.
    """
    start_time = time.perf_counter()
    parsed_info = make_url(settings.database.url)
    try:
        # Use single connection from canonical pool with guaranteed closure
        async with engine.connect() as conn:
            # Execute version and database inspection queries
            version_res = await conn.execute(text("SELECT version();"))
            version_row = version_res.scalar()

            db_res = await conn.execute(text("SELECT current_database();"))
            db_name = db_res.scalar()

            user_res = await conn.execute(text("SELECT current_user;"))
            user_name = user_res.scalar()

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return {
                "status": "connected",
                "connection": "success",
                "driver": parsed_info.drivername or "postgresql+asyncpg",
                "host": parsed_info.host or "unknown",
                "database": str(db_name) if db_name else "Unknown",
                "user": str(user_name) if user_name else "Unknown",
                "version": str(version_row) if version_row else "Unknown",
                "latency_ms": latency_ms,
            }
    except Exception as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        error_msg = str(exc) or type(exc).__name__
        tb_str = traceback.format_exc()
        logger.error(f"Database health check failed ({type(exc).__name__}): {exc}\n{tb_str}")
        return {
            "status": "disconnected",
            "connection": "failed",
            "driver": parsed_info.drivername or "postgresql+asyncpg",
            "host": parsed_info.host or "unknown",
            "database": parsed_info.database or "unknown",
            "user": parsed_info.username or "unknown",
            "version": None,
            "latency_ms": latency_ms,
            "error": error_msg,
        }
