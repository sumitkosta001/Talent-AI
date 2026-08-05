"""RefreshToken ORM Entity Model — TalentAI Platform.

Stores hashed refresh tokens in PostgreSQL for secure, server-side session
management. Each token is linked to a specific user and has an explicit
expiration timestamp, enabling token rotation and revocation.

Architecture:
    - Inherits from BaseModel which provides: id (UUID), created_at, updated_at,
      is_deleted, deleted_at, created_by, updated_by.
    - Uses SQLAlchemy 2.0 typed ORM (Mapped, mapped_column) exclusively.
    - Foreign key references users.id with ON DELETE CASCADE so deleting a
      user automatically purges all their refresh tokens.
    - Relationship uses TYPE_CHECKING to prevent circular imports.

Table: refresh_tokens
Primary Key: id (UUID v4, inherited from BaseModel)
Foreign Key: user_id → users.id (CASCADE)
Indexes: user_id, token, revoked, created_at, expires_at
Unique Constraints: token
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

# ---------------------------------------------------------------------------
# TYPE_CHECKING import for the User model to prevent circular imports.
#
# The relationship() uses a string reference "User" which SQLAlchemy resolves
# at mapper configuration time, so the actual import is only needed for
# static type checking and IDE autocompletion.
# ---------------------------------------------------------------------------
if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(BaseModel):
    """Persistent refresh token entity for JWT session management.

    Each row represents a single refresh token issued to a user during
    login or token rotation. The token value stored here is a SHA-256
    hash of the actual token sent to the client, preventing token
    exposure even in the event of a database breach.

    Lifecycle:
        1. LOGIN:   Create a new RefreshToken row with revoked=False.
        2. REFRESH: Revoke the current token, issue a new one (rotation).
        3. LOGOUT:  Revoke the token (set revoked=True).
        4. CLEANUP: Periodic job deletes expired/revoked tokens.

    Attributes:
        user_id:    UUID foreign key linking this token to its owner.
        token:      SHA-256 hash of the refresh token value. Unique.
        expires_at: UTC timestamp after which the token is no longer valid.
        revoked:    Flag indicating the token has been explicitly revoked.

    Inherited from BaseModel:
        id, created_at, updated_at, is_deleted, deleted_at, created_by, updated_by
    """

    __tablename__ = "refresh_tokens"

    # ==========================================================================
    # FOREIGN KEY — USER OWNERSHIP
    # ==========================================================================

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc=(
            "UUID of the user who owns this refresh token. "
            "Indexed for fast lookup during token refresh and revocation. "
            "CASCADE delete ensures tokens are removed when the user is deleted."
        ),
    )

    # ==========================================================================
    # TOKEN VALUE (HASHED)
    # ==========================================================================

    token: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
        index=True,
        doc=(
            "SHA-256 hash of the refresh token value sent to the client. "
            "The raw token is NEVER stored — only the hash. "
            "Unique constraint prevents duplicate token issuance."
        ),
    )

    # ==========================================================================
    # EXPIRATION
    # ==========================================================================

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc=(
            "UTC timestamp after which this refresh token is no longer valid. "
            "Typically set to 7 days (development) or 30 days (production)."
        ),
    )

    # ==========================================================================
    # REVOCATION FLAG
    # ==========================================================================

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
        index=True,
        doc=(
            "Indicates whether this token has been explicitly revoked. "
            "Set to True on logout, password change, or token rotation."
        ),
    )

    # ==========================================================================
    # RELATIONSHIP — BACK-REFERENCE TO USER
    # ==========================================================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
        lazy="joined",
        doc="Many-to-one relationship to the owning User entity.",
    )

    # ==========================================================================
    # TABLE-LEVEL CONSTRAINTS AND INDEXES
    # ==========================================================================

    __table_args__ = (
        # Composite index: "Find active tokens for a specific user."
        Index(
            "ix_refresh_tokens_user_id_revoked",
            "user_id",
            "revoked",
        ),

        # Index on expires_at for cleanup job: DELETE WHERE expires_at < NOW().
        Index(
            "ix_refresh_tokens_expires_at",
            "expires_at",
        ),

        # Index on created_at for chronological session listing.
        Index(
            "ix_refresh_tokens_created_at",
            "created_at",
        ),

        # Table comment visible in PostgreSQL catalog.
        {
            "comment": (
                "Stores hashed JWT refresh tokens for secure session management. "
                "Supports revocation, rotation, and multi-device session tracking."
            ),
        },
    )

    # ==========================================================================
    # COMPUTED PROPERTIES
    # ==========================================================================

    @property
    def is_expired(self) -> bool:
        """Check whether this token has passed its expiration timestamp."""
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_usable(self) -> bool:
        """Check whether this token can be used for a refresh operation."""
        return not self.revoked and not self.is_expired

    # ==========================================================================
    # REPRESENTATION
    # ==========================================================================

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        token_preview = self.token[:12] + "..." if self.token else "N/A"
        return (
            f"<RefreshToken("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"token='{token_preview}', "
            f"revoked={self.revoked!r}, "
            f"expires_at={self.expires_at!r}"
            f")>"
        )
