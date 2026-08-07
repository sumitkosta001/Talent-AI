import asyncio
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from app.database.session import SessionLocal

from app.models.user import User
from app.models.refresh_token import RefreshToken

from app.models.enums import UserRole, AuthProvider

from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository

from app.auth.password import hash_password


async def main():

    async with SessionLocal() as db:

        user_repo = UserRepository(db)
        token_repo = RefreshTokenRepository(db)

        print("=" * 70)
        print("USER REPOSITORY TEST")
        print("=" * 70)

        email = f"repo_test_{uuid4().hex[:8]}@gmail.com"

        user = User(
            first_name="Repository",
            last_name="Testing",
            email=email,
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
            provider=AuthProvider.LOCAL,
        )

        user = await user_repo.create_user(user)

        print("✔ User Created")
        print(user.id)

        print()

        found = await user_repo.get_by_email(email)
        assert found is not None, f"User with email {email} was not found"

        print("✔ get_by_email")
        print(found.email)

        print()

        exists = await user_repo.email_exists(email)

        print("✔ email_exists")
        print(exists)

        print()

        found.first_name = "Updated"

        updated = await user_repo.update_user(found)

        print("✔ update_user")
        print(updated.first_name)

        print()

        total = await user_repo.count_users()

        print("✔ count_users")
        print(total)

        print()

        users = await user_repo.list_active_users()

        print("✔ list_active_users")
        print(len(users))

        print()

        print("=" * 70)
        print("REFRESH TOKEN REPOSITORY TEST")
        print("=" * 70)

        refresh = RefreshToken(
            user_id=user.id,
            token="repo_test_token_" + uuid4().hex,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=7),
        )

        refresh = await token_repo.create_refresh_token(refresh)

        print("✔ Refresh Token Created")

        token = await token_repo.get_by_token(refresh.token)
        assert token is not None, "Refresh token was not found"

        print("✔ get_by_token")
        print(token.token)

        print()

        active = await token_repo.get_active_user_tokens(user.id)

        print("✔ get_active_user_tokens")
        print(len(active))

        print()

        count = await token_repo.count_active_tokens(user.id)

        print("✔ count_active_tokens")
        print(count)

        print()

        await token_repo.revoke_token(token)

        print("✔ revoke_token")

        print()

        count = await token_repo.count_active_tokens(user.id)

        print("Active After Revoke:", count)

        print()

        await user_repo.soft_delete_user(user)

        print("✔ soft_delete_user")

        deleted = await user_repo.get_by_email(email)

        print()

        print("After Delete:", deleted)

        print()

        print("=" * 70)
        print("ALL TESTS PASSED")
        print("=" * 70)


asyncio.run(main())