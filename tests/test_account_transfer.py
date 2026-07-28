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
    REMEMBER_ITEM_FIELDS,
    TASK_FIELDS,
    AccountImportConflictError,
    InvalidAccountExportError,
    export_account,
    import_account,
    parse_account_export,
    serialize_account_export,
)
from timemanager.db import get_db, get_engine, local_installation_id, new_public_id
from timemanager.models import (
    installations,
    projects,
    remember_items,
    task_components,
    task_dependencies,
    task_waits,
    tasks,
    users,
)

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
        database.execute(
            sa.insert(remember_items),
            [
                {
                    "public_id": new_public_id(),
                    "origin_installation_id": installation_id,
                    "user_id": user_id,
                    "title": "Get coffee",
                },
                {
                    "public_id": new_public_id(),
                    "origin_installation_id": installation_id,
                    "user_id": other_id,
                    "title": "Not my reminder",
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
    assert document["format_version"] == 4
    assert document["source_schema_revision"] == "0006"
    assert document["exported_at"] == "2026-07-24T10:00:00Z"
    assert set(document["account"]) == ACCOUNT_FIELDS
    assert [task["title"] for task in document["tasks"]] == ["Mine"]
    assert set(document["tasks"][0]) == TASK_FIELDS
    assert document["projects"] == []
    assert document["components"] == []
    assert document["dependencies"] == []
    assert document["waits"] == []
    assert [item["title"] for item in document["remember_items"]] == ["Get coffee"]
    assert set(document["remember_items"][0]) == REMEMBER_ITEM_FIELDS
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
    assert "Not my reminder" not in serialized


def test_revision_0002_fixture_import_is_adapted_idempotently(tmp_path):
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
    imported_task = round_trip["tasks"][0]
    assert imported_task["title"] == document["tasks"][0]["title"]
    assert imported_task["notes"] == document["tasks"][0]["notes"]
    assert imported_task["state"] == "active"
    assert imported_task["workflow_status"] == "open"
    assert imported_task["today_placement"] == "active"
    assert imported_task["next_action"] == ""
    assert imported_task["definition_of_done"] == ""
    assert imported_task["project_public_id"] is None
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


def test_revision_0002_import_adapts_only_first_three_options_per_date(tmp_path):
    destination = _new_app(tmp_path / "legacy-transfer.sqlite3")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    document = _fixture_document()
    base_task = document["tasks"][0]
    document["tasks"] = []
    for index in range(4):
        task = deepcopy(base_task)
        task["public_id"] = f"66666666-6666-4666-8666-{index:012d}"
        task["title"] = f"Legacy option {index}"
        document["tasks"].append(task)

    with destination.app_context():
        database = get_db()
        result = import_account(database, target_id, document)
        database.commit()
        states = database.execute(
            sa.select(tasks.c.state).order_by(tasks.c.public_id)
        ).scalars().all()

    assert result.inserted == 4
    assert states == ["active", "active", "active", "ready"]


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

        with pytest.raises(AccountImportConflictError, match="constraints"):
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


def test_import_cannot_overfill_the_active_today_plan(tmp_path):
    destination = _new_app(tmp_path / "capacity.sqlite3")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    document = _fixture_document()
    base_task = document["tasks"][0]
    document["tasks"] = []
    for index in range(4):
        task = deepcopy(base_task)
        task["public_id"] = f"55555555-5555-4555-8555-{index:012d}"
        task["state"] = "active"
        document["tasks"].append(task)

    with destination.app_context():
        database = get_db()
        with pytest.raises(AccountImportConflictError, match="active option limit"):
            import_account(database, target_id, document)
        database.commit()
        assert database.execute(
            sa.select(sa.func.count()).select_from(tasks)
        ).scalar_one() == 0


def test_export_parser_rejects_unknown_versions_fields_and_duplicate_keys():
    document = _fixture_document()
    document["format_version"] = 5
    with pytest.raises(InvalidAccountExportError, match="not supported"):
        parse_account_export(json.dumps(document))

    document = _fixture_document()
    document["password_hash"] = "must not be accepted"
    with pytest.raises(InvalidAccountExportError, match="unexpected password_hash"):
        parse_account_export(json.dumps(document))

    with pytest.raises(InvalidAccountExportError, match="Duplicate JSON field"):
        parse_account_export('{"format": "one", "format": "two"}')


def test_version_2_task_detail_and_components_remain_importable(tmp_path):
    document = _fixture_document()
    document["format_version"] = 2
    document["source_schema_revision"] = "0004"
    document["tasks"][0]["next_action"] = "Drive to the shop"
    document["tasks"][0]["definition_of_done"] = "Groceries put away"
    document["components"] = [
        {
            "public_id": "55555555-5555-4555-8555-555555555555",
            "origin_installation_public_id": document["tasks"][0][
                "origin_installation_public_id"
            ],
            "revision": 1,
            "task_public_id": document["tasks"][0]["public_id"],
            "title": "Bring reusable bags",
            "position": 0,
            "is_done": False,
            "created_at": "2026-07-24 10:00:00",
            "updated_at": "2026-07-24 10:00:00",
        }
    ]
    document = parse_account_export(json.dumps(document))
    destination = _new_app(tmp_path / "v2.sqlite3")
    target_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )

    with destination.app_context():
        database = get_db()
        result = import_account(database, target_id, document)
        database.commit()
        task = database.execute(
            sa.select(tasks.c.next_action, tasks.c.definition_of_done)
        ).mappings().one()
        component = database.execute(
            sa.select(task_components.c.title, task_components.c.position)
        ).mappings().one()

    assert result.inserted == 1
    assert dict(task) == {
        "next_action": "Drive to the shop",
        "definition_of_done": "Groceries put away",
    }
    assert dict(component) == {"title": "Bring reusable bags", "position": 0}


def test_version_4_complex_relationships_and_remember_items_round_trip_atomically(
    tmp_path,
):
    source = _new_app(tmp_path / "source-v3.sqlite3")
    source_id = create_user(
        source,
        "Source",
        "source@example.com",
        generate_password_hash("source-password"),
    )
    with source.app_context():
        database = get_db()
        installation_id = local_installation_id(database)
        project_id = database.execute(
            sa.insert(projects)
            .values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=source_id,
                title="Launch website",
                desired_outcome="Website published",
            )
            .returning(projects.c.id)
        ).scalar_one()
        first_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=source_id,
                title="Approve design",
                project_id=project_id,
                project_position=0,
                workflow_status="open",
                today_placement="active",
                state="active",
            )
            .returning(tasks.c.id)
        ).scalar_one()
        second_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=source_id,
                title="Publish",
                project_id=project_id,
                project_position=1,
                workflow_status="waiting",
                state="active",
            )
            .returning(tasks.c.id)
        ).scalar_one()
        database.execute(
            sa.insert(task_components).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=source_id,
                task_id=first_id,
                title="Open mockup",
                position=0,
            )
        )
        database.execute(
            sa.insert(task_dependencies).values(
                user_id=source_id,
                task_id=second_id,
                prerequisite_task_id=first_id,
            )
        )
        database.execute(
            sa.insert(task_waits).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=source_id,
                task_id=second_id,
                reason="Hosting approval",
                resume_status="open",
            )
        )
        database.execute(
            sa.insert(remember_items).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=source_id,
                title="Get coffee",
            )
        )
        database.commit()
        document = export_account(database, source_id)

    destination = _new_app(tmp_path / "destination-v3.sqlite3")
    destination_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    with destination.app_context():
        database = get_db()
        first = import_account(database, destination_id, document)
        database.commit()
        second = import_account(database, destination_id, document)
        database.commit()
        counts = {
            "projects": database.execute(
                sa.select(sa.func.count()).select_from(projects)
            ).scalar_one(),
            "tasks": database.execute(
                sa.select(sa.func.count()).select_from(tasks)
            ).scalar_one(),
            "components": database.execute(
                sa.select(sa.func.count()).select_from(task_components)
            ).scalar_one(),
            "dependencies": database.execute(
                sa.select(sa.func.count()).select_from(task_dependencies)
            ).scalar_one(),
            "waits": database.execute(
                sa.select(sa.func.count()).select_from(task_waits)
            ).scalar_one(),
            "remember_items": database.execute(
                sa.select(sa.func.count()).select_from(remember_items)
            ).scalar_one(),
        }

    assert first.inserted == 2
    assert second.unchanged == 2
    assert counts == {
        "projects": 1,
        "tasks": 2,
        "components": 1,
        "dependencies": 1,
        "waits": 1,
        "remember_items": 1,
    }


