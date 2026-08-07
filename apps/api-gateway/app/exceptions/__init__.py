"""Domain Custom Exception Hierarchy Package.

Provides structured, domain-specific exception classes for error handling
and response formatting across the API Gateway.
"""

from .base import TalentAIException
from .auth import (
    AuthenticationError,
    InvalidCredentialsError,
    EmailAlreadyExistsError,
    AccountDisabledError,
    InvalidTokenError,
    ExpiredTokenError,
    TokenExpiredError,
    TokenTypeMismatchError,
    PermissionDeniedError,
)
from .database import EntityNotFoundError, DuplicateEntityError
from .jobs import JobNotFoundError, JobClosedError
from .users import UserNotFoundError, UserInactiveError
from .resume import ResumeParsingError, InvalidFileTypeError

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
    "EntityNotFoundError",
    "DuplicateEntityError",
    "JobNotFoundError",
    "JobClosedError",
    "UserNotFoundError",
    "UserInactiveError",
    "ResumeParsingError",
    "InvalidFileTypeError",
    "auth",
    "database",
    "jobs",
    "users",
    "resume",
]
