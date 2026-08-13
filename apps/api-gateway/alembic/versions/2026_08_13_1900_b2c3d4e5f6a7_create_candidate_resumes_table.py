"""create_candidate_resumes_table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-13 19:00:00.000000+00:00

Creates the candidate_resumes table and resumestatus PostgreSQL ENUM type
for Phase 3 Day 11 — Resume Upload.
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create resumestatus ENUM type if not present
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE resumestatus AS ENUM (
                'uploaded', 'processing', 'processed', 'failed'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    resumestatus_enum = postgresql.ENUM(
        'uploaded', 'processing', 'processed', 'failed',
        name='resumestatus',
        create_type=False,
    )

    # 2. Create candidate_resumes table
    op.create_table(
        'candidate_resumes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_profile_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('original_filename', sa.String(length=500), nullable=False),
        sa.Column('stored_filename', sa.String(length=300), nullable=False),
        sa.Column('mime_type', sa.String(length=255), nullable=False),
        sa.Column('file_extension', sa.String(length=20), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('status', resumestatus_enum, server_default='uploaded', nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('is_current', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['candidate_profile_id'], ['candidate_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stored_filename', name='uq_candidate_resumes_stored_filename'),
    )

    # 3. Create indexes
    op.create_index(
        op.f('ix_candidate_resumes_candidate_profile_id'),
        'candidate_resumes',
        ['candidate_profile_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_candidate_resumes_is_deleted'),
        'candidate_resumes',
        ['is_deleted'],
        unique=False,
    )
    op.create_index(
        op.f('ix_candidate_resumes_is_current'),
        'candidate_resumes',
        ['is_current'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table('candidate_resumes')
    op.execute("DROP TYPE IF EXISTS resumestatus")
