"""RefreshToken Entity Database Repository.

Provides data access routines for JWT refresh token persistence, token rotation,
revocation, session lookup, and cleanup using SQLAlchemy 2.0 Async ORM.
"""

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    """Repository managing RefreshToken entity database operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize RefreshTokenRepository with an active AsyncSession.

        Args:
            db: SQLAlchemy AsyncSession database session.
        """
        self.db = db

    async def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        """Persist a new RefreshToken entity to the database.

        Args:
            token: Unpersisted RefreshToken ORM instance.

        Returns:
            Persisted RefreshToken instance with database-generated columns populated.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            self.db.add(token)
            await self.db.commit()
            await self.db.refresh(token)
            return token
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_token(self, token_hash: str) -> Optional[RefreshToken]:
        """Fetch a non-deleted RefreshToken entity by its SHA-256 token hash.

        Args:
            token_hash: SHA-256 hash string of the refresh token.

        Returns:
            Matching RefreshToken instance or None if not found/soft-deleted.
        """
        if not token_hash or not token_hash.strip():
            return None

        stmt = select(RefreshToken).where(
            RefreshToken.token == token_hash.strip(),
            RefreshToken.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, token_id: UUID | str) -> Optional[RefreshToken]:
        """Fetch a non-deleted RefreshToken entity by its primary key UUID.

        Args:
            token_id: RefreshToken UUID or string representation.

        Returns:
            Matching RefreshToken instance or None if not found/soft-deleted.
        """
        if isinstance(token_id, str):
            token_id = UUID(token_id)

        stmt = select(RefreshToken).where(
            RefreshToken.id == token_id,
            RefreshToken.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_user_tokens(self, user_id: UUID | str) -> List[RefreshToken]:
        """Retrieve all non-revoked, unexpired, non-deleted refresh tokens for a user.

        Args:
            user_id: Owner User UUID or string representation.

        Returns:
            List of active RefreshToken entities.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        now = datetime.now(timezone.utc)
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
                RefreshToken.expires_at > now,
                RefreshToken.is_deleted == False,
            )
            .order_by(RefreshToken.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def revoke_token(self, token: RefreshToken) -> RefreshToken:
        """Revoke a single refresh token instance.

        Sets revoked=True and updates updated_at.

        Args:
            token: RefreshToken instance to revoke.

        Returns:
            Refreshed RefreshToken instance with revoked status.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            now = datetime.now(timezone.utc)
            token.revoked = True
            token.updated_at = now
            await self.db.commit()
            await self.db.refresh(token)
            return token
        except Exception:
            await self.db.rollback()
            raise

    async def revoke_all_user_tokens(self, user_id: UUID | str) -> int:
        """Bulk revoke all active refresh tokens belonging to a specific user.

        Used during security events (password reset, logout-all-devices).

        Args:
            user_id: Owner User UUID or string representation.

        Returns:
            Number of affected/revoked token records.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        try:
            now = datetime.now(timezone.utc)
            stmt = (
                update(RefreshToken)
                .where(
                    RefreshToken.user_id == user_id,
                    RefreshToken.revoked == False,
                    RefreshToken.is_deleted == False,
                )
                .values(
                    revoked=True,
                    updated_at=now,
                )
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return getattr(result, "rowcount", getattr(getattr(result, "raw", None), "rowcount", 0))
        except Exception:
            await self.db.rollback()
            raise

    async def delete_expired_tokens(self) -> int:
        """Soft delete all refresh tokens that have passed their expiration timestamp.

        Intended for periodic background cleanup jobs.

        Returns:
            Number of soft-deleted expired token records.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            now = datetime.now(timezone.utc)
            stmt = (
                update(RefreshToken)
                .where(
                    RefreshToken.expires_at < now,
                    RefreshToken.is_deleted == False,
                )
                .values(
                    is_deleted=True,
                    deleted_at=now,
                    updated_at=now,
                )
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return getattr(result, "rowcount", getattr(getattr(result, "raw", None), "rowcount", 0))
        except Exception:
            await self.db.rollback()
            raise

    async def delete_revoked_tokens(self) -> int:
        """Soft delete all refresh tokens that have been marked as revoked.

        Intended for periodic database maintenance jobs.

        Returns:
            Number of soft-deleted revoked token records.

        Raises:
            Exception: Re-raises database exceptions after performing session rollback.
        """
        try:
            now = datetime.now(timezone.utc)
            stmt = (
                update(RefreshToken)
                .where(
                    RefreshToken.revoked == True,
                    RefreshToken.is_deleted == False,
                )
                .values(
                    is_deleted=True,
                    deleted_at=now,
                    updated_at=now,
                )
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return getattr(result, "rowcount", getattr(getattr(result, "raw", None), "rowcount", 0))
        except Exception:
            await self.db.rollback()
            raise

    async def count_active_tokens(self, user_id: UUID | str) -> int:
        """Count total active (non-revoked, unexpired, non-deleted) refresh tokens for a user.

        Args:
            user_id: Owner User UUID or string representation.

        Returns:
            Total active token count for the specified user.
        """
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        now = datetime.now(timezone.utc)
        stmt = select(func.count(RefreshToken.id)).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > now,
            RefreshToken.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count if count is not None else 0
