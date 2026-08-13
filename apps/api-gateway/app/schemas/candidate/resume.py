"""Resume Document Request and Response Pydantic Schemas."""

from datetime import datetime
from typing import Optional
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
    uploaded_at: datetime = Field(description="UTC timestamp when the file was received.")
    created_at: datetime = Field(description="UTC timestamp when the record was created.")


class ResumeUploadResponse(BaseModel):
    """Wrapper response for successful resume upload."""

    success: bool = Field(default=True, description="Upload operation success indicator.")
    message: str = Field(default="Resume uploaded successfully.", description="Human-readable result message.")
    resume: ResumeResponse = Field(description="Uploaded resume metadata.")
