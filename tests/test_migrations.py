from __future__ import annotations

import sqlite3
from pathlib import Path
from uuid import UUID

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.util.exc import CommandError

from timemanager import database_migrations
from timemanager.database_migrations import (
    UnsupportedSchemaError,
    current_revision,
    head_revision,
    upgrade_database,
)
from timemanager.models import installations, tasks, users


SCHEMA_V1 = Path(__file__).with_name("fixtures") / "schema_v1.sql"


def _engine(path: Path) -> sa.Engine:
    return sa.create_engine(
        sa.URL.create("sqlite+pysqlite", database=str(path.resolve()))
    )


def test_fresh_database_upgrades_to_head_and_is_idempotent(tmp_path):
    engine = _engine(tmp_path / "fresh.sqlite3")

    upgrade_database(engine)
    assert current_revision(engine) == head_revision() == "0003"

    with engine.connect() as connection:
        installation = connection.execute(sa.select(installations)).mappings().one()
        original_public_id = installation["public_id"]
        assert installation["is_local"] is True
        UUID(original_public_id)

    upgrade_database(engine)
    with engine.connect() as connection:
        assert (
            connection.execute(sa.select(installations.c.public_id)).scalar_one()
            == original_public_id
        )


def test_exact_legacy_database_is_stamped_upgraded_and_preserved(tmp_path):
    database_path = tmp_path / "legacy.sqlite3"
    legacy = sqlite3.connect(database_path)
    legacy.executescript(SCHEMA_V1.read_text(encoding="utf-8"))
    legacy.execute(
        """
        INSERT INTO users (
            id, display_name, email, password_hash, created_at
        )
        VALUES (7, 'Alex', 'alex@example.com', 'preserved-hash',
                '2026-07-20 08:00:00')
        """
    )
    legacy.execute(
        """
        INSERT INTO tasks (
            id, user_id, title, notes, state, planned_date, is_highlight,
            created_at, updated_at, completed_at
        )
        VALUES (
            11, 7, 'Preserve this task', 'Original note', 'done',
            '2026-07-20', 0, '2026-07-20 08:10:00',
            '2026-07-20 09:00:00', '2026-07-20T09:00:00'
        )
        """
    )
    legacy.commit()
    legacy.close()

    engine = _engine(database_path)
    upgrade_database(engine)

    assert current_revision(engine) == "0003"
    backups = list(tmp_path.glob("legacy.sqlite3.pre-migration-unversioned-*.bak"))
    assert len(backups) == 1
    backup = sqlite3.connect(backups[0])
    assert backup.execute("SELECT password_hash FROM users").fetchone()[0] == (
        "preserved-hash"
    )
    assert backup.execute(
        "SELECT 1 FROM sqlite_master WHERE name = 'alembic_version'"
    ).fetchone() is None
    backup.close()

    with engine.connect() as connection:
        installation = connection.execute(sa.select(installations)).mappings().one()
        user = connection.execute(sa.select(users)).mappings().one()
        task = connection.execute(sa.select(tasks)).mappings().one()

    UUID(installation["public_id"])
    UUID(user["public_id"])
    UUID(task["public_id"])
    assert user["id"] == 7
    assert user["password_hash"] == "preserved-hash"
    assert user["created_at"] == "2026-07-20 08:00:00"
    assert user["origin_installation_id"] == installation["id"]
    assert user["revision"] == 1
    assert task["id"] == 11
    assert task["user_id"] == 7
    assert task["title"] == "Preserve this task"
    assert task["notes"] == "Original note"
    assert task["state"] == "done"
    assert task["planned_date"] == "2026-07-20"
    assert task["completed_at"] == "2026-07-20T09:00:00"
    assert task["origin_installation_id"] == installation["id"]
    assert task["revision"] == 1

    public_ids = {
        "installation": installation["public_id"],
        "user": user["public_id"],
        "task": task["public_id"],
    }
    upgrade_database(engine)
    with engine.connect() as connection:
        assert connection.execute(
            sa.select(installations.c.public_id)
        ).scalar_one() == public_ids["installation"]
        assert (
            connection.execute(sa.select(users.c.public_id)).scalar_one()
            == public_ids["user"]
        )
        assert (
            connection.execute(sa.select(tasks.c.public_id)).scalar_one()
            == public_ids["task"]
        )


def test_exact_legacy_database_with_empty_version_table_is_upgraded(tmp_path):
    database_path = tmp_path / "empty-version.sqlite3"
    legacy = sqlite3.connect(database_path)
    legacy.executescript(SCHEMA_V1.read_text(encoding="utf-8"))
    legacy.execute(
        "CREATE TABLE alembic_version "
        "(version_num VARCHAR(32) NOT NULL PRIMARY KEY)"
    )
    legacy.close()
    engine = _engine(database_path)

    upgrade_database(engine)

    assert current_revision(engine) == head_revision()
    assert sa.inspect(engine).has_table("installations")


