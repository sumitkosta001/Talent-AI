"""Job Entity Database Repository.

Provides data access routines for Job entity management using SQLAlchemy 2.0 Async ORM.
"""

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List, Tuple

from sqlalchemy import select, func, or_, and_, String, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.enums import JobStatus, WorkMode


class JobRepository:
    """Repository managing Job entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize JobRepository with active AsyncSession."""
        self.db = db

    async def create_job(self, job: Job) -> Job:
        """Persist a new Job entity to the database."""
        try:
            self.db.add(job)
            await self.db.commit()
            await self.db.refresh(job)
            return job
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, job_id: UUID | str) -> Optional[Job]:
        """Fetch an active Job entity by UUID primary key."""
        if isinstance(job_id, str):
            job_id = UUID(job_id)

        stmt = select(Job).where(
            Job.id == job_id,
            Job.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_job(self, job: Job) -> Job:
        """Commit updates for an existing Job entity."""
        try:
            job.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(job)
            return job
        except Exception:
            await self.db.rollback()
            raise

    async def soft_delete_job(self, job: Job) -> None:
        """Perform logical soft deletion on a Job entity."""
        try:
            now = datetime.now(timezone.utc)
            job.is_deleted = True
            job.deleted_at = now
            job.updated_at = now
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def search_jobs(
        self,
        q: Optional[str] = None,
        location: Optional[str] = None,
        skills: Optional[List[str]] = None,
        experience_months: Optional[int] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        work_mode: Optional[WorkMode] = None,
        sort_by: str = "published_at",
        sort_order: str = "desc",
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[Job], int]:
        """Query published, non-deleted jobs with relational multi-criteria filtering and pagination.

        CRITICAL DISCOVERABILITY CONSTRAINT:
        Only returns jobs where status == PUBLISHED and is_deleted == False.
        """
        # Base query restricting to published, active jobs only
        base_where = [
            Job.status == JobStatus.PUBLISHED,
            Job.is_deleted == False,
        ]

        # Free-text search matching title, description, department, location, skills, keywords
        if q and q.strip():
            clean_q = q.strip().lower()
            q_pattern = f"%{clean_q}%"
            text_filter = or_(
                func.lower(Job.title).contains(clean_q),
                func.lower(Job.description).contains(clean_q),
                func.lower(Job.department).contains(clean_q),
                func.lower(Job.location).contains(clean_q),
                func.cast(Job.required_skills, String).ilike(q_pattern),
                func.cast(Job.required_keywords, String).ilike(q_pattern),
            )
            base_where.append(text_filter)

        # Location filter (case-insensitive substring match)
        if location and location.strip():
            clean_loc = location.strip().lower()
            base_where.append(func.lower(Job.location).contains(clean_loc))

        # Skill filter (matches if required_skills or preferred_skills contains any of requested skills)
        if skills:
            skill_filters = []
            for skill in skills:
                if skill and skill.strip():
                    pattern = f"%{skill.strip()}%"
                    skill_filters.append(func.cast(Job.required_skills, String).ilike(pattern))
                    skill_filters.append(func.cast(Job.preferred_skills, String).ilike(pattern))
            if skill_filters:
                base_where.append(or_(*skill_filters))

        # Experience filter (find jobs requiring <= specified experience_months or with no experience requirement)
        if experience_months is not None:
            base_where.append(
                or_(
                    Job.required_experience_months.is_(None),
                    Job.required_experience_months <= experience_months,
                )
            )

        # Salary Min filter (find jobs where maximum salary exceeds or matches candidate minimum salary)
        if salary_min is not None:
            base_where.append(
                or_(
                    Job.salary_max.is_(None),
                    Job.salary_max >= salary_min,
                )
            )

        # Salary Max filter (find jobs where minimum salary is within candidate maximum salary)
        if salary_max is not None:
            base_where.append(
                or_(
                    Job.salary_min.is_(None),
                    Job.salary_min <= salary_max,
                )
            )

        # Work Mode filter
        if work_mode is not None:
            base_where.append(Job.work_mode == work_mode)

        # Whitelisted sort column mapping
        sort_columns = {
            "created_at": Job.created_at,
            "updated_at": Job.updated_at,
            "published_at": Job.published_at,
            "salary_min": Job.salary_min,
            "salary_max": Job.salary_max,
            "title": Job.title,
        }

        sort_col = sort_columns.get(sort_by, Job.published_at)
        order_clause = desc(sort_col) if sort_order.lower() == "desc" else asc(sort_col)

        # Execute total count query
        count_stmt = select(func.count(Job.id)).where(and_(*base_where))
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0

        # Execute paginated items query
        items_stmt = (
            select(Job)
            .where(and_(*base_where))
            .order_by(order_clause, desc(Job.created_at))
            .limit(limit)
            .offset(offset)
        )
        items_result = await self.db.execute(items_stmt)
        jobs = list(items_result.scalars().all())

        return jobs, total

    async def get_company_jobs(
        self,
        company_id: UUID | str,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[Job], int]:
        """Fetch all non-deleted job postings belonging to a specific company (DRAFT, PUBLISHED, CLOSED)."""
        if isinstance(company_id, str):
            company_id = UUID(company_id)

        base_where = [
            Job.company_id == company_id,
            Job.is_deleted == False,
        ]

        count_stmt = select(func.count(Job.id)).where(and_(*base_where))
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0

        items_stmt = (
            select(Job)
            .where(and_(*base_where))
            .order_by(desc(Job.created_at))
            .limit(limit)
            .offset(offset)
        )
        items_result = await self.db.execute(items_stmt)
        jobs = list(items_result.scalars().all())

        return jobs, total
