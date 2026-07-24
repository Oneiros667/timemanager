from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

import click
import sqlalchemy as sa
from flask import Flask
from flask.cli import with_appcontext
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from .database_migrations import current_revision
from .db import get_engine
from .models import installations, tasks, users
from .planning import TODAY_OPTION_LIMIT


EXPORT_FORMAT = "timemanager.account-export"
EXPORT_FORMAT_VERSION = 1
TASK_STATES = {"inbox", "ready", "active", "done", "dropped"}

ACCOUNT_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "display_name",
    "email",
    "created_at",
}
TASK_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "title",
    "notes",
    "state",
    "planned_date",
    "is_highlight",
    "created_at",
    "updated_at",
    "completed_at",
}
TOP_LEVEL_FIELDS = {
    "format",
    "format_version",
    "exported_at",
    "source_schema_revision",
    "account",
    "tasks",
}


class AccountTransferError(ValueError):
    """Base error for account transfer validation and conflicts."""


class InvalidAccountExportError(AccountTransferError):
    """Raised when an export package does not match the supported contract."""


class AccountImportConflictError(AccountTransferError):
    """Raised when importing would overwrite ambiguous or foreign data."""


@dataclass(frozen=True)
class ImportResult:
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0
    kept_newer: int = 0


def export_account(
    connection: Connection,
    user_id: int,
    *,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    origin = installations.alias("account_origin")
    account = (
        connection.execute(
            sa.select(
                users.c.public_id,
                origin.c.public_id.label("origin_installation_public_id"),
                users.c.revision,
                users.c.display_name,
                users.c.email,
                users.c.created_at,
            )
            .join(origin, users.c.origin_installation_id == origin.c.id)
            .where(users.c.id == user_id)
        )
        .mappings()
        .one_or_none()
    )
    if account is None:
        raise AccountTransferError("The selected account does not exist.")

    task_origin = installations.alias("task_origin")
    task_rows = (
        connection.execute(
            sa.select(
                tasks.c.public_id,
                task_origin.c.public_id.label("origin_installation_public_id"),
                tasks.c.revision,
                tasks.c.title,
                tasks.c.notes,
                tasks.c.state,
                tasks.c.planned_date,
                tasks.c.is_highlight,
                tasks.c.created_at,
                tasks.c.updated_at,
                tasks.c.completed_at,
            )
            .join(
                task_origin,
                tasks.c.origin_installation_id == task_origin.c.id,
            )
            .where(tasks.c.user_id == user_id)
            .order_by(tasks.c.public_id)
        )
        .mappings()
        .all()
    )

    timestamp = exported_at or datetime.now(timezone.utc)
    return {
        "format": EXPORT_FORMAT,
        "format_version": EXPORT_FORMAT_VERSION,
        "exported_at": timestamp.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "source_schema_revision": current_revision(connection.engine),
        "account": dict(account),
        "tasks": [dict(task) for task in task_rows],
    }


def serialize_account_export(document: dict[str, Any]) -> str:
    validate_account_export(document)
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def parse_account_export(content: str) -> dict[str, Any]:
    try:
        document = json.loads(content, object_pairs_hook=_reject_duplicate_keys)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise InvalidAccountExportError(f"Invalid JSON: {error}") from error
    validate_account_export(document)
    return document


def validate_account_export(document: Any) -> None:
    if not isinstance(document, dict):
        raise InvalidAccountExportError("The export root must be a JSON object.")
    _require_exact_fields(document, TOP_LEVEL_FIELDS, "export")
    if document["format"] != EXPORT_FORMAT:
        raise InvalidAccountExportError("The export format is not supported.")
    if document["format_version"] != EXPORT_FORMAT_VERSION:
        raise InvalidAccountExportError(
            f"Export format version {document['format_version']!r} is not supported."
        )
    _require_string(document["exported_at"], "exported_at")
    _require_string(document["source_schema_revision"], "source_schema_revision")

    account = document["account"]
    if not isinstance(account, dict):
        raise InvalidAccountExportError("account must be a JSON object.")
    _require_exact_fields(account, ACCOUNT_FIELDS, "account")
    _require_uuid(account["public_id"], "account.public_id")
    _require_uuid(
        account["origin_installation_public_id"],
        "account.origin_installation_public_id",
    )
    _require_revision(account["revision"], "account.revision")
    for field in ("display_name", "email", "created_at"):
        _require_string(account[field], f"account.{field}")

    task_rows = document["tasks"]
    if not isinstance(task_rows, list):
        raise InvalidAccountExportError("tasks must be a JSON array.")
    seen_public_ids: set[str] = set()
    for index, task in enumerate(task_rows):
        path = f"tasks[{index}]"
        if not isinstance(task, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(task, TASK_FIELDS, path)
        public_id = _require_uuid(task["public_id"], f"{path}.public_id")
        if public_id in seen_public_ids:
            raise InvalidAccountExportError(
                f"{path}.public_id duplicates another task."
            )
        seen_public_ids.add(public_id)
        _require_uuid(
            task["origin_installation_public_id"],
            f"{path}.origin_installation_public_id",
        )
        _require_revision(task["revision"], f"{path}.revision")
        for field in ("title", "notes", "created_at", "updated_at"):
            _require_string(task[field], f"{path}.{field}")
        if task["state"] not in TASK_STATES:
            raise InvalidAccountExportError(f"{path}.state is not supported.")
        for field in ("planned_date", "completed_at"):
            if task[field] is not None:
                _require_string(task[field], f"{path}.{field}")
        if not isinstance(task["is_highlight"], bool):
            raise InvalidAccountExportError(f"{path}.is_highlight must be boolean.")


def import_account(
    connection: Connection,
    target_user_id: int,
    document: dict[str, Any],
) -> ImportResult:
    validate_account_export(document)
    task_rows = _normalized_tasks_for_import(document)
    target_exists = connection.execute(
        sa.select(users.c.id).where(users.c.id == target_user_id)
    ).scalar_one_or_none()
    if target_exists is None:
        raise AccountTransferError("The destination account does not exist.")

    existing_tasks = _existing_tasks(
        connection,
        [task["public_id"] for task in task_rows],
    )

    inserted = updated = unchanged = kept_newer = 0
    try:
        with connection.begin_nested():
            origins = {
                task["origin_installation_public_id"]
                for task in task_rows
            }
            origin_ids = _installation_ids(connection, origins)
            for task in task_rows:
                existing = existing_tasks.get(task["public_id"])
                values = _task_values(task, target_user_id, origin_ids)
                if existing is None:
                    connection.execute(sa.insert(tasks).values(**values))
                    inserted += 1
                    continue
                if existing["user_id"] != target_user_id:
                    raise AccountImportConflictError(
                        f"Task {task['public_id']} belongs to another local account."
                    )
                if task["revision"] < existing["revision"]:
                    kept_newer += 1
                    continue
                if task["revision"] == existing["revision"]:
                    if _same_task(existing, task):
                        unchanged += 1
                        continue
                    raise AccountImportConflictError(
                        f"Task {task['public_id']} has divergent content at "
                        f"revision {task['revision']}."
                    )
                connection.execute(
                    sa.update(tasks)
                    .where(tasks.c.id == existing["id"])
                    .values(**values)
                )
                updated += 1
            _assert_today_capacity(connection, target_user_id)
    except IntegrityError as error:
        raise AccountImportConflictError(
            "The import conflicts with destination task constraints."
        ) from error

    return ImportResult(
        inserted=inserted,
        updated=updated,
        unchanged=unchanged,
        kept_newer=kept_newer,
    )


def _normalized_tasks_for_import(document: dict[str, Any]) -> list[dict[str, Any]]:
    task_rows = [dict(task) for task in document["tasks"]]
    if document["source_schema_revision"] != "0002":
        return task_rows

    ready_by_date: dict[str, list[dict[str, Any]]] = {}
    for task in task_rows:
        if task["planned_date"] is None or task["state"] != "ready":
            continue
        if task["is_highlight"]:
            task["state"] = "active"
            continue
        ready_by_date.setdefault(task["planned_date"], []).append(task)

    for planned_tasks in ready_by_date.values():
        planned_tasks.sort(key=lambda task: (task["created_at"], task["public_id"]))
        for task in planned_tasks[:TODAY_OPTION_LIMIT]:
            task["state"] = "active"
    return task_rows


def _assert_today_capacity(connection: Connection, user_id: int) -> None:
    overfilled_date = connection.execute(
        sa.select(tasks.c.planned_date)
        .where(
            tasks.c.user_id == user_id,
            tasks.c.planned_date.is_not(None),
            tasks.c.state == "active",
            tasks.c.is_highlight.is_(False),
        )
        .group_by(tasks.c.planned_date)
        .having(sa.func.count() > TODAY_OPTION_LIMIT)
        .limit(1)
    ).scalar_one_or_none()
    if overfilled_date is not None:
        raise AccountImportConflictError(
            f"The import would exceed the active option limit on {overfilled_date}."
        )


def _installation_ids(
    connection: Connection,
    public_ids: set[str],
) -> dict[str, int]:
    rows = connection.execute(
        sa.select(installations.c.id, installations.c.public_id).where(
            installations.c.public_id.in_(public_ids)
        )
    ).all()
    result = {public_id: installation_id for installation_id, public_id in rows}
    for public_id in sorted(public_ids - result.keys()):
        installation_id = connection.execute(
            sa.insert(installations)
            .values(public_id=public_id, is_local=False)
            .returning(installations.c.id)
        ).scalar_one()
        result[public_id] = int(installation_id)
    return result


def _existing_tasks(
    connection: Connection,
    public_ids: list[str],
) -> dict[str, dict[str, Any]]:
    if not public_ids:
        return {}
    origin = installations.alias("existing_origin")
    rows = (
        connection.execute(
            sa.select(
                tasks,
                origin.c.public_id.label("origin_installation_public_id"),
            )
            .join(origin, tasks.c.origin_installation_id == origin.c.id)
            .where(tasks.c.public_id.in_(public_ids))
        )
        .mappings()
        .all()
    )
    return {row["public_id"]: dict(row) for row in rows}


def _task_values(
    task: dict[str, Any],
    target_user_id: int,
    origin_ids: dict[str, int],
) -> dict[str, Any]:
    return {
        "public_id": task["public_id"],
        "origin_installation_id": origin_ids[
            task["origin_installation_public_id"]
        ],
        "revision": task["revision"],
        "user_id": target_user_id,
        "title": task["title"],
        "notes": task["notes"],
        "state": task["state"],
        "planned_date": task["planned_date"],
        "is_highlight": task["is_highlight"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
        "completed_at": task["completed_at"],
    }


def _same_task(existing: dict[str, Any], incoming: dict[str, Any]) -> bool:
    return all(existing[field] == incoming[field] for field in TASK_FIELDS)


def _require_exact_fields(
    value: dict[str, Any],
    expected: set[str],
    path: str,
) -> None:
    actual = set(value)
    if actual == expected:
        return
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    details = []
    if missing:
        details.append(f"missing {', '.join(missing)}")
    if unexpected:
        details.append(f"unexpected {', '.join(unexpected)}")
    detail = "; ".join(details)
    raise InvalidAccountExportError(f"{path} fields are invalid: {detail}.")


def _require_string(value: Any, path: str) -> str:
    if not isinstance(value, str):
        raise InvalidAccountExportError(f"{path} must be a string.")
    return value


def _require_uuid(value: Any, path: str) -> str:
    _require_string(value, path)
    try:
        parsed = UUID(value)
    except ValueError as error:
        raise InvalidAccountExportError(f"{path} must be a UUID.") from error
    if str(parsed) != value:
        raise InvalidAccountExportError(f"{path} must use canonical UUID form.")
    return value


def _require_revision(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise InvalidAccountExportError(f"{path} must be a positive integer.")
    return value


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidAccountExportError(f"Duplicate JSON field: {key}.")
        result[key] = value
    return result


def _user_id_for_email(connection: Connection, email: str) -> int:
    user_id = connection.execute(
        sa.select(users.c.id).where(users.c.email == email.strip().casefold())
    ).scalar_one_or_none()
    if user_id is None:
        raise click.ClickException("No local account has that email address.")
    return int(user_id)


def _write_private_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise click.ClickException(
            f"{path} already exists; choose a new path."
        ) from error
    with os.fdopen(descriptor, "w", encoding="utf-8") as output:
        output.write(content)


@click.command("export-account")
@click.option("--email", required=True, help="Local account email to export.")
@click.option(
    "--output",
    required=True,
    type=click.Path(path_type=Path, dir_okay=False),
    help="New JSON export file; existing files are never overwritten.",
)
@with_appcontext
def export_account_command(email: str, output: Path) -> None:
    engine = get_engine()
    with engine.connect() as connection:
        user_id = _user_id_for_email(connection, email)
        content = serialize_account_export(export_account(connection, user_id))
    _write_private_file(output, content)
    click.echo(f"Exported one account to {output}.")


@click.command("import-account")
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(path_type=Path, exists=True, dir_okay=False, readable=True),
    help="Versioned Timemanager account export.",
)
@click.option(
    "--into-email",
    required=True,
    help="Existing local account that will own the imported tasks.",
)
@with_appcontext
def import_account_command(input_path: Path, into_email: str) -> None:
    try:
        document = parse_account_export(input_path.read_text(encoding="utf-8"))
        with get_engine().begin() as connection:
            user_id = _user_id_for_email(connection, into_email)
            result = import_account(connection, user_id, document)
    except AccountTransferError as error:
        raise click.ClickException(str(error)) from error

    click.echo(
        "Import complete: "
        f"{result.inserted} inserted, "
        f"{result.updated} updated, "
        f"{result.unchanged} unchanged, "
        f"{result.kept_newer} kept as newer local records."
    )


def init_app(app: Flask) -> None:
    app.cli.add_command(export_account_command)
    app.cli.add_command(import_account_command)
