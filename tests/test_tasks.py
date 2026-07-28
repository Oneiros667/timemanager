from __future__ import annotations

from datetime import date

import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from timemanager.account_transfer import export_account
from timemanager.db import get_db, local_installation_id, new_public_id
from timemanager.models import (
    projects,
    task_components,
    task_dependencies,
    task_waits,
    tasks,
    users,
)

from .conftest import create_user, csrf_token, register


def _post_with_csrf(client, path: str, data: dict | None = None, page: str = "/today"):
    payload = {"_csrf_token": csrf_token(client, page)}
    payload.update(data or {})
    return client.post(path, data=payload, follow_redirects=True)


def _task_snapshot(app) -> list[dict]:
    with app.app_context():
        rows = (
            get_db()
            .execute(sa.select(tasks).order_by(tasks.c.id))
            .mappings()
            .all()
        )
        return [dict(row) for row in rows]


def _insert_project(
    database,
    user_id: int,
    title: str,
    *,
    desired_outcome: str = "",
    state: str = "active",
) -> int:
    return int(
        database.execute(
            sa.insert(projects)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=user_id,
                title=title,
                desired_outcome=desired_outcome,
                state=state,
            )
            .returning(projects.c.id)
        ).scalar_one()
    )


def test_capture_to_today_and_tasks(app, client):
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
        {"title": "Compare calendar options", "placement": "later"},
    )
    assert b"Compare calendar options" in response.data
    assert b"Captured" in response.data

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


def test_today_and_later_are_explicit_views_without_old_view_routes(client):
    register(client)

    today = client.get("/today")
    assert b"Current view \xc2\xb7 Today" in today.data
    assert b'href="/later"' in today.data
    assert b"data-mode-toggle" in today.data
    assert b"Low capacity Today" in today.data
    assert today.data.count(b'aria-current="page"') == 2

    later = client.get("/later")
    assert later.status_code == 200
    assert b"Current view \xc2\xb7 Later" in later.data
    assert today.data.count(b"Quick capture") == 1
    assert later.data.count(b"Quick capture") == 1
    assert b"Get it out of your head" not in today.data
    assert b"Add a task" not in later.data
    assert b"Captured" in later.data
    assert b"Ready and waiting" in later.data
    assert b"data-mode-toggle" not in later.data
    assert later.data.count(b'aria-current="page"') == 2

    assert client.get("/inbox").status_code == 404
    assert client.get("/tasks").status_code == 405


def test_low_capacity_today_has_a_calm_empty_state_and_full_view_escape(client):
    response = register(client)

    assert b'data-hidden-today-count="0"' in response.data
    assert b"data-low-capacity-empty" in response.data
    assert b"No actionable Today task right now" in response.data
    assert b"There is no unfinished Today work to choose from" in response.data
    assert b"data-show-full-today" in response.data
    assert b"Show full Today" in response.data
    assert b"data-low-capacity-task-id" not in response.data


def test_low_capacity_fallback_skips_blocked_overflow_and_completed_tasks(
    app,
    client,
):
    register(client)
    for title in (
        "Blocked first",
        "Available second",
        "Completed third",
        "Overflow fourth",
    ):
        _post_with_csrf(
            client,
            "/tasks",
            {"title": title, "placement": "today"},
        )
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Unfinished prerequisite", "placement": "later"},
    )

    with app.app_context():
        database = get_db()
        rows = (
            database.execute(
                sa.select(tasks.c.id, tasks.c.title, tasks.c.user_id).order_by(
                    tasks.c.id
                )
            )
            .mappings()
            .all()
        )
        by_title = {row["title"]: row for row in rows}
        database.execute(
            sa.insert(task_dependencies).values(
                user_id=by_title["Blocked first"]["user_id"],
                task_id=by_title["Blocked first"]["id"],
                prerequisite_task_id=by_title["Unfinished prerequisite"]["id"],
            )
        )
        database.execute(
            sa.update(tasks)
            .where(tasks.c.id == by_title["Available second"]["id"])
            .values(
                next_action="Open the working document",
                revision=tasks.c.revision + 1,
            )
        )
        database.commit()

    _post_with_csrf(
        client,
        f"/tasks/{by_title['Completed third']['id']}/toggle",
    )
    before = _task_snapshot(app)

    response = client.get("/today")

    assert response.status_code == 200
    assert response.data.count(b"data-low-capacity-task-id=") == 1
    assert (
        f'data-low-capacity-task-id="{by_title["Available second"]["id"]}"'.encode()
        in response.data
    )
    assert b'data-low-capacity-kind="fallback"' in response.data
    assert b"Next: Open the working document" in response.data
    assert b'data-hidden-today-count="2"' in response.data
    assert b"2 unfinished Today" in response.data
    assert (
        f'data-low-capacity-task-id="{by_title["Blocked first"]["id"]}"'.encode()
        not in response.data
    )
    assert (
        f'data-low-capacity-task-id="{by_title["Overflow fourth"]["id"]}"'.encode()
        not in response.data
    )
    assert (
        f'data-low-capacity-task-id="{by_title["Completed third"]["id"]}"'.encode()
        not in response.data
    )
    assert _task_snapshot(app) == before

    _post_with_csrf(
        client,
        f"/tasks/{by_title['Available second']['id']}/toggle",
    )
    before_blocked_only = _task_snapshot(app)

    response = client.get("/today")

    assert b"data-low-capacity-empty" in response.data
    assert b"data-low-capacity-task-id" not in response.data
    assert b'data-hidden-today-count="2"' in response.data
    assert b"Blocked and overflow tasks are still in the full Today view" in response.data
    assert _task_snapshot(app) == before_blocked_only


