"""Resume text extraction and document structure processing package."""

from .models import (
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    DocumentParagraph,
    DocumentTable,
    DocumentTableRow,
    DocumentTableCell,
    DocumentMetadata,
)
from .pdf_extractor import extract_pdf_text
from .docx_extractor import extract_docx_text
from .extractor import extract_document

__all__ = [
    "ExtractedDocument",
    "DocumentPage",
    "DocumentBlock",
    "DocumentParagraph",
    "DocumentTable",
    "DocumentTableRow",
    "DocumentTableCell",
    "DocumentMetadata",
    "extract_pdf_text",
    "extract_docx_text",
    "extract_document",
]
