# ADR 0003: Database migrations and hosted database target

Status: accepted

Date: 2026-07-24

## Context

The Phase 1 local pilot needs to upgrade existing SQLite databases without
losing account or task data. Upcoming features also need stable identifiers and
provenance for account-scoped export and eventual hosted migration.

Moving the local pilot to PostgreSQL would add a service dependency and
operational burden before the product needs hosted concurrency. Continuing with
SQLite-specific queries and migrations, however, would increase the later
porting cost as the information model grows.

## Decision

- Keep SQLite as the active Phase 1 local-pilot database.
- Use SQLAlchemy Core for application persistence and database-independent
  statement construction.
- Use ordered Alembic revisions for schema changes.
- Detect the exact pre-Alembic users/tasks schema, stamp it as revision `0001`,
  and upgrade it normally. Unknown unversioned schemas fail closed.
- Give the installation, users, and tasks stable public UUIDs while retaining
  integer primary keys as internal database identifiers.
- Record the originating installation and a positive revision number on
  user-owned objects.
- Before a pending migration, create a consistent snapshot of an existing
  file-backed SQLite database. Restore it automatically if an upgrade fails;
  retain the snapshot after success for operator recovery.
- Use PostgreSQL as the Phase 3 hosted database target. Add its driver,
  deployment configuration, migration validation, and integration-test matrix
  when hosted implementation begins.
- Move selected account data from SQLite to PostgreSQL through the versioned,
  idempotent export/import contract, not by treating the two database files as
  interchangeable or continuously synchronized.

## Consequences

The local pilot remains a single-process application with simple file-based
operation. Schema version is inspectable, repeat startup is idempotent, and
legacy data receives stable provenance without changing its internal IDs.

SQLAlchemy and Alembic add dependencies and require metadata-to-migration drift
checks. SQLite does not provide transactional DDL guarantees for every table
rewrite, so the pre-migration snapshot is part of the safety contract rather
than optional convenience.

This decision prepares SQL statements and migrations for PostgreSQL but does
not claim that PostgreSQL is currently configured, tested, or supported. The
hosted release remains blocked until production database, tenant-isolation,
backup, restore, monitoring, and operational evidence pass.

Relevant upstream guidance:

- [SQLAlchemy engine configuration](https://docs.sqlalchemy.org/en/20/core/engines.html)
- [Alembic programmatic connection sharing](https://alembic.sqlalchemy.org/en/latest/cookbook.html)
- [Alembic batch migrations for SQLite](https://alembic.sqlalchemy.org/en/latest/batch.html)
