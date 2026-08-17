"""Add processing status timestamps and failure reason fields to candidate_resumes table.

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-08-17 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add processing_started_at, processing_completed_at, and failure_reason columns."""
    op.add_column(
        'candidate_resumes',
        sa.Column(
            'processing_started_at',
            sa.DateTime(timezone=True),
            nullable=True,
            comment='UTC timestamp when resume processing/parsing started.'
        )
    )
    op.add_column(
        'candidate_resumes',
        sa.Column(
            'processing_completed_at',
            sa.DateTime(timezone=True),
            nullable=True,
            comment='UTC timestamp when resume processing/parsing completed.'
        )
    )
    op.add_column(
        'candidate_resumes',
        sa.Column(
            'failure_reason',
            sa.String(length=1000),
            nullable=True,
            comment='Safe human-readable failure reason message if processing failed.'
        )
    )


def downgrade() -> None:
    """Remove processing lifecycle columns from candidate_resumes."""
    op.drop_column('candidate_resumes', 'failure_reason')
    op.drop_column('candidate_resumes', 'processing_completed_at')
    op.drop_column('candidate_resumes', 'processing_started_at')
