"""Data models for extracted resume documents and structure preservation.

Designed for consumption by downstream NLP pipelines:
Day 21 (Text Extraction) -> Day 22 (OCR) -> Day 23 (Text Processing / Section Detection)
-> Day 24-27 (Entity Extraction) -> Day 28 (Structured JSON Persistence).
"""

import uuid
from typing import Optional, List, Dict, Any, Tuple, Union
from pydantic import BaseModel, Field

from app.services.resume_processing.interview_taxonomy import QuestionCategory, QuestionDifficulty



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

    @property
    def raw_text(self) -> str:
        return self.text

    @property
    def is_ocr(self) -> bool:
        return self.extraction_method == "ocr"



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

    @property
    def raw_text(self) -> str:
        return self.original_document.text if self.original_document else self.cleaned_text


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


# Day 25 Education Extraction Models

class EducationRecord(BaseModel):
    """Represents an individual education entry extracted from a resume (Day 25)."""

    degree: Optional[str] = None  # Canonical degree name e.g. 'Bachelor of Technology'
    normalized_degree: Optional[str] = None  # Lowercase identifier e.g. 'bachelor_of_technology'
    degree_level: Optional[str] = None  # 'UNDERGRADUATE', 'POSTGRADUATE', 'DOCTORATE', 'DIPLOMA', 'SECONDARY', 'OTHER'

    field_of_study: Optional[str] = None  # Major/Specialization e.g. 'Electrical Engineering'

    institution: Optional[str] = None  # Cleaned / Canonical institution name e.g. 'National Institute of Technology, Rourkela'
    normalized_institution: Optional[str] = None  # Lowercase normalized institution identifier

    start_year: Optional[int] = None  # e.g. 2022
    end_year: Optional[int] = None  # e.g. 2026
    graduation_year: Optional[int] = None  # e.g. 2026
    graduation_status: Optional[str] = None  # 'COMPLETED', 'EXPECTED', 'UNKNOWN'

    cgpa: Optional[float] = None  # e.g. 7.99
    percentage: Optional[float] = None  # e.g. 94.0
    score_type: Optional[str] = None  # 'CGPA', 'GPA', 'CPI', 'PERCENTAGE', None

    source_text: str = ""  # Raw text line / block evidence
    section: str = "EDUCATION"  # Section where found
    source: str = "pattern"  # Source ('dictionary', 'pattern', 'section', 'spacy', 'hybrid')
    confidence: float = 0.90  # Heuristic confidence score (0.0 to 1.0)


class ExtractedEducation(BaseModel):
    """Container model for all extracted education records and metadata (Day 25)."""

    education_records: List[EducationRecord] = Field(default_factory=list)
    total_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def educations(self) -> List[EducationRecord]:
        return self.education_records



# Day 26 Experience Extraction Models

class ExperienceRecord(BaseModel):
    """Represents an individual work/employment experience entry extracted from a resume (Day 26)."""

    company: Optional[str] = None  # Raw/Cleaned company name e.g. 'Google LLC'
    normalized_company: Optional[str] = None  # Canonical lowercase company identifier e.g. 'google'

    job_title: Optional[str] = None  # Raw/Cleaned job title e.g. 'Senior Software Engineer'
    normalized_job_title: Optional[str] = None  # Canonical lowercase title identifier e.g. 'senior_software_engineer'

    employment_type: Optional[str] = None  # 'FULL_TIME', 'PART_TIME', 'INTERNSHIP', 'CONTRACT', 'FREELANCE', 'TEMPORARY', 'APPRENTICESHIP', 'VOLUNTEER', 'RESEARCH', 'UNKNOWN'

    start_date: Optional[str] = None  # e.g. '2022-01'
    end_date: Optional[str] = None  # e.g. '2024-01'

    start_year: Optional[int] = None  # e.g. 2022
    start_month: Optional[int] = None  # 1-12

    end_year: Optional[int] = None  # e.g. 2024
    end_month: Optional[int] = None  # 1-12

    duration_months: Optional[int] = None  # e.g. 24
    duration_text: Optional[str] = None  # e.g. '2 years'

    is_current: Optional[bool] = None  # True if currently employed in role

    responsibilities: List[str] = Field(default_factory=list)  # Bullet points / responsibility text lines

    seniority: Optional[str] = None  # 'INTERN', 'ENTRY_LEVEL', 'JUNIOR', 'MID_LEVEL', 'SENIOR', 'LEAD', 'STAFF', 'PRINCIPAL', 'MANAGER', 'DIRECTOR', 'EXECUTIVE', 'UNKNOWN'

    location: Optional[str] = None  # e.g. 'Bengaluru, India' or 'Remote'

    source_text: str = ""  # Raw text block evidence
    section: str = "EXPERIENCE"  # Section where found
    source: str = "pattern"  # Source ('dictionary', 'pattern', 'section', 'spacy', 'hybrid')
    confidence: float = 0.90  # Heuristic confidence score (0.0 to 1.0)


