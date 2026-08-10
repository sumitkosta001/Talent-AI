"""Candidate Profile Entity Database Repository."""

from uuid import UUID
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.candidate_profile import CandidateProfile


class CandidateProfileRepository:
    """Repository managing CandidateProfile entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with an active AsyncSession."""
        self.db = db

    async def get_by_user_id(self, user_id: UUID | str) -> Optional[CandidateProfile]:
        """Fetch a CandidateProfile by user_id with all child collections eagerly loaded."""
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = (
            select(CandidateProfile)
            .where(
                CandidateProfile.user_id == user_id,
                CandidateProfile.is_deleted == False
            )
            .options(
                selectinload(CandidateProfile.education),
                selectinload(CandidateProfile.experience),
                selectinload(CandidateProfile.skills),
                selectinload(CandidateProfile.user),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, profile_id: UUID | str) -> Optional[CandidateProfile]:
        """Fetch a CandidateProfile by its unique primary key ID."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(CandidateProfile)
            .where(
                CandidateProfile.id == profile_id,
                CandidateProfile.is_deleted == False
            )
            .options(
                selectinload(CandidateProfile.user),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, profile: CandidateProfile) -> CandidateProfile:
        """Persist a new CandidateProfile entity."""
        try:
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
            return profile
        except Exception:
            await self.db.rollback()
            raise

    async def update(self, profile: CandidateProfile) -> CandidateProfile:
        """Update an existing CandidateProfile entity."""
        try:
            await self.db.commit()
            await self.db.refresh(profile)
            return profile
        except Exception:
            await self.db.rollback()
            raise
