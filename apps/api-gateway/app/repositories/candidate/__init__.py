"""Candidate Module Repositories Package."""

from app.repositories.candidate.profile_repository import CandidateProfileRepository
from app.repositories.candidate.education_repository import EducationRepository
from app.repositories.candidate.experience_repository import ExperienceRepository
from app.repositories.candidate.skill_repository import SkillRepository

__all__ = [
    "CandidateProfileRepository",
    "EducationRepository",
    "ExperienceRepository",
    "SkillRepository",
]
