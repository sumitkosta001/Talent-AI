"""Add company_id foreign key column to users table.

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-09-04 21:51:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f6a7b8c9d0e1'
down_revision: Union[str, None] = 'e5f6a7b8c9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add company_id column and foreign key constraint to users table."""
    op.add_column(
        'users',
        sa.Column(
            'company_id',
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('companies.id', ondelete='SET NULL'),
            nullable=True,
            comment='Foreign key referencing companies.id for recruiter/hiring manager affiliation.'
        )
    )
    op.create_index('ix_users_company_id', 'users', ['company_id'], unique=False)


def downgrade() -> None:
    """Remove company_id column and index from users table."""
    op.drop_index('ix_users_company_id', table_name='users')
    op.drop_column('users', 'company_id')
