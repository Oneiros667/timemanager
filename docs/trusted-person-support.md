# Adult trusted-person support

Status: proposed product direction

Updated: 2026-07-28

## Purpose and boundary

Timemanager should let an adult invite a partner, friend, family member, coach,
or other trusted person to assist with selected planning work without granting
access to the adult's whole account.

This is planning support, not clinical care, employee monitoring, diagnosis,
location tracking, or authority to control another adult's plan. The adult
account owner remains the decision maker.

The hosted subscription includes one trusted-support companion seat. The seat
grants only the permissions approved by the adult and does not include a
separate personal planning workspace for the companion.

## Non-negotiable privacy boundaries

- Assistance access is opt-in, item- or purpose-scoped, time-limited, auditable,
  and immediately revocable.
- Co-resident local accounts do not form a household or assistance
  relationship.
- The adult sees a human-readable disclosure preview before an invitation or
  scope change.
- Private task content is not shared in bulk.
- Timemanager does not claim to detect every sensitive detail in free text.
- Tracked activities, execution histories, Day Context, medication records,
  Quick Help, and private notes are excluded from the first implementation.
- A general planning permission never implies health, calendar, location,
  financial, or other sensitive-data access.
- Declining a proposal or revoking a helper creates no failure score or
  retaliatory notification.

## Roles and permissions

| Role | May see | May create | May change | May complete/drop | May invite |
| --- | --- | --- | --- | --- | --- |
| Adult owner | Their full account | Tasks, commitments, reminders, scopes | Everything they own | Yes | Yes |
| Trusted planner | Only selected items and chosen availability | Proposals and their own drafts | Their own unaccepted drafts | No by default | No |
| Focus companion | Session intention, time boundary, join/leave status | Invited check-ins or distraction captures | No plan data | No | No |

An adult may grant a narrow, time-limited delegation for a named action. The
interface must show the delegated action, fields, recipient, and expiry.
Delegation never silently expands to deadlines, completion, deletion,
recurrence, external calendar writes, or other objects.

## Workflow

1. The adult chooses a trusted person and purpose: focus presence, selected
   tasks, appointment/reminder proposals, or a time-limited planning session.
2. Timemanager resolves the invited identity and shows the exact fields,
   direction, start, and expiry.
3. The adult confirms the disclosure preview.
4. The recipient accepts the invitation and sees only the active scope.
5. Recipient-created planning objects enter as clearly attributed proposals.
6. The adult may accept, edit, schedule, defer, decline, or revoke.
7. Material events record actor, action, time, scope, and outcome.

Possession of an invitation link, email address, subscription, or shared device
does not establish trust or permission.

## Shared planning objects

Objects shared through an assistance workspace need:

- workspace, owner, and relationship identifiers;
- created-by, proposed-by, and last-changed-by identity;
- selected field scope and purpose;
- proposal state: draft, awaiting response, accepted, adjusted, declined,
  expired, or revoked;
- optional intended recipient and acknowledgement state;
- reminder recipients and delivery status; and
- audit events for creation, material edits, acceptance, delegation,
  completion, revocation, and deletion requests.

The ordinary personal task view remains simple. Provenance and permission
detail appears when the adult reviews a proposal, disclosure, or history.

## Reminders and appointments

### Reminders

- A trusted person may propose a reminder; the adult decides whether it becomes
  active.
- The preview shows who receives it, which channel is used, and how often.
- Dismissing a reminder does not silently report failure to the helper.
- Sensitive reminder notifications contain generic wording and no personal
  detail.

### Appointments

- A helper may propose an appointment with source, time, travel, and
  preparation details.
- External calendar creation or modification requires a separate adult preview
  and explicit confirmation.
- Calendar detail outside the assistance scope remains private.

## Focus companion

A focus companion receives only:

- the adult-approved session intention;
- planned start/end or duration;
- presence/join/leave state; and
- invited check-in messages.

The companion does not receive the adult's task list, browsing/app activity,
camera, microphone recording, precise location, keystrokes, or productivity
score. Ending or leaving a session is not failure.

## Privacy, security, and release gates

Real trusted-person support requires:

- hosted accounts and production server-side authorization;
- authenticated, expiring invitations;
- field-level scope checks on every read and mutation;
- strong account recovery and session protection;
- disclosure previews and explicit scope changes;
- immutable access/change history;
- immediate revocation and recipient role termination;
- export, correction, retention, and deletion behavior;
- abuse reporting and a coercive-helper threat model;
- content-free notification, analytics, logging, tracing, and support tooling;
- penetration and cross-account isolation testing; and
- supervised usability and accessibility validation.

Payment establishes a billing relationship only and does not prove identity,
trust, consent, or authority over another adult.

## Validation topology

### Synthetic prototype

Use fictional adults, relationships, tasks, appointments, reminders, and
messages. Simulate roles on the same trusted device. Reset after each session.
Do not send invitations, persist real assistance relationships, connect
calendars, or deliver notifications.

### Hosted adult pilot

A real pilot is limited to approved accounts and scopes after all authorization,
privacy, abuse, security, deletion, and operational gates pass. Prototype
verification does not authorize live sharing.

## Evaluation

Test:

- whether adults understand exactly what the trusted person can see and change;
- whether useful proposals reduce planning friction;
- whether accepting, editing, declining, and revoking remain easy;
- whether helpers understand proposal-only defaults;
- whether reminders help without duplication or pressure;
- whether focus presence helps without surveillance; and
- whether assistance adds shame, conflict, maintenance burden, or unwanted
  dependence.

Do not use disclosure volume, helper activity, task completion, time in app, or
declined proposals as success metrics.

## Confirmed adult-support decisions

- Trusted people are proposal-only by default.
- The adult may grant a narrow, explicit, time-limited delegation.
- The first prototype uses synthetic data and same-device role simulation.
- Real relationships require hosted server authorization.
- Health histories and private state/context records are excluded by default.
