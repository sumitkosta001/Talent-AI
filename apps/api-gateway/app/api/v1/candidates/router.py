"""Candidate Profile REST API Routers."""

from typing import Annotated, List
from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import io
import os

from app.database.dependencies import get_db
from app.models.user import User
from app.auth.dependencies import get_current_candidate
from app.repositories.candidate.profile_repository import CandidateProfileRepository
from app.repositories.candidate.education_repository import EducationRepository
from app.repositories.candidate.experience_repository import ExperienceRepository
from app.repositories.candidate.skill_repository import SkillRepository
from app.services.candidate.candidate_service import CandidateService
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
    "/me/resume/upload",
    status_code=status.HTTP_200_OK,
    summary="Upload candidate resume",
)
async def upload_my_resume(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
    file: UploadFile = File(...),
):
    """Upload and save candidate's primary resume PDF file."""
    # Ensure uploads directory exists
    upload_dir = os.path.join(os.getcwd(), "uploads", "resumes")
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, f"{current_user.id}.pdf")
    
    # Save the file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
        
    # Update candidate profile with the resume URL/path
    profile = await service.get_or_create_profile(current_user.id)
    profile.resume_url = "/api/v1/candidates/me/resume/download"
    await service.profile_repo.update(profile)
    
    return {
        "success": True,
        "message": "Resume uploaded successfully.",
        "filename": file.filename,
    }


@router.get(
    "/me/resume/download",
    status_code=status.HTTP_200_OK,
    summary="Download candidate resume file",
)
async def download_my_resume(
    current_user: Annotated[User, Depends(get_current_candidate)],
    service: Annotated[CandidateService, Depends(get_candidate_service)],
):
    """Retrieve and stream the candidate's primary resume PDF file."""
    upload_dir = os.path.join(os.getcwd(), "uploads", "resumes")
    file_path = os.path.join(upload_dir, f"{current_user.id}.pdf")
    
    filename = f"{current_user.full_name.replace(' ', '_')}_Resume.pdf"
    
    if os.path.exists(file_path):
        # Open and stream the file
        def iterfile():
            with open(file_path, "rb") as f:
                yield from f
        
        return StreamingResponse(
            iterfile(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    else:
        # Generate and stream a dummy PDF with candidate name
        pdf_data = generate_dummy_pdf(current_user.full_name)
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )


def generate_dummy_pdf(candidate_name: str) -> bytes:
    """Generate a simple, valid in-memory PDF file for fallback downloading."""
    pdf_template = (
        "%PDF-1.4\n"
        "1 0 obj\n"
        "<< /Type /Catalog /Pages 2 0 R >>\n"
        "endobj\n"
        "2 0 obj\n"
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        "endobj\n"
        "3 0 obj\n"
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\n"
        "endobj\n"
        "4 0 obj\n"
        f"<< /Length {50 + len(candidate_name)} >>\n"
        "stream\n"
        "BT\n"
        "/F1 12 Tf\n"
        "72 712 Td\n"
        f"({candidate_name} - Resume Document) Tj\n"
        "ET\n"
        "endstream\n"
        "endobj\n"
        "xref\n"
        "0 5\n"
        "0000000000 65535 f \n"
        "0000000009 00000 n \n"
        "0000000058 00000 n \n"
        "0000000115 00000 n \n"
        f"0000000{212 + len(candidate_name)} n \n"
        "trailer\n"
        "<< /Size 5 /Root 1 0 R >>\n"
        "startxref\n"
        f"{314 + len(candidate_name)}\n"
        "%%EOF"
    )
    return pdf_template.encode("utf-8")
