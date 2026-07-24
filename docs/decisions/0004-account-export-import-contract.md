# ADR 0004: Account export and import contract

Status: accepted

Date: 2026-07-24

## Context

The local pilot needs a tested foundation for user data portability, recovery,
and eventual one-time hosted migration. A raw SQLite copy contains every local
account plus internal implementation details, while a database-to-database copy
would couple local recovery to SQLite and would not define retry or conflict
behavior.

Password hashes cannot become portable credentials. Importing them would
silently transfer authentication material and would not satisfy hosted account
verification or recovery requirements. The initial implementation also needs
to preserve the accepted boundary that co-resident accounts do not share data.

## Decision

- Define `timemanager.account-export` JSON format version `1`.
- Export exactly one selected account's portable profile and owned tasks.
- Include stable public IDs, source-installation public IDs, positive object
  revisions, user-authored fields, state, and timestamps.
- Exclude password hashes, session/application secrets, internal database IDs,
  and every other account.
- Treat all export files as potentially sensitive because profile fields,
  titles, and notes contain user-authored content.
- Provide the initial workflow as explicit local operator CLI commands.
  Exported files are created with mode `0600` and existing paths are not
  overwritten.
- Import into an explicitly selected, already existing destination account.
  The source profile is informational; import does not replace destination
  identity or authentication fields.
- Retain each task's stable public ID and source-installation provenance.
- Make retries idempotent by public ID and revision:
  - an unseen task is inserted;
  - identical content at the same revision is unchanged;
  - a higher incoming revision updates the local task;
  - a lower incoming revision preserves the newer local task;
  - divergent content at the same revision fails closed; and
  - a public ID already owned by another local account fails closed.
- Apply each import atomically. Constraint or conflict failure must not leave a
  partial set of imported tasks.
- Reject an import that would leave any date above the implemented limit of
  three active non-highlight actions.
- Reject malformed documents, duplicate JSON fields, unknown fields, and
  unsupported format versions rather than guessing.
- Preserve a static version-1 fixture and automated round-trip, idempotency,
  ownership, conflict, validation, and secret-exclusion tests.

## Consequences

The repository now has portable and database-independent task transfer
plumbing. It can be retried safely and can later serve as one input to a
hosted-migration adapter without treating a SQLite file as PostgreSQL data.

The current command is an operator capability, equivalent to the operator's
documented filesystem access. It is not an authenticated self-service export
or restore screen. Import requires a separately created destination account
and does not create or recover credentials.

Format version 1 transfers the currently implemented profile and task model
only. It does not mirror deletions, merge unrelated tasks, transfer session
state, copy application configuration, restore all accounts, or prove hosted
tenant isolation. Each future user-owned object type must extend the format
through an explicit compatible version and receive account-scope, fixture,
round-trip, and conflict tests.
