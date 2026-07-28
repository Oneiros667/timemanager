# ADR 0006: Complex-work state and relationships

Status: accepted

Date: 2026-07-28

## Context

Task clarification, multi-task outcomes, and blockers must coexist with the
small Today plan. A displayed order must not accidentally become a dependency,
and resolving a blocker must not silently change what the user chose for Today.
All relationships must remain account-scoped and portable.

## Decision

- Use one shallow hierarchy: project → task → optional component.
- Keep workflow status (`inbox`, `open`, `waiting`, `done`, or `dropped`)
  separate from Today placement (`unplanned`, `active`, or `overflow`).
- Store project task position as preferred order only.
- Store prerequisites as directed task relationships and reject self-links,
  cycles, and cross-account references.
- Store an external wait separately, with an optional review date and follow-up
  task.
- Compute readiness from workflow state and unresolved blockers. An explicit
  “Can start anyway” override leaves the blocker saved and visible.
- Never add newly ready work to Today automatically. A blocked Today task keeps
  its placement until the user chooses otherwise.
- Show captured, open, or waiting work outside the current Today plan in Later
  as a recovery route. This presentation rule does not change its workflow
  status or add it to Today.
- Require confirmation for project completion and task completion with
  unfinished components.
- Preserve these objects and relationships in account-transfer format v3 while
  continuing to import supported v1 and v2 documents.

The legacy `tasks.state` column remains synchronized during this compatibility
slice so older application behavior and transfer formats migrate
deterministically. New complex-work decisions use workflow status and Today
placement.

## Consequences

Readiness and daily capacity can evolve independently, and reorder controls
cannot create hidden blockers. Relationship validation is required in routes,
migrations, and atomic import. Nested projects, automatic scheduling, progress
percentages, and critical-path behavior remain out of scope.

This accepted implementation decision does not establish usability validation.
The synthetic prototype must still pass its participant and manual
accessibility gates.
