"""Authentication Module for TalentAI API Gateway.

Handles JWT encoding/decoding, Argon2 password hashing, security dependencies,
role/permission checkers, and security token rotation protocols.
"""

from app.auth.password import hash_password, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_access_token,
    verify_refresh_token,
)
from app.auth.security import decode_access_token, extract_bearer_token
from app.auth.permissions import PermissionChecker, require_permissions, ROLE_PERMISSIONS
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
    RoleChecker,
)

__all__ = [
    "jwt",
    "oauth",
    "password",
    "permissions",
    "security",
    "tokens",
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "verify_access_token",
    "verify_refresh_token",
    "decode_access_token",
    "extract_bearer_token",
    "PermissionChecker",
    "require_permissions",
    "ROLE_PERMISSIONS",
    "bearer_scheme",
    "get_current_user",
    "get_current_active_user",
    "get_current_verified_user",
    "get_current_superuser",
    "get_current_candidate",
    "get_current_company",
    "get_current_admin",
    "require_roles",
    "RoleChecker",
]
