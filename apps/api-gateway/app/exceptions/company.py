"""Company domain-specific exception types."""

from typing import Any, Dict, Optional
from app.exceptions.base import TalentAIException


class CompanyNotFoundError(TalentAIException):
    """Raised when requested company record is not found or soft-deleted."""

    def __init__(self, message: str = "Company not found.", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=404, details=details)


class CompanyAlreadyExistsError(TalentAIException):
    """Raised when creating a company with a name that already exists."""

    def __init__(self, message: str = "A company with this name already exists.", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=409, details=details)
