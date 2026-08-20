"""OCR service for scanned PDF resume processing.

Day 22: Provides page-level OCR detection, PDF page rendering, Tesseract integration,
and hybrid native/OCR document assembly.

Architecture:
    PDF bytes -> native extraction (Day 21) -> detect OCR pages -> render & preprocess
    -> Tesseract OCR -> merge into ExtractedDocument

The OCR service does NOT handle MinIO, database, or authorization concerns.
"""

import logging
import time
from typing import List, Tuple, Optional

import pymupdf
from PIL import Image

from app.config.settings import settings
from app.exceptions.resume import ResumeParsingError
from .models import (
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    OCRMetadata,
)
from .image_preprocessing import preprocess_image_for_ocr

logger = logging.getLogger("talentai.resume_processing.ocr")


# ---------------------------------------------------------------------------
# Tesseract availability
# ---------------------------------------------------------------------------

_tesseract_available: Optional[bool] = None


def check_tesseract_available() -> bool:
    """Check whether the Tesseract OCR engine is available and configured.

    Caches the result after the first successful probe. Uses pytesseract's
    own version check which invokes the Tesseract binary.

    Returns:
        True if Tesseract is reachable, False otherwise.
    """
    global _tesseract_available
    if _tesseract_available is not None:
        return _tesseract_available

    try:
        import pytesseract

        # Configure executable path from settings
        cmd = settings.ocr.tesseract_cmd.strip()
        if cmd:
            pytesseract.pytesseract.tesseract_cmd = cmd

        version = pytesseract.get_tesseract_version()
        logger.info("Tesseract OCR available: version=%s", version)
        _tesseract_available = True
        return True

    except Exception as exc:
        logger.warning(
            "Tesseract OCR is not available. Scanned PDFs will not be processable. "
            "Error: %s", str(exc),
        )
        _tesseract_available = False
        return False


def reset_tesseract_cache() -> None:
    """Reset the cached Tesseract availability flag (useful for testing)."""
    global _tesseract_available
    _tesseract_available = None


# ---------------------------------------------------------------------------
# OCR page detection
# ---------------------------------------------------------------------------

def detect_ocr_pages(
    pages: List[DocumentPage],
    content: bytes,
    min_chars_per_page: int = 30,
) -> OCRMetadata:
    """Analyze native extraction results to determine which pages need OCR.

    A page requires OCR when:
    - Native extracted text is empty or whitespace-only, OR
    - Native text character count is below the configurable threshold, AND
    - The page contains image content (when detectable)

    Args:
        pages: List of DocumentPage objects from native PDF extraction.
        content: Raw PDF bytes (used to check for images via PyMuPDF).
        min_chars_per_page: Minimum characters threshold per page.

    Returns:
        OCRMetadata with detection results including page numbers requiring OCR.
    """
    pages_requiring_ocr: List[int] = []
    total_native_chars = 0

    # Open PDF to inspect image content per page
    doc = None
    page_image_counts: dict = {}
    try:
        doc = pymupdf.open(stream=content, filetype="pdf")
        for page_idx in range(len(doc)):
            page = doc.load_page(page_idx)
            image_list = page.get_images(full=True)
            page_image_counts[page_idx + 1] = len(image_list)
    except Exception as exc:
        logger.debug("Could not inspect PDF images for OCR detection: %s", str(exc))
    finally:
        if doc is not None:
            doc.close()

    for doc_page in pages:
        total_native_chars += doc_page.character_count

        # Update image count on the page model
        doc_page.image_count = page_image_counts.get(doc_page.page_number, 0)

        text_stripped = doc_page.text.strip() if doc_page.text else ""
        text_is_sparse = len(text_stripped) < min_chars_per_page
        has_images = doc_page.image_count > 0

        if not text_stripped or text_is_sparse:
            # Flag for OCR if text is empty/whitespace, or below minimum threshold.
            # Image presence is a strong signal but not required — a near-empty page
            # in a resume context almost always indicates a scan or rendering issue.
            pages_requiring_ocr.append(doc_page.page_number)

    ocr_required = len(pages_requiring_ocr) > 0

    logger.info(
        "OCR detection: total_pages=%d, native_chars=%d, ocr_pages=%s, ocr_required=%s",
        len(pages), total_native_chars, pages_requiring_ocr, ocr_required,
    )

    return OCRMetadata(
        ocr_required=ocr_required,
        pages_requiring_ocr=pages_requiring_ocr,
        ocr_pages_count=len(pages_requiring_ocr),
        native_text_character_count=total_native_chars,
    )


# ---------------------------------------------------------------------------
# PDF page rendering
# ---------------------------------------------------------------------------

