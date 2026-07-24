from __future__ import annotations

from datetime import date

import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from timemanager.db import get_db, local_installation_id, new_public_id
from timemanager.models import tasks

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
        rows = (
            get_db()
            .execute(
                sa.select(tasks.c.title, tasks.c.state, tasks.c.planned_date).order_by(
                    tasks.c.id
                )
            )
            .mappings()
            .all()
        )
        assert dict(rows[0]) == {
            "title": "Open the project brief",
            "state": "active",
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
        assert (
            get_db().execute(sa.select(sa.func.count()).select_from(tasks)).scalar_one()
            == 0
        )


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
        rows = (
            get_db()
            .execute(sa.select(tasks.c.id, tasks.c.title).order_by(tasks.c.id))
            .mappings()
            .all()
        )
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
        highlights = (
            get_db()
            .execute(sa.select(tasks.c.id).where(tasks.c.is_highlight.is_(True)))
            .mappings()
            .all()
        )
        assert [row["id"] for row in highlights] == [second_id]

    response = _post_with_csrf(client, f"/tasks/{second_id}/toggle")
    assert b"Done. Take a breath before the next thing." in response.data
    assert b"1 completed today" in response.data

    response = _post_with_csrf(client, f"/tasks/{second_id}/toggle")
    assert b"Restored to today." in response.data
    assert b"Second action" in response.data


def test_today_caps_active_options_and_keeps_explicit_overflow(app, client):
    register(client)
    for title in ("One", "Two", "Three", "Four"):
        response = _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )

    assert b"Captured in Today overflow" in response.data
    assert b"3 of 3 options" in response.data
    assert b"extra" in response.data
    assert b"waiting for a decision" in response.data
    assert b"Four" in response.data

    with app.app_context():
        rows = (
            get_db()
            .execute(sa.select(tasks.c.title, tasks.c.state).order_by(tasks.c.id))
            .mappings()
            .all()
        )
    assert [row["state"] for row in rows] == [
        "active",
        "active",
        "active",
        "ready",
    ]


def test_overflow_requires_space_and_can_move_back_to_inbox(app, client):
    register(client)
    for title in ("One", "Two", "Three", "Four"):
        _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )
    with app.app_context():
        rows = (
            get_db()
            .execute(sa.select(tasks.c.id, tasks.c.title).order_by(tasks.c.id))
            .mappings()
            .all()
        )
        first_id = rows[0]["id"]
        overflow_id = rows[3]["id"]

    response = _post_with_csrf(client, f"/tasks/{overflow_id}/activate")
    assert b"Save one for later first" in response.data

    response = _post_with_csrf(client, f"/tasks/{first_id}/inbox")
    assert b"Saved" in response.data
    with app.app_context():
        assert get_db().execute(
            sa.select(tasks.c.state).where(tasks.c.id == overflow_id)
        ).scalar_one() == "ready"
    response = _post_with_csrf(client, f"/tasks/{overflow_id}/activate")
    assert b"Moved into your active Today plan" in response.data

    with app.app_context():
        rows = (
            get_db()
            .execute(
                sa.select(tasks.c.id, tasks.c.state, tasks.c.planned_date).where(
                    tasks.c.id.in_((first_id, overflow_id))
                )
            )
            .mappings()
            .all()
        )
    by_id = {row["id"]: row for row in rows}
    assert by_id[first_id]["state"] == "inbox"
    assert by_id[first_id]["planned_date"] is None
    assert by_id[overflow_id]["state"] == "active"


def test_move_from_inbox_uses_overflow_when_today_is_full(app, client):
    register(client)
    for title in ("One", "Two", "Three"):
        _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Inbox task", "placement": "inbox"},
    )
    with app.app_context():
        inbox_id = get_db().execute(
            sa.select(tasks.c.id).where(tasks.c.state == "inbox")
        ).scalar_one()

    response = _post_with_csrf(
        client,
        f"/tasks/{inbox_id}/today",
        page="/inbox",
    )

    assert b"Added to Today overflow" in response.data
    with app.app_context():
        row = (
            get_db()
            .execute(
                sa.select(tasks.c.state, tasks.c.planned_date).where(
                    tasks.c.id == inbox_id
                )
            )
            .mappings()
            .one()
        )
    assert row["state"] == "ready"
    assert row["planned_date"] == date.today().isoformat()


