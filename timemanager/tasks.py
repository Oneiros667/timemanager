from __future__ import annotations

from datetime import date, datetime, timezone

import sqlalchemy as sa
from flask import (
    Blueprint,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from .auth import login_required
from .db import get_db, local_installation_id, new_public_id
from .models import (
    projects,
    remember_items,
    task_components,
    task_dependencies,
    task_waits,
    tasks as task_table,
)
from .planning import TODAY_OPTION_LIMIT

blueprint = Blueprint("tasks", __name__)


def _today() -> str:
    return date.today().isoformat()


def _owned_task(task_id: int):
    task = (
        get_db()
        .execute(
            sa.select(task_table).where(
                task_table.c.id == task_id,
                task_table.c.user_id == g.user["id"],
            )
        )
        .mappings()
        .one_or_none()
    )
    if task is None:
        abort(404)
    return task


def _active_option_count(
    database,
    user_id: int,
    *,
    exclude_task_id: int | None = None,
) -> int:
    query = (
        sa.select(sa.func.count())
        .select_from(task_table)
        .where(
            task_table.c.user_id == user_id,
            task_table.c.planned_date == _today(),
            task_table.c.workflow_status == "open",
            task_table.c.today_placement == "active",
            task_table.c.is_highlight.is_(False),
        )
    )
    if exclude_task_id is not None:
        query = query.where(task_table.c.id != exclude_task_id)
    return int(database.execute(query).scalar_one())


def _today_placement(database, user_id: int) -> str:
    if _active_option_count(database, user_id) < TODAY_OPTION_LIMIT:
        return "active"
    return "overflow"


def _legacy_state(workflow_status: str, today_placement: str) -> str:
    if workflow_status in ("inbox", "done", "dropped"):
        return workflow_status
    return "ready" if today_placement == "overflow" else "active"


def _task_state_values(workflow_status: str, today_placement: str) -> dict:
    return {
        "workflow_status": workflow_status,
        "today_placement": today_placement,
        "state": _legacy_state(workflow_status, today_placement),
    }


def _blocker_summary(database, task, *, honor_override: bool = True) -> str | None:
    if honor_override and task["dependency_override"]:
        return None
    wait_reason = database.execute(
        sa.select(task_waits.c.reason).where(
            task_waits.c.user_id == g.user["id"],
            task_waits.c.task_id == task["id"],
        )
    ).scalar_one_or_none()
    if wait_reason:
        return f"Waiting for: {wait_reason}"
    prerequisite = task_table.alias("prerequisite")
    title = database.execute(
        sa.select(prerequisite.c.title)
        .select_from(
            task_dependencies.join(
                prerequisite,
                task_dependencies.c.prerequisite_task_id == prerequisite.c.id,
            )
        )
        .where(
            task_dependencies.c.user_id == g.user["id"],
            task_dependencies.c.task_id == task["id"],
            prerequisite.c.workflow_status != "done",
        )
        .order_by(prerequisite.c.title)
        .limit(1)
    ).scalar_one_or_none()
    return f"Needs: {title}" if title else None


def _task_view(database, task) -> dict:
    result = dict(task)
    result["blocker_summary"] = _blocker_summary(database, task)
    result["saved_blocker_summary"] = _blocker_summary(
        database,
        task,
        honor_override=False,
    )
    result["project_title"] = (
        database.execute(
            sa.select(projects.c.title).where(
                projects.c.id == task["project_id"],
                projects.c.user_id == g.user["id"],
            )
        ).scalar_one_or_none()
        if task["project_id"] is not None
        else None
    )
    result["is_on_today"] = (
        task["planned_date"] == _today()
        and task["today_placement"] in ("active", "overflow")
    )
    result["can_add_to_today"] = (
        task["workflow_status"] in ("inbox", "open")
        and not result["is_on_today"]
        and result["blocker_summary"] is None
    )
    return result


def _later_view_clause():
    """Include captures plus otherwise undiscoverable non-project work."""
    not_on_current_today = sa.or_(
        task_table.c.planned_date.is_(None),
        task_table.c.planned_date != _today(),
        task_table.c.today_placement == "unplanned",
    )
    return sa.or_(
        task_table.c.workflow_status == "inbox",
        sa.and_(
            task_table.c.workflow_status.in_(("open", "waiting")),
            not_on_current_today,
        ),
    )


def _safe_return_path(value: str | None, fallback: str) -> str:
    if value and value.startswith("/") and not value.startswith("//"):
        return value
    return fallback


def _owned_project(project_id: int):
    project = (
        get_db()
        .execute(
            sa.select(projects).where(
                projects.c.id == project_id,
                projects.c.user_id == g.user["id"],
            )
        )
        .mappings()
        .one_or_none()
    )
    if project is None:
        abort(404)
    return project


def _owned_component(component_id: int):
    component = (
        get_db()
        .execute(
            sa.select(task_components).where(
                task_components.c.id == component_id,
                task_components.c.user_id == g.user["id"],
            )
        )
        .mappings()
        .one_or_none()
    )
    if component is None:
        abort(404)
    return component


@blueprint.get("/today")
@login_required
def today():
    database = get_db()
    today_value = _today()
    task_rows = (
        database.execute(
            sa.select(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.planned_date == today_value,
                task_table.c.workflow_status.in_(("open", "waiting")),
                task_table.c.today_placement.in_(("active", "overflow")),
            )
            .order_by(
                task_table.c.is_highlight.desc(),
                task_table.c.created_at,
                task_table.c.id,
            )
        )
        .mappings()
        .all()
    )
    completed = (
        database.execute(
            sa.select(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.planned_date == today_value,
                task_table.c.workflow_status == "done",
            )
            .order_by(task_table.c.completed_at.desc())
            .limit(5)
        )
        .mappings()
        .all()
    )
    later_count = database.execute(
        sa.select(sa.func.count())
        .select_from(task_table)
        .where(
            task_table.c.user_id == g.user["id"],
            _later_view_clause(),
        )
    ).scalar_one()
    remember_rows = (
        database.execute(
            sa.select(remember_items)
            .where(remember_items.c.user_id == g.user["id"])
            .order_by(remember_items.c.created_at, remember_items.c.id)
        )
        .mappings()
        .all()
    )
    task_rows = [_task_view(database, task) for task in task_rows]
    highlight = next((task for task in task_rows if task["is_highlight"]), None)
    optional_tasks = [
        task
        for task in task_rows
        if not task["is_highlight"] and task["today_placement"] == "active"
    ]
    overflow_tasks = [
        task
        for task in task_rows
        if not task["is_highlight"] and task["today_placement"] == "overflow"
    ]
    low_capacity_fallback = next(
        (
            task
            for task in optional_tasks
            if task["workflow_status"] == "open"
            and task["blocker_summary"] is None
        ),
        None,
    )
    low_capacity_task = highlight or low_capacity_fallback
    low_capacity_hidden_count = len(task_rows) - int(low_capacity_task is not None)

    return render_template(
        "today.html",
        today_label=date.today().strftime("%A, %d %B"),
        highlight=highlight,
        optional_tasks=optional_tasks,
        option_limit=TODAY_OPTION_LIMIT,
        overflow_tasks=overflow_tasks,
        completed=completed,
        low_capacity_task=low_capacity_task,
        low_capacity_hidden_count=low_capacity_hidden_count,
        later_count=later_count,
        remember_items=remember_rows,
    )


@blueprint.get("/later")
@login_required
def later():
    database = get_db()
    task_rows = (
        database.execute(
            sa.select(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                _later_view_clause(),
            )
            .order_by(task_table.c.created_at.desc())
        )
        .mappings()
        .all()
    )
    task_views = [_task_view(database, task) for task in task_rows]
    return render_template(
        "later.html",
        captured_tasks=[
            task for task in task_views if task["workflow_status"] == "inbox"
        ],
        ready_or_waiting_tasks=[
            task for task in task_views if task["workflow_status"] != "inbox"
        ],
    )


@blueprint.get("/recently-dropped")
@login_required
def recently_dropped():
    database = get_db()
    just_dropped_id = request.args.get("dropped", type=int)
    rows = (
        database.execute(
            sa.select(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.workflow_status == "dropped",
                task_table.c.dropped_at.is_not(None),
            )
            .order_by(
                task_table.c.dropped_at.desc(),
                task_table.c.id.desc(),
            )
            .limit(10)
        )
        .mappings()
        .all()
    )
    task_views = []
    for row in rows:
        task = _task_view(database, row)
        task["can_restore_to_today"] = task["blocker_summary"] is None
        task_views.append(task)
    just_dropped = next(
        (task for task in task_views if task["id"] == just_dropped_id),
        None,
    )
    if just_dropped_id is not None and just_dropped is None:
        just_dropped_row = (
            database.execute(
                sa.select(task_table).where(
                    task_table.c.id == just_dropped_id,
                    task_table.c.user_id == g.user["id"],
                    task_table.c.workflow_status == "dropped",
                    task_table.c.dropped_at.is_not(None),
                )
            )
            .mappings()
            .one_or_none()
        )
        if just_dropped_row is not None:
            just_dropped = _task_view(database, just_dropped_row)
    return render_template(
        "recently_dropped.html",
        dropped_tasks=task_views,
        just_dropped=just_dropped,
    )


@blueprint.post("/tasks")
@login_required
def create_task():
    title = " ".join(request.form.get("title", "").split())
    placement = request.form.get("placement", "today")
    if placement not in ("today", "later"):
        abort(400)
    destination = "tasks.later" if placement == "later" else "tasks.today"

    if not title:
        flash("Add a few words so the thought has somewhere to land.", "error")
        return redirect(url_for(destination))
    if len(title) > 180:
        flash("Keep the capture under 180 characters. Details can come later.", "error")
        return redirect(url_for(destination))

    database = get_db()
    today_placement = "unplanned" if placement == "later" else _today_placement(
        database,
        g.user["id"],
    )
    workflow_status = "inbox" if placement == "later" else "open"
    planned_date = None if placement == "later" else _today()
    task_id = database.execute(
        sa.insert(task_table).values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            title=title,
            **_task_state_values(workflow_status, today_placement),
            planned_date=planned_date,
        )
        .returning(task_table.c.id)
    ).scalar_one()
    database.commit()
    if today_placement == "overflow":
        flash(
            "Captured in Today overflow. Your three active options stay small.",
            "success",
        )
    else:
        flash("Captured. You can keep moving.", "success")
    return redirect(url_for(destination, created=task_id))


