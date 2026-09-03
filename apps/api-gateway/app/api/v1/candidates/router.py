"""Candidate Profile REST API Routers."""

from typing import Annotated, List, Optional

from uuid import UUID
import urllib.parse
from fastapi import APIRouter, Depends, status, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.models.user import User
from app.auth.dependencies import get_current_candidate
from app.repositories.candidate.profile_repository import CandidateProfileRepository
from app.repositories.candidate.education_repository import EducationRepository
from app.repositories.candidate.experience_repository import ExperienceRepository
from app.repositories.candidate.skill_repository import SkillRepository
from app.repositories.candidate.resume_repository import ResumeRepository
from app.services.candidate.candidate_service import CandidateService
from app.services.candidate.resume_service import ResumeService
from app.services.storage.minio_service import MinioStorageService
from app.schemas.candidate.profile import (
    CandidateProfileUpdate,
    CandidateProfileDetailResponse,
)
from app.schemas.candidate.education import (
    EducationCreate,
    EducationUpdate,
    EducationResponse,
)
from app.schemas.candidate.experience import (
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse,
)
from app.schemas.candidate.skill import (
    SkillCreate,
    SkillUpdate,
    SkillResponse,
)
from app.schemas.candidate.resume import (
    ResumeResponse,
    ResumeUploadResponse,
    PaginatedResumeResponse,
    ResumeRestoreResponse,
    ResumeProcessingResponse,
)
from pydantic import BaseModel, Field

from app.services.resume_processing.models import (
    FAISSIndexResult,
    FAISSSearchResult,
    JobRecommendationResponse,
    StructuredResume,
    GeneratedInterviewQuestions,
    ResumeClassification,
)


from app.services.resume_processing import JobRequirements, ATSScore, SimilarityMatch




router = APIRouter(
    prefix="/candidates",
    tags=["Candidate Profile"],
)


def get_candidate_service(db: AsyncSession = Depends(get_db)) -> CandidateService:
    """Dependency provider injecting CandidateService with configured repositories."""
    profile_repo = CandidateProfileRepository(db)
    education_repo = EducationRepository(db)
    experience_repo = ExperienceRepository(db)
    skill_repo = SkillRepository(db)
    return CandidateService(
        profile_repo=profile_repo,
        education_repo=education_repo,
        experience_repo=experience_repo,
        skill_repo=skill_repo,
    )


def get_resume_service(db: AsyncSession = Depends(get_db)) -> ResumeService:
    """Dependency provider injecting ResumeService with configured repositories."""
    profile_repo = CandidateProfileRepository(db)
    resume_repo = ResumeRepository(db)
    storage_service = MinioStorageService()
    return ResumeService(
        profile_repo=profile_repo,
        resume_repo=resume_repo,
        storage_service=storage_service,
    )


# ==============================================================================
# PROFILE ENDPOINTS
# ==============================================================================

@router.get(
    "/me",
    response_model=CandidateProfileDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve current candidate profile",
    description="Retrieve the authenticated candidate's profile, including education, experience, and skills.",
)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> CandidateProfileDetailResponse:
    """Get active candidate's profile details."""
    profile = await service.get_or_create_profile(current_user.id)
    return CandidateProfileDetailResponse.model_validate(profile)


