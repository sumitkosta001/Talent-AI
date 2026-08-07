"""Security Utilities and Authorization Token Parsers.

Extracts bearer tokens from HTTP request headers and coordinates JWT decoding
and claim verification using application settings and security helpers.
"""

import logging
from typing import Dict, Any, Optional

from app.auth.jwt import decode_token, verify_access_token
from app.exceptions.auth import (
    AuthenticationError,
    InvalidTokenError,
    ExpiredTokenError,
    TokenTypeMismatchError,
)

logger = logging.getLogger("talentai.auth.security")


def extract_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """Extract raw JWT bearer token from Authorization header value.

    Args:
        authorization_header: Value of HTTP 'Authorization' header.

    Returns:
        Extracted token string or None if header is missing or malformed.
    """
    if not authorization_header or not authorization_header.strip():
        return None

    parts = authorization_header.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token's signature, structure, and expiration.

    Enforces that the token type claim is strictly 'access'.

    Args:
        token: Raw JWT access token string to decode.

    Returns:
        Decoded payload claims dictionary.

    Raises:
        ExpiredTokenError: If token has passed its expiration limit.
        InvalidTokenError: If token signature, structure, or type is invalid.
        AuthenticationError: For general token validation failures.
    """
    if not token or not isinstance(token, str):
        logger.warning("Failed JWT verification: Empty or non-string token provided.")
        raise InvalidTokenError("Access token must be provided.")

    try:
        payload = verify_access_token(token)
        logger.debug("Successfully validated access token for user sub: %s", payload.get("sub"))
        return payload
    except ExpiredTokenError as exc:
        logger.warning("Failed JWT verification: Expired token presented.")
        raise exc
    except TokenTypeMismatchError as exc:
        logger.warning("Failed JWT verification: Token type mismatch (expected 'access').")
        raise InvalidTokenError("Expected access token, but received refresh token.") from exc
    except InvalidTokenError as exc:
        logger.warning("Failed JWT verification: Invalid token format or signature.")
        raise exc
    except Exception as exc:
        logger.error("Failed JWT verification: Unexpected decoding error: %s", exc)
        raise AuthenticationError("Could not validate authorization token.") from exc
