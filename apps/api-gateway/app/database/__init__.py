"""SQLAlchemy 2.0 Async Database Package.

Re-exports AsyncEngine, DeclarativeBase, BaseModel, Mixins, SessionLocal, get_async_session, get_db, and health check.
"""

from app.database.engine import engine
from app.database.base import (
    Base,
    BaseModel,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    AuditMixin,
)
from app.database.session import SessionLocal, AsyncSessionLocal, get_async_session
from app.database.dependencies import get_db
from app.database.health import check_database_health

__all__ = [
    "engine",
    "Base",
    "BaseModel",
    "UUIDMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    "AuditMixin",
    "SessionLocal",
    "AsyncSessionLocal",
    "get_async_session",
    "get_db",
    "check_database_health",
]
