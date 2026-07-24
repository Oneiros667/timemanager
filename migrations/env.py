from __future__ import annotations

import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import URL, engine_from_config, pool

from timemanager.models import metadata


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

configured_url = os.environ.get("TIMEMANAGER_DATABASE_URL")
if configured_url:
    config.set_main_option("sqlalchemy.url", configured_url.replace("%", "%%"))
elif configured_path := os.environ.get("TIMEMANAGER_DATABASE"):
    database_url = URL.create(
        "sqlite+pysqlite",
        database=str(Path(configured_path).resolve()),
    )
    config.set_main_option(
        "sqlalchemy.url",
        database_url.render_as_string(hide_password=False).replace("%", "%%"),
    )

target_metadata = metadata


def configure_context(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=connection.dialect.name == "sqlite",
    )


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    supplied_connection = config.attributes.get("connection")
    if supplied_connection is not None:
        configure_context(supplied_connection)
        with context.begin_transaction():
            context.run_migrations()
        return

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        configure_context(connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