def test_low_capacity_prefers_the_existing_highlight_without_mutation(app, client):
    register(client)
    for title in ("First active task", "Chosen highlight"):
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
    by_title = {row["title"]: row["id"] for row in rows}
    _post_with_csrf(client, f"/tasks/{by_title['Chosen highlight']}/highlight")
    before = _task_snapshot(app)

    response = client.get("/today")

    assert (
        f'data-low-capacity-task-id="{by_title["Chosen highlight"]}"'.encode()
        in response.data
    )
    assert b'data-low-capacity-kind="highlight"' in response.data
    assert b'data-hidden-today-count="1"' in response.data
    assert (
        f'data-low-capacity-task-id="{by_title["First active task"]}"'.encode()
        not in response.data
    )
    assert _task_snapshot(app) == before


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
        {"title": "Second action", "placement": "later"},
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
        page="/later",
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
    assert b"outside the active plan" in response.data
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


def test_overflow_requires_space_and_can_move_to_later(app, client):
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

    response = _post_with_csrf(client, f"/tasks/{first_id}/later")
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
                sa.select(
                    tasks.c.id,
                    tasks.c.state,
                    tasks.c.workflow_status,
                    tasks.c.today_placement,
                    tasks.c.planned_date,
                ).where(tasks.c.id.in_((first_id, overflow_id)))
            )
            .mappings()
            .all()
        )
    by_id = {row["id"]: row for row in rows}
    assert by_id[first_id]["workflow_status"] == "open"
    assert by_id[first_id]["today_placement"] == "unplanned"
    assert by_id[first_id]["planned_date"] is None
    assert by_id[overflow_id]["state"] == "active"


