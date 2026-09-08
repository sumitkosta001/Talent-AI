"""Jobs REST API Router (Day 32 & Phase 5 Steps 5 & 6).

Provides endpoints for:
1. Relational Job CRUD operations (Create DRAFT, Get by ID, Update, Soft-delete).
2. Controlled Status Lifecycle transitions (Publish, Unpublish, Close).
3. Phase 4 ML vector indexing into FAISS, vector search for matching resumes, and candidate recommendations.
"""

import logging
from uuid import UUID
from typing import Annotated, Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_company
from app.models.enums import WorkMode, JobStatus
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobPaginatedResponse
from app.services.job_service import JobService

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


# ==============================================================================
# PHASE 5 STEP 5: RELATIONAL JOB CRUD & PUBLIC SEARCH ENDPOINTS
# ==============================================================================

@router.get(
    "",
    response_model=JobPaginatedResponse,
    status_code=status.HTTP_200_OK,
    summary="Search public published job postings",
    description="Public candidate search endpoint returning published, non-deleted job postings with optional filters.",
)
async def search_public_jobs_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    q: Optional[str] = Query(None, description="Free-text search query"),
    location: Optional[str] = Query(None, description="Filter by location"),
    skills: Optional[str] = Query(None, description="Comma-separated skill names"),
    experience_months: Optional[int] = Query(None, ge=0, description="Minimum required experience in months"),
    salary_min: Optional[int] = Query(None, ge=0, description="Minimum salary threshold"),
    salary_max: Optional[int] = Query(None, ge=0, description="Maximum salary threshold"),
    work_mode: Optional[WorkMode] = Query(None, description="Filter by work mode"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    sort_by: str = Query("published_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort direction"),
) -> JobPaginatedResponse:
    """Search published job postings for public candidate discovery."""
    service = JobService(db)
    offset = (page - 1) * size
    skill_list = [s.strip() for s in skills.split(",") if s.strip()] if skills else None

    jobs, total, total_pages = await service.search_jobs(
        q=q,
        location=location,
        skills_str=skills,
        experience_months=experience_months,
        salary_min=salary_min,
        salary_max=salary_max,
        work_mode=work_mode,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return JobPaginatedResponse(
        items=[JobResponse.model_validate(j) for j in jobs],
        total=total,
        page=page,
        size=size,
        total_pages=total_pages,
    )

@router.get(
    "/company/me",
    response_model=JobPaginatedResponse,
    status_code=status.HTTP_200_OK,
    summary="List all company job postings for current recruiter",
    description="Fetches all non-deleted job postings (DRAFT, PUBLISHED, CLOSED) belonging to the authenticated recruiter's company.",
)
async def list_company_jobs_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=100),
) -> JobPaginatedResponse:
    """Get all company job postings for the authenticated recruiter."""
    service = JobService(db)
    offset = (page - 1) * size
    jobs, total, total_pages = await service.get_company_jobs(current_user, limit=size, offset=offset)
    return JobPaginatedResponse(
        items=[JobResponse.model_validate(j) for j in jobs],
        total=total,
        page=page,
        size=size,
        total_pages=total_pages,
    )

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new job posting",
    description="Registers a new job posting entity initialized in DRAFT status for the authenticated recruiter's company.",
    operation_id="create_job",
)
async def create_job_endpoint(
    payload: JobCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> JobResponse:
    """Create a new job posting in DRAFT status."""
    service = JobService(db)
    job = await service.create_job(payload, user=current_user)
    return JobResponse.model_validate(job)

# Phase 4 FAISS endpoints
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


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Get job posting details by ID",
    description="Fetches non-deleted job posting details for the specified job UUID.",
    operation_id="get_job",
)
async def get_job_endpoint(
    job_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JobResponse:
    """Get job posting details by ID."""
    service = JobService(db)
    job = await service.get_job(job_id)
    return JobResponse.model_validate(job)


@router.patch(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Update job posting details",
    description="Updates existing job posting fields with company ownership verification.",
    operation_id="update_job",
)
async def update_job_endpoint(
    job_id: UUID,
    payload: JobUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> JobResponse:
    """Update job posting details with company ownership check."""
    service = JobService(db)
    job = await service.update_job(job_id, payload, user=current_user)
    return JobResponse.model_validate(job)


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete job posting",
    description="Soft-deletes the job posting with company ownership verification.",
    operation_id="delete_job",
)
async def delete_job_endpoint(
    job_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> None:
    """Soft delete job posting with company ownership check."""
    service = JobService(db)
    await service.delete_job(job_id, user=current_user)


# ==============================================================================
# PHASE 5 STEP 6: JOB PUBLISHING & STATUS LIFECYCLE ENDPOINTS
# ==============================================================================

@router.post(
    "/{job_id}/publish",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Publish job posting",
    description="Transitions a DRAFT job posting to PUBLISHED status with company ownership verification.",
)
async def publish_job_endpoint(
    job_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> JobResponse:
    """Publish a draft job posting."""
    service = JobService(db)
    job = await service.publish_job(job_id, user=current_user)
    return JobResponse.model_validate(job)


@router.post(
    "/{job_id}/unpublish",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Unpublish job posting",
    description="Transitions a PUBLISHED job posting back to DRAFT status with company ownership verification.",
)
async def unpublish_job_endpoint(
    job_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> JobResponse:
    """Unpublish a published job posting back to draft."""
    service = JobService(db)
    job = await service.unpublish_job(job_id, user=current_user)
    return JobResponse.model_validate(job)


@router.post(
    "/{job_id}/close",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Close job posting",
    description="Transitions a PUBLISHED job posting to CLOSED status with company ownership verification.",
)
async def close_job_endpoint(
    job_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> JobResponse:
    """Close a published job posting."""
    service = JobService(db)
    job = await service.close_job(job_id, user=current_user)
    return JobResponse.model_validate(job)


# ==============================================================================
# PHASE 4: FAISS VECTOR & CANDIDATE RECOMMENDATION ENDPOINTS
# ==============================================================================
# Phase 4 FAISS endpoints moved
