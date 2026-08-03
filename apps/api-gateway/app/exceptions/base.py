"""Base Exception for TalentAI Domain Custom Exceptions."""

from typing import Any, Dict, Optional


class TalentAIException(Exception):
    """Base exception for all domain-specific TalentAI errors.
    
    Attributes:
        message: Human-readable error message string.
        status_code: Suggested HTTP status code.
        details: Optional payload with additional error contextual details.
    """

    def __init__(
        self, message: str = "An unexpected error occurred.", status_code: int = 500, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize base exception with message and status code."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