def test_move_from_tasks_uses_overflow_when_today_is_full(app, client):
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
        {"title": "Captured task", "placement": "later"},
    )
    with app.app_context():
        inbox_id = get_db().execute(
            sa.select(tasks.c.id).where(tasks.c.state == "inbox")
        ).scalar_one()

    response = _post_with_csrf(
        client,
        f"/tasks/{inbox_id}/today",
        page="/later",
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


def test_work_saved_for_later_remains_discoverable_in_later(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Confirm the venue", "placement": "later"},
    )
    with app.app_context():
        task_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()

    _post_with_csrf(
        client,
        f"/tasks/{task_id}/wait",
        {"reason": "Venue reply"},
        page=f"/tasks/{task_id}",
    )

    later = client.get("/later")
    assert b"Confirm the venue" in later.data
    assert b"Review blocker" in later.data
    today_action = f'action="/tasks/{task_id}/today"'.encode()
    assert today_action not in later.data
    today = client.get("/today")
    assert b"<strong>1</strong>" in today.data

    _post_with_csrf(
        client,
        f"/tasks/{task_id}/override",
        {"confirm": "1"},
        page=f"/tasks/{task_id}",
    )
    later = client.get("/later")
    assert b"Confirm the venue" in later.data
    assert today_action in later.data

    response = _post_with_csrf(
        client,
        f"/tasks/{task_id}/today",
        page="/later",
    )
    assert b"Added to today." in response.data
    assert b"Confirm the venue" in response.data
    assert b"<strong>0</strong>" in response.data


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


def test_task_workspace_autosave_and_revision_conflict(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Prepare report", "placement": "later"},
    )
    with app.app_context():
        task = get_db().execute(sa.select(tasks)).mappings().one()

    response = client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    assert b"Start here" in response.data
    assert b"Steps" in response.data

    token = csrf_token(client, f"/tasks/{task['id']}")
    response = client.post(
        f"/tasks/{task['id']}/details",
        data={
            "_csrf_token": token,
            "revision": task["revision"],
            "title": "Prepare quarterly report",
            "next_action": "Open the figures",
            "definition_of_done": "Report sent",
            "notes": "Keep it short",
        },
        headers={"Accept": "application/json", "X-Requested-With": "fetch"},
    )
    assert response.status_code == 200
    assert response.json["revision"] == 2

    response = client.post(
        f"/tasks/{task['id']}/details",
        data={
            "_csrf_token": token,
            "revision": 1,
            "title": "Stale title",
            "next_action": "",
            "definition_of_done": "",
            "notes": "",
        },
        headers={"Accept": "application/json", "X-Requested-With": "fetch"},
    )
    assert response.status_code == 409
    assert response.json["current"]["title"] == "Prepare quarterly report"

    response = _post_with_csrf(
        client,
        f"/tasks/{task['id']}/details",
        {
            "revision": "2",
            "title": "Prepare final report",
            "next_action": "Open the figures",
            "definition_of_done": "Report sent",
            "notes": "Keep it short",
        },
        page=f"/tasks/{task['id']}",
    )
    assert b"Saved." in response.data
    assert b"Prepare final report" in response.data


def test_components_are_rapidly_added_reordered_and_require_completion_confirmation(
    app, client
):
    register(client)
    _post_with_csrf(client, "/tasks", {"title": "Pack bag", "placement": "today"})
    with app.app_context():
        task_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()

    for title in ("Laptop", "Charger"):
        _post_with_csrf(
            client,
            f"/tasks/{task_id}/components",
            {"title": title},
            page=f"/tasks/{task_id}",
        )

    with app.app_context():
        rows = (
            get_db()
            .execute(
                sa.select(task_components).order_by(task_components.c.position)
            )
            .mappings()
            .all()
        )
        assert [row["title"] for row in rows] == ["Laptop", "Charger"]
        charger_id = rows[1]["id"]
        charger_revision = rows[1]["revision"]

    response = _post_with_csrf(
        client,
        f"/components/{charger_id}/details",
        {"title": "Phone charger", "revision": str(charger_revision)},
        page=f"/tasks/{task_id}",
    )
    assert b"Phone charger" in response.data

    _post_with_csrf(
        client,
        f"/components/{charger_id}/move",
        {"direction": "up"},
        page=f"/tasks/{task_id}",
    )
    with app.app_context():
        titles = get_db().execute(
            sa.select(task_components.c.title).order_by(task_components.c.position)
        ).scalars().all()
        assert titles == ["Phone charger", "Laptop"]

    response = _post_with_csrf(client, f"/tasks/{task_id}/toggle")
    assert b"unfinished steps" in response.data
    with app.app_context():
        assert get_db().execute(
            sa.select(tasks.c.workflow_status).where(tasks.c.id == task_id)
        ).scalar_one() == "open"

    response = _post_with_csrf(
        client,
        f"/tasks/{task_id}/toggle",
        {"confirm_unfinished": "1"},
        page=f"/tasks/{task_id}",
    )
    assert b"Done." in response.data


def test_structural_mutation_rejects_a_stale_task_revision(app, client):
    register(client)
    _post_with_csrf(client, "/tasks", {"title": "Plan trip", "placement": "later"})
    with app.app_context():
        task_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()

    _post_with_csrf(
        client,
        f"/tasks/{task_id}/components",
        {"title": "Choose dates", "revision": "1"},
        page=f"/tasks/{task_id}",
    )
    response = _post_with_csrf(
        client,
        f"/tasks/{task_id}/components",
        {"title": "Book travel", "revision": "1"},
        page=f"/tasks/{task_id}",
    )

    assert response.status_code == 409
    assert b"Current saved value: Plan trip" in response.data
    with app.app_context():
        assert get_db().execute(
            sa.select(sa.func.count()).select_from(task_components)
        ).scalar_one() == 1


def test_project_dependencies_waits_and_unblocking_do_not_change_today(app, client):
    register(client)
    for title in ("Approve design", "Build pages", "Publish"):
        _post_with_csrf(client, "/tasks", {"title": title, "placement": "later"})
    with app.app_context():
        rows = (
            get_db()
            .execute(
                sa.select(tasks.c.id, tasks.c.title, tasks.c.revision).order_by(
                    tasks.c.id
                )
            )
            .mappings()
            .all()
        )
    by_title = {row["title"]: row["id"] for row in rows}
    revision_by_title = {row["title"]: row["revision"] for row in rows}

    response = _post_with_csrf(
        client,
        f"/tasks/{by_title['Approve design']}/promote-to-project",
        {
            "revision": str(revision_by_title["Approve design"]),
            "project_title": "Launch website",
            "confirm": "1",
        },
        page=f"/tasks/{by_title['Approve design']}",
    )
    assert b"Project created" in response.data
    with app.app_context():
        project_id = get_db().execute(sa.select(projects.c.id)).scalar_one()

    for title in ("Build pages", "Publish"):
        _post_with_csrf(
            client,
            f"/tasks/{by_title[title]}/project",
            {"project_id": str(project_id), "project_title": ""},
            page=f"/tasks/{by_title[title]}",
        )

    _post_with_csrf(
        client,
        f"/tasks/{by_title['Build pages']}/dependencies",
        {"prerequisite_task_id": str(by_title["Approve design"])},
        page=f"/tasks/{by_title['Build pages']}",
    )
    response = _post_with_csrf(
        client,
        f"/tasks/{by_title['Approve design']}/dependencies",
        {"prerequisite_task_id": str(by_title["Build pages"])},
        page=f"/tasks/{by_title['Approve design']}",
    )
    assert b"circular dependency" in response.data

    _post_with_csrf(
        client,
        f"/tasks/{by_title['Publish']}/wait",
        {
            "reason": "Hosting approval",
            "waiting_on": "Operator",
            "review_date": "2026-08-01",
            "follow_up_title": "Check hosting approval",
        },
        page=f"/tasks/{by_title['Publish']}",
    )
    with app.app_context():
        database = get_db()
        assert database.execute(
            sa.select(sa.func.count()).select_from(task_dependencies)
        ).scalar_one() == 1
        assert database.execute(
            sa.select(task_waits.c.reason)
        ).scalar_one() == "Hosting approval"
        follow_up_title = database.execute(
            sa.select(tasks.c.title)
            .join(task_waits, task_waits.c.follow_up_task_id == tasks.c.id)
        ).scalar_one()
        assert follow_up_title == "Check hosting approval"
        assert database.execute(
            sa.select(tasks.c.today_placement).where(
                tasks.c.id == by_title["Build pages"]
            )
        ).scalar_one() == "unplanned"

    _post_with_csrf(
        client,
        f"/tasks/{by_title['Approve design']}/today",
        page="/later",
    )
    _post_with_csrf(
        client,
        f"/tasks/{by_title['Approve design']}/toggle",
    )
    with app.app_context():
        database = get_db()
        build = database.execute(
            sa.select(tasks.c.workflow_status, tasks.c.today_placement).where(
                tasks.c.id == by_title["Build pages"]
            )
        ).mappings().one()
        assert dict(build) == {
            "workflow_status": "inbox",
            "today_placement": "unplanned",
        }


def test_promoting_steps_preserves_their_original_preferred_order(app, client):
    register(client)
    _post_with_csrf(client, "/tasks", {"title": "Move house", "placement": "later"})
    with app.app_context():
        task_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()

    for title in ("Pack", "Book van", "Return keys"):
        _post_with_csrf(
            client,
            f"/tasks/{task_id}/components",
            {"title": title},
            page=f"/tasks/{task_id}",
        )
    with app.app_context():
        component_rows = (
            get_db()
            .execute(
                sa.select(task_components.c.id, task_components.c.title).order_by(
                    task_components.c.position
                )
            )
            .mappings()
            .all()
        )
    ids = {row["title"]: row["id"] for row in component_rows}

    for title in ("Return keys", "Pack", "Book van"):
        _post_with_csrf(
            client,
            f"/components/{ids[title]}/promote",
            {"confirm": "1"},
            page=f"/tasks/{task_id}",
        )

    with app.app_context():
        titles = (
            get_db()
            .execute(
                sa.select(tasks.c.title)
                .where(tasks.c.project_id.is_not(None))
                .order_by(tasks.c.project_position)
            )
            .scalars()
            .all()
        )
    assert titles == ["Move house", "Pack", "Book van", "Return keys"]


def test_task_can_be_turned_into_a_project_without_losing_task_state(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Plan the launch", "placement": "today"},
    )
    with app.app_context():
        task = get_db().execute(sa.select(tasks)).mappings().one()

    missing_revision = _post_with_csrf(
        client,
        f"/tasks/{task['id']}/promote-to-project",
        {"project_title": "No revision", "confirm": "1"},
        page=f"/tasks/{task['id']}",
    )
    assert missing_revision.status_code == 400

    _post_with_csrf(
        client,
        f"/tasks/{task['id']}/details",
        {
            "revision": str(task["revision"]),
            "title": task["title"],
            "next_action": "List the launch tasks",
            "definition_of_done": "The launch is complete",
            "notes": "Keep the first version small",
        },
        page=f"/tasks/{task['id']}",
    )
    with app.app_context():
        task = get_db().execute(sa.select(tasks)).mappings().one()

    _post_with_csrf(
        client,
        f"/tasks/{task['id']}/components",
        {"revision": str(task["revision"]), "title": "List launch tasks"},
        page=f"/tasks/{task['id']}",
    )
    with app.app_context():
        task = get_db().execute(sa.select(tasks)).mappings().one()

    stale = _post_with_csrf(
        client,
        f"/tasks/{task['id']}/promote-to-project",
        {
            "revision": str(task["revision"] - 1),
            "project_title": "Stale project",
            "confirm": "1",
        },
        page=f"/tasks/{task['id']}",
    )
    assert stale.status_code == 409
    with app.app_context():
        assert get_db().execute(
            sa.select(sa.func.count()).select_from(projects)
        ).scalar_one() == 0

    response = _post_with_csrf(
        client,
        f"/tasks/{task['id']}/promote-to-project",
        {
            "revision": str(task["revision"]),
            "project_title": "Website launch",
            "confirm": "1",
        },
        page=f"/tasks/{task['id']}",
    )

    assert b"Project created" in response.data
    assert b"Website launch" in response.data
    assert b"Plan the launch" in response.data
    with app.app_context():
        project = get_db().execute(sa.select(projects)).mappings().one()
        promoted_task = get_db().execute(sa.select(tasks)).mappings().one()
        component = get_db().execute(sa.select(task_components)).mappings().one()

    assert project["title"] == "Website launch"
    assert project["desired_outcome"] == "The launch is complete"
    assert promoted_task["project_id"] == project["id"]
    assert promoted_task["project_position"] == 0
    assert promoted_task["today_placement"] == "active"
    assert promoted_task["planned_date"] == date.today().isoformat()
    assert promoted_task["next_action"] == "List the launch tasks"
    assert promoted_task["notes"] == "Keep the first version small"
    assert component["task_id"] == promoted_task["id"]
    assert component["title"] == "List launch tasks"


def test_project_collection_is_scoped_and_read_only_with_next_ready_and_archive(
    app,
    client,
):
    register(client)
    other_user_id = create_user(
        app,
        "Other",
        "other@example.com",
        generate_password_hash("other password"),
    )
    with app.app_context():
        database = get_db()
        user_id = database.execute(
            sa.select(users.c.id).where(users.c.email == "alex@example.com")
        ).scalar_one()
        active_id = _insert_project(
            database,
            user_id,
            "Release the guide",
            desired_outcome="The guide is available to readers",
        )
        _insert_project(
            database,
            user_id,
            "Completed project",
            desired_outcome="The completed outcome",
            state="completed",
        )
        _insert_project(
            database,
            user_id,
            "Dropped project",
            state="dropped",
        )
        _insert_project(
            database,
            other_user_id,
            "Another account project",
            state="completed",
        )
        for position, title, workflow_status, state in (
            (0, "Draft the guide", "open", "active"),
            (1, "Wait for review", "waiting", "active"),
            (2, "Choose a topic", "done", "done"),
        ):
            database.execute(
                sa.insert(tasks).values(
                    public_id=new_public_id(),
                    origin_installation_id=local_installation_id(database),
                    user_id=user_id,
                    title=title,
                    state=state,
                    workflow_status=workflow_status,
                    today_placement="unplanned",
                    project_id=active_id,
                    project_position=position,
                )
            )
        database.commit()
    before = _task_snapshot(app)

    response = client.get("/projects")

    assert response.status_code == 200
    assert b"Current view \xc2\xb7 Projects" in response.data
    assert b"Release the guide" in response.data
    assert b"The guide is available to readers" in response.data
    assert b"Draft the guide" in response.data
    assert b"1 ready \xc2\xb7" in response.data
    assert b"1 waiting \xc2\xb7" in response.data
    assert b"1 done" in response.data
    assert b"Project archive (2)" in response.data
    assert b"Completed project" in response.data
    assert b"Dropped project" in response.data
    assert b"Another account project" not in response.data
    assert b'<details class="workspace-card project-archive">' in response.data
    assert b'<details class="workspace-card project-archive" open>' not in response.data
    assert _task_snapshot(app) == before

    later = client.get("/later")
    assert b'href="/projects"' in later.data
    assert b"View projects" in later.data

    detail = client.get(f"/projects/{active_id}?return_to=/later")
    assert b'href="/later"' in detail.data
    assert b'name="return_to" value="/later"' in detail.data

    unsafe_return = client.get(
        f"/projects/{active_id}?return_to=//example.com/leave"
    )
    assert b'href="/projects"' in unsafe_return.data
    assert b'name="return_to" value="/projects"' in unsafe_return.data
    assert b'href="//example.com/leave"' not in unsafe_return.data


def test_archived_project_restore_is_explicit_revisioned_and_task_safe(app, client):
    register(client)
    other_user_id = create_user(
        app,
        "Other",
        "other@example.com",
        generate_password_hash("other password"),
    )
    with app.app_context():
        database = get_db()
        user_id = database.execute(
            sa.select(users.c.id).where(users.c.email == "alex@example.com")
        ).scalar_one()
        archived_id = _insert_project(
            database,
            user_id,
            "Paused move",
            desired_outcome="Everything is in the new home",
            state="dropped",
        )
        foreign_id = _insert_project(
            database,
            other_user_id,
            "Private project",
            state="dropped",
        )
        linked_task_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=user_id,
                title="Book the moving van",
                state="active",
                workflow_status="open",
                today_placement="unplanned",
                project_id=archived_id,
                project_position=0,
            )
            .returning(tasks.c.id)
        ).scalar_one()
        standalone_task_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=user_id,
                title="Choose a new project",
                state="inbox",
                workflow_status="inbox",
                today_placement="unplanned",
            )
            .returning(tasks.c.id)
        ).scalar_one()
        database.commit()
    before = _task_snapshot(app)

    assert client.post(
        f"/projects/{archived_id}/state",
        data={"revision": "1", "state": "active"},
    ).status_code == 400

    stale = _post_with_csrf(
        client,
        f"/projects/{archived_id}/state",
        {"revision": "0", "state": "active", "redirect_to": "/projects"},
        page="/projects",
    )
    assert stale.status_code == 409

    archived_detail = client.get(f"/projects/{archived_id}")
    assert b"Project \xc2\xb7 Dropped" in archived_detail.data
    assert b"This project is dropped" in archived_detail.data
    assert b"Restore project" in archived_detail.data
    assert b"data-autosave-form" not in archived_detail.data
    assert b"Add project task" not in archived_detail.data

    blocked_edit = _post_with_csrf(
        client,
        f"/projects/{archived_id}/details",
        {
            "revision": "1",
            "title": "Changed title",
            "desired_outcome": "",
            "notes": "",
        },
        page=f"/projects/{archived_id}",
    )
    assert blocked_edit.status_code == 409
    blocked_add = _post_with_csrf(
        client,
        f"/projects/{archived_id}/tasks",
        {"revision": "1", "title": "Unexpected task"},
        page=f"/projects/{archived_id}",
    )
    assert blocked_add.status_code == 409
    blocked_assignment = _post_with_csrf(
        client,
        f"/tasks/{standalone_task_id}/project",
        {"revision": "1", "project_id": str(archived_id)},
        page=f"/tasks/{standalone_task_id}",
    )
    assert blocked_assignment.status_code == 400
    foreign_restore = _post_with_csrf(
        client,
        f"/projects/{foreign_id}/state",
        {"revision": "1", "state": "active"},
        page="/projects",
    )
    assert foreign_restore.status_code == 404
    assert _task_snapshot(app) == before

    token = csrf_token(client, "/projects")
    restored = client.post(
        f"/projects/{archived_id}/state",
        data={
            "_csrf_token": token,
            "revision": "1",
            "state": "active",
            "redirect_to": "/projects",
        },
        follow_redirects=False,
    )

    assert restored.status_code == 302
    assert restored.headers["Location"] == "/projects"
    with app.app_context():
        database = get_db()
        project = database.execute(
            sa.select(projects).where(projects.c.id == archived_id)
        ).mappings().one()
        linked_task = database.execute(
            sa.select(tasks).where(tasks.c.id == linked_task_id)
        ).mappings().one()
    assert project["state"] == "active"
    assert project["revision"] == 2
    assert dict(linked_task) == before[0]
    assert _task_snapshot(app) == before