@blueprint.post("/tasks/<int:task_id>/today")
@login_required
def move_to_today(task_id: int):
    task = _owned_task(task_id)
    database = get_db()
    task_view = _task_view(database, task)
    if not task_view["can_add_to_today"]:
        abort(400)
    placement = _today_placement(database, g.user["id"])
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            **_task_state_values("open", placement),
            planned_date=_today(),
            is_highlight=False,
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    if placement == "overflow":
        flash(
            "Added to Today overflow. Choose what should enter the active plan.",
            "success",
        )
    else:
        flash("Added to today.", "success")
    return redirect(url_for("tasks.today"))


@blueprint.post("/tasks/<int:task_id>/activate")
@login_required
def activate_task(task_id: int):
    task = _owned_task(task_id)
    if (
        task["planned_date"] != _today()
        or task["workflow_status"] not in ("open", "waiting")
        or task["today_placement"] != "overflow"
        or task["is_highlight"]
    ):
        abort(400)

    database = get_db()
    if _active_option_count(database, g.user["id"]) >= TODAY_OPTION_LIMIT:
        flash(
            "Today already has three active options. Save one for later first.",
            "error",
        )
        return redirect(url_for("tasks.today"))

    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            **_task_state_values(task["workflow_status"], "active"),
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("Moved into your active Today plan.", "success")
    return redirect(url_for("tasks.today"))


