"""Add installation provenance and stable public identifiers.

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-24
"""

from typing import Sequence
from uuid import uuid4

import sqlalchemy as sa
from alembic import op


revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "installations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=36), nullable=False),
        sa.Column(
            "is_local",
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
        sa.PrimaryKeyConstraint("id", name="pk_installations"),
        sa.UniqueConstraint("public_id", name="uq_installations_public_id"),
    )
    op.create_index(
        "installations_one_local",
        "installations",
        ["is_local"],
        unique=True,
        sqlite_where=sa.text("is_local = 1"),
        postgresql_where=sa.text("is_local IS TRUE"),
    )

    connection = op.get_bind()
    installation_id = connection.execute(
        sa.text(
            """
            INSERT INTO installations (public_id, is_local)
            VALUES (:public_id, :is_local)
            RETURNING id
            """
        ),
        {"public_id": str(uuid4()), "is_local": True},
    ).scalar_one()

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("public_id", sa.String(length=36)))
        batch_op.add_column(sa.Column("origin_installation_id", sa.Integer()))
        batch_op.add_column(
            sa.Column(
                "revision",
                sa.Integer(),
                server_default=sa.text("1"),
                nullable=False,
            )
        )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("public_id", sa.String(length=36)))
        batch_op.add_column(sa.Column("origin_installation_id", sa.Integer()))
        batch_op.add_column(
            sa.Column(
                "revision",
                sa.Integer(),
                server_default=sa.text("1"),
                nullable=False,
            )
        )

    for user_id in connection.execute(sa.text("SELECT id FROM users")).scalars():
        connection.execute(
            sa.text(
                """
                UPDATE users
                SET public_id = :public_id,
                    origin_installation_id = :installation_id
                WHERE id = :user_id
                """
            ),
            {
                "public_id": str(uuid4()),
                "installation_id": installation_id,
                "user_id": user_id,
            },
        )

    for task_id in connection.execute(sa.text("SELECT id FROM tasks")).scalars():
        connection.execute(
            sa.text(
                """
                UPDATE tasks
                SET public_id = :public_id,
                    origin_installation_id = :installation_id
                WHERE id = :task_id
                """
            ),
            {
                "public_id": str(uuid4()),
                "installation_id": installation_id,
                "task_id": task_id,
            },
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("public_id", existing_type=sa.String(36), nullable=False)
        batch_op.alter_column(
            "origin_installation_id",
            existing_type=sa.Integer(),
            nullable=False,
        )
        batch_op.create_unique_constraint("uq_users_public_id", ["public_id"])
        batch_op.create_check_constraint("ck_users_revision_positive", "revision >= 1")
        batch_op.create_foreign_key(
            "fk_users_origin_installation_id_installations",
            "installations",
            ["origin_installation_id"],
            ["id"],
            ondelete="RESTRICT",
        )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.alter_column("public_id", existing_type=sa.String(36), nullable=False)
        batch_op.alter_column(
            "origin_installation_id",
            existing_type=sa.Integer(),
            nullable=False,
        )
        batch_op.create_unique_constraint("uq_tasks_public_id", ["public_id"])
        batch_op.create_check_constraint("ck_tasks_revision_positive", "revision >= 1")
        batch_op.create_foreign_key(
            "fk_tasks_origin_installation_id_installations",
            "installations",
            ["origin_installation_id"],
            ["id"],
            ondelete="RESTRICT",
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint(
            "fk_tasks_origin_installation_id_installations",
            type_="foreignkey",
        )
        batch_op.drop_constraint("ck_tasks_revision_positive", type_="check")
        batch_op.drop_constraint("uq_tasks_public_id", type_="unique")
        batch_op.drop_column("revision")
        batch_op.drop_column("origin_installation_id")
        batch_op.drop_column("public_id")

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint(
            "fk_users_origin_installation_id_installations",
            type_="foreignkey",
        )
        batch_op.drop_constraint("ck_users_revision_positive", type_="check")
        batch_op.drop_constraint("uq_users_public_id", type_="unique")
        batch_op.drop_column("revision")
        batch_op.drop_column("origin_installation_id")
        batch_op.drop_column("public_id")

    op.drop_index("installations_one_local", table_name="installations")
    op.drop_table("installations")
