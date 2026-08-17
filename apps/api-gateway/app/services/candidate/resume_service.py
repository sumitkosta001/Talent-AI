"""Resume Upload Business Logic Service.

Handles file validation, filename sanitization, metadata creation,
and orchestrates the resume upload workflow for Day 11.

Extended in Day 16 with versioning, restore, and auto-promotion logic.
"""

import logging
import re
import unicodedata
import urllib.parse
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath, PureWindowsPath
from typing import Optional
from uuid import UUID
import io

from fastapi import UploadFile

from app.config.settings import settings
from app.models.enums import ResumeStatus
from app.models.resume import Resume
from app.repositories.candidate.profile_repository import CandidateProfileRepository
from app.repositories.candidate.resume_repository import ResumeRepository
from app.services.storage.minio_service import MinioStorageService
from app.exceptions.resume import (
    InvalidFileTypeError,
    FileTooLargeError,
    InvalidFileContentError,
    UnsafeFilenameError,
    MissingFileError,
    ResumeNotFoundError,
    ResumeStorageObjectNotFoundError,
    ResumeAlreadyCurrentError,
    ResumeProcessingConflictError,
    ResumeAlreadyProcessedError,
    ResumeNotRetryableError,
)
from app.exceptions.candidate import CandidateProfileNotFoundError
from app.exceptions.storage import StorageError, MinioDeleteError

logger = logging.getLogger("talentai.services.resume")

# ======================================================================
# FILE SIGNATURE CONSTANTS
# ======================================================================

# PDF files start with %PDF-
PDF_MAGIC_BYTES = b"%PDF-"

# DOCX files are ZIP archives — ZIP magic bytes: PK\x03\x04
DOCX_MAGIC_BYTES = b"PK\x03\x04"

# MIME type mapping for allowed types
ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}

# Windows reserved device names
WINDOWS_RESERVED_NAMES = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
})

# Maximum original filename length after sanitization
MAX_FILENAME_LENGTH = 255


