"""Company Management REST API Router."""

from uuid import UUID
from typing import Annotated, List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_active_user, get_current_company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company profile",
    description="Registers a new company profile entity in the platform directory.",
)
async def create_company(
    payload: CompanyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> CompanyResponse:
    """Create a new company profile."""
    service = CompanyService(db)
    company = await service.create_company(payload, creator_user=current_user)
    return CompanyResponse.model_validate(company)


@router.get(
    "/me",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current recruiter's company profile",
    description="Fetches company profile details associated with the authenticated recruiter account.",
)
async def get_my_company(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> CompanyResponse:
    """Get authenticated recruiter's associated company."""
    service = CompanyService(db)
    company = await service.get_my_company(current_user)
    return CompanyResponse.model_validate(company)


@router.patch(
    "/me",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current recruiter's company profile",
    description="Updates company details for the company associated with the authenticated recruiter.",
)
async def update_my_company(
    payload: CompanyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> CompanyResponse:
    """Update authenticated recruiter's associated company."""
    service = CompanyService(db)
    company = await service.update_my_company(current_user, payload)
    return CompanyResponse.model_validate(company)


@router.post(
    "/{company_id}/join",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Associate recruiter with company",
    description="Associates the authenticated recruiter account with the specified company entity.",
)
async def join_company(
    company_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_company)],
) -> CompanyResponse:
    """Associate authenticated recruiter with company."""
    service = CompanyService(db)
    company = await service.associate_recruiter(company_id, current_user)
    return CompanyResponse.model_validate(company)


@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get company profile details by ID",
    description="Fetches company profile details for the given company UUID.",
)
async def get_company_by_id(
    company_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CompanyResponse:
    """Get company profile details by ID."""
    service = CompanyService(db)
    company = await service.get_company(company_id)
    return CompanyResponse.model_validate(company)


@router.patch(
    "/{company_id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Update company profile details",
    description="Updates existing company fields for the specified company ID.",
)
async def update_company(
    company_id: UUID,
    payload: CompanyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> CompanyResponse:
    """Update company profile details."""
    service = CompanyService(db)
    company = await service.update_company(company_id, payload, updater_id=current_user.id)
    return CompanyResponse.model_validate(company)


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete company profile",
    description="Soft-deletes the company profile for the specified company ID.",
)
async def delete_company(
    company_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    """Soft delete company profile."""
    service = CompanyService(db)
    await service.delete_company(company_id)


@router.get(
    "",
    response_model=List[CompanyResponse],
    status_code=status.HTTP_200_OK,
    summary="List active company profiles",
    description="Retrieves a paginated list of active company profiles.",
)
async def list_companies(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[CompanyResponse]:
    """List active company profiles."""
    service = CompanyService(db)
    companies, _ = await service.list_companies(limit=limit, offset=offset)
    return [CompanyResponse.model_validate(c) for c in companies]
