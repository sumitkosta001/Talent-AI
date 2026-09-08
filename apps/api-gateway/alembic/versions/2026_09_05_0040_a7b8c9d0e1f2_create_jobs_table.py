"""Create jobs table with status and work_mode enums.

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-09-05 00:40:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a7b8c9d0e1f2'
down_revision: Union[str, None] = 'f6a7b8c9d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create job_status and work_mode enum types and jobs table."""
    # Create Native PostgreSQL Enums
    job_status_enum = postgresql.ENUM('draft', 'published', 'closed', name='job_status', create_type=False)
    job_status_enum.create(op.get_bind(), checkfirst=True)

    work_mode_enum = postgresql.ENUM('remote', 'hybrid', 'onsite', name='work_mode', create_type=False)
    work_mode_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False),
        sa.Column('recruiter_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('status', job_status_enum, nullable=False, server_default=sa.text("'draft'")),
        sa.Column('work_mode', work_mode_enum, nullable=False, server_default=sa.text("'remote'")),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('salary_min', sa.Integer(), nullable=True),
        sa.Column('salary_max', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default=sa.text("'USD'")),
        sa.Column('required_skills', sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column('preferred_skills', sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column('required_experience_months', sa.Integer(), nullable=True),
        sa.Column('education_requirements', sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column('required_keywords', sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.create_index('ix_jobs_company_id', 'jobs', ['company_id'], unique=False)
    op.create_index('ix_jobs_recruiter_id', 'jobs', ['recruiter_id'], unique=False)
    op.create_index('ix_jobs_title', 'jobs', ['title'], unique=False)
    op.create_index('ix_jobs_status', 'jobs', ['status'], unique=False)
    op.create_index('ix_jobs_work_mode', 'jobs', ['work_mode'], unique=False)
    op.create_index('ix_jobs_is_deleted', 'jobs', ['is_deleted'], unique=False)


def downgrade() -> None:
    """Drop jobs table and native PostgreSQL enums."""
    op.drop_index('ix_jobs_is_deleted', table_name='jobs')
    op.drop_index('ix_jobs_work_mode', table_name='jobs')
    op.drop_index('ix_jobs_status', table_name='jobs')
    op.drop_index('ix_jobs_title', table_name='jobs')
    op.drop_index('ix_jobs_recruiter_id', table_name='jobs')
    op.drop_index('ix_jobs_company_id', table_name='jobs')
    op.drop_table('jobs')

    sa.Enum(name='work_mode').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='job_status').drop(op.get_bind(), checkfirst=True)
