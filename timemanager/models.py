from __future__ import annotations

import sqlalchemy as sa


NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)

installations = sa.Table(
    "installations",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column("is_local", sa.Boolean, nullable=False, server_default=sa.false()),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
)

sa.Index(
    "installations_one_local",
    installations.c.is_local,
    unique=True,
    sqlite_where=installations.c.is_local.is_(True),
    postgresql_where=installations.c.is_local.is_(True),
)

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column(
        "origin_installation_id",
        sa.Integer,
        sa.ForeignKey("installations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sa.Column(
        "revision",
        sa.Integer,
        sa.CheckConstraint("revision >= 1", name="revision_positive"),
        nullable=False,
        server_default=sa.text("1"),
    ),
    sa.Column("display_name", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("password_hash", sa.String, nullable=False),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
)

remember_items = sa.Table(
    "remember_items",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column(
        "origin_installation_id",
        sa.Integer,
        sa.ForeignKey("installations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sa.Column(
        "revision",
        sa.Integer,
        sa.CheckConstraint("revision >= 1", name="revision_positive"),
        nullable=False,
        server_default=sa.text("1"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("title", sa.String, nullable=False),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.Column(
        "updated_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
)

tasks = sa.Table(
    "tasks",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column(
        "origin_installation_id",
        sa.Integer,
        sa.ForeignKey("installations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sa.Column(
        "revision",
        sa.Integer,
        sa.CheckConstraint("revision >= 1", name="revision_positive"),
        nullable=False,
        server_default=sa.text("1"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("title", sa.String, nullable=False),
    sa.Column("notes", sa.String, nullable=False, server_default=""),
    sa.Column("next_action", sa.String, nullable=False, server_default=""),
    sa.Column("definition_of_done", sa.String, nullable=False, server_default=""),
    sa.Column(
        "state",
        sa.String,
        sa.CheckConstraint(
            "state IN ('inbox', 'ready', 'active', 'done', 'dropped')",
            name="state_allowed",
        ),
        nullable=False,
        server_default="inbox",
    ),
    sa.Column("planned_date", sa.String),
    sa.Column(
        "is_highlight",
        sa.Boolean,
        nullable=False,
        server_default=sa.false(),
    ),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.Column(
        "updated_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.Column("completed_at", sa.String),
    sa.Column("dropped_at", sa.String),
    sa.Column(
        "project_id",
        sa.Integer,
        sa.ForeignKey("projects.id", ondelete="SET NULL"),
    ),
    sa.Column("project_position", sa.Integer),
    sa.Column(
        "workflow_status",
        sa.String,
        sa.CheckConstraint(
            "workflow_status IN ('inbox', 'open', 'waiting', 'done', 'dropped')",
            name="workflow_status_allowed",
        ),
        nullable=False,
        server_default="open",
    ),
    sa.Column(
        "today_placement",
        sa.String,
        sa.CheckConstraint(
            "today_placement IN ('unplanned', 'active', 'overflow')",
            name="today_placement_allowed",
        ),
        nullable=False,
        server_default="unplanned",
    ),
    sa.Column(
        "dependency_override",
        sa.Boolean,
        nullable=False,
        server_default=sa.false(),
    ),
)

sa.Index("tasks_user_state", tasks.c.user_id, tasks.c.state, tasks.c.planned_date)
sa.Index("tasks_user_dropped_at", tasks.c.user_id, tasks.c.dropped_at)
sa.Index(
    "tasks_one_active_highlight",
    tasks.c.user_id,
    tasks.c.planned_date,
    unique=True,
    sqlite_where=sa.and_(
        tasks.c.is_highlight.is_(True),
        tasks.c.state.not_in(("done", "dropped")),
    ),
    postgresql_where=sa.and_(
        tasks.c.is_highlight.is_(True),
        tasks.c.state.not_in(("done", "dropped")),
    ),
)

projects = sa.Table(
    "projects",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column(
        "origin_installation_id",
        sa.Integer,
        sa.ForeignKey("installations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sa.Column(
        "revision",
        sa.Integer,
        sa.CheckConstraint("revision >= 1", name="revision_positive"),
        nullable=False,
        server_default=sa.text("1"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("title", sa.String, nullable=False),
    sa.Column("desired_outcome", sa.String, nullable=False, server_default=""),
    sa.Column("notes", sa.String, nullable=False, server_default=""),
    sa.Column(
        "state",
        sa.String,
        sa.CheckConstraint(
            "state IN ('active', 'completed', 'dropped')",
            name="state_allowed",
        ),
        nullable=False,
        server_default="active",
    ),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.Column(
        "updated_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
)

task_components = sa.Table(
    "task_components",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column(
        "origin_installation_id",
        sa.Integer,
        sa.ForeignKey("installations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sa.Column(
        "revision",
        sa.Integer,
        sa.CheckConstraint("revision >= 1", name="revision_positive"),
        nullable=False,
        server_default=sa.text("1"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "task_id",
        sa.Integer,
        sa.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("title", sa.String, nullable=False),
    sa.Column("position", sa.Integer, nullable=False),
    sa.Column("is_done", sa.Boolean, nullable=False, server_default=sa.false()),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.Column(
        "updated_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.UniqueConstraint("task_id", "position"),
)

task_dependencies = sa.Table(
    "task_dependencies",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "task_id",
        sa.Integer,
        sa.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "prerequisite_task_id",
        sa.Integer,
        sa.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.CheckConstraint("task_id != prerequisite_task_id", name="not_self"),
    sa.UniqueConstraint(
        "task_id",
        "prerequisite_task_id",
        name="uq_task_dependencies_edge",
    ),
)

task_waits = sa.Table(
    "task_waits",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(36), nullable=False, unique=True),
    sa.Column(
        "origin_installation_id",
        sa.Integer,
        sa.ForeignKey("installations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sa.Column(
        "revision",
        sa.Integer,
        sa.CheckConstraint("revision >= 1", name="revision_positive"),
        nullable=False,
        server_default=sa.text("1"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "task_id",
        sa.Integer,
        sa.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    ),
    sa.Column("reason", sa.String, nullable=False),
    sa.Column("waiting_on", sa.String, nullable=False, server_default=""),
    sa.Column(
        "resume_status",
        sa.String,
        sa.CheckConstraint(
            "resume_status IN ('inbox', 'open')",
            name="resume_status_allowed",
        ),
        nullable=False,
        server_default="open",
    ),
    sa.Column("review_date", sa.String),
    sa.Column(
        "follow_up_task_id",
        sa.Integer,
        sa.ForeignKey("tasks.id", ondelete="SET NULL"),
    ),
    sa.Column(
        "created_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
    sa.Column(
        "updated_at",
        sa.String,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    ),
)

sa.Index("projects_user_state", projects.c.user_id, projects.c.state)
sa.Index(
    "remember_items_user_created",
    remember_items.c.user_id,
    remember_items.c.created_at,
)
sa.Index(
    "task_components_user_task",
    task_components.c.user_id,
    task_components.c.task_id,
)
sa.Index(
    "task_dependencies_user_task",
    task_dependencies.c.user_id,
    task_dependencies.c.task_id,
)
sa.Index(
    "tasks_user_workflow_today",
    tasks.c.user_id,
    tasks.c.workflow_status,
    tasks.c.planned_date,
    tasks.c.today_placement,
)
