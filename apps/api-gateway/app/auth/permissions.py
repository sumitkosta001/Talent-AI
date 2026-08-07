"""Role-Based (RBAC) and Permission-Based (PBAC) Access Control System.

Provides fine-grained permission mappings, role hierarchies, and reusable
FastAPI dependency checkers for route-level and resource-level authorization.
"""

import logging
from typing import Set, Sequence, Union, Dict
from fastapi import Depends

from app.models.enums import UserRole
from app.models.user import User
from app.exceptions.auth import PermissionDeniedError

logger = logging.getLogger("talentai.auth.permissions")

# Default RBAC permission mapping per UserRole
ROLE_PERMISSIONS: Dict[Union[UserRole, str], Set[str]] = {
    UserRole.CANDIDATE: {
        "resume:view",
        "resume:create",
        "resume:update",
        "jobs:view",
        "applications:create",
        "applications:view",
        "users:view",
        "profile:update",
    },
    UserRole.RECRUITER: {
        "jobs:create",
        "jobs:update",
        "jobs:delete",
        "jobs:view",
        "applications:view",
        "applications:update",
        "companies:update",
        "users:view",
        "profile:update",
    },
    UserRole.HIRING_MANAGER: {
        "jobs:create",
        "jobs:update",
        "jobs:delete",
        "jobs:view",
        "applications:view",
        "applications:update",
        "companies:update",
        "users:view",
        "profile:update",
    },
    UserRole.INTERVIEWER: {
        "jobs:view",
        "interviews:view",
        "interviews:update",
        "users:view",
        "profile:update",
    },
    UserRole.ADMIN: {"*"},
    UserRole.SUPER_ADMIN: {"*"},
}


class PermissionChecker:
    """Callable dependency class for enforcing granular route permissions."""

    def __init__(self, required_permissions: Sequence[str]) -> None:
        """Initialize PermissionChecker with required scope strings.

        Args:
            required_permissions: Collection of permission scope strings (e.g. 'jobs:create').
        """
        self.required_permissions = set(required_permissions)

    def check_permissions(self, user: User) -> bool:
        """Evaluate whether a user entity satisfies permission requirements.

        Superusers automatically bypass permission checks.

        Args:
            user: Authenticated User entity.

        Returns:
            True if user possesses required permissions, False otherwise.
        """
        if getattr(user, "is_superuser", False):
            logger.debug("Permission check granted for superuser: %s", user.email)
            return True

        user_role = user.role
        granted_permissions = ROLE_PERMISSIONS.get(user_role, set())

        # Wildcard permission grants unrestricted access
        if "*" in granted_permissions:
            return True

        # Check if all required permissions are covered in user's granted permissions
        has_access = self.required_permissions.issubset(granted_permissions)
        if not has_access:
            logger.warning(
                "Permission denied for user %s (role: %s). Missing permissions from %s",
                user.email,
                user_role,
                self.required_permissions - granted_permissions,
            )
        return has_access

    def __call__(self, user: User) -> User:
        """FastAPI dependency entry point evaluating permission requirements.

        Args:
            user: Authenticated user injected from active user dependency.

        Returns:
            User entity if authorized.

        Raises:
            PermissionDeniedError: 403 Forbidden if user lacks required permissions.
        """
        if not self.check_permissions(user):
            raise PermissionDeniedError(
                f"Required permission scope missing for this action: {', '.join(self.required_permissions)}"
            )
        return user


def require_permissions(*permissions: str):
    """FastAPI dependency helper creating a PermissionChecker for route protection.

    Usage:
        @router.post('/jobs', dependencies=[Depends(require_permissions('jobs:create'))])

    Args:
        *permissions: Permission scope strings.

    Returns:
        PermissionChecker callable dependency instance.
    """
    return PermissionChecker(required_permissions=permissions)
