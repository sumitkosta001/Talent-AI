"""User Entity Database Repository.

Provides data access routines for User identity management, registration,
email lookups, and account status operations using SQLAlchemy 2.0 Async ORM.
"""

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Repository managing User entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize UserRepository with an active AsyncSession.

        Args:
            db: SQLAlchemy AsyncSession database session.
        """
        self.db = db

    async def create_user(self, user: User) -> User:
        """Persist a new User entity to the database.

        Args:
            user: Unpersisted User ORM instance.

        Returns:
            Persisted User instance with database-generated columns populated.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, user_id: UUID | str) -> Optional[User]:
        """Fetch a active User entity by its unique primary key UUID.

        Args:
            user_id: User UUID or string representation.

        Returns:
            Matching User instance or None if not found/soft-deleted.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = select(User).where(
            User.id == user_id,
            User.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a User entity by email address (case-insensitive search).

        Args:
            email: Account login email address.

        Returns:
            Matching User instance or None if not found/soft-deleted.
        """
        if not email or not email.strip():
            return None

        clean_email = email.strip().lower()
        stmt = select(User).where(
            func.lower(User.email) == clean_email,
            User.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """Check whether a non-deleted user exists with the given email address.

        Args:
            email: Email address to check for existence.

        Returns:
            True if email exists in database, False otherwise.
        """
        user = await self.get_by_email(email)
        return user is not None

    async def update_user(self, user: User) -> User:
        """Commit updates for an existing User entity.

        Args:
            user: Modified User ORM instance.

        Returns:
            Refreshed User instance reflecting updated database state.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            user.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception:
            await self.db.rollback()
            raise

    async def soft_delete_user(self, user: User) -> None:
        """Perform logical soft deletion on a User entity.

        Sets is_deleted=True and deleted_at to current UTC timestamp without deleting row.

        Args:
            user: User entity to soft-delete.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            now = datetime.now(timezone.utc)
            user.is_deleted = True
            user.deleted_at = now
            user.updated_at = now
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def list_active_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Retrieve paginated list of non-deleted, active users ordered by creation date.

        Args:
            limit: Maximum number of records to return.
            offset: Number of records to skip for pagination.

        Returns:
            List of active User entities.
        """
        stmt = (
            select(User)
            .where(
                User.is_deleted == False,
                User.is_active == True,
            )
            .order_by(User.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_users(self) -> int:
        """Count total number of non-deleted users in the database.

        Returns:
            Total active/non-deleted user count.
        """
        stmt = select(func.count(User.id)).where(User.is_deleted == False)
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count if count is not None else 0
