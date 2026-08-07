"""Authentication & User Identity Request/Response Pydantic v2 DTO Schemas.

Provides fully-validated, production-grade Data Transfer Objects (DTOs) for
authentication workflows including registration, login, token refresh, logout,
and current user profile inspection.
"""

from __future__ import annotations

import re
from uuid import UUID
from typing import Optional, Any
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    AliasChoices,
    field_validator,
    model_validator,
)

from app.models.enums import UserRole, AuthProvider


# ==============================================================================
# REUSABLE VALIDATION HELPERS
# ==============================================================================

def clean_email(v: Any) -> str:
    """Strip whitespace and convert email address to lowercase.

    Args:
        v: Incoming email value.

    Returns:
        Cleaned, lowercased email string.

    Raises:
        ValueError: If email is empty or invalid type.
    """
    if not isinstance(v, str) or not v.strip():
        raise ValueError("Email address cannot be empty or blank.")
    return v.strip().lower()


def validate_name(v: Any, field_name: str = "Name") -> str:
    """Validate and clean user first/last name.

    Args:
        v: Incoming name string.
        field_name: Field label for error messaging.

    Returns:
        Cleaned name string.

    Raises:
        ValueError: If name is empty, whitespace-only, or outside length limits (2-50).
    """
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"{field_name} cannot be empty or consist only of whitespace.")
    cleaned = v.strip()
    if len(cleaned) < 2 or len(cleaned) > 50:
        raise ValueError(f"{field_name} must be between 2 and 50 characters in length.")
    return cleaned


def validate_password_strength(v: str) -> str:
    """Enforce enterprise password complexity requirements.

    Requirements:
        - 8 to 128 characters in length.
        - Must contain at least one uppercase letter (A-Z).
        - Must contain at least one lowercase letter (a-z).
        - Must contain at least one numerical digit (0-9).
        - Must contain at least one special character (!@#$%^&* etc.).
        - No whitespace allowed.

    Args:
        v: Plaintext password string.

    Returns:
        Validated password string.

    Raises:
        ValueError: If password fails complexity rules or contains whitespace.
    """
    if not isinstance(v, str) or not v:
        raise ValueError("Password cannot be empty.")

    if any(c.isspace() for c in v):
        raise ValueError("Password must not contain any whitespace characters.")

    if len(v) < 8 or len(v) > 128:
        raise ValueError("Password must be between 8 and 128 characters in length.")

    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter (A-Z).")

    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter (a-z).")

    if not re.search(r"[0-9]", v):
        raise ValueError("Password must contain at least one numerical digit (0-9).")

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]", v):
        raise ValueError(
            "Password must contain at least one special character (e.g., !@#$%^&*)."
        )

    return v


# ==============================================================================
# AUTHENTICATION SCHEMAS
# ==============================================================================

class UserSummary(BaseModel):
    """Lightweight user identity representation for auth responses.

    Used across authentication responses, user state inspection, and session
    verification. Immutable (frozen) model with attribute mapping support for ORM instances.
    """

    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "candidate@talentai.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "full_name": "Jane Doe",
                "role": "candidate",
                "provider": "local",
                "is_verified": True,
                "avatar_url": "https://cdn.talentai.com/avatars/jane_doe.jpg",
            }
        },
    )

    id: UUID = Field(
        ...,
        description="Unique user identifier (UUID v4).",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    email: EmailStr = Field(
        ...,
        description="Primary account email address.",
        examples=["candidate@talentai.com"],
    )
    first_name: str = Field(
        ...,
        description="User's given first name.",
        examples=["Jane"],
    )
    last_name: str = Field(
        ...,
        description="User's family last name.",
        examples=["Doe"],
    )
    full_name: str = Field(
        ...,
        description="Computed full display name (first + last name).",
        examples=["Jane Doe"],
    )
    role: UserRole = Field(
        ...,
        description="Role-based authorization access level.",
        examples=[UserRole.CANDIDATE],
    )
    provider: AuthProvider = Field(
        ...,
        description="Authentication provider used to register.",
        examples=[AuthProvider.LOCAL],
    )
    is_verified: bool = Field(
        ...,
        description="Indicates whether the account email address has been verified.",
        examples=[True],
    )
    avatar_url: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("avatar_url", "profile_picture_url"),
        serialization_alias="avatar_url",
        description="URL pointing to the user's avatar image.",
        examples=["https://cdn.talentai.com/avatars/jane_doe.jpg"],
    )


class TokenPair(BaseModel):
    """JWT Access and Refresh token pair payload.

    Returned to the client after successful authentication or token refresh operations.
    """

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        },
    )

    access_token: str = Field(
        ...,
        description="Short-lived JWT access token for authenticating API calls.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    refresh_token: str = Field(
        ...,
        description="Long-lived JWT refresh token for renewing access tokens.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        "bearer",
        description="OAuth2 token type (defaults to 'bearer').",
        examples=["bearer"],
    )


