"""Candidate Experience Entity Database Repository."""

from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_experience import CandidateExperience


class ExperienceRepository:
    """Repository managing CandidateExperience entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with an active AsyncSession."""
        self.db = db

    async def list_by_profile_id(self, profile_id: UUID | str) -> List[CandidateExperience]:
        """Fetch all active experience records for a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateExperience)
            .where(
                CandidateExperience.candidate_profile_id == profile_id,
                CandidateExperience.is_deleted == False
            )
            .order_by(CandidateExperience.start_date.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id_for_profile(
        self, experience_id: UUID | str, profile_id: UUID | str
    ) -> Optional[CandidateExperience]:
        """Fetch a specific active experience record belonging to a candidate profile."""
        if isinstance(experience_id, str):
            experience_id = UUID(experience_id)
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateExperience)
            .where(
                CandidateExperience.id == experience_id,
                CandidateExperience.candidate_profile_id == profile_id,
                CandidateExperience.is_deleted == False
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, experience: CandidateExperience) -> CandidateExperience:
        """Persist a new CandidateExperience record."""
        try:
            self.db.add(experience)
            await self.db.commit()
            await self.db.refresh(experience)
            return experience
        except Exception:
            await self.db.rollback()
            raise

    async def update(self, experience: CandidateExperience) -> CandidateExperience:
        """Update an existing CandidateExperience record."""
        try:
            await self.db.commit()
            await self.db.refresh(experience)
            return experience
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, experience: CandidateExperience) -> None:
        """Soft delete a CandidateExperience record."""
        try:
            from datetime import datetime, timezone
            experience.is_deleted = True
            experience.deleted_at = datetime.now(timezone.utc)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
