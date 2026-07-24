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
)

sa.Index("tasks_user_state", tasks.c.user_id, tasks.c.state, tasks.c.planned_date)
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
