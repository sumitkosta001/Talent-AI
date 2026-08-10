"""SQLAlchemy 2.0 ORM Entity Models Package.

Re-exports all domain entities and enumeration types so Alembic and application code
can import models directly from `app.models`.
"""

from app.models.enums import UserRole, AuthProvider, SkillCategory, SkillProficiency
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.candidate_profile import CandidateProfile
from app.models.candidate_education import CandidateEducation
from app.models.candidate_experience import CandidateExperience
from app.models.candidate_skill import CandidateSkill

__all__ = [
    "UserRole",
    "AuthProvider",
    "SkillCategory",
    "SkillProficiency",
    "User",
    "RefreshToken",
    "CandidateProfile",
    "CandidateEducation",
    "CandidateExperience",
    "CandidateSkill",
]
