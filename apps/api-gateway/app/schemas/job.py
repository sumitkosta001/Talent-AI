"""Job Pydantic Validation & Serialization Schemas."""

from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, field_serializer

from app.models.enums import JobStatus, WorkMode


def sanitize_string_list(items: Optional[List[str]]) -> List[str]:
    """Helper function to strip whitespace and discard empty/blank strings from a list."""
    if not items:
        return []
    sanitized = [item.strip() for item in items if isinstance(item, str) and item.strip()]
    return sanitized


class JobBase(BaseModel):
    """Base Job schema containing common fields."""

    title: str = Field(..., min_length=1, max_length=255, description="Official job posting title.")
    description: str = Field(..., min_length=1, max_length=50000, description="Detailed job description.")
    department: Optional[str] = Field(None, max_length=100, description="Department or team name.")
    work_mode: WorkMode = Field(default=WorkMode.REMOTE, description="Workplace setting.")
    location: Optional[str] = Field(None, max_length=255, description="Office location or region.")
    salary_min: Optional[int] = Field(None, ge=0, description="Minimum annual salary bound.")
    salary_max: Optional[int] = Field(None, ge=0, description="Maximum annual salary bound.")
    currency: str = Field(default="USD", max_length=10, description="Salary currency code.")
    required_skills: List[str] = Field(default_factory=list, description="Mandatory technical/soft skills.")
    preferred_skills: List[str] = Field(default_factory=list, description="Nice-to-have skills.")
    required_experience_months: Optional[int] = Field(None, ge=0, description="Required experience in months.")
    education_requirements: List[str] = Field(default_factory=list, description="Education requirements.")
    required_keywords: List[str] = Field(default_factory=list, description="ATS keyword requirements.")

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, v: Optional[str]) -> str:
        """Normalize currency code to uppercase."""
        if isinstance(v, str) and v.strip():
            return v.strip().upper()
        return "USD"

    @field_validator("work_mode", mode="before")
    @classmethod
    def normalize_work_mode(cls, v: Any) -> Any:
        """Normalize work_mode string to match WorkMode enum case-insensitively."""
        if isinstance(v, str) and v.strip():
            val = v.strip().lower()
            if val in WorkMode._value2member_map_:
                return WorkMode(val)
        return v

    @field_validator("required_skills", "preferred_skills", "education_requirements", "required_keywords", mode="before")
    @classmethod
    def sanitize_lists(cls, v: Optional[List[str]]) -> List[str]:
        """Sanitize string lists by stripping whitespace and removing empty items."""
        return sanitize_string_list(v)

    @model_validator(mode="after")
    def validate_salary_range(self) -> "JobBase":
        """Ensure salary_min does not exceed salary_max when both are provided."""
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_min > self.salary_max:
                raise ValueError("salary_min cannot exceed salary_max.")
        return self


class JobCreate(JobBase):
    """Payload schema for creating a new job posting."""

    pass


class JobUpdate(BaseModel):
    """Payload schema for updating an existing job posting (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Official job posting title.")
    description: Optional[str] = Field(None, min_length=1, max_length=50000, description="Detailed job description.")
    department: Optional[str] = Field(None, max_length=100, description="Department or team name.")
    work_mode: Optional[WorkMode] = Field(None, description="Workplace setting.")
    location: Optional[str] = Field(None, max_length=255, description="Office location or region.")
    salary_min: Optional[int] = Field(None, ge=0, description="Minimum annual salary bound.")
    salary_max: Optional[int] = Field(None, ge=0, description="Maximum annual salary bound.")
    currency: Optional[str] = Field(None, max_length=10, description="Salary currency code.")
    required_skills: Optional[List[str]] = Field(None, description="Mandatory technical/soft skills.")
    preferred_skills: Optional[List[str]] = Field(None, description="Nice-to-have skills.")
    required_experience_months: Optional[int] = Field(None, ge=0, description="Required experience in months.")
    education_requirements: Optional[List[str]] = Field(None, description="Education requirements.")
    required_keywords: Optional[List[str]] = Field(None, description="ATS keyword requirements.")

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, v: Optional[str]) -> Optional[str]:
        """Normalize currency code to uppercase."""
        if isinstance(v, str) and v.strip():
            return v.strip().upper()
        return v

    @field_validator("work_mode", mode="before")
    @classmethod
    def normalize_work_mode(cls, v: Any) -> Any:
        """Normalize work_mode string to match WorkMode enum case-insensitively."""
        if isinstance(v, str) and v.strip():
            val = v.strip().lower()
            if val in WorkMode._value2member_map_:
                return WorkMode(val)
        return v

    @field_validator("required_skills", "preferred_skills", "education_requirements", "required_keywords", mode="before")
    @classmethod
    def sanitize_lists(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Sanitize string lists by stripping whitespace and removing empty items."""
        if v is None:
            return None
        return sanitize_string_list(v)

    @model_validator(mode="after")
    def validate_salary_range(self) -> "JobUpdate":
        """Ensure salary_min does not exceed salary_max when both are updated."""
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_min > self.salary_max:
                raise ValueError("salary_min cannot exceed salary_max.")
        return self


class JobResponse(JobBase):
    """Response serialization payload for job posting details."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    recruiter_id: Optional[UUID] = None
    status: JobStatus = JobStatus.DRAFT
    published_at: Optional[datetime] = None
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    @field_serializer("status", "work_mode", mode="plain")
    def serialize_enum_uppercase(self, v: Any, _info: Any) -> str:
        """Serialize JobStatus and WorkMode enum values as uppercase strings."""
        if hasattr(v, "name"):
            return v.name
        if hasattr(v, "value"):
            return str(v.value).upper()
        return str(v).upper()


class JobPaginatedResponse(BaseModel):
    """Paginated container response payload for job search queries."""

    items: List[JobResponse]
    total: int = Field(..., ge=0, description="Total matching published jobs count.")
    page: int = Field(..., ge=1, description="Current page number.")
    size: int = Field(..., ge=1, description="Items per page.")
    total_pages: int = Field(..., ge=0, description="Total available pages.")

