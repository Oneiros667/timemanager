"""Add projects, dependencies, waiting, and separated task state.

Revision ID: 0005
Revises: 0004
Create Date: 2026-07-28
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0005"
down_revision: str | Sequence[str] | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "projects",
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
        sa.Column("desired_outcome", sa.String(), server_default="", nullable=False),
        sa.Column("notes", sa.String(), server_default="", nullable=False),
        sa.Column("state", sa.String(), server_default="active", nullable=False),
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
        sa.CheckConstraint("revision >= 1", name="ck_projects_revision_positive"),
        sa.CheckConstraint(
            "state IN ('active', 'completed', 'dropped')",
            name="ck_projects_state_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["origin_installation_id"],
            ["installations.id"],
            name="fk_projects_origin_installation_id_installations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_projects_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_projects"),
        sa.UniqueConstraint("public_id", name="uq_projects_public_id"),
    )
    op.create_index("projects_user_state", "projects", ["user_id", "state"])

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("project_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("project_position", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "workflow_status",
                sa.String(),
                server_default="open",
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "today_placement",
                sa.String(),
                server_default="unplanned",
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "dependency_override",
                sa.Boolean(),
                server_default=sa.false(),
                nullable=False,
            )
        )
        batch_op.create_check_constraint(
            "ck_tasks_workflow_status_allowed",
            "workflow_status IN ('inbox', 'open', 'waiting', 'done', 'dropped')",
        )
        batch_op.create_check_constraint(
            "ck_tasks_today_placement_allowed",
            "today_placement IN ('unplanned', 'active', 'overflow')",
        )
        batch_op.create_check_constraint(
            "ck_tasks_project_position_nonnegative",
            "project_position IS NULL OR project_position >= 0",
        )
        batch_op.create_foreign_key(
            "fk_tasks_project_id_projects",
            "projects",
            ["project_id"],
            ["id"],
            ondelete="SET NULL",
        )

    op.execute(
        """
        UPDATE tasks
        SET workflow_status = CASE state
                WHEN 'inbox' THEN 'inbox'
                WHEN 'done' THEN 'done'
                WHEN 'dropped' THEN 'dropped'
                ELSE 'open'
            END,
            today_placement = CASE state
                WHEN 'active' THEN 'active'
                WHEN 'ready' THEN 'overflow'
                ELSE 'unplanned'
            END
        """
    )
    op.create_index(
        "tasks_user_workflow_today",
        "tasks",
        ["user_id", "workflow_status", "planned_date", "today_placement"],
    )

    op.create_table(
        "task_dependencies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("prerequisite_task_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.String(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "task_id != prerequisite_task_id",
            name="ck_task_dependencies_not_self",
        ),
        sa.ForeignKeyConstraint(
            ["prerequisite_task_id"],
            ["tasks.id"],
            name="fk_task_dependencies_prerequisite_task_id_tasks",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name="fk_task_dependencies_task_id_tasks",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_task_dependencies_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_task_dependencies"),
        sa.UniqueConstraint(
            "task_id",
            "prerequisite_task_id",
            name="uq_task_dependencies_edge",
        ),
    )
    op.create_index(
        "task_dependencies_user_task",
        "task_dependencies",
        ["user_id", "task_id"],
    )

    op.create_table(
        "task_waits",
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
        sa.Column("reason", sa.String(), nullable=False),
        sa.Column("waiting_on", sa.String(), server_default="", nullable=False),
        sa.Column("resume_status", sa.String(), server_default="open", nullable=False),
        sa.Column("review_date", sa.String(), nullable=True),
        sa.Column("follow_up_task_id", sa.Integer(), nullable=True),
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
        sa.CheckConstraint("revision >= 1", name="ck_task_waits_revision_positive"),
        sa.CheckConstraint(
            "resume_status IN ('inbox', 'open')",
            name="ck_task_waits_resume_status_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["follow_up_task_id"],
            ["tasks.id"],
            name="fk_task_waits_follow_up_task_id_tasks",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["origin_installation_id"],
            ["installations.id"],
            name="fk_task_waits_origin_installation_id_installations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name="fk_task_waits_task_id_tasks",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_task_waits_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_task_waits"),
        sa.UniqueConstraint("public_id", name="uq_task_waits_public_id"),
        sa.UniqueConstraint("task_id", name="uq_task_waits_task_id"),
    )


def downgrade() -> None:
    op.drop_table("task_waits")
    op.drop_index("task_dependencies_user_task", table_name="task_dependencies")
    op.drop_table("task_dependencies")
    op.drop_index("tasks_user_workflow_today", table_name="tasks")
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint("fk_tasks_project_id_projects", type_="foreignkey")
        batch_op.drop_constraint(
            "ck_tasks_project_position_nonnegative",
            type_="check",
        )
        batch_op.drop_constraint("ck_tasks_today_placement_allowed", type_="check")
        batch_op.drop_constraint("ck_tasks_workflow_status_allowed", type_="check")
        batch_op.drop_column("dependency_override")
        batch_op.drop_column("today_placement")
        batch_op.drop_column("workflow_status")
        batch_op.drop_column("project_position")
        batch_op.drop_column("project_id")
    op.drop_index("projects_user_state", table_name="projects")
    op.drop_table("projects")
