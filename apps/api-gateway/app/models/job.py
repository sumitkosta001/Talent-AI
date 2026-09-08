"""Job ORM Entity Model for TalentAI."""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON, text
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel
from app.models.enums import JobStatus, WorkMode

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.user import User
    from app.services.resume_processing.models import JobRequirements


class Job(BaseModel):
    """Job entity model representing a job posting managed by a company and recruiter."""

    __tablename__ = "jobs"

    company_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key referencing companies.id (job owner organization).",
    )

    recruiter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
        index=True,
        doc="Foreign key referencing users.id for recruiter who posted the job.",
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Official job posting title (e.g. Senior Fullstack Engineer).",
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Detailed job description and responsibilities.",
    )

    department: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default=None,
        doc="Department or team (e.g. Engineering, Product).",
    )

    status: Mapped[JobStatus] = mapped_column(
        PG_ENUM(
            JobStatus,
            name="job_status",
            create_constraint=False,
            native_enum=True,
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=False,
        default=JobStatus.DRAFT,
        server_default=text("'draft'"),
        index=True,
        doc="Publication lifecycle status (draft, published, closed).",
    )

    work_mode: Mapped[WorkMode] = mapped_column(
        PG_ENUM(
            WorkMode,
            name="work_mode",
            create_constraint=False,
            native_enum=True,
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=False,
        default=WorkMode.REMOTE,
        server_default=text("'remote'"),
        index=True,
        doc="Workplace setting (remote, hybrid, onsite).",
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc="Office location or geographic region.",
    )

    salary_min: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        doc="Minimum annual salary range lower bound.",
    )

    salary_max: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        doc="Maximum annual salary range upper bound.",
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="USD",
        server_default=text("'USD'"),
        doc="Salary currency code (e.g. USD, EUR, INR).",
    )

    required_skills: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'"),
        doc="List of mandatory technical and soft skills.",
    )

    preferred_skills: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'"),
        doc="List of nice-to-have skills.",
    )

    required_experience_months: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        doc="Minimum required work experience in months.",
    )

    education_requirements: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'"),
        doc="Required degrees or field of study (e.g. Bachelor's in Computer Science).",
    )

    required_keywords: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'"),
        doc="ATS keyword requirements.",
    )

    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="UTC timestamp when the job posting was published.",
    )

    # Relationships
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="jobs",
        uselist=False,
    )

    recruiter: Mapped[Optional["User"]] = relationship(
        "User",
        uselist=False,
    )

    def to_job_requirements(self) -> "JobRequirements":
        """Convert database Job model instance into Phase 4 ML JobRequirements Pydantic model."""
        from app.services.resume_processing.models import JobRequirements

        return JobRequirements(
            job_id=str(self.id),
            title=self.title,
            description=self.description,
            required_keywords=self.required_keywords or [],
            preferred_keywords=[],
            required_skills=self.required_skills or [],
            preferred_skills=self.preferred_skills or [],
            required_education=self.education_requirements or [],
            preferred_education=[],
            required_experience_months=self.required_experience_months,
            preferred_experience_months=None,
            required_roles=[self.title] if self.title else [],
            preferred_roles=[],
            required_domains=[],
            preferred_domains=[],
            metadata={
                "company_id": str(self.company_id),
                "location": self.location,
                "work_mode": self.work_mode.value if hasattr(self.work_mode, "value") else str(self.work_mode),
                "salary_min": self.salary_min,
                "salary_max": self.salary_max,
                "currency": self.currency,
                "status": self.status.value if hasattr(self.status, "value") else str(self.status),
            },
        )
