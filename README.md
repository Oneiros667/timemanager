# Timemanager

Timemanager is an early local-pilot PWA for moving through a day with less
planning friction. It combines quick capture, a deliberately small Today view,
one meaningful highlight, a Low Capacity view, and a bounded focus timer.

The intended product supports day-to-day functioning; it is not medical advice,
a diagnostic tool, or a replacement for ADHD assessment or treatment.

## Implemented now

- local user registration, sign-in, and sign-out;
- password hashing, signed session cookies, and CSRF-protected forms;
- per-user SQLite task persistence;
- quick capture to Today or Inbox;
- one changeable daily highlight;
- complete, restore, deliberately drop, and move-to-Today actions;
- Low Capacity display mode;
- a 5/15/25-minute client-side focus timer;
- responsive desktop/mobile presentation;
- installable PWA manifest, icons, service worker, and offline shell.

Google Calendar, trusted-person sessions, hosted accounts, local-to-online
migration, and native mobile clients are not implemented yet. Their intended
scope is documented in the
[high-level product design](docs/high-level-product-design.md).

## Local account topology

One trusted local installation may contain multiple isolated accounts. Sharing
an installation does not create household, guardian, helper, or data-sharing
permissions between those accounts.

The installation operator can access the SQLite database and backups on disk.
The local pilot is therefore not a privacy boundary against that operator and
must not be exposed as a public multi-tenant service.

## Quick start

Requirements:

- Python 3.11 or newer
- [`uv`](https://docs.astral.sh/uv/)

Install the locked environment and start the local app:

```bash
uv sync
uv run timemanager
```

Open <http://127.0.0.1:5000>. Register a local account, then capture the first
task.

The SQLite database and generated session secret are stored under `instance/`,
which is intentionally ignored by Git. An operator backup of that directory
contains every registered local account; protect it accordingly if the pilot
data matters.

Optional local settings:

```bash
TIMEMANAGER_HOST=0.0.0.0 TIMEMANAGER_PORT=5000 uv run timemanager
```

Binding to `0.0.0.0` makes the development server reachable from the local
network; it does not add TLS or make Flask's development server suitable for a
public deployment. PWA installation on another device requires a trusted HTTPS
origin.

## Verify

```bash
uv run pytest
uv run pytest --cov=timemanager --cov-report=term-missing
uv run python -m compileall -q main.py timemanager tests
git diff --check
```

## Research

Start with the [research index](docs/README.md). It distinguishes supported
evidence, plausible product hypotheses, lived-experience signals, and
commercial claims. Proposed features and architectures must not be described as
implemented.

## Working with Codex

Launch Codex from the repository (or a subdirectory) so it discovers the root
`AGENTS.md`; work under `docs/` also receives the nested research guidance.
The tracked `.codebase-memory/config.json` describes the optional local
Codebase Memory connector, while generated index status and data remain
untracked.
