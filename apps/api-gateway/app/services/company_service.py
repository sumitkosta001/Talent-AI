"""Company Management Service Layer.

Encapsulates business operations, validation rules, and repository coordination for Company entities.
"""

from uuid import UUID
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.company import Company
from app.models.enums import UserRole
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.exceptions.company import CompanyNotFoundError, CompanyAlreadyExistsError
from app.exceptions.auth import PermissionDeniedError


class CompanyService:
    """Service class handling business operations for Companies."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize CompanyService with AsyncSession and repositories."""
        self.db = db
        self.repository = CompanyRepository(db)
        self.user_repository = UserRepository(db)

    async def create_company(self, data: CompanyCreate, creator_user: Optional[User] = None) -> Company:
        """Create a new company entity after verifying uniqueness of company name.
        
        If the creator is a Recruiter or Hiring Manager without an associated company,
        they are automatically linked to the newly created company.
        """
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise CompanyAlreadyExistsError(f"A company with name '{data.name}' already exists.")

        creator_id = creator_user.id if creator_user else None

        company = Company(
            name=data.name.strip(),
            description=data.description.strip() if data.description else None,
            website=data.website.strip() if data.website else None,
            logo_url=data.logo_url.strip() if data.logo_url else None,
            location=data.location.strip() if data.location else None,
            industry=data.industry.strip() if data.industry else None,
            created_by=creator_id,
            updated_by=creator_id,
        )

        created_company = await self.repository.create_company(company)

        # Auto-associate creator with company and establish recruiter affiliation
        if creator_user:
            if not creator_user.company_id:
                creator_user.company_id = created_company.id
            if creator_user.role == UserRole.CANDIDATE:
                creator_user.role = UserRole.RECRUITER
            await self.user_repository.update_user(creator_user)

        return created_company

    async def get_company(self, company_id: UUID | str) -> Company:
        """Retrieve an active company by ID or raise CompanyNotFoundError."""
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with ID '{company_id}' not found.")
        return company

    async def update_company(
        self, company_id: UUID | str, data: CompanyUpdate, updater_id: Optional[UUID] = None
    ) -> Company:
        """Update existing company fields."""
        company = await self.get_company(company_id)

        if data.name is not None and data.name.strip().lower() != company.name.lower():
            existing = await self.repository.get_by_name(data.name)
            if existing and existing.id != company.id:
                raise CompanyAlreadyExistsError(f"A company with name '{data.name}' already exists.")
            company.name = data.name.strip()

        if data.description is not None:
            company.description = data.description.strip() if data.description else None
        if data.website is not None:
            company.website = data.website.strip() if data.website else None
        if data.logo_url is not None:
            company.logo_url = data.logo_url.strip() if data.logo_url else None
        if data.location is not None:
            company.location = data.location.strip() if data.location else None
        if data.industry is not None:
            company.industry = data.industry.strip() if data.industry else None

        if updater_id:
            company.updated_by = updater_id

        return await self.repository.update_company(company)

    async def delete_company(self, company_id: UUID | str) -> None:
        """Soft delete a company entity by ID."""
        company = await self.get_company(company_id)
        await self.repository.soft_delete_company(company)

    async def list_companies(self, limit: int = 100, offset: int = 0) -> Tuple[List[Company], int]:
        """List active companies with total count."""
        companies = await self.repository.list_companies(limit=limit, offset=offset)
        total = await self.repository.count_companies()
        return companies, total

    async def associate_recruiter(self, company_id: UUID | str, user: User) -> Company:
        """Associate an authenticated recruiter with a specified company entity."""
        if not user.is_superuser and user.role not in (UserRole.RECRUITER, UserRole.HIRING_MANAGER):
            raise PermissionDeniedError("Only Recruiters or Hiring Managers can associate with a company.")

        company = await self.get_company(company_id)

        if user.company_id and user.company_id != company.id:
            raise CompanyAlreadyExistsError("Recruiter is already associated with a different company.")

        if user.company_id != company.id:
            user.company_id = company.id
            await self.user_repository.update_user(user)

        return company

    async def get_my_company(self, user: User) -> Company:
        """Fetch company profile affiliated with the current authenticated recruiter."""
        if not user.company_id:
            raise CompanyNotFoundError("No company associated with the current user account.")
        return await self.get_company(user.company_id)

    async def update_my_company(self, user: User, data: CompanyUpdate) -> Company:
        """Update company profile affiliated with the current authenticated recruiter."""
        if not user.company_id:
            raise CompanyNotFoundError("No company associated with the current user account.")
        return await self.update_company(user.company_id, data, updater_id=user.id)
