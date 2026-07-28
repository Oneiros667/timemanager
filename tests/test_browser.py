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
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
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


def test_task_can_be_turned_into_a_project_in_one_confirmed_flow(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Plan the launch")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()

    page.locator("summary").filter(has_text="Turn into a project").click()
    project_name = page.get_by_label("Project name")
    expect(project_name).to_have_value("Plan the launch")
    project_name.fill("Website launch")
    page.get_by_role("button", name="Turn into a project").click()

    expect(page.get_by_label("Project title")).to_have_value("Website launch")
    expect(
        page.locator(".next-ready-card").get_by_role("link", name="Plan the launch")
    ).to_be_visible()
    assert "/projects/" in page.url


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


def test_edit_during_delayed_save_keeps_and_saves_the_newer_draft(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Call supplier")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()
    page.evaluate(
        """
        () => {
          const originalFetch = window.fetch.bind(window);
          let delayed = false;
          window.fetch = (...args) => {
            if (delayed) return originalFetch(...args);
            delayed = true;
            return new Promise((resolve, reject) => {
              window.setTimeout(
                () => originalFetch(...args).then(resolve, reject),
                1200,
              );
            });
          };
        }
        """
    )

    next_action = page.get_by_label("Next action")
    next_action.fill("First thought")
    expect(page.get_by_text("Saving…", exact=True)).to_be_visible()
    next_action.fill("Newer thought while saving")

    expect(page.get_by_text("Saved", exact=True)).to_be_visible(timeout=5000)
    page.reload()
    expect(page.get_by_label("Next action")).to_have_value(
        "Newer thought while saving"
    )


def test_task_workspace_draft_survives_immediate_reload_and_clears_after_save(
    page,
    live_url,
):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Prepare report")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()
    page.on("dialog", lambda dialog: dialog.accept())

    next_action = page.get_by_label("Next action")
    next_action.fill("Open the figures before the interruption")
    page.reload()

    expect(page.get_by_label("Next action")).to_have_value(
        "Open the figures before the interruption"
    )
    expect(page.get_by_text("Unsaved draft restored.")).to_be_visible()
    page.get_by_role("button", name="Save now").click()
    expect(page.get_by_text("Saved", exact=True)).to_be_visible()
    assert page.evaluate(
        "Object.keys(localStorage).filter((key) => "
        "key.startsWith('timemanager-draft-v1:')).length"
    ) == 0

    page.reload()
    expect(page.get_by_label("Next action")).to_have_value(
        "Open the figures before the interruption"
    )


def test_task_workspace_draft_survives_navigation_and_page_close(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Prepare report")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()
    task_url = page.url
    page.on("dialog", lambda dialog: dialog.accept())
    page.route(
        "**/tasks/*/details",
        lambda route: (
            route.abort()
            if route.request.method == "POST"
            else route.continue_()
        ),
    )

    page.get_by_label("Next action").fill("Return to this exact thought")
    page.get_by_role("link", name="Back").click()
    page.goto(task_url)
    expect(page.get_by_label("Next action")).to_have_value(
        "Return to this exact thought"
    )

    context = page.context
    page.close()
    reopened = context.new_page()
    reopened.goto(task_url)
    expect(reopened.get_by_label("Next action")).to_have_value(
        "Return to this exact thought"
    )
    expect(reopened.get_by_text("Unsaved draft restored.")).to_be_visible()


def test_inline_and_project_drafts_restore_in_their_existing_context(page, live_url):
    _register(page, live_url)
    page.on("dialog", lambda dialog: dialog.accept())

    page.get_by_placeholder("What do you need to remember?").fill("Plan the launch")
    page.get_by_role("button", name="Add to today").click()
    page.get_by_role("button", name="Edit").click()
    editor = page.locator("[data-inline-edit]:visible")
    editor.get_by_label("Next action").fill("Open the launch checklist")
    page.reload()

    restored_editor = page.locator("[data-inline-edit]:visible")
    expect(restored_editor.get_by_label("Next action")).to_have_value(
        "Open the launch checklist"
    )
    restored_editor.get_by_role("button", name="Save now").click()
    expect(restored_editor.get_by_text("Saved", exact=True)).to_be_visible()

    page.get_by_role("link", name="Plan the launch").click()
    page.locator("summary").filter(has_text="Turn into a project").click()
    page.get_by_role("button", name="Turn into a project").click()
    outcome = page.get_by_label("Outcome")
    outcome.fill("The first release is available")
    page.reload()

    expect(page.get_by_label("Outcome")).to_have_value(
        "The first release is available"
    )
    expect(page.get_by_text("Unsaved draft restored.")).to_be_visible()


def test_sign_out_clears_account_scoped_drafts(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Call supplier")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()
    page.get_by_label("Next action").fill("Find the order number")

    assert page.evaluate(
        "Object.keys(localStorage).filter((key) => "
        "key.startsWith('timemanager-draft-v1:')).length"
    ) == 1
    page.get_by_role("button", name="Sign out").click()
    page.wait_for_url(f"{live_url}/login")
    assert page.evaluate(
        "Object.keys(localStorage).filter((key) => "
        "key.startsWith('timemanager-draft-v1:')).length"
    ) == 0


def test_expired_draft_is_removed_without_replacing_saved_fields(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Call supplier")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()
    page.evaluate(
        """
        () => {
          const form = document.querySelector("[data-autosave-form]");
          const account = document.body.dataset.draftAccount;
          const key = `timemanager-draft-v1:${account}:${form.dataset.draftScope}:fixture`;
          localStorage.setItem(key, JSON.stringify({
            version: 1,
            savedAt: Date.now() - (25 * 60 * 60 * 1000),
            revision: Number(form.querySelector("[data-revision]").value),
            requiresExplicitSave: false,
            fields: {
              title: "Expired title",
              next_action: "Expired action",
              definition_of_done: "",
              notes: "",
            },
          }));
          localStorage.setItem(
            `timemanager-draft-v1:${account}:task:unrelated-expired:inline:fixture`,
            JSON.stringify({
              version: 1,
              savedAt: Date.now() - (25 * 60 * 60 * 1000),
              revision: 1,
              requiresExplicitSave: false,
              fields: {title: "Also expired"},
            }),
          );
          localStorage.setItem(
            `timemanager-draft-v1:${account}:task:unrelated-current:inline:fixture`,
            JSON.stringify({
              version: 1,
              savedAt: Date.now(),
              revision: 1,
              requiresExplicitSave: false,
              fields: {title: "Still current"},
            }),
          );
        }
        """
    )

    page.reload()

    expect(page.get_by_label("Task title")).to_have_value("Call supplier")
    expect(page.get_by_label("Next action")).to_have_value("")
    draft_keys = page.evaluate(
        "Object.keys(localStorage).filter((key) => "
        "key.startsWith('timemanager-draft-v1:'))"
    )
    assert len(draft_keys) == 1
    assert ":task:unrelated-current:inline:" in draft_keys[0]


def test_stale_draft_requires_an_explicit_conflict_choice(page, live_url):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Call supplier")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()

    page.evaluate(
        """
        () => {
          const form = document.querySelector("[data-autosave-form]");
          const account = document.body.dataset.draftAccount;
          const key = `timemanager-draft-v1:${account}:${form.dataset.draftScope}:fixture`;
          localStorage.setItem(key, JSON.stringify({
            version: 1,
            savedAt: Date.now(),
            revision: Number(form.querySelector("[data-revision]").value),
            requiresExplicitSave: false,
            fields: {
              title: "Call supplier",
              next_action: "Use the interrupted draft",
              definition_of_done: "",
              notes: "",
            },
          }));
        }
        """
    )
    page.evaluate(
        """
        async () => {
          const form = document.querySelector("[data-autosave-form]");
          const data = new FormData(form);
          data.set("title", "Call supplier from the saved copy");
          data.set("next_action", "Use the server copy");
          const response = await fetch(form.action, {
            method: "POST",
            body: data,
            headers: {
              Accept: "application/json",
              "X-Requested-With": "fetch",
            },
          });
          if (!response.ok) throw new Error("fixture update failed");
        }
        """
    )

    page.reload()

    expect(page.get_by_label("Next action")).to_have_value(
        "Use the interrupted draft"
    )
    expect(page.get_by_text("Saved version changed.", exact=False)).to_be_visible()
    page.get_by_role("button", name="Discard draft").click()
    expect(page.get_by_label("Task title")).to_have_value(
        "Call supplier from the saved copy"
    )
    expect(page.get_by_label("Next action")).to_have_value("Use the server copy")


def test_concurrent_tabs_keep_separate_drafts_and_expose_revision_conflict(
    page,
    live_url,
):
    _register(page, live_url)
    page.get_by_placeholder("What do you need to remember?").fill("Call supplier")
    page.get_by_role("button", name="Add to Later").click()
    page.get_by_role("link", name="Add details").click()
    task_url = page.url

    other_tab = page.context.new_page()
    other_tab.goto(task_url)

    page.route("**/tasks/*/details", lambda route: route.abort())
    page.get_by_label("Next action").fill("Keep the first tab draft")
    expect(page.get_by_role("button", name="Couldn’t save — Retry")).to_be_visible()

    other_tab.get_by_label("Task title").fill("Saved from the second tab")
    other_tab.get_by_label("Task title").blur()
    expect(other_tab.get_by_text("Saved", exact=True)).to_be_visible()

    draft_keys = page.evaluate(
        "Object.keys(localStorage).filter((key) => "
        "key.startsWith('timemanager-draft-v1:'))"
    )
    assert len(draft_keys) == 1

    page.unroute("**/tasks/*/details")
    page.on("dialog", lambda dialog: dialog.accept())
    page.reload()

    expect(page.get_by_label("Next action")).to_have_value(
        "Keep the first tab draft"
    )
    expect(
        page.get_by_text("Draft restored but not saved.", exact=False)
    ).to_be_visible()
    page.get_by_role("button", name="Discard draft").click()
    expect(page.get_by_label("Task title")).to_have_value("Saved from the second tab")
    assert page.evaluate(
        "Object.keys(localStorage).filter((key) => "
        "key.startsWith('timemanager-draft-v1:')).length"
    ) == 0
