from __future__ import annotations

from datetime import date, datetime

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db

blueprint = Blueprint("tasks", __name__)


def _today() -> str:
    return date.today().isoformat()


def _owned_task(task_id: int):
    task = get_db().execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, g.user["id"]),
    ).fetchone()
    if task is None:
        abort(404)
    return task


@blueprint.get("/today")
@login_required
def today():
    database = get_db()
    today_value = _today()
    tasks = database.execute(
        """
        SELECT * FROM tasks
        WHERE user_id = ?
          AND planned_date = ?
          AND state NOT IN ('done', 'dropped')
        ORDER BY is_highlight DESC, created_at ASC
        """,
        (g.user["id"], today_value),
    ).fetchall()
    completed = database.execute(
        """
        SELECT * FROM tasks
        WHERE user_id = ? AND planned_date = ? AND state = 'done'
        ORDER BY completed_at DESC
        LIMIT 5
        """,
        (g.user["id"], today_value),
    ).fetchall()
    inbox_count = database.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND state = 'inbox'",
        (g.user["id"],),
    ).fetchone()[0]
    highlight = next((task for task in tasks if task["is_highlight"]), None)
    optional_tasks = [task for task in tasks if not task["is_highlight"]]

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
    tasks = get_db().execute(
        """
        SELECT * FROM tasks
        WHERE user_id = ? AND state = 'inbox'
        ORDER BY created_at DESC
        """,
        (g.user["id"],),
    ).fetchall()
    return render_template("inbox.html", tasks=tasks)


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
        """
        INSERT INTO tasks (user_id, title, state, planned_date)
        VALUES (?, ?, ?, ?)
        """,
        (g.user["id"], title, state, planned_date),
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
        """
        UPDATE tasks
        SET state = 'ready', planned_date = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
        """,
        (_today(), task_id, g.user["id"]),
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
        """
        UPDATE tasks SET is_highlight = 0, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ? AND planned_date = ?
        """,
        (g.user["id"], _today()),
    )
    database.execute(
        """
        UPDATE tasks SET is_highlight = 1, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
        """,
        (task_id, g.user["id"]),
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
            """
            UPDATE tasks
            SET state = 'ready', completed_at = NULL, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (task_id, g.user["id"]),
        )
        flash("Restored to today.", "success")
    elif task["state"] not in ("dropped", "inbox"):
        database.execute(
            """
            UPDATE tasks
            SET state = 'done', is_highlight = 0,
                completed_at = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (datetime.now().isoformat(timespec="seconds"), task_id, g.user["id"]),
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
        """
        UPDATE tasks
        SET state = 'dropped', is_highlight = 0, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
        """,
        (task_id, g.user["id"]),
    )
    database.commit()
    flash(f"Dropped “{task['title']}”. Letting go is a valid decision.", "success")
    destination = "tasks.inbox" if task["state"] == "inbox" else "tasks.today"
    return redirect(url_for(destination))
