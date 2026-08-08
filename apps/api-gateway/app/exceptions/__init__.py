"""Exception Hierarchy and Custom Domain Error Classes Package.
"""

from app.exceptions.base import TalentAIException
from app.exceptions.auth import (
    AuthenticationError,
    InvalidCredentialsError,
    EmailAlreadyExistsError,
    AccountDisabledError,
    InvalidTokenError,
    ExpiredTokenError,
    TokenExpiredError,
    TokenTypeMismatchError,
    PermissionDeniedError,
    EmailVerificationError,
    VerificationTokenExpiredError,
    VerificationTokenInvalidError,
    EmailSendFailedError,
)
from app.exceptions.users import UserNotFoundError

__all__ = [
    "TalentAIException",
    "AuthenticationError",
    "InvalidCredentialsError",
    "EmailAlreadyExistsError",
    "AccountDisabledError",
    "InvalidTokenError",
    "ExpiredTokenError",
    "TokenExpiredError",
    "TokenTypeMismatchError",
    "PermissionDeniedError",
    "EmailVerificationError",
    "VerificationTokenExpiredError",
    "VerificationTokenInvalidError",
    "EmailSendFailedError",
    "UserNotFoundError",
]
