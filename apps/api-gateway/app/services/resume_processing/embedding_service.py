"""Phase 4 — Day 31: Embedding Service.

Provides singleton lazy loading of pretrained SentenceTransformer models,
clean text representation builders for resumes and job requirements,
vector validation, cosine similarity calculation, and 0-100 score normalization.
"""

import logging
import threading
from typing import Optional, List, Union, Dict, Any
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from app.config.settings import ApplicationSettings
from app.services.resume_processing.models import StructuredResume, JobRequirements

logger = logging.getLogger(__name__)

# Process-wide singleton model instance & lock
_model_instance: Optional[Any] = None
_model_name_cached: Optional[str] = None
_model_lock = threading.Lock()

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding_model(model_name: Optional[str] = None) -> Any:
    """Lazy-loads and caches process-wide SentenceTransformer model.

    Thread-safe implementation with graceful error handling.
    """
    global _model_instance, _model_name_cached

    if SentenceTransformer is None:
        raise RuntimeError(
            "sentence-transformers package is not installed. Please install sentence-transformers>=3.0.0."
        )

    target_model_name = model_name or getattr(
        ApplicationSettings(), "embedding_model_name", DEFAULT_MODEL_NAME
    )

    if _model_instance is not None and _model_name_cached == target_model_name:
        return _model_instance

    with _model_lock:
        if _model_instance is not None and _model_name_cached == target_model_name:
            return _model_instance

        logger.info("Loading SentenceTransformer model: %s", target_model_name)
        try:
            model = SentenceTransformer(target_model_name)
            _model_instance = model
            _model_name_cached = target_model_name
            logger.info("Successfully loaded SentenceTransformer model: %s", target_model_name)
            return _model_instance
        except Exception as e:
            logger.error("Failed to load SentenceTransformer model '%s': %s", target_model_name, str(e))
            raise RuntimeError(f"Could not load embedding model '{target_model_name}': {str(e)}") from e


def build_resume_embedding_text(resume: StructuredResume) -> str:
    """Builds clean, structured text representation of a resume for embedding.

    Excludes PII (phone, email, full_name, URLs) and OCR noise.
    Aggregates domain classification, skills, experience, education, and projects.
    """
    parts: List[str] = []

    # 1. Summary
    if resume.summary and resume.summary.strip():
        parts.append(f"Professional Summary: {resume.summary.strip()}")

    # 2. Domain Classification & Seniority
    if resume.classification:
        cls = resume.classification
        cls_parts: List[str] = []
        if cls.domain:
            cls_parts.append(f"Domain: {cls.domain}")
        role_val = getattr(cls, "primary_role", getattr(cls, "role", None))
        if role_val:
            cls_parts.append(f"Role: {role_val}")
        if cls.experience_level:
            cls_parts.append(f"Experience Level: {cls.experience_level}")
        if cls_parts:
            parts.append("Classification: " + "; ".join(cls_parts))


    # 3. Skills
    if resume.skills:
        skill_parts: List[str] = []
        all_skill_names = getattr(resume.skills, "all_skills", None)
        if not all_skill_names and getattr(resume.skills, "skills", None):
            all_skill_names = [s.name for s in resume.skills.skills if hasattr(s, "name") and s.name]
        if all_skill_names:
            skill_parts.append("All Skills: " + ", ".join(all_skill_names))
        if getattr(resume.skills, "categories", None):
            for cat, s_list in resume.skills.categories.items():
                if s_list:
                    skill_parts.append(f"{cat}: {', '.join(s_list)}")
        if skill_parts:
            parts.append("Skills & Expertise:\n" + "\n".join(skill_parts))


    # 4. Work Experience
    if resume.experience:
        exp_records = getattr(resume.experience, "records", None) or getattr(resume.experience, "experiences", None)
        if exp_records:
            exp_parts: List[str] = []
            for rec in exp_records:
                item_parts: List[str] = []
                if getattr(rec, "job_title", None):
                    item_parts.append(rec.job_title)
                if getattr(rec, "company", None):
                    item_parts.append(f"at {rec.company}")
                if getattr(rec, "responsibilities", None):
                    item_parts.append("- " + "; ".join(rec.responsibilities))
                if item_parts:
                    exp_parts.append(" ".join(item_parts))
            if exp_parts:
                parts.append("Work Experience:\n" + "\n".join(exp_parts))

    # 5. Education
    if resume.education:
        edu_records = getattr(resume.education, "records", None) or getattr(resume.education, "education_records", None)
        if edu_records:
            edu_parts: List[str] = []
            for rec in edu_records:
                deg = getattr(rec, "normalized_degree", None) or getattr(rec, "degree", None) or ""
                inst = f"from {rec.institution}" if getattr(rec, "institution", None) else ""
                field = f"in {rec.field_of_study}" if getattr(rec, "field_of_study", None) else ""
                entry = " ".join(p for p in [deg, field, inst] if p).strip()
                if entry:
                    edu_parts.append(entry)
            if edu_parts:
                parts.append("Education:\n" + "\n".join(edu_parts))

    # 6. Projects
    if resume.projects:
        proj_records = getattr(resume.projects, "records", None) or getattr(resume.projects, "projects", None)
        if proj_records:
            proj_parts: List[str] = []
            for proj in proj_records:
                p_str = getattr(proj, "name", None) or "Project"
                if getattr(proj, "technologies", None):
                    p_str += f" (Technologies: {', '.join(proj.technologies)})"
                if getattr(proj, "description", None):
                    p_str += f": {proj.description}"
                proj_parts.append(p_str)
            if proj_parts:
                parts.append("Key Projects:\n" + "\n".join(proj_parts))


    combined = "\n\n".join(parts).strip()
    return combined if combined else "Empty candidate resume profile"


