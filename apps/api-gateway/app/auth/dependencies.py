"""Authentication and Authorization FastAPI Security Dependencies.

Provides reusable dependency injection providers for JWT authentication,
account state verification, superuser bypass, role-based access control (RBAC),
and fine-grained permission enforcement across all API endpoints.
"""

import logging
from typing import Annotated, Sequence, Union
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.models.user import User
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
from app.auth.security import decode_access_token
from app.exceptions.auth import (
    AuthenticationError,
    InvalidTokenError,
    ExpiredTokenError,
    PermissionDeniedError,
)
from app.exceptions.users import UserNotFoundError

logger = logging.getLogger("talentai.auth.dependencies")

# Singleton HTTPBearer instance enforcing Authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=True)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Extract JWT bearer token, decode access claims, and load active User entity.

    Args:
        credentials: HTTPAuthorizationCredentials containing the Bearer token string.
        db: Scoped database AsyncSession instance.

    Returns:
        User ORM entity associated with the token.

    Raises:
        AuthenticationError: If token is missing, malformed, invalid, or expired.
        UserNotFoundError: If user associated with token sub claim does not exist.
    """
    if not credentials or not credentials.credentials:
        logger.warning("Authentication failed: Missing Authorization bearer header.")
        raise AuthenticationError("Authorization bearer token required.")

    token = credentials.credentials
    payload = decode_access_token(token)

    user_id_str = payload.get("sub")
    if not user_id_str:
        logger.warning("Authentication failed: JWT access token missing 'sub' claim.")
        raise InvalidTokenError("Access token missing subject identifier.")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id_str)

    if not user or user.is_deleted:
        logger.warning("Authentication failed: User ID '%s' not found or deleted.", user_id_str)
        raise AuthenticationError("User account associated with token not found.")

    logger.info("Successfully authenticated user: %s (ID: %s)", user.email, user.id)
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Validate that the authenticated user account is active and non-suspended.

    Args:
        current_user: User entity injected from get_current_user.

    Returns:
        Active User ORM entity.

    Raises:
        PermissionDeniedError: 403 Forbidden if user account is deactivated.
    """
    if not current_user.is_active:
        logger.warning("Access denied: User account %s is inactive.", current_user.email)
        raise PermissionDeniedError("User account has been suspended or deactivated.")

    return current_user


async def get_current_verified_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Validate that the active user account has completed email verification.

    Args:
        current_user: User entity injected from get_current_active_user.

    Returns:
        Verified active User ORM entity.

    Raises:
        PermissionDeniedError: 403 Forbidden if user email is unverified.
    """
    if not current_user.is_verified:
        logger.warning("Access denied: User %s email is unverified.", current_user.email)
        raise PermissionDeniedError("Email verification is required to access this resource.")

    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Validate that the active user possesses root superuser privileges.

    Args:
        current_user: User entity injected from get_current_active_user.

    Returns:
        Superuser ORM entity.

    Raises:
        PermissionDeniedError: 403 Forbidden if user is not a superuser.
    """
    if not current_user.is_superuser:
        logger.warning("Superuser access denied for user: %s", current_user.email)
        raise PermissionDeniedError("Superuser administrative privileges required.")

    logger.info("Superuser access granted for: %s", current_user.email)
    return current_user


async def get_current_candidate(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Enforce that the authenticated user possesses Candidate role permissions.

    Superusers automatically bypass role checks.

    Args:
        current_user: Active User entity.

    Returns:
        Authorized Candidate User entity.

    Raises:
        PermissionDeniedError: 403 Forbidden if user is not a candidate or superuser.
    """
    if current_user.is_superuser or current_user.role == UserRole.CANDIDATE:
        return current_user

    logger.warning("Candidate role access denied for user: %s (role: %s)", current_user.email, current_user.role)
    raise PermissionDeniedError("Candidate role required for this action.")


async def get_current_company(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Enforce that the authenticated user possesses Company/Recruiter role permissions.

    Superusers automatically bypass role checks.

    Args:
        current_user: Active User entity.

    Returns:
        Authorized Recruiter/Hiring Manager User entity.

    Raises:
        PermissionDeniedError: 403 Forbidden if user is not a recruiter/hiring manager or superuser.
    """
    allowed_roles = {UserRole.RECRUITER, UserRole.HIRING_MANAGER, "company", "recruiter", "hiring_manager"}
    if current_user.is_superuser or current_user.role in allowed_roles or str(current_user.role).lower() in allowed_roles:
        return current_user

    logger.warning("Company role access denied for user: %s (role: %s)", current_user.email, current_user.role)
    raise PermissionDeniedError("Company or Recruiter role required for this action.")


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Enforce that the authenticated user possesses Administrator role permissions.

    Superusers automatically bypass role checks.

    Args:
        current_user: Active User entity.

    Returns:
        Authorized Admin User entity.

    Raises:
        PermissionDeniedError: 403 Forbidden if user is not an admin or superuser.
    """
    allowed_roles = {UserRole.ADMIN, UserRole.SUPER_ADMIN, "admin", "super_admin"}
    if current_user.is_superuser or current_user.role in allowed_roles or str(current_user.role).lower() in allowed_roles:
        return current_user

    logger.warning("Admin role access denied for user: %s (role: %s)", current_user.email, current_user.role)
    raise PermissionDeniedError("Administrator role required for this action.")


class RoleChecker:
    """Callable dependency enforcing dynamic role-based access control (RBAC)."""

    def __init__(self, allowed_roles: Sequence[Union[UserRole, str]]) -> None:
        """Initialize RoleChecker with permitted roles.

        Args:
            allowed_roles: Collection of permitted UserRole values or string names.
        """
        self.allowed_roles = set(allowed_roles)

    def __call__(
        self,
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        """Evaluate whether current_user role is authorized.

        Superusers automatically bypass role checks.

        Args:
            current_user: Active authenticated User entity.

        Returns:
            User entity if role is permitted.

        Raises:
            PermissionDeniedError: 403 Forbidden if user role is not authorized.
        """
        if current_user.is_superuser:
            logger.debug("Role check bypassed for superuser %s", current_user.email)
            return current_user

        user_role = current_user.role
        role_val = user_role.value if hasattr(user_role, "value") else str(user_role)

        if user_role in self.allowed_roles or role_val in self.allowed_roles:
            return current_user

        logger.warning(
            "RBAC Role denied for user %s (role: %s). Allowed roles: %s",
            current_user.email,
            user_role,
            self.allowed_roles,
        )
        raise PermissionDeniedError(
            f"Insufficient privileges. Role '{role_val}' is not authorized for this operation."
        )


def require_roles(*roles: Union[UserRole, str]):
    """FastAPI dependency helper creating a RoleChecker instance.

    Usage:
        @router.get('/admin/dashboard', dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN))])

    Args:
        *roles: Permitted UserRole enums or role string names.

    Returns:
        RoleChecker dependency instance.
    """
    return RoleChecker(allowed_roles=roles)
