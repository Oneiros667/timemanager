# ADR 0002: Local account topology

Status: accepted

Date: 2026-07-24

## Context

The Phase 1 local pilot runs as one trusted local installation. The application
already supports registration of multiple accounts, stores each task with an
owner, and tests that one account cannot access another account's tasks.

Describing this as a single-user or single-account pilot would contradict the
implemented behavior. At the same time, sharing one installation must not imply
that its accounts form a household, trust each other, or have permission to
share planning data.

## Decision

One Phase 1 local installation may contain multiple isolated local accounts.

- Every user-owned object and mutation is scoped to one authenticated account.
- Local accounts cannot discover, read, change, export, or migrate another
  account's data through the application.
- Registration on the same installation does not establish a family,
  assistance, or trusted-person relationship.
- Cross-account sharing remains unavailable unless a separately approved
  assistance design explicitly provides it.
- The installation is intended for a trusted machine and local network, not
  exposure as a public multi-tenant service.
- The installation operator can access the SQLite database, generated secret,
  and backups at the filesystem level. The local pilot is not zero-knowledge
  storage and does not protect data from that operator.
- An operator backup of the `instance/` directory contains every local account
  and must be protected as a whole.
- User-facing export, deletion, restore, and hosted migration are scoped to the
  authenticated account. Migrating one account never selects or transfers
  another local account.
- The implemented Phase 1 export/import foundation is an installation-operator
  CLI, not a user-facing account session. Its ability to select an account is
  part of the operator-access boundary above; each package still contains only
  the selected account.

## Consequences

The existing registration and ownership model remains part of the supported
Phase 1 topology rather than unused preparation for hosting. Every new task,
activity, execution, preference, and related query needs an ownership test.

Account isolation reduces accidental disclosure through the application but
does not create a security boundary against the local installation operator.
Documentation and backup handling must state that limitation plainly.

A later hosted service still requires production tenant isolation,
authorization, account recovery, abuse controls, operational security, and
auditable migrations. Local account registration is not evidence that any of
those hosted requirements are satisfied.
