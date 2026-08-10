"""Candidate Skill Entity Database Repository."""

from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_skill import CandidateSkill


class SkillRepository:
    """Repository managing CandidateSkill entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with an active AsyncSession."""
        self.db = db

    async def list_by_profile_id(self, profile_id: UUID | str) -> List[CandidateSkill]:
        """Fetch all active skill records for a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateSkill)
            .where(
                CandidateSkill.candidate_profile_id == profile_id,
                CandidateSkill.is_deleted == False
            )
            .order_by(CandidateSkill.skill_name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id_for_profile(
        self, skill_id: UUID | str, profile_id: UUID | str
    ) -> Optional[CandidateSkill]:
        """Fetch a specific active skill record belonging to a candidate profile."""
        if isinstance(skill_id, str):
            skill_id = UUID(skill_id)
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateSkill)
            .where(
                CandidateSkill.id == skill_id,
                CandidateSkill.candidate_profile_id == profile_id,
                CandidateSkill.is_deleted == False
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_normalized_name(
        self, profile_id: UUID | str, normalized_name: str
    ) -> Optional[CandidateSkill]:
        """Fetch a specific skill by its normalized name (for duplicate detection)."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateSkill)
            .where(
                CandidateSkill.candidate_profile_id == profile_id,
                CandidateSkill.normalized_skill_name == normalized_name,
                CandidateSkill.is_deleted == False
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, skill: CandidateSkill) -> CandidateSkill:
        """Persist a new CandidateSkill record."""
        try:
            self.db.add(skill)
            await self.db.commit()
            await self.db.refresh(skill)
            return skill
        except Exception:
            await self.db.rollback()
            raise

    async def update(self, skill: CandidateSkill) -> CandidateSkill:
        """Update an existing CandidateSkill record."""
        try:
            await self.db.commit()
            await self.db.refresh(skill)
            return skill
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, skill: CandidateSkill) -> None:
        """Soft delete a CandidateSkill record."""
        try:
            from datetime import datetime, timezone
            skill.is_deleted = True
            skill.deleted_at = datetime.now(timezone.utc)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