def test_project_assignment_and_creation_are_separate_and_return_to_context(
    app,
    client,
):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Write the launch email", "placement": "later"},
    )
    with app.app_context():
        database = get_db()
        task = database.execute(sa.select(tasks)).mappings().one()
        project_id = _insert_project(
            database,
            task["user_id"],
            "Launch",
            desired_outcome="Customers can use the release",
        )
        database.commit()

    detail = client.get(f"/tasks/{task['id']}?return_to=/later")

    assert detail.status_code == 200
    assert b"Add to an existing project" in detail.data
    assert b"Turn into a new project" in detail.data
    assert b"Add to existing project" in detail.data
    assert detail.data.count(b'name="return_to" value="/later"') == 2

    token = csrf_token(client, f"/tasks/{task['id']}?return_to=/later")
    assigned = client.post(
        f"/tasks/{task['id']}/project",
        data={
            "_csrf_token": token,
            "revision": str(task["revision"]),
            "project_id": str(project_id),
            "return_to": "/later",
        },
        follow_redirects=False,
    )

    assert assigned.status_code == 302
    assert assigned.headers["Location"] == (
        f"/tasks/{task['id']}?return_to=/later"
    )
    with app.app_context():
        updated = get_db().execute(
            sa.select(tasks).where(tasks.c.id == task["id"])
        ).mappings().one()
    assert updated["project_id"] == project_id
    assert updated["project_position"] == 0
    assert updated["revision"] == task["revision"] + 1

    before_noop = dict(updated)
    token = csrf_token(client, f"/tasks/{task['id']}?return_to=/later")
    noop = client.post(
        f"/tasks/{task['id']}/project",
        data={
            "_csrf_token": token,
            "revision": str(updated["revision"]),
            "project_id": str(project_id),
            "return_to": "/later",
        },
        follow_redirects=False,
    )
    assert noop.status_code == 302
    with app.app_context():
        after_noop = get_db().execute(
            sa.select(tasks).where(tasks.c.id == task["id"])
        ).mappings().one()
    assert dict(after_noop) == before_noop


def test_task_and_project_relationships_are_account_scoped(app, client):
    register(client)
    _post_with_csrf(client, "/tasks", {"title": "Mine", "placement": "later"})
    with app.app_context():
        mine_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()
        other_id = create_user(
            app,
            "Other",
            "other@example.com",
            generate_password_hash("other password"),
        )
        database = get_db()
        foreign_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=other_id,
                title="Foreign",
            )
            .returning(tasks.c.id)
        ).scalar_one()
        database.commit()

    assert client.get(f"/tasks/{foreign_id}").status_code == 404
    response = _post_with_csrf(
        client,
        f"/tasks/{mine_id}/dependencies",
        {"prerequisite_task_id": str(foreign_id)},
        page=f"/tasks/{mine_id}",
    )
    assert response.status_code == 404


def test_drop_is_deliberate_and_removes_task_from_active_view(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "An optional task", "placement": "today"},
    )
    with app.app_context():
        task_id = get_db().execute(sa.select(tasks.c.id)).scalar_one()

    confirmation = client.get(f"/tasks/{task_id}/drop?return_to=/today")
    assert confirmation.status_code == 200
    assert b'Type the task title exactly to confirm' in confirmation.data
    assert b'value="/today"' in confirmation.data

    rejected = _post_with_csrf(
        client,
        f"/tasks/{task_id}/drop",
        {
            "confirm_title": "A different title",
            "revision": "1",
            "return_to": "/today",
        },
    )
    assert rejected.status_code == 400
    assert b"Type the task title exactly to confirm." in rejected.data

    assert client.post(
        f"/tasks/{task_id}/drop",
        data={"confirm_title": "An optional task", "revision": "1"},
    ).status_code == 400

    response = _post_with_csrf(
        client,
        f"/tasks/{task_id}/drop",
        {
            "confirm_title": "An optional task",
            "revision": "1",
            "return_to": "/today",
        },
    )
    assert b"to Recently dropped. You can undo below." in response.data
    assert b'data-focus-task="An optional task"' not in response.data
    assert b"Undo \xe2\x80\x94 restore to Later" in response.data

    with app.app_context():
        task = (
            get_db()
            .execute(
                sa.select(
                    tasks.c.state,
                    tasks.c.workflow_status,
                    tasks.c.dropped_at,
                    tasks.c.revision,
                )
            )
            .mappings()
            .one()
        )
        assert task["state"] == "dropped"
        assert task["workflow_status"] == "dropped"
        assert task["dropped_at"] is not None
        assert task["revision"] == 2

    repeated = _post_with_csrf(
        client,
        f"/tasks/{task_id}/drop",
        {
            "confirm_title": "An optional task",
            "revision": "1",
        },
    )
    assert b"already in Recently dropped" in repeated.data
    with app.app_context():
        assert get_db().execute(
            sa.select(tasks.c.revision).where(tasks.c.id == task_id)
        ).scalar_one() == 2

    restored = _post_with_csrf(
        client,
        f"/tasks/{task_id}/restore",
        {"destination": "later", "revision": "2"},
        page="/recently-dropped",
    )
    assert (
        b"Restored \xe2\x80\x9cAn optional task\xe2\x80\x9d to Later."
        in restored.data
    )
    with app.app_context():
        task = (
            get_db()
            .execute(
                sa.select(
                    tasks.c.workflow_status,
                    tasks.c.today_placement,
                    tasks.c.planned_date,
                    tasks.c.dropped_at,
                    tasks.c.revision,
                )
            )
            .mappings()
            .one()
        )
    assert dict(task) == {
        "workflow_status": "open",
        "today_placement": "unplanned",
        "planned_date": None,
        "dropped_at": None,
        "revision": 3,
    }


def test_recently_dropped_shows_newest_ten_for_current_account(app, client):
    register(client)
    other_id = create_user(
        app,
        "Morgan",
        "morgan@example.com",
        generate_password_hash("another secure password"),
    )
    with app.app_context():
        database = get_db()
        installation_id = local_installation_id(database)
        user_id = database.execute(
            sa.select(users.c.id).where(users.c.email == "alex@example.com")
        ).scalar_one()
        database.execute(
            sa.insert(tasks),
            [
                {
                    "public_id": new_public_id(),
                    "origin_installation_id": installation_id,
                    "user_id": user_id,
                    "title": f"Dropped task {index:02d}",
                    "state": "dropped",
                    "workflow_status": "dropped",
                    "dropped_at": f"2026-07-28T12:{index:02d}:00",
                }
                for index in range(1, 12)
            ],
        )
        database.execute(
            sa.insert(tasks).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=other_id,
                title="Private dropped task",
                state="dropped",
                workflow_status="dropped",
                dropped_at="2026-07-28T13:00:00",
            )
        )
        database.commit()
        exported_titles = {
            task["title"] for task in export_account(database, user_id)["tasks"]
        }

    response = client.get("/recently-dropped")
    assert response.status_code == 200
    assert b"Dropped task 11" in response.data
    assert b"Dropped task 02" in response.data
    assert b"Dropped task 01" not in response.data
    assert b"Private dropped task" not in response.data
    assert "Dropped task 01" in exported_titles
    assert "Private dropped task" not in exported_titles
    positions = [
        response.data.index(f"Dropped task {index:02d}".encode())
        for index in range(11, 1, -1)
    ]
    assert positions == sorted(positions)


