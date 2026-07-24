from __future__ import annotations

from datetime import date

from werkzeug.security import generate_password_hash

from timemanager.db import get_db

from .conftest import create_user, csrf_token, register


def _post_with_csrf(client, path: str, data: dict | None = None, page: str = "/today"):
    payload = {"_csrf_token": csrf_token(client, page)}
    payload.update(data or {})
    return client.post(path, data=payload, follow_redirects=True)


def test_capture_to_today_and_inbox(app, client):
    register(client)

    response = _post_with_csrf(
        client,
        "/tasks",
        {"title": "  Open   the project brief  ", "placement": "today"},
    )
    assert b"Open the project brief" in response.data
    assert b"Captured. You can keep moving." in response.data

    response = _post_with_csrf(
        client,
        "/tasks",
        {"title": "Compare calendar options", "placement": "inbox"},
    )
    assert b"Compare calendar options" in response.data
    assert b"Waiting for a decision" in response.data

    with app.app_context():
        rows = get_db().execute(
            "SELECT title, state, planned_date FROM tasks ORDER BY id"
        ).fetchall()
        assert dict(rows[0]) == {
            "title": "Open the project brief",
            "state": "ready",
            "planned_date": date.today().isoformat(),
        }
        assert dict(rows[1]) == {
            "title": "Compare calendar options",
            "state": "inbox",
            "planned_date": None,
        }


def test_empty_and_overlong_capture_are_rejected(app, client):
    register(client)
    response = _post_with_csrf(
        client,
        "/tasks",
        {"title": "   ", "placement": "today"},
    )
    assert b"Add a few words" in response.data

    response = _post_with_csrf(
        client,
        "/tasks",
        {"title": "x" * 181, "placement": "today"},
    )
    assert b"Keep the capture under 180 characters" in response.data

    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0


def test_move_to_today_choose_one_highlight_complete_and_restore(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "First action", "placement": "today"},
    )
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Second action", "placement": "inbox"},
    )

    with app.app_context():
        rows = get_db().execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
        first_id, second_id = rows[0]["id"], rows[1]["id"]

    response = _post_with_csrf(
        client,
        f"/tasks/{second_id}/today",
        page="/inbox",
    )
    assert b"Added to today." in response.data

    _post_with_csrf(client, f"/tasks/{first_id}/highlight")
    response = _post_with_csrf(client, f"/tasks/{second_id}/highlight")
    assert b"Second action" in response.data
    assert b"Your chosen focus" in response.data

    with app.app_context():
        highlights = get_db().execute(
            "SELECT id FROM tasks WHERE is_highlight = 1"
        ).fetchall()
        assert [row["id"] for row in highlights] == [second_id]

    response = _post_with_csrf(client, f"/tasks/{second_id}/toggle")
    assert b"Done. Take a breath before the next thing." in response.data
    assert b"1 completed today" in response.data

    response = _post_with_csrf(client, f"/tasks/{second_id}/toggle")
    assert b"Restored to today." in response.data
    assert b"Second action" in response.data


def test_drop_is_deliberate_and_removes_task_from_active_view(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "An optional task", "placement": "today"},
    )
    with app.app_context():
        task_id = get_db().execute("SELECT id FROM tasks").fetchone()["id"]

    response = _post_with_csrf(client, f"/tasks/{task_id}/drop")
    assert b"Letting go is a valid decision." in response.data
    assert b'data-focus-task="An optional task"' not in response.data

    with app.app_context():
        task = get_db().execute("SELECT state FROM tasks").fetchone()
        assert task["state"] == "dropped"


def test_users_cannot_read_or_mutate_another_users_tasks(app, client):
    register(client)
    other_id = create_user(
        app,
        "Morgan",
        "morgan@example.com",
        generate_password_hash("another secure password"),
    )
    with app.app_context():
        database = get_db()
        cursor = database.execute(
            """
            INSERT INTO tasks (user_id, title, state, planned_date)
            VALUES (?, 'Private task', 'ready', ?)
            """,
            (other_id, date.today().isoformat()),
        )
        database.commit()
        private_task_id = cursor.lastrowid

    today = client.get("/today")
    assert b"Private task" not in today.data

    response = _post_with_csrf(client, f"/tasks/{private_task_id}/drop")
    assert response.status_code == 404
    with app.app_context():
        task = get_db().execute(
            "SELECT state FROM tasks WHERE id = ?",
            (private_task_id,),
        ).fetchone()
        assert task["state"] == "ready"
