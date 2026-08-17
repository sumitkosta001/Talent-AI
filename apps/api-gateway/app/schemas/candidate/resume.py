"""Resume Document Request and Response Pydantic Schemas."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ResumeResponse(BaseModel):
    """Response DTO exposing safe resume metadata after upload.

    Does NOT expose:
        - stored_filename (internal object key for MinIO)
        - database credentials or internal paths
        - authentication tokens
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Unique resume record identifier.")
    candidate_profile_id: UUID = Field(description="Owning candidate profile identifier.")
    original_filename: str = Field(description="Sanitized original filename from client.")
    mime_type: str = Field(description="Validated MIME type of the uploaded file.")
    file_extension: str = Field(description="Normalized lowercase file extension.")
    file_size_bytes: int = Field(description="Actual file size in bytes.")
    status: str = Field(description="Current processing lifecycle status.")
    version: int = Field(description="Resume version number.")
    is_current: bool = Field(description="Whether this is the active resume.")
    storage_provider: Optional[str] = Field(None, description="Storage provider name.")
    bucket_name: Optional[str] = Field(None, description="S3 bucket name.")
    object_key: Optional[str] = Field(None, description="S3 object key.")
    uploaded_at: datetime = Field(description="UTC timestamp when the file was received.")
    processing_started_at: Optional[datetime] = Field(None, description="UTC timestamp when resume processing/parsing started.")
    processing_completed_at: Optional[datetime] = Field(None, description="UTC timestamp when resume processing/parsing completed.")
    failure_reason: Optional[str] = Field(None, description="Failure reason message if processing failed.")
    created_at: datetime = Field(description="UTC timestamp when the record was created.")


class ResumeUploadResponse(BaseModel):
    """Wrapper response for successful resume upload."""

    success: bool = Field(default=True, description="Upload operation success indicator.")
    message: str = Field(default="Resume uploaded successfully.", description="Human-readable result message.")
    resume: ResumeResponse = Field(description="Uploaded resume metadata.")


class PaginatedResumeResponse(BaseModel):
    """Paginated response containing a list of resumes and metadata."""

    items: List[ResumeResponse] = Field(description="List of resume metadata records.")
    total: int = Field(description="Total number of matching resume records.")
    page: int = Field(description="Current page number.")
    page_size: int = Field(description="Number of items per page.")
    total_pages: int = Field(description="Total number of pages available.")
    has_next: bool = Field(description="Whether there is a next page.")
    has_previous: bool = Field(description="Whether there is a previous page.")


class ResumeRestoreResponse(BaseModel):
    """Response DTO for resume version restore operation."""

    success: bool = Field(default=True, description="Restore operation success indicator.")
    message: str = Field(default="Resume version restored successfully.", description="Human-readable result message.")
    resume: ResumeResponse = Field(description="Restored resume metadata.")


class ResumeProcessingResponse(BaseModel):
    """Response DTO for resume processing and retry operations."""

    success: bool = Field(default=True, description="Processing operation success indicator.")
    message: str = Field(default="Resume processing initiated.", description="Human-readable result message.")
    resume: ResumeResponse = Field(description="Processed resume metadata.")


