"""Candidate Profile REST API Routers."""

from typing import Annotated, List
from fastapi import APIRouter, Depends, status, File, UploadFile
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
)

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
    return ResumeService(
        profile_repo=profile_repo,
        resume_repo=resume_repo,
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

