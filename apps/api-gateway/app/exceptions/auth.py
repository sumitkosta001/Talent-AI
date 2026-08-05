"""Authentication and Authorization Custom Exceptions."""

from .base import TalentAIException


class AuthenticationError(TalentAIException):
    """Raised when authentication fails (invalid credentials, expired token)."""

    def __init__(self, message: str = "Invalid credentials or expired session.") -> None:
        """Initialize authentication error with 401 status."""
        super().__init__(message=message, status_code=401)


class InvalidTokenError(AuthenticationError):
    """Raised when a JWT token signature or claim is invalid."""

    def __init__(self, message: str = "Malformed or signature-invalid token.") -> None:
        """Initialize invalid token error."""
        super().__init__(message=message)


class ExpiredTokenError(AuthenticationError):
    """Raised when a JWT token has expired."""

    def __init__(self, message: str = "Token has expired.") -> None:
        """Initialize expired token error."""
        super().__init__(message=message)


class TokenTypeMismatchError(AuthenticationError):
    """Raised when a token type (access vs refresh) does not match expectation."""

    def __init__(self, message: str = "Invalid token type for requested action.") -> None:
        """Initialize token type mismatch error."""
        super().__init__(message=message)


class PermissionDeniedError(TalentAIException):
    """Raised when user lacks required role/permission scope."""

    def __init__(self, message: str = "Insufficient permissions for requested action.") -> None:
        """Initialize permission denied error with 403 status."""
        super().__init__(message=message, status_code=403)
