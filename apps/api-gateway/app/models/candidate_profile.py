"""Candidate Profile SQLAlchemy 2.0 ORM Entity Model."""

import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.candidate_education import CandidateEducation
    from app.models.candidate_experience import CandidateExperience
    from app.models.candidate_skill import CandidateSkill


class CandidateProfile(BaseModel):
    """Candidate profile entity associated with a single User account (1-to-1)."""

    __tablename__ = "candidate_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        doc="Foreign key referencing users.id (1-to-1 identity mapping).",
    )

    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        default=None,
        doc="Normalized phone number.",
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
        default=None,
        doc="City, country, or remote location preference.",
    )

    headline: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc="Professional headline or title.",
    )

    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        default=None,
        doc="Personal summary biography or elevator pitch.",
    )

    profile_picture_url: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="URL pointing to hosted profile avatar picture.",
    )

    linkedin_url: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="LinkedIn public profile URL.",
    )

    github_url: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="GitHub public profile or portfolio repository URL.",
    )

    portfolio_url: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="Personal website or online portfolio URL.",
    )
 
    resume_url: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="URL pointing to candidate's primary resume document.",
    )

    profile_completion_percentage: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        doc="Centralized deterministic profile completion percentage (0-100%).",
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="candidate_profile",
        uselist=False,
    )

    education: Mapped[List["CandidateEducation"]] = relationship(
        "CandidateEducation",
        back_populates="candidate_profile",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    experience: Mapped[List["CandidateExperience"]] = relationship(
        "CandidateExperience",
        back_populates="candidate_profile",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill",
        back_populates="candidate_profile",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def name(self) -> str:
        return self.user.full_name if self.user else ""

    @property
    def email(self) -> str:
        return self.user.email if self.user else ""

