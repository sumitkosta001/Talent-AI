"""JWT Encoding, Decoding, and Verification Service.

Provides production-grade JWT generation, claim parsing, signature validation,
and token type checking using PyJWT. This module is the single source of truth for
JSON Web Token operations across the TalentAI platform.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from app.config.settings import settings
from app.exceptions.auth import (
    ExpiredTokenError,
    InvalidTokenError,
    TokenTypeMismatchError,
)


def _generate_jti() -> str:
    """Generate a cryptographically unique JWT ID (jti) claim.

    Returns:
        String representation of a UUID v4.
    """
    return str(uuid.uuid4())


def _current_timestamp() -> int:
    """Get the current UTC POSIX timestamp in seconds.

    Returns:
        Integer seconds since Unix epoch.
    """
    return int(datetime.now(timezone.utc).timestamp())


def _expiration_datetime(delta: timedelta) -> datetime:
    """Calculate future UTC expiration datetime given a time delta.

    Args:
        delta: Timedelta offset from current time.

    Returns:
        Timezone-aware UTC datetime.
    """
    return datetime.now(timezone.utc) + delta


def create_access_token(user_id: str, email: str, role: str) -> str:
    """Generate a signed JWT access token for user authentication.

    Access tokens are short-lived tokens containing user identity, email, and RBAC role
    claims used for authorizing API requests.

    Args:
        user_id: Unique string identifier of the user (UUID).
        email: User's primary email address.
        role: RBAC authorization role string.

    Returns:
        Encoded signed JWT string.

    Raises:
        InvalidTokenError: If encoding fails due to invalid parameters.
    """
    if not user_id or not email or not role:
        raise InvalidTokenError("user_id, email, and role are required to issue an access token.")

    now = datetime.now(timezone.utc)
    expire = _expiration_datetime(timedelta(minutes=settings.jwt.access_token_expire_minutes))

    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "email": str(email),
        "role": str(role),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "jti": _generate_jti(),
    }

    try:
        return jwt.encode(
            payload,
            settings.jwt.secret,
            algorithm=settings.jwt.algorithm,
        )
    except Exception as exc:
        raise InvalidTokenError("Failed to encode access token.") from exc


def create_refresh_token(user_id: str) -> str:
    """Generate a signed JWT refresh token for session renewal.

    Refresh tokens are long-lived tokens containing only subject and session claims.
    Email and role are intentionally excluded to keep refresh tokens minimal.

    Args:
        user_id: Unique string identifier of the user (UUID).

    Returns:
        Encoded signed JWT string.

    Raises:
        InvalidTokenError: If user_id is missing or encoding fails.
    """
    if not user_id:
        raise InvalidTokenError("user_id is required to issue a refresh token.")

    now = datetime.now(timezone.utc)
    expire = _expiration_datetime(timedelta(days=settings.jwt.refresh_token_expire_days))

    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "jti": _generate_jti(),
    }

    try:
        return jwt.encode(
            payload,
            settings.jwt.secret,
            algorithm=settings.jwt.algorithm,
        )
    except Exception as exc:
        raise InvalidTokenError("Failed to encode refresh token.") from exc


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token's signature, structure, and expiration.

    Args:
        token: Raw JWT string to decode and verify.

    Returns:
        Decoded payload dictionary containing claims.

    Raises:
        ExpiredTokenError: If the token has expired (`exp` claim in the past).
        InvalidTokenError: If token signature is invalid, malformed, or unparseable.
    """
    if not token or not isinstance(token, str):
        raise InvalidTokenError("Token string must be provided.")

    try:
        payload = jwt.decode(
            token,
            settings.jwt.secret,
            algorithms=[settings.jwt.algorithm],
            options={"verify_signature": True, "verify_exp": True},
        )
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise ExpiredTokenError("Token has expired.") from exc
    except jwt.PyJWTError as exc:
        raise InvalidTokenError("Invalid token format or signature.") from exc
    except Exception as exc:
        raise InvalidTokenError("Failed to decode token.") from exc


def verify_access_token(token: str) -> Dict[str, Any]:
    """Decode token and verify that it is a valid access token.

    Args:
        token: Raw JWT string to verify.

    Returns:
        Decoded claims dictionary.

    Raises:
        ExpiredTokenError: If the access token is expired.
        TokenTypeMismatchError: If the token type claim is not 'access'.
        InvalidTokenError: If signature or structure is invalid.
    """
    payload = decode_token(token)
    token_type = payload.get("type")

    if token_type != "access":
        raise TokenTypeMismatchError(
            f"Expected token type 'access', but received '{token_type}'."
        )

    return payload


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Decode token and verify that it is a valid refresh token.

    Args:
        token: Raw JWT string to verify.

    Returns:
        Decoded claims dictionary.

    Raises:
        ExpiredTokenError: If the refresh token is expired.
        TokenTypeMismatchError: If the token type claim is not 'refresh'.
        InvalidTokenError: If signature or structure is invalid.
    """
    payload = decode_token(token)
    token_type = payload.get("type")

    if token_type != "refresh":
        raise TokenTypeMismatchError(
            f"Expected token type 'refresh', but received '{token_type}'."
        )

    return payload
