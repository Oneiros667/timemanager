"""Add task clarity fields and ordered components.

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-28
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0004"
down_revision: str | Sequence[str] | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(
            sa.Column("next_action", sa.String(), server_default="", nullable=False)
        )
        batch_op.add_column(
            sa.Column(
                "definition_of_done",
                sa.String(),
                server_default="",
                nullable=False,
            )
        )

    op.create_table(
        "task_components",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=36), nullable=False),
        sa.Column("origin_installation_id", sa.Integer(), nullable=False),
        sa.Column(
            "revision",
            sa.Integer(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column(
            "is_done",
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
        sa.CheckConstraint(
            "revision >= 1",
            name="ck_task_components_revision_positive",
        ),
        sa.CheckConstraint(
            "position >= 0",
            name="ck_task_components_position_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["origin_installation_id"],
            ["installations.id"],
            name="fk_task_components_origin_installation_id_installations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name="fk_task_components_task_id_tasks",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_task_components_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_task_components"),
        sa.UniqueConstraint("public_id", name="uq_task_components_public_id"),
        sa.UniqueConstraint(
            "task_id",
            "position",
            name="uq_task_components_task_id_position",
        ),
    )
    op.create_index(
        "task_components_user_task",
        "task_components",
        ["user_id", "task_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("task_components_user_task", table_name="task_components")
    op.drop_table("task_components")
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_column("definition_of_done")
        batch_op.drop_column("next_action")
