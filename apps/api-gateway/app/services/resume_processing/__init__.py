"""Resume text extraction, OCR, text processing, and skill extraction package."""

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
    ProcessedSection,
    ProcessedResumeText,
    ExtractedSkill,
    ExtractedSkills,
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
from .text_cleaner import clean_text, remove_extraction_noise
from .section_detector import detect_sections, SECTION_ALIASES
from .tokenizer import tokenize_resume_text
from .text_processor import process_extracted_document
from .spacy_service import get_spacy_nlp, reset_spacy_cache, set_spacy_nlp
from .skill_dictionary import SKILL_DICTIONARY, SKILL_CATEGORIES, ALIAS_MAP
from .skill_normalizer import normalize_and_deduplicate_skills
from .skill_extractor import extract_skills

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
    "ProcessedSection",
    "ProcessedResumeText",
    "ExtractedSkill",
    "ExtractedSkills",
    "extract_pdf_text",
    "extract_docx_text",
    "extract_document",
    "check_tesseract_available",
    "detect_ocr_pages",
    "render_pdf_page_to_image",
    "ocr_single_page",
    "process_pdf_with_ocr",
    "preprocess_image_for_ocr",
    "clean_text",
    "remove_extraction_noise",
    "detect_sections",
    "SECTION_ALIASES",
    "tokenize_resume_text",
    "process_extracted_document",
    "get_spacy_nlp",
    "reset_spacy_cache",
    "set_spacy_nlp",
    "SKILL_DICTIONARY",
    "SKILL_CATEGORIES",
    "ALIAS_MAP",
    "normalize_and_deduplicate_skills",
    "extract_skills",
]
