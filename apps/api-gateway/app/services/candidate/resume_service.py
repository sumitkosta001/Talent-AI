"""Resume Upload Business Logic Service.

Handles file validation, filename sanitization, metadata creation,
and orchestrates the resume upload workflow for Day 11.

Designed so MinIO integration can be added in Day 12 without
restructuring the service interface.
"""

import logging
import re
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath, PureWindowsPath
from typing import Optional
from uuid import UUID

from fastapi import UploadFile

from app.config.settings import settings
from app.models.enums import ResumeStatus
from app.models.resume import Resume
from app.repositories.candidate.profile_repository import CandidateProfileRepository
from app.repositories.candidate.resume_repository import ResumeRepository
from app.exceptions.resume import (
    InvalidFileTypeError,
    FileTooLargeError,
    InvalidFileContentError,
    UnsafeFilenameError,
    MissingFileError,
)
from app.exceptions.candidate import CandidateProfileNotFoundError

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

    MinIO integration placeholder:
        The service is structured so that Day 12 can inject a storage client
        and call it between steps 4 and 5 without redesigning the interface.
    """

    def __init__(
        self,
        profile_repo: CandidateProfileRepository,
        resume_repo: ResumeRepository,
    ) -> None:
        self.profile_repo = profile_repo
        self.resume_repo = resume_repo

    async def upload_resume(self, user_id: UUID | str, file: UploadFile) -> Resume:
        """Orchestrate the full resume upload workflow.

        Args:
            user_id: ID of the authenticated user.
            file: FastAPI UploadFile instance from multipart/form-data.

        Returns:
            Persisted Resume entity with validated metadata.

        Raises:
            CandidateProfileNotFoundError: If no profile exists for the user.
            MissingFileError: If no file is provided.
            InvalidFileTypeError: If extension or MIME type is not allowed.
            FileTooLargeError: If file exceeds configured maximum size.
            InvalidFileContentError: If file content doesn't match declared type.
            UnsafeFilenameError: If filename contains dangerous characters.
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
        stored_filename = self._generate_stored_filename(extension)

        # 10. Determine version (increment from existing resumes)
        current_max_version = await self.resume_repo.get_max_version(profile.id)
        new_version = current_max_version + 1

        # 11. Mark existing resumes as not current
        if current_max_version > 0:
            await self.resume_repo.mark_all_not_current(profile.id)

        # 12. Create Resume entity
        resume = Resume(
            candidate_profile_id=profile.id,
            original_filename=safe_original_filename,
            stored_filename=stored_filename,
            mime_type=mime_type,
            file_extension=extension,
            file_size_bytes=file_size,
            status=ResumeStatus.UPLOADED,
            version=new_version,
            is_current=True,
            uploaded_at=datetime.now(timezone.utc),
        )

        # 13. Persist to database
        resume = await self.resume_repo.create(resume)

        logger.info(
            "Resume uploaded successfully: user=%s, profile=%s, resume=%s, filename=%s, size=%d bytes",
            user_id, profile.id, resume.id, safe_original_filename, file_size,
        )

        return resume

    # ==================================================================
    # VALIDATION METHODS
    # ==================================================================

    def _validate_file_size(self, file_size: int) -> None:
        """Validate file size against configured maximum.

        Args:
            file_size: Actual file size in bytes.

        Raises:
            FileTooLargeError: If file exceeds the limit.
        """
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

        Args:
            filename: Original filename from the client.

        Returns:
            Normalized lowercase extension (e.g., '.pdf').

        Raises:
            InvalidFileTypeError: If extension is not allowed or double-extension detected.
        """
        if not filename:
            raise InvalidFileTypeError("Filename is missing.")

        # Extract all suffixes to detect double-extension attacks
        # Use PurePosixPath to safely parse (works on all platforms)
        path = PurePosixPath(filename)
        suffixes = path.suffixes  # e.g., ['.pdf', '.exe'] for 'resume.pdf.exe'

        if len(suffixes) > 1:
            # Double extension detected — check if the LAST extension is dangerous
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

        # The actual extension is the last suffix
        extension = suffixes[-1].lower() if suffixes else ""

        allowed = settings.resume.allowed_extensions_list
        if extension not in allowed:
            raise InvalidFileTypeError(
                f"File extension '{extension}' is not supported. Allowed: {', '.join(allowed)}"
            )

        return extension

    def _validate_mime_type(self, content_type: Optional[str], extension: str) -> str:
        """Validate MIME type against allowed types and cross-check with extension.

        Args:
            content_type: Client-provided MIME type from the upload.
            extension: Validated and normalized file extension.

        Returns:
            Validated MIME type string.

        Raises:
            InvalidFileTypeError: If MIME type is not allowed or mismatches extension.
        """
        if not content_type:
            raise InvalidFileTypeError("File MIME type could not be determined.")

        # Normalize — some clients send with charset suffix
        mime = content_type.split(";")[0].strip().lower()

        allowed = settings.resume.allowed_mime_types_list
        if mime not in allowed:
            raise InvalidFileTypeError(
                f"MIME type '{mime}' is not supported. Allowed types: {', '.join(allowed)}"
            )

        # Cross-validate MIME with extension
        expected_ext = ALLOWED_MIME_TYPES.get(mime)
        if expected_ext and expected_ext != extension:
            raise InvalidFileTypeError(
                f"MIME type '{mime}' does not match file extension '{extension}'."
            )

        return mime

    def _validate_file_content(self, content: bytes, extension: str) -> None:
        """Validate file content by checking magic bytes / file signature.

        Args:
            content: Raw file bytes.
            extension: Validated file extension.

        Raises:
            InvalidFileContentError: If content does not match expected format.
        """
        if not content:
            raise InvalidFileContentError("The uploaded file is empty.")

        if extension == ".pdf":
            # PDF files must start with %PDF-
            # Some PDFs may have leading whitespace or BOM, check first 1024 bytes
            header = content[:1024]
            if PDF_MAGIC_BYTES not in header:
                logger.warning("PDF magic bytes not found in file header.")
                raise InvalidFileContentError(
                    "The uploaded file does not appear to be a valid PDF document."
                )

        elif extension == ".docx":
            # DOCX files are ZIP archives and must start with PK\x03\x04
            if not content[:4].startswith(DOCX_MAGIC_BYTES):
                logger.warning("DOCX/ZIP magic bytes not found in file header.")
                raise InvalidFileContentError(
                    "The uploaded file does not appear to be a valid DOCX document."
                )

    # ==================================================================
    # FILENAME SANITIZATION
    # ==================================================================

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize the original filename for safe metadata storage.

        Protection against:
            - Path traversal (../, ..\\)
            - Directory separators (/, \\)
            - Null bytes and control characters
            - Windows reserved device names
            - Extremely long filenames
            - Dangerous special characters

        The sanitized filename is used as metadata only — actual storage
        uses a UUID-based identifier from _generate_stored_filename().

        Args:
            filename: Raw filename from the client upload.

        Returns:
            Sanitized filename string safe for database storage.

        Raises:
            UnsafeFilenameError: If the filename cannot be safely sanitized.
        """
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
        # Handle both Unix and Windows path separators
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
        # Allow: letters, digits, hyphens, underscores, dots, spaces, parentheses
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
        """Generate a secure UUID-based filename for internal storage.

        Args:
            extension: Normalized file extension (e.g., '.pdf').

        Returns:
            Secure filename string (e.g., 'a1b2c3d4-e5f6-7890-abcd-ef1234567890.pdf').
        """
        return f"{uuid.uuid4()}{extension}"
