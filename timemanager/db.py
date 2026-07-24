from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
from sqlalchemy import URL, Engine, create_engine, event, select
from sqlalchemy.engine import Connection

from .database_migrations import (
    current_revision,
    head_revision,
    upgrade_database,
)
from .models import installations


def get_engine() -> Engine:
    return current_app.extensions["timemanager_engine"]


def get_db() -> Connection:
    if "db" not in g:
        g.db = get_engine().connect()

    return g.db


def close_db(_error=None) -> None:
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db() -> None:
    upgrade_database(get_engine())


def new_public_id() -> str:
    return str(uuid4())


def local_installation_id(database: Connection | None = None) -> int:
    connection = database or get_db()
    installation_id = connection.execute(
        select(installations.c.id).where(installations.c.is_local.is_(True))
    ).scalar_one_or_none()
    if installation_id is None:
        raise RuntimeError("The local installation provenance record is missing.")
    return int(installation_id)


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    init_db()
    click.echo(f"Database schema is at revision {head_revision()}.")


@click.command("schema-version")
@with_appcontext
def schema_version_command() -> None:
    revision = current_revision(get_engine()) or "unversioned"
    click.echo(f"{revision} (latest: {head_revision()})")


def _database_url(app: Flask) -> str | URL:
    configured_url = app.config.get("DATABASE_URL")
    if configured_url:
        return str(configured_url)

    database_path = Path(app.config["DATABASE"]).resolve()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return URL.create("sqlite+pysqlite", database=str(database_path))


def _create_engine(app: Flask) -> Engine:
    engine = create_engine(_database_url(app))
    if engine.dialect.name == "sqlite":

        @event.listens_for(engine, "connect")
        def enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.close()

    return engine


def init_app(app: Flask) -> None:
    app.extensions["timemanager_engine"] = _create_engine(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(schema_version_command)
