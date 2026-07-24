from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

import pytest
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from timemanager import create_app
from timemanager.account_transfer import (
    ACCOUNT_FIELDS,
    TASK_FIELDS,
    AccountImportConflictError,
    InvalidAccountExportError,
    export_account,
    import_account,
    parse_account_export,
    serialize_account_export,
)
from timemanager.db import get_db, get_engine, local_installation_id, new_public_id
from timemanager.models import installations, tasks, users

from .conftest import create_user, register


EXPORT_V1 = Path(__file__).with_name("fixtures") / "account_export_v1.json"


def _fixture_document() -> dict:
    return parse_account_export(EXPORT_V1.read_text(encoding="utf-8"))


def _registered_user_id(app, client) -> int:
    register(client)
    with app.app_context():
        return int(get_db().execute(sa.select(users.c.id)).scalar_one())


def _new_app(database_path: Path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "destination-secret",
            "DATABASE": str(database_path),
            "DATABASE_URL": None,
        }
    )


def test_export_is_account_scoped_versioned_and_excludes_secrets(app, client):
    user_id = _registered_user_id(app, client)
    other_id = create_user(
        app,
        "Other",
        "other@example.com",
        generate_password_hash("other-password"),
    )
    with app.app_context():
        database = get_db()
        installation_id = local_installation_id(database)
        database.execute(
            sa.insert(tasks),
            [
                {
                    "public_id": new_public_id(),
                    "origin_installation_id": installation_id,
                    "user_id": user_id,
                    "title": "Mine",
                },
                {
                    "public_id": new_public_id(),
                    "origin_installation_id": installation_id,
                    "user_id": other_id,
                    "title": "Not mine",
                },
            ],
        )
        database.commit()
        document = export_account(
            database,
            user_id,
            exported_at=datetime(2026, 7, 24, 10, tzinfo=timezone.utc),
        )

    assert document["format"] == "timemanager.account-export"
    assert document["format_version"] == 1
    assert document["source_schema_revision"] == "0002"
    assert document["exported_at"] == "2026-07-24T10:00:00Z"
    assert set(document["account"]) == ACCOUNT_FIELDS
    assert [task["title"] for task in document["tasks"]] == ["Mine"]
    assert set(document["tasks"][0]) == TASK_FIELDS
    UUID(document["account"]["public_id"])

    serialized = serialize_account_export(document)
    keys = set()

    def collect_keys(value):
        if isinstance(value, dict):
            keys.update(value)
            for child in value.values():
                collect_keys(child)
        elif isinstance(value, list):
            for child in value:
                collect_keys(child)

    collect_keys(json.loads(serialized))
    assert {
        "password",
        "password_hash",
        "secret",
        "secret_key",
        "session",
        "user_id",
        "id",
        "origin_installation_id",
    }.isdisjoint(keys)
    assert "other@example.com" not in serialized


def test_fixture_import_round_trip_is_idempotent_and_preserves_provenance(tmp_path):
    destination = _new_app(tmp_path / "destination.sqlite3")
    destination_password_hash = generate_password_hash("destination-password")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        destination_password_hash,
    )
    document = _fixture_document()

    with destination.app_context():
        database = get_db()
        first = import_account(database, target_id, document)
        database.commit()
        second = import_account(database, target_id, document)
        database.commit()
        round_trip = export_account(
            database,
            target_id,
            exported_at=datetime(2026, 7, 24, 11, tzinfo=timezone.utc),
        )
        imported = (
            database.execute(
                sa.select(
                    tasks.c.user_id,
                    installations.c.public_id.label("origin_public_id"),
                )
                .join(
                    installations,
                    tasks.c.origin_installation_id == installations.c.id,
                )
                .where(tasks.c.public_id == document["tasks"][0]["public_id"])
            )
            .mappings()
            .one()
        )
        target_password_hash = database.execute(
            sa.select(users.c.password_hash).where(users.c.id == target_id)
        ).scalar_one()

    assert first.inserted == 1
    assert second.unchanged == 1
    assert round_trip["tasks"] == document["tasks"]
    assert round_trip["account"]["email"] == "destination@example.com"
    assert imported["user_id"] == target_id
    assert imported["origin_public_id"] == (
        document["tasks"][0]["origin_installation_public_id"]
    )
    assert target_password_hash == destination_password_hash


