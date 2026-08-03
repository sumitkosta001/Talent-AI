"""Database AsyncSession Dependency Injection Providers.

Yields scoped AsyncSession context for FastAPI route handlers with automatic
rollback on exception, automatic commit on success, and guaranteed session closure.
"""

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal

logger = logging.getLogger("talentai.database.dependencies")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency provider yielding an active AsyncSession database context.

    Yields:
        Active SQLAlchemy AsyncSession instance.

    Raises:
        Exception: Re-raises any exception after executing session rollback.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            logger.error(f"Database session error occurred, transaction rolled back: {exc}")
            raise
        finally:
            await session.close()
