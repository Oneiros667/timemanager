from __future__ import annotations

import re

import pytest
import sqlalchemy as sa

from timemanager import create_app
from timemanager.db import get_db, local_installation_id, new_public_id
from timemanager.models import users

CSRF_PATTERN = re.compile(rb'name="_csrf_token" value="([^"]+)"')


@pytest.fixture()
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def csrf_token(client, path: str = "/login") -> str:
    response = client.get(path)
    match = CSRF_PATTERN.search(response.data)
    assert match is not None, f"No CSRF token found at {path}"
    return match.group(1).decode()


def register(
    client,
    *,
    name: str = "Alex",
    email: str = "alex@example.com",
    password: str = "a calm password",
):
    token = csrf_token(client, "/register")
    return client.post(
        "/register",
        data={
            "_csrf_token": token,
            "display_name": name,
            "email": email,
            "password": password,
            "confirm_password": password,
        },
        follow_redirects=True,
    )


def create_user(app, name: str, email: str, password_hash: str) -> int:
    with app.app_context():
        database = get_db()
        user_id = database.execute(
            sa.insert(users)
            .values(
                public_id=new_public_id(),
                origin_installation_id=local_installation_id(database),
                display_name=name,
                email=email,
                password_hash=password_hash,
            )
            .returning(users.c.id)
        ).scalar_one()
        database.commit()
        return int(user_id)