class ResumeService:
    """Service encapsulating resume upload validation and metadata persistence.

    Responsibilities:
        1. Validate authenticated candidate context
        2. Validate uploaded file (size, extension, MIME, content signature)
        3. Sanitize original filename
        4. Generate secure internal storage identifier
        5. Create and persist Resume database record
        6. Return created Resume entity
        7. Version management (version generation, current-version swaps)
        8. Restore previous version as current
        9. Auto-promote on delete
    """

    def __init__(
        self,
        profile_repo: CandidateProfileRepository,
        resume_repo: ResumeRepository,
        storage_service: Optional[MinioStorageService] = None,
    ) -> None:
        self.profile_repo = profile_repo
        self.resume_repo = resume_repo
        self.storage_service = storage_service if storage_service is not None else MinioStorageService()

    async def upload_resume(self, user_id: UUID | str, file: UploadFile) -> Resume:
        """Orchestrate the full resume upload workflow with concurrency-safe versioning.

        Uses FOR UPDATE locking on the candidate profile row to serialize
        concurrent version generation for the same candidate.
        """
        # 1. Get or create candidate profile
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        # 2. Validate file presence
        if not file or not file.filename:
            raise MissingFileError()

        # 3. Read file content (needed for size and content validation)
        content = await file.read()
        await file.seek(0)  # Reset for potential future use

        # 4. Validate file size
        file_size = len(content)
        self._validate_file_size(file_size)

        # 5. Validate and normalize extension
        extension = self._validate_extension(file.filename)

        # 6. Validate MIME type
        mime_type = self._validate_mime_type(file.content_type, extension)

        # 7. Validate file content/signature
        self._validate_file_content(content, extension)

        # 8. Sanitize original filename
        safe_original_filename = self._sanitize_filename(file.filename)

        # 9. Generate secure internal identifier
        resume_uuid = uuid.uuid4()
        stored_filename = f"{resume_uuid}{extension}"
        object_key = f"candidates/{profile.id}/resumes/{resume_uuid}/resume{extension}"
        bucket_name = settings.minio.bucket

        # 10. Upload file to MinIO
        try:
            logger.info("Uploading resume to MinIO: bucket=%s, key=%s", bucket_name, object_key)
            self.storage_service.upload_object(
                bucket_name=bucket_name,
                object_key=object_key,
                data=io.BytesIO(content),
                length=file_size,
                content_type=mime_type,
                metadata={
                    "original-filename": urllib.parse.quote(safe_original_filename),
                    "candidate-profile-id": str(profile.id),
                    "resume-id": str(resume_uuid),
                }
            )
        except Exception as e:
            logger.error("MinIO upload failed for user %s: %s", user_id, str(e))
            raise

        # 11. Atomic version generation with concurrency protection
        try:
            # Lock candidate profile row to serialize concurrent uploads
            current_max_version = await self.resume_repo.get_max_version_locked(profile.id)
            new_version = current_max_version + 1

            # 12. Mark existing resumes as not current (within same transaction)
            await self.resume_repo.mark_all_not_current_no_commit(profile.id)

            # 13. Create Resume entity
            resume = Resume(
                id=resume_uuid,
                candidate_profile_id=profile.id,
                original_filename=safe_original_filename,
                stored_filename=stored_filename,
                mime_type=mime_type,
                file_extension=extension,
                file_size_bytes=file_size,
                status=ResumeStatus.UPLOADED,
                version=new_version,
                is_current=True,
                storage_provider="minio",
                bucket_name=bucket_name,
                object_key=object_key,
                uploaded_at=datetime.now(timezone.utc),
            )

            # 14. Persist to database (single atomic commit)
            resume = await self.resume_repo.create(resume)

            logger.info(
                "Resume uploaded successfully: user=%s, profile=%s, resume=%s, filename=%s, version=%d, size=%d bytes",
                user_id, profile.id, resume.id, safe_original_filename, new_version, file_size,
            )

            return resume

        except Exception as db_exc:
            logger.error("Database operation failed after MinIO upload. Performing cleanup for object_key=%s", object_key)
            try:
                self.storage_service.delete_object(bucket_name, object_key)
                logger.info("Successfully cleaned up orphan MinIO object_key=%s", object_key)
            except Exception as cleanup_exc:
                logger.critical("FAILED to clean up orphan MinIO object_key=%s: %s", object_key, str(cleanup_exc))
            raise db_exc

    async def list_resumes(
        self,
        user_id: UUID | str,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "uploaded_at",
        sort_order: str = "desc",
    ) -> dict:
        """Resolve candidate profile, validate parameters, and fetch a paginated list of resumes."""
        # 1. Resolve candidate profile
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        # 2. Parameter validations
        if page < 1:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Page number must be greater than or equal to 1.")
        if page_size < 1 or page_size > 50:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Page size must be between 1 and 50.")
        if sort_by not in ["uploaded_at", "file_size_bytes", "status", "original_filename", "version"]:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail=f"Invalid sort field '{sort_by}'.")
        if sort_order not in ["asc", "desc"]:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Sort order must be 'asc' or 'desc'.")

        # 3. Calculate database offset
        offset = (page - 1) * page_size

        # 4. Query paginated items and total matching count
        items = await self.resume_repo.list_by_profile_id_paginated(
            profile_id=profile.id,
            offset=offset,
            limit=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        total = await self.resume_repo.count_by_profile_id(profile.id)

        # 5. Calculate total pages and navigation bounds
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        has_next = page < total_pages
        has_previous = page > 1

        logger.info(
            "Listed resumes for user %s: profile=%s, page=%d, page_size=%d, total=%d",
            user_id, profile.id, page, page_size, total
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_previous": has_previous,
        }

    async def get_resume_metadata(self, user_id: UUID | str, resume_id: UUID | str) -> Resume:
        """Resolve candidate profile and securely retrieve target resume metadata.

        Enforces candidate ownership and active (non-deleted) status check.
        """
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        resume = await self.resume_repo.get_by_id_for_profile(resume_id, profile.id)
        if not resume:
            raise ResumeNotFoundError(str(resume_id))

        return resume

    async def get_resume_file_stream(self, user_id: UUID | str, resume_id: UUID | str):
        """Securely fetch the target resume's physical file stream from MinIO.

        Validates candidate ownership, deleted flag, and storage object integrity.
        Works for both current and previous (non-deleted) resume versions.
        """
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        resume = await self.resume_repo.get_by_id_for_profile(resume_id, profile.id)
        if not resume:
            raise ResumeNotFoundError(str(resume_id))

        if not resume.bucket_name or not resume.object_key:
            logger.warning("Resume record %s exists but lacks bucket_name or object_key references.", resume_id)
            raise ResumeStorageObjectNotFoundError()

        if not self.storage_service.object_exists(resume.bucket_name, resume.object_key):
            logger.warning("Resume file missing in MinIO: bucket=%s, key=%s", resume.bucket_name, resume.object_key)
            raise ResumeStorageObjectNotFoundError()

        try:
            stream = self.storage_service.get_object(resume.bucket_name, resume.object_key)
            return resume, stream
        except Exception as e:
            logger.error("Failed to retrieve resume object from MinIO for resume %s: %s", resume_id, str(e))
            raise StorageError("Failed to retrieve file from storage.")

    async def get_current_resume(self, user_id: UUID | str) -> Resume:
        """Get the candidate's current (active) resume version.

        Raises:
            CandidateProfileNotFoundError: If no profile exists.
            ResumeNotFoundError: If no current resume exists.
        """
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        resume = await self.resume_repo.get_current_for_profile(profile.id)
        if not resume:
            raise ResumeNotFoundError()

        return resume

    async def restore_resume_version(self, user_id: UUID | str, resume_id: UUID | str) -> Resume:
        """Restore a previous resume version as the current version.

        Atomically swaps is_current flags within a single transaction:
        1. Verify candidate ownership
        2. Verify resume exists and is not deleted
        3. Check resume is not already current (raises 400)
        4. Set all active candidate resumes to is_current=False
        5. Set target resume to is_current=True
        6. Commit transaction

        Args:
            user_id: Authenticated user ID.
            resume_id: ID of the resume version to restore.

        Returns:
            The restored Resume entity.

        Raises:
            CandidateProfileNotFoundError: If no profile exists.
            ResumeNotFoundError: If resume doesn't exist, is deleted, or belongs to another candidate.
            ResumeAlreadyCurrentError: If resume is already the current version.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        if isinstance(resume_id, str):
            resume_id = UUID(resume_id)

        # 1. Resolve candidate profile
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        # 2. Get active resume (ownership & non-deleted check)
        resume = await self.resume_repo.get_by_id_for_profile(resume_id, profile.id)
        if not resume:
            raise ResumeNotFoundError(str(resume_id))

        # 3. Check if already current
        if resume.is_current:
            raise ResumeAlreadyCurrentError(str(resume_id))

        # 4. Atomic swap: mark all not current, then set target as current
        try:
            await self.resume_repo.mark_all_not_current_no_commit(profile.id)
            resume.is_current = True
            await self.resume_repo.db.commit()
            await self.resume_repo.db.refresh(resume)

            logger.info(
                "Resume version restored: user=%s, profile=%s, resume=%s, version=%d",
                user_id, profile.id, resume_id, resume.version,
            )
            return resume

        except Exception:
            await self.resume_repo.db.rollback()
            raise

    async def get_resume_history(
        self,
        user_id: UUID | str,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "uploaded_at",
        sort_order: str = "desc",
    ) -> dict:
        """Fetch upload and processing history for the authenticated candidate.

        Defaults to newest upload first (uploaded_at desc, id desc).
        """
        return await self.list_resumes(
            user_id=user_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def process_resume(
        self,
        user_id: UUID | str,
        resume_id: UUID | str,
        simulate_failure: Optional[str] = None,
    ) -> Resume:
        """Process an uploaded resume document through the processing lifecycle.

        Transitions: UPLOADED -> PROCESSING -> PROCESSED (or FAILED).
        Uses row-level locking to prevent concurrent double-processing.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        if isinstance(resume_id, str):
            resume_id = UUID(resume_id)

        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        resume = await self.resume_repo.get_by_id_for_profile_locked(resume_id, profile.id)
        if not resume:
            raise ResumeNotFoundError(str(resume_id))

        if resume.status == ResumeStatus.PROCESSING:
            raise ResumeProcessingConflictError(str(resume_id))
        if resume.status == ResumeStatus.PROCESSED:
            raise ResumeAlreadyProcessedError(str(resume_id))

        return await self._execute_processing(resume, profile, simulate_failure)

    async def retry_resume_processing(
        self,
        user_id: UUID | str,
        resume_id: UUID | str,
        simulate_failure: Optional[str] = None,
    ) -> Resume:
        """Retry processing a failed resume document.

        Transitions: FAILED -> PROCESSING -> PROCESSED (or FAILED).
        Uses row-level locking to prevent concurrent duplicate retries.

        Crucially preserves:
            - Same resume database ID
            - Same version number
            - Same is_current status
            - Same MinIO storage object key
            - Does NOT create a new version or new MinIO object
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        if isinstance(resume_id, str):
            resume_id = UUID(resume_id)

        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        resume = await self.resume_repo.get_by_id_for_profile_locked(resume_id, profile.id)
        if not resume:
            raise ResumeNotFoundError(str(resume_id))

        if resume.status == ResumeStatus.PROCESSING:
            raise ResumeProcessingConflictError(str(resume_id))
        if resume.status == ResumeStatus.PROCESSED:
            raise ResumeAlreadyProcessedError(str(resume_id))

        return await self._execute_processing(resume, profile, simulate_failure)

    async def _execute_processing(
        self,
        resume: Resume,
        profile,
        simulate_failure: Optional[str] = None,
    ) -> Resume:
        """Internal lifecycle executor for processing/retrying a resume document."""
        # 1. Transition to PROCESSING state and clear failure reason
        resume.status = ResumeStatus.PROCESSING
        resume.processing_started_at = datetime.now(timezone.utc)
        resume.failure_reason = None
        await self.resume_repo.db.commit()
        await self.resume_repo.db.refresh(resume)

        logger.info(
            "Resume processing started: user=%s, profile=%s, resume=%s, version=%d",
            profile.user_id, profile.id, resume.id, resume.version,
        )

        # 2. Perform processing verification
        try:
            if simulate_failure:
                raise Exception(simulate_failure)

            # Check MinIO storage object exists
            if not resume.bucket_name or not resume.object_key:
                raise Exception("Storage location reference missing.")

            if not self.storage_service.object_exists(resume.bucket_name, resume.object_key):
                raise Exception("Resume document file not found in storage.")

            # Validate object stream can be read
            stream = self.storage_service.get_object(resume.bucket_name, resume.object_key)
            data = stream.read(1024)
            stream.close()
            stream.release_conn()

            if not data:
                raise Exception("Uploaded document is empty.")

            # Transition to PROCESSED on success
            resume.status = ResumeStatus.PROCESSED
            resume.processing_completed_at = datetime.now(timezone.utc)
            resume.failure_reason = None
            await self.resume_repo.db.commit()
            await self.resume_repo.db.refresh(resume)

            logger.info(
                "Resume processing completed successfully: profile=%s, resume=%s, version=%d",
                profile.id, resume.id, resume.version,
            )
            return resume

        except Exception as exc:
            # Safe failure reason sanitization (prevent leaking credentials, stack traces)
            raw_msg = str(exc)
            safe_msg = self._sanitize_failure_reason(raw_msg)

            resume.status = ResumeStatus.FAILED
            resume.failure_reason = safe_msg
            resume.processing_completed_at = None
            await self.resume_repo.db.commit()
            await self.resume_repo.db.refresh(resume)

            logger.warning(
                "Resume processing failed: profile=%s, resume=%s, version=%d, reason='%s'",
                profile.id, resume.id, resume.version, safe_msg,
            )
            return resume

    def _sanitize_failure_reason(self, msg: str) -> str:
        """Sanitize error messages to ensure no infrastructure secrets or stack traces leak."""
        sensitive_patterns = [
            "password", "secret", "token", "postgres", "neon", "aws", "minio-admin", "key="
        ]
        lower = msg.lower()
        for pat in sensitive_patterns:
            if pat in lower:
                return "Resume processing failed due to an internal system error."

        if len(msg) > 500:
            return msg[:497] + "..."
        return msg if msg.strip() else "Resume processing failed."

    async def delete_resume(self, user_id: UUID | str, resume_id: UUID | str) -> dict:
        """Resolve candidate profile, verify ownership, delete S3 object, soft-delete DB record,
        and auto-promote the highest remaining active version if the deleted resume was current.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        if isinstance(resume_id, str):
            resume_id = UUID(resume_id)

        # 1. Resolve candidate profile
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise CandidateProfileNotFoundError()

        # 2. Get active resume (ownership & non-deleted check are performed by get_by_id_for_profile)
        resume = await self.resume_repo.get_by_id_for_profile(resume_id, profile.id)
        if not resume:
            raise ResumeNotFoundError(str(resume_id))

        was_current = resume.is_current
        bucket_name = resume.bucket_name
        object_key = resume.object_key
        original_filename = resume.original_filename
        profile_id_str = str(profile.id)
        resume_id_str = str(resume_id)

        # 3. Read & preserve file data/metadata in memory before deletion (for database compensation)
        content = None
        content_type = resume.mime_type
        if bucket_name and object_key:
            try:
                # Read content from MinIO
                stream = self.storage_service.get_object(bucket_name, object_key)
                content = stream.read()
                stream.close()
                stream.release_conn()
            except Exception as read_exc:
                logger.warning("Could not read object content for rollback backup: %s", str(read_exc))

        # 4. Delete physical file from MinIO
        if bucket_name and object_key:
            try:
                logger.info("Deleting S3 object for resume %s: bucket=%s, key=%s", resume_id, bucket_name, object_key)
                self.storage_service.delete_object(bucket_name, object_key)
            except Exception as storage_exc:
                logger.error("MinIO object deletion failed for resume %s: %s", resume_id, str(storage_exc))
                raise MinioDeleteError(f"Failed to delete file from object storage: {str(storage_exc)}")

        # 5. Soft-delete database record and auto-promote if needed
        try:
            await self.resume_repo.delete_no_commit(resume)

            # 6. Auto-promote highest remaining active version if deleted resume was current
            if was_current:
                next_current = await self.resume_repo.get_highest_active_resume(
                    profile.id, exclude_id=resume_id
                )
                if next_current:
                    next_current.is_current = True
                    logger.info(
                        "Auto-promoted version %d as current after deleting version %d",
                        next_current.version, resume.version,
                    )

            await self.resume_repo.db.commit()

            logger.info("Resume successfully deleted: profile=%s, resume=%s", profile.id, resume_id)
            return {
                "success": True,
                "message": "Resume deleted successfully",
                "resume_id": str(resume_id),
            }
        except Exception as db_exc:
            logger.error("Database deletion failed for resume %s: %s. Initiating S3 rollback.", resume_id, str(db_exc))
            await self.resume_repo.db.rollback()
            # Rollback S3 deletion by re-uploading content if we backed it up successfully
            if bucket_name and object_key and content:
                try:
                    self.storage_service.upload_object(
                        bucket_name=bucket_name,
                        object_key=object_key,
                        data=io.BytesIO(content),
                        length=len(content),
                        content_type=content_type,
                        metadata={
                            "original-filename": urllib.parse.quote(original_filename),
                            "candidate-profile-id": profile_id_str,
                            "resume-id": resume_id_str,
                        }
                    )
                    logger.info("Successfully restored S3 object after DB deletion failure for key=%s", object_key)
                except Exception as restore_exc:
                    logger.critical("FAILED to restore S3 object key=%s after DB deletion failure: %s", object_key, str(restore_exc))
            raise db_exc

    # ==================================================================
    # VALIDATION METHODS
    # ==================================================================

    def _validate_file_size(self, file_size: int) -> None:
        """Validate file size against configured maximum."""
        max_bytes = settings.resume.max_resume_size_bytes
        if file_size > max_bytes:
            logger.warning(
                "File size %d bytes exceeds maximum %d bytes (%d MB).",
                file_size, max_bytes, settings.resume.max_resume_size_mb,
            )
            raise FileTooLargeError(max_size_mb=settings.resume.max_resume_size_mb)

        if file_size == 0:
            raise InvalidFileContentError("The uploaded file is empty.")

    def _validate_extension(self, filename: str) -> str:
        """Validate and normalize file extension.

        Rejects double-extension attacks (e.g., resume.pdf.exe).
        """
        if not filename:
            raise InvalidFileTypeError("Filename is missing.")

        # Extract all suffixes to detect double-extension attacks
        path = PurePosixPath(filename)
        suffixes = path.suffixes

        if len(suffixes) > 1:
            last_ext = suffixes[-1].lower()
            dangerous_extensions = {
                ".exe", ".bat", ".cmd", ".com", ".msi", ".scr", ".pif", ".vbs",
                ".js", ".ws", ".wsf", ".ps1", ".sh", ".bash", ".cgi", ".pl",
                ".py", ".rb", ".php", ".html", ".htm", ".svg", ".xml",
            }
            if last_ext in dangerous_extensions:
                logger.warning("Double extension attack detected: %s", filename)
                raise InvalidFileTypeError(
                    f"Double file extension detected. '{filename}' is not allowed."
                )

        extension = suffixes[-1].lower() if suffixes else ""

        allowed = settings.resume.allowed_extensions_list
        if extension not in allowed:
            raise InvalidFileTypeError(
                f"File extension '{extension}' is not supported. Allowed: {', '.join(allowed)}"
            )

        return extension

    def _validate_mime_type(self, content_type: Optional[str], extension: str) -> str:
        """Validate MIME type against allowed types and cross-check with extension."""
        if not content_type:
            raise InvalidFileTypeError("File MIME type could not be determined.")

        mime = content_type.split(";")[0].strip().lower()

        allowed = settings.resume.allowed_mime_types_list
        if mime not in allowed:
            raise InvalidFileTypeError(
                f"MIME type '{mime}' is not supported. Allowed types: {', '.join(allowed)}"
            )

        expected_ext = ALLOWED_MIME_TYPES.get(mime)
        if expected_ext and expected_ext != extension:
            raise InvalidFileTypeError(
                f"MIME type '{mime}' does not match file extension '{extension}'."
            )

        return mime

    def _validate_file_content(self, content: bytes, extension: str) -> None:
        """Validate file content by checking magic bytes / file signature."""
        if not content:
            raise InvalidFileContentError("The uploaded file is empty.")

        if extension == ".pdf":
            header = content[:1024]
            if PDF_MAGIC_BYTES not in header:
                logger.warning("PDF magic bytes not found in file header.")
                raise InvalidFileContentError(
                    "The uploaded file does not appear to be a valid PDF document."
                )

        elif extension == ".docx":
            if not content[:4].startswith(DOCX_MAGIC_BYTES):
                logger.warning("DOCX/ZIP magic bytes not found in file header.")
                raise InvalidFileContentError(
                    "The uploaded file does not appear to be a valid DOCX document."
                )

    # ==================================================================
    # FILENAME SANITIZATION
    # ==================================================================

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize the original filename for safe metadata storage."""
        if not filename:
            raise UnsafeFilenameError("Filename is empty.")

        # 1. Remove null bytes
        sanitized = filename.replace("\x00", "")

        # 2. Remove control characters (U+0000 to U+001F, U+007F to U+009F)
        sanitized = "".join(
            ch for ch in sanitized
            if not unicodedata.category(ch).startswith("C") or ch in (" ", "\t")
        )

        # 3. Strip path components — extract only the base filename
        for separator in ("/", "\\"):
            if separator in sanitized:
                sanitized = sanitized.rsplit(separator, 1)[-1]

        # 4. Also try PurePosixPath and PureWindowsPath for thorough extraction
        try:
            sanitized = PurePosixPath(sanitized).name
        except (ValueError, TypeError):
            pass
        try:
            sanitized = PureWindowsPath(sanitized).name
        except (ValueError, TypeError):
            pass

        # 5. Remove leading/trailing whitespace and dots
        sanitized = sanitized.strip().strip(".")

        # 6. Remove dangerous characters but preserve extension dots
        sanitized = re.sub(r'[^\w\s.\-()]', '_', sanitized)

        # 7. Collapse multiple dots/spaces/underscores
        sanitized = re.sub(r'\.{2,}', '.', sanitized)
        sanitized = re.sub(r'\s{2,}', ' ', sanitized)
        sanitized = re.sub(r'_{2,}', '_', sanitized)

        # 8. Check for Windows reserved names
        stem = PurePosixPath(sanitized).stem.upper()
        if stem in WINDOWS_RESERVED_NAMES:
            sanitized = f"resume_{sanitized}"

        # 9. Truncate if too long (preserve extension)
        if len(sanitized) > MAX_FILENAME_LENGTH:
            path = PurePosixPath(sanitized)
            ext = path.suffix
            max_stem_len = MAX_FILENAME_LENGTH - len(ext)
            sanitized = path.stem[:max_stem_len] + ext

        # 10. Final validation
        if not sanitized or sanitized in (".", ".."):
            raise UnsafeFilenameError("The uploaded filename could not be sanitized to a safe value.")

        return sanitized

    def _generate_stored_filename(self, extension: str) -> str:
        """Generate a secure UUID-based filename for internal storage."""
        return f"{uuid.uuid4()}{extension}"
