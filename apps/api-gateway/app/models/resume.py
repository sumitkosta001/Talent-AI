"""Resume Document SQLAlchemy 2.0 ORM Entity Model.

Stores metadata for uploaded candidate resume files (PDF/DOCX).
Actual file content will be stored in MinIO object storage (Day 12+).
This model captures ownership, validation metadata, processing status,
and versioning information needed across the resume lifecycle.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel
from app.models.enums import ResumeStatus

if TYPE_CHECKING:
    from app.models.candidate_profile import CandidateProfile


class Resume(BaseModel):
    """Resume document metadata entity linked to a CandidateProfile.

    Each resume record tracks:
        - File identification (original + stored filenames, extension, MIME type)
        - Validation metadata (file size, content type verification)
        - Processing lifecycle (status: uploaded → processing → processed/failed)
        - Version management (version number, is_current flag)

    Ownership chain:
        User → CandidateProfile → Resume

    The candidate_profile_id foreign key ensures resumes are cascade-deleted
    when the parent candidate profile is removed.

    Attributes:
        candidate_profile_id: FK to candidate_profiles.id (CASCADE delete).
        original_filename:    Client-provided filename after sanitization.
        stored_filename:      Secure UUID-based filename for object storage.
        mime_type:            Validated MIME type (application/pdf or DOCX MIME).
        file_extension:       Normalized lowercase extension (.pdf or .docx).
        file_size_bytes:      Actual file size in bytes after upload.
        status:               Processing lifecycle status (ResumeStatus enum).
        version:              Monotonically increasing version number.
        is_current:           Whether this is the candidate's active resume.
        uploaded_at:          UTC timestamp when the file was received.

    Inherited from BaseModel:
        id, created_at, updated_at, is_deleted, deleted_at, created_by, updated_by
    """

    __tablename__ = "candidate_resumes"

    candidate_profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key referencing candidate_profiles.id (many-to-one).",
    )

    original_filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="Sanitized original filename provided by the client.",
    )

    stored_filename: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        unique=True,
        doc="Secure UUID-based filename for MinIO/object storage. Format: {uuid}.{ext}",
    )

    mime_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Validated MIME type of the uploaded file.",
    )

    file_extension: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        doc="Normalized lowercase file extension including dot (e.g., '.pdf', '.docx').",
    )

    file_size_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Actual file size in bytes.",
    )

    status: Mapped[ResumeStatus] = mapped_column(
        PG_ENUM(
            ResumeStatus,
            name="resumestatus",
            create_constraint=False,
            native_enum=True,
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=False,
        default=ResumeStatus.UPLOADED,
        server_default=text("'uploaded'"),
        doc="Current processing lifecycle status of the resume.",
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default=text("1"),
        doc="Monotonically increasing version number for resume re-uploads.",
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=True,
        server_default=text("true"),
        doc="Whether this resume is the candidate's currently active resume.",
    )

    storage_provider: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default="minio",
        server_default=text("'minio'"),
        doc="Storage provider name (e.g., 'minio').",
    )

    bucket_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default="talentai-resumes",
        server_default=text("'talentai-resumes'"),
        doc="S3 bucket name where the file is stored.",
    )

    object_key: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        unique=True,
        doc="S3 object key for the stored resume file.",
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
        doc="UTC timestamp when the resume file was received by the server.",
    )

    processing_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="UTC timestamp when resume processing/parsing started.",
    )

    processing_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="UTC timestamp when resume processing/parsing completed.",
    )

    failure_reason: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
        doc="Safe human-readable failure reason message if processing failed.",
    )



    # ======================================================================
    # RELATIONSHIPS
    # ======================================================================

    candidate_profile: Mapped["CandidateProfile"] = relationship(
        "CandidateProfile",
        back_populates="resumes",
    )

    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return (
            f"<Resume("
            f"id={self.id!r}, "
            f"candidate_profile_id={self.candidate_profile_id!r}, "
            f"original_filename={self.original_filename!r}, "
            f"status={self.status.value!r}, "
            f"version={self.version!r}, "
            f"is_current={self.is_current!r}"
            f")>"
        )
