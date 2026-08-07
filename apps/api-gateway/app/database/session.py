"""SQLAlchemy 2.0 Async Session Factory and Generator.

Configures SessionLocal async_sessionmaker bound to the global AsyncEngine.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.database.engine import engine

# Async Session Factory
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
AsyncSessionLocal = SessionLocal


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a scoped AsyncSession context for database operations.

    Yields:
        Active SQLAlchemy AsyncSession instance.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
