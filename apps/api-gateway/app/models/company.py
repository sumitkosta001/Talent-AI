"""Company ORM Entity Model for TalentAI."""

from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.job import Job


class Company(BaseModel):
    """Company entity model for managing employer organization profiles."""

    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Official company or organization name.",
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        default=None,
        doc="Company overview description or mission statement.",
    )

    website: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="Official company website URL.",
    )

    logo_url: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
        default=None,
        doc="URL pointing to company logo image.",
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc="Headquarters location or primary operational address.",
    )

    industry: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc="Industry sector (e.g. Technology, Healthcare, Finance).",
    )

    recruiters: Mapped[List["User"]] = relationship(
        "User",
        back_populates="company",
        lazy="selectin",
        doc="List of recruiters or hiring managers affiliated with this company.",
    )

    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="List of job postings owned by this company.",
    )
