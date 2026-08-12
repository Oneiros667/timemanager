# Security policy

## Supported scope

Time Manager is an early local development pilot. The supported runtime is a
trusted installation using Flask's development server on `127.0.0.1` with a
local SQLite database. There is no supported internet-facing deployment,
hosted account service, production operations environment, or security support
window yet.

The database, migration backups, account exports, session secret, browser-local
drafts, and task text may contain sensitive personal information. The local
installation operator and anyone with access to the host or browser profile may
be able to read it. Do not attach real databases, exports, browser profiles,
screenshots, logs, or task content to a public issue.

## Reporting a vulnerability

Do not disclose a suspected vulnerability or personal data in a public issue.
Email the repository owner at
[pieter.devilliers@gmail.com](mailto:pieter.devilliers@gmail.com) before
sharing reproduction details. Send only a short, non-sensitive summary first;
the owner will arrange a suitable private channel for any sensitive details.
When GitHub private vulnerability reporting is enabled, that channel may be
used instead.

Include only the minimum information needed to understand the affected version,
impact, and a synthetic reproduction. Remove secrets, real account details,
tasks, notes, exports, cookies, CSRF tokens, password hashes, local paths, and
browser data.

## Security expectations

- Keep the server bound to loopback. Setting `TIMEMANAGER_HOST=0.0.0.0` exposes
  the development server to the local network without TLS or production
  hardening.
- Treat `instance/`, `*.pre-migration-*.bak`, and account-export JSON as
  sensitive. Protect backups and delete temporary exports through the
  operator's normal secure process after use.
- Never place credentials in source, client-side JavaScript, committed `.env`
  files, screenshots, fixtures, logs, or issue reports.
- Use fictional `example.com`/`example.test` accounts and synthetic tasks for
  tests and demonstrations.
- Do not infer production or multi-tenant security from the local account
  isolation tests.

Known limitations and the current security review are tracked in
[`docs/publication-readiness.md`](docs/publication-readiness.md).
