"""Add short-term Remember items.

Revision ID: 0006
Revises: 0005
Create Date: 2026-07-28
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0006"
down_revision: str | Sequence[str] | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "remember_items",
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
        sa.Column("title", sa.String(), nullable=False),
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
            name="ck_remember_items_revision_positive",
        ),
        sa.ForeignKeyConstraint(
            ["origin_installation_id"],
            ["installations.id"],
            name="fk_remember_items_origin_installation_id_installations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_remember_items_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_remember_items"),
        sa.UniqueConstraint("public_id", name="uq_remember_items_public_id"),
    )
    op.create_index(
        "remember_items_user_created",
        "remember_items",
        ["user_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "remember_items_user_created",
        table_name="remember_items",
    )
    op.drop_table("remember_items")