def build_job_embedding_text(job: JobRequirements) -> str:
    """Builds clean, structured text representation of job requirements for embedding."""
    parts: List[str] = []

    # 1. Job Title & Description
    if job.title and job.title.strip():
        parts.append(f"Job Title: {job.title.strip()}")
    if job.description and job.description.strip():
        parts.append(f"Job Description: {job.description.strip()}")

    # 2. Roles & Domain
    role_domain_parts: List[str] = []
    if job.required_roles:
        role_domain_parts.append("Required Roles: " + ", ".join(job.required_roles))
    if job.required_domains:
        role_domain_parts.append("Required Domains: " + ", ".join(job.required_domains))
    if job.required_experience_level:
        role_domain_parts.append(f"Experience Level: {job.required_experience_level}")
    if role_domain_parts:
        parts.append("; ".join(role_domain_parts))

    # 3. Required & Preferred Skills
    skill_parts: List[str] = []
    if job.required_skills:
        skill_parts.append("Required Skills: " + ", ".join(job.required_skills))
    if job.preferred_skills:
        skill_parts.append("Preferred Skills: " + ", ".join(job.preferred_skills))
    if skill_parts:
        parts.append("\n".join(skill_parts))

    # 4. Keywords
    kw_parts: List[str] = []
    if job.required_keywords:
        kw_parts.append("Required Keywords: " + ", ".join(job.required_keywords))
    if job.preferred_keywords:
        kw_parts.append("Preferred Keywords: " + ", ".join(job.preferred_keywords))
    if kw_parts:
        parts.append("\n".join(kw_parts))

    # 5. Education Requirements
    if job.required_education or job.preferred_education:
        edu_reqs = job.required_education + job.preferred_education
        parts.append("Education Requirements: " + ", ".join(edu_reqs))

    combined = "\n\n".join(parts).strip()
    return combined if combined else "Empty job requirements"


def generate_embedding(
    text: Union[str, StructuredResume, JobRequirements], model_name: Optional[str] = None
) -> np.ndarray:
    """Generates normalized 1D float32 vector embedding for given input text or model."""
    if isinstance(text, StructuredResume):
        text = build_resume_embedding_text(text)
    elif isinstance(text, JobRequirements):
        text = build_job_embedding_text(text)

    if not text or not str(text).strip():
        text = "empty"

    model = get_embedding_model(model_name)
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    if not isinstance(embedding, np.ndarray):
        embedding = np.array(embedding, dtype=np.float32)

    # Ensure 1D array
    if embedding.ndim > 1:
        embedding = embedding.flatten()

    if embedding.size == 0:
        raise ValueError("Generated vector embedding is empty.")

    return embedding.astype(np.float32)


def generate_resume_embedding(
    resume: Union[StructuredResume, str], model_name: Optional[str] = None
) -> np.ndarray:
    """Generates normalized 1D float32 vector embedding for a StructuredResume or resume text string."""
    if isinstance(resume, StructuredResume):
        text = build_resume_embedding_text(resume)
    else:
        text = str(resume)
    return generate_embedding(text, model_name=model_name)


def generate_job_embedding(
    job: Union[JobRequirements, str], model_name: Optional[str] = None
) -> np.ndarray:
    """Generates normalized 1D float32 vector embedding for JobRequirements or job text string."""
    if isinstance(job, JobRequirements):
        text = build_job_embedding_text(job)
    else:
        text = str(job)
    return generate_embedding(text, model_name=model_name)


def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculates cosine similarity between two 1D vector embeddings.

    cosine_sim = (vec1 . vec2) / (||vec1|| * ||vec2||)
    """
    if vec1.ndim > 1:
        vec1 = vec1.flatten()
    if vec2.ndim > 1:
        vec2 = vec2.flatten()

    if vec1.shape != vec2.shape:
        raise ValueError(
            f"Vector dimension mismatch for similarity calculation: {vec1.shape} vs {vec2.shape}"
        )

    if np.isnan(vec1).any() or np.isnan(vec2).any() or np.isinf(vec1).any() or np.isinf(vec2).any():
        return 0.0

    norm1 = float(np.linalg.norm(vec1))
    norm2 = float(np.linalg.norm(vec2))

    if norm1 == 0.0 or norm2 == 0.0 or np.isnan(norm1) or np.isnan(norm2) or np.isinf(norm1) or np.isinf(norm2):
        return 0.0

    dot_product = float(np.dot(vec1, vec2))
    if np.isnan(dot_product) or np.isinf(dot_product):
        return 0.0

    cosine_sim = dot_product / (norm1 * norm2)

    # Clamp cosine similarity to [-1.0, 1.0] to handle floating point precision
    return float(np.clip(cosine_sim, -1.0, 1.0))


def normalize_similarity_score(cosine_sim: float) -> float:
    """Normalizes raw cosine similarity (-1.0 to 1.0) into a 0.0 to 100.0 score scale.

    Formula: score = ((cosine_sim + 1.0) / 2.0) * 100.0
    Clamped to [0.0, 100.0] and rounded to 2 decimal places.
    """
    score = ((cosine_sim + 1.0) / 2.0) * 100.0
    clamped = float(np.clip(score, 0.0, 100.0))
    return round(clamped, 2)


def get_similarity_tier(score: float) -> str:
    """Determines human-readable similarity match tier based on 0-100 score."""
    if score >= 80.0:
        return "Strong Match"
    elif score >= 65.0:
        return "Good Match"
    elif score >= 50.0:
        return "Moderate Match"
    else:
        return "Low Match"
