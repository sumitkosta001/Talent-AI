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


class ResumeNotFoundError(TalentAIException):
    """Raised when a resume document metadata record is not found."""

    def __init__(self, resume_id: str = "") -> None:
        """Initialize resume not found error with 404 status."""
        msg = f"Resume record '{resume_id}' was not found." if resume_id else "Resume record was not found."
        super().__init__(message=msg, status_code=404)


class ResumeStorageObjectNotFoundError(TalentAIException):
    """Raised when the database record exists, but the physical file is missing in object storage."""

    def __init__(self) -> None:
        """Initialize with 404 status."""
        super().__init__(
            message="Resume document file not found in storage.",
            status_code=404,
        )


class ResumeAlreadyCurrentError(TalentAIException):
    """Raised when attempting to restore a resume version that is already current."""

    def __init__(self, resume_id: str = "") -> None:
        """Initialize with 400 status."""
        msg = f"Resume '{resume_id}' is already the current version." if resume_id else "Resume is already the current version."
        super().__init__(message=msg, status_code=400)


class ResumeProcessingConflictError(TalentAIException):
    """Raised when attempting to process/retry a resume that is already currently processing."""

    def __init__(self, resume_id: str = "") -> None:
        """Initialize with 409 Conflict status."""
        msg = f"Resume '{resume_id}' is already being processed." if resume_id else "Resume is already being processed."
        super().__init__(message=msg, status_code=409)


class ResumeAlreadyProcessedError(TalentAIException):
    """Raised when attempting to retry a resume that has already been processed successfully."""

    def __init__(self, resume_id: str = "") -> None:
        """Initialize with 400 status."""
        msg = f"Resume '{resume_id}' has already been processed successfully." if resume_id else "Resume has already been processed successfully."
        super().__init__(message=msg, status_code=400)


class ResumeNotRetryableError(TalentAIException):
    """Raised when attempting to retry a resume that is in an invalid state for retry."""

    def __init__(self, message: str = "Resume is not in a retryable state.") -> None:
        """Initialize with 400 status."""
        super().__init__(message=message, status_code=400)


