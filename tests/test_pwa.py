from __future__ import annotations

import json

from .conftest import register


def test_manifest_has_installable_pwa_metadata(client):
    response = client.get("/manifest.webmanifest")
    assert response.status_code == 200
    assert response.mimetype == "application/manifest+json"

    manifest = json.loads(response.data)
    assert manifest["name"] == "Timemanager"
    assert manifest["start_url"] == "/"
    assert manifest["display"] == "standalone"
    icon_sizes = {icon["sizes"] for icon in manifest["icons"]}
    assert {"192x192", "512x512"} <= icon_sizes

    for icon in manifest["icons"]:
        icon_response = client.get(icon["src"])
        assert icon_response.status_code == 200
        assert icon_response.mimetype == "image/png"


def test_service_worker_controls_the_app_shell(client):
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert response.mimetype == "application/javascript"
    assert response.headers["Service-Worker-Allowed"] == "/"
    assert b"/offline" in response.data
    assert b"timemanager-shell-v3" in response.data

    offline = client.get("/offline")
    assert offline.status_code == 200
    assert b"Connection paused" in offline.data
    assert b"Nothing has been marked late or missed." in offline.data


def test_pages_link_manifest_and_include_security_headers(client):
    response = client.get("/login")
    assert b'rel="manifest"' in response.data
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]

    response = register(client)
    assert b"/static/app.js" in response.data
    assert b"Low capacity" in response.data
    assert b"Get it out of your head" in response.data
