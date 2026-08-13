from __future__ import annotations

import pytest

from timemanager.security import local_return_path, redirect_to_local_path


@pytest.mark.parametrize(
    "candidate",
    (
        None,
        "",
        "relative/path",
        "https://example.net/collect",
        "//example.net/collect",
        "/\\example.net/collect",
        "/safe\r\nLocation: https://example.net/collect",
    ),
)
def test_local_redirect_helpers_reject_non_local_paths(app, candidate):
    fallback = "/today"

    assert local_return_path(candidate, fallback) == fallback
    with app.test_request_context():
        response = redirect_to_local_path(candidate, fallback)

    assert response.status_code == 302
    assert response.headers["Location"] == fallback


def test_local_redirect_helpers_retain_paths_queries_and_fragments(app):
    candidate = "/projects?page=2#active"

    assert local_return_path(candidate, "/today") == candidate
    with app.test_request_context():
        response = redirect_to_local_path(candidate, "/today")

    assert response.status_code == 302
    assert response.headers["Location"] == candidate
