"""Authentication and Authorization Custom Exceptions."""

from .base import TalentAIException


class AuthenticationError(TalentAIException):
    """Raised when authentication fails (invalid credentials, expired token)."""

    def __init__(self, message: str = "Invalid credentials or expired session.") -> None:
        """Initialize authentication error with 401 status."""
        super().__init__(message=message, status_code=401)


class InvalidCredentialsError(AuthenticationError):
    """Raised when provided email or password during login is incorrect."""

    def __init__(self, message: str = "Invalid email or password.") -> None:
        """Initialize invalid credentials error with 401 status."""
        super().__init__(message=message)


class EmailAlreadyExistsError(TalentAIException):
    """Raised when attempting to register an email address that is already in use."""

    def __init__(self, message: str = "An account with this email address already exists.") -> None:
        """Initialize email already exists error with 409 status."""
        super().__init__(message=message, status_code=409)


class AccountDisabledError(TalentAIException):
    """Raised when an inactive or suspended user attempts to log in."""

    def __init__(self, message: str = "Account has been disabled or suspended.") -> None:
        """Initialize account disabled error with 403 status."""
        super().__init__(message=message, status_code=403)


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


# Alias for ExpiredTokenError for naming flexibility
TokenExpiredError = ExpiredTokenError


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
