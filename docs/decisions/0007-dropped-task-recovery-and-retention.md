# ADR 0007: Dropped-task recovery and retention

Status: accepted

Date: 2026-07-28

## Context

Drop is a consequential action. The earlier local pilot submitted it directly
when JavaScript was unavailable and removed the task from every ordinary view.
That made an accidental activation difficult to detect or recover from.

The ordinary recovery surface must remain bounded, but hiding the eleventh item
does not justify silently deleting user-authored data. Automatic purging would
also change export, migration, privacy, and operational-recovery contracts.

## Decision

- Keep Drop as a reversible workflow state, not a hard delete.
- Require a server-rendered confirmation with the exact task title, current
  revision, CSRF protection, and account ownership before changing state.
- Record `dropped_at` for ordering and recovery. New timestamps use UTC; the
  migration uses `updated_at` for already-dropped records whose original Drop
  time was not recorded.
- Show the ten most recently dropped tasks in an account-scoped `Recently
  dropped` surface.
- Offer immediate Undo and make restoration to Later the safe default.
- Make Add to Today a separate explicit action and retain existing blocker and
  Today-capacity rules.
- Retain older dropped tasks in protected database storage and account export.
  Do not add a deeper user-facing archive or automatic purge in this slice.
- Extend account export to format version 5 with `dropped_at`, while preserving
  v1 through v4 import compatibility.

## Consequences

An accidental Drop has a no-JavaScript recovery path and does not require
operator or database intervention while the task is in the newest ten.
Restoration does not silently consume Today capacity.

Older dropped tasks continue to consume storage and are not self-service
recoverable through the current UI. A future deeper archive, retention period,
or purge requires a separate product decision, privacy review, migration and
export contract, and explicit user-facing consequences.

Exports remain sensitive because they include retained dropped task content and
timestamps. Account isolation, CSRF, revision checks, and operator-access
boundaries continue to apply.
