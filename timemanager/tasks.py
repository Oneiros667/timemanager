from __future__ import annotations

from datetime import date, datetime

import sqlalchemy as sa
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db, local_installation_id, new_public_id
from .models import tasks as task_table

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
                task_table.c.state.not_in(("done", "dropped")),
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
    optional_tasks = [task for task in task_rows if not task["is_highlight"]]

    return render_template(
        "today.html",
        today_label=date.today().strftime("%A, %d %B"),
        highlight=highlight,
        optional_tasks=optional_tasks,
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

    state = "inbox" if placement == "inbox" else "ready"
    planned_date = None if placement == "inbox" else _today()
    database = get_db()
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
    flash("Captured. You can keep moving.", "success")
    return redirect(url_for(destination))


@blueprint.post("/tasks/<int:task_id>/today")
@login_required
def move_to_today(task_id: int):
    _owned_task(task_id)
    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.id == task_id,
            task_table.c.user_id == g.user["id"],
        )
        .values(
            state="ready",
            planned_date=_today(),
            updated_at=sa.func.current_timestamp(),
            revision=task_table.c.revision + 1,
        )
    )
    database.commit()
    flash("Added to today.", "success")
    return redirect(url_for("tasks.inbox"))


@blueprint.post("/tasks/<int:task_id>/highlight")
@login_required
def choose_highlight(task_id: int):
    task = _owned_task(task_id)
    if task["planned_date"] != _today() or task["state"] in ("done", "dropped"):
        abort(400)

    database = get_db()
    database.execute(
        sa.update(task_table)
        .where(
            task_table.c.user_id == g.user["id"],
            task_table.c.planned_date == _today(),
            task_table.c.is_highlight.is_(True),
            task_table.c.id != task_id,
        )
        .values(
            is_highlight=False,
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
        database.execute(
            sa.update(task_table)
            .where(
                task_table.c.id == task_id,
                task_table.c.user_id == g.user["id"],
            )
            .values(
                state="ready",
                completed_at=None,
                updated_at=sa.func.current_timestamp(),
                revision=task_table.c.revision + 1,
            )
        )
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