def test_highlight_is_separate_from_three_optional_actions(app, client):
    register(client)
    for title in ("Highlight", "Two", "Three", "Four"):
        _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )
    with app.app_context():
        rows = (
            get_db()
            .execute(sa.select(tasks.c.id).order_by(tasks.c.id))
            .scalars()
            .all()
        )

    _post_with_csrf(client, f"/tasks/{rows[0]}/highlight")
    response = _post_with_csrf(client, f"/tasks/{rows[3]}/activate")

    assert b"3 of 3 options" in response.data
    with app.app_context():
        database = get_db()
        assert database.execute(
            sa.select(sa.func.count())
            .select_from(tasks)
            .where(tasks.c.is_highlight.is_(True))
        ).scalar_one() == 1
        assert database.execute(
            sa.select(sa.func.count())
            .select_from(tasks)
            .where(
                tasks.c.state == "active",
                tasks.c.is_highlight.is_(False),
            )
        ).scalar_one() == 3


def test_overflow_can_replace_the_highlight_without_expanding_options(app, client):
    register(client)
    for title in ("Old highlight", "Two", "Three", "Four", "New highlight"):
        _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )
    with app.app_context():
        rows = (
            get_db()
            .execute(sa.select(tasks.c.id, tasks.c.title).order_by(tasks.c.id))
            .mappings()
            .all()
        )
    old_id = rows[0]["id"]
    fourth_id = rows[3]["id"]
    new_id = rows[4]["id"]

    _post_with_csrf(client, f"/tasks/{old_id}/highlight")
    _post_with_csrf(client, f"/tasks/{fourth_id}/activate")
    response = _post_with_csrf(client, f"/tasks/{new_id}/highlight")

    assert b"New highlight" in response.data
    with app.app_context():
        database = get_db()
        states = {
            row["id"]: row
            for row in database.execute(
                sa.select(tasks.c.id, tasks.c.state, tasks.c.is_highlight)
            )
            .mappings()
            .all()
        }
        assert states[new_id]["state"] == "active"
        assert states[new_id]["is_highlight"] is True
        assert states[old_id]["state"] == "ready"
        assert states[old_id]["is_highlight"] is False
        assert sum(
            row["state"] == "active" and not row["is_highlight"]
            for row in states.values()
        ) == 3


def test_restoring_when_today_is_full_uses_overflow(app, client):
    register(client)
    for title in ("One", "Two", "Three"):
        _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )
    with app.app_context():
        first_id = get_db().execute(
            sa.select(tasks.c.id).order_by(tasks.c.id)
        ).scalars().first()
    _post_with_csrf(client, f"/tasks/{first_id}/toggle")
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Replacement", "placement": "today"},
    )

    response = _post_with_csrf(client, f"/tasks/{first_id}/toggle")

    assert b"Restored to Today overflow" in response.data
    with app.app_context():
        assert get_db().execute(
            sa.select(tasks.c.state).where(tasks.c.id == first_id)
        ).scalar_one() == "ready"


def test_drop_is_deliberate_and_removes_task_from_active_view(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "An optional task", "placement": "today"},
    )
    with app.app_context():
        task_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()

    response = _post_with_csrf(client, f"/tasks/{task_id}/drop")
    assert b"Letting go is a valid decision." in response.data
    assert b'data-focus-task="An optional task"' not in response.data

    with app.app_context():
        task = (
            get_db()
            .execute(sa.select(tasks.c.state, tasks.c.revision))
            .mappings()
            .one()
        )
        assert task["state"] == "dropped"
        assert task["revision"] == 2


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
        private_task_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=other_id,
                title="Private task",
                state="ready",
                planned_date=date.today().isoformat(),
            )
            .returning(tasks.c.id)
        ).scalar_one()
        database.commit()

    today = client.get("/today")
    assert b"Private task" not in today.data

    response = _post_with_csrf(client, f"/tasks/{private_task_id}/drop")
    assert response.status_code == 404
    response = _post_with_csrf(client, f"/tasks/{private_task_id}/activate")
    assert response.status_code == 404
    response = _post_with_csrf(client, f"/tasks/{private_task_id}/inbox")
    assert response.status_code == 404
    with app.app_context():
        task = (
            get_db()
            .execute(sa.select(tasks.c.state).where(tasks.c.id == private_task_id))
            .mappings()
            .one()
        )
        assert task["state"] == "ready"
