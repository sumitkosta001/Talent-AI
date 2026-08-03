"""User ORM Entity Model — TalentAI Platform.

The User model is the foundational entity of the TalentAI platform. Every other
domain model (Resume, JobApplication, Company, Interview, Notification, etc.)
references this model directly or transitively.

Architecture:
    - Inherits from BaseModel which provides: id (UUID), created_at, updated_at,
      is_deleted, deleted_at, created_by, updated_by.
    - Uses SQLAlchemy 2.0 typed ORM (Mapped, mapped_column) exclusively.
    - PostgreSQL-native types (UUID, ENUM, TIMESTAMPTZ) for optimal storage.
    - Relationship placeholders use TYPE_CHECKING to prevent circular imports.
    - Designed for Clean Architecture: the model contains NO business logic,
      NO password hashing, NO JWT generation. Those belong in the service layer.

Table: users
Primary Key: id (UUID v4, inherited from BaseModel)
Indexes: email, role, is_active, created_at
Unique Constraints: email, phone_number (partial — only when not null)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel
from app.models.enums import AuthProvider, UserRole

# ---------------------------------------------------------------------------
# TYPE_CHECKING imports for forward-referenced relationship targets.
#
# These models do not exist yet. By importing them inside TYPE_CHECKING,
# we get IDE autocompletion and type-checker support without triggering
# ImportError at runtime. When these models are created, the relationship()
# back_populates will link them bidirectionally.
# ---------------------------------------------------------------------------
if TYPE_CHECKING:
    pass
    # from app.models.resume import Resume
    # from app.models.job_application import JobApplication
    # from app.models.company import Company
    # from app.models.interview import Interview
    # from app.models.notification import Notification
    # from app.models.refresh_token import RefreshToken
    # from app.models.audit_log import AuditLog


class User(BaseModel):
    """Core user identity and authentication entity.

    Represents a registered user on the TalentAI platform. Supports multiple
    authentication strategies (local email/password, Google, GitHub, LinkedIn,
    Microsoft) and role-based access control (RBAC).

    This model is intentionally thin — it stores identity and authentication
    state only. Extended profile data (bio, skills, experience) should live
    in a separate UserProfile model linked via one-to-one relationship.

    Attributes:
        first_name:           User's given name. Required for personalization.
        last_name:            User's family name. Required for formal communications.
        email:                Primary login identifier. Unique, indexed, lowercased.
        phone_number:         Optional contact number. Unique when provided.
        password_hash:        Bcrypt/Argon2 hash. Null for OAuth-only accounts.
        profile_picture_url:  CDN URL for avatar image (Cloudinary, S3, etc.).
        role:                 RBAC authorization role (candidate, recruiter, admin, etc.).
        provider:             Authentication identity provider (local, google, etc.).
        provider_id:          External OAuth provider's unique user identifier.
        is_active:            Account activation status. Disabled accounts cannot login.
        is_verified:          Email verification status. Unverified users have limited access.
        is_superuser:         Superuser bypass flag. Grants unrestricted platform access.
        last_login_at:        Timestamp of most recent successful authentication.
        failed_login_attempts: Consecutive failed login count. Used for account lockout policy.

    Inherited from BaseModel:
        id, created_at, updated_at, is_deleted, deleted_at, created_by, updated_by

    Table Constraints:
        - UNIQUE on email (enforced at database level).
        - UNIQUE on phone_number (partial — only when not null).
        - CHECK on failed_login_attempts >= 0.
        - Indexes on email, role, is_active, created_at for query performance.
    """

    __tablename__ = "users"

    # ==========================================================================
    # PERSONAL INFORMATION
    # ==========================================================================

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="User's given (first) name. Used in greetings and display.",
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="User's family (last) name. Used in formal contexts and full name display.",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Primary email address. Serves as the login identifier. Must be unique.",
    )

    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        default=None,
        doc="Optional contact phone number in E.164 format (e.g., +919876543210).",
    )

    # ==========================================================================
    # AUTHENTICATION & SECURITY
    # ==========================================================================

    password_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc=(
            "Bcrypt or Argon2id hash of the user's password. "
            "Null for OAuth-only accounts that never set a local password. "
            "NEVER store or expose the raw password."
        ),
    )

    profile_picture_url: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
        default=None,
        doc="URL to the user's profile/avatar image hosted on CDN (Cloudinary, S3).",
    )

    role: Mapped[UserRole] = mapped_column(
        PG_ENUM(
            UserRole,
            name="user_role",
            create_constraint=False,
            native_enum=True,
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=False,
        default=UserRole.CANDIDATE,
        server_default=text("'candidate'"),
        index=True,
        doc="RBAC authorization role determining the user's platform permissions.",
    )

    provider: Mapped[AuthProvider] = mapped_column(
        PG_ENUM(
            AuthProvider,
            name="auth_provider",
            create_constraint=False,
            native_enum=True,
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=False,
        default=AuthProvider.LOCAL,
        server_default=text("'local'"),
        doc="Authentication provider that issued this user's identity credentials.",
    )

    provider_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc=(
            "Unique identifier from the external OAuth provider. "
            "For example, Google sub claim or GitHub user ID. "
            "Null for locally-registered accounts."
        ),
    )

    # ==========================================================================
    # ACCOUNT STATUS FLAGS
    # ==========================================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
        index=True,
        doc="Account activation status. Deactivated users are denied login access.",
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
        doc="Email verification status. Unverified users may have restricted access.",
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
        doc="Superuser flag. Bypasses all RBAC checks. Use sparingly.",
    )

    # ==========================================================================
    # LOGIN TRACKING
    # ==========================================================================

    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="UTC timestamp of the most recent successful authentication event.",
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
        doc=(
            "Count of consecutive failed login attempts. "
            "Reset to 0 on successful login. Used by the account lockout policy."
        ),
    )

    # ==========================================================================
    # RELATIONSHIP PLACEHOLDERS
    # ==========================================================================
    # These relationships reference models that do not exist yet.
    # They are defined as commented-out placeholders to document the intended
    # data model relationships. Uncomment and configure back_populates when
    # the target model is created.
    #
    # resumes: Mapped[list["Resume"]] = relationship(
    #     "Resume",
    #     back_populates="user",
    #     lazy="selectin",
    #     cascade="all, delete-orphan",
    #     doc="User's uploaded resumes and resume builder documents.",
    # )
    #
    # job_applications: Mapped[list["JobApplication"]] = relationship(
    #     "JobApplication",
    #     back_populates="user",
    #     lazy="selectin",
    #     cascade="all, delete-orphan",
    #     doc="Job applications submitted by this user.",
    # )
    #
    # company: Mapped[Optional["Company"]] = relationship(
    #     "Company",
    #     back_populates="owner",
    #     uselist=False,
    #     doc="Company owned or managed by this user (recruiters/hiring managers).",
    # )
    #
    # interviews: Mapped[list["Interview"]] = relationship(
    #     "Interview",
    #     back_populates="candidate",
    #     lazy="selectin",
    #     doc="AI or live interviews associated with this user.",
    # )
    #
    # notifications: Mapped[list["Notification"]] = relationship(
    #     "Notification",
    #     back_populates="user",
    #     lazy="selectin",
    #     cascade="all, delete-orphan",
    #     doc="Push/email/in-app notifications sent to this user.",
    # )
    #
    # refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
    #     "RefreshToken",
    #     back_populates="user",
    #     lazy="selectin",
    #     cascade="all, delete-orphan",
    #     doc="Active JWT refresh tokens for session management.",
    # )
    #
    # audit_logs: Mapped[list["AuditLog"]] = relationship(
    #     "AuditLog",
    #     back_populates="user",
    #     lazy="selectin",
    #     doc="Audit trail entries recording user actions.",
    # )

    # ==========================================================================
    # TABLE-LEVEL CONSTRAINTS AND INDEXES
    # ==========================================================================

    __table_args__ = (
        # Unique constraint on phone_number — only enforced when NOT NULL.
        # PostgreSQL partial unique indexes naturally handle this behavior:
        # multiple NULL values are allowed, but non-null values must be unique.
        UniqueConstraint(
            "phone_number",
            name="uq_users_phone_number",
        ),

        # Composite index for authentication queries:
        # SELECT * FROM users WHERE email = ? AND provider = ?
        Index(
            "ix_users_email_provider",
            "email",
            "provider",
        ),

        # Index on created_at for sorting and pagination queries.
        Index(
            "ix_users_created_at",
            "created_at",
        ),

        # Prevent negative failed login attempts at the database level.
        CheckConstraint(
            "failed_login_attempts >= 0",
            name="ck_users_failed_login_attempts_non_negative",
        ),

        # Table comment visible in PostgreSQL catalog (pg_description).
        {
            "comment": (
                "Core user identity table for the TalentAI platform. "
                "Stores authentication credentials, RBAC roles, and account status."
            ),
        },
    )

    # ==========================================================================
    # COMPUTED PROPERTIES
    # ==========================================================================

    @property
    def full_name(self) -> str:
        """Compute the user's display name by joining first and last name.

        Returns:
            Full name string with proper spacing.
        """
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_oauth_user(self) -> bool:
        """Check whether this user authenticated via an external OAuth provider.

        Returns:
            True if the user registered via Google, GitHub, LinkedIn, or Microsoft.
        """
        return self.provider != AuthProvider.LOCAL

    @property
    def is_locked(self) -> bool:
        """Check whether the account is locked due to excessive failed login attempts.

        The lockout threshold (default: 5) should be configurable via settings.
        This property provides a quick check; the actual lockout enforcement
        belongs in the authentication service layer.

        Returns:
            True if failed_login_attempts exceeds the lockout threshold.
        """
        return (self.failed_login_attempts or 0) >= 5

    # ==========================================================================
    # REPRESENTATION
    # ==========================================================================

    def __repr__(self) -> str:
        """Return a developer-friendly string representation.

        Intentionally excludes password_hash and other sensitive fields.
        Includes only identity and status fields useful for debugging.
        """
        return (
            f"<User("
            f"id={self.id!r}, "
            f"email={self.email!r}, "
            f"role={self.role.value!r}, "
            f"provider={self.provider.value!r}, "
            f"is_active={self.is_active!r}, "
            f"is_verified={self.is_verified!r}"
            f")>"
        )