@router.patch(
    "/me",
    response_model=CandidateProfileDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Update candidate profile details",
    description="Perform a partial update on the candidate profile details and return the updated profile.",
)
async def update_my_profile(
    updates: CandidateProfileUpdate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> CandidateProfileDetailResponse:
    """Perform partial update on active candidate's profile."""
    profile = await service.update_profile(current_user.id, updates)
    return CandidateProfileDetailResponse.model_validate(profile)


# ==============================================================================
# EDUCATION ENDPOINTS
# ==============================================================================

@router.post(
    "/me/education",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add education entry",
)
async def add_education_entry(
    data: EducationCreate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> EducationResponse:
    """Add a new education history record."""
    edu = await service.add_education(current_user.id, data)
    return EducationResponse.model_validate(edu)


@router.get(
    "/me/education",
    response_model=List[EducationResponse],
    status_code=status.HTTP_200_OK,
    summary="List education history entries",
)
async def get_education_entries(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> List[EducationResponse]:
    """Retrieve all education history records."""
    edu_list = await service.get_education_list(current_user.id)
    return [EducationResponse.model_validate(edu) for edu in edu_list]


@router.patch(
    "/me/education/{education_id}",
    response_model=EducationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update education entry details",
)
async def update_education_entry(
    education_id: str,
    data: EducationUpdate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> EducationResponse:
    """Update details of a specific education record."""
    edu = await service.update_education(current_user.id, education_id, data)
    return EducationResponse.model_validate(edu)


@router.delete(
    "/me/education/{education_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete education entry",
)
async def delete_education_entry(
    education_id: str,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
):
    """Delete a specific education record."""
    await service.delete_education(current_user.id, education_id)
    return {"success": True, "message": "Education entry deleted successfully."}


# ==============================================================================
# WORK EXPERIENCE ENDPOINTS
# ==============================================================================

@router.post(
    "/me/experience",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add work experience entry",
)
async def add_experience_entry(
    data: ExperienceCreate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> ExperienceResponse:
    """Add a new work experience history record."""
    exp = await service.add_experience(current_user.id, data)
    return ExperienceResponse.model_validate(exp)


@router.get(
    "/me/experience",
    response_model=List[ExperienceResponse],
    status_code=status.HTTP_200_OK,
    summary="List work experience entries",
)
async def get_experience_entries(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> List[ExperienceResponse]:
    """Retrieve all work experience history records."""
    exp_list = await service.get_experience_list(current_user.id)
    return [ExperienceResponse.model_validate(exp) for exp in exp_list]


@router.patch(
    "/me/experience/{experience_id}",
    response_model=ExperienceResponse,
    status_code=status.HTTP_200_OK,
    summary="Update work experience details",
)
async def update_experience_entry(
    experience_id: str,
    data: ExperienceUpdate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> ExperienceResponse:
    """Update details of a specific work experience record."""
    exp = await service.update_experience(current_user.id, experience_id, data)
    return ExperienceResponse.model_validate(exp)


@router.delete(
    "/me/experience/{experience_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete work experience entry",
)
async def delete_experience_entry(
    experience_id: str,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
):
    """Delete a specific work experience record."""
    await service.delete_experience(current_user.id, experience_id)
    return {"success": True, "message": "Experience entry deleted successfully."}


# ==============================================================================
# SKILLS ENDPOINTS
# ==============================================================================

@router.post(
    "/me/skills",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add skill entry",
)
async def add_skill_entry(
    data: SkillCreate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> SkillResponse:
    """Add a new skill selection."""
    skill = await service.add_skill(current_user.id, data)
    return SkillResponse.model_validate(skill)


@router.get(
    "/me/skills",
    response_model=List[SkillResponse],
    status_code=status.HTTP_200_OK,
    summary="List candidate skills",
)
async def get_skill_entries(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> List[SkillResponse]:
    """Retrieve all selected candidate skills."""
    skills_list = await service.get_skills_list(current_user.id)
    return [SkillResponse.model_validate(s) for s in skills_list]


@router.patch(
    "/me/skills/{skill_id}",
    response_model=SkillResponse,
    status_code=status.HTTP_200_OK,
    summary="Update skill category or proficiency",
)
async def update_skill_entry(
    skill_id: str,
    data: SkillUpdate,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
) -> SkillResponse:
    """Update details of a specific skill record."""
    skill = await service.update_skill(current_user.id, skill_id, data)
    return SkillResponse.model_validate(skill)


@router.delete(
    "/me/skills/{skill_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove skill entry",
)
async def delete_skill_entry(
    skill_id: str,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
):
    """Remove a specific skill from candidate profile."""
    await service.delete_skill(current_user.id, skill_id)
    return {"success": True, "message": "Skill entry deleted successfully."}


# ==============================================================================
# RESUME ENDPOINTS
# ==============================================================================

@router.post(
    "/me/resumes",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload candidate resume",
    description=(
        "Upload a PDF or DOCX resume file for the authenticated candidate. "
        "The file is validated for extension, MIME type, file content signature, "
        "and size before metadata is persisted. The candidate is determined from "
        "the JWT token — no candidate_id is accepted from the client."
    ),
)
async def upload_my_resume(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
    file: UploadFile = File(..., description="Resume file (PDF or DOCX, max 10 MB)"),
) -> ResumeUploadResponse:
    """Upload and validate a candidate resume file.

    Accepts multipart/form-data with a single file field.
    Validates file size, extension, MIME type, and content signature.
    Creates a Resume database record associated with the authenticated candidate.
    """
    resume = await service.upload_resume(current_user.id, file)
    return ResumeUploadResponse(
        success=True,
        message="Resume uploaded successfully.",
        resume=ResumeResponse.model_validate(resume),
    )


@router.get(
    "/me/resumes",
    response_model=PaginatedResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="List candidate resumes",
    description=(
        "Retrieve a paginated, sorted list of resumes uploaded by the authenticated candidate. "
        "Allows sorting by uploaded_at, file_size_bytes, status, original_filename, or version. "
        "Candidate profile is determined server-side from token claims."
    ),
)
async def list_my_resumes(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
    page: int = Query(1, ge=1, description="Page number (minimum 1)"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page (between 1 and 50)"),
    sort_by: str = Query("uploaded_at", description="Field to sort results by"),
    sort_order: str = Query("desc", description="Sort direction ('asc' or 'desc')"),
) -> PaginatedResumeResponse:
    """List resumes for the authenticated candidate with pagination and sorting."""
    # Extra validation for sorting to raise HTTP 400 for invalid sort options
    if sort_by not in ["uploaded_at", "file_size_bytes", "status", "original_filename", "version"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Invalid sort field '{sort_by}'.")
    if sort_order not in ["asc", "desc"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")

    data = await service.list_resumes(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return PaginatedResumeResponse.model_validate(data)


@router.get(
    "/me/resumes/current",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current resume version",
    description="Retrieve metadata for the candidate's current (active) resume version.",
)
async def get_current_resume(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeResponse:
    """Retrieve the current active resume version for the authenticated candidate."""
    resume = await service.get_current_resume(current_user.id)
    return ResumeResponse.model_validate(resume)


@router.get(
    "/me/resumes/history",
    response_model=PaginatedResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get resume upload history and processing status",
    description=(
        "Retrieve upload and processing lifecycle history for the authenticated candidate. "
        "Default ordering is newest upload first (uploaded_at desc). "
        "Exposes processing lifecycle timestamps and failure reasons."
    ),
)
async def get_my_resume_history(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
    page: int = Query(1, ge=1, description="Page number (minimum 1)"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page (between 1 and 50)"),
    sort_by: str = Query("uploaded_at", description="Field to sort results by"),
    sort_order: str = Query("desc", description="Sort direction ('asc' or 'desc')"),
) -> PaginatedResumeResponse:
    """Retrieve paginated resume upload history and processing status for candidate."""
    if sort_by not in ["uploaded_at", "file_size_bytes", "status", "original_filename", "version"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Invalid sort field '{sort_by}'.")
    if sort_order not in ["asc", "desc"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")

    data = await service.get_resume_history(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return PaginatedResumeResponse.model_validate(data)


@router.get(
    "/me/resumes/{resume_id}",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get resume metadata",
    description="Retrieve metadata for a specific resume belonging to the authenticated candidate.",
)
async def get_resume_metadata(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeResponse:
    """Retrieve metadata of a specific candidate resume securely."""
    resume = await service.get_resume_metadata(current_user.id, resume_id)
    return ResumeResponse.model_validate(resume)


@router.get(
    "/me/resumes/{resume_id}/preview",
    status_code=status.HTTP_200_OK,
    summary="Preview resume PDF inline",
    description="Stream a specific candidate's resume for inline browser previewing.",
)
async def preview_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
):
    """Retrieve the resume file stream for inline rendering (preview) securely."""
    resume, stream = await service.get_resume_file_stream(current_user.id, resume_id)

    # Sanitize original filename (remove CR/LF, strip double quotes)
    safe_filename = resume.original_filename.replace("\r", "").replace("\n", "").replace('"', "")
    encoded_filename = urllib.parse.quote(safe_filename)

    # Generate ASCII-only fallback filename for Latin-1 header support in Starlette
    ascii_filename = safe_filename.encode("ascii", errors="ignore").decode("ascii")
    if not ascii_filename.strip() or ascii_filename.startswith("."):
        ext = resume.file_extension or ".pdf"
        ascii_filename = f"resume{ext}"

    headers = {
        "Content-Disposition": f'inline; filename="{ascii_filename}"; filename*=UTF-8\'\'{encoded_filename}'
    }

    def file_generator():
        try:
            while chunk := stream.read(65536):
                yield chunk
        finally:
            stream.close()
            if hasattr(stream, "release_conn"):
                stream.release_conn()


    return StreamingResponse(
        file_generator(),
        media_type=resume.mime_type,
        headers=headers,
    )


@router.get(
    "/me/resumes/{resume_id}/download",
    status_code=status.HTTP_200_OK,
    summary="Download resume securely",
    description="Securely download a specific candidate resume as an attachment.",
)
async def download_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
):
    """Retrieve the resume file stream as an attachment download securely."""
    resume, stream = await service.get_resume_file_stream(current_user.id, resume_id)

    # Sanitize original filename (remove CR/LF, strip double quotes)
    safe_filename = resume.original_filename.replace("\r", "").replace("\n", "").replace('"', "")
    encoded_filename = urllib.parse.quote(safe_filename)

    # Generate ASCII-only fallback filename for Latin-1 header support in Starlette
    ascii_filename = safe_filename.encode("ascii", errors="ignore").decode("ascii")
    if not ascii_filename.strip() or ascii_filename.startswith("."):
        ext = resume.file_extension or ".pdf"
        ascii_filename = f"resume{ext}"

    headers = {
        "Content-Disposition": f'attachment; filename="{ascii_filename}"; filename*=UTF-8\'\'{encoded_filename}'
    }

    def file_generator():
        try:
            while chunk := stream.read(65536):
                yield chunk
        finally:
            stream.close()
            if hasattr(stream, "release_conn"):
                stream.release_conn()


    return StreamingResponse(
        file_generator(),
        media_type=resume.mime_type,
        headers=headers,
    )


@router.post(
    "/me/resumes/{resume_id}/restore",
    response_model=ResumeRestoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Restore resume version",
    description="Restore a previous resume version as the current active version.",
)
async def restore_resume_version(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeRestoreResponse:
    """Restore a previous resume version as current."""
    resume = await service.restore_resume_version(current_user.id, resume_id)
    return ResumeRestoreResponse(
        success=True,
        message="Resume version restored successfully.",
        resume=ResumeResponse.model_validate(resume),
    )


@router.post(
    "/me/resumes/{resume_id}/process",
    response_model=ResumeProcessingResponse,
    status_code=status.HTTP_200_OK,
    summary="Process candidate resume",
    description="Execute document parsing and processing lifecycle on an uploaded candidate resume.",
)
async def process_candidate_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeProcessingResponse:
    """Trigger processing lifecycle on an uploaded resume."""
    resume = await service.process_resume(current_user.id, resume_id)
    return ResumeProcessingResponse(
        success=(resume.status.value != "failed"),
        message="Resume processing completed." if resume.status.value == "processed" else "Resume processing failed.",
        resume=ResumeResponse.model_validate(resume),
    )


@router.post(
    "/me/resumes/{resume_id}/retry",
    response_model=ResumeProcessingResponse,
    status_code=status.HTTP_200_OK,
    summary="Retry resume processing",
    description="Retry processing lifecycle on a failed candidate resume without incrementing version or changing storage key.",
)
async def retry_candidate_resume_processing(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeProcessingResponse:
    """Retry processing for a failed resume document securely."""
    resume = await service.retry_resume_processing(current_user.id, resume_id)
    return ResumeProcessingResponse(
        success=(resume.status.value != "failed"),
        message="Resume processing completed successfully." if resume.status.value == "processed" else "Resume processing failed.",
        resume=ResumeResponse.model_validate(resume),
    )


@router.delete(
    "/me/resumes/{resume_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete candidate resume",
    description="Soft-delete a specific candidate's resume from database and remove its S3 object storage file. If the deleted resume was the current version, the highest remaining active version is auto-promoted.",
)
async def delete_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
):
    """Soft-delete candidate resume securely with auto-promotion."""
    return await service.delete_resume(current_user.id, resume_id)

@router.get(
    "/me/resumes/{resume_id}/structured",
    response_model=StructuredResume,
    status_code=status.HTTP_200_OK,
    summary="Get canonical structured resume JSON",
    description="Retrieve canonical Day 28 structured JSON representation (skills, education, experience, projects, metadata) for processed candidate resume.",
)
async def get_candidate_structured_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> StructuredResume:
    """Retrieve Day 28 canonical structured JSON for candidate resume."""
    from fastapi import HTTPException

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    return StructuredResume.model_validate(resume.structured_data)


@router.get(
    "/me/resumes/{resume_id}/classification",
    response_model=ResumeClassification,
    status_code=status.HTTP_200_OK,
    summary="Get candidate resume domain and role classification",
    description="Retrieve explainable domain classification, predicted role, experience level, confidence, and scores for processed candidate resume (Day 29).",
)
async def get_candidate_resume_classification(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeClassification:
    """Retrieve Day 29 classification for candidate resume."""
    from fastapi import HTTPException
    from app.services.resume_processing import StructuredResume, classify_resume

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    if structured.classification:
        return structured.classification

    try:
        classification = classify_resume(structured)
        return classification
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed to classify resume: {str(err)}")


@router.post(
    "/me/resumes/{resume_id}/ats-score",

    response_model=ATSScore,
    status_code=status.HTTP_200_OK,
    summary="Calculate job-specific ATS score",
    description="Evaluate processed candidate resume against specified JobRequirements and return explainable ATS score breakdown (Day 30).",
)
async def score_candidate_resume(
    resume_id: UUID,
    job_requirements: JobRequirements,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ATSScore:
    """Calculate job-specific ATS score for candidate resume."""
    from fastapi import HTTPException
    from app.services.resume_processing import StructuredResume, score_resume_against_job

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    try:
        ats_result = score_resume_against_job(structured, job_requirements)
        return ats_result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))


@router.post(
    "/me/resumes/{resume_id}/similarity-score",
    response_model=SimilarityMatch,
    status_code=status.HTTP_200_OK,
    summary="Calculate semantic embedding similarity score",
    description="Calculate semantic vector embedding similarity match between processed candidate resume and specified JobRequirements using sentence-transformers (Day 31).",
)
async def calculate_resume_similarity(
    resume_id: UUID,
    job_requirements: JobRequirements,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> SimilarityMatch:
    """Calculate semantic embedding similarity score for candidate resume against job requirements."""
    from fastapi import HTTPException
    from app.services.resume_processing import StructuredResume, SimilarityMatch, calculate_resume_job_similarity

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    try:
        match_result = calculate_resume_job_similarity(structured, job_requirements)
        return match_result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed to calculate similarity score: {str(err)}")


# Day 32 FAISS Vector Indexing & Search Endpoints

@router.post(
    "/me/resumes/{resume_id}/faiss-index",
    response_model=FAISSIndexResult,
    status_code=status.HTTP_200_OK,
    summary="Index candidate resume vector in FAISS",
    description="Generate Day 31 vector embedding for processed candidate resume and index it into the Resume FAISS vector index (Day 32).",
)
async def index_candidate_resume_vector(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> FAISSIndexResult:
    """Index candidate resume vector into FAISS."""
    from fastapi import HTTPException
    from app.services.resume_processing import StructuredResume, FAISSIndexResult, index_resume

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    try:
        res = index_resume(resume_id, structured)
        return res
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"FAISS indexing failed: {str(err)}")


@router.delete(
    "/me/resumes/{resume_id}/faiss-index",
    status_code=status.HTTP_200_OK,
    summary="Remove candidate resume vector from FAISS",
    description="Remove candidate resume vector embedding from the Resume FAISS vector index (Day 32).",
)
async def remove_candidate_resume_vector(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> dict:
    """Remove candidate resume vector from FAISS."""
    from app.services.resume_processing import remove_resume_index

    # Confirm candidate owns the resume
    await service.get_resume_metadata(current_user.id, resume_id)
    removed = remove_resume_index(resume_id)
    return {"resume_id": str(resume_id), "removed": removed}


@router.post(
    "/me/resumes/{resume_id}/search-jobs",
    response_model=FAISSSearchResult,
    status_code=status.HTTP_200_OK,
    summary="Search FAISS Job vector index using candidate resume",
    description="Query Job FAISS vector index using candidate resume embedding to find top-k matching jobs (Day 32).",
)
async def search_jobs_for_resume_endpoint(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
    top_k: int = 10,
) -> FAISSSearchResult:
    """Search Job FAISS vector index using candidate resume."""
    from fastapi import HTTPException
    from app.services.resume_processing import StructuredResume, FAISSSearchResult, search_jobs_for_resume

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    try:
        result = search_jobs_for_resume(structured, top_k=top_k)
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"FAISS search failed: {str(err)}")


# ==============================================================================
# DAY 33 RECOMMENDATIONS ENDPOINTS
# ==============================================================================

class CandidateJobRecommendationRequest(BaseModel):
    """Optional request payload for candidate job recommendations."""

    jobs: Optional[List[JobRequirements]] = None


@router.post(
    "/me/resumes/{resume_id}/recommendations/jobs",
    response_model=JobRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get job recommendations for authenticated candidate resume",
    description="Retrieve ranked, evidence-explained job recommendations combining FAISS vector search and Day 30 ATS scoring (Day 33).",
)
async def get_job_recommendations_for_my_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
    top_k: int = Query(default=10, ge=1, le=50),
    body: Optional[CandidateJobRecommendationRequest] = None,
) -> JobRecommendationResponse:
    """Get job recommendations for candidate's processed resume."""
    from fastapi import HTTPException
    from app.services.resume_processing import StructuredResume, JobRecommendationResponse, recommend_jobs_for_resume

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    candidate_jobs = body.jobs if body else None
    try:
        result = recommend_jobs_for_resume(structured, candidate_jobs=candidate_jobs, top_k=top_k)
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Job recommendation failed: {str(err)}")


class GeneralJobRecommendationRequest(BaseModel):
    """Payload for general job recommendation endpoint."""

    structured_resume: StructuredResume
    jobs: Optional[List[JobRequirements]] = None


@router.post(
    "/recommend-jobs",
    response_model=JobRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Recommend jobs for structured resume payload",
    description="Query job recommendations for a StructuredResume payload combining FAISS vector search and Day 30 ATS scoring (Day 33).",
)
async def recommend_jobs_endpoint(
    payload: GeneralJobRecommendationRequest,
    top_k: int = Query(default=10, ge=1, le=50),
) -> JobRecommendationResponse:
    """Recommend jobs for a given structured resume payload."""
    from fastapi import HTTPException
    from app.services.resume_processing import JobRecommendationResponse, recommend_jobs_for_resume

    try:
        result = recommend_jobs_for_resume(payload.structured_resume, candidate_jobs=payload.jobs, top_k=top_k)
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Job recommendation failed: {str(err)}")


# ==============================================================================
# DAY 34 AI INTERVIEW QUESTIONS ENDPOINTS
# ==============================================================================

class GeneralInterviewQuestionRequest(BaseModel):
    """Payload for general interview question generation endpoint."""

    structured_resume: StructuredResume
    count: int = Field(default=10, ge=1, le=50)
    difficulty: str = "MEDIUM"
    categories: Optional[List[str]] = None
    provider: str = "auto"


@router.post(
    "/me/resumes/{resume_id}/interview-questions",
    response_model=GeneratedInterviewQuestions,
    status_code=status.HTTP_200_OK,
    summary="Generate interview questions for authenticated candidate resume",
    description="Generate candidate-tailored role, skill, project, and experience interview questions (Day 34).",
)
async def generate_interview_questions_for_my_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[ResumeService, Depends(get_resume_service)],
    count: int = Query(default=10, ge=1, le=50),
    difficulty: str = Query(default="MEDIUM"),
    categories: Optional[List[str]] = Query(default=None),
    provider: str = Query(default="auto"),
) -> GeneratedInterviewQuestions:
    """Generate interview questions for candidate's processed resume."""
    from fastapi import HTTPException
    from app.services.resume_processing import (
        StructuredResume,
        GeneratedInterviewQuestions,
        generate_interview_questions,
    )

    resume = await service.get_resume_metadata(current_user.id, resume_id)
    if not resume.structured_data:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been processed into structured format yet. Please trigger processing first."
        )

    structured = StructuredResume.model_validate(resume.structured_data)
    try:
        result = generate_interview_questions(
            structured, count=count, difficulty=difficulty, categories=categories, provider=provider
        )
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Interview question generation failed: {str(err)}")


@router.post(
    "/generate-interview-questions",
    response_model=GeneratedInterviewQuestions,
    status_code=status.HTTP_200_OK,
    summary="Generate interview questions for structured resume payload",
    description="Generate interview questions for a provided StructuredResume payload (Day 34).",
)
async def generate_interview_questions_endpoint(
    payload: GeneralInterviewQuestionRequest,
) -> GeneratedInterviewQuestions:
    """Generate interview questions for a given structured resume payload."""
    from fastapi import HTTPException
    from app.services.resume_processing import GeneratedInterviewQuestions, generate_interview_questions

    try:
        result = generate_interview_questions(
            payload.structured_resume,
            count=payload.count,
            difficulty=payload.difficulty,
            categories=payload.categories,
            provider=payload.provider,
        )
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Interview question generation failed: {str(err)}")





