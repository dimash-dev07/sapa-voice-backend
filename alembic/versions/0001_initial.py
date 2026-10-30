"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("ADMIN", "USER", name="user_role"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "voice_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("client_phone", sa.String(32), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("response", sa.Text()),
        sa.Column(
            "status",
            sa.Enum("PENDING", "PROCESSING", "PROCESSED", "FAILED", name="request_status"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_voice_requests_client_phone", "voice_requests", ["client_phone"])
    op.create_index(
        "ix_voice_requests_status_created", "voice_requests", ["status", "created_at"]
    )

    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(32), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("company", sa.String(255)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_clients_phone", "clients", ["phone"])
    op.create_index("ix_clients_email", "clients", ["email"])
    op.create_index("ix_clients_name_phone", "clients", ["full_name", "phone"])


def downgrade() -> None:
    op.drop_table("clients")
    op.drop_table("voice_requests")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS request_status")
    op.execute("DROP TYPE IF EXISTS user_role")