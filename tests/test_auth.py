from __future__ import annotations

from werkzeug.security import check_password_hash

from timemanager.db import get_db

from .conftest import csrf_token, register


def test_anonymous_user_is_sent_to_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

    response = client.get("/today")
    assert response.status_code == 302
    assert "/login?next=/today" in response.headers["Location"]


def test_registration_creates_a_signed_in_user_with_hashed_password(app, client):
    response = register(
        client,
        name="  Alex Rivera  ",
        email="ALEX@Example.COM",
        password="something memorable",
    )

    assert response.status_code == 200
    assert b"Good to see you, Alex Rivera." in response.data
    assert b"Your calm space is ready." in response.data

    with app.app_context():
        user = get_db().execute("SELECT * FROM users").fetchone()
        assert user["email"] == "alex@example.com"
        assert user["password_hash"] != "something memorable"
        assert check_password_hash(user["password_hash"], "something memorable")

    with client.session_transaction() as session:
        assert session["user_id"] == user["id"]


def test_registration_validates_fields_and_duplicate_email(client):
    token = csrf_token(client, "/register")
    response = client.post(
        "/register",
        data={
            "_csrf_token": token,
            "display_name": "A",
            "email": "not-an-email",
            "password": "short",
            "confirm_password": "different",
        },
        follow_redirects=True,
    )
    assert b"Use a name between 2 and 40 characters." in response.data

    register(client)
    token = csrf_token(client, "/today")
    client.post("/logout", data={"_csrf_token": token})
    response = register(client, name="Other Alex", email="alex@example.com")
    assert b"An account with that email already exists." in response.data


def test_login_and_logout(client):
    register(client, password="a secure local password")
    token = csrf_token(client, "/today")
    client.post("/logout", data={"_csrf_token": token})

    token = csrf_token(client, "/login")
    wrong = client.post(
        "/login",
        data={
            "_csrf_token": token,
            "email": "alex@example.com",
            "password": "incorrect password",
        },
        follow_redirects=True,
    )
    assert b"That email and password combination was not found." in wrong.data

    token = csrf_token(client, "/login")
    response = client.post(
        "/login",
        data={
            "_csrf_token": token,
            "email": "alex@example.com",
            "password": "a secure local password",
        },
        follow_redirects=True,
    )
    assert b"Good to see you, Alex." in response.data

    token = csrf_token(client, "/today")
    response = client.post(
        "/logout",
        data={"_csrf_token": token},
        follow_redirects=True,
    )
    assert b"Sign in" in response.data


def test_post_requests_require_a_valid_csrf_token(client):
    response = client.post(
        "/register",
        data={
            "display_name": "Alex",
            "email": "alex@example.com",
            "password": "a calm password",
            "confirm_password": "a calm password",
        },
    )
    assert response.status_code == 400
