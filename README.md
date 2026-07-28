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
- SQLAlchemy Core persistence with ordered Alembic schema upgrades;
- stable public UUIDs, installation provenance, and object revisions;
- versioned, account-scoped JSON task export/import through operator CLI
  commands;
- quick capture to Today or Later;
- a separate three-item Remember list for short-term context-switching cues;
- one changeable daily highlight plus at most three optional active actions;
- explicit, recoverable Today overflow with activate and save-for-later choices;
- complete, restore, move-to-Today, and server-confirmed Drop actions;
- a newest-ten Recently dropped recovery surface with immediate Undo,
  restore-to-Later defaults, and separate Add-to-Today actions;
- inline task editing plus task workspaces for next action, definition of done,
  notes, and ordered steps;
- 24-hour browser-local recovery for interrupted task and project autosave
  drafts, including explicit handling of stale server revisions;
- lightweight project workspaces with preferred ordering and one next-ready
  task;
- a lightweight project collection reached from Later, with active outcomes,
  next-ready tasks, and a collapsed completed/dropped archive with explicit
  restoration;
- one-confirmation task-to-project conversion that preserves the original task
  as the project’s first task;
- explicit task prerequisites, external waits, optional follow-up tasks, and
  reversible blocker overrides separated from Today placement;
- a Today-scoped Low Capacity view that shows the existing highlight or the
  first unblocked active Today task without changing task state, with a hidden
  unfinished-work count and a full-Today escape;
- a 5/15/25-minute client-side focus timer with non-chattering assistive
  announcements;
- responsive desktop/mobile presentation with matching mobile visual and
  sequential focus order;
- tested functional-control, placeholder, and focus-indicator contrast tokens;
- installable PWA manifest, icons, service worker, and offline shell.

Self-service account restore, credential recovery, Google Calendar,
trusted-person sessions, hosted PostgreSQL accounts, local-to-online migration,
and native mobile clients are not implemented yet.
Guardian-operated child accounts, school/carer communication, and medication
sharing belong to a proposed separate child-support application; they are not
features of this adult local pilot.
The implemented complex-work interaction remains a plausible design whose
five-participant usability gate has not yet been run. Manual screen-reader,
keyboard, zoom, forced-colors, and real-device verification also remains open.
Intended and gated scope is documented in the
[high-level product design](docs/high-level-product-design.md).

## Local account topology

One trusted local installation may contain multiple isolated accounts. Sharing
an installation does not create household, guardian, helper, or data-sharing
permissions between those accounts.

The installation operator can access the SQLite database and backups on disk.
The local pilot is therefore not a privacy boundary against that operator and
must not be exposed as a public multi-tenant service.

Interrupted task and project drafts may contain sensitive text. They are kept
in the signed-in browser profile, scoped by account, object, form, and tab.
Drafts expire after 24 hours and are pruned on the next Timemanager page load;
matching drafts are removed after an acknowledged save, and all drafts for the
account are removed on sign-out. They are not placed in the public
service-worker cache or included in account export. Browser-profile and device
access remain part of the trusted local-installation boundary.

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

## Database upgrades

Application startup automatically applies pending Alembic revisions. An exact
database from the earlier users/tasks schema is recognized, recorded as
revision `0001`, and upgraded without changing its internal IDs or existing
values. An unknown unversioned schema or unknown newer revision stops startup
instead of being guessed.

Inspect or apply the current schema explicitly:

```bash
uv run flask --app timemanager schema-version
uv run flask --app timemanager init-db
```

Before changing an existing file-backed SQLite database, Timemanager writes a
timestamped `*.pre-migration-*.bak` snapshot beside it. A failed upgrade
restores that snapshot automatically. A successful upgrade retains it until
the operator has verified the application and incorporated the new database
into the normal protected backup process.

SQLite remains the supported Phase 1 database. PostgreSQL is the Phase 3 hosted
target but is not configured or supported by the local pilot yet. Future
SQLite-to-PostgreSQL data movement will use account-scoped export/import rather
than direct database-file conversion.

