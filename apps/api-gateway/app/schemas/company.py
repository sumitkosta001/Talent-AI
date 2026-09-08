"""Company Pydantic Validation & Serialization Schemas."""

from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class CompanyBase(BaseModel):
    """Base Company schema with shared attributes."""

    name: str = Field(..., min_length=1, max_length=255, description="Company or organization name.")
    description: Optional[str] = Field(None, max_length=5000, description="Company overview or description.")
    website: Optional[str] = Field(None, max_length=1024, description="Official company website URL.")
    logo_url: Optional[str] = Field(None, max_length=1024, description="URL pointing to company logo image.")
    location: Optional[str] = Field(None, max_length=255, description="Headquarters location.")
    industry: Optional[str] = Field(None, max_length=255, description="Industry sector.")


class CompanyCreate(CompanyBase):
    """Payload schema for creating a new company."""

    pass


class CompanyUpdate(BaseModel):
    """Payload schema for updating an existing company (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Company or organization name.")
    description: Optional[str] = Field(None, max_length=5000, description="Company overview or description.")
    website: Optional[str] = Field(None, max_length=1024, description="Official company website URL.")
    logo_url: Optional[str] = Field(None, max_length=1024, description="URL pointing to company logo image.")
    location: Optional[str] = Field(None, max_length=255, description="Headquarters location.")
    industry: Optional[str] = Field(None, max_length=255, description="Industry sector.")


class CompanyResponse(CompanyBase):
    """Response payload schema for company details."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
