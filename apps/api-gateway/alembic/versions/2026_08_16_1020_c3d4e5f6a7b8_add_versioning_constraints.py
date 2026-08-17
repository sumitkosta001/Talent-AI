"""add_versioning_constraints

Revision ID: c3d4e5f6a7b8
Revises: f989fec16afb
Create Date: 2026-08-16 10:20:00.000000+00:00

Adds versioning constraints for Day 16 — Resume Versioning:
1. Partial unique index on (candidate_profile_id, version) WHERE is_deleted = false
   to prevent duplicate active version numbers per candidate.
2. Check constraint ensuring version >= 1.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'f989fec16afb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply versioning constraints."""
    # 1. Partial unique index: no two active resumes for the same candidate
    #    can share a version number. Soft-deleted records are excluded.
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uix_candidate_resume_version_active
        ON candidate_resumes (candidate_profile_id, version)
        WHERE is_deleted = false
    """)

    # 2. Check constraint: version must be >= 1
    op.execute("""
        ALTER TABLE candidate_resumes
        ADD CONSTRAINT ck_candidate_resumes_version_positive
        CHECK (version >= 1)
    """)


def downgrade() -> None:
    """Reverse versioning constraints."""
    op.execute("ALTER TABLE candidate_resumes DROP CONSTRAINT IF EXISTS ck_candidate_resumes_version_positive")
    op.execute("DROP INDEX IF EXISTS uix_candidate_resume_version_active")
