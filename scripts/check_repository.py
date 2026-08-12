#!/usr/bin/env python3
"""Check publication hygiene that can be verified without external services."""

from __future__ import annotations

import re
import struct
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EXPORT_FIXTURES = {"tests/fixtures/account_export_v1.json"}
SELF_PATH = "scripts/check_repository.py"
FORBIDDEN_PARTS = {
    ".env",
    ".pytest_cache",
    "blob-report",
    "coverage",
    "htmlcov",
    "instance",
    "logs",
    "playwright-report",
    "test-results",
    "traces",
}
FORBIDDEN_SUFFIXES = {
    ".bak",
    ".cer",
    ".crt",
    ".db",
    ".har",
    ".key",
    ".log",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite3",
}
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".lock",
    ".md",
    ".mako",
    ".py",
    ".sql",
    ".svg",
    ".toml",
    ".txt",
    ".webmanifest",
    ".yml",
    ".yaml",
}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub token": re.compile(r"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{20,}"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "credential-bearing database URL": re.compile(
        r"(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s/:]+:[^\s/@]+@"
    ),
}
ABSOLUTE_PRIVATE_PATH = re.compile(r"(?:/home/[^/\s]+|/Users/[^/\s]+)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ACTION_USE = re.compile(r"^\s*uses:\s*[^#\s]+@([^#\s]+)", re.MULTILINE)
PNG_TEXT_CHUNKS = {b"eXIf", b"iTXt", b"tEXt", b"tIME", b"zTXt"}


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths = [ROOT / path.decode() for path in result.stdout.split(b"\0") if path]
    return [path for path in paths if path.exists()]


def check_tracked_names(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        parts = {part.casefold() for part in path.relative_to(ROOT).parts}
        if parts & FORBIDDEN_PARTS or path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden generated or sensitive path: {relative}")
        if (
            path.suffix.casefold() == ".json"
            and "account" in path.name.casefold()
            and "export" in path.name.casefold()
            and relative not in ALLOWED_EXPORT_FIXTURES
        ):
            failures.append(f"unexpected account-export-shaped path: {relative}")
    return failures


def read_text(path: Path) -> str | None:
    if path.suffix.casefold() not in TEXT_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def check_text(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative == SELF_PATH:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{label} pattern: {relative}")
        if ABSOLUTE_PRIVATE_PATH.search(text):
            failures.append(f"local absolute path: {relative}")
        for match in EMAIL.finditer(text):
            allowed_domains = {
                "example.com",
                "example.net",
                "example.org",
                "example.test",
            }
            if match.group(1).casefold() not in allowed_domains:
                failures.append(f"non-example email address: {relative}")
                break
    return failures


def check_markdown_links(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        if path.suffix.casefold() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_part = unquote(target.split("#", 1)[0])
            if local_part and not (path.parent / local_part).resolve().exists():
                failures.append(
                    f"missing Markdown link target in {path.relative_to(ROOT)}: {target}"
                )
    return failures


def png_chunks(path: Path) -> set[bytes]:
    chunks: set[bytes] = set()
    with path.open("rb") as image:
        if image.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG file")
        while True:
            header = image.read(8)
            if len(header) != 8:
                raise ValueError("truncated PNG file")
            length, chunk_type = struct.unpack(">I4s", header)
            image.seek(length + 4, 1)
            chunks.add(chunk_type)
            if chunk_type == b"IEND":
                return chunks


def check_png_metadata(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        if path.suffix.casefold() != ".png":
            continue
        forbidden = png_chunks(path) & PNG_TEXT_CHUNKS
        if forbidden:
            labels = ", ".join(sorted(chunk.decode() for chunk in forbidden))
            failures.append(
                f"PNG contains text/time metadata ({labels}): {path.relative_to(ROOT)}"
            )
    return failures


def check_action_pins(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        if path.suffix.casefold() not in {".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for reference in ACTION_USE.findall(text):
            if not re.fullmatch(r"[0-9a-f]{40}", reference):
                failures.append(
                    f"GitHub Action is not pinned to a full commit SHA: {path.relative_to(ROOT)}"
                )
    return failures


def main() -> int:
    paths = candidate_files()
    failures = [
        *check_tracked_names(paths),
        *check_text(paths),
        *check_markdown_links(paths),
        *check_png_metadata(paths),
        *check_action_pins(paths),
    ]
    if failures:
        for failure in sorted(set(failures)):
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    print(f"Repository hygiene checks passed for {len(paths)} candidate files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
