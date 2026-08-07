import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import engine
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
)


async def main():
    async with AsyncSession(engine) as db:

        user_repo = UserRepository(db)
        refresh_repo = RefreshTokenRepository(db)

        auth_service = AuthService(
            user_repository=user_repo,
            refresh_repository=refresh_repo,
        )

        email = f"auth_test_{uuid.uuid4().hex[:8]}@gmail.com"

        print("=" * 70)
        print("TEST 1 - REGISTER")
        print("=" * 70)

        register_response = await auth_service.register_user(
            RegisterRequest(
                email=email,
                password="Password123!",
                confirm_password="Password123!",
                first_name="John",
                last_name="Doe",
            )
        )

        print(register_response)

        print("\n")

        print("=" * 70)
        print("TEST 2 - LOGIN")
        print("=" * 70)

        login_response = await auth_service.login_user(
            LoginRequest(
                email=email,
                password="Password123!",
            )
        )

        print(login_response)

        print("\n")

        print("=" * 70)
        print("TEST 3 - REFRESH TOKEN")
        print("=" * 70)

        refresh_response = await auth_service.refresh_access_token(
            RefreshTokenRequest(
                refresh_token=login_response.tokens.refresh_token
            )
        )

        print(refresh_response)

        print("\n")

        print("=" * 70)
        print("TEST 4 - CURRENT USER")
        print("=" * 70)

        current_user = await auth_service.get_current_user(
            refresh_response.tokens.access_token
        )

        print(current_user)

        print("\n")

        print("=" * 70)
        print("TEST 5 - LOGOUT")
        print("=" * 70)

        logout = await auth_service.logout(
            refresh_response.tokens.refresh_token
        )

        print(logout)

        print("\n")

        print("=" * 70)
        print("TEST 6 - LOGOUT ALL DEVICES")
        print("=" * 70)

        logout_all = await auth_service.logout_all_devices(
            current_user.id
        )

        print(logout_all)

        print("\n")
        print("=" * 70)
        print("ALL AUTH SERVICE TESTS PASSED")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())