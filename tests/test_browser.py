from __future__ import annotations

from threading import Thread

import pytest
from playwright.sync_api import Page, expect, sync_playwright
from werkzeug.serving import make_server

from timemanager import create_app


@pytest.fixture()
def live_url(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "browser-test-secret",
            "DATABASE": str(tmp_path / "browser.sqlite3"),
            "ENABLE_PROTOTYPES": True,
        }
    )
    server = make_server("127.0.0.1", 0, app)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


def _register(page: Page, live_url: str) -> None:
    page.goto(f"{live_url}/register")
    page.get_by_label("What should we call you?").fill("Alex")
    page.get_by_label("Email").fill("alex@example.com")
    page.locator("input[name=password]").fill("a calm password")
    page.locator("input[name=confirm_password]").fill("a calm password")
    page.get_by_role("button", name="Create account").click()
    page.wait_for_url(f"{live_url}/today")


def test_remember_is_beside_quick_capture_and_clears_checked_items(page, live_url):
    page.set_viewport_size({"width": 1280, "height": 900})
    _register(page, live_url)

    capture_box = page.locator(".capture-card").bounding_box()
    remember_box = page.locator(".remember-card").bounding_box()
    assert capture_box is not None
    assert remember_box is not None
    assert abs(capture_box["y"] - remember_box["y"]) < 2
    assert capture_box["x"] < remember_box["x"]

    page.get_by_label("Add a short-term reminder").fill("Get coffee")
    page.get_by_role("button", name="Add", exact=True).click()
    expect(page.get_by_text("Get coffee", exact=True)).to_be_visible()
    page.get_by_role("button", name="Done: Get coffee").click()
    expect(page.get_by_text("Get coffee", exact=True)).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 844})
    capture_box = page.locator(".capture-card").bounding_box()
    remember_box = page.locator(".remember-card").bounding_box()
    assert capture_box is not None
    assert remember_box is not None
    assert remember_box["y"] > capture_box["y"]


def test_synthetic_prototype_is_keyboard_operable_and_responsive(page, live_url):
    page.set_viewport_size({"width": 390, "height": 844})
    page.emulate_media(reduced_motion="reduce")
    page.goto(f"{live_url}/prototypes/complex-work")

    assert page.get_by_text("Synthetic prototype").is_visible()
    assert page.evaluate("navigator.serviceWorker?.controller ?? null") is None
    capture = page.get_by_placeholder("What do you need to remember?")
    capture.fill("Sort this out")
    capture.press("Enter")
    expect(page.get_by_role("button", name="Add details")).to_be_visible()
    page.get_by_role("button", name="Low capacity").click()
    expect(page.locator('[data-prototype-panel="today"] .is-blocked')).to_be_hidden()
    page.get_by_role("button", name="Standard view").click()
    page.get_by_role("button", name="Task", exact=True).click()
    step = page.get_by_placeholder("Add a step, then press Enter")
    step.fill("Check the date range")
    step.press("Enter")
    assert page.get_by_text("Check the date range", exact=True).is_visible()

    page.get_by_role("button", name="Project", exact=True).click()
    task = page.get_by_placeholder("Type a task, then press Enter")
    task.fill("Check confirmation email")
    task.press("Enter")
    assert page.get_by_text("Check confirmation email", exact=True).is_visible()
    assert page.get_by_text("Next ready", exact=True).is_visible()


def test_capture_task_workspace_autosave_and_rapid_steps(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Prepare report")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()

    assert page.get_by_text("Start here").is_visible()
    next_action = page.get_by_label("Next action")
    next_action.fill("Open the figures")
    next_action.blur()
    save_state = page.locator("[data-save-state]")
    page.wait_for_timeout(1000)
    assert save_state.get_by_text("Saved", exact=True).is_visible(), save_state.inner_text()

    step = page.get_by_placeholder("Add a step, then press Enter")
    step.fill("Check totals")
    step.press("Enter")
    expect(page.get_by_text("Check totals", exact=True)).to_be_visible()
    expect(step).to_be_focused()
    expect(page.get_by_role("button", name="Complete Check totals")).to_be_visible()
    for title in ("Confirm date", "Attach chart", "Send report"):
        step.fill(title)
        step.press("Enter")
        expect(page.get_by_text(f"Added “{title}”", exact=True)).to_be_visible()
    expect(page.get_by_text("Send report", exact=True)).to_be_hidden()
    page.get_by_text("1 more step", exact=True).click()
    expect(page.get_by_text("Send report", exact=True)).to_be_visible()
    page.get_by_role("button", name="Start focus").click()
    expect(page.get_by_role("dialog", name="Prepare report")).to_be_visible()


def test_inline_edit_retains_list_context(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Draft report")
    page.get_by_role("button", name="Add to today").click()
    page.get_by_role("button", name="Edit").click()
    editor = page.locator("[data-inline-edit]:visible")
    editor.get_by_label("Next action").fill("Open the document")
    editor.get_by_label("Next action").blur()
    expect(editor.get_by_text("Saved", exact=True)).to_be_visible()
    assert page.url == f"{live_url}/today?created=1"


def test_today_and_later_navigation_shows_the_current_view(page, live_url):
    _register(page, live_url)
    primary = page.get_by_role("navigation", name="Primary views")
    expect(primary.get_by_role("link", name="Today")).to_have_attribute(
        "aria-current", "page"
    )
    expect(primary.get_by_role("link", name="Later")).not_to_have_attribute(
        "aria-current", "page"
    )

    primary.get_by_role("link", name="Later").click()
    page.wait_for_url(f"{live_url}/later")
    expect(page.get_by_role("heading", name="Captured", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Later", exact=True)).to_be_visible()
    expect(
        page.get_by_role("heading", name="Ready and waiting", exact=True)
    ).to_be_visible()
    expect(primary.get_by_role("link", name="Later")).to_have_attribute(
        "aria-current", "page"
    )


def test_failed_autosave_keeps_the_edit_and_can_retry(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Call supplier")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()

    page.route("**/tasks/*/details", lambda route: route.abort())
    next_action = page.get_by_label("Next action")
    next_action.fill("Find the order number")
    next_action.blur()
    retry = page.get_by_role("button", name="Couldn’t save — Retry")
    expect(retry).to_be_visible()
    expect(next_action).to_have_value("Find the order number")

    page.unroute("**/tasks/*/details")
    retry.click()
    expect(page.get_by_text("Saved", exact=True)).to_be_visible()
    page.reload()
    expect(page.get_by_label("Next action")).to_have_value("Find the order number")
