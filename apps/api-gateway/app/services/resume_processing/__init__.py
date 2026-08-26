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
    EducationRecord,
    ExtractedEducation,
    ExperienceRecord,
    ExtractedExperience,
    ProjectRecord,
    ExtractedProjects,
    StructuredResume,
    ResumeClassification,
    JobRequirements,
    ATSScore,
    SimilarityMatch,
    FAISSIndexResult,
    FAISSSearchItem,
    FAISSSearchResult,
    RecommendationExplanation,
    JobRecommendation,
    CandidateRecommendation,
    JobRecommendationResponse,
    CandidateRecommendationResponse,
    InterviewQuestion,
    GeneratedInterviewQuestions,
    InterviewQuestionRequest,
)
from .interview_taxonomy import (
    QuestionCategory,
    QuestionDifficulty,
    normalize_category,
    normalize_difficulty,
)
from .recommendation_engine import (
    RecommendationEngine,
    calculate_recommendation_score,
    build_match_explanation,
    recommend_jobs_for_resume,
    recommend_candidates_for_job,
)
from .interview_question_generator import (
    BaseInterviewQuestionGenerator,
    RuleBasedInterviewQuestionGenerator,
    LLMInterviewQuestionGenerator,
    build_candidate_context,
    generate_interview_questions,
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
tokenize_text = tokenize_resume_text

from .text_processor import process_extracted_document
from .spacy_service import get_spacy_nlp, reset_spacy_cache, set_spacy_nlp
from .skill_dictionary import SKILL_DICTIONARY, SKILL_CATEGORIES, ALIAS_MAP
from .skill_normalizer import normalize_and_deduplicate_skills
from .skill_extractor import extract_skills
from .degree_dictionary import DEGREE_DICTIONARY, DEGREE_LEVELS
from .education_normalizer import normalize_degree, normalize_institution, deduplicate_education_records
from .education_extractor import extract_education
from .job_title_dictionary import SENIORITY_LEVELS, EMPLOYMENT_TYPES
from .experience_normalizer import normalize_company, normalize_job_title, detect_seniority, deduplicate_experience_records
from .experience_extractor import extract_experience
from .project_normalizer import normalize_project_name, normalize_technologies, classify_project, deduplicate_project_records
from .project_extractor import extract_projects
from .structured_resume import build_structured_resume, validate_structured_resume, extract_contact_info
from .resume_classifier import HybridResumeClassifier, classify_resume
from .ats_scorer import HybridATSScorer, score_resume_against_job
calculate_ats_score = score_resume_against_job


from .embedding_service import (
    get_embedding_model,
    build_resume_embedding_text,
    build_job_embedding_text,
    generate_embedding,
    generate_resume_embedding,
    generate_job_embedding,
    calculate_cosine_similarity,
    normalize_similarity_score,
)
compute_cosine_similarity = calculate_cosine_similarity

from .similarity_matcher import calculate_resume_job_similarity
calculate_similarity_match = calculate_resume_job_similarity

from .faiss_index_service import (
    FAISSVectorIndex,
    get_resume_faiss_index,
    get_job_faiss_index,
    index_resume,
    index_job,
    remove_resume_index,
    remove_job_index,
    search_jobs_for_resume,
    search_resumes_for_job,
)


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
    "EducationRecord",
    "ExtractedEducation",
    "ExperienceRecord",
    "ExtractedExperience",
    "ProjectRecord",
    "ExtractedProjects",
    "StructuredResume",
    "ResumeClassification",
    "JobRequirements",
    "ATSScore",
    "SimilarityMatch",
    "FAISSIndexResult",
    "FAISSSearchItem",
    "FAISSSearchResult",
    "RecommendationExplanation",
    "JobRecommendation",
    "CandidateRecommendation",
    "JobRecommendationResponse",
    "CandidateRecommendationResponse",
    "InterviewQuestion",
    "GeneratedInterviewQuestions",
    "InterviewQuestionRequest",
    "QuestionCategory",
    "QuestionDifficulty",
    "normalize_category",
    "normalize_difficulty",
    "BaseInterviewQuestionGenerator",
    "RuleBasedInterviewQuestionGenerator",
    "LLMInterviewQuestionGenerator",
    "build_candidate_context",
    "generate_interview_questions",

    "RecommendationEngine",
    "calculate_recommendation_score",
    "build_match_explanation",
    "recommend_jobs_for_resume",
    "recommend_candidates_for_job",
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
    "DEGREE_DICTIONARY",
    "DEGREE_LEVELS",
    "normalize_degree",
    "normalize_institution",
    "deduplicate_education_records",
    "extract_education",
    "SENIORITY_LEVELS",
    "EMPLOYMENT_TYPES",
    "normalize_company",
    "normalize_job_title",
    "detect_seniority",
    "deduplicate_experience_records",
    "extract_experience",
    "normalize_project_name",
    "normalize_technologies",
    "classify_project",
    "deduplicate_project_records",
    "extract_projects",
    "build_structured_resume",
    "validate_structured_resume",
    "extract_contact_info",
    "HybridResumeClassifier",
    "classify_resume",
    "HybridATSScorer",
    "score_resume_against_job",
    "get_embedding_model",
    "build_resume_embedding_text",
    "build_job_embedding_text",
    "generate_embedding",
    "generate_resume_embedding",
    "generate_job_embedding",
    "calculate_cosine_similarity",
    "normalize_similarity_score",
    "calculate_resume_job_similarity",
    "FAISSVectorIndex",
    "get_resume_faiss_index",
    "get_job_faiss_index",
    "index_resume",
    "index_job",
    "remove_resume_index",
    "remove_job_index",
    "search_jobs_for_resume",
    "search_resumes_for_job",
]



