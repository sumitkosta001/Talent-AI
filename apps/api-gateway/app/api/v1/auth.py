"""Authentication API Router.

Provides HTTP REST endpoints for user registration, authentication (login),
token rotation (refresh), session termination (logout, logout-all), and current user state inspection.
Uses HTTP Bearer authentication for JWT bearer tokens.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService
from app.auth.dependencies import get_current_active_user
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutResponse,
    CurrentUserResponse,
    UserSummary,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency provider instantiating AuthService with repository dependencies.

    Args:
        db: Scoped database AsyncSession from get_db dependency.

    Returns:
        Configured AuthService instance.
    """
    user_repo = UserRepository(db)
    refresh_repo = RefreshTokenRepository(db)
    return AuthService(user_repository=user_repo, refresh_repository=refresh_repo)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description=(
        "Register a new TalentAI candidate user account. Validates email uniqueness, "
        "hashes the password using Argon2id, creates the user record, and issues an initial JWT token pair."
    ),
    responses={
        201: {"description": "User account created successfully."},
        400: {"description": "Validation error or invalid request payload."},
        409: {"description": "Account with specified email already exists."},
        422: {"description": "Unprocessable entity (Pydantic validation failure)."},
    },
)
async def register(
    request: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterResponse:
    """Register a new TalentAI user account.

    Args:
        request: Validated registration request DTO.
        auth_service: Injected AuthService instance.

    Returns:
        RegisterResponse containing user profile summary and JWT token pair.
    """
    return await auth_service.register_user(request)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user credentials",
    description=(
        "Authenticate a user using email and password JSON credentials. Upon successful validation, "
        "resets failed login counters, records last login timestamp, and issues a fresh JWT access and refresh token pair."
    ),
    responses={
        200: {"description": "User authenticated successfully."},
        401: {"description": "Invalid email or password credentials."},
        403: {"description": "User account is suspended or deactivated."},
        422: {"description": "Validation failure on login request payload."},
    },
)
async def login(
    request: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    """Authenticate user credentials using email and password JSON.

    Args:
        request: Validated login credentials request DTO.
        auth_service: Injected AuthService instance.

    Returns:
        LoginResponse containing user summary and new JWT token pair.
    """
    return await auth_service.login_user(request)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Rotate refresh token and issue new access token",
    description=(
        "Validate an existing JWT refresh token against database state, revoke the current token, "
        "and issue a new access and refresh token pair (Refresh Token Rotation)."
    ),
    responses={
        200: {"description": "Token pair refreshed successfully."},
        401: {"description": "Refresh token is invalid, expired, or revoked."},
        403: {"description": "Associated user account is inactive."},
        404: {"description": "User associated with refresh token not found."},
    },
)
async def refresh_tokens(
    request: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RefreshTokenResponse:
    """Rotate refresh token and generate a new access token.

    Args:
        request: RefreshTokenRequest containing active refresh token string.
        auth_service: Injected AuthService instance.

    Returns:
        RefreshTokenResponse containing new JWT access and refresh token pair.
    """
    return await auth_service.refresh_access_token(request)


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user session",
    description="Invalidate current refresh token by marking it as revoked in database storage.",
    responses={
        200: {"description": "User session logged out successfully."},
        401: {"description": "Invalid refresh token payload or signature."},
    },
)
async def logout(
    request: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LogoutResponse:
    """Logout current user session by revoking the refresh token.

    Args:
        request: RefreshTokenRequest containing the refresh token to revoke.
        auth_service: Injected AuthService instance.

    Returns:
        LogoutResponse indicating successful revocation.
    """
    return await auth_service.logout(request.refresh_token)


@router.post(
    "/logout-all",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user from all active devices",
    description="Revoke all active refresh tokens for the authenticated user across all devices and sessions.",
    responses={
        200: {"description": "All user sessions logged out successfully."},
        401: {"description": "Not authenticated or bearer token invalid."},
    },
)
async def logout_all_devices(
    current_user: Annotated[User, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LogoutResponse:
    """Revoke all active refresh tokens for the authenticated user.

    Args:
        current_user: Currently authenticated active User entity.
        auth_service: Injected AuthService instance.

    Returns:
        LogoutResponse indicating successful bulk revocation.
    """
    return await auth_service.logout_all_devices(current_user.id)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile",
    description="Retrieve the profile details and role summary of the currently authenticated user.",
    responses={
        200: {"description": "Current user profile fetched successfully."},
        401: {"description": "Not authenticated or bearer token invalid."},
        403: {"description": "User account is suspended or inactive."},
    },
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> CurrentUserResponse:
    """Return currently authenticated user's profile summary.

    Args:
        current_user: Currently authenticated active User entity.

    Returns:
        CurrentUserResponse containing user summary payload.
    """
    return CurrentUserResponse(user=UserSummary.model_validate(current_user))
