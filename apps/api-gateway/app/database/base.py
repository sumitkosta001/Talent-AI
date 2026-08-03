"""SQLAlchemy 2.0 Declarative Base Root and Entity Mixins.

Defines the root DeclarativeBase class, reusable entity mixins (UUID, Timestamp,
SoftDelete, Audit), and the abstract BaseModel entity class.

Mixin Composition:
    Base            — Root DeclarativeBase (SQLAlchemy 2.0 registry).
    UUIDMixin       — UUID v4 primary key.
    TimestampMixin  — created_at / updated_at with server defaults.
    SoftDeleteMixin — Logical deletion flag and timestamp.
    AuditMixin      — created_by / updated_by user tracking.
    BaseModel       — Abstract model combining all mixins above.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Root DeclarativeBase class for all SQLAlchemy 2.0 ORM entity models."""

    pass


class UUIDMixin:
    """Mixin providing UUID v4 primary key column.

    Uses PostgreSQL-native UUID type for storage efficiency and index performance.
    UUID v4 keys are generated client-side, eliminating database round-trips for
    ID assignment and enabling distributed ID generation without coordination.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique UUID v4 surrogate primary key identifier.",
    )


class TimestampMixin:
    """Mixin providing creation and automatic modification UTC timestamps.

    Both columns use server_default=func.now() so the database generates the
    timestamp even for raw SQL inserts outside the ORM. The Python-side defaults
    ensure consistency when creating objects in application code.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
        doc="UTC timestamp indicating when the entity was created.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
        doc="UTC timestamp indicating when the entity was last updated.",
    )


class SoftDeleteMixin:
    """Mixin providing logical soft deletion flags and timestamp tracking.

    Soft deletion preserves referential integrity and audit trails by marking
    records as deleted rather than physically removing them. Query filters
    should exclude is_deleted=True for normal operations.
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Boolean flag indicating whether entity has been soft deleted.",
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
        doc="UTC timestamp indicating when the entity was soft deleted.",
    )


class AuditMixin:
    """Mixin providing user-level audit trail fields.

    Tracks which user created or last modified a record. Nullable because
    system-generated records (seeds, migrations, background jobs) may not
    have an originating user context.

    Note:
        These columns intentionally do NOT use ForeignKey("users.id") to avoid
        circular dependency issues during table creation. The application layer
        enforces referential integrity via service/repository validation.
    """

    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        default=None,
        doc="UUID of the user who created this entity. Null for system operations.",
    )
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        default=None,
        doc="UUID of the user who last updated this entity. Null for system operations.",
    )


class BaseModel(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Abstract base model entity combining all standard mixins.

    Every domain entity in the TalentAI platform should inherit from this class
    to receive: UUID primary key, timestamps, soft-delete, and audit tracking.

    Usage:
        class User(BaseModel):
            __tablename__ = "users"
            email: Mapped[str] = mapped_column(...)
    """

    __abstract__ = True