@blueprint.post("/tasks/<int:task_id>/later")
@login_required
def move_to_later(task_id: int):
    task = _owned_task(task_id)
    if (
        task["planned_date"] != _today()
        or task["today_placement"] not in ("active", "overflow")
    ):
        abort(400)

    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            **_task_state_values(task["workflow_status"], "unplanned"),
            planned_date=None,
            is_highlight=False,
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash(f"Moved “{task['title']}” outside Today.", "success")
    return redirect(url_for("tasks.later"))


@blueprint.post("/tasks/<int:task_id>/highlight")
@login_required
def choose_highlight(task_id: int):
    task = _owned_task(task_id)
    if (
        task["planned_date"] != _today()
        or task["today_placement"] not in ("active", "overflow")
    ):
        abort(400)

    database = get_db()
    old_highlight = (
        database.execute(
            sa.select(task_table).where(
                task_table.c.user_id == g.user["id"],
                task_table.c.planned_date == _today(),
                task_table.c.is_highlight.is_(True),
                task_table.c.id != task_id,
                task_table.c.workflow_status.in_(("open", "waiting")),
                task_table.c.today_placement.in_(("active", "overflow")),
            )
        )
        .mappings()
        .one_or_none()
    )
    if old_highlight is not None:
        active_options = _active_option_count(
            database,
            g.user["id"],
            exclude_task_id=task_id,
        )
        old_placement = (
            "active" if active_options < TODAY_OPTION_LIMIT else "overflow"
        )
        database.execute(
            sa.update(task_table)
            .where(task_table.c.id == old_highlight["id"])
            .values(
                is_highlight=False,
                **_task_state_values(
                    old_highlight["workflow_status"],
                    old_placement,
                ),
                updated_at=sa.func.current_timestamp(),
                revision=task_table.c.revision + 1,
            )
        )
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            is_highlight=True,
            **_task_state_values(task["workflow_status"], "active"),
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("Highlight chosen. One meaningful win is enough.", "success")
    return redirect(url_for("tasks.today"))


