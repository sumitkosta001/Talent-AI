"""Data models for extracted resume documents and structure preservation.

Designed for consumption by downstream NLP pipelines:
Day 21 (Text Extraction) -> Day 22 (OCR) -> Day 23 (Text Processing / Section Detection)
-> Day 24-27 (Entity Extraction) -> Day 28 (Structured JSON Persistence).
"""

from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field


class DocumentBlock(BaseModel):
    """Represents a text block within a document page (preserves spatial and visual order)."""

    text: str
    block_index: int
    bbox: Optional[Tuple[float, float, float, float]] = None  # (x0, y0, x1, y1) bounding box
    block_type: int = 0  # 0 for text, 1 for image/other
    style_name: Optional[str] = None
    is_heading: bool = False
    heading_level: Optional[int] = None


class DocumentPage(BaseModel):
    """Represents a single page within a multi-page document (e.g., PDF)."""

    page_number: int  # 1-indexed
    text: str
    blocks: List[DocumentBlock] = Field(default_factory=list)
    character_count: int = 0
    word_count: int = 0
    has_extractable_text: bool = True
    extraction_method: str = "native"  # "native" or "ocr" (Day 22)
    ocr_confidence: Optional[float] = None  # Average OCR confidence 0-100 (Day 22)
    image_count: int = 0  # Number of images detected on the page (Day 22)


class DocumentTableCell(BaseModel):
    """Represents a single cell within a table."""

    text: str
    row_index: int
    col_index: int


class DocumentTableRow(BaseModel):
    """Represents a row of cells within a table."""

    row_index: int
    cells: List[DocumentTableCell] = Field(default_factory=list)


class DocumentTable(BaseModel):
    """Represents a structured table (e.g., in DOCX resumes)."""

    table_index: int
    rows: List[DocumentTableRow] = Field(default_factory=list)
    text: str = ""  # Plain-text formatted representation


class DocumentParagraph(BaseModel):
    """Represents a paragraph in flowable document formats (e.g., DOCX)."""

    text: str
    paragraph_index: int
    style_name: Optional[str] = None
    is_heading: bool = False
    heading_level: Optional[int] = None


class DocumentMetadata(BaseModel):
    """Basic document metadata extracted from PDF/DOCX headers and properties."""

    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    custom: Dict[str, Any] = Field(default_factory=dict)


class OCRMetadata(BaseModel):
    """Day 22 OCR detection and processing statistics for a document."""

    ocr_required: bool = False
    pages_requiring_ocr: List[int] = Field(default_factory=list)
    ocr_pages_count: int = 0
    native_text_character_count: int = 0
    pages_ocr_succeeded: List[int] = Field(default_factory=list)
    pages_ocr_failed: List[int] = Field(default_factory=list)
    average_ocr_confidence: Optional[float] = None
    ocr_processing_duration_seconds: Optional[float] = None


class ExtractedDocument(BaseModel):
    """Unified internal representation of an extracted resume document.

    Preserves page boundaries, paragraph boundaries, blocks, tables,
    and metadata while providing a normalized full-text string for NLP.
    """

    text: str  # Normalized combined full text
    document_type: str  # 'pdf' or 'docx'
    extraction_method: str  # 'pymupdf', 'python-docx', or 'hybrid' (native+ocr)
    page_count: int = 1
    pages: List[DocumentPage] = Field(default_factory=list)
    paragraphs: List[DocumentParagraph] = Field(default_factory=list)
    tables: List[DocumentTable] = Field(default_factory=list)
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    character_count: int = 0
    word_count: int = 0
    has_extractable_text: bool = True  # Signal for Day 22 OCR if False
    ocr_metadata: Optional[OCRMetadata] = None  # Day 22 OCR statistics


# Day 23 Text Processing & Section Detection Models

class ProcessedSection(BaseModel):
    """Represents a detected canonical section within a resume document."""

    name: str  # Canonical name (e.g., 'EXPERIENCE', 'SKILLS', 'EDUCATION', 'PROJECTS', 'SUMMARY', 'UNKNOWN')
    title: str  # Original heading text as found in the resume
    content: str  # Text content belonging to this section
    confidence: float = 1.0  # Heuristic detection confidence score (0.0 to 1.0)
    start_line: int = 1  # 1-indexed start line number in normalized text
    end_line: int = 1  # 1-indexed end line number in normalized text
    page_number: Optional[int] = None  # Page number where section heading starts


class ProcessedResumeText(BaseModel):
    """Structured, cleaned, normalized, and tokenized representation of a resume for downstream NLP (Day 23).

    Original ExtractedDocument is preserved intact for auditing and debugging.
    """

    cleaned_text: str  # Text with extraction noise, page numbers, and bad line breaks removed
    normalized_text: str  # NFKC normalized, case-preserved human-readable text
    lowercase_text: str  # Lowercase text for search and matching
    sections: List[ProcessedSection] = Field(default_factory=list)  # Detected sections in document order
    tokens: List[str] = Field(default_factory=list)  # Case-preserved tokens (technical terms intact)
    normalized_tokens: List[str] = Field(default_factory=list)  # Lowercase tokens for indexing
    metadata: Dict[str, Any] = Field(default_factory=dict)  # Processing stats
    original_document: ExtractedDocument  # Reference to original ExtractedDocument (not mutated)


# Day 24 Skills Extraction Models

class ExtractedSkill(BaseModel):
    """Represents a single canonical skill extracted from a resume document (Day 24)."""

    name: str  # Canonical display name (e.g. 'React.js', 'Python', 'PostgreSQL')
    normalized_name: str  # Lowercase identifier (e.g. 'react.js', 'python', 'postgresql')
    category: str  # Canonical category (e.g. 'FRONTEND', 'PROGRAMMING_LANGUAGE', 'DATABASE')
    source: str = "dictionary"  # Extraction source ('dictionary', 'phrase_match', 'regex', 'ner', 'hybrid')
    confidence: float = 0.95  # Heuristic confidence score (0.0 to 1.0)
    matched_text: str  # Raw matched text string as found in resume text (e.g. 'ReactJS')
    sections: List[str] = Field(default_factory=list)  # Sections where skill appeared e.g. ['SKILLS', 'PROJECTS']
    mentions_count: int = 1  # Number of times skill was mentioned across document


class ExtractedSkills(BaseModel):
    """Container model for all extracted skills, counts, and category breakdowns (Day 24)."""

    skills: List[ExtractedSkill] = Field(default_factory=list)  # Deduplicated list of extracted skills
    total_count: int = 0  # Total unique skills extracted
    categories: Dict[str, List[str]] = Field(default_factory=dict)  # Grouped canonical skill names by category
    metadata: Dict[str, Any] = Field(default_factory=dict)  # Processing stats (duration, spacy model, match count)

