"""Create companies table.

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-09-04 21:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e5f6a7b8c9d0'
down_revision: Union[str, None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create companies table with all required columns and indexes."""
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=1024), nullable=True),
        sa.Column('logo_url', sa.String(length=1024), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('industry', sa.String(length=255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index('ix_companies_name', 'companies', ['name'], unique=False)
    op.create_index('ix_companies_is_deleted', 'companies', ['is_deleted'], unique=False)


def downgrade() -> None:
    """Drop companies table."""
    op.drop_index('ix_companies_is_deleted', table_name='companies')
    op.drop_index('ix_companies_name', table_name='companies')
    op.drop_table('companies')
