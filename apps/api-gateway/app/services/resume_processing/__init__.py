"""Resume text extraction, OCR, and document structure processing package."""

from .models import (
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    DocumentParagraph,
    DocumentTable,
    DocumentTableRow,
    DocumentTableCell,
    DocumentMetadata,
    OCRMetadata,
)
from .pdf_extractor import extract_pdf_text
from .docx_extractor import extract_docx_text
from .extractor import extract_document
from .ocr import (
    check_tesseract_available,
    detect_ocr_pages,
    render_pdf_page_to_image,
    ocr_single_page,
    process_pdf_with_ocr,
)
from .image_preprocessing import preprocess_image_for_ocr

__all__ = [
    "ExtractedDocument",
    "DocumentPage",
    "DocumentBlock",
    "DocumentParagraph",
    "DocumentTable",
    "DocumentTableRow",
    "DocumentTableCell",
    "DocumentMetadata",
    "OCRMetadata",
    "extract_pdf_text",
    "extract_docx_text",
    "extract_document",
    "check_tesseract_available",
    "detect_ocr_pages",
    "render_pdf_page_to_image",
    "ocr_single_page",
    "process_pdf_with_ocr",
    "preprocess_image_for_ocr",
]
