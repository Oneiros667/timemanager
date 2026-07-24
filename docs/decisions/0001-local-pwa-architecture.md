# ADR 0001: Local PWA architecture

Status: accepted

Date: 2026-07-24

## Context

The Phase 1 Timemanager local pilot is a development application. It needs
simple registration, personal task persistence, an ADHD-friendly responsive
experience, and an installable PWA shell. The approved delivery path later
replaces the pilot with the Phase 3 hosted release, followed by native mobile
clients and an optional one-time local-data migration.

The first slice should be easy to run and inspect without committing the hosted
release to premature infrastructure. It must still preserve user isolation and
data-model boundaries that can evolve safely.

## Decision

Use:

- Flask 3.1 with an application factory and focused blueprints;
- SQLAlchemy Core over SQLite for local users and tasks;
- server-rendered Jinja templates with progressive client-side JavaScript;
- Werkzeug password hashing and Flask's signed session cookie;
- a per-session CSRF token for every state-changing form;
- ordered Alembic revisions with per-user foreign keys, internal integer IDs,
  stable public UUIDs, installation origin, and object revisions;
- a web app manifest and root-scoped service worker;
- network-only authenticated navigation, with caching limited to public static
  shell assets and a non-personal offline page.

The automatically generated local secret and SQLite database live under the
ignored `instance/` directory. The service worker must not cache authenticated
Today, Inbox, or task responses.

The installation-level account and operator-access boundary is defined in
[ADR 0002: Local account topology](0002-local-account-topology.md).

## Consequences

Benefits:

- one small Python runtime serves registration, persistence, and the PWA;
- server rendering provides a useful experience before JavaScript loads;
- SQLite is sufficient for the single-machine Phase 1 local pilot and simple to
  back up;
- exact legacy databases upgrade automatically, with a pre-migration SQLite
  snapshot retained and restored if the upgrade fails;
- the application factory and isolated test database make behavior testable;
- minimal client JavaScript keeps the daily path fast and comprehensible.

Costs and boundaries:

- Flask's development server is not a public deployment server;
- SQLite and local signed-cookie authentication are not the final hosted
  multi-tenant architecture; PostgreSQL is the hosted database target;
- the Phase 3 hosted release still needs PostgreSQL migration validation,
  TLS-secure cookie configuration, email verification/recovery, login
  throttling, tenant controls, operational monitoring, and backup/restore;
- PWA installation on a separate home-network device requires a trusted HTTPS
  origin;
- offline personal-data mutation is not supported by this service worker;
- the one-time migration must explicitly translate local IDs to stable hosted
  identifiers and must not copy local secrets or provider credentials.

These constraints are deliberate. They keep the Phase 1 local pilot working
while leaving the hosted security and synchronization contracts visible rather
than pretending they already exist.
