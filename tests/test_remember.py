from __future__ import annotations

import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from timemanager.db import get_db, local_installation_id, new_public_id
from timemanager.models import remember_items

from .conftest import create_user, csrf_token, register


def _post(client, path: str, data: dict | None = None):
    payload = {"_csrf_token": csrf_token(client, "/today")}
    payload.update(data or {})
    return client.post(path, data=payload, follow_redirects=True)


def test_remember_panel_adds_up_to_three_short_term_items(app, client):
    response = register(client)
    start_grid = response.data.split(b'<div class="today-start-grid">', 1)[1].split(
        b'<div class="day-grid">', 1
    )[0]
    assert start_grid.index(b"Quick capture") < start_grid.index(b"Remember")
    assert response.data.index(b"Remember") < response.data.index(b"Right now")
    assert b"not part of your task plan" in response.data

    for title in ("  Get   coffee ", "Bring charger", "Ask Sam"):
        response = _post(client, "/remember", {"title": title})

    assert b"Get coffee" in response.data
    assert b"Bring charger" in response.data
    assert b"Ask Sam" in response.data
    assert b"3/3" in response.data
    assert b'id="remember-title"' in response.data
    remember_input = response.data.split(b'id="remember-title"', 1)[1].split(b">", 1)[0]
    assert b"disabled" in remember_input

    response = _post(client, "/remember", {"title": "Fourth item"})
    assert b"Remember can hold three items" in response.data
    assert b"Fourth item" not in response.data

    with app.app_context():
        titles = get_db().execute(
            sa.select(remember_items.c.title).order_by(remember_items.c.id)
        ).scalars().all()
    assert titles == ["Get coffee", "Bring charger", "Ask Sam"]


def test_checking_a_remember_item_removes_it(app, client):
    register(client)
    _post(client, "/remember", {"title": "Get coffee"})
    with app.app_context():
        item_id = get_db().execute(sa.select(remember_items.c.id)).scalar_one()

    response = _post(client, f"/remember/{item_id}/complete")

    assert b"<span>Get coffee</span>" not in response.data
    assert b"Nothing to hold in mind right now" in response.data
    with app.app_context():
        assert get_db().execute(
            sa.select(sa.func.count()).select_from(remember_items)
        ).scalar_one() == 0


def test_remember_mutations_require_csrf_and_account_ownership(app, client):
    register(client)
    assert client.post("/remember", data={"title": "No token"}).status_code == 400

    other_user_id = create_user(
        app,
        "Other",
        "other@example.com",
        generate_password_hash("other-password"),
    )
    with app.app_context():
        database = get_db()
        item_id = database.execute(
            sa.insert(remember_items)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                user_id=other_user_id,
                title="Other account reminder",
            )
            .returning(remember_items.c.id)
        ).scalar_one()
        database.commit()

    token = csrf_token(client, "/today")
    response = client.post(
        f"/remember/{item_id}/complete",
        data={"_csrf_token": token},
    )
    assert response.status_code == 404
    with app.app_context():
        assert get_db().execute(
            sa.select(remember_items.c.title).where(remember_items.c.id == item_id)
        ).scalar_one() == "Other account reminder"
