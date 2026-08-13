"""Candidate Profile Module Schemas Package."""

from app.schemas.candidate.profile import (
    CandidateProfileCreate,
    CandidateProfileUpdate,
    CandidateProfileResponse,
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

__all__ = [
    "CandidateProfileCreate",
    "CandidateProfileUpdate",
    "CandidateProfileResponse",
    "CandidateProfileDetailResponse",
    "EducationCreate",
    "EducationUpdate",
    "EducationResponse",
    "ExperienceCreate",
    "ExperienceUpdate",
    "ExperienceResponse",
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    "ResumeResponse",
    "ResumeUploadResponse",
]