## Account export and import foundation

An installation operator can export the portable profile and tasks for exactly
one local account:

```bash
uv run flask --app timemanager export-account \
  --email alex@example.com \
  --output ./alex-timemanager.json
```

The command creates a new mode-`0600` file and refuses to overwrite an existing
path. The versioned JSON contains user-authored profile and task content, so it
may be sensitive. It excludes password hashes, session/application secrets,
internal database IDs, and every other local account.

Import currently targets an existing local account whose credentials are
managed separately:

```bash
uv run flask --app timemanager import-account \
  --input ./alex-timemanager.json \
  --into-email destination@example.com
```

Export format v5 includes task detail, dropped-task recovery timestamps,
projects, ordered steps, dependencies, external waits, and Remember items.
Import remains compatible with supported v1, v2, v3, and v4 documents and
validates relationships atomically. Stable object IDs insert once; a higher
incoming revision updates an object, a lower revision leaves newer local data
unchanged, and differing content at the same revision fails closed. Imported
objects retain their source-installation provenance. The source profile is
informational and does not replace the destination account's name, email, or
password.

Recently dropped shows only the newest ten account-scoped tasks. Older dropped
tasks remain in protected database storage and account export; this slice does
not add a deeper user-facing archive or automatic purge.

This is tested migration and recovery plumbing, not yet a self-service restore
experience, full-database backup, deletion mirror, credential transfer, or
hosted migration. Keep normal protected backups of `instance/`.

## Small Today plan

Today separates one highlight from at most three optional active actions.
Additional tasks captured or moved to Today remain in a visible overflow rather
than expanding the active plan or being discarded. Overflow tasks are never
promoted silently: make space by saving an active item for later, then activate
the chosen overflow item, or make an overflow item the new highlight.

## Remember

Today opens with a small Remember panel beside Quick Capture. It holds at most
three account-scoped micro-reminders, such as “Get coffee,” for short-term
memory during context switching. Remember items do not consume Today capacity
and do not participate in task, project, ordering, or blocker state. Checking
one removes it immediately; deletion is not mirrored by account import.
Active items persist in SQLite and are included in account export format v5.

Optional local settings:

```bash
TIMEMANAGER_HOST=0.0.0.0 TIMEMANAGER_PORT=5000 uv run timemanager
```

Binding to `0.0.0.0` makes the development server reachable from the local
network; it does not add TLS or make Flask's development server suitable for a
public deployment. PWA installation on another device requires a trusted HTTPS
origin.

The synthetic complex-work prototype is disabled by default. To run a research
session with browser-memory-only synthetic data, including the calm-break
guardian/young-person interaction:

```bash
TIMEMANAGER_ENABLE_PROTOTYPES=1 uv run timemanager
```

Open <http://127.0.0.1:5000/prototypes/complex-work>. The route returns `404`
when disabled and `Cache-Control: no-store` when enabled.
The calm-break prototype is at
<http://127.0.0.1:5000/prototypes/calm-break> and has the same boundaries.
The school-support disclosure prototype is at
<http://127.0.0.1:5000/prototypes/school-support-share>; it sends and stores
nothing and must be used only with fictional scenarios.

## Verify

```bash
uv run pytest
uv run playwright install chromium
uv run pytest --cov=timemanager --cov-report=term-missing
uv run python -m compileall -q main.py timemanager tests migrations
git diff --check
```

## Research

Start with the [research index](docs/README.md). It distinguishes supported
evidence, plausible product hypotheses, lived-experience signals, and
commercial claims. Proposed features and architectures must not be described as
implemented.

The proposed, separate application for children aged 8–17 is documented under
[Timemanager Kids](docs_kids/README.md). No real child application or child-data
workflow is implemented by those documents.

## Working with Codex

Launch Codex from the repository (or a subdirectory) so it discovers the root
`AGENTS.md`; work under `docs/` also receives the nested research guidance.
The tracked `.codebase-memory/config.json` describes the optional local
Codebase Memory connector, while generated index status and data remain
untracked.