class ExtractedExperience(BaseModel):
    """Container model for all extracted experience records and metadata (Day 26)."""

    experiences: List[ExperienceRecord] = Field(default_factory=list)
    total_count: int = 0
    total_experience_months: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Day 27 Project Extraction Models

class ProjectRecord(BaseModel):
    """Represents an individual project entry extracted from a resume (Day 27)."""

    name: Optional[str] = None  # Raw/Cleaned project name e.g. 'Talent AI'
    normalized_name: Optional[str] = None  # Lowercase normalized identifier e.g. 'talent ai'

    technologies: List[str] = Field(default_factory=list)  # Canonical tech names e.g. ['FastAPI', 'React.js']
    normalized_technologies: List[str] = Field(default_factory=list)  # Lowercase tech IDs e.g. ['fastapi', 'react.js']

    description: str = ""  # Original verbatim project description text

    project_type: Optional[str] = None  # 'PERSONAL', 'ACADEMIC', 'COMMERCIAL', 'OPEN_SOURCE', 'UNKNOWN'
    classification: Optional[str] = None  # 'FULL_STACK', 'WEB_APPLICATION', 'MACHINE_LEARNING', 'ARTIFICIAL_INTELLIGENCE', 'MOBILE_APPLICATION', 'DATA_SCIENCE', 'DEVOPS', 'EMBEDDED', 'RESEARCH', 'OTHER'

    start_year: Optional[int] = None  # e.g. 2024
    end_year: Optional[int] = None  # e.g. 2025

    project_url: Optional[str] = None  # Optional project link
    github_url: Optional[str] = None  # Optional GitHub repository link

    source_text: str = ""  # Raw text block evidence
    section: str = "PROJECTS"  # Section where found
    source: str = "pattern"  # Source ('dictionary', 'pattern', 'section', 'spacy', 'hybrid')
    confidence: float = 0.90  # Heuristic confidence score (0.0 to 1.0)


