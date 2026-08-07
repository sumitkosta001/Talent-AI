"""Authentication Dependency Injection Providers.

Yields current authenticated user identity and enforces role authorization checks
for route handlers using `Depends()`. Re-exports core dependencies from `app.auth.dependencies`.
"""

from app.auth.dependencies import (
    bearer_scheme,
    get_current_user,
    get_current_active_user,
    get_current_verified_user,
    get_current_superuser,
    get_current_candidate,
    get_current_company,
    get_current_admin,
    require_roles,
)

__all__ = [
    "bearer_scheme",
    "get_current_user",
    "get_current_active_user",
    "get_current_verified_user",
    "get_current_superuser",
    "get_current_candidate",
    "get_current_company",
    "get_current_admin",
    "require_roles",
]
