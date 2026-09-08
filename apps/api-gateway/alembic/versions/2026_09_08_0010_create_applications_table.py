# alembic migration to create applications table
"""Create applications table for candidate job applications.

Revision ID: 2026_09_08_0010_create_applications_table
Revises: 2026_09_05_0040_a7b8c9d0e1f2_create_jobs_table
Create Date: 2026-09-08
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql

# revision identifiers, used by Alembic.
revision = "2026_09_08_0010_create_applications_table"
down_revision = "2026_09_05_0040_a7b8c9d0e1f2_create_jobs_table"
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type for application status
    op.execute("CREATE TYPE application_status AS ENUM ('applied','reviewed','interviewed','rejected','accepted')")
    op.create_table(
        "applications",
        sa.Column("id", psql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("job_id", psql.UUID(as_uuid=True), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("candidate_id", psql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=False, index=True),
        sa.Column(
            "status",
            psql.ENUM(
                "applied",
                "reviewed",
                "interviewed",
                "rejected",
                "accepted",
                name="application_status",
                create_constraint=False,
                native_enum=True,
            ),
            nullable=False,
            server_default=sa.text("'applied'"),
            index=True,
        ),
        sa.Column("resume_path", sa.String(512), nullable=True),
        sa.Column("cover_letter", sa.Text, nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("created_by", psql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", psql.UUID(as_uuid=True), nullable=True),
    )


def downgrade():
    op.drop_table("applications")
    op.execute("DROP TYPE IF EXISTS application_status")
