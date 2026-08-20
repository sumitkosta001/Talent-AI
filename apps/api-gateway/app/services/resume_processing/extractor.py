"""Unified Document Extraction Dispatcher.

Dispatches binary content to appropriate format extractors (.pdf, .docx)
and validates document integrity.

Day 22: Integrates OCR fallback for scanned PDF pages after native extraction.
"""

import logging
from typing import Optional
from app.exceptions.resume import ResumeParsingError
from .models import ExtractedDocument
from .pdf_extractor import extract_pdf_text
from .docx_extractor import extract_docx_text
from .ocr import detect_ocr_pages, process_pdf_with_ocr

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

    For PDF documents, native text extraction is attempted first. If pages are detected
    as scanned/image-only, OCR is automatically invoked for those pages (Day 22 hybrid).

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
        return _extract_pdf_with_ocr_fallback(content)

    # Check for DOCX
    if ext_clean in DOCX_EXTENSIONS or mime_clean in DOCX_MIME_TYPES:
        logger.debug("Dispatching document to DOCX extractor (extension=%s, mime=%s)", ext_clean, mime_clean)
        return extract_docx_text(content)

    # Unsupported format
    logger.warning("Unsupported file type for extraction: extension=%s, mime=%s", extension, mime_type)
    raise ResumeParsingError(
        f"Unsupported document format '{extension}'. Only PDF and DOCX documents are supported."
    )


def _extract_pdf_with_ocr_fallback(content: bytes) -> ExtractedDocument:
    """Extract text from a PDF with automatic OCR fallback for scanned pages.

    1. Run Day 21 native PDF extraction.
    2. Analyze pages for OCR necessity.
    3. If OCR pages detected → run hybrid native+OCR pipeline.
    4. If no OCR needed → return native result with extraction_method annotations.

    Args:
        content: Raw PDF binary bytes.

    Returns:
        ExtractedDocument with per-page extraction_method annotations.
    """
    # Step 1: Native extraction (Day 21)
    native_doc = extract_pdf_text(content)

    # Step 2: Check if any pages need OCR
    from app.config.settings import settings
    ocr_meta = detect_ocr_pages(
        pages=native_doc.pages,
        content=content,
        min_chars_per_page=settings.ocr.ocr_min_text_chars_per_page,
    )

    if not ocr_meta.ocr_required:
        # All pages have sufficient native text — annotate and return
        for page in native_doc.pages:
            page.extraction_method = "native"
        native_doc.ocr_metadata = ocr_meta
        logger.info(
            "PDF extraction complete (native only): pages=%d, chars=%d",
            native_doc.page_count, native_doc.character_count,
        )
        return native_doc

    # Step 3: OCR is needed — run hybrid pipeline
    logger.info(
        "OCR required for %d page(s): %s — invoking hybrid extraction",
        ocr_meta.ocr_pages_count, ocr_meta.pages_requiring_ocr,
    )
    return process_pdf_with_ocr(content=content, native_doc=native_doc)
