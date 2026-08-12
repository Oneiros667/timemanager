# Contributing

Time Manager is an early local pilot licensed under the Apache License 2.0.
Before submitting work, confirm that the repository owner is accepting
contributions and review the contribution treatment in section 5 of
[`LICENSE`](LICENSE).

## Set up

Use Python 3.11 or newer and the committed `uv.lock`:

```bash
uv sync --locked
uv run playwright install chromium
```

Run the application locally with `uv run timemanager`. Keep it bound to
`127.0.0.1`; Flask's development server is not a public hosting configuration.

## Privacy and test data

Use only fictional accounts and tasks with reserved example domains. Never add
real task, account, health, child, medication, school, calendar, email, or
personal data to code, fixtures, screenshots, traces, logs, databases, or
documentation.

Keep these artifacts out of Git:

- `instance/`, SQLite databases, migration backups, and account exports;
- `.env` files, tokens, keys, certificates, cookies, CSRF values, password
  hashes, and browser profiles;
- coverage output, Playwright reports/traces, logs, and generated test data; and
- screenshots not produced by the synthetic capture procedure.

The adult application and the proposed child product under `docs_kids/` are
separate. Do not create child accounts or move child, school, guardian, health,
or medication workflows into the adult application.

## Changes

- Preserve one highlight, at most three optional active Today actions, visible
  recoverable overflow, and non-mutating Low Capacity behavior.
- Keep task placement, prerequisites, external waits, and project state
  separate.
- Scope every data query and mutation to the signed-in account and retain CSRF
  protection on state-changing forms.
- Keep authenticated HTML network-only and personal data out of the service
  worker cache.
- Label proposed behavior and research hypotheses clearly. Do not make medical,
  accessibility-conformance, productivity-effectiveness, or usability claims
  without the required evidence.
- Add migrations for schema changes and focused tests for executable behavior.
- Keep patches small and do not reformat unrelated research.

## Verify

Before requesting review, run:

```bash
uv sync --locked
uv run python scripts/check_repository.py
PYTHONDONTWRITEBYTECODE=1 uv run pytest
uv run pytest --cov=timemanager --cov-report=term-missing
uv run python -m compileall -q main.py timemanager tests migrations scripts
git diff --check
```

Use a unique temporary `TIMEMANAGER_DATABASE` for manual CLI checks. Do not run
schema, export, import, or screenshot commands against an existing pilot
database.

## Synthetic screenshots

Regenerate publication screenshots from a temporary database and browser
profile with:

```bash
uv run python scripts/capture_synthetic_screenshots.py
```

Review every output image visually and run the repository checker before
committing it. Generated captures are demonstrations only; they do not prove
manual accessibility, real-device, participant, or usability acceptance.
