"""Domain Enumeration Types for TalentAI ORM Models.

Defines Python enums that map to PostgreSQL ENUM types via SQLAlchemy.
These enums are used as column types in ORM models and are automatically
created as native PostgreSQL enum types during Alembic migrations.

Design Decisions:
    - Inherit from (str, enum.Enum) so values serialize cleanly to JSON
      in Pydantic schemas and API responses without custom encoders.
    - Use SCREAMING_SNAKE_CASE for enum members (Python convention).
    - Use lowercase values for PostgreSQL storage (database convention).
    - Each enum is a separate class to support independent evolution
      and avoid monolithic type definitions.
"""

import enum


class UserRole(str, enum.Enum):
    """Authorization roles within the TalentAI platform.

    Determines access control boundaries across the application.
    Used by the RBAC middleware and permission decorators to enforce
    route-level and resource-level authorization.

    Members:
        CANDIDATE       — Job seekers using resume builder and applying to jobs.
        RECRUITER       — Agency or in-house recruiters managing job postings.
        HIRING_MANAGER  — Internal hiring managers reviewing candidates.
        INTERVIEWER     — Users conducting interviews and providing feedback.
        ADMIN           — Platform administrators with elevated privileges.
        SUPER_ADMIN     — Root-level administrators with unrestricted access.
    """

    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
    INTERVIEWER = "interviewer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class AuthProvider(str, enum.Enum):
    """Authentication identity providers supported by TalentAI.

    Tracks how a user originally registered and authenticated.
    Used by the OAuth service to determine which external provider
    issued the identity token, and by the auth middleware to select
    the correct token validation strategy.

    Members:
        LOCAL       — Email/password registration (internal credentials).
        GOOGLE      — Google OAuth 2.0 identity provider.
        GITHUB      — GitHub OAuth 2.0 identity provider.
        LINKEDIN    — LinkedIn OAuth 2.0 identity provider.
        MICROSOFT   — Microsoft Entra ID (Azure AD) identity provider.
    """

    LOCAL = "local"
    GOOGLE = "google"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    MICROSOFT = "microsoft"
