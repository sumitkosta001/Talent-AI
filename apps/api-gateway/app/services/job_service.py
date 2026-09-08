"""Job Management Service Layer.

Encapsulates business operations, company ownership validation rules, and repository coordination for Job entities.
"""

import math
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.user import User
from app.models.enums import JobStatus, WorkMode
from app.schemas.job import JobCreate, JobUpdate
from app.repositories.job_repository import JobRepository
from app.exceptions.jobs import JobNotFoundError, InvalidJobStatusTransitionError
from app.exceptions.auth import PermissionDeniedError


class JobService:
    """Service class handling business operations and company authorization for Jobs."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize JobService with AsyncSession and JobRepository."""
        self.db = db
        self.repository = JobRepository(db)

    async def create_job(self, data: JobCreate, user: User) -> Job:
        """Create a new job posting initialized in DRAFT status for the user's company."""
        if not user.company_id:
            raise PermissionDeniedError("Recruiter account must be associated with a company to create job postings.")

        job = Job(
            company_id=user.company_id,
            recruiter_id=user.id,
            title=data.title.strip(),
            description=data.description.strip(),
            department=data.department.strip() if data.department else None,
            status=JobStatus.DRAFT,
            work_mode=data.work_mode,
            location=data.location.strip() if data.location else None,
            salary_min=data.salary_min,
            salary_max=data.salary_max,
            currency=data.currency.strip() if data.currency else "USD",
            required_skills=data.required_skills or [],
            preferred_skills=data.preferred_skills or [],
            required_experience_months=data.required_experience_months,
            education_requirements=data.education_requirements or [],
            required_keywords=data.required_keywords or [],
            created_by=user.id,
            updated_by=user.id,
        )

        return await self.repository.create_job(job)

    async def get_job(self, job_id: UUID | str) -> Job:
        """Retrieve an active job entity by ID or raise JobNotFoundError."""
        job = await self.repository.get_by_id(job_id)
        if not job:
            raise JobNotFoundError(job_id)
        return job

    async def update_job(self, job_id: UUID | str, data: JobUpdate, user: User) -> Job:
        """Update existing job posting with company ownership verification."""
        job = await self.get_job(job_id)

        # Company Ownership Authorization Check
        if not user.is_superuser and job.company_id != user.company_id:
            raise PermissionDeniedError("Access denied. You can only update job postings for your own company.")

        if data.title is not None:
            job.title = data.title.strip()
        if data.description is not None:
            job.description = data.description.strip()
        if data.department is not None:
            job.department = data.department.strip() if data.department else None
        if data.work_mode is not None:
            job.work_mode = data.work_mode
        if data.location is not None:
            job.location = data.location.strip() if data.location else None
        if data.salary_min is not None:
            job.salary_min = data.salary_min
        if data.salary_max is not None:
            job.salary_max = data.salary_max
        if data.currency is not None:
            job.currency = data.currency.strip() if data.currency else "USD"
        if data.required_skills is not None:
            job.required_skills = data.required_skills
        if data.preferred_skills is not None:
            job.preferred_skills = data.preferred_skills
        if data.required_experience_months is not None:
            job.required_experience_months = data.required_experience_months
        if data.education_requirements is not None:
            job.education_requirements = data.education_requirements
        if data.required_keywords is not None:
            job.required_keywords = data.required_keywords

        job.updated_by = user.id
        return await self.repository.update_job(job)

    async def delete_job(self, job_id: UUID | str, user: User) -> None:
        """Soft delete a job posting with company ownership verification."""
        job = await self.get_job(job_id)

        # Company Ownership Authorization Check
        if not user.is_superuser and job.company_id != user.company_id:
            raise PermissionDeniedError("Access denied. You can only delete job postings for your own company.")

        await self.repository.soft_delete_job(job)

    async def publish_job(self, job_id: UUID | str, user: User) -> Job:
        """Transition a DRAFT job posting to PUBLISHED status."""
        job = await self.get_job(job_id)

        # Company Ownership Authorization Check
        if not user.is_superuser and job.company_id != user.company_id:
            raise PermissionDeniedError("Access denied. You can only publish job postings for your own company.")

        if job.status == JobStatus.PUBLISHED:
            raise InvalidJobStatusTransitionError("Job posting is already published.")
        if job.status == JobStatus.CLOSED:
            raise InvalidJobStatusTransitionError("Closed job postings cannot be republished.")

        job.status = JobStatus.PUBLISHED
        job.published_at = datetime.now(timezone.utc)
        job.updated_by = user.id

        return await self.repository.update_job(job)

    async def unpublish_job(self, job_id: UUID | str, user: User) -> Job:
        """Transition a PUBLISHED job posting back to DRAFT status."""
        job = await self.get_job(job_id)

        # Company Ownership Authorization Check
        if not user.is_superuser and job.company_id != user.company_id:
            raise PermissionDeniedError("Access denied. You can only unpublish job postings for your own company.")

        if job.status == JobStatus.DRAFT:
            raise InvalidJobStatusTransitionError("Job posting is already in draft status.")
        if job.status == JobStatus.CLOSED:
            raise InvalidJobStatusTransitionError("Closed job postings cannot be unpublished to draft.")

        job.status = JobStatus.DRAFT
        job.updated_by = user.id

        return await self.repository.update_job(job)

    async def close_job(self, job_id: UUID | str, user: User) -> Job:
        """Transition a PUBLISHED job posting to CLOSED status."""
        job = await self.get_job(job_id)

        # Company Ownership Authorization Check
        if not user.is_superuser and job.company_id != user.company_id:
            raise PermissionDeniedError("Access denied. You can only close job postings for your own company.")

        if job.status == JobStatus.CLOSED:
            raise InvalidJobStatusTransitionError("Job posting is already closed.")
        if job.status == JobStatus.DRAFT:
            raise InvalidJobStatusTransitionError("Draft job postings cannot be directly closed. Publish the job before closing.")

        job.status = JobStatus.CLOSED
        job.updated_by = user.id

        return await self.repository.update_job(job)

    async def search_jobs(
        self,
        q: Optional[str] = None,
        location: Optional[str] = None,
        skills_str: Optional[str] = None,
        experience_months: Optional[int] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        work_mode: Optional[WorkMode] = None,
        page: int = 1,
        size: int = 20,
        sort_by: str = "published_at",
        sort_order: str = "desc",
    ) -> Tuple[List[Job], int, int]:
        """Search published, non-deleted jobs with relational multi-criteria filtering and pagination.

        Returns:
            Tuple of (list of matching Job instances, total matching count, total pages).
        """
        # Parse comma-separated skills parameter (e.g. "React,TypeScript" -> ["React", "TypeScript"])
        skills_list: Optional[List[str]] = None
        if skills_str and skills_str.strip():
            skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]

        # Calculate SQL pagination offset
        safe_page = max(1, page)
        safe_size = max(1, min(100, size))
        offset = (safe_page - 1) * safe_size

        # Whitelist safe sort fields
        allowed_sort_fields = {"published_at", "created_at", "updated_at", "salary_min", "salary_max", "title"}
        safe_sort_by = sort_by if sort_by in allowed_sort_fields else "published_at"
        safe_sort_order = "desc" if sort_order.lower() == "desc" else "asc"

        # Query database repository
        jobs, total = await self.repository.search_jobs(
            q=q,
            location=location,
            skills=skills_list,
            experience_months=experience_months,
            salary_min=salary_min,
            salary_max=salary_max,
            work_mode=work_mode,
            sort_by=safe_sort_by,
            sort_order=safe_sort_order,
            limit=safe_size,
            offset=offset,
        )

        total_pages = math.ceil(total / safe_size) if total > 0 else 0

        return jobs, total, total_pages

    async def get_company_jobs(
        self,
        user: User,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[Job], int, int]:
        """Fetch all company jobs (DRAFT, PUBLISHED, CLOSED) for the authenticated recruiter's company."""
        if not user.company_id:
            raise PermissionDeniedError("Recruiter account must be associated with a company to list company jobs.")

        jobs, total = await self.repository.get_company_jobs(
            company_id=user.company_id,
            limit=limit,
            offset=offset,
        )
        total_pages = math.ceil(total / limit) if total > 0 else 0
        return jobs, total, total_pages
