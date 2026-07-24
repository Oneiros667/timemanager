from __future__ import annotations

from datetime import date, datetime

import sqlalchemy as sa
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db, local_installation_id, new_public_id
from .models import tasks as task_table
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
            task_table.c.state == "active",
            task_table.c.is_highlight.is_(False),
        )
    )
    if exclude_task_id is not None:
        query = query.where(task_table.c.id != exclude_task_id)
    return int(database.execute(query).scalar_one())


def _today_state(database, user_id: int) -> str:
    if _active_option_count(database, user_id) < TODAY_OPTION_LIMIT:
        return "active"
    return "ready"


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
                task_table.c.state.in_(("active", "ready")),
            )
            .order_by(task_table.c.is_highlight.desc(), task_table.c.created_at)
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
                task_table.c.state == "done",
            )
            .order_by(task_table.c.completed_at.desc())
            .limit(5)
        )
        .mappings()
        .all()
    )
    inbox_count = database.execute(
        sa.select(sa.func.count())
        .select_from(task_table)
        .where(
            task_table.c.user_id == g.user["id"],
            task_table.c.state == "inbox",
        )
    ).scalar_one()
    highlight = next((task for task in task_rows if task["is_highlight"]), None)
    optional_tasks = [
        task
        for task in task_rows
        if not task["is_highlight"] and task["state"] == "active"
    ]
    overflow_tasks = [
        task
        for task in task_rows
        if not task["is_highlight"] and task["state"] == "ready"
    ]

    return render_template(
        "today.html",
        today_label=date.today().strftime("%A, %d %B"),
        highlight=highlight,
        optional_tasks=optional_tasks,
        option_limit=TODAY_OPTION_LIMIT,
        overflow_tasks=overflow_tasks,
        completed=completed,
        inbox_count=inbox_count,
    )


@blueprint.get("/inbox")
@login_required
def inbox():
    task_rows = (
        get_db()
        .execute(
            sa.select(task_table)
            .where(
                task_table.c.user_id == g.user["id"],
                task_table.c.state == "inbox",
            )
            .order_by(task_table.c.created_at.desc())
        )
        .mappings()
        .all()
    )
    return render_template("inbox.html", tasks=task_rows)


@blueprint.post("/tasks")
@login_required
def create_task():
    title = " ".join(request.form.get("title", "").split())
    placement = request.form.get("placement", "today")
    destination = "tasks.inbox" if placement == "inbox" else "tasks.today"

    if not title:
        flash("Add a few words so the thought has somewhere to land.", "error")
        return redirect(url_for(destination))
    if len(title) > 180:
        flash("Keep the capture under 180 characters. Details can come later.", "error")
        return redirect(url_for(destination))

    database = get_db()
    state = "inbox" if placement == "inbox" else _today_state(
        database,
        g.user["id"],
    )
    planned_date = None if placement == "inbox" else _today()
    database.execute(
        sa.insert(task_table).values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            title=title,
            state=state,
            planned_date=planned_date,
        )
    )
    database.commit()
    if state == "ready":
        flash(
            "Captured in Today overflow. Your three active options stay small.",
            "success",
        )
    else:
        flash("Captured. You can keep moving.", "success")
    return redirect(url_for(destination))


@blueprint.post("/tasks/<int:task_id>/today")
@login_required
def move_to_today(task_id: int):
    task = _owned_task(task_id)
    if task["state"] != "inbox":
        abort(400)
    database = get_db()
    state = _today_state(database, g.user["id"])
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            state=state,
            planned_date=_today(),
            is_highlight=False,
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    if state == "ready":
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
        or task["state"] != "ready"
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
            state="active",
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("Moved into your active Today plan.", "success")
    return redirect(url_for("tasks.today"))


@blueprint.post("/tasks/<int:task_id>/inbox")
@login_required
def move_to_inbox(task_id: int):
    task = _owned_task(task_id)
    if task["planned_date"] != _today() or task["state"] not in ("active", "ready"):
        abort(400)

    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            state="inbox",
            planned_date=None,
            is_highlight=False,
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash(f"Saved “{task['title']}” for later.", "success")
    return redirect(url_for("tasks.today"))


@blueprint.post("/tasks/<int:task_id>/highlight")
@login_required
def choose_highlight(task_id: int):
    task = _owned_task(task_id)
    if (
        task["planned_date"] != _today()
        or task["state"] not in ("active", "ready")
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
                task_table.c.state.in_(("active", "ready")),
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
        old_state = "active" if active_options < TODAY_OPTION_LIMIT else "ready"
        database.execute(
            sa.update(task_table)
            .where(task_table.c.id == old_highlight["id"])
            .values(
                is_highlight=False,
                state=old_state,
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
            state="active",
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
    database = get_db()
    if task["state"] == "done":
        restored_state = _today_state(database, g.user["id"])
        database.execute(
            sa.update(task_table)
            .where(
                task_table.c.id == task_id,
                task_table.c.user_id == g.user["id"],
            )
            .values(
                state=restored_state,
                completed_at=None,
                updated_at=sa.func.current_timestamp(),
                revision=task_table.c.revision + 1,
            )
        )
        if restored_state == "ready":
            flash(
                "Restored to Today overflow. Your active plan remains at three.",
                "success",
            )
        else:
            flash("Restored to today.", "success")
    elif task["state"] not in ("dropped", "inbox"):
        database.execute(
            sa.update(task_table)
            .where(
                task_table.c.id == task_id,
                task_table.c.user_id == g.user["id"],
            )
            .values(
                state="done",
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


@blueprint.post("/tasks/<int:task_id>/drop")
@login_required
def drop_task(task_id: int):
    task = _owned_task(task_id)
    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            state="dropped",
            is_highlight=False,
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash(f"Dropped “{task['title']}”. Letting go is a valid decision.", "success")
    destination = "tasks.inbox" if task["state"] == "inbox" else "tasks.today"
    return redirect(url_for(destination))