class ExtractedProjects(BaseModel):
    """Container model for all extracted project records and metadata (Day 27)."""

    projects: List[ProjectRecord] = Field(default_factory=list)
    total_count: int = 0
    classifications: Dict[str, List[str]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Day 29 Classification Models

class ResumeClassification(BaseModel):
    """Candidate domain, role, and experience level classification result (Day 29)."""

    domain: str = "UNKNOWN"
    domain_confidence: float = 0.0

    role: str = "UNKNOWN"
    role_confidence: float = 0.0

    experience_level: str = "UNKNOWN"
    experience_level_confidence: float = 0.0

    domain_scores: Dict[str, float] = Field(default_factory=dict)
    role_scores: Dict[str, float] = Field(default_factory=dict)
    evidence: Dict[str, List[str]] = Field(default_factory=dict)

    classifier_version: str = "day29-v1"
    classification_method: str = "hybrid_rule_based"
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Day 28 Structured Resume Model

class StructuredResume(BaseModel):
    """Canonical structured representation of a parsed resume (Day 28).

    Combines Day 21-27 outputs into a validated, serializable, versioned document payload,
    and Day 29 classification outputs.
    """

    schema_version: str = "1.0"
    pipeline_version: str = "phase4-day28"

    resume_id: Optional[Union[str, Any]] = None
    candidate_profile_id: Optional[Union[str, Any]] = None

    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

    summary: Optional[str] = None

    skills: ExtractedSkills = Field(default_factory=ExtractedSkills)
    education: ExtractedEducation = Field(default_factory=ExtractedEducation)
    experience: ExtractedExperience = Field(default_factory=ExtractedExperience)
    projects: ExtractedProjects = Field(default_factory=ExtractedProjects)

    classification: Optional[ResumeClassification] = None

    certifications: List[Any] = Field(default_factory=list)
    languages: List[Any] = Field(default_factory=list)
    achievements: List[Any] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(default_factory=dict)


# Day 30 ATS Scoring Models

class JobRequirements(BaseModel):
    """Structured job requirements model for candidate ATS comparison (Day 30)."""

    job_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    required_keywords: List[str] = Field(default_factory=list)
    preferred_keywords: List[str] = Field(default_factory=list)

    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)

    required_education: List[str] = Field(default_factory=list)
    preferred_education: List[str] = Field(default_factory=list)

    required_experience_months: Optional[int] = None
    preferred_experience_months: Optional[int] = None

    required_roles: List[str] = Field(default_factory=list)
    preferred_roles: List[str] = Field(default_factory=list)

    required_domains: List[str] = Field(default_factory=list)
    preferred_domains: List[str] = Field(default_factory=list)

    required_experience_level: Optional[str] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)


class ATSScore(BaseModel):
    """Job-specific ATS score and explainable component breakdown (Day 30)."""

    score: float = 0.0

    keyword_score: float = 0.0
    skill_score: float = 0.0
    education_score: float = 0.0
    experience_score: float = 0.0

    matched_keywords: List[str] = Field(default_factory=list)
    missing_required_keywords: List[str] = Field(default_factory=list)
    missing_preferred_keywords: List[str] = Field(default_factory=list)

    matched_required_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    matched_preferred_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)

    matched_education: List[str] = Field(default_factory=list)
    missing_education: List[str] = Field(default_factory=list)

    experience_match: Dict[str, Any] = Field(default_factory=dict)
    score_breakdown: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

    explanation: str = ""
    recommendations: List[str] = Field(default_factory=list)

    scorer_version: str = "day30-v1"
    scoring_method: str = "weighted_hybrid_rule_based"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def overall_score(self) -> float:
        return self.score

    @property
    def skill_match_score(self) -> float:
        return self.skill_score

    @property
    def breakdown(self) -> Dict[str, Dict[str, Any]]:
        return self.score_breakdown



# Day 31 Similarity Matching Models

class SimilarityMatch(BaseModel):
    """Semantic embedding-based similarity match output (Day 31)."""

    resume_id: Optional[str] = None
    job_id: Optional[str] = None

    raw_cosine_similarity: float = 0.0
    similarity_score: float = 0.0

    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    resume_text_length: int = 0
    job_text_length: int = 0

    similarity_tier: str = "Low"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def match_score(self) -> float:
        return self.similarity_score


# Day 32 FAISS Vector Indexing & Search Models

class FAISSIndexResult(BaseModel):
    """Result payload for vector indexing operation (Day 32)."""

    entity_id: str
    entity_type: str = "resume"  # "resume" or "job"
    indexed: bool = True
    dimension: int = 384
    index_type: str = "IndexFlatIP"
    vector_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def status(self) -> str:
        return "indexed" if self.indexed else "failed"



