"""Resume Parsing and ATS Processing Custom Exceptions."""

from .base import TalentAIException


class ResumeParsingError(TalentAIException):
    """Raised when PDF/DOCX resume file extraction fails."""

    def __init__(self, message: str = "Failed to parse resume document content.") -> None:
        """Initialize resume parsing error with 422 status."""
        super().__init__(message=message, status_code=422)


class InvalidFileTypeError(TalentAIException):
    """Raised when uploaded resume file format is unsupported."""

    def __init__(self, message: str = "Unsupported file format. Only PDF and DOCX are allowed.") -> None:
        """Initialize invalid file type error with 400 status."""
        super().__init__(message=message, status_code=400)
