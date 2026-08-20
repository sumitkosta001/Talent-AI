"""Unified Document Extraction Dispatcher.

Dispatches binary content to appropriate format extractors (.pdf, .docx)
and validates document integrity.
"""

import logging
from typing import Optional
from app.exceptions.resume import ResumeParsingError
from .models import ExtractedDocument
from .pdf_extractor import extract_pdf_text
from .docx_extractor import extract_docx_text

logger = logging.getLogger("talentai.resume_processing.extractor")

PDF_EXTENSIONS = {".pdf", "pdf"}
DOCX_EXTENSIONS = {".docx", "docx"}

PDF_MIME_TYPES = {
    "application/pdf",
    "application/x-pdf",
}

DOCX_MIME_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/docx",
}


def extract_document(
    content: bytes,
    extension: str,
    mime_type: Optional[str] = None,
) -> ExtractedDocument:
    """Dispatch binary content to the appropriate document extractor based on extension and MIME type.

    Args:
        content: Raw binary document bytes.
        extension: File extension (e.g., '.pdf', '.docx').
        mime_type: Optional MIME type (e.g., 'application/pdf').

    Returns:
        ExtractedDocument containing structured and full text representations.

    Raises:
        ResumeParsingError: If document is empty, corrupted, or format is unsupported.
    """
    if not content or len(content.strip()) == 0:
        logger.warning("Extraction rejected: empty binary payload.")
        raise ResumeParsingError("The uploaded resume file is empty.")

    ext_clean = extension.strip().lower() if extension else ""
    if not ext_clean.startswith(".") and ext_clean:
        ext_clean = f".{ext_clean}"

    mime_clean = mime_type.strip().lower() if mime_type else ""

    # Check for PDF
    if ext_clean in PDF_EXTENSIONS or mime_clean in PDF_MIME_TYPES:
        logger.debug("Dispatching document to PDF extractor (extension=%s, mime=%s)", ext_clean, mime_clean)
        return extract_pdf_text(content)

    # Check for DOCX
    if ext_clean in DOCX_EXTENSIONS or mime_clean in DOCX_MIME_TYPES:
        logger.debug("Dispatching document to DOCX extractor (extension=%s, mime=%s)", ext_clean, mime_clean)
        return extract_docx_text(content)

    # Unsupported format
    logger.warning("Unsupported file type for extraction: extension=%s, mime=%s", extension, mime_type)
    raise ResumeParsingError(
        f"Unsupported document format '{extension}'. Only PDF and DOCX documents are supported."
    )