def render_pdf_page_to_image(content: bytes, page_index: int, dpi: int = 300) -> Image.Image:
    """Render a single PDF page to a PIL RGB Image using PyMuPDF.

    Args:
        content: Raw PDF binary bytes.
        page_index: 0-based page index.
        dpi: Resolution for rendering (higher = better quality, more memory).

    Returns:
        PIL Image in RGB mode.

    Raises:
        ResumeParsingError: If page rendering fails.
    """
    doc = None
    try:
        doc = pymupdf.open(stream=content, filetype="pdf")
        if page_index < 0 or page_index >= len(doc):
            raise ResumeParsingError(
                f"Page {page_index + 1} is out of range for this document."
            )

        page = doc.load_page(page_index)
        zoom = dpi / 72.0  # PyMuPDF default is 72 DPI
        matrix = pymupdf.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)

        # Convert PyMuPDF pixmap to PIL Image
        img = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)

        logger.debug(
            "Rendered PDF page %d: size=%dx%d, dpi=%d",
            page_index + 1, pixmap.width, pixmap.height, dpi,
        )
        return img

    except ResumeParsingError:
        raise
    except Exception as exc:
        logger.error("Failed to render PDF page %d: %s", page_index + 1, str(exc))
        raise ResumeParsingError(
            f"Failed to render page {page_index + 1} for OCR processing."
        ) from exc
    finally:
        if doc is not None:
            doc.close()


# ---------------------------------------------------------------------------
# Single-page OCR
# ---------------------------------------------------------------------------

def ocr_single_page(
    image: Image.Image,
    lang: str = "eng",
    psm: int = 6,
) -> Tuple[str, Optional[float]]:
    """Run Tesseract OCR on a preprocessed image and return text + confidence.

    Args:
        image: Preprocessed PIL Image.
        lang: Tesseract language code.
        psm: Page segmentation mode.

    Returns:
        Tuple of (extracted_text, average_confidence_or_None).

    Raises:
        ResumeParsingError: If Tesseract fails or is unavailable.
    """
    if not check_tesseract_available():
        raise ResumeParsingError(
            "OCR processing is unavailable. The Tesseract OCR engine is not installed or configured."
        )

    try:
        import pytesseract

        # Configure Tesseract executable
        cmd = settings.ocr.tesseract_cmd.strip()
        if cmd:
            pytesseract.pytesseract.tesseract_cmd = cmd

        custom_config = f"--psm {psm}"

        # Primary text extraction
        text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
        text = text.strip() if text else ""

        # Attempt to get confidence data
        confidence = None
        try:
            data = pytesseract.image_to_data(
                image, lang=lang, config=custom_config, output_type=pytesseract.Output.DICT
            )
            conf_values = [
                int(c) for c in data.get("conf", [])
                if str(c).lstrip("-").isdigit() and int(c) >= 0
            ]
            if conf_values:
                confidence = sum(conf_values) / len(conf_values)
        except Exception as conf_exc:
            logger.debug("Could not extract OCR confidence: %s", str(conf_exc))

        return text, confidence

    except ResumeParsingError:
        raise
    except Exception as exc:
        error_msg = str(exc).lower()
        if "tesseract" in error_msg and ("not found" in error_msg or "no such file" in error_msg):
            raise ResumeParsingError(
                "OCR processing failed. The Tesseract OCR engine is not properly installed."
            ) from exc
        if "failed loading language" in error_msg or "couldn't load any languages" in error_msg:
            raise ResumeParsingError(
                "OCR processing failed due to missing language data configuration."
            ) from exc

        logger.error("OCR engine error: %s", str(exc))
        raise ResumeParsingError(
            "OCR processing encountered an unexpected error."
        ) from exc


# ---------------------------------------------------------------------------
# Hybrid PDF processing (main entry point)
# ---------------------------------------------------------------------------

