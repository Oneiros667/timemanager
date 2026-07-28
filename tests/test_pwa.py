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


def test_service_worker_controls_the_app_shell(app, client):
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert response.mimetype == "application/javascript"
    assert response.headers["Service-Worker-Allowed"] == "/"
    assert b"/offline" in response.data
    assert b"timemanager-shell-v6" in response.data
    assert b"/static/styles.css?v=6" in response.data
    assert b"/static/app.js?v=6" in response.data
    assert f"?v={app.config['STATIC_ASSET_VERSION']}".encode() in response.data
    assert b"await cache.put(event.request, response.clone())" in response.data

    offline = client.get("/offline")
    assert offline.status_code == 200
    assert b"Connection paused" in offline.data
    assert b"Nothing has been marked late or missed." in offline.data
    assert b"/static/styles.css?v=6" in offline.data


def test_pages_link_manifest_and_include_security_headers(client):
    response = client.get("/login")
    assert b'rel="manifest"' in response.data
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]

    response = register(client)
    assert b"/static/styles.css?v=6" in response.data
    assert b"/static/app.js?v=6" in response.data
    assert b"Low capacity" in response.data
    assert response.data.count(b"Quick capture") == 1


def test_complex_work_prototype_is_disabled_by_default(client):
    assert client.get("/prototypes/complex-work").status_code == 404


def test_complex_work_prototype_is_synthetic_and_no_store(app):
    app.config["ENABLE_PROTOTYPES"] = True
    client = app.test_client()

    response = client.get("/prototypes/complex-work")

    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert b"Synthetic prototype" in response.data
    assert b"Reset scenario" in response.data
    assert b"prototype-complex-work.js" in response.data
