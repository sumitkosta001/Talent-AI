"""Candidate Education SQLAlchemy 2.0 ORM Entity Model."""

import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.candidate_profile import CandidateProfile


class CandidateEducation(BaseModel):
    """Education history entry for a candidate profile."""

    __tablename__ = "candidate_education"

    candidate_profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key referencing candidate_profiles.id.",
    )

    degree: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Degree name or field of study (e.g. B.Tech Computer Science).",
    )

    institution: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Name of the university, college, or educational institution.",
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Start date of study.",
    )

    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        default=None,
        doc="End or graduation date of study. Nullable for ongoing education.",
    )

    grade_or_cgpa: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        doc="Grade, CGPA, GPA, or classification achieved.",
    )

    # Relationships
    candidate_profile: Mapped["CandidateProfile"] = relationship(
        "CandidateProfile",
        back_populates="education",
    )
