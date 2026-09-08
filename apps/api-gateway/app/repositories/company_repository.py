"""Company Entity Database Repository.

Provides data access routines for Company entity management using SQLAlchemy 2.0 Async ORM.
"""

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company


class CompanyRepository:
    """Repository managing Company entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize CompanyRepository with active AsyncSession."""
        self.db = db

    async def create_company(self, company: Company) -> Company:
        """Persist a new Company entity to the database."""
        try:
            self.db.add(company)
            await self.db.commit()
            await self.db.refresh(company)
            return company
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, company_id: UUID | str) -> Optional[Company]:
        """Fetch an active Company entity by UUID primary key."""
        if isinstance(company_id, str):
            company_id = UUID(company_id)

        stmt = select(Company).where(
            Company.id == company_id,
            Company.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Company]:
        """Fetch a Company entity by name (case-insensitive)."""
        if not name or not name.strip():
            return None

        clean_name = name.strip().lower()
        stmt = select(Company).where(
            func.lower(Company.name) == clean_name,
            Company.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_company(self, company: Company) -> Company:
        """Commit updates for an existing Company entity."""
        try:
            company.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(company)
            return company
        except Exception:
            await self.db.rollback()
            raise

    async def soft_delete_company(self, company: Company) -> None:
        """Perform logical soft deletion on a Company entity."""
        try:
            now = datetime.now(timezone.utc)
            company.is_deleted = True
            company.deleted_at = now
            company.updated_at = now
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def list_companies(self, limit: int = 100, offset: int = 0) -> List[Company]:
        """Retrieve paginated list of active companies ordered by creation date."""
        stmt = (
            select(Company)
            .where(Company.is_deleted == False)
            .order_by(Company.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_companies(self) -> int:
        """Count total non-deleted companies."""
        stmt = select(func.count(Company.id)).where(Company.is_deleted == False)
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count if count is not None else 0
