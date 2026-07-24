"""Separate the active Today plan from recoverable overflow.

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-24
"""

from typing import Sequence

from alembic import op


revision: str = "0003"
down_revision: str | Sequence[str] | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE tasks
        SET state = 'ready'
        WHERE state = 'active'
          AND planned_date IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE tasks
        SET state = 'active'
        WHERE state = 'ready'
          AND planned_date IS NOT NULL
          AND is_highlight = TRUE
        """
    )
    op.execute(
        """
        WITH ranked_options AS (
            SELECT
                id,
                ROW_NUMBER() OVER (
                    PARTITION BY user_id, planned_date
                    ORDER BY created_at, id
                ) AS option_position
            FROM tasks
            WHERE state = 'ready'
              AND planned_date IS NOT NULL
              AND is_highlight = FALSE
        )
        UPDATE tasks
        SET state = 'active'
        WHERE id IN (
            SELECT id
            FROM ranked_options
            WHERE option_position <= 3
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE tasks
        SET state = 'ready'
        WHERE state = 'active'
        """
    )
