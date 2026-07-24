from __future__ import annotations

import re
from functools import wraps
from typing import Any, Callable, TypeVar, cast

import sqlalchemy as sa
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db, local_installation_id, new_public_id
from .models import users

blueprint = Blueprint("auth", __name__)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
View = TypeVar("View", bound=Callable[..., Any])


@blueprint.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        return

    g.user = (
        get_db()
        .execute(
            sa.select(users.c.id, users.c.display_name, users.c.email).where(
                users.c.id == user_id
            )
        )
        .mappings()
        .one_or_none()
    )
    if g.user is None:
        session.clear()


def login_required(view: View) -> View:
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return cast(View, wrapped_view)


@blueprint.route("/register", methods=("GET", "POST"))
def register():
    if g.user is not None:
        return redirect(url_for("tasks.today"))

    values = {"display_name": "", "email": ""}
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip().casefold()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        values = {"display_name": display_name, "email": email}

        error = _registration_error(display_name, email, password, confirm_password)
        if error is None:
            try:
                database = get_db()
                user_id = database.execute(
                    sa.insert(users)
                    .values(
                        public_id=new_public_id(),
                        origin_installation_id=local_installation_id(database),
                        display_name=display_name,
                        email=email,
                        password_hash=generate_password_hash(password),
                    )
                    .returning(users.c.id)
                ).scalar_one()
                database.commit()
            except IntegrityError:
                database.rollback()
                error = "An account with that email already exists."
            else:
                session.clear()
                session["user_id"] = user_id
                flash("Your calm space is ready.", "success")
                return redirect(url_for("tasks.today"))

        flash(error, "error")

    return render_template("auth/register.html", values=values)


def _registration_error(
    display_name: str,
    email: str,
    password: str,
    confirm_password: str,
) -> str | None:
    if len(display_name) < 2 or len(display_name) > 40:
        return "Use a name between 2 and 40 characters."
    if len(email) > 254 or not EMAIL_PATTERN.match(email):
        return "Enter a valid email address."
    if len(password) < 10:
        return "Use at least 10 characters for your password."
    if password != confirm_password:
        return "The passwords do not match."
    return None


@blueprint.route("/login", methods=("GET", "POST"))
def login():
    if g.user is not None:
        return redirect(url_for("tasks.today"))

    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().casefold()
        password = request.form.get("password", "")
        user = (
            get_db()
            .execute(sa.select(users).where(users.c.email == email))
            .mappings()
            .one_or_none()
        )

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("That email and password combination was not found.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            destination = request.args.get("next", "")
            if not destination.startswith("/") or destination.startswith("//"):
                destination = url_for("tasks.today")
            return redirect(destination)

    return render_template("auth/login.html", email=email)


@blueprint.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
