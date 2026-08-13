"""Resume Entity Database Repository.

Handles all database operations for Resume entities following the same
pattern as EducationRepository and ExperienceRepository.
"""

from uuid import UUID
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume


class ResumeRepository:
    """Repository managing Resume entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with an active AsyncSession."""
        self.db = db

    async def create(self, resume: Resume) -> Resume:
        """Persist a new Resume entity."""
        try:
            self.db.add(resume)
            await self.db.commit()
            await self.db.refresh(resume)
            return resume
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id_for_profile(
        self, resume_id: UUID | str, profile_id: UUID | str
    ) -> Optional[Resume]:
        """Fetch a specific active resume belonging to a candidate profile."""
        if isinstance(resume_id, str):
            resume_id = UUID(resume_id)
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(Resume)
            .where(
                Resume.id == resume_id,
                Resume.candidate_profile_id == profile_id,
                Resume.is_deleted == False,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_profile_id(self, profile_id: UUID | str) -> List[Resume]:
        """Fetch all active resume records for a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(Resume)
            .where(
                Resume.candidate_profile_id == profile_id,
                Resume.is_deleted == False,
            )
            .order_by(Resume.uploaded_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_current_for_profile(self, profile_id: UUID | str) -> Optional[Resume]:
        """Fetch the currently active resume for a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(Resume)
            .where(
                Resume.candidate_profile_id == profile_id,
                Resume.is_current == True,
                Resume.is_deleted == False,
            )
            .order_by(Resume.version.desc())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_all_not_current(self, profile_id: UUID | str) -> None:
        """Mark all existing resumes for a profile as not current (for versioning)."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        resumes = await self.list_by_profile_id(profile_id)
        for resume in resumes:
            if resume.is_current:
                resume.is_current = False

        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def get_max_version(self, profile_id: UUID | str) -> int:
        """Get the highest version number for a candidate's resumes."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        resumes = await self.list_by_profile_id(profile_id)
        if not resumes:
            return 0
        return max(r.version for r in resumes)
