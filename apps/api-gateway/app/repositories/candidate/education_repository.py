"""Candidate Education Entity Database Repository."""

from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_education import CandidateEducation


class EducationRepository:
    """Repository managing CandidateEducation entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with an active AsyncSession."""
        self.db = db

    async def list_by_profile_id(self, profile_id: UUID | str) -> List[CandidateEducation]:
        """Fetch all active education records for a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateEducation)
            .where(
                CandidateEducation.candidate_profile_id == profile_id,
                CandidateEducation.is_deleted == False
            )
            .order_by(CandidateEducation.start_date.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id_for_profile(
        self, education_id: UUID | str, profile_id: UUID | str
    ) -> Optional[CandidateEducation]:
        """Fetch a specific active education record belonging to a candidate profile."""
        if isinstance(education_id, str):
            education_id = UUID(education_id)
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateEducation)
            .where(
                CandidateEducation.id == education_id,
                CandidateEducation.candidate_profile_id == profile_id,
                CandidateEducation.is_deleted == False
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, education: CandidateEducation) -> CandidateEducation:
        """Persist a new CandidateEducation record."""
        try:
            self.db.add(education)
            await self.db.commit()
            await self.db.refresh(education)
            return education
        except Exception:
            await self.db.rollback()
            raise

    async def update(self, education: CandidateEducation) -> CandidateEducation:
        """Update an existing CandidateEducation record."""
        try:
            await self.db.commit()
            await self.db.refresh(education)
            return education
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, education: CandidateEducation) -> None:
        """Soft delete a CandidateEducation record."""
        try:
            from datetime import datetime, timezone
            education.is_deleted = True
            education.deleted_at = datetime.now(timezone.utc)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
