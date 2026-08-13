from __future__ import annotations

from urllib.parse import urlsplit

from flask import redirect


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


def redirect_to_local_path(value: str | None, fallback: str):
    """Redirect to an explicitly validated origin-local absolute path."""
    if not value:
        return redirect(fallback)

    normalized = value.replace("\\", "/")
    if normalized != value:
        return redirect(fallback)
    if not normalized.startswith("/") or normalized.startswith("//"):
        return redirect(fallback)
    if any(character in normalized for character in ("\r", "\n")):
        return redirect(fallback)

    parsed = urlsplit(normalized)
    if parsed.scheme or parsed.netloc:
        return redirect(fallback)
    return redirect(normalized)
