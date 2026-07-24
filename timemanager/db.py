from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(_error=None) -> None:
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db() -> None:
    database = get_db()
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    database.executescript(schema)
    database.commit()


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Initialized the Timemanager database.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
