"""create_candidate_profile_tables

Revision ID: a1b2c3d4e5f6
Revises: 89da7b85e15c
Create Date: 2026-08-09 16:00:00.000000+00:00

Creates candidate_profiles, candidate_education, candidate_experience, and candidate_skills tables
along with skillcategory and skillproficiency PostgreSQL ENUM types.
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '89da7b85e15c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create skillcategory and skillproficiency ENUM types if not present
    skillcategory_enum = postgresql.ENUM(
        'programming', 'framework', 'database', 'cloud', 'devops',
        'data_science', 'machine_learning', 'soft_skill', 'communication', 'other',
        name='skillcategory',
        create_type=False
    )
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE skillcategory AS ENUM (
                'programming', 'framework', 'database', 'cloud', 'devops',
                'data_science', 'machine_learning', 'soft_skill', 'communication', 'other'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    skillproficiency_enum = postgresql.ENUM(
        'beginner', 'intermediate', 'advanced', 'expert',
        name='skillproficiency',
        create_type=False
    )
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE skillproficiency AS ENUM (
                'beginner', 'intermediate', 'advanced', 'expert'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # 2. Create candidate_profiles table
    op.create_table(
        'candidate_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('location', sa.String(length=150), nullable=True),
        sa.Column('headline', sa.String(length=255), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('profile_picture_url', sa.String(length=1024), nullable=True),
        sa.Column('linkedin_url', sa.String(length=1024), nullable=True),
        sa.Column('github_url', sa.String(length=1024), nullable=True),
        sa.Column('portfolio_url', sa.String(length=1024), nullable=True),
        sa.Column('profile_completion_percentage', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_candidate_profiles_user_id')
    )
    op.create_index(op.f('ix_candidate_profiles_is_deleted'), 'candidate_profiles', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_candidate_profiles_user_id'), 'candidate_profiles', ['user_id'], unique=True)

    # 3. Create candidate_education table
    op.create_table(
        'candidate_education',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_profile_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('degree', sa.String(length=255), nullable=False),
        sa.Column('institution', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('grade_or_cgpa', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['candidate_profile_id'], ['candidate_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_education_candidate_profile_id'), 'candidate_education', ['candidate_profile_id'], unique=False)
    op.create_index(op.f('ix_candidate_education_is_deleted'), 'candidate_education', ['is_deleted'], unique=False)

    # 4. Create candidate_experience table
    op.create_table(
        'candidate_experience',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_profile_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=False),
        sa.Column('job_title', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['candidate_profile_id'], ['candidate_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_experience_candidate_profile_id'), 'candidate_experience', ['candidate_profile_id'], unique=False)
    op.create_index(op.f('ix_candidate_experience_is_deleted'), 'candidate_experience', ['is_deleted'], unique=False)

    # 5. Create candidate_skills table
    op.create_table(
        'candidate_skills',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_profile_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('skill_name', sa.String(length=100), nullable=False),
        sa.Column('normalized_skill_name', sa.String(length=100), nullable=False),
        sa.Column('category', skillcategory_enum, server_default='other', nullable=False),
        sa.Column('proficiency', skillproficiency_enum, server_default='intermediate', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['candidate_profile_id'], ['candidate_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_profile_id', 'normalized_skill_name', name='uq_candidate_skill_profile_normalized_name')
    )
    op.create_index(op.f('ix_candidate_skills_candidate_profile_id'), 'candidate_skills', ['candidate_profile_id'], unique=False)
    op.create_index(op.f('ix_candidate_skills_is_deleted'), 'candidate_skills', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_candidate_skills_normalized_skill_name'), 'candidate_skills', ['normalized_skill_name'], unique=False)


def downgrade() -> None:
    op.drop_table('candidate_skills')
    op.drop_table('candidate_experience')
    op.drop_table('candidate_education')
    op.drop_table('candidate_profiles')
    op.execute("DROP TYPE IF EXISTS skillproficiency")
    op.execute("DROP TYPE IF EXISTS skillcategory")
