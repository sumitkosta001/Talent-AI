"""Authentication Module for TalentAI API Gateway.

Handles JWT encoding/decoding, OAuth2 integration (Google/GitHub), Argon2 password
hashing, role/permission checkers, and security token rotation protocols.
"""

from app.auth.password import hash_password, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_access_token,
    verify_refresh_token,
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
]
