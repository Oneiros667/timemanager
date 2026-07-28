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
from .models import (
    installations,
    projects,
    remember_items,
    task_components,
    task_dependencies,
    task_waits,
    tasks,
    users,
)
from .planning import TODAY_OPTION_LIMIT


EXPORT_FORMAT = "timemanager.account-export"
EXPORT_FORMAT_VERSION = 5
SUPPORTED_EXPORT_VERSIONS = {1, 2, 3, 4, 5}
TASK_STATES = {"inbox", "ready", "active", "done", "dropped"}
WORKFLOW_STATUSES = {"inbox", "open", "waiting", "done", "dropped"}
TODAY_PLACEMENTS = {"unplanned", "active", "overflow"}

ACCOUNT_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "display_name",
    "email",
    "created_at",
}
TASK_V1_FIELDS = {
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
TASK_V2_FIELDS = TASK_V1_FIELDS | {"next_action", "definition_of_done"}
TASK_V3_FIELDS = TASK_V2_FIELDS | {
    "project_public_id",
    "project_position",
    "workflow_status",
    "today_placement",
    "dependency_override",
}
TASK_FIELDS = TASK_V3_FIELDS | {"dropped_at"}
PROJECT_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "title",
    "desired_outcome",
    "notes",
    "state",
    "created_at",
    "updated_at",
}
COMPONENT_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "task_public_id",
    "title",
    "position",
    "is_done",
    "created_at",
    "updated_at",
}
DEPENDENCY_FIELDS = {"task_public_id", "prerequisite_task_public_id", "created_at"}
WAIT_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "task_public_id",
    "reason",
    "waiting_on",
    "resume_status",
    "review_date",
    "follow_up_task_public_id",
    "created_at",
    "updated_at",
}
REMEMBER_ITEM_FIELDS = {
    "public_id",
    "origin_installation_public_id",
    "revision",
    "title",
    "created_at",
    "updated_at",
}
TOP_LEVEL_FIELDS = {
    "format",
    "format_version",
    "exported_at",
    "source_schema_revision",
    "account",
    "tasks",
}
TOP_LEVEL_V2_FIELDS = TOP_LEVEL_FIELDS | {"components"}
TOP_LEVEL_V3_FIELDS = TOP_LEVEL_V2_FIELDS | {
    "projects",
    "dependencies",
    "waits",
}
TOP_LEVEL_V4_FIELDS = TOP_LEVEL_V3_FIELDS | {"remember_items"}
TOP_LEVEL_V5_FIELDS = TOP_LEVEL_V4_FIELDS


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
    task_project = projects.alias("task_project")
    task_rows = (
        connection.execute(
            sa.select(
                tasks.c.public_id,
                task_origin.c.public_id.label("origin_installation_public_id"),
                tasks.c.revision,
                tasks.c.title,
                tasks.c.notes,
                tasks.c.next_action,
                tasks.c.definition_of_done,
                tasks.c.state,
                tasks.c.planned_date,
                tasks.c.is_highlight,
                tasks.c.created_at,
                tasks.c.updated_at,
                tasks.c.completed_at,
                tasks.c.dropped_at,
                task_project.c.public_id.label("project_public_id"),
                tasks.c.project_position,
                tasks.c.workflow_status,
                tasks.c.today_placement,
                tasks.c.dependency_override,
            )
            .join(
                task_origin,
                tasks.c.origin_installation_id == task_origin.c.id,
            )
            .outerjoin(task_project, tasks.c.project_id == task_project.c.id)
            .where(tasks.c.user_id == user_id)
            .order_by(tasks.c.public_id)
        )
        .mappings()
        .all()
    )
    project_origin = installations.alias("project_origin")
    project_rows = (
        connection.execute(
            sa.select(
                projects.c.public_id,
                project_origin.c.public_id.label("origin_installation_public_id"),
                projects.c.revision,
                projects.c.title,
                projects.c.desired_outcome,
                projects.c.notes,
                projects.c.state,
                projects.c.created_at,
                projects.c.updated_at,
            )
            .join(
                project_origin,
                projects.c.origin_installation_id == project_origin.c.id,
            )
            .where(projects.c.user_id == user_id)
            .order_by(projects.c.public_id)
        )
        .mappings()
        .all()
    )
    component_origin = installations.alias("component_origin")
    component_task = tasks.alias("component_task")
    component_rows = (
        connection.execute(
            sa.select(
                task_components.c.public_id,
                component_origin.c.public_id.label(
                    "origin_installation_public_id"
                ),
                task_components.c.revision,
                component_task.c.public_id.label("task_public_id"),
                task_components.c.title,
                task_components.c.position,
                task_components.c.is_done,
                task_components.c.created_at,
                task_components.c.updated_at,
            )
            .join(
                component_origin,
                task_components.c.origin_installation_id == component_origin.c.id,
            )
            .join(component_task, task_components.c.task_id == component_task.c.id)
            .where(task_components.c.user_id == user_id)
            .order_by(component_task.c.public_id, task_components.c.position)
        )
        .mappings()
        .all()
    )
    dependency_task = tasks.alias("dependency_task")
    prerequisite = tasks.alias("dependency_prerequisite")
    dependency_rows = (
        connection.execute(
            sa.select(
                dependency_task.c.public_id.label("task_public_id"),
                prerequisite.c.public_id.label("prerequisite_task_public_id"),
                task_dependencies.c.created_at,
            )
            .join(
                dependency_task,
                task_dependencies.c.task_id == dependency_task.c.id,
            )
            .join(
                prerequisite,
                task_dependencies.c.prerequisite_task_id == prerequisite.c.id,
            )
            .where(task_dependencies.c.user_id == user_id)
            .order_by(
                dependency_task.c.public_id,
                prerequisite.c.public_id,
            )
        )
        .mappings()
        .all()
    )
    wait_origin = installations.alias("wait_origin")
    wait_task = tasks.alias("wait_task")
    follow_up = tasks.alias("wait_follow_up")
    wait_rows = (
        connection.execute(
            sa.select(
                task_waits.c.public_id,
                wait_origin.c.public_id.label("origin_installation_public_id"),
                task_waits.c.revision,
                wait_task.c.public_id.label("task_public_id"),
                task_waits.c.reason,
                task_waits.c.waiting_on,
                task_waits.c.resume_status,
                task_waits.c.review_date,
                follow_up.c.public_id.label("follow_up_task_public_id"),
                task_waits.c.created_at,
                task_waits.c.updated_at,
            )
            .join(
                wait_origin,
                task_waits.c.origin_installation_id == wait_origin.c.id,
            )
            .join(wait_task, task_waits.c.task_id == wait_task.c.id)
            .outerjoin(follow_up, task_waits.c.follow_up_task_id == follow_up.c.id)
            .where(task_waits.c.user_id == user_id)
            .order_by(task_waits.c.public_id)
        )
        .mappings()
        .all()
    )
    remember_origin = installations.alias("remember_origin")
    remember_rows = (
        connection.execute(
            sa.select(
                remember_items.c.public_id,
                remember_origin.c.public_id.label(
                    "origin_installation_public_id"
                ),
                remember_items.c.revision,
                remember_items.c.title,
                remember_items.c.created_at,
                remember_items.c.updated_at,
            )
            .join(
                remember_origin,
                remember_items.c.origin_installation_id == remember_origin.c.id,
            )
            .where(remember_items.c.user_id == user_id)
            .order_by(remember_items.c.created_at, remember_items.c.public_id)
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
        "projects": [dict(project) for project in project_rows],
        "components": [dict(component) for component in component_rows],
        "dependencies": [dict(dependency) for dependency in dependency_rows],
        "waits": [dict(wait) for wait in wait_rows],
        "remember_items": [dict(item) for item in remember_rows],
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
    if document.get("format") != EXPORT_FORMAT:
        raise InvalidAccountExportError("The export format is not supported.")
    version = document.get("format_version")
    if version not in SUPPORTED_EXPORT_VERSIONS:
        raise InvalidAccountExportError(
            f"Export format version {version!r} is not supported."
        )
    expected_top = {
        1: TOP_LEVEL_FIELDS,
        2: TOP_LEVEL_V2_FIELDS,
        3: TOP_LEVEL_V3_FIELDS,
        4: TOP_LEVEL_V4_FIELDS,
        5: TOP_LEVEL_V5_FIELDS,
    }[version]
    _require_exact_fields(document, expected_top, "export")
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

    task_fields = {
        1: TASK_V1_FIELDS,
        2: TASK_V2_FIELDS,
        3: TASK_V3_FIELDS,
        4: TASK_V3_FIELDS,
        5: TASK_FIELDS,
    }[version]
    task_rows = _require_list(document["tasks"], "tasks")
    seen_public_ids: set[str] = set()
    for index, task in enumerate(task_rows):
        path = f"tasks[{index}]"
        if not isinstance(task, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(task, task_fields, path)
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
        if version >= 2:
            for field in ("next_action", "definition_of_done"):
                _require_string(task[field], f"{path}.{field}")
        if task["state"] not in TASK_STATES:
            raise InvalidAccountExportError(f"{path}.state is not supported.")
        for field in ("planned_date", "completed_at"):
            if task[field] is not None:
                _require_string(task[field], f"{path}.{field}")
        if not isinstance(task["is_highlight"], bool):
            raise InvalidAccountExportError(f"{path}.is_highlight must be boolean.")
        if version >= 3:
            if task["project_public_id"] is not None:
                _require_uuid(
                    task["project_public_id"],
                    f"{path}.project_public_id",
                )
            if task["project_position"] is not None:
                _require_nonnegative_int(
                    task["project_position"],
                    f"{path}.project_position",
                )
            if task["workflow_status"] not in WORKFLOW_STATUSES:
                raise InvalidAccountExportError(
                    f"{path}.workflow_status is not supported."
                )
            if task["today_placement"] not in TODAY_PLACEMENTS:
                raise InvalidAccountExportError(
                    f"{path}.today_placement is not supported."
                )
            if not isinstance(task["dependency_override"], bool):
                raise InvalidAccountExportError(
                    f"{path}.dependency_override must be boolean."
                )
        if version >= 5:
            if task["dropped_at"] is not None:
                _require_string(task["dropped_at"], f"{path}.dropped_at")
            if (
                task["workflow_status"] == "dropped"
                and task["dropped_at"] is None
            ):
                raise InvalidAccountExportError(
                    f"{path}.dropped_at is required for a dropped task."
                )
            if (
                task["workflow_status"] != "dropped"
                and task["dropped_at"] is not None
            ):
                raise InvalidAccountExportError(
                    f"{path}.dropped_at is only valid for a dropped task."
                )

    if version >= 2:
        _validate_components(document["components"], seen_public_ids)
    if version >= 3:
        project_ids = _validate_projects(document["projects"])
        for index, task in enumerate(task_rows):
            project_id = task["project_public_id"]
            if project_id is not None and project_id not in project_ids:
                raise InvalidAccountExportError(
                    f"tasks[{index}].project_public_id is missing from projects."
                )
        _validate_dependencies(document["dependencies"], seen_public_ids)
        _validate_waits(document["waits"], seen_public_ids)
    if version >= 4:
        _validate_remember_items(document["remember_items"])


def _require_list(value: Any, path: str) -> list:
    if not isinstance(value, list):
        raise InvalidAccountExportError(f"{path} must be a JSON array.")
    return value


def _validate_projects(value: Any) -> set[str]:
    rows = _require_list(value, "projects")
    seen: set[str] = set()
    for index, project in enumerate(rows):
        path = f"projects[{index}]"
        if not isinstance(project, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(project, PROJECT_FIELDS, path)
        public_id = _require_uuid(project["public_id"], f"{path}.public_id")
        if public_id in seen:
            raise InvalidAccountExportError(f"{path}.public_id is duplicated.")
        seen.add(public_id)
        _require_uuid(
            project["origin_installation_public_id"],
            f"{path}.origin_installation_public_id",
        )
        _require_revision(project["revision"], f"{path}.revision")
        for field in (
            "title",
            "desired_outcome",
            "notes",
            "created_at",
            "updated_at",
        ):
            _require_string(project[field], f"{path}.{field}")
        if project["state"] not in {"active", "completed", "dropped"}:
            raise InvalidAccountExportError(f"{path}.state is not supported.")
    return seen


def _validate_components(value: Any, task_ids: set[str]) -> None:
    rows = _require_list(value, "components")
    seen: set[str] = set()
    positions: set[tuple[str, int]] = set()
    for index, component in enumerate(rows):
        path = f"components[{index}]"
        if not isinstance(component, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(component, COMPONENT_FIELDS, path)
        public_id = _require_uuid(component["public_id"], f"{path}.public_id")
        if public_id in seen:
            raise InvalidAccountExportError(f"{path}.public_id is duplicated.")
        seen.add(public_id)
        _require_uuid(
            component["origin_installation_public_id"],
            f"{path}.origin_installation_public_id",
        )
        _require_revision(component["revision"], f"{path}.revision")
        task_id = _require_uuid(
            component["task_public_id"],
            f"{path}.task_public_id",
        )
        if task_id not in task_ids:
            raise InvalidAccountExportError(f"{path}.task_public_id is missing.")
        _require_string(component["title"], f"{path}.title")
        position = _require_nonnegative_int(
            component["position"],
            f"{path}.position",
        )
        key = (task_id, position)
        if key in positions:
            raise InvalidAccountExportError(
                f"{path}.position duplicates another component."
            )
        positions.add(key)
        if not isinstance(component["is_done"], bool):
            raise InvalidAccountExportError(f"{path}.is_done must be boolean.")
        for field in ("created_at", "updated_at"):
            _require_string(component[field], f"{path}.{field}")


def _validate_dependencies(value: Any, task_ids: set[str]) -> None:
    rows = _require_list(value, "dependencies")
    edges: set[tuple[str, str]] = set()
    graph: dict[str, set[str]] = {}
    for index, dependency in enumerate(rows):
        path = f"dependencies[{index}]"
        if not isinstance(dependency, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(dependency, DEPENDENCY_FIELDS, path)
        task_id = _require_uuid(
            dependency["task_public_id"],
            f"{path}.task_public_id",
        )
        prerequisite_id = _require_uuid(
            dependency["prerequisite_task_public_id"],
            f"{path}.prerequisite_task_public_id",
        )
        if task_id not in task_ids or prerequisite_id not in task_ids:
            raise InvalidAccountExportError(f"{path} references a missing task.")
        if task_id == prerequisite_id:
            raise InvalidAccountExportError(f"{path} is a self-dependency.")
        edge = (task_id, prerequisite_id)
        if edge in edges:
            raise InvalidAccountExportError(f"{path} duplicates another dependency.")
        edges.add(edge)
        graph.setdefault(task_id, set()).add(prerequisite_id)
        _require_string(dependency["created_at"], f"{path}.created_at")
    for start in graph:
        pending = list(graph.get(start, ()))
        seen: set[str] = set()
        while pending:
            current = pending.pop()
            if current == start:
                raise InvalidAccountExportError("dependencies contain a cycle.")
            if current in seen:
                continue
            seen.add(current)
            pending.extend(graph.get(current, ()))


def _validate_waits(value: Any, task_ids: set[str]) -> None:
    rows = _require_list(value, "waits")
    seen: set[str] = set()
    waited_tasks: set[str] = set()
    for index, wait in enumerate(rows):
        path = f"waits[{index}]"
        if not isinstance(wait, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(wait, WAIT_FIELDS, path)
        public_id = _require_uuid(wait["public_id"], f"{path}.public_id")
        if public_id in seen:
            raise InvalidAccountExportError(f"{path}.public_id is duplicated.")
        seen.add(public_id)
        _require_uuid(
            wait["origin_installation_public_id"],
            f"{path}.origin_installation_public_id",
        )
        _require_revision(wait["revision"], f"{path}.revision")
        task_id = _require_uuid(wait["task_public_id"], f"{path}.task_public_id")
        if task_id not in task_ids or task_id in waited_tasks:
            raise InvalidAccountExportError(f"{path}.task_public_id is invalid.")
        waited_tasks.add(task_id)
        follow_up_id = wait["follow_up_task_public_id"]
        if follow_up_id is not None:
            follow_up_id = _require_uuid(
                follow_up_id,
                f"{path}.follow_up_task_public_id",
            )
            if follow_up_id not in task_ids:
                raise InvalidAccountExportError(
                    f"{path}.follow_up_task_public_id is missing."
                )
        for field in (
            "reason",
            "waiting_on",
            "resume_status",
            "created_at",
            "updated_at",
        ):
            _require_string(wait[field], f"{path}.{field}")
        if wait["resume_status"] not in {"inbox", "open"}:
            raise InvalidAccountExportError(
                f"{path}.resume_status is not supported."
            )
        if wait["review_date"] is not None:
            _require_string(wait["review_date"], f"{path}.review_date")


def _validate_remember_items(value: Any) -> None:
    rows = _require_list(value, "remember_items")
    if len(rows) > 3:
        raise InvalidAccountExportError(
            "remember_items exceeds the three-item limit."
        )
    seen: set[str] = set()
    for index, item in enumerate(rows):
        path = f"remember_items[{index}]"
        if not isinstance(item, dict):
            raise InvalidAccountExportError(f"{path} must be a JSON object.")
        _require_exact_fields(item, REMEMBER_ITEM_FIELDS, path)
        public_id = _require_uuid(item["public_id"], f"{path}.public_id")
        if public_id in seen:
            raise InvalidAccountExportError(f"{path}.public_id is duplicated.")
        seen.add(public_id)
        _require_uuid(
            item["origin_installation_public_id"],
            f"{path}.origin_installation_public_id",
        )
        _require_revision(item["revision"], f"{path}.revision")
        for field in ("title", "created_at", "updated_at"):
            _require_string(item[field], f"{path}.{field}")
        if not item["title"].strip() or len(item["title"]) > 100:
            raise InvalidAccountExportError(
                f"{path}.title must contain 1 to 100 characters."
            )


def import_account(
    connection: Connection,
    target_user_id: int,
    document: dict[str, Any],
) -> ImportResult:
    validate_account_export(document)
    task_rows = _normalized_tasks_for_import(document)
    project_rows = [dict(row) for row in document.get("projects", [])]
    component_rows = [dict(row) for row in document.get("components", [])]
    dependency_rows = [dict(row) for row in document.get("dependencies", [])]
    wait_rows = [dict(row) for row in document.get("waits", [])]
    remember_rows = [dict(row) for row in document.get("remember_items", [])]
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
            origins.update(
                row["origin_installation_public_id"]
                for row in project_rows + component_rows + wait_rows + remember_rows
            )
            origin_ids = _installation_ids(connection, origins)
            project_ids = _import_projects(
                connection,
                target_user_id,
                project_rows,
                origin_ids,
            )
            for task in task_rows:
                existing = existing_tasks.get(task["public_id"])
                values = _task_values(
                    task,
                    target_user_id,
                    origin_ids,
                    project_ids,
                )
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
            task_ids = _owned_public_ids(
                connection,
                tasks,
                target_user_id,
                [task["public_id"] for task in task_rows],
            )
            _import_components(
                connection,
                target_user_id,
                component_rows,
                origin_ids,
                task_ids,
            )
            _import_dependencies(
                connection,
                target_user_id,
                dependency_rows,
                task_ids,
            )
            _import_waits(
                connection,
                target_user_id,
                wait_rows,
                origin_ids,
                task_ids,
            )
            _import_remember_items(
                connection,
                target_user_id,
                remember_rows,
                origin_ids,
            )
            _assert_today_capacity(connection, target_user_id)
            _assert_remember_capacity(connection, target_user_id)
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
    version = document["format_version"]
    for task in task_rows:
        if version == 1:
            task["next_action"] = ""
            task["definition_of_done"] = ""
        if version < 3:
            state = task["state"]
            task["workflow_status"] = {
                "inbox": "inbox",
                "done": "done",
                "dropped": "dropped",
            }.get(state, "open")
            task["today_placement"] = {
                "active": "active",
                "ready": "overflow",
            }.get(state, "unplanned")
            task["project_public_id"] = None
            task["project_position"] = None
            task["dependency_override"] = False
        if version < 5:
            task["dropped_at"] = (
                task["updated_at"]
                if task["workflow_status"] == "dropped"
                else None
            )
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
            task["today_placement"] = "active"
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


def _assert_remember_capacity(connection: Connection, user_id: int) -> None:
    item_count = connection.execute(
        sa.select(sa.func.count())
        .select_from(remember_items)
        .where(remember_items.c.user_id == user_id)
    ).scalar_one()
    if item_count > 3:
        raise AccountImportConflictError(
            "The import would exceed the three-item Remember limit."
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
    project = projects.alias("existing_project")
    rows = (
        connection.execute(
            sa.select(
                tasks,
                origin.c.public_id.label("origin_installation_public_id"),
                project.c.public_id.label("project_public_id"),
            )
            .join(origin, tasks.c.origin_installation_id == origin.c.id)
            .outerjoin(project, tasks.c.project_id == project.c.id)
            .where(tasks.c.public_id.in_(public_ids))
        )
        .mappings()
        .all()
    )
    return {row["public_id"]: dict(row) for row in rows}


def _owned_public_ids(
    connection: Connection,
    table,
    user_id: int,
    public_ids: list[str],
) -> dict[str, int]:
    if not public_ids:
        return {}
    rows = connection.execute(
        sa.select(table.c.public_id, table.c.id).where(
            table.c.user_id == user_id,
            table.c.public_id.in_(public_ids),
        )
    ).all()
    result = {public_id: int(object_id) for public_id, object_id in rows}
    if set(result) != set(public_ids):
        raise AccountImportConflictError(
            f"Imported {table.name} relationships are incomplete."
        )
    return result


def _import_projects(
    connection: Connection,
    user_id: int,
    rows: list[dict[str, Any]],
    origin_ids: dict[str, int],
) -> dict[str, int]:
    public_ids = [row["public_id"] for row in rows]
    if not public_ids:
        return {}
    origin = installations.alias("import_project_origin")
    existing_rows = (
        connection.execute(
            sa.select(
                projects,
                origin.c.public_id.label("origin_installation_public_id"),
            )
            .join(origin, projects.c.origin_installation_id == origin.c.id)
            .where(projects.c.public_id.in_(public_ids))
        )
        .mappings()
        .all()
    )
    existing = {row["public_id"]: dict(row) for row in existing_rows}
    for row in rows:
        current = existing.get(row["public_id"])
        values = {
            "public_id": row["public_id"],
            "origin_installation_id": origin_ids[
                row["origin_installation_public_id"]
            ],
            "revision": row["revision"],
            "user_id": user_id,
            "title": row["title"],
            "desired_outcome": row["desired_outcome"],
            "notes": row["notes"],
            "state": row["state"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        if current is None:
            connection.execute(sa.insert(projects).values(**values))
        elif current["user_id"] != user_id:
            raise AccountImportConflictError(
                f"Project {row['public_id']} belongs to another local account."
            )
        elif row["revision"] > current["revision"]:
            connection.execute(
                sa.update(projects)
                .where(projects.c.id == current["id"])
                .values(**values)
            )
        elif row["revision"] == current["revision"]:
            for field in PROJECT_FIELDS:
                if current[field] != row[field]:
                    raise AccountImportConflictError(
                        f"Project {row['public_id']} has divergent content at "
                        f"revision {row['revision']}."
                    )
    return _owned_public_ids(connection, projects, user_id, public_ids)


def _import_components(
    connection: Connection,
    user_id: int,
    rows: list[dict[str, Any]],
    origin_ids: dict[str, int],
    task_ids: dict[str, int],
) -> None:
    if not rows:
        return
    public_ids = [row["public_id"] for row in rows]
    origin = installations.alias("import_component_origin")
    parent = tasks.alias("import_component_task")
    existing_rows = (
        connection.execute(
            sa.select(
                task_components,
                origin.c.public_id.label("origin_installation_public_id"),
                parent.c.public_id.label("task_public_id"),
            )
            .join(
                origin,
                task_components.c.origin_installation_id == origin.c.id,
            )
            .join(parent, task_components.c.task_id == parent.c.id)
            .where(task_components.c.public_id.in_(public_ids))
        )
        .mappings()
        .all()
    )
    existing = {row["public_id"]: dict(row) for row in existing_rows}
    for row in rows:
        current = existing.get(row["public_id"])
        values = {
            "public_id": row["public_id"],
            "origin_installation_id": origin_ids[
                row["origin_installation_public_id"]
            ],
            "revision": row["revision"],
            "user_id": user_id,
            "task_id": task_ids[row["task_public_id"]],
            "title": row["title"],
            "position": row["position"],
            "is_done": row["is_done"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        if current is None:
            connection.execute(sa.insert(task_components).values(**values))
        elif current["user_id"] != user_id:
            raise AccountImportConflictError(
                f"Component {row['public_id']} belongs to another local account."
            )
        elif row["revision"] > current["revision"]:
            connection.execute(
                sa.update(task_components)
                .where(task_components.c.id == current["id"])
                .values(**values)
            )
        elif row["revision"] == current["revision"]:
            for field in COMPONENT_FIELDS:
                if current[field] != row[field]:
                    raise AccountImportConflictError(
                        f"Component {row['public_id']} has divergent content."
                    )


def _import_dependencies(
    connection: Connection,
    user_id: int,
    rows: list[dict[str, Any]],
    task_ids: dict[str, int],
) -> None:
    for row in rows:
        task_id = task_ids[row["task_public_id"]]
        prerequisite_id = task_ids[row["prerequisite_task_public_id"]]
        exists = connection.execute(
            sa.select(task_dependencies.c.id).where(
                task_dependencies.c.user_id == user_id,
                task_dependencies.c.task_id == task_id,
                task_dependencies.c.prerequisite_task_id == prerequisite_id,
            )
        ).scalar_one_or_none()
        if exists is None:
            connection.execute(
                sa.insert(task_dependencies).values(
                    user_id=user_id,
                    task_id=task_id,
                    prerequisite_task_id=prerequisite_id,
                    created_at=row["created_at"],
                )
            )
    edges = connection.execute(
        sa.select(
            task_dependencies.c.task_id,
            task_dependencies.c.prerequisite_task_id,
        ).where(task_dependencies.c.user_id == user_id)
    ).all()
    graph: dict[int, set[int]] = {}
    for task_id, prerequisite_id in edges:
        graph.setdefault(task_id, set()).add(prerequisite_id)
    for start in graph:
        pending = list(graph[start])
        seen: set[int] = set()
        while pending:
            current = pending.pop()
            if current == start:
                raise AccountImportConflictError(
                    "The import would create a dependency cycle."
                )
            if current in seen:
                continue
            seen.add(current)
            pending.extend(graph.get(current, ()))


def _import_waits(
    connection: Connection,
    user_id: int,
    rows: list[dict[str, Any]],
    origin_ids: dict[str, int],
    task_ids: dict[str, int],
) -> None:
    if not rows:
        return
    public_ids = [row["public_id"] for row in rows]
    origin = installations.alias("import_wait_origin")
    waited = tasks.alias("import_wait_task")
    follow_up = tasks.alias("import_wait_follow_up")
    existing_rows = (
        connection.execute(
            sa.select(
                task_waits,
                origin.c.public_id.label("origin_installation_public_id"),
                waited.c.public_id.label("task_public_id"),
                follow_up.c.public_id.label("follow_up_task_public_id"),
            )
            .join(origin, task_waits.c.origin_installation_id == origin.c.id)
            .join(waited, task_waits.c.task_id == waited.c.id)
            .outerjoin(follow_up, task_waits.c.follow_up_task_id == follow_up.c.id)
            .where(task_waits.c.public_id.in_(public_ids))
        )
        .mappings()
        .all()
    )
    existing = {row["public_id"]: dict(row) for row in existing_rows}
    for row in rows:
        current = existing.get(row["public_id"])
        follow_up_public_id = row["follow_up_task_public_id"]
        values = {
            "public_id": row["public_id"],
            "origin_installation_id": origin_ids[
                row["origin_installation_public_id"]
            ],
            "revision": row["revision"],
            "user_id": user_id,
            "task_id": task_ids[row["task_public_id"]],
            "reason": row["reason"],
            "waiting_on": row["waiting_on"],
            "resume_status": row["resume_status"],
            "review_date": row["review_date"],
            "follow_up_task_id": (
                task_ids[follow_up_public_id]
                if follow_up_public_id is not None
                else None
            ),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        if current is None:
            connection.execute(sa.insert(task_waits).values(**values))
        elif current["user_id"] != user_id:
            raise AccountImportConflictError(
                f"Wait {row['public_id']} belongs to another local account."
            )
        elif row["revision"] > current["revision"]:
            connection.execute(
                sa.update(task_waits)
                .where(task_waits.c.id == current["id"])
                .values(**values)
            )
        elif row["revision"] == current["revision"]:
            for field in WAIT_FIELDS:
                if current[field] != row[field]:
                    raise AccountImportConflictError(
                        f"Wait {row['public_id']} has divergent content."
                    )


def _import_remember_items(
    connection: Connection,
    user_id: int,
    rows: list[dict[str, Any]],
    origin_ids: dict[str, int],
) -> None:
    if not rows:
        return
    public_ids = [row["public_id"] for row in rows]
    origin = installations.alias("import_remember_origin")
    existing_rows = (
        connection.execute(
            sa.select(
                remember_items,
                origin.c.public_id.label("origin_installation_public_id"),
            )
            .join(
                origin,
                remember_items.c.origin_installation_id == origin.c.id,
            )
            .where(remember_items.c.public_id.in_(public_ids))
        )
        .mappings()
        .all()
    )
    existing = {row["public_id"]: dict(row) for row in existing_rows}
    for row in rows:
        current = existing.get(row["public_id"])
        values = {
            "public_id": row["public_id"],
            "origin_installation_id": origin_ids[
                row["origin_installation_public_id"]
            ],
            "revision": row["revision"],
            "user_id": user_id,
            "title": row["title"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        if current is None:
            connection.execute(sa.insert(remember_items).values(**values))
        elif current["user_id"] != user_id:
            raise AccountImportConflictError(
                f"Remember item {row['public_id']} belongs to another local account."
            )
        elif row["revision"] > current["revision"]:
            connection.execute(
                sa.update(remember_items)
                .where(remember_items.c.id == current["id"])
                .values(**values)
            )
        elif row["revision"] == current["revision"]:
            for field in REMEMBER_ITEM_FIELDS:
                if current[field] != row[field]:
                    raise AccountImportConflictError(
                        f"Remember item {row['public_id']} has divergent content."
                    )


def _task_values(
    task: dict[str, Any],
    target_user_id: int,
    origin_ids: dict[str, int],
    project_ids: dict[str, int],
) -> dict[str, Any]:
    project_public_id = task["project_public_id"]
    return {
        "public_id": task["public_id"],
        "origin_installation_id": origin_ids[
            task["origin_installation_public_id"]
        ],
        "revision": task["revision"],
        "user_id": target_user_id,
        "title": task["title"],
        "notes": task["notes"],
        "next_action": task["next_action"],
        "definition_of_done": task["definition_of_done"],
        "state": task["state"],
        "planned_date": task["planned_date"],
        "is_highlight": task["is_highlight"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
        "completed_at": task["completed_at"],
        "dropped_at": task["dropped_at"],
        "project_id": (
            project_ids[project_public_id]
            if project_public_id is not None
            else None
        ),
        "project_position": task["project_position"],
        "workflow_status": task["workflow_status"],
        "today_placement": task["today_placement"],
        "dependency_override": task["dependency_override"],
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


def _require_nonnegative_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise InvalidAccountExportError(
            f"{path} must be a non-negative integer."
        )
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
