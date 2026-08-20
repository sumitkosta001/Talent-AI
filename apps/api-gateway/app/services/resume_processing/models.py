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


class ExtractedDocument(BaseModel):
    """Unified internal representation of an extracted resume document.

    Preserves page boundaries, paragraph boundaries, blocks, tables,
    and metadata while providing a normalized full-text string for NLP.
    """

    text: str  # Normalized combined full text
    document_type: str  # 'pdf' or 'docx'
    extraction_method: str  # 'pymupdf' or 'python-docx'
    page_count: int = 1
    pages: List[DocumentPage] = Field(default_factory=list)
    paragraphs: List[DocumentParagraph] = Field(default_factory=list)
    tables: List[DocumentTable] = Field(default_factory=list)
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    character_count: int = 0
    word_count: int = 0
    has_extractable_text: bool = True  # Signal for Day 22 OCR if False
