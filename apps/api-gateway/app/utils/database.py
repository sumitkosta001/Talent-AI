"""Reusable Database Operation Utility Helpers.

Provides wrapper utilities for SQLAlchemy 2.0 AsyncSession transactions,
query execution, scalar retrieval, and session state management.
"""

import logging
from typing import Any, Dict, Optional, Sequence
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Executable
from app.exceptions.database import DatabaseTransactionError, DatabaseQueryError

logger = logging.getLogger("talentai.utils.database")


async def commit(session: AsyncSession) -> None:
    """Safely commit session transaction with automatic rollback on error.
    
    Args:
        session: Active AsyncSession instance.
        
    Raises:
        DatabaseTransactionError: If commit operation fails.
    """
    try:
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.error(f"Failed to commit transaction: {exc}")
        raise DatabaseTransactionError(message=f"Transaction commit failed: {exc}") from exc


async def rollback(session: AsyncSession) -> None:
    """Roll back active session transaction.
    
    Args:
        session: Active AsyncSession instance.
    """
    try:
        await session.rollback()
    except Exception as exc:
        logger.error(f"Failed to rollback transaction: {exc}")


async def refresh(
    session: AsyncSession,
    instance: Any,
    attribute_names: Optional[Sequence[str]] = None,
) -> None:
    """Refresh model instance state from database.
    
    Args:
        session: Active AsyncSession instance.
        instance: ORM model entity instance.
        attribute_names: Optional list of attribute names to refresh.
        
    Raises:
        DatabaseQueryError: If refresh operation fails.
    """
    try:
        await session.refresh(instance, attribute_names=attribute_names)
    except Exception as exc:
        logger.error(f"Failed to refresh model instance: {exc}")
        raise DatabaseQueryError(message=f"Model refresh failed: {exc}") from exc


async def flush(session: AsyncSession) -> None:
    """Flush pending model state changes to database transaction.
    
    Args:
        session: Active AsyncSession instance.
        
    Raises:
        DatabaseTransactionError: If flush operation fails.
    """
    try:
        await session.flush()
    except Exception as exc:
        await session.rollback()
        logger.error(f"Failed to flush session changes: {exc}")
        raise DatabaseTransactionError(message=f"Session flush failed: {exc}") from exc


@asynccontextmanager
async def transaction(session: AsyncSession):
    """Async context manager executing block within a single transaction with auto rollback.
    
    Args:
        session: Active AsyncSession instance.
        
    Yields:
        Active AsyncSession instance.
    """
    try:
        yield session
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.error(f"Transaction block failed, rolled back: {exc}")
        raise DatabaseTransactionError(message=f"Transaction context failed: {exc}") from exc


async def execute(
    session: AsyncSession,
    statement: Executable,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """Execute a raw SQL or ORM statement.
    
    Args:
        session: Active AsyncSession instance.
        statement: Executable statement.
        params: Optional query parameter bindings.
        
    Returns:
        Result execution object.
        
    Raises:
        DatabaseQueryError: If query execution fails.
    """
    try:
        return await session.execute(statement, params or {})
    except Exception as exc:
        logger.error(f"Statement execution failed: {exc}")
        raise DatabaseQueryError(message=f"Query execution failed: {exc}") from exc


async def scalar(
    session: AsyncSession,
    statement: Executable,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """Execute a statement and return scalar result value.
    
    Args:
        session: Active AsyncSession instance.
        statement: Executable statement.
        params: Optional query parameter bindings.
        
    Returns:
        First column of first row scalar value or None.
        
    Raises:
        DatabaseQueryError: If scalar query execution fails.
    """
    try:
        result = await session.execute(statement, params or {})
        return result.scalar()
    except Exception as exc:
        logger.error(f"Scalar query execution failed: {exc}")
        raise DatabaseQueryError(message=f"Scalar query execution failed: {exc}") from exc


def parse_database_url(url: str) -> dict:
    """Parse connection details from a DATABASE_URL string using SQLAlchemy make_url parser."""
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    return {
        "driver": parsed.drivername or "unknown",
        "host": parsed.host or "unknown",
        "port": parsed.port or 5432,
        "database": parsed.database or "unknown",
        "username": parsed.username or "unknown",
    }

