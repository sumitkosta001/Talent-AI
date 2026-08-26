"""Phase 4 — Day 31: Similarity Matcher.

Computes semantic embedding-based similarity match between structured candidate resumes
and job requirements using pretrained sentence transformers.
"""

import logging, time
from typing import Optional, Dict, Any

from app.services.resume_processing.models import StructuredResume, JobRequirements, SimilarityMatch
from app.services.resume_processing.embedding_service import (
    build_resume_embedding_text,
    build_job_embedding_text,
    generate_embedding,
    calculate_cosine_similarity,
    calculate_cosine_similarity as compute_cosine_similarity,
    normalize_similarity_score,
    get_similarity_tier,
    DEFAULT_MODEL_NAME,
)

logger = logging.getLogger(__name__)


def calculate_resume_job_similarity(
    resume: StructuredResume,
    job: JobRequirements,
    model_name: Optional[str] = None,
) -> SimilarityMatch:
    """Calculates semantic vector embedding similarity match between a StructuredResume and JobRequirements.

    Returns SimilarityMatch object with raw cosine similarity, normalized 0-100 score,
    model metadata, and match tier classification.
    """
    selected_model_name = model_name or DEFAULT_MODEL_NAME

    # 1. Build canonical texts
    resume_text = build_resume_embedding_text(resume)
    job_text = build_job_embedding_text(job)

    # 2. Generate embeddings
    start_time = time.time()
    resume_vec = generate_embedding(resume_text, model_name=selected_model_name)
    job_vec = generate_embedding(job_text, model_name=selected_model_name)
    elapsed_ms = (time.time() - start_time) * 1000.0

    # 3. Calculate similarity
    raw_cosine_sim = calculate_cosine_similarity(resume_vec, job_vec)
    similarity_score = normalize_similarity_score(raw_cosine_sim)
    similarity_tier = get_similarity_tier(similarity_score)

    dim = len(resume_vec) if hasattr(resume_vec, "__len__") else 384

    res_id_str = str(resume.resume_id) if resume.resume_id is not None else None
    job_id_str = str(job.job_id) if job.job_id is not None else None

    logger.info(
        "Computed similarity match for resume_id=%s, job_id=%s: score=%.2f, raw_sim=%.4f (%.2fms)",
        res_id_str,
        job_id_str,
        similarity_score,
        raw_cosine_sim,
        elapsed_ms,
    )

    return SimilarityMatch(
        resume_id=res_id_str,
        job_id=job_id_str,
        raw_cosine_similarity=round(raw_cosine_sim, 4),
        similarity_score=similarity_score,
        model_name=selected_model_name,
        embedding_dimension=dim,
        resume_text_length=len(resume_text),
        job_text_length=len(job_text),
        similarity_tier=similarity_tier,
        metadata={
            "execution_time_ms": round(elapsed_ms, 2),
            "scoring_method": "semantic_embedding_cosine",
        },
    )