class RegisterRequest(BaseModel):
    """Request DTO for new user account registration."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jane.doe@example.com",
                "password": "SecurePassword123!",
                "confirm_password": "SecurePassword123!",
                "first_name": "Jane",
                "last_name": "Doe",
            }
        }
    )

    email: EmailStr = Field(
        ...,
        description="Primary email address for account registration.",
        examples=["jane.doe@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plaintext password meeting complexity requirements (8-128 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char).",
        examples=["SecurePassword123!"],
    )
    confirm_password: str = Field(
        ...,
        description="Must match the password field exactly.",
        examples=["SecurePassword123!"],
    )
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User's first name (2-50 characters).",
        examples=["Jane"],
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User's last name (2-50 characters).",
        examples=["Doe"],
    )

    @field_validator("email", mode="before")
    @classmethod
    def validate_and_clean_email(cls, v: Any) -> str:
        """Strip and lowercase incoming email."""
        return clean_email(v)

    @field_validator("first_name", mode="before")
    @classmethod
    def validate_first_name(cls, v: Any) -> str:
        """Strip and validate first name length."""
        return validate_name(v, "First name")

    @field_validator("last_name", mode="before")
    @classmethod
    def validate_last_name(cls, v: Any) -> str:
        """Strip and validate last name length."""
        return validate_name(v, "Last name")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength complexity rules."""
        return validate_password_strength(v)

    @model_validator(mode="after")
    def validate_passwords_match(self) -> RegisterRequest:
        """Ensure password and confirm_password fields match."""
        if self.password != self.confirm_password:
            raise ValueError("Password and confirm_password do not match.")
        return self


class RegisterResponse(BaseModel):
    """Response DTO following successful user account registration."""

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "message": "User account registered successfully.",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "jane.doe@example.com",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "full_name": "Jane Doe",
                    "role": "candidate",
                    "provider": "local",
                    "is_verified": False,
                    "avatar_url": None,
                },
                "tokens": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                },
            }
        },
    )

    message: str = Field(
        "User account registered successfully.",
        description="Human-readable success message.",
        examples=["User account registered successfully."],
    )
    user: UserSummary = Field(
        ...,
        description="Summary profile of the newly created user.",
    )
    tokens: TokenPair = Field(
        ...,
        description="Generated access and refresh JWT token pair.",
    )


class LoginRequest(BaseModel):
    """Request DTO for authenticating existing local users."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jane.doe@example.com",
                "password": "SecurePassword123!",
            }
        }
    )

    email: EmailStr = Field(
        ...,
        description="Account login email address.",
        examples=["jane.doe@example.com"],
    )
    password: str = Field(
        ...,
        description="User account authentication password.",
        examples=["SecurePassword123!"],
    )

    @field_validator("email", mode="before")
    @classmethod
    def validate_and_clean_email(cls, v: Any) -> str:
        """Strip and lowercase incoming email."""
        return clean_email(v)

    @field_validator("password")
    @classmethod
    def validate_login_password(cls, v: str) -> str:
        """Ensure password is provided and non-blank."""
        if not v or not v.strip():
            raise ValueError("Password cannot be blank or empty.")
        return v


class LoginResponse(BaseModel):
    """Response DTO returned upon successful authentication."""

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "message": "User authenticated successfully.",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "jane.doe@example.com",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "full_name": "Jane Doe",
                    "role": "candidate",
                    "provider": "local",
                    "is_verified": True,
                    "avatar_url": None,
                },
                "tokens": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                },
            }
        },
    )

    message: str = Field(
        "User authenticated successfully.",
        description="Human-readable status message.",
        examples=["User authenticated successfully."],
    )
    user: UserSummary = Field(
        ...,
        description="Authenticated user summary profile.",
    )
    tokens: TokenPair = Field(
        ...,
        description="Newly issued JWT token pair.",
    )


class RefreshTokenRequest(BaseModel):
    """Request DTO for renewing expired access tokens using a valid refresh token."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
    )

    refresh_token: str = Field(
        ...,
        description="Valid active refresh token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )

    @field_validator("refresh_token")
    @classmethod
    def validate_token_value(cls, v: str) -> str:
        """Strip whitespace and reject blank tokens."""
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Refresh token cannot be empty or consist only of whitespace.")
        return v.strip()


class RefreshTokenResponse(BaseModel):
    """Response DTO containing newly rotated JWT access and refresh token pair."""

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "message": "Token pair refreshed successfully.",
                "tokens": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                },
            }
        },
    )

    message: str = Field(
        "Token pair refreshed successfully.",
        description="Human-readable success message.",
        examples=["Token pair refreshed successfully."],
    )
    tokens: TokenPair = Field(
        ...,
        description="Newly rotated JWT access and refresh token pair.",
    )


class LogoutResponse(BaseModel):
    """Response DTO returned upon session revocation/logout."""

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "message": "User session logged out successfully.",
                "success": True,
            }
        },
    )

    message: str = Field(
        "User session logged out successfully.",
        description="Human-readable operation summary.",
        examples=["User session logged out successfully."],
    )
    success: bool = Field(
        True,
        description="Indicates successful completion of logout.",
        examples=[True],
    )


class CurrentUserResponse(BaseModel):
    """Response DTO for returning current authenticated user profile."""

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "jane.doe@example.com",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "full_name": "Jane Doe",
                    "role": "candidate",
                    "provider": "local",
                    "is_verified": True,
                    "avatar_url": None,
                }
            }
        },
    )

    user: UserSummary = Field(
        ...,
        description="Summary details of the currently authenticated user.",
    )
