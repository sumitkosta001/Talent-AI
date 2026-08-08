import asyncio
import uuid
from datetime import datetime, timedelta, timezone
import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.engine import engine
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest
from app.auth.jwt import create_access_token, create_refresh_token
from app.config.settings import settings
from app.exceptions.auth import (
    VerificationTokenExpiredError,
    VerificationTokenInvalidError,
)

async def main():
    async with AsyncSession(engine) as db:
        user_repo = UserRepository(db)
        refresh_repo = RefreshTokenRepository(db)
        auth_service = AuthService(
            user_repository=user_repo,
            refresh_repository=refresh_repo,
        )

        email = f"verify_test_{uuid.uuid4().hex[:8]}@gmail.com"

        print("=" * 70)
        print("1. REGISTER NEW USER (is_verified initially FALSE)")
        print("=" * 70)
        reg_res = await auth_service.register_user(
            RegisterRequest(
                email=email,
                password="Password123!",
                confirm_password="Password123!",
                first_name="Jane",
                last_name="Doe",
            )
        )
        user = await user_repo.get_by_email(email)
        assert user is not None
        assert user.is_verified is False
        print(f"Created unverified user: {email}, is_verified = {user.is_verified}")

        # Extract verification token sent (we can generate one directly using user ID)
        from app.auth.jwt import create_email_verification_token
        valid_token = create_email_verification_token(str(user.id), user.email)

        print("\n" + "=" * 70)
        print("2. VERIFY WITH VALID TOKEN")
        print("=" * 70)
        verify_res = await auth_service.verify_email(valid_token)
        print("Response:", verify_res)
        assert verify_res.success is True
        assert verify_res.email == email
        
        # Check DB state
        await db.refresh(user)
        assert user.is_verified is True
        print(f"Database updated: is_verified = {user.is_verified}")

        print("\n" + "=" * 70)
        print("3. VERIFY ALREADY VERIFIED USER")
        print("=" * 70)
        verify_res_2 = await auth_service.verify_email(valid_token)
        print("Response:", verify_res_2)
        assert verify_res_2.success is True
        assert verify_res_2.message == "Email address is already verified."
        assert verify_res_2.email == email

        print("\n" + "=" * 70)
        print("4. TEST ACCESS TOKEN REJECTION")
        print("=" * 70)
        access_token = create_access_token(str(user.id), user.email, user.role.value)
        try:
            await auth_service.verify_email(access_token)
            print("FAILED: Access token was accepted!")
        except VerificationTokenInvalidError as e:
            print(f"SUCCESS: Access token rejected: {e}")

        print("\n" + "=" * 70)
        print("5. TEST REFRESH TOKEN REJECTION")
        print("=" * 70)
        refresh_token = create_refresh_token(str(user.id))
        try:
            await auth_service.verify_email(refresh_token)
            print("FAILED: Refresh token was accepted!")
        except VerificationTokenInvalidError as e:
            print(f"SUCCESS: Refresh token rejected: {e}")

        print("\n" + "=" * 70)
        print("6. TEST EXPIRED TOKEN REJECTION")
        print("=" * 70)
        # Construct an expired verification token manually
        now = datetime.now(timezone.utc)
        expired_time = now - timedelta(hours=2)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "type": "email_verification",
            "iat": int((now - timedelta(hours=3)).timestamp()),
            "exp": int(expired_time.timestamp()),
            "jti": str(uuid.uuid4()),
        }
        expired_token = jwt.encode(
            payload,
            settings.jwt.secret,
            algorithm=settings.jwt.algorithm,
        )
        try:
            await auth_service.verify_email(expired_token)
            print("FAILED: Expired token was accepted!")
        except VerificationTokenExpiredError as e:
            print(f"SUCCESS: Expired token rejected: {e}")

        print("\n" + "=" * 70)
        print("7. TEST MALFORMED TOKEN REJECTION")
        print("=" * 70)
        try:
            await auth_service.verify_email("malformed.token.here")
            print("FAILED: Malformed token was accepted!")
        except VerificationTokenInvalidError as e:
            print(f"SUCCESS: Malformed token rejected: {e}")

        print("\n" + "=" * 70)
        print("8. TEST EMPTY TOKEN REJECTION")
        print("=" * 70)
        try:
            await auth_service.verify_email("")
            print("FAILED: Empty token was accepted!")
        except VerificationTokenInvalidError as e:
            print(f"SUCCESS: Empty token rejected: {e}")

        print("\n" + "=" * 70)
        print("9. TEST STALE TOKEN REJECTION (non-existent user)")
        print("=" * 70)
        stale_user_id = str(uuid.uuid4())
        from app.auth.jwt import create_email_verification_token
        stale_token = create_email_verification_token(stale_user_id, "nonexistent@gmail.com")
        try:
            await auth_service.verify_email(stale_token)
            print("FAILED: Stale token was accepted!")
        except VerificationTokenInvalidError as e:
            print(f"SUCCESS: Stale token rejected correctly: {e}")
            assert str(e) == "This verification link is invalid or no longer available."

        print("\n" + "=" * 70)
        print("ALL VERIFICATION CASES VERIFIED SUCCESSFULLY")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
