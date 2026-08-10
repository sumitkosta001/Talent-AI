"""Candidate Experience SQLAlchemy 2.0 ORM Entity Model."""

import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.candidate_profile import CandidateProfile


class CandidateExperience(BaseModel):
    """Work experience history entry for a candidate profile."""

    __tablename__ = "candidate_experience"

    candidate_profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key referencing candidate_profiles.id.",
    )

    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Name of the employer company or organization.",
    )

    job_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Job title or role position (e.g. Senior Software Engineer).",
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Start date of employment.",
    )

    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        default=None,
        doc="End date of employment. Nullable for current employment.",
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        default=None,
        doc="Detailed description of responsibilities and achievements.",
    )

    # Relationships
    candidate_profile: Mapped["CandidateProfile"] = relationship(
        "CandidateProfile",
        back_populates="experience",
    )