def test_import_applies_newer_revision_and_keeps_newer_local_record(tmp_path):
    destination = _new_app(tmp_path / "revisions.sqlite3")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    original = _fixture_document()
    newer = deepcopy(original)
    newer["tasks"][0]["revision"] = 2
    newer["tasks"][0]["title"] = "Buy groceries and fruit"

    with destination.app_context():
        database = get_db()
        import_account(database, target_id, original)
        database.commit()
        updated = import_account(database, target_id, newer)
        database.commit()
        kept = import_account(database, target_id, original)
        database.commit()
        task = database.execute(
            sa.select(tasks.c.title, tasks.c.revision)
        ).mappings().one()

    assert updated.updated == 1
    assert kept.kept_newer == 1
    assert dict(task) == {"title": "Buy groceries and fruit", "revision": 2}


def test_same_revision_divergence_fails_without_partial_import(tmp_path):
    destination = _new_app(tmp_path / "conflict.sqlite3")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    original = _fixture_document()
    divergent = deepcopy(original)
    divergent["tasks"][0]["title"] = "Conflicting title"
    extra = deepcopy(divergent["tasks"][0])
    extra["public_id"] = "44444444-4444-4444-8444-444444444444"
    divergent["tasks"].insert(0, extra)

    with destination.app_context():
        database = get_db()
        import_account(database, target_id, original)
        database.commit()
        with pytest.raises(AccountImportConflictError, match="divergent content"):
            import_account(database, target_id, divergent)
        database.commit()
        titles = database.execute(
            sa.select(tasks.c.title).order_by(tasks.c.title)
        ).scalars().all()

    assert titles == ["Buy groceries"]


def test_task_public_id_cannot_cross_local_account_boundary(tmp_path):
    destination = _new_app(tmp_path / "ownership.sqlite3")
    first_id = create_user(
        destination,
        "First",
        "first@example.com",
        generate_password_hash("first-password"),
    )
    second_id = create_user(
        destination,
        "Second",
        "second@example.com",
        generate_password_hash("second-password"),
    )
    document = _fixture_document()

    with destination.app_context():
        database = get_db()
        import_account(database, first_id, document)
        database.commit()
        with pytest.raises(AccountImportConflictError, match="another local account"):
            import_account(database, second_id, document)
        database.rollback()


def test_constraint_conflict_rolls_back_tasks_and_imported_provenance(tmp_path):
    destination = _new_app(tmp_path / "constraint.sqlite3")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    document = _fixture_document()
    document["tasks"][0]["is_highlight"] = True

    with destination.app_context():
        database = get_db()
        database.execute(
            sa.insert(tasks).values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=target_id,
                title="Existing highlight",
                state="ready",
                planned_date="2026-07-24",
                is_highlight=True,
            )
        )
        database.commit()

        with pytest.raises(AccountImportConflictError, match="task constraints"):
            import_account(database, target_id, document)
        database.commit()

        assert database.execute(
            sa.select(sa.func.count()).select_from(tasks)
        ).scalar_one() == 1
        assert database.execute(
            sa.select(sa.func.count())
            .select_from(installations)
            .where(
                installations.c.public_id
                == document["tasks"][0]["origin_installation_public_id"]
            )
        ).scalar_one() == 0


def test_export_parser_rejects_unknown_versions_fields_and_duplicate_keys():
    document = _fixture_document()
    document["format_version"] = 2
    with pytest.raises(InvalidAccountExportError, match="not supported"):
        parse_account_export(json.dumps(document))

    document = _fixture_document()
    document["password_hash"] = "must not be accepted"
    with pytest.raises(InvalidAccountExportError, match="unexpected password_hash"):
        parse_account_export(json.dumps(document))

    with pytest.raises(InvalidAccountExportError, match="Duplicate JSON field"):
        parse_account_export('{"format": "one", "format": "two"}')


def test_cli_exports_private_file_and_imports_into_explicit_account(
    app,
    client,
    tmp_path,
):
    _registered_user_id(app, client)
    export_path = tmp_path / "account.json"
    result = app.test_cli_runner().invoke(
        args=[
            "export-account",
            "--email",
            "alex@example.com",
            "--output",
            str(export_path),
        ]
    )

    assert result.exit_code == 0
    assert export_path.stat().st_mode & 0o777 == 0o600
    assert "password_hash" not in export_path.read_text(encoding="utf-8")
    overwrite = app.test_cli_runner().invoke(
        args=[
            "export-account",
            "--email",
            "alex@example.com",
            "--output",
            str(export_path),
        ]
    )
    assert overwrite.exit_code != 0
    assert "already exists" in overwrite.output

    destination = _new_app(tmp_path / "cli-destination.sqlite3")
    create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    imported = destination.test_cli_runner().invoke(
        args=[
            "import-account",
            "--input",
            str(export_path),
            "--into-email",
            "destination@example.com",
        ]
    )
    assert imported.exit_code == 0
    assert "Import complete:" in imported.output
