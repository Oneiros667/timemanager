# Repository guidance for coding agents

## Scope and current state

These instructions apply to the whole repository. More specific guidance in
`docs/AGENTS.md` also applies to work under `docs/`.

Timemanager is implementing the local development/pilot PWA described in the
product design. The current application includes local account registration,
session login, SQLite task persistence, Today and Inbox views, a Low Capacity
view, a client-side focus timer, schema migrations, and operator-level
account/task export-import. Calendar integration, self-service account restore,
trusted-person sessions, hosted accounts, local-to-online data migration, and
mobile applications remain proposed. Keep proposed and implemented behaviour
clearly separated in code, documentation, and status reports.

## Start here

1. Inspect `git status --short --branch` and preserve unrelated work.
2. Read `README.md`, then `docs/README.md` and any document relevant to the
   task.
3. If Codebase Memory tools are available, use the `timemanager` project for
   architecture or relationship discovery before broad code searches. Confirm
   that the project is actually available; `.codebase-memory/status.json` is
   generated local state and may be stale. The current index excludes `docs/`,
   so inspect research files directly with `rg` or targeted reads.
4. Fall back to direct repository inspection when the memory service or a
   needed tool is unavailable. Do not invent tool names or index results.

## Repository map

- `main.py`: development entry point.
- `timemanager/`: Flask application, SQLAlchemy Core tables, templates, and PWA
  assets.
- `migrations/`: ordered Alembic revisions for fresh and existing databases.
- `timemanager/account_transfer.py`: versioned account/task export-import
  contract and operator CLI commands.
- `tests/`: authentication, ownership, migration, transfer, state-flow, and PWA
  tests.
- `pyproject.toml`: package metadata, runtime dependencies, and test config.
- `uv.lock`: reproducible `uv` environment.
- `docs/README.md`: research index and evidence-label definitions.
- `docs/*.md`: domain research and proposed product/architecture directions.
- `docs/decisions/`: accepted implementation decisions.
- `.codebase-memory/config.json`: tracked connector metadata. Generated status
  and graph data are intentionally ignored.

## Environment and commands

Use `uv` for the local Python environment:

```bash
uv sync
uv run timemanager
```

The local app listens on `http://127.0.0.1:5000` by default. Run verification
with:

```bash
uv run pytest
uv run pytest --cov=timemanager --cov-report=term-missing
uv run python -m compileall -q main.py timemanager tests migrations
uv run flask --app timemanager schema-version
uv run flask --app timemanager export-account --help
uv run flask --app timemanager import-account --help
```

There is no production deployment configuration yet. Flask's development
server is for the local pilot only.

For every change, run:

```bash
git diff --check
```

## Working agreements

- Make the smallest coherent change that satisfies the request. Do not rewrite
  unrelated research or reformat large files incidentally.
- Prefer `rg`/`rg --files` for discovery and targeted patches for edits.
- Never discard existing work or use destructive Git commands unless the user
  explicitly requests it.
- Keep secrets, API keys, access tokens, raw voice recordings, and personal
  task data out of Git. Provider credentials belong in server-side environment
  configuration, not client code.
- Treat automatic task edits, scheduling, deletion, and completion as
  user-confirmed actions unless a product decision explicitly establishes a
  narrower safe rule.
- When adding a document, link it from `docs/README.md`. When adding executable
  behaviour, add proportionate tests and replace placeholder setup guidance
  with commands that have been run successfully.
- Keep authenticated HTML network-only. The service worker may cache public
  shell assets and the offline page, but must not cache personal task pages.
- Every state-changing form must retain CSRF protection and every task query or
  mutation must be scoped to the signed-in user.
- Record durable architecture choices as a short decision document under
  `docs/decisions/` once implementation creates a real choice to preserve. Do
  not write an ADR merely to restate an unimplemented proposal.

## Product and safety boundaries

- This is an executive-function support tool, not a diagnosis, treatment, or
  replacement for a clinician, coach, or human support.
- Preserve user autonomy, low-capacity/recovery paths, and neutral language.
  Avoid shame, forced streaks, manipulative urgency, or dependency-oriented AI
  copy.
- Do not present model-generated steps, durations, priorities, or schedules as
  facts. Make suggestions identifiable, editable, and reversible.
- Keep non-AI task, routine, and timer flows useful without a microphone,
  network connection, or AI account.
- State privacy and retention behaviour precisely. A locally hosted application
  that calls a cloud provider is not fully local.

## Completion and review

Before handing off:

- review the diff and confirm it is limited to the requested scope;
- run the relevant commands above plus any tests introduced by the change;
- update nearby documentation when behaviour or setup changes;
- report what was verified and what remains proposed or unverified.

Treat unsupported clinical efficacy claims, concealed external data transfer,
hard-coded credentials, unconfirmed destructive actions, and documentation that
describes proposed features as shipped as blocking review findings.
