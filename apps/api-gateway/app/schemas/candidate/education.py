"""Candidate Education Request and Response Schemas."""

from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator


class EducationBase(BaseModel):
    """Base fields for candidate education records."""

    degree: str = Field(..., min_length=2, max_length=255, description="Degree or program of study.")
    institution: str = Field(..., min_length=2, max_length=255, description="Educational institution name.")
    start_date: date = Field(..., description="Start date of study.")
    end_date: Optional[date] = Field(None, description="End date of study (None if ongoing).")
    grade_or_cgpa: Optional[str] = Field(None, max_length=50, description="Grade, GPA, or CGPA achieved.")

    @model_validator(mode="after")
    def validate_dates(self) -> "EducationBase":
        """Verify that start_date is not after end_date."""
        if self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date cannot be after end date.")
        return self


class EducationCreate(EducationBase):
    """Payload for creating a new education entry."""

    pass


class EducationUpdate(BaseModel):
    """Payload for updating an existing education entry (all fields optional)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "degree": "Master of Science in Computer Science",
                "grade_or_cgpa": "3.9 GPA"
            }
        }
    )

    degree: Optional[str] = Field(None, min_length=2, max_length=255)
    institution: Optional[str] = Field(None, min_length=2, max_length=255)
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    grade_or_cgpa: Optional[str] = Field(None, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self) -> "EducationUpdate":
        """Verify that start_date is not after end_date when both are present or modified."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date cannot be after end date.")
        return self


class EducationResponse(EducationBase):
    """Response DTO for an education record."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_profile_id: UUID