def test_version_3_complex_documents_remain_importable(tmp_path):
    source = _new_app(tmp_path / "source-v3.sqlite3")
    source_id = create_user(
        source,
        "Source",
        "source@example.com",
        generate_password_hash("source-password"),
    )
    with source.app_context():
        database = get_db()
        database.execute(
            sa.insert(tasks).values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=source_id,
                title="Imported v3 task",
            )
        )
        database.commit()
        document = export_account(database, source_id)

    document["format_version"] = 3
    document.pop("remember_items")
    document = parse_account_export(json.dumps(document))

    destination = _new_app(tmp_path / "destination-v3.sqlite3")
    destination_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    with destination.app_context():
        database = get_db()
        result = import_account(database, destination_id, document)
        database.commit()
        title = database.execute(sa.select(tasks.c.title)).scalar_one()

    assert result.inserted == 1
    assert title == "Imported v3 task"


def test_remember_import_is_atomic_when_destination_would_exceed_limit(tmp_path):
    source = _new_app(tmp_path / "remember-source.sqlite3")
    source_id = create_user(
        source,
        "Source",
        "source@example.com",
        generate_password_hash("source-password"),
    )
    with source.app_context():
        database = get_db()
        installation_id = local_installation_id(database)
        for title in ("Source one", "Source two"):
            database.execute(
                sa.insert(remember_items).values(
                    public_id=new_public_id(),
                    origin_installation_id=installation_id,
                    user_id=source_id,
                    title=title,
                )
            )
        database.commit()
        document = export_account(database, source_id)

    destination = _new_app(tmp_path / "remember-destination.sqlite3")
    destination_id = create_user(
        destination,
        "Destination",
        "destination@example.com",
        generate_password_hash("destination-password"),
    )
    with destination.app_context():
        database = get_db()
        installation_id = local_installation_id(database)
        for title in ("Local one", "Local two"):
            database.execute(
                sa.insert(remember_items).values(
                    public_id=new_public_id(),
                    origin_installation_id=installation_id,
                    user_id=destination_id,
                    title=title,
                )
            )
        database.commit()

        with pytest.raises(AccountImportConflictError, match="Remember limit"):
            import_account(database, destination_id, document)
        database.commit()
        titles = database.execute(
            sa.select(remember_items.c.title).order_by(remember_items.c.title)
        ).scalars().all()

    assert titles == ["Local one", "Local two"]


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
