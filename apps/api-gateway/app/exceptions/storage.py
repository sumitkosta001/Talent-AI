"""Storage and MinIO Integration Custom Exceptions."""

from app.exceptions.base import TalentAIException


class StorageError(TalentAIException):
    """Base exception for all storage-related errors."""

    def __init__(self, message: str = "Storage operation failed.", status_code: int = 500) -> None:
        """Initialize storage error."""
        super().__init__(message=message, status_code=status_code)


class MinioConnectionError(StorageError):
    """Raised when the application fails to connect to the MinIO server."""

    def __init__(self, message: str = "Failed to connect to object storage.") -> None:
        """Initialize connection error with 500 status."""
        super().__init__(message=message, status_code=500)


class MinioUploadError(StorageError):
    """Raised when file upload to MinIO fails."""

    def __init__(self, message: str = "Failed to store resume. Please try again.") -> None:
        """Initialize upload error with 500 status."""
        super().__init__(message=message, status_code=500)


class MinioDeleteError(StorageError):
    """Raised when file deletion from MinIO fails."""

    def __init__(self, message: str = "Failed to delete file from object storage.") -> None:
        """Initialize delete error with 500 status."""
        super().__init__(message=message, status_code=500)


class MinioBucketError(StorageError):
    """Raised when bucket verification or creation fails."""

    def __init__(self, message: str = "Failed to verify or create storage bucket.") -> None:
        """Initialize bucket error with 500 status."""
        super().__init__(message=message, status_code=500)


class StorageConfigurationError(StorageError):
    """Raised when storage configuration variables are missing or invalid."""

    def __init__(self, message: str = "Storage configuration is invalid.") -> None:
        """Initialize configuration error with 500 status."""
        super().__init__(message=message, status_code=500)