def test_revision_0003_limits_existing_active_today_options(tmp_path):
    engine = _engine(tmp_path / "small-today.sqlite3")
    upgrade_database(engine, "0002")
    today = "2026-07-24"
    with engine.begin() as connection:
        installation_id = connection.execute(
            sa.select(installations.c.id)
        ).scalar_one()
        user_id = connection.execute(
            sa.insert(users)
            .values(
                public_id="11111111-1111-4111-8111-111111111111",
                origin_installation_id=installation_id,
                display_name="Alex",
                email="alex@example.com",
                password_hash="hash",
            )
            .returning(users.c.id)
        ).scalar_one()
        connection.execute(
            sa.insert(tasks),
            [
                {
                    "public_id": f"22222222-2222-4222-8222-{index:012d}",
                    "origin_installation_id": installation_id,
                    "user_id": user_id,
                    "title": f"Task {index}",
                    "state": "active" if index == 5 else "ready",
                    "planned_date": today,
                    "is_highlight": index == 1,
                }
                for index in range(1, 6)
            ],
        )

    upgrade_database(engine)

    with engine.connect() as connection:
        rows = (
            connection.execute(
                sa.select(tasks.c.title, tasks.c.state, tasks.c.is_highlight).order_by(
                    tasks.c.id
                )
            )
            .mappings()
            .all()
        )
    assert rows[0]["state"] == "active"
    assert rows[0]["is_highlight"] is True
    assert [row["state"] for row in rows[1:]] == [
        "active",
        "active",
        "active",
        "ready",
    ]


def test_unrecognized_unversioned_database_fails_closed(tmp_path):
    engine = _engine(tmp_path / "unknown.sqlite3")
    with engine.begin() as connection:
        connection.execute(sa.text("CREATE TABLE unexpected (id INTEGER PRIMARY KEY)"))

    with pytest.raises(UnsupportedSchemaError, match="does not match"):
        upgrade_database(engine)

    assert not sa.inspect(engine).has_table("alembic_version")


def test_legacy_lookalike_with_different_constraints_fails_closed(tmp_path):
    database_path = tmp_path / "lookalike.sqlite3"
    schema = SCHEMA_V1.read_text(encoding="utf-8").replace(
        "FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE",
        "FOREIGN KEY (user_id) REFERENCES users (id)",
    )
    legacy = sqlite3.connect(database_path)
    legacy.executescript(schema)
    legacy.close()
    engine = _engine(database_path)

    with pytest.raises(UnsupportedSchemaError, match="does not match"):
        upgrade_database(engine)

    assert not sa.inspect(engine).has_table("alembic_version")


def test_database_from_newer_unknown_revision_is_rejected(tmp_path):
    engine = _engine(tmp_path / "newer.sqlite3")
    upgrade_database(engine)
    with engine.begin() as connection:
        connection.execute(
            sa.text("UPDATE alembic_version SET version_num = '9999'")
        )

    with pytest.raises(CommandError, match="Can't locate revision"):
        upgrade_database(engine)


def test_failed_programmatic_upgrade_rolls_back_its_transaction(
    tmp_path,
    monkeypatch,
):
    engine = _engine(tmp_path / "failed.sqlite3")

    def fail_after_ddl(config, _revision):
        connection = config.attributes["connection"]
        connection.execute(
            sa.text("CREATE TABLE migration_probe (id INTEGER PRIMARY KEY)")
        )
        raise RuntimeError("simulated migration failure")

    monkeypatch.setattr(database_migrations.command, "upgrade", fail_after_ddl)

    with pytest.raises(RuntimeError, match="simulated migration failure"):
        upgrade_database(engine)

    assert not sa.inspect(engine).has_table("migration_probe")


def test_in_memory_database_upgrades_without_file_recovery():
    engine = sa.create_engine("sqlite+pysqlite:///:memory:")

    upgrade_database(engine)

    assert current_revision(engine) == head_revision()


def test_failed_legacy_upgrade_restores_the_pre_migration_snapshot(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "restore.sqlite3"
    legacy = sqlite3.connect(database_path)
    legacy.executescript(SCHEMA_V1.read_text(encoding="utf-8"))
    legacy.execute(
        """
        INSERT INTO users (display_name, email, password_hash)
        VALUES ('Alex', 'alex@example.com', 'original-hash')
        """
    )
    legacy.commit()
    legacy.close()
    engine = _engine(database_path)

    def fail_after_ddl(config, _revision):
        connection = config.attributes["connection"]
        connection.execute(
            sa.text("CREATE TABLE migration_probe (id INTEGER PRIMARY KEY)")
        )
        connection.execute(
            sa.text("UPDATE users SET password_hash = 'changed-during-migration'")
        )
        raise RuntimeError("simulated migration failure")

    monkeypatch.setattr(database_migrations.command, "upgrade", fail_after_ddl)

    with pytest.raises(RuntimeError, match="simulated migration failure"):
        upgrade_database(engine)

    inspector = sa.inspect(engine)
    assert set(inspector.get_table_names()) == {"tasks", "users"}
    with engine.connect() as connection:
        assert connection.execute(
            sa.text("SELECT password_hash FROM users")
        ).scalar_one() == "original-hash"
    assert len(
        list(tmp_path.glob("restore.sqlite3.pre-migration-unversioned-*.bak"))
    ) == 1


def test_model_metadata_matches_the_latest_migration(tmp_path):
    engine = _engine(tmp_path / "metadata.sqlite3")
    upgrade_database(engine)

    with engine.begin() as connection:
        command.check(database_migrations.migration_config(connection))


def test_schema_version_command_reports_current_and_latest(runner):
    result = runner.invoke(args=["schema-version"])

    assert result.exit_code == 0
    assert result.output.strip() == "0003 (latest: 0003)"