def test_restore_dropped_task_to_today_is_explicit_and_csrf_protected(app, client):
    register(client)
    with app.app_context():
        database = get_db()
        installation_id = local_installation_id(database)
        user_id = database.execute(
            sa.select(users.c.id).where(users.c.email == "alex@example.com")
        ).scalar_one()
        task_id = database.execute(
            sa.insert(tasks)
            .values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=user_id,
                title="Bring this back today",
                state="dropped",
                workflow_status="dropped",
                dropped_at="2026-07-28T12:00:00",
            )
            .returning(tasks.c.id)
        ).scalar_one()
        database.commit()

    assert client.post(
        f"/tasks/{task_id}/restore",
        data={"destination": "today", "revision": "1"},
    ).status_code == 400
    response = _post_with_csrf(
        client,
        f"/tasks/{task_id}/restore",
        {"destination": "today", "revision": "1"},
        page="/recently-dropped",
    )
    assert (
        b"Restored \xe2\x80\x9cBring this back today\xe2\x80\x9d to Today."
        in response.data
    )
    with app.app_context():
        task = (
            get_db()
            .execute(
                sa.select(
                    tasks.c.workflow_status,
                    tasks.c.today_placement,
                    tasks.c.planned_date,
                    tasks.c.dropped_at,
                ).where(tasks.c.id == task_id)
            )
            .mappings()
            .one()
        )
    assert dict(task) == {
        "workflow_status": "open",
        "today_placement": "active",
        "planned_date": date.today().isoformat(),
        "dropped_at": None,
    }


