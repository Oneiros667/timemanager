from __future__ import annotations

from urllib.parse import urlsplit


def local_return_path(value: str | None, fallback: str) -> str:
    """Return only an origin-local absolute path suitable for redirects."""
    if not value or not value.startswith("/") or value.startswith("//"):
        return fallback
    if "\\" in value or any(character in value for character in ("\r", "\n")):
        return fallback

    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return fallback
    return value
