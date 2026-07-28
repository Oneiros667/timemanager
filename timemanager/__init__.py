from __future__ import annotations

import hmac
import os
import secrets
from pathlib import Path
from typing import Any

from flask import Flask, abort, redirect, request, send_from_directory, session, url_for


def _local_secret(instance_path: str) -> str:
    configured = os.environ.get("TIMEMANAGER_SECRET_KEY")
    if configured:
        return configured

    secret_path = Path(instance_path) / ".secret-key"
    if secret_path.exists():
        return secret_path.read_text(encoding="utf-8").strip()

    secret = secrets.token_hex(32)
    descriptor = os.open(secret_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as secret_file:
        secret_file.write(secret)
    return secret


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        DATABASE=os.environ.get(
            "TIMEMANAGER_DATABASE",
            str(Path(app.instance_path) / "timemanager.sqlite3"),
        ),
        DATABASE_URL=os.environ.get("TIMEMANAGER_DATABASE_URL"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        MAX_CONTENT_LENGTH=64 * 1024,
        ENABLE_PROTOTYPES=os.environ.get("TIMEMANAGER_ENABLE_PROTOTYPES") == "1",
        STATIC_ASSET_VERSION="10",
    )

    if test_config is None:
        app.config["SECRET_KEY"] = _local_secret(app.instance_path)
    else:
        app.config.update(test_config)

    from . import account_transfer, auth, db, prototype, remember, tasks

    db.init_app(app)
    account_transfer.init_app(app)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(tasks.blueprint)
    app.register_blueprint(remember.blueprint)
    app.register_blueprint(prototype.blueprint)

    with app.app_context():
        db.init_db()

    @app.before_request
    def protect_forms() -> None:
        if request.method != "POST":
            return
        expected = session.get("_csrf_token", "")
        supplied = request.form.get("_csrf_token", "")
        if not expected or not supplied or not hmac.compare_digest(expected, supplied):
            abort(400, description="This form expired. Please go back and try again.")

    @app.context_processor
    def inject_csrf_token() -> dict[str, Any]:
        def csrf_token() -> str:
            token = session.get("_csrf_token")
            if token is None:
                token = secrets.token_urlsafe(32)
                session["_csrf_token"] = token
            return token

        return {
            "asset_version": app.config["STATIC_ASSET_VERSION"],
            "csrf_token": csrf_token,
        }

    @app.after_request
    def secure_response(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self'; "
            "script-src 'self'; "
            "connect-src 'self'; "
            "manifest-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'",
        )
        return response

    @app.get("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("tasks.today"))
        return redirect(url_for("auth.login"))

    @app.get("/offline")
    def offline():
        return send_from_directory(app.static_folder, "offline.html")

    @app.get("/manifest.webmanifest")
    def manifest():
        return send_from_directory(
            app.static_folder,
            "manifest.webmanifest",
            mimetype="application/manifest+json",
        )

    @app.get("/sw.js")
    def service_worker():
        response = send_from_directory(
            app.static_folder,
            "sw.js",
            mimetype="application/javascript",
        )
        response.headers["Service-Worker-Allowed"] = "/"
        response.headers["Cache-Control"] = "no-cache"
        return response

    return app