class FAISSSearchItem(BaseModel):
    """Single matching item from FAISS similarity search (Day 32)."""

    entity_id: str
    raw_similarity: float = 0.0
    similarity_score: float = 0.0
    similarity_tier: str = "Low Match"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FAISSSearchResult(BaseModel):
    """Aggregated response for FAISS vector similarity search (Day 32)."""

    query_type: str = "vector_search"  # "resume_to_jobs", "job_to_resumes", "vector_search"
    total_results: int = 0
    top_k: int = 10
    results: List[FAISSSearchItem] = Field(default_factory=list)
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Day 33 Recommendation Models

class RecommendationExplanation(BaseModel):
    """Structured, evidence-based match explanation breakdown (Day 33)."""

    summary: str = ""
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    role_domain_compatibility: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class JobRecommendation(BaseModel):
    """Recommendation item representing a job suitable for a candidate (Day 33)."""

    job_id: str
    title: Optional[str] = None
    company: Optional[str] = None
    recommendation_score: float = 0.0
    semantic_similarity_score: float = 0.0
    ats_score: float = 0.0
    skill_match_score: float = 0.0
    education_match_score: float = 0.0
    experience_match_score: float = 0.0
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    ranking_position: int = 1
    explanation: RecommendationExplanation = Field(default_factory=RecommendationExplanation)
    confidence: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CandidateRecommendation(BaseModel):
    """Recommendation item representing a candidate resume suitable for a job (Day 33)."""

    candidate_id: Optional[str] = None
    resume_id: str
    full_name: Optional[str] = None
    recommendation_score: float = 0.0
    semantic_similarity_score: float = 0.0
    ats_score: float = 0.0
    skill_match_score: float = 0.0
    education_match_score: float = 0.0
    experience_match_score: float = 0.0
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    ranking_position: int = 1
    explanation: RecommendationExplanation = Field(default_factory=RecommendationExplanation)
    confidence: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class JobRecommendationResponse(BaseModel):
    """Container payload for candidate job recommendations (Day 33)."""

    resume_id: Optional[str] = None
    recommendations: List[JobRecommendation] = Field(default_factory=list)
    total_results: int = 0
    top_k: int = 10
    ranking_method: str = "weighted_hybrid_faiss_ats"
    scoring_version: str = "day33-v1"
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CandidateRecommendationResponse(BaseModel):
    """Container payload for job candidate recommendations (Day 33)."""

    job_id: Optional[str] = None
    recommendations: List[CandidateRecommendation] = Field(default_factory=list)
    total_results: int = 0
    top_k: int = 10
    ranking_method: str = "weighted_hybrid_faiss_ats"
    scoring_version: str = "day33-v1"
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Day 34 AI Interview Question Models

class InterviewQuestion(BaseModel):
    """Single generated interview question with taxonomy, role/skill targeting, and source metadata (Day 34)."""

    id: str = Field(default_factory=lambda: f"q-{uuid.uuid4().hex[:8]}")
    question: str
    category: QuestionCategory = QuestionCategory.TECHNICAL
    difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM
    question_type: str = "general"  # SKILL_SPECIFIC, ROLE_SPECIFIC, PROJECT, EXPERIENCE, BEHAVIORAL, SYSTEM_DESIGN, CODING, CONCEPTUAL
    target_role: Optional[str] = None
    target_skill: Optional[str] = None
    rationale: Optional[str] = None
    source: str = "rule_based"  # llm_openai, llm_gemini, rule_based_fallback
    confidence: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GeneratedInterviewQuestions(BaseModel):
    """Container response payload for generated interview questions (Day 34)."""

    resume_id: Optional[str] = None
    questions: List[InterviewQuestion] = Field(default_factory=list)
    total_count: int = 0
    role: Optional[str] = None
    domain: Optional[str] = None
    experience_level: Optional[str] = None
    skills_used: List[str] = Field(default_factory=list)
    categories: List[QuestionCategory] = Field(default_factory=list)
    difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM
    provider: str = "auto"
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InterviewQuestionRequest(BaseModel):
    """Optional request parameters for interview question generation (Day 34)."""

    count: int = Field(10, ge=1, le=50)
    difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM
    categories: Optional[List[QuestionCategory]] = None
    provider: str = "auto"