def test_drop_rejects_a_stale_confirmation_without_mutating(app, client):
    register(client)
    _post_with_csrf(
        client,
        "/tasks",
        {"title": "Original title", "placement": "later"},
    )
    with app.app_context():
        database = get_db()
        task_id = database.execute(sa.select(tasks.c.id)).scalar_one()
        database.execute(
            sa.update(tasks)
            .where(tasks.c.id == task_id)
            .values(title="Newer saved title", revision=2)
        )
        database.commit()

    response = _post_with_csrf(
        client,
        f"/tasks/{task_id}/drop",
        {"confirm_title": "Original title", "revision": "1"},
    )
    assert response.status_code == 409
    with app.app_context():
        task = (
            get_db()
            .execute(
                sa.select(
                    tasks.c.workflow_status,
                    tasks.c.dropped_at,
                    tasks.c.revision,
                ).where(tasks.c.id == task_id)
            )
            .mappings()
            .one()
        )
    assert dict(task) == {
        "workflow_status": "inbox",
        "dropped_at": None,
        "revision": 2,
    }


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
    response = _post_with_csrf(client, f"/tasks/{private_task_id}/restore")
    assert response.status_code == 404
    response = _post_with_csrf(client, f"/tasks/{private_task_id}/activate")
    assert response.status_code == 404
    response = _post_with_csrf(client, f"/tasks/{private_task_id}/later")
    assert response.status_code == 404
    with app.app_context():
        task = (
            get_db()
            .execute(sa.select(tasks.c.state).where(tasks.c.id == private_task_id))
            .mappings()
            .one()
        )
        assert task["state"] == "ready"
