"""Database Domain Custom Exceptions.

Defines custom exception hierarchy for database connection, query, transaction,
and integrity failures across TalentAI API Gateway.
"""

from typing import Any, Dict, Optional
from app.exceptions.base import TalentAIException


class DatabaseError(TalentAIException):
    """Base exception for all database operational failures."""

    def __init__(
        self,
        message: str = "Database error occurred.",
        status_code: int = 500,
        error_code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize database exception with status code and error code."""
        super().__init__(message=message, status_code=status_code, details=details)
        self.error_code = error_code


class DatabaseConnectionError(DatabaseError):
    """Raised when establishing a connection to PostgreSQL server fails."""

    def __init__(self, message: str = "Failed to connect to database server.") -> None:
        """Initialize connection error with 503 status code."""
        super().__init__(message=message, status_code=503, error_code="DATABASE_CONNECTION_ERROR")


class DatabaseNotAvailableError(DatabaseError):
    """Raised when database engine or service is completely unreachable."""

    def __init__(self, message: str = "Database service is currently unavailable.") -> None:
        """Initialize unavailable error with 503 status code."""
        super().__init__(message=message, status_code=503, error_code="DATABASE_NOT_AVAILABLE")


class DatabaseTransactionError(DatabaseError):
    """Raised when a commit, rollback, or flush transaction fails."""

    def __init__(self, message: str = "Database transaction failed.") -> None:
        """Initialize transaction error with 500 status code."""
        super().__init__(message=message, status_code=500, error_code="DATABASE_TRANSACTION_ERROR")


class DatabaseQueryError(DatabaseError):
    """Raised when executing a query statement fails."""

    def __init__(self, message: str = "Failed to execute database query.") -> None:
        """Initialize query error with 500 status code."""
        super().__init__(message=message, status_code=500, error_code="DATABASE_QUERY_ERROR")


class DatabaseTimeoutError(DatabaseError):
    """Raised when query or connection pool times out."""

    def __init__(self, message: str = "Database query operation timed out.") -> None:
        """Initialize timeout error with 504 status code."""
        super().__init__(message=message, status_code=504, error_code="DATABASE_TIMEOUT_ERROR")


class DatabaseIntegrityError(DatabaseError):
    """Raised when unique constraint, foreign key, or check constraint is violated."""

    def __init__(self, message: str = "Database constraint integrity violation.") -> None:
        """Initialize integrity error with 409 status code."""
        super().__init__(message=message, status_code=409, error_code="DATABASE_INTEGRITY_ERROR")


class EntityNotFoundError(DatabaseError):
    """Raised when a requested database record is not found."""

    def __init__(self, entity_name: str = "Record", entity_id: Any = "") -> None:
        """Initialize entity not found error with 404 status code."""
        msg = f"{entity_name} with ID '{entity_id}' was not found." if entity_id else f"{entity_name} not found."
        super().__init__(message=msg, status_code=404, error_code="ENTITY_NOT_FOUND")


class DuplicateEntityError(DatabaseError):
    """Raised when unique constraint is violated (e.g. duplicate email)."""

    def __init__(self, message: str = "A record with these details already exists.") -> None:
        """Initialize duplicate entity error with 409 status code."""
        super().__init__(message=message, status_code=409, error_code="DUPLICATE_ENTITY_ERROR")
