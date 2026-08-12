"""Candidate Profile Request and Response Schemas."""

import re
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.candidate.education import EducationResponse
from app.schemas.candidate.experience import ExperienceResponse
from app.schemas.candidate.skill import SkillResponse


class CandidateProfileBase(BaseModel):
    """Base fields for candidate profile."""

    phone_number: Optional[str] = Field(None, max_length=20, description="Contact phone number.")
    location: Optional[str] = Field(None, max_length=150, description="Current location.")
    headline: Optional[str] = Field(None, max_length=255, description="Professional headline.")
    bio: Optional[str] = Field(None, description="Candidate bio.")
    profile_picture_url: Optional[str] = Field(None, max_length=1024, description="Profile avatar picture URL.")
    linkedin_url: Optional[str] = Field(None, max_length=1024, description="LinkedIn URL.")
    github_url: Optional[str] = Field(None, max_length=1024, description="GitHub URL.")
    portfolio_url: Optional[str] = Field(None, max_length=1024, description="Portfolio website URL.")
    resume_url: Optional[str] = Field(None, max_length=1024, description="Candidate primary resume URL.")
    name: Optional[str] = Field(None, description="Candidate full name.")
    email: Optional[str] = Field(None, description="Candidate email address.")


class CandidateProfileCreate(BaseModel):
    """Payload for initializing a candidate profile."""

    pass


class CandidateProfileUpdate(BaseModel):
    """Payload for updating candidate profile details (all fields optional)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alex Johnson",
                "headline": "Lead Python Developer",
                "location": "San Francisco, CA",
                "phone_number": "+15550199"
            }
        }
    )

    name: Optional[str] = Field(None, description="Candidate full name.")
    phone_number: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=150)
    headline: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = Field(None)
    profile_picture_url: Optional[str] = Field(None, max_length=1024)
    linkedin_url: Optional[str] = Field(None, max_length=1024)
    github_url: Optional[str] = Field(None, max_length=1024)
    portfolio_url: Optional[str] = Field(None, max_length=1024)
    resume_url: Optional[str] = Field(None, max_length=1024)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace and normalize phone number if provided."""
        if v is not None:
            cleaned = v.strip()
            if cleaned and not re.match(r"^\+?[0-9\s\-()]{7,20}$", cleaned):
                raise ValueError("Invalid phone number format.")
            return cleaned
        return v

    @field_validator("linkedin_url", "github_url", "portfolio_url", "profile_picture_url", "resume_url")
    @classmethod
    def validate_urls(cls, v: Optional[str]) -> Optional[str]:
        """Validate that provided URLs start with http:// or https://."""
        if v is not None:
            cleaned = v.strip()
            if cleaned:
                if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
                    raise ValueError("URL must start with http:// or https://")
            return cleaned
        return v


class CandidateProfileResponse(CandidateProfileBase):
    """Response DTO for candidate profile."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    profile_completion_percentage: int


class CandidateProfileDetailResponse(CandidateProfileResponse):
    """Detailed response DTO for candidate profile containing child collections."""

    education: List[EducationResponse] = Field(default_factory=list)
    experience: List[ExperienceResponse] = Field(default_factory=list)
    skills: List[SkillResponse] = Field(default_factory=list)
