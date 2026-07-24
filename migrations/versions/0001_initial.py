"""Create the original local users and tasks schema.

Revision ID: 0001
Revises:
Create Date: 2026-07-24
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.String(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("notes", sa.String(), server_default="", nullable=False),
        sa.Column("state", sa.String(), server_default="inbox", nullable=False),
        sa.Column("planned_date", sa.String(), nullable=True),
        sa.Column(
            "is_highlight",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.String(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.String(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.String(), nullable=True),
        sa.CheckConstraint(
            "state IN ('inbox', 'ready', 'active', 'done', 'dropped')",
            name="ck_tasks_state_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_tasks_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_tasks"),
    )
    op.create_index(
        "tasks_user_state",
        "tasks",
        ["user_id", "state", "planned_date"],
        unique=False,
    )
    op.create_index(
        "tasks_one_active_highlight",
        "tasks",
        ["user_id", "planned_date"],
        unique=True,
        sqlite_where=sa.text(
            "is_highlight = 1 AND state NOT IN ('done', 'dropped')"
        ),
        postgresql_where=sa.text(
            "is_highlight IS TRUE AND state NOT IN ('done', 'dropped')"
        ),
    )


def downgrade() -> None:
    op.drop_index("tasks_one_active_highlight", table_name="tasks")
    op.drop_index("tasks_user_state", table_name="tasks")
    op.drop_table("tasks")
    op.drop_table("users")
