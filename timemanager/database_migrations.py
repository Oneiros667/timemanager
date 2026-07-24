from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Connection, Engine


class UnsupportedSchemaError(RuntimeError):
    """Raised when an unversioned database cannot be safely identified."""


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALEMBIC_CONFIG_PATH = PROJECT_ROOT / "alembic.ini"
MIGRATIONS_PATH = PROJECT_ROOT / "migrations"
LEGACY_REVISION = "0001"

LEGACY_USER_COLUMNS = {
    "id": ("INTEGER", True, None, 1),
    "display_name": ("TEXT", False, None, 0),
    "email": ("TEXT", False, None, 0),
    "password_hash": ("TEXT", False, None, 0),
    "created_at": ("TEXT", False, "CURRENT_TIMESTAMP", 0),
}
LEGACY_TASK_COLUMNS = {
    "id": ("INTEGER", True, None, 1),
    "user_id": ("INTEGER", False, None, 0),
    "title": ("TEXT", False, None, 0),
    "notes": ("TEXT", False, "''", 0),
    "state": ("TEXT", False, "'inbox'", 0),
    "planned_date": ("TEXT", True, None, 0),
    "is_highlight": ("INTEGER", False, "0", 0),
    "created_at": ("TEXT", False, "CURRENT_TIMESTAMP", 0),
    "updated_at": ("TEXT", False, "CURRENT_TIMESTAMP", 0),
    "completed_at": ("TEXT", True, None, 0),
}


@dataclass(frozen=True)
class SQLiteRecovery:
    database_path: Path
    backup_path: Path | None
    remove_on_failure: bool


def migration_config(connection: Connection | None = None) -> Config:
    config = Config(str(ALEMBIC_CONFIG_PATH))
    config.set_main_option("script_location", str(MIGRATIONS_PATH))
    if connection is not None:
        config.attributes["connection"] = connection
    return config


def upgrade_database(engine: Engine, revision: str = "head") -> None:
    recovery = _prepare_sqlite_recovery(engine, revision)
    try:
        with engine.begin() as connection:
            _stamp_supported_legacy_database(connection)
            command.upgrade(migration_config(connection), revision)
    except Exception:
        if recovery is not None:
            _restore_sqlite_database(engine, recovery)
        raise


def current_revision(engine: Engine) -> str | None:
    with engine.connect() as connection:
        return MigrationContext.configure(connection).get_current_revision()


def head_revision() -> str:
    return ScriptDirectory.from_config(migration_config()).get_current_head()


def _prepare_sqlite_recovery(
    engine: Engine,
    revision: str,
) -> SQLiteRecovery | None:
    if (
        engine.dialect.name != "sqlite"
        or not engine.url.database
        or engine.url.database == ":memory:"
    ):
        return None

    database_path = Path(engine.url.database)
    existed_before_connect = database_path.exists()
    with engine.connect() as connection:
        tables = set(sa.inspect(connection).get_table_names())
        current = MigrationContext.configure(connection).get_current_revision()

    target = head_revision() if revision == "head" else revision
    if current == target:
        return None

    if not existed_before_connect or not tables:
        return SQLiteRecovery(database_path, None, remove_on_failure=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    current_label = current or "unversioned"
    backup_path = database_path.with_name(
        f"{database_path.name}.pre-migration-{current_label}-{timestamp}.bak"
    )
    with (
        sqlite3.connect(database_path) as source,
        sqlite3.connect(backup_path) as destination,
    ):
        source.backup(destination)

    return SQLiteRecovery(database_path, backup_path, remove_on_failure=False)


def _restore_sqlite_database(engine: Engine, recovery: SQLiteRecovery) -> None:
    engine.dispose()
    _remove_sqlite_sidecars(recovery.database_path)
    if recovery.remove_on_failure:
        recovery.database_path.unlink(missing_ok=True)
        return

    if recovery.backup_path is None:
        raise RuntimeError("SQLite recovery metadata has no backup path.")
    with (
        sqlite3.connect(recovery.backup_path) as source,
        sqlite3.connect(recovery.database_path) as destination,
    ):
        source.backup(destination)


def _remove_sqlite_sidecars(database_path: Path) -> None:
    database_path.with_name(f"{database_path.name}-wal").unlink(missing_ok=True)
    database_path.with_name(f"{database_path.name}-shm").unlink(missing_ok=True)


def _stamp_supported_legacy_database(connection: Connection) -> None:
    inspector = sa.inspect(connection)
    tables = set(inspector.get_table_names())
    if not tables:
        return

    if "alembic_version" in tables:
        revision = MigrationContext.configure(connection).get_current_revision()
        if revision is not None:
            return
        tables.remove("alembic_version")

    if connection.dialect.name != "sqlite" or tables != {"users", "tasks"}:
        raise UnsupportedSchemaError(
            "Database has no Alembic history and does not match the supported "
            "legacy SQLite schema."
        )

    user_columns = _column_signatures(inspector.get_columns("users"))
    task_columns = _column_signatures(inspector.get_columns("tasks"))
    user_uniques = {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints("users")
    }
    task_checks = {
        " ".join(constraint["sqltext"].split())
        for constraint in inspector.get_check_constraints("tasks")
    }
    task_indexes = {
        index["name"]: (
            tuple(index["column_names"]),
            bool(index["unique"]),
            " ".join(
                str(index.get("dialect_options", {}).get("sqlite_where", "")).split()
            ),
        )
        for index in inspector.get_indexes("tasks")
    }
    task_foreign_keys = inspector.get_foreign_keys("tasks")

    if (
        user_columns != LEGACY_USER_COLUMNS
        or task_columns != LEGACY_TASK_COLUMNS
        or inspector.get_pk_constraint("users")["constrained_columns"] != ["id"]
        or inspector.get_pk_constraint("tasks")["constrained_columns"] != ["id"]
        or user_uniques != {("email",)}
        or task_checks
        != {
            "state IN ('inbox', 'ready', 'active', 'done', 'dropped')",
            "is_highlight IN (0, 1)",
        }
        or task_indexes
        != {
            "tasks_user_state": (
                ("user_id", "state", "planned_date"),
                False,
                "",
            ),
            "tasks_one_active_highlight": (
                ("user_id", "planned_date"),
                True,
                "is_highlight = 1 AND state NOT IN ('done', 'dropped')",
            ),
        }
        or len(task_foreign_keys) != 1
        or task_foreign_keys[0]["constrained_columns"] != ["user_id"]
        or task_foreign_keys[0]["referred_table"] != "users"
        or task_foreign_keys[0]["referred_columns"] != ["id"]
        or task_foreign_keys[0]["options"].get("ondelete") != "CASCADE"
    ):
        raise UnsupportedSchemaError(
            "Database has no Alembic history and does not match schema revision "
            f"{LEGACY_REVISION}."
        )

    command.stamp(migration_config(connection), LEGACY_REVISION)


def _column_signatures(columns: list[dict]) -> dict[str, tuple]:
    return {
        column["name"]: (
            type(column["type"]).__name__.upper(),
            bool(column["nullable"]),
            column["default"],
            int(column["primary_key"]),
        )
        for column in columns
    }
