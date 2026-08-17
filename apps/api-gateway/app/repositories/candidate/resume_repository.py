"""Resume Entity Database Repository.

Handles all database operations for Resume entities following the same
pattern as EducationRepository and ExperienceRepository.
"""

from uuid import UUID
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import select, func, update
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

    async def create_no_commit(self, resume: Resume) -> Resume:
        """Persist a new Resume entity without committing (for transactional use)."""
        self.db.add(resume)
        await self.db.flush()
        await self.db.refresh(resume)
        return resume

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

    async def get_by_id_for_profile_locked(
        self, resume_id: UUID | str, profile_id: UUID | str
    ) -> Optional[Resume]:
        """Fetch a specific active resume with row-level lock (FOR UPDATE) for concurrent operations."""
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
            .with_for_update()
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, resume: Resume) -> Resume:
        """Update and commit a Resume entity."""
        try:
            await self.db.commit()
            await self.db.refresh(resume)
            return resume
        except Exception:
            await self.db.rollback()
            raise


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

    async def mark_all_not_current_no_commit(self, profile_id: UUID | str) -> None:
        """Mark all active resumes as not current using a bulk UPDATE (no commit)."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            update(Resume)
            .where(
                Resume.candidate_profile_id == profile_id,
                Resume.is_deleted == False,
                Resume.is_current == True,
            )
            .values(is_current=False)
        )
        await self.db.execute(stmt)

    async def get_max_version(self, profile_id: UUID | str) -> int:
        """Get the highest version number for a candidate's resumes.

        Includes deleted resumes to prevent version number reuse.
        """
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(func.max(Resume.version))
            .where(Resume.candidate_profile_id == profile_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_max_version_locked(self, profile_id: UUID | str) -> int:
        """Get the highest version number with row-level locking for concurrency safety.

        Acquires a FOR UPDATE lock on the candidate profile row to serialize
        concurrent version generation for the same candidate.
        """
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        # Lock the candidate profile row to serialize concurrent uploads
        from app.models.candidate_profile import CandidateProfile
        lock_stmt = (
            select(CandidateProfile.id)
            .where(CandidateProfile.id == profile_id)
            .with_for_update()
        )
        await self.db.execute(lock_stmt)

        # Now safely query max version (includes deleted to prevent reuse)
        return await self.get_max_version(profile_id)

    async def get_highest_active_resume(
        self, profile_id: UUID | str, exclude_id: Optional[UUID] = None
    ) -> Optional[Resume]:
        """Get the highest-versioned active (non-deleted) resume, optionally excluding one.

        Used for auto-promotion when the current version is deleted.
        """
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(Resume)
            .where(
                Resume.candidate_profile_id == profile_id,
                Resume.is_deleted == False,
            )
        )
        if exclude_id:
            stmt = stmt.where(Resume.id != exclude_id)
        stmt = stmt.order_by(Resume.version.desc()).limit(1)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_profile_id_paginated(
        self,
        profile_id: UUID | str,
        offset: int,
        limit: int,
        sort_by: str,
        sort_order: str,
    ) -> List[Resume]:
        """Fetch a paginated, sorted list of resumes belonging to a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        # Map string parameters safely to SQLAlchemy columns to prevent SQL injection
        sort_mapping = {
            "uploaded_at": Resume.uploaded_at,
            "file_size_bytes": Resume.file_size_bytes,
            "status": Resume.status,
            "original_filename": Resume.original_filename,
            "version": Resume.version,
        }

        sort_col = sort_mapping.get(sort_by, Resume.uploaded_at)

        # Implement stable sorting: order by sort_col then fallback to Resume.id
        if sort_order == "desc":
            order_by_clause = [sort_col.desc(), Resume.id.desc()]
        else:
            order_by_clause = [sort_col.asc(), Resume.id.asc()]

        stmt = (
            select(Resume)
            .where(
                Resume.candidate_profile_id == profile_id,
                Resume.is_deleted == False,
            )
            .order_by(*order_by_clause)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_profile_id(self, profile_id: UUID | str) -> int:
        """Count total active resumes for a candidate profile."""
        if isinstance(profile_id, str):
            profile_id = UUID(profile_id)

        stmt = (
            select(func.count())
            .select_from(Resume)
            .where(
                Resume.candidate_profile_id == profile_id,
                Resume.is_deleted == False,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def delete(self, resume: Resume) -> None:
        """Soft delete a Resume record."""
        try:
            resume.is_deleted = True
            resume.deleted_at = datetime.now(timezone.utc)
            resume.is_current = False
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def delete_no_commit(self, resume: Resume) -> None:
        """Soft delete a Resume record without committing (for transactional use)."""
        resume.is_deleted = True
        resume.deleted_at = datetime.now(timezone.utc)
        resume.is_current = False
