#!/usr/bin/env python3
"""Create publication screenshots from a temporary synthetic installation."""

from __future__ import annotations

import struct
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from threading import Thread

import sqlalchemy as sa
from playwright.sync_api import Page, sync_playwright
from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server

from timemanager import create_app
from timemanager.db import get_db, local_installation_id, new_public_id
from timemanager.models import projects, remember_items, task_waits, tasks, users


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "assets"
SYNTHETIC_EMAIL = "sam@example.test"
SYNTHETIC_PASSWORD = "fictional screenshot password"
PNG_METADATA_CHUNKS = {b"eXIf", b"iTXt", b"tEXt", b"tIME", b"zTXt"}


def _insert_task(connection, installation_id: int, user_id: int, **values) -> int:
    defaults = {
        "public_id": new_public_id(),
        "origin_installation_id": installation_id,
        "user_id": user_id,
        "notes": "",
        "next_action": "",
        "definition_of_done": "",
        "state": "ready",
        "planned_date": None,
        "is_highlight": False,
        "project_id": None,
        "project_position": None,
        "workflow_status": "open",
        "today_placement": "unplanned",
        "dependency_override": False,
        "created_at": "2026-08-11 12:00:00",
        "updated_at": "2026-08-11 12:00:00",
    }
    defaults.update(values)
    return int(
        connection.execute(
            sa.insert(tasks).values(**defaults).returning(tasks.c.id)
        ).scalar_one()
    )


def _seed(app) -> None:
    today = date.today().isoformat()
    dropped_at = datetime(2026, 8, 11, 12, tzinfo=timezone.utc).isoformat()
    with app.app_context():
        connection = get_db()
        installation_id = local_installation_id(connection)
        user_id = int(
            connection.execute(
                sa.insert(users)
                .values(
                    public_id=new_public_id(),
                    origin_installation_id=installation_id,
                    display_name="Sam",
                    email=SYNTHETIC_EMAIL,
                    password_hash=generate_password_hash(SYNTHETIC_PASSWORD),
                )
                .returning(users.c.id)
            ).scalar_one()
        )

        connection.execute(
            sa.insert(remember_items).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=user_id,
                title="Refill the water bottle",
            )
        )

        _insert_task(
            connection,
            installation_id,
            user_id,
            title="Prepare the sample workshop",
            next_action="Open the fictional agenda",
            state="active",
            planned_date=today,
            is_highlight=True,
            workflow_status="open",
            today_placement="active",
        )
        for title, next_action in (
            ("Review example notes", "Read the first sample page"),
            ("Pack demo materials", "Put the blank cards in the bag"),
            ("Check the sample room", "Open the fictional booking"),
        ):
            _insert_task(
                connection,
                installation_id,
                user_id,
                title=title,
                next_action=next_action,
                state="active",
                planned_date=today,
                workflow_status="open",
                today_placement="active",
            )
        _insert_task(
            connection,
            installation_id,
            user_id,
            title="Draft a fictional follow-up",
            state="ready",
            planned_date=today,
            workflow_status="open",
            today_placement="overflow",
        )

        project_id = int(
            connection.execute(
                sa.insert(projects)
                .values(
                    public_id=new_public_id(),
                    origin_installation_id=installation_id,
                    user_id=user_id,
                    title="Publish the sample guide",
                    desired_outcome="A fictional guide is ready for a demo review.",
                )
                .returning(projects.c.id)
            ).scalar_one()
        )
        _insert_task(
            connection,
            installation_id,
            user_id,
            title="Outline the sample guide",
            next_action="Write three fictional headings",
            project_id=project_id,
            project_position=0,
        )
        waiting_task_id = _insert_task(
            connection,
            installation_id,
            user_id,
            title="Review the fictional print proof",
            project_id=project_id,
            project_position=1,
            workflow_status="waiting",
        )
        connection.execute(
            sa.insert(task_waits).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=user_id,
                task_id=waiting_task_id,
                reason="the sample proof",
                waiting_on="Example Print Studio",
                resume_status="open",
            )
        )
        _insert_task(
            connection,
            installation_id,
            user_id,
            title="Capture a made-up idea",
            state="inbox",
            workflow_status="inbox",
        )
        for title in ("Old fictional errand", "Unused sample checklist"):
            _insert_task(
                connection,
                installation_id,
                user_id,
                title=title,
                state="dropped",
                workflow_status="dropped",
                dropped_at=dropped_at,
            )

        connection.execute(
            sa.insert(projects).values(
                public_id=new_public_id(),
                origin_installation_id=installation_id,
                user_id=user_id,
                title="Archived sample project",
                desired_outcome="A completed fictional outcome.",
                state="completed",
            )
        )
        connection.commit()


def _login(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/login")
    page.get_by_label("Email").fill(SYNTHETIC_EMAIL)
    page.get_by_label("Password").fill(SYNTHETIC_PASSWORD)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url(f"{base_url}/today")


def _capture(page: Page, base_url: str, route: str, filename: str) -> Path:
    page.goto(f"{base_url}{route}")
    page.wait_for_load_state("networkidle")
    output = OUTPUT_DIR / filename
    page.screenshot(path=output, full_page=True)
    _strip_png_metadata(output)
    return output


def _strip_png_metadata(path: Path) -> None:
    source = path.read_bytes()
    if source[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")

    output = bytearray(source[:8])
    offset = 8
    while offset < len(source):
        length = struct.unpack(">I", source[offset : offset + 4])[0]
        chunk_end = offset + 12 + length
        chunk_type = source[offset + 4 : offset + 8]
        if chunk_type not in PNG_METADATA_CHUNKS:
            output.extend(source[offset:chunk_end])
        offset = chunk_end
        if chunk_type == b"IEND":
            break
    path.write_bytes(output)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="timemanager-synthetic-") as temp:
        database_path = Path(temp) / "synthetic.sqlite3"
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "synthetic-screenshot-session-key",
                "DATABASE": str(database_path),
                "DATABASE_URL": None,
                "ENABLE_PROTOTYPES": False,
            }
        )
        _seed(app)

        server = make_server("127.0.0.1", 0, app)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}"
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={"width": 1440, "height": 1000},
                    reduced_motion="reduce",
                )
                page = context.new_page()
                _login(page, base_url)
                outputs = [
                    _capture(page, base_url, "/today", "synthetic-today.png"),
                ]
                page.locator("[data-mode-toggle]").click()
                page.wait_for_timeout(100)
                low_capacity = OUTPUT_DIR / "synthetic-low-capacity.png"
                page.screenshot(path=low_capacity, full_page=True)
                _strip_png_metadata(low_capacity)
                outputs.append(low_capacity)
                outputs.extend(
                    (
                        _capture(page, base_url, "/later", "synthetic-later.png"),
                        _capture(page, base_url, "/projects", "synthetic-projects.png"),
                        _capture(
                            page,
                            base_url,
                            "/recently-dropped",
                            "synthetic-recently-dropped.png",
                        ),
                    )
                )
                page.set_viewport_size({"width": 390, "height": 844})
                page.goto(f"{base_url}/today")
                page.wait_for_load_state("networkidle")
                if page.locator("[data-show-full-today]").is_visible():
                    page.locator("[data-show-full-today]").click()
                mobile_today = OUTPUT_DIR / "synthetic-mobile-today.png"
                page.screenshot(path=mobile_today, full_page=True)
                _strip_png_metadata(mobile_today)
                outputs.append(mobile_today)
                context.close()
                browser.close()
        finally:
            server.shutdown()
            thread.join(timeout=5)

    for output in outputs:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
