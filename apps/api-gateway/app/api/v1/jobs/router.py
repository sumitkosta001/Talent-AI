"""Jobs REST API Router (Day 32).

Provides endpoints for job requirements vector indexing into FAISS,
job vector removal, vector search for matching candidate resumes, and FAISS index status.
"""

import logging
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Query

from app.services.resume_processing.models import (
    JobRequirements,
    StructuredResume,
    FAISSIndexResult,
    FAISSSearchResult,
    CandidateRecommendationResponse,
)

from app.services.resume_processing.faiss_index_service import (
    index_job,
    remove_job_index,
    search_resumes_for_job,
    get_job_faiss_index,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "/index",
    response_model=FAISSIndexResult,
    status_code=status.HTTP_200_OK,
    summary="Index job requirements vector in FAISS",
    description="Generate Day 31 vector embedding for job requirements and index it into the Job FAISS vector index (Day 32).",
)
async def index_job_vector(
    job_requirements: JobRequirements,
) -> FAISSIndexResult:
    """Index job requirements vector into FAISS."""
    try:
        res = index_job(job_requirements.job_id, job_requirements)
        return res
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Job FAISS indexing failed: {str(err)}")


@router.delete(
    "/{job_id}/index",
    status_code=status.HTTP_200_OK,
    summary="Remove job vector from FAISS",
    description="Remove job vector embedding from the Job FAISS vector index (Day 32).",
)
async def remove_job_vector(job_id: str) -> dict:
    """Remove job vector from FAISS."""
    removed = remove_job_index(job_id)
    return {"job_id": job_id, "removed": removed}


@router.post(
    "/search-resumes",
    response_model=FAISSSearchResult,
    status_code=status.HTTP_200_OK,
    summary="Search FAISS Resume vector index using job requirements",
    description="Query Resume FAISS vector index using job requirements embedding to find top-k matching candidate resumes (Day 32).",
)
async def search_resumes_for_job_endpoint(
    job_requirements: JobRequirements,
    top_k: int = Query(default=10, ge=1, le=100),
) -> FAISSSearchResult:
    """Search Resume FAISS vector index using job requirements."""
    try:
        result = search_resumes_for_job(job_requirements, top_k=top_k)
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"FAISS resume search failed: {str(err)}")


@router.get(
    "/faiss-status",
    status_code=status.HTTP_200_OK,
    summary="Get Job FAISS index status",
    description="Get vector count and status of the Job FAISS vector index (Day 32).",
)
async def get_job_faiss_status() -> dict:
    """Get Job FAISS index status."""
    job_index = get_job_faiss_index()
    return {
        "index_name": job_index.index_name,
        "is_loaded": job_index.is_loaded(),
        "vector_count": job_index.count(),
        "dimension": job_index.dimension,
        "index_type": job_index.index_type,
    }


class CandidateRecommendationRequest(BaseModel):
    """Payload for candidate recommendation endpoint (Day 33)."""

    job_requirements: JobRequirements
    candidate_resumes: Optional[List[StructuredResume]] = None


@router.post(
    "/recommend-candidates",
    response_model=CandidateRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Recommend candidate resumes for job requirements",
    description="Query candidate resume recommendations for a JobRequirements payload combining FAISS vector search and Day 30 ATS scoring (Day 33).",
)
async def recommend_candidates_endpoint(
    payload: CandidateRecommendationRequest,
    top_k: int = Query(default=10, ge=1, le=50),
) -> CandidateRecommendationResponse:
    """Recommend candidate resumes for job requirements."""
    from app.services.resume_processing import CandidateRecommendationResponse, recommend_candidates_for_job

    try:
        result = recommend_candidates_for_job(
            payload.job_requirements, candidate_resumes=payload.candidate_resumes, top_k=top_k
        )
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Candidate recommendation failed: {str(err)}")

