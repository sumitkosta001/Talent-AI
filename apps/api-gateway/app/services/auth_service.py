"""Authentication Business Logic Service.

Encapsulates all core authentication operations including user registration,
email verification workflows, credential validation, JWT token pair issuance,
refresh token rotation, session revocation, and authenticated profile retrieval.
"""

import logging
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, Union

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.enums import UserRole, AuthProvider
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.email_service import EmailService
from app.auth.password import hash_password, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    create_email_verification_token,
    verify_access_token,
    verify_refresh_token,
    verify_email_verification_token,
    decode_token,
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
    VerifyEmailRequest,
    ResendVerificationRequest,
    VerifyEmailResponse,
    ResendVerificationResponse,
)
from app.exceptions.auth import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    AccountDisabledError,
    InvalidTokenError,
    ExpiredTokenError,
    VerificationTokenExpiredError,
    VerificationTokenInvalidError,
)
from app.exceptions.users import UserNotFoundError

logger = logging.getLogger("talentai.services.auth")


class AuthService:
    """Service handling core authentication business logic, email verification, and session workflows."""

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
        email_service: Optional[EmailService] = None,
    ) -> None:
        """Initialize AuthService with required database repositories and email service.

        Args:
            user_repository: Data access repository for User entities.
            refresh_repository: Data access repository for RefreshToken entities.
            email_service: Optional EmailService instance for email delivery.
        """
        self.user_repo = user_repository
        self.refresh_repo = refresh_repository
        self.email_service = email_service if email_service is not None else EmailService()

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
        import hashlib
        token_hash = hashlib.sha256(refresh_token_str.encode("utf-8")).hexdigest()

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
        """Register a new user account, issue verification JWT token, send email, and return token pair.

        Args:
            request: Validated registration request DTO containing user registration details.

        Returns:
            RegisterResponse containing success message, user summary, verification_sent, and token pair.

        Raises:
            EmailAlreadyExistsError: If an account with the specified email already exists.
        """
        if await self.user_repo.email_exists(request.email):
            raise EmailAlreadyExistsError(
                f"An account with email '{request.email}' already exists."
            )

        hashed_pw = hash_password(request.password)
        allowed_reg_roles = {UserRole.CANDIDATE, UserRole.RECRUITER, UserRole.HIRING_MANAGER}
        assigned_role = request.role if (request.role and request.role in allowed_reg_roles) else UserRole.CANDIDATE

        new_user = User(
            email=request.email,
            password_hash=hashed_pw,
            first_name=request.first_name,
            last_name=request.last_name,
            role=assigned_role,
            provider=AuthProvider.LOCAL,
            is_active=True,
            is_verified=False,
            verified_at=None,
        )

        user = await self.user_repo.create_user(new_user)

        # Generate JWT email verification token
        verification_token = create_email_verification_token(
            user_id=str(user.id),
            email=user.email,
        )

        # Dispatch verification email asynchronously
        try:
            await self.email_service.send_verification_email(
                email=user.email,
                name=user.first_name,
                token=verification_token,
            )
            logger.info("Verification email dispatched for registered user: %s", user.email)
        except Exception as exc:
            logger.warning("Failed to send registration verification email to %s: %s", user.email, exc)

        # Issue JWT Access & Refresh Token Pair
        tokens = await self._issue_token_pair(user)

        return RegisterResponse(
            message="User account registered successfully. Verification email sent.",
            user=UserSummary.model_validate(user),
            verification_sent=True,
            tokens=tokens,
        )

    async def verify_email(self, token: str) -> VerifyEmailResponse:
        """Validate a JWT email verification token and mark user account as verified.

        Args:
            token: Raw JWT email verification token string.

        Returns:
            VerifyEmailResponse indicating successful email verification.

        Raises:
            VerificationTokenInvalidError: If token signature, structure, or type is invalid.
            VerificationTokenExpiredError: If verification token has passed its 24h expiration limit.
            UserNotFoundError: If associated user record does not exist in database.
        """
        if not token or not token.strip():
            raise VerificationTokenInvalidError("Verification token must be provided.")

        payload = verify_email_verification_token(token.strip())

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise VerificationTokenInvalidError("Verification token missing subject claim.")

        user = await self.user_repo.get_by_id(user_id_str)
        if not user:
            raise VerificationTokenInvalidError(
                "This verification link is invalid or no longer available."
            )

        if user.is_verified:
            logger.info("User email %s is already verified.", user.email)
            return VerifyEmailResponse(
                success=True,
                message="Email address is already verified.",
                email=user.email,
            )

        now = datetime.now(timezone.utc)
        user.is_verified = True
        user.verified_at = now
        await self.user_repo.update_user(user)

        logger.info("Successfully verified email for user %s at %s", user.email, now.isoformat())

        return VerifyEmailResponse(
            success=True,
            message="Email verified successfully.",
            email=user.email,
        )

    async def resend_verification_email(
        self, request: ResendVerificationRequest
    ) -> ResendVerificationResponse:
        """Issue a new JWT email verification token and send a fresh verification email link.

        Args:
            request: ResendVerificationRequest containing target account email.

        Returns:
            ResendVerificationResponse indicating status message.
        """
        user = await self.user_repo.get_by_email(request.email)
        if not user:
            # Security best practice: return success without leaking account non-existence
            logger.info("Resend verification requested for non-existent email: %s", request.email)
            return ResendVerificationResponse(
                success=True,
                message="Verification email sent.",
            )

        if user.is_verified:
            logger.info("Resend verification requested for already-verified email: %s", user.email)
            return ResendVerificationResponse(
                success=True,
                message="Email address is already verified.",
            )

        # Issue fresh JWT email verification token
        verification_token = create_email_verification_token(
            user_id=str(user.id),
            email=user.email,
        )

        # Dispatch email
        try:
            await self.email_service.send_resend_verification_email(
                email=user.email,
                name=user.first_name,
                token=verification_token,
            )
            logger.info("Resent verification email successfully to %s", user.email)
        except Exception as exc:
            logger.warning("Failed to resend verification email to %s: %s", user.email, exc)

        return ResendVerificationResponse(
            success=True,
            message="Verification email sent.",
        )

    async def login_user(self, request: LoginRequest) -> LoginResponse:
        """Authenticate user credentials and issue a new token pair upon success."""
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
        """Rotate refresh token and issue a new token pair."""
        raw_token = request.refresh_token
        payload = verify_refresh_token(raw_token)

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenError("Refresh token missing subject claim.")

        import hashlib
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        db_token = await self.refresh_repo.get_by_token(token_hash)

        if not db_token:
            raise InvalidTokenError("Refresh token not found or already invalidated.")

        if db_token.revoked:
            raise InvalidTokenError("Refresh token has been revoked.")

        if db_token.is_expired:
            raise ExpiredTokenError("Refresh token has expired.")

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
        """Revoke a single refresh token session."""
        verify_refresh_token(refresh_token)

        import hashlib
        token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
        db_token = await self.refresh_repo.get_by_token(token_hash)

        if db_token and not db_token.revoked:
            await self.refresh_repo.revoke_token(db_token)

        return LogoutResponse(
            message="User session logged out successfully.",
            success=True,
        )

    async def logout_all_devices(self, user_id: Union[UUID, str]) -> LogoutResponse:
        """Revoke all active refresh tokens for a user across all devices."""
        await self.refresh_repo.revoke_all_user_tokens(user_id)
        return LogoutResponse(
            message="All active user sessions logged out successfully.",
            success=True,
        )

    async def get_current_user(self, access_token: str) -> UserSummary:
        """Retrieve UserSummary profile for an authenticated access token."""
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