def process_pdf_with_ocr(
    content: bytes,
    native_doc: ExtractedDocument,
) -> ExtractedDocument:
    """Process a PDF with hybrid native/OCR extraction at page level.

    Pages with sufficient native text keep their original extraction.
    Pages detected as scanned/image-only are rendered, preprocessed, and OCR'd.

    Args:
        content: Raw PDF binary bytes.
        native_doc: ExtractedDocument from Day 21 native extraction.

    Returns:
        ExtractedDocument with hybrid extraction results and OCR metadata.

    Raises:
        ResumeParsingError: If OCR is required but fails fatally.
    """
    ocr_settings = settings.ocr
    start_time = time.time()

    # Step 1: Detect which pages need OCR
    ocr_meta = detect_ocr_pages(
        pages=native_doc.pages,
        content=content,
        min_chars_per_page=ocr_settings.ocr_min_text_chars_per_page,
    )

    if not ocr_meta.ocr_required:
        # No OCR needed — mark all pages as native and return
        for page in native_doc.pages:
            page.extraction_method = "native"
        native_doc.ocr_metadata = ocr_meta
        return native_doc

    # Step 2: Verify Tesseract is available before attempting OCR
    if not check_tesseract_available():
        raise ResumeParsingError(
            "OCR processing is required for this scanned document but the Tesseract "
            "OCR engine is not installed or configured."
        )

    # Step 3: Process each page (native or OCR)
    merged_pages: List[DocumentPage] = []
    full_text_parts: List[str] = []
    total_chars = 0
    total_words = 0
    ocr_confidences: List[float] = []

    for page in native_doc.pages:
        if page.page_number in ocr_meta.pages_requiring_ocr:
            # OCR this page
            try:
                # Render page to image
                page_image = render_pdf_page_to_image(
                    content=content,
                    page_index=page.page_number - 1,
                    dpi=ocr_settings.ocr_render_dpi,
                )

                # Preprocess image
                try:
                    preprocessed = preprocess_image_for_ocr(
                        image=page_image,
                        upscale_factor=ocr_settings.ocr_upscale_factor,
                        threshold_value=ocr_settings.ocr_threshold_value,
                    )
                except Exception as prep_exc:
                    logger.warning(
                        "Image preprocessing failed for page %d, using grayscale fallback: %s",
                        page.page_number, str(prep_exc),
                    )
                    # Fallback: just convert to grayscale
                    preprocessed = page_image.convert("L")

                # Run OCR
                ocr_text, ocr_conf = ocr_single_page(
                    image=preprocessed,
                    lang=ocr_settings.ocr_language,
                    psm=ocr_settings.ocr_psm,
                )

                # Clean up image references
                page_image.close()
                preprocessed.close()

                # Strip whitespace — treat whitespace-only OCR output as empty
                ocr_text = ocr_text.strip() if ocr_text else ""

                if ocr_text:
                    page_char_count = len(ocr_text)
                    page_word_count = len(ocr_text.split())
                    ocr_page = DocumentPage(
                        page_number=page.page_number,
                        text=ocr_text,
                        blocks=[DocumentBlock(text=ocr_text, block_index=0)],
                        character_count=page_char_count,
                        word_count=page_word_count,
                        has_extractable_text=True,
                        extraction_method="ocr",
                        ocr_confidence=ocr_conf,
                        image_count=page.image_count,
                    )
                    merged_pages.append(ocr_page)
                    full_text_parts.append(ocr_text)
                    total_chars += page_char_count
                    total_words += page_word_count
                    ocr_meta.pages_ocr_succeeded.append(page.page_number)

                    if ocr_conf is not None:
                        ocr_confidences.append(ocr_conf)

                    logger.info(
                        "OCR succeeded for page %d: chars=%d, confidence=%.1f",
                        page.page_number, page_char_count,
                        ocr_conf if ocr_conf is not None else -1,
                    )
                else:
                    # OCR returned empty text
                    empty_page = DocumentPage(
                        page_number=page.page_number,
                        text="",
                        blocks=[],
                        character_count=0,
                        word_count=0,
                        has_extractable_text=False,
                        extraction_method="ocr",
                        ocr_confidence=ocr_conf,
                        image_count=page.image_count,
                    )
                    merged_pages.append(empty_page)
                    ocr_meta.pages_ocr_failed.append(page.page_number)
                    logger.warning(
                        "OCR returned empty text for page %d", page.page_number
                    )

            except ResumeParsingError:
                # OCR failure for this page — record it but continue with other pages
                failed_page = DocumentPage(
                    page_number=page.page_number,
                    text="",
                    blocks=[],
                    character_count=0,
                    word_count=0,
                    has_extractable_text=False,
                    extraction_method="ocr",
                    image_count=page.image_count,
                )
                merged_pages.append(failed_page)
                ocr_meta.pages_ocr_failed.append(page.page_number)
                logger.warning(
                    "OCR processing failed for page %d", page.page_number
                )

        else:
            # Keep native extraction for this page
            page.extraction_method = "native"
            merged_pages.append(page)
            if page.text:
                full_text_parts.append(page.text)
            total_chars += page.character_count
            total_words += page.word_count

    # Step 4: Finalize OCR metadata
    elapsed = time.time() - start_time
    ocr_meta.ocr_processing_duration_seconds = round(elapsed, 3)
    if ocr_confidences:
        ocr_meta.average_ocr_confidence = round(
            sum(ocr_confidences) / len(ocr_confidences), 2
        )

    # Step 5: Check if we got any usable text at all
    if total_chars == 0:
        raise ResumeParsingError(
            "No readable text could be extracted from the document."
        )

    # Step 6: Determine extraction method label
    has_native = any(p.extraction_method == "native" and p.character_count > 0 for p in merged_pages)
    has_ocr = any(p.extraction_method == "ocr" and p.character_count > 0 for p in merged_pages)
    if has_native and has_ocr:
        extraction_method = "hybrid"
    elif has_ocr:
        extraction_method = "ocr"
    else:
        extraction_method = "pymupdf"

    full_text = "\n\n--- Page Break ---\n\n".join(full_text_parts) if full_text_parts else ""

    logger.info(
        "Hybrid OCR processing complete: method=%s, pages=%d, ocr_pages=%d, "
        "ocr_succeeded=%d, ocr_failed=%d, chars=%d, duration=%.3fs",
        extraction_method, len(merged_pages), ocr_meta.ocr_pages_count,
        len(ocr_meta.pages_ocr_succeeded), len(ocr_meta.pages_ocr_failed),
        total_chars, elapsed,
    )

    return ExtractedDocument(
        text=full_text,
        document_type="pdf",
        extraction_method=extraction_method,
        page_count=len(merged_pages),
        pages=merged_pages,
        metadata=native_doc.metadata,
        character_count=total_chars,
        word_count=total_words,
        has_extractable_text=total_chars > 0,
        ocr_metadata=ocr_meta,
    )
