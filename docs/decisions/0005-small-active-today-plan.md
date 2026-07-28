# ADR 0005: Small active Today plan

Status: accepted

Date: 2026-07-24

## Context

Today previously displayed every unfinished task assigned to the current date.
That contradicted the product rule that the present is deliberately small and
left "keep the list small" as copy rather than behavior. The accepted product
design specifies one highlight plus up to three optional active actions by
default.

Hard rejection would make quick capture fragile, while silently moving excess
tasks outside Today or automatically promoting another task when space opens would
change the user's plan without an explicit choice. Existing databases and
versioned imports can also contain more assigned tasks than the new active
limit.

## Decision

- A daily active plan contains:
  - at most one highlight; and
  - at most three non-highlight optional actions.
- Use the existing task state deliberately:
  - `active` means the task is in the small active plan;
  - `ready` with today's planned date means recoverable Today overflow awaiting
    a decision;
  - `inbox` remains saved for later without a planned date.
- Capture and move-to-Today always preserve the task. When all three optional
  slots are occupied, the task enters explicit overflow and the user receives
  a clear status message.
- Do not promote overflow automatically when a slot opens.
- Let the user:
  - activate an overflow task when a slot is available;
  - move an active, highlighted, or overflow task to Later;
  - make an active or overflow task the highlight;
  - complete or deliberately drop active tasks as before.
- If an overflow task replaces the highlight while all optional slots are
  occupied, move the previous highlight to overflow. If a slot is free, the
  previous highlight may remain as an optional active action.
- Restoring a completed task uses an open optional slot or enters overflow when
  the active plan is full.
- Revision `0003` converts prior planned `ready` tasks deterministically:
  highlights remain active, the earliest three optional tasks per account and
  date become active, and the remainder stay recoverable as overflow.
- Import applies the same translation to version-1 account packages exported
  from schema revision `0002`, which predates the active/overflow distinction.
- Keep the capacity account-scoped and date-scoped.
- Reject an account import atomically if its final state would exceed three
  active non-highlight actions for any date.

## Consequences

The main Today list now stays credibly small without losing captured work.
Overflow remains visible as a separate decision queue and retains the same task
records, provenance, timestamps, and revisions.

`active` and `ready` now have user-visible planning meanings. Future scheduling,
Reset, review, export versions, and hosted migration must preserve that
distinction. The limit is a product default, not evidence that three options are
optimal for every user; later personalization requires validation and must not
silently increase an existing plan.

This slice does not implement must/consequence-bearing commitments, automatic
priority recommendations, stale-day Reset, or learned capacity. Those remain
separate roadmap items.
