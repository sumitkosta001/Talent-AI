"""Candidate Skill Request and Response Schemas."""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.enums import SkillCategory, SkillProficiency


class SkillBase(BaseModel):
    """Base fields for candidate skill records."""

    skill_name: str = Field(..., min_length=1, max_length=100, description="Display name of the skill.")
    category: SkillCategory = Field(default=SkillCategory.OTHER, description="Skill category classification.")
    proficiency: SkillProficiency = Field(default=SkillProficiency.INTERMEDIATE, description="Proficiency level.")

    @field_validator("skill_name")
    @classmethod
    def clean_skill_name(cls, v: str) -> str:
        """Strip and validate that skill name is not empty."""
        if not v or not v.strip():
            raise ValueError("Skill name cannot be empty or whitespace.")
        return v.strip()


class SkillCreate(SkillBase):
    """Payload for creating a new skill entry."""

    pass


class SkillUpdate(BaseModel):
    """Payload for updating an existing skill entry (all fields optional)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "proficiency": "expert",
                "category": "programming"
            }
        }
    )

    skill_name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[SkillCategory] = Field(None)
    proficiency: Optional[SkillProficiency] = Field(None)

    @field_validator("skill_name")
    @classmethod
    def clean_skill_name(cls, v: Optional[str]) -> Optional[str]:
        """Strip and validate that skill name is not empty if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError("Skill name cannot be empty or whitespace.")
            return v.strip()
        return v


class SkillResponse(SkillBase):
    """Response DTO for a skill record."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_profile_id: UUID
    normalized_skill_name: str
