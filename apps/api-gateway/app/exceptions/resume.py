"""Resume Upload and Processing Custom Exceptions."""

from .base import TalentAIException


class ResumeUploadError(TalentAIException):
    """Base exception for resume upload operations."""

    def __init__(self, message: str = "Resume upload failed.", status_code: int = 400) -> None:
        """Initialize resume upload error."""
        super().__init__(message=message, status_code=status_code)


class InvalidFileTypeError(TalentAIException):
    """Raised when uploaded resume file format is unsupported."""

    def __init__(self, message: str = "Unsupported file format. Only PDF and DOCX are allowed.") -> None:
        """Initialize invalid file type error with 400 status."""
        super().__init__(message=message, status_code=400)


class FileTooLargeError(TalentAIException):
    """Raised when uploaded file exceeds the maximum allowed size."""

    def __init__(self, max_size_mb: int = 10) -> None:
        """Initialize file too large error with 413 status."""
        super().__init__(
            message=f"File size exceeds the maximum allowed size of {max_size_mb} MB.",
            status_code=413,
        )


class InvalidFileContentError(TalentAIException):
    """Raised when file content does not match its declared type (magic bytes mismatch)."""

    def __init__(self, message: str = "File content does not match the expected format.") -> None:
        """Initialize invalid file content error with 400 status."""
        super().__init__(message=message, status_code=400)


class UnsafeFilenameError(TalentAIException):
    """Raised when the uploaded filename contains unsafe characters or path traversal attempts."""

    def __init__(self, message: str = "The uploaded filename is invalid or contains unsafe characters.") -> None:
        """Initialize unsafe filename error with 400 status."""
        super().__init__(message=message, status_code=400)


class ResumeParsingError(TalentAIException):
    """Raised when PDF/DOCX resume file extraction fails."""

    def __init__(self, message: str = "Failed to parse resume document content.") -> None:
        """Initialize resume parsing error with 422 status."""
        super().__init__(message=message, status_code=422)


class MissingFileError(TalentAIException):
    """Raised when no file is provided in the upload request."""

    def __init__(self, message: str = "No file was provided. Please upload a PDF or DOCX resume.") -> None:
        """Initialize missing file error with 400 status."""
        super().__init__(message=message, status_code=400)
