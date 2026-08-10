"""Candidate Experience Request and Response Schemas."""

from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExperienceBase(BaseModel):
    """Base fields for candidate experience records."""

    company: str = Field(..., min_length=2, max_length=255, description="Employer company name.")
    job_title: str = Field(..., min_length=2, max_length=255, description="Position job title.")
    start_date: date = Field(..., description="Start date of employment.")
    end_date: Optional[date] = Field(None, description="End date of employment (None if current job).")
    description: Optional[str] = Field(None, max_length=5000, description="Role description and achievements.")

    @model_validator(mode="after")
    def validate_dates(self) -> "ExperienceBase":
        """Verify that start_date is not after end_date."""
        if self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date cannot be after end date.")
        return self


class ExperienceCreate(ExperienceBase):
    """Payload for creating a new experience entry."""

    pass


class ExperienceUpdate(BaseModel):
    """Payload for updating an existing experience entry (all fields optional)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_title": "Lead Software Engineer",
                "description": "Led a team of developers building enterprise cloud solutions."
            }
        }
    )

    company: Optional[str] = Field(None, min_length=2, max_length=255)
    job_title: Optional[str] = Field(None, min_length=2, max_length=255)
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    description: Optional[str] = Field(None, max_length=5000)

    @model_validator(mode="after")
    def validate_dates(self) -> "ExperienceUpdate":
        """Verify that start_date is not after end_date when both are present or modified."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date cannot be after end date.")
        return self
        

class ExperienceResponse(ExperienceBase):
    """Response DTO for an experience record."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_profile_id: UUID