@blueprint.post("/tasks/<int:task_id>/toggle")
@login_required
def toggle_task(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    database = get_db()
    if task["workflow_status"] == "done":
        restored_placement = _today_placement(database, g.user["id"])
        database.execute(
            sa.update(task_table)
            .where(
                task_table.c.id == task_id,
                task_table.c.user_id == g.user["id"],
            )
            .values(
                **_task_state_values("open", restored_placement),
                completed_at=None,
                updated_at=sa.func.current_timestamp(),
                revision=task_table.c.revision + 1,
            )
        )
        if restored_placement == "overflow":
            flash(
                "Restored to Today overflow. Your active plan remains at three.",
                "success",
            )
        else:
            flash("Restored to today.", "success")
    elif task["workflow_status"] not in ("dropped", "inbox"):
        unfinished = database.execute(
            sa.select(sa.func.count())
            .select_from(task_components)
            .where(
                task_components.c.user_id == g.user["id"],
                task_components.c.task_id == task_id,
                task_components.c.is_done.is_(False),
            )
        ).scalar_one()
        if unfinished and request.form.get("confirm_unfinished") != "1":
            flash(
                "This task still has unfinished steps. Confirm completion here.",
                "error",
            )
            return redirect(
                url_for(
                    "tasks.task_detail",
                    task_id=task_id,
                    confirm_completion="1",
                )
            )
        database.execute(
            sa.update(task_table)
            .where(
                task_table.c.id == task_id,
                task_table.c.user_id == g.user["id"],
            )
            .values(
                **_task_state_values("done", task["today_placement"]),
                is_highlight=False,
                completed_at=datetime.now().isoformat(timespec="seconds"),
                updated_at=sa.func.current_timestamp(),
                revision=task_table.c.revision + 1,
            )
        )
        flash("Done. Take a breath before the next thing.", "success")
    else:
        abort(400)
    database.commit()
    return redirect(url_for("tasks.today"))


@blueprint.route("/tasks/<int:task_id>/drop", methods=("GET", "POST"))
@login_required
def drop_task(task_id: int):
    task = _owned_task(task_id)
    fallback = (
        url_for("tasks.today")
        if task["planned_date"] == _today()
        and task["today_placement"] in ("active", "overflow")
        else url_for("tasks.later")
    )
    return_to = _safe_return_path(
        request.values.get("return_to"),
        fallback,
    )
    if task["workflow_status"] == "dropped":
        flash(f"“{task['title']}” is already in Recently dropped.", "success")
        return redirect(url_for("tasks.recently_dropped"))
    if request.method == "GET":
        return render_template(
            "drop_task.html",
            task=task,
            return_to=return_to,
            confirmation_error=None,
        )

    _require_current_revision(task)
    if request.form.get("confirm_title", "").strip() != task["title"]:
        return (
            render_template(
                "drop_task.html",
                task=task,
                return_to=return_to,
                confirmation_error="Type the task title exactly to confirm.",
            ),
            400,
        )

    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            **_task_state_values("dropped", task["today_placement"]),
            is_highlight=False,
            dropped_at=(
                datetime.now(timezone.utc)
                .isoformat(timespec="seconds")
                .replace("+00:00", "Z")
            ),
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash(
        f"Moved “{task['title']}” to Recently dropped. You can undo below.",
        "success",
    )
    return redirect(
        url_for(
            "tasks.recently_dropped",
            dropped=task_id,
        )
    )


@blueprint.post("/tasks/<int:task_id>/restore")
@login_required
def restore_dropped_task(task_id: int):
    task = _owned_task(task_id)
    if task["workflow_status"] != "dropped":
        abort(400)
    _require_current_revision(task)
    destination = request.form.get("destination", "later")
    if destination not in ("later", "today"):
        abort(400)

    database = get_db()
    if destination == "today" and _blocker_summary(database, task) is not None:
        abort(400)
    placement = (
        _today_placement(database, g.user["id"])
        if destination == "today"
        else "unplanned"
    )
    planned_date = _today() if destination == "today" else None
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            **_task_state_values("open", placement),
            planned_date=planned_date,
            is_highlight=False,
            completed_at=None,
            dropped_at=None,
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    if destination == "today":
        if placement == "overflow":
            flash(
                f"Restored “{task['title']}” to Today overflow.",
                "success",
            )
        else:
            flash(f"Restored “{task['title']}” to Today.", "success")
        return redirect(url_for("tasks.today"))
    flash(f"Restored “{task['title']}” to Later.", "success")
    return redirect(url_for("tasks.later"))


def _wants_json() -> bool:
    return (
        request.headers.get("X-Requested-With") == "fetch"
        or request.accept_mimetypes.best == "application/json"
    )


def _clean_field(name: str, limit: int, *, required: bool = False) -> str:
    value = request.form.get(name, "").strip()
    if required and not value:
        abort(400, description=f"{name.replace('_', ' ').title()} is required.")
    if len(value) > limit:
        abort(400, description=f"{name.replace('_', ' ').title()} is too long.")
    return value


def _revision_conflict(record) -> bool:
    try:
        submitted = int(request.form.get("revision", "0"))
    except ValueError:
        submitted = 0
    return submitted != record["revision"]


def _require_current_revision(record, field: str = "revision") -> None:
    """Reject stale UI mutations while tolerating older non-workspace callers."""
    if field not in request.form:
        return
    try:
        submitted = int(request.form[field])
    except ValueError:
        submitted = 0
    if submitted != record["revision"]:
        abort(
            409,
            description=(
                f"Saved version changed. Current saved value: "
                f"{record.get('title', 'revision')} "
                f"(revision {record['revision']})."
            ),
        )


def _save_response(record, destination: str):
    if _wants_json():
        return jsonify(
            {
                "status": "saved",
                "revision": record["revision"] + 1,
            }
        )
    flash("Saved.", "success")
    return redirect(destination)


@blueprint.get("/tasks/<int:task_id>")
@login_required
def task_detail(task_id: int):
    task = _owned_task(task_id)
    database = get_db()
    components = (
        database.execute(
            sa.select(task_components)
            .where(
                task_components.c.user_id == g.user["id"],
                task_components.c.task_id == task_id,
            )
            .order_by(task_components.c.position)
        )
        .mappings()
        .all()
    )
    project = None
    if task["project_id"] is not None:
        project = _owned_project(task["project_id"])
    prerequisite = task_table.alias("prerequisite")
    prerequisites = (
        database.execute(
            sa.select(prerequisite.c.id, prerequisite.c.title, prerequisite.c.workflow_status)
            .select_from(
                task_dependencies.join(
                    prerequisite,
                    task_dependencies.c.prerequisite_task_id == prerequisite.c.id,
                )
            )
            .where(
                task_dependencies.c.user_id == g.user["id"],
                task_dependencies.c.task_id == task_id,
            )
            .order_by(prerequisite.c.title)
        )
        .mappings()
        .all()
    )
    wait = (
        database.execute(
            sa.select(task_waits).where(
                task_waits.c.user_id == g.user["id"],
                task_waits.c.task_id == task_id,
            )
        )
        .mappings()
        .one_or_none()
    )
    candidate_tasks = (
        database.execute(
            sa.select(task_table.c.id, task_table.c.title)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.id != task_id,
                task_table.c.workflow_status.in_(("inbox", "open", "waiting")),
            )
            .order_by(task_table.c.title)
        )
        .mappings()
        .all()
    )
    candidate_projects = (
        database.execute(
            sa.select(projects.c.id, projects.c.title)
            .where(
                projects.c.user_id == g.user["id"],
                projects.c.state == "active",
            )
            .order_by(projects.c.title)
        )
        .mappings()
        .all()
    )
    return render_template(
        "task_detail.html",
        task=_task_view(database, task),
        components=components,
        project=project,
        prerequisites=prerequisites,
        wait=wait,
        candidate_tasks=candidate_tasks,
        candidate_projects=candidate_projects,
        return_to=request.args.get("return_to", url_for("tasks.today")),
    )


