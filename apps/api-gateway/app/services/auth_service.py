"""Authentication Business Logic Service.

Encapsulates all core authentication operations including user registration,
credential validation, JWT token pair issuance, refresh token rotation,
session revocation, and authenticated profile retrieval.
"""

import hashlib
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, Union

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.enums import UserRole, AuthProvider
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.auth.password import hash_password, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_access_token,
    verify_refresh_token,
)
from app.schemas.auth import (
    UserSummary,
    TokenPair,
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutResponse,
)
from app.exceptions.auth import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    AccountDisabledError,
    InvalidTokenError,
    ExpiredTokenError,
    TokenExpiredError,
)
from app.exceptions.users import UserNotFoundError


class AuthService:
    """Service handling core authentication business logic and session workflows."""

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ) -> None:
        """Initialize AuthService with required database repositories.

        Args:
            user_repository: Data access repository for User entities.
            refresh_repository: Data access repository for RefreshToken entities.
        """
        self.user_repo = user_repository
        self.refresh_repo = refresh_repository

    def _hash_token(self, token_str: str) -> str:
        """Compute SHA-256 hash of a raw JWT string for secure database storage.

        Args:
            token_str: Plaintext JWT string.

        Returns:
            SHA-256 hex digest string.
        """
        return hashlib.sha256(token_str.encode("utf-8")).hexdigest()

    async def _issue_token_pair(self, user: User) -> TokenPair:
        """Generate, persist, and return a fresh access and refresh token pair.

        Args:
            user: Authenticated User ORM entity.

        Returns:
            TokenPair containing access_token, refresh_token, and token_type.
        """
        access_token_str = create_access_token(
            user_id=str(user.id),
            email=user.email,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
        )
        refresh_token_str = create_refresh_token(user_id=str(user.id))

        # Calculate expiration time from encoded JWT payload
        payload = decode_token(refresh_token_str)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        else:
            expires_at = datetime.now(timezone.utc)

        # Hash refresh token for storage
        token_hash = self._hash_token(refresh_token_str)

        refresh_token_obj = RefreshToken(
            user_id=user.id,
            token=token_hash,
            expires_at=expires_at,
            revoked=False,
        )
        await self.refresh_repo.create_refresh_token(refresh_token_obj)

        return TokenPair(
            access_token=access_token_str,
            refresh_token=refresh_token_str,
            token_type="bearer",
        )

    async def register_user(self, request: RegisterRequest) -> RegisterResponse:
        """Register a new user account with hashed password and initial token pair.

        Args:
            request: Validated registration request DTO containing registration details.

        Returns:
            RegisterResponse containing success message, user summary, and token pair.

        Raises:
            EmailAlreadyExistsError: If an account with the specified email already exists.
        """
        if await self.user_repo.email_exists(request.email):
            raise EmailAlreadyExistsError(
                f"An account with email '{request.email}' already exists."
            )

        hashed_pw = hash_password(request.password)

        new_user = User(
            email=request.email,
            password_hash=hashed_pw,
            first_name=request.first_name,
            last_name=request.last_name,
            role=UserRole.CANDIDATE,
            provider=AuthProvider.LOCAL,
            is_active=True,
            is_verified=False,
        )

        user = await self.user_repo.create_user(new_user)
        tokens = await self._issue_token_pair(user)

        return RegisterResponse(
            message="User account registered successfully.",
            user=UserSummary.model_validate(user),
            tokens=tokens,
        )

    async def login_user(self, request: LoginRequest) -> LoginResponse:
        """Authenticate user credentials and issue a new token pair upon success.

        Args:
            request: Validated login request DTO containing email and password.

        Returns:
            LoginResponse containing success message, user summary, and token pair.

        Raises:
            InvalidCredentialsError: If email is not found or password verification fails.
            AccountDisabledError: If user account has been deactivated or suspended.
        """
        user = await self.user_repo.get_by_email(request.email)
        if not user or not user.password_hash:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(request.password, user.password_hash):
            user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
            await self.user_repo.update_user(user)
            raise InvalidCredentialsError("Invalid email or password.")

        if not user.is_active:
            raise AccountDisabledError("User account has been suspended or deactivated.")

        # Reset failed attempts and update last login timestamp
        user.failed_login_attempts = 0
        user.last_login_at = datetime.now(timezone.utc)
        user = await self.user_repo.update_user(user)

        tokens = await self._issue_token_pair(user)

        return LoginResponse(
            message="User authenticated successfully.",
            user=UserSummary.model_validate(user),
            tokens=tokens,
        )

    async def refresh_access_token(
        self, request: RefreshTokenRequest
    ) -> RefreshTokenResponse:
        """Rotate refresh token and issue a new token pair.

        Verifies JWT signature, verifies DB token state (not revoked/expired), revokes the old
        token, and issues a fresh token pair (Refresh Token Rotation).

        Args:
            request: RefreshTokenRequest containing the current raw refresh token.

        Returns:
            RefreshTokenResponse containing success message and new token pair.

        Raises:
            InvalidTokenError: If token is malformed, invalid, or revoked.
            TokenExpiredError: If token has passed its expiration limit.
            AccountDisabledError: If user account is inactive.
            UserNotFoundError: If associated user record is missing.
        """
        raw_token = request.refresh_token
        payload = verify_refresh_token(raw_token)

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenError("Refresh token missing subject claim.")

        token_hash = self._hash_token(raw_token)
        db_token = await self.refresh_repo.get_by_token(token_hash)

        if not db_token:
            raise InvalidTokenError("Refresh token not found or already invalidated.")

        if db_token.revoked:
            raise InvalidTokenError("Refresh token has been revoked.")

        if db_token.is_expired:
            raise TokenExpiredError("Refresh token has expired.")

        user = await self.user_repo.get_by_id(user_id_str)
        if not user:
            raise UserNotFoundError(user_id_str)

        if not user.is_active:
            raise AccountDisabledError("User account has been suspended or deactivated.")

        # Revoke old refresh token (Token Rotation)
        await self.refresh_repo.revoke_token(db_token)

        # Issue new token pair
        new_tokens = await self._issue_token_pair(user)

        return RefreshTokenResponse(
            message="Token pair refreshed successfully.",
            tokens=new_tokens,
        )

    async def logout(self, refresh_token: str) -> LogoutResponse:
        """Revoke a single refresh token session.

        Args:
            refresh_token: Raw JWT refresh token string to revoke.

        Returns:
            LogoutResponse indicating successful revocation.

        Raises:
            InvalidTokenError: If token signature or format is invalid.
        """
        # Validate JWT format/signature
        verify_refresh_token(refresh_token)

        token_hash = self._hash_token(refresh_token)
        db_token = await self.refresh_repo.get_by_token(token_hash)

        if db_token and not db_token.revoked:
            await self.refresh_repo.revoke_token(db_token)

        return LogoutResponse(
            message="User session logged out successfully.",
            success=True,
        )

    async def logout_all_devices(self, user_id: Union[UUID, str]) -> LogoutResponse:
        """Revoke all active refresh tokens for a user across all devices.

        Args:
            user_id: User UUID or string identifier.

        Returns:
            LogoutResponse indicating successful bulk session revocation.
        """
        await self.refresh_repo.revoke_all_user_tokens(user_id)
        return LogoutResponse(
            message="All active user sessions logged out successfully.",
            success=True,
        )

    async def get_current_user(self, access_token: str) -> UserSummary:
        """Retrieve UserSummary profile for an authenticated access token.

        Args:
            access_token: Raw JWT access token string.

        Returns:
            UserSummary profile DTO.

        Raises:
            InvalidTokenError: If access token signature or claims are invalid.
            UserNotFoundError: If user associated with token sub claim does not exist.
            AccountDisabledError: If user account is suspended or inactive.
        """
        payload = verify_access_token(access_token)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenError("Access token missing subject claim.")

        user = await self.user_repo.get_by_id(user_id_str)
        if not user:
            raise UserNotFoundError(user_id_str)

        if not user.is_active:
            raise AccountDisabledError("User account has been suspended or deactivated.")

        return UserSummary.model_validate(user)
