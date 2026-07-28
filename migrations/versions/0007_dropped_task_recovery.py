"""Add dropped-task recovery timestamps.

Revision ID: 0007
Revises: 0006
Create Date: 2026-07-28
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0007"
down_revision: str | Sequence[str] | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("dropped_at", sa.String(), nullable=True))

    op.execute(
        """
        UPDATE tasks
        SET dropped_at = updated_at
        WHERE workflow_status = 'dropped'
          AND dropped_at IS NULL
        """
    )
    op.create_index(
        "tasks_user_dropped_at",
        "tasks",
        ["user_id", "dropped_at"],
    )


def downgrade() -> None:
    op.drop_index("tasks_user_dropped_at", table_name="tasks")
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_column("dropped_at")
