"""Candidate Skill SQLAlchemy 2.0 ORM Entity Model."""

import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel
from app.models.enums import SkillCategory, SkillProficiency

if TYPE_CHECKING:
    from app.models.candidate_profile import CandidateProfile


class CandidateSkill(BaseModel):
    """Skill entry associated with a candidate profile."""

    __tablename__ = "candidate_skills"

    candidate_profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key referencing candidate_profiles.id.",
    )

    skill_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Display name of the skill (e.g. Python, React).",
    )

    normalized_skill_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Normalized skill name (lowercased & trimmed) for duplicate prevention.",
    )

    category: Mapped[SkillCategory] = mapped_column(
        SQLEnum(
            SkillCategory,
            name="skillcategory",
            create_type=False,
            values_callable=lambda e: [member.value for member in e]
        ),
        nullable=False,
        default=SkillCategory.OTHER,
        server_default=SkillCategory.OTHER.value,
        doc="Skill category domain classification.",
    )

    proficiency: Mapped[SkillProficiency] = mapped_column(
        SQLEnum(
            SkillProficiency,
            name="skillproficiency",
            create_type=False,
            values_callable=lambda e: [member.value for member in e]
        ),
        nullable=False,
        default=SkillProficiency.INTERMEDIATE,
        server_default=SkillProficiency.INTERMEDIATE.value,
        doc="Self-assessed skill proficiency level.",
    )

    # Relationships
    candidate_profile: Mapped["CandidateProfile"] = relationship(
        "CandidateProfile",
        back_populates="skills",
    )

    __table_args__ = (
        UniqueConstraint(
            "candidate_profile_id",
            "normalized_skill_name",
            name="uq_candidate_skill_profile_normalized_name",
        ),
    )
