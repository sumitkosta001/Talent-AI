"""PyMuPDF-based PDF Resume Text Extractor.

Extracts plain text and structured blocks, preserving page boundaries,
spatial bounding boxes, and document metadata.
"""

import logging
from typing import List
import pymupdf

from app.exceptions.resume import ResumeParsingError
from .models import (
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    DocumentMetadata,
)

logger = logging.getLogger("talentai.resume_processing.pdf")

# Minimum characters threshold to consider a document as having extractable text
MIN_EXTRACTABLE_CHAR_THRESHOLD = 15


def extract_pdf_text(content: bytes) -> ExtractedDocument:
    """Extract text, blocks, page structure, and metadata from a PDF binary stream.

    Args:
        content: Raw binary bytes of the PDF document.

    Returns:
        ExtractedDocument containing full text, pages, blocks, and metadata.

    Raises:
        ResumeParsingError: If document is empty, corrupted, encrypted, or unreadable.
    """
    if not content or len(content.strip()) == 0:
        logger.warning("PDF extraction failed: file content is empty.")
        raise ResumeParsingError("The uploaded PDF file is empty.")

    doc = None
    try:
        doc = pymupdf.open(stream=content, filetype="pdf")
    except Exception as exc:
        logger.warning("PyMuPDF failed to open document: %s", str(exc))
        raise ResumeParsingError("Failed to open or parse corrupted PDF document.") from exc

    try:
        # Check for encryption / password protection
        if doc.is_encrypted:
            # Try decrypting with empty password
            if not doc.authenticate(""):
                logger.warning("PDF extraction failed: document is password-protected/encrypted.")
                raise ResumeParsingError("The PDF document is password-protected or encrypted.")

        page_count = len(doc)
        if page_count == 0:
            logger.warning("PDF extraction failed: document contains 0 pages.")
            raise ResumeParsingError("The PDF document contains no pages.")

        pages: List[DocumentPage] = []
        full_text_parts: List[str] = []
        total_chars = 0
        total_words = 0

        for page_idx in range(page_count):
            page_num = page_idx + 1
            page = doc.load_page(page_idx)

            # Extract structured blocks: (x0, y0, x1, y1, text, block_no, block_type)
            # block_type == 0 is text, block_type == 1 is image
            raw_blocks = page.get_text("blocks")
            blocks: List[DocumentBlock] = []
            page_text_parts: List[str] = []

            for b_idx, b in enumerate(raw_blocks):
                b_text = b[4].strip() if len(b) > 4 and isinstance(b[4], str) else ""
                b_type = b[6] if len(b) > 6 else 0
                bbox = (float(b[0]), float(b[1]), float(b[2]), float(b[3])) if len(b) >= 4 else None

                if b_text:
                    blocks.append(
                        DocumentBlock(
                            text=b_text,
                            block_index=b_idx,
                            bbox=bbox,
                            block_type=b_type,
                        )
                    )
                    page_text_parts.append(b_text)

            page_text = "\n\n".join(page_text_parts)
            page_char_count = len(page_text)
            page_word_count = len(page_text.split()) if page_text else 0
            page_has_text = page_char_count >= MIN_EXTRACTABLE_CHAR_THRESHOLD

            total_chars += page_char_count
            total_words += page_word_count

            if page_text:
                full_text_parts.append(page_text)

            pages.append(
                DocumentPage(
                    page_number=page_num,
                    text=page_text,
                    blocks=blocks,
                    character_count=page_char_count,
                    word_count=page_word_count,
                    has_extractable_text=page_has_text,
                )
            )

        # Extract metadata
        raw_meta = doc.metadata or {}
        metadata = DocumentMetadata(
            title=raw_meta.get("title") or None,
            author=raw_meta.get("author") or None,
            subject=raw_meta.get("subject") or None,
            keywords=raw_meta.get("keywords") or None,
            creator=raw_meta.get("creator") or None,
            producer=raw_meta.get("producer") or None,
            creation_date=raw_meta.get("creationDate") or None,
            modification_date=raw_meta.get("modDate") or None,
        )

        full_text = "\n\n--- Page Break ---\n\n".join(full_text_parts) if full_text_parts else ""
        has_extractable_text = total_chars >= MIN_EXTRACTABLE_CHAR_THRESHOLD

        logger.info(
            "PDF extraction completed: pages=%d, characters=%d, words=%d, has_text=%s",
            page_count, total_chars, total_words, has_extractable_text,
        )

        return ExtractedDocument(
            text=full_text,
            document_type="pdf",
            extraction_method="pymupdf",
            page_count=page_count,
            pages=pages,
            metadata=metadata,
            character_count=total_chars,
            word_count=total_words,
            has_extractable_text=has_extractable_text,
        )

    finally:
        if doc is not None:
            doc.close()