@blueprint.post("/tasks/<int:task_id>/details")
@login_required
def update_task_details(task_id: int):
    task = _owned_task(task_id)
    if _revision_conflict(task):
        return (
            jsonify(
                {
                    "status": "conflict",
                    "revision": task["revision"],
                    "current": {
                        "title": task["title"],
                        "next_action": task["next_action"],
                        "definition_of_done": task["definition_of_done"],
                        "notes": task["notes"],
                    },
                }
            ),
            409,
        )
    values = {
        "title": _clean_field("title", 180, required=True),
        "next_action": _clean_field("next_action", 500),
        "definition_of_done": _clean_field("definition_of_done", 1000),
        "notes": _clean_field("notes", 4000),
        "updated_at": sa.func.current_timestamp(),
        "revision": task_table.c.revision + 1,
    }
    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
            task_table.c.revision == task["revision"],
        )
        .values(**values)
    )
    database.commit()
    return _save_response(task, url_for("tasks.task_detail", task_id=task_id))


@blueprint.post("/tasks/<int:task_id>/components")
@login_required
def add_component(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    title = _clean_field("title", 180, required=True)
    database = get_db()
    position = database.execute(
        sa.select(sa.func.coalesce(sa.func.max(task_components.c.position), -1) + 1)
        .where(
            task_components.c.user_id == g.user["id"],
            task_components.c.task_id == task_id,
        )
    ).scalar_one()
    component_id = database.execute(
        sa.insert(task_components).values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            task_id=task_id,
            title=title,
            position=position,
        ).returning(task_components.c.id)
    ).scalar_one()
    database.execute(
        sa.update(task_table)
        .where(task_table.c.id == task_id, task_table.c.user_id == g.user["id"])
        .values(
            revision=task_table.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    if _wants_json():
        component = (
            database.execute(
                sa.select(task_components).where(
                    task_components.c.id == component_id,
                    task_components.c.user_id == g.user["id"],
                )
            )
            .mappings()
            .one()
        )
        project = (
            _owned_project(task["project_id"])
            if task["project_id"] is not None
            else None
        )
        task_for_render = dict(task)
        task_for_render["revision"] += 1
        return (
            jsonify(
                {
                    "status": "added",
                    "title": title,
                    "task_revision": task["revision"] + 1,
                    "html": render_template(
                        "_component_row.html",
                        component=component,
                        task=task_for_render,
                        project=project,
                        is_first=position == 0,
                    ),
                }
            ),
            201,
        )
    return redirect(url_for("tasks.task_detail", task_id=task_id))


@blueprint.post("/components/<int:component_id>/toggle")
@login_required
def toggle_component(component_id: int):
    component = _owned_component(component_id)
    _require_current_revision(component)
    database = get_db()
    database.execute(
        sa.update(task_components)
        .where(
            task_components.c.id == component_id,
            task_components.c.user_id == g.user["id"],
        )
        .values(
            is_done=not component["is_done"],
            revision=task_components.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    return redirect(url_for("tasks.task_detail", task_id=component["task_id"]))


@blueprint.post("/components/<int:component_id>/details")
@login_required
def update_component(component_id: int):
    component = _owned_component(component_id)
    if _revision_conflict(component):
        return (
            jsonify(
                {
                    "status": "conflict",
                    "revision": component["revision"],
                    "current": {"title": component["title"]},
                }
            ),
            409,
        )
    database = get_db()
    database.execute(
        sa.update(task_components)
        .where(
            task_components.c.id == component_id,
            task_components.c.user_id == g.user["id"],
            task_components.c.revision == component["revision"],
        )
        .values(
            title=_clean_field("title", 180, required=True),
            revision=task_components.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    return _save_response(
        component,
        url_for("tasks.task_detail", task_id=component["task_id"]),
    )


@blueprint.post("/components/<int:component_id>/move")
@login_required
def move_component(component_id: int):
    component = _owned_component(component_id)
    _require_current_revision(component)
    direction = request.form.get("direction")
    if direction not in ("up", "down"):
        abort(400)
    target_position = component["position"] + (-1 if direction == "up" else 1)
    database = get_db()
    other = (
        database.execute(
            sa.select(task_components).where(
                task_components.c.user_id == g.user["id"],
                task_components.c.task_id == component["task_id"],
                task_components.c.position == target_position,
            )
        )
        .mappings()
        .one_or_none()
    )
    if other is not None:
        temporary = database.execute(
            sa.select(sa.func.max(task_components.c.position) + 1).where(
                task_components.c.task_id == component["task_id"]
            )
        ).scalar_one()
        with database.begin_nested():
            database.execute(
                sa.update(task_components)
                .where(task_components.c.id == component_id)
                .values(position=temporary)
            )
            database.execute(
                sa.update(task_components)
                .where(task_components.c.id == other["id"])
                .values(
                    position=component["position"],
                    revision=task_components.c.revision + 1,
                )
            )
            database.execute(
                sa.update(task_components)
                .where(task_components.c.id == component_id)
                .values(
                    position=target_position,
                    revision=task_components.c.revision + 1,
                )
            )
        database.commit()
    return redirect(url_for("tasks.task_detail", task_id=component["task_id"]))


def _next_project_position(database, project_id: int) -> int:
    return int(
        database.execute(
            sa.select(sa.func.coalesce(sa.func.max(task_table.c.project_position), -1) + 1)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.project_id == project_id,
            )
        ).scalar_one()
    )


@blueprint.post("/tasks/<int:task_id>/project")
@login_required
def set_task_project(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    database = get_db()
    choice = request.form.get("project_id", "")
    if choice:
        try:
            project_id = int(choice)
        except ValueError:
            abort(400)
        _owned_project(project_id)
    else:
        project_id = None
    position = (
        _next_project_position(database, project_id)
        if project_id is not None
        else None
    )
    database.execute(
        sa.update(task_table)
        .where(task_table.c.id == task_id, task_table.c.user_id == g.user["id"])
        .values(
            project_id=project_id,
            project_position=position,
            revision=task_table.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    flash("Project updated.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task["id"]))


@blueprint.post("/tasks/<int:task_id>/promote-to-project")
@login_required
def promote_task_to_project(task_id: int):
    task = _owned_task(task_id)
    if "revision" not in request.form:
        abort(400, description="Current task revision is required.")
    _require_current_revision(task)
    if task["project_id"] is not None:
        abort(409, description="This task already belongs to a project.")
    if request.form.get("confirm") != "1":
        abort(400, description="Project conversion requires confirmation.")

    project_title = _clean_field("project_title", 180, required=True)
    database = get_db()
    project_id = database.execute(
        sa.insert(projects)
        .values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            title=project_title,
            desired_outcome=task["definition_of_done"],
        )
        .returning(projects.c.id)
    ).scalar_one()
    updated_task_id = database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
            task_table.c.revision == task["revision"],
        )
        .values(
            project_id=project_id,
            project_position=0,
            revision=task_table.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
        .returning(task_table.c.id)
    ).scalar_one_or_none()
    if updated_task_id is None:
        database.rollback()
        abort(409, description="The task changed while creating the project.")
    database.commit()
    flash("Project created. The original task is its first task.", "success")
    return redirect(url_for("tasks.project_detail", project_id=project_id))


@blueprint.post("/components/<int:component_id>/promote")
@login_required
def promote_component(component_id: int):
    component = _owned_component(component_id)
    task = _owned_task(component["task_id"])
    _require_current_revision(component)
    _require_current_revision(task, "task_revision")
    if request.form.get("confirm") != "1":
        abort(400)
    database = get_db()
    project_id = task["project_id"]
    parent_position = task["project_position"]
    if project_id is None:
        project_id = database.execute(
            sa.insert(projects)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=g.user["id"],
                title=task["title"],
                desired_outcome=task["definition_of_done"],
            )
            .returning(projects.c.id)
        ).scalar_one()
        database.execute(
            sa.update(task_table)
            .where(task_table.c.id == task["id"])
            .values(
                project_id=project_id,
                project_position=0,
                revision=task_table.c.revision + 1,
            )
        )
        parent_position = 0
    insertion_position = int(parent_position or 0) + component["position"] + 1
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.user_id == g.user["id"],
            task_table.c.project_id == project_id,
            task_table.c.project_position >= insertion_position,
        )
        .values(project_position=task_table.c.project_position + 1)
    )
    database.execute(
        sa.insert(task_table).values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            title=component["title"],
            project_id=project_id,
            project_position=insertion_position,
            **_task_state_values("inbox", "unplanned"),
        )
    )
    database.execute(
        sa.delete(task_components).where(task_components.c.id == component_id)
    )
    database.commit()
    flash("Step turned into a project task.", "success")
    return redirect(url_for("tasks.project_detail", project_id=project_id))


def _dependency_would_cycle(database, task_id: int, prerequisite_id: int) -> bool:
    edges = database.execute(
        sa.select(
            task_dependencies.c.task_id,
            task_dependencies.c.prerequisite_task_id,
        ).where(task_dependencies.c.user_id == g.user["id"])
    ).all()
    prerequisites_by_task: dict[int, set[int]] = {}
    for dependent, prerequisite in edges:
        prerequisites_by_task.setdefault(dependent, set()).add(prerequisite)
    prerequisites_by_task.setdefault(task_id, set()).add(prerequisite_id)
    pending = [prerequisite_id]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        if current == task_id:
            return True
        if current in seen:
            continue
        seen.add(current)
        pending.extend(prerequisites_by_task.get(current, ()))
    return False


@blueprint.post("/tasks/<int:task_id>/dependencies")
@login_required
def add_dependency(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    try:
        prerequisite_id = int(request.form.get("prerequisite_task_id", ""))
    except ValueError:
        abort(400)
    _owned_task(prerequisite_id)
    database = get_db()
    if _dependency_would_cycle(database, task_id, prerequisite_id):
        flash("That would create a circular dependency.", "error")
        return redirect(url_for("tasks.task_detail", task_id=task_id))
    try:
        database.execute(
            sa.insert(task_dependencies).values(
                user_id=g.user["id"],
                task_id=task_id,
                prerequisite_task_id=prerequisite_id,
            )
        )
        database.execute(
            sa.update(task_table)
            .where(task_table.c.id == task_id)
            .values(
                dependency_override=False,
                revision=task_table.c.revision + 1,
            )
        )
        database.commit()
    except sa.exc.IntegrityError:
        database.rollback()
        flash("That prerequisite is already linked.", "error")
    else:
        flash("Blocker added. Today was not rearranged.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task["id"]))


@blueprint.post("/tasks/<int:task_id>/dependencies/<int:prerequisite_id>/remove")
@login_required
def remove_dependency(task_id: int, prerequisite_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    _owned_task(prerequisite_id)
    database = get_db()
    database.execute(
        sa.delete(task_dependencies).where(
            task_dependencies.c.user_id == g.user["id"],
            task_dependencies.c.task_id == task_id,
            task_dependencies.c.prerequisite_task_id == prerequisite_id,
        )
    )
    database.execute(
        sa.update(task_table)
        .where(task_table.c.id == task_id, task_table.c.user_id == g.user["id"])
        .values(revision=task_table.c.revision + 1)
    )
    database.commit()
    flash("Blocker removed. The task was not added to Today.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task_id))


@blueprint.post("/tasks/<int:task_id>/wait")
@login_required
def set_wait(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    reason = _clean_field("reason", 500, required=True)
    waiting_on = _clean_field("waiting_on", 180)
    follow_up_title = _clean_field("follow_up_title", 180)
    review_date = request.form.get("review_date") or None
    if review_date:
        try:
            date.fromisoformat(review_date)
        except ValueError:
            abort(400, description="Review date must be a valid date.")
    database = get_db()
    follow_up_task_id = None
    if follow_up_title:
        project_position = (
            _next_project_position(database, task["project_id"])
            if task["project_id"] is not None
            else None
        )
        follow_up_task_id = database.execute(
            sa.insert(task_table)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=g.user["id"],
                title=follow_up_title,
                project_id=task["project_id"],
                project_position=project_position,
                **_task_state_values("inbox", "unplanned"),
            )
            .returning(task_table.c.id)
        ).scalar_one()
    existing = database.execute(
        sa.select(task_waits.c.id).where(
            task_waits.c.user_id == g.user["id"],
            task_waits.c.task_id == task_id,
        )
    ).scalar_one_or_none()
    if existing is None:
        database.execute(
            sa.insert(task_waits).values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=g.user["id"],
                task_id=task_id,
                reason=reason,
                waiting_on=waiting_on,
                resume_status=(
                    task["workflow_status"]
                    if task["workflow_status"] in ("inbox", "open")
                    else "open"
                ),
                review_date=review_date,
                follow_up_task_id=follow_up_task_id,
            )
        )
    else:
        database.execute(
            sa.update(task_waits)
            .where(task_waits.c.id == existing)
            .values(
                reason=reason,
                waiting_on=waiting_on,
                review_date=review_date,
                **(
                    {"follow_up_task_id": follow_up_task_id}
                    if follow_up_task_id is not None
                    else {}
                ),
                revision=task_waits.c.revision + 1,
                updated_at=sa.func.current_timestamp(),
            )
        )
    database.execute(
        sa.update(task_table)
        .where(task_table.c.id == task_id)
        .values(
            **_task_state_values("waiting", task["today_placement"]),
            dependency_override=False,
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("Waiting recorded. Today was not rearranged.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task_id))


@blueprint.post("/tasks/<int:task_id>/wait/remove")
@login_required
def remove_wait(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    database = get_db()
    wait = (
        database.execute(
            sa.select(task_waits.c.resume_status).where(
                task_waits.c.user_id == g.user["id"],
                task_waits.c.task_id == task_id,
            )
        ).scalar_one_or_none()
        or "open"
    )
    database.execute(
        sa.delete(task_waits).where(
            task_waits.c.user_id == g.user["id"],
            task_waits.c.task_id == task_id,
        )
    )
    database.execute(
        sa.update(task_table)
        .where(task_table.c.id == task_id)
        .values(
            **_task_state_values(wait, task["today_placement"]),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("Waiting removed. The task was not added to Today.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task_id))


@blueprint.post("/tasks/<int:task_id>/override")
@login_required
def override_blockers(task_id: int):
    task = _owned_task(task_id)
    _require_current_revision(task)
    if request.form.get("confirm") != "1":
        abort(400)
    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(task_table.c.id == task_id)
        .values(
            dependency_override=True,
            **_task_state_values("open", task["today_placement"]),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("This task can start anyway. It was not added to Today.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task_id))


def _project_task_groups(database, project_id: int) -> dict[str, list[dict]]:
    rows = (
        database.execute(
            sa.select(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.project_id == project_id,
            )
            .order_by(task_table.c.project_position, task_table.c.created_at)
        )
        .mappings()
        .all()
    )
    groups = {"ready": [], "waiting": [], "done": []}
    for row in rows:
        task = _task_view(database, row)
        if row["workflow_status"] == "done":
            groups["done"].append(task)
        elif task["blocker_summary"] or row["workflow_status"] == "waiting":
            groups["waiting"].append(task)
        elif row["workflow_status"] != "dropped":
            groups["ready"].append(task)
    return groups


@blueprint.get("/projects/<int:project_id>")
@login_required
def project_detail(project_id: int):
    project = _owned_project(project_id)
    groups = _project_task_groups(get_db(), project_id)
    return render_template(
        "project_detail.html",
        project=project,
        groups=groups,
        next_ready=groups["ready"][0] if groups["ready"] else None,
    )


@blueprint.post("/projects/<int:project_id>/details")
@login_required
def update_project_details(project_id: int):
    project = _owned_project(project_id)
    if _revision_conflict(project):
        return (
            jsonify(
                {
                    "status": "conflict",
                    "revision": project["revision"],
                    "current": {
                        "title": project["title"],
                        "desired_outcome": project["desired_outcome"],
                        "notes": project["notes"],
                    },
                }
            ),
            409,
        )
    database = get_db()
    database.execute(
        sa.update(projects)
        .where(
            projects.c.id == project_id,
            projects.c.user_id == g.user["id"],
            projects.c.revision == project["revision"],
        )
        .values(
            title=_clean_field("title", 180, required=True),
            desired_outcome=_clean_field("desired_outcome", 1000),
            notes=_clean_field("notes", 4000),
            revision=projects.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    return _save_response(
        project,
        url_for("tasks.project_detail", project_id=project_id),
    )


@blueprint.post("/projects/<int:project_id>/tasks")
@login_required
def add_project_task(project_id: int):
    project = _owned_project(project_id)
    _require_current_revision(project)
    title = _clean_field("title", 180, required=True)
    database = get_db()
    task_id = database.execute(
        sa.insert(task_table)
        .values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            title=title,
            project_id=project_id,
            project_position=_next_project_position(database, project_id),
            **_task_state_values("open", "unplanned"),
        )
        .returning(task_table.c.id)
    ).scalar_one()
    database.execute(
        sa.update(projects)
        .where(projects.c.id == project_id, projects.c.user_id == g.user["id"])
        .values(
            revision=projects.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    if _wants_json():
        return (
            jsonify(
                {
                    "status": "added",
                    "id": task_id,
                    "title": title,
                    "project_revision": project["revision"] + 1,
                }
            ),
            201,
        )
    return redirect(url_for("tasks.project_detail", project_id=project_id))


@blueprint.post("/projects/<int:project_id>/tasks/<int:task_id>/move")
@login_required
def move_project_task(project_id: int, task_id: int):
    project = _owned_project(project_id)
    _require_current_revision(project)
    task = _owned_task(task_id)
    if task["project_id"] != project_id:
        abort(404)
    direction = request.form.get("direction")
    if direction not in ("up", "down"):
        abort(400)
    target_position = task["project_position"] + (-1 if direction == "up" else 1)
    database = get_db()
    other = (
        database.execute(
            sa.select(task_table).where(
                task_table.c.user_id == g.user["id"],
                task_table.c.project_id == project_id,
                task_table.c.project_position == target_position,
            )
        )
        .mappings()
        .one_or_none()
    )
    if other is not None:
        temporary = database.execute(
            sa.select(sa.func.max(task_table.c.project_position) + 1).where(
                task_table.c.user_id == g.user["id"],
                task_table.c.project_id == project_id,
            )
        ).scalar_one()
        with database.begin_nested():
            database.execute(
                sa.update(task_table)
                .where(task_table.c.id == task_id)
                .values(project_position=temporary)
            )
            database.execute(
                sa.update(task_table)
                .where(task_table.c.id == other["id"])
                .values(project_position=task["project_position"])
            )
            database.execute(
                sa.update(task_table)
                .where(task_table.c.id == task_id)
                .values(project_position=target_position)
            )
            database.execute(
                sa.update(projects)
                .where(projects.c.id == project_id)
                .values(
                    revision=projects.c.revision + 1,
                    updated_at=sa.func.current_timestamp(),
                )
            )
        database.commit()
    return redirect(url_for("tasks.project_detail", project_id=project_id))


@blueprint.post("/projects/<int:project_id>/state")
@login_required
def set_project_state(project_id: int):
    project = _owned_project(project_id)
    _require_current_revision(project)
    state = request.form.get("state")
    if state not in ("active", "completed", "dropped"):
        abort(400)
    if state == "completed":
        remaining = get_db().execute(
            sa.select(sa.func.count())
            .select_from(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.project_id == project_id,
                task_table.c.workflow_status.not_in(("done", "dropped")),
            )
        ).scalar_one()
        if remaining:
            flash("The project still has open tasks.", "error")
            return redirect(url_for("tasks.project_detail", project_id=project_id))
        if request.form.get("confirm") != "1":
            abort(400)
    database = get_db()
    database.execute(
        sa.update(projects)
        .where(projects.c.id == project_id)
        .values(
            state=state,
            revision=projects.c.revision + 1,
            updated_at=sa.func.current_timestamp(),
        )
    )
    database.commit()
    flash("Project updated.", "success")
    return redirect(url_for("tasks.project_detail", project_id=project["id"]))
