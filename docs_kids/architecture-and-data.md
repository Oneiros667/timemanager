# Architecture and data requirements

Status: proposed child-application architecture; no implementation decision is
accepted by this document

Updated: 2026-07-28

## Architecture objective

Build Timemanager Kids as a separate hosted product whose authorization,
storage, operations, and release controls are designed around child workspaces
and verified adult relationships.

The adult Flask/SQLite PWA is useful implementation evidence for interaction
patterns, migrations, CSRF, account scope, public-shell caching, and testing. It
is not an acceptable real-data child sharing architecture.

## Separation from adult Timemanager

The child product must have separate:

- application audience and deployment;
- domains/origins and session cookies;
- identity clients and recovery policies;
- production database and encryption scope;
- API authorization audience;
- service-worker cache namespace;
- notification topics and push credentials;
- analytics/telemetry identity;
- account exports and import formats;
- operator/support access;
- incident and deletion workflows; and
- market feature flags and authorization records.

An adult account ID cannot be used as a child workspace ID. Cross-product
transfer is absent by default and requires a previewed, consented, versioned,
audited, one-time process if later approved.

## Proposed deployment shape

```text
Child/guardian web or native client
Teacher/carer restricted client
School-health restricted client
             |
             v
        API gateway
             |
             v
  identity + policy enforcement
             |
    +--------+---------+----------------+
    |                  |                |
planning service   relationship     communication
                   and consent       and delivery
    |                  |                |
    +--------+---------+----------------+
             |
       PostgreSQL
   tenant/workspace scoped
             |
    encrypted object/export storage

Transactional outbox -> notification providers
Restricted audit pipeline -> immutable audit store
```

This is a conceptual boundary, not a technology authorization. A modular
monolith may be safer than premature distributed services if it preserves the
same policy boundaries and transactional behavior.

## Request authorization

Every request evaluates:

- application audience;
- authenticated actor and session/device assurance;
- child workspace/tenant;
- active verified relationship;
- role;
- purpose;
- object and field scope;
- read/write/delivery direction;
- time and expiry;
- consent/authority policy version;
- market feature authorization;
- dispute/suspension state; and
- object revision where mutation is involved.

Routes must load objects through workspace-scoped queries. A later check after
an unscoped read is insufficient. A denied or guessed identifier returns no
data and does not reveal object existence.

Authorization is server-enforced. Client visibility, disabled controls,
template branches, URLs, and organization membership are not permission.

## Conceptual information model

The following are product concepts, not an approved schema.

### Identity and workspace

- **Child workspace:** supported child, age band, market, status, privacy
  defaults, transition state, and current policy versions.
- **Actor:** adult or child identity separated from workspace relationships.
- **Relationship:** workspace, actor, organization, role, purpose, scopes,
  direction, dates, verification, status, and child-visible label.
- **Organization:** verified school/care organization, domain evidence,
  administrators, security/contact metadata, and status.
- **Authority record:** guardian or other lawful authority, notice, consent or
  legal basis, child participation, method, scope, expiry, and revocation.

### Planning

- **Capture:** original child/guardian input, source, time, author, and
  clarification state.
- **Task:** title, next action, definition of done, workflow status, Today
  placement, author/last editor, and revision.
- **Step:** short optional checklist item without independent scheduling or
  permissions.
- **Project/outcome:** shallow grouping, desired outcome, preferred order, and
  next-ready task.
- **Dependency/external wait:** explicit blocker distinct from preferred order.
- **Fixed commitment:** time interval, timezone, source, transition data, and
  sync provenance.
- **Daily plan:** date, anchor, optional actions, capacity mode, and explicit
  child/guardian choices.
- **Calm-break plan:** reason, optional supports, check-in agreement, author,
  child response, and retention policy.

### Communication and school support

- **Support signal:** child-authored message kind, intended recipient role,
  exact recipient, timestamps, delivery states, acknowledgement, cancellation,
  expiry, and fallback shown.
- **Support card:** selected field set disclosed for a named purpose.
- **Feedback entry:** adult observation, support offered, child response,
  follow-up request, attribution, correction link, and expiry.
- **Disclosure:** source fields, resolved recipient, purpose, preview/confirm
  actor, time, direction, processor/transfer, and revocation state.

### Health/medication

Later gated concepts:

- medication identity and exact formulation;
- source-provenanced current instructions;
- guardian-provided context;
- school administration plan;
- planned administration occurrence;
- human-confirmed administration record;
- child report;
- discrepancy/correction; and
- reviewed content rule.

Planning tasks and schedules never stand in for these records.

### Safety, audit, and operations

- **Audit event:** actor, workspace, relationship, action, object, selected
  fields, purpose, result, time, session/device, policy version, and integrity
  metadata.
- **Concern/dispute:** reporter, safe-contact preference, category, restricted
  details, status, reviewer, decision, review/expiry, and notification policy.
- **Delivery outbox item:** idempotency key, payload class, opaque target,
  provider status, retry, expiry, and final evidence.
- **Export/deletion job:** exact workspace scope, authority, format/policy
  version, included domains, status, protected artifact, expiry, and evidence.

## State models

### Relationship

```text
pending -> verified -> active -> expired
                  |       |
                  |       +-> paused -> active
                  +----------> revoked
                  +----------> suspended/disputed
```

No expired, revoked, suspended, or disputed relationship authorizes access.

### Support signal

```text
draft -> queued -> server accepted -> delivered -> acknowledged
  |         |             |              |
  +-> cancelled           +-> failed     +-> expired
            +-> unavailable/expired
```

The UI renders only the highest evidenced state. Provider acceptance is not
recipient delivery; delivery is not acknowledgement.

### Disclosure

```text
draft -> previewed -> confirmed -> disclosed
  |          |            |          |
  +-> cancelled           +-> failed +-> revoked for future access
```

Revocation does not rewrite history or claim that the recipient forgot
previously disclosed information.

## Data integrity

- Use stable public identifiers and internal database identifiers.
- Record positive revisions on mutable user-owned objects.
- Use optimistic concurrency for adult/child simultaneous edits.
- Reject same-revision divergent content.
- Make retried consequential operations idempotent.
- Use transactions for state changes and their audit/outbox records.
- Prevent cycles and cross-workspace relationships.
- Preserve original attribution during corrections and imports.
- Fail closed for unknown schema, policy, export, or event versions.
- Store UTC instants plus the relevant local timezone/offset and semantic local
  date where user meaning depends on it.

## Messaging and notifications

External notification is driven through a transactional outbox so a UI cannot
report a successful send when the database change or provider enqueue failed.

Sensitive payloads contain:

- opaque message/cue ID;
- generic event class;
- target identifier;
- expiry; and
- no child name, message text, diagnosis, medication, task, school, person,
  location, or revealing action label.

The authenticated client retrieves detail after server authorization.
Notification history and mirrored-device fixtures follow the same boundary.

Rate limits, deduplication, recipient on-duty state, retry, quiet hours,
escalation prohibition, expiry, acknowledgement, and fallback behavior must be
explicit.

## Web and offline behavior

- Server-rendered or equivalent progressively enhanced core flows remain usable
  without JavaScript where safe.
- Every state-changing browser form uses CSRF protection.
- Authenticated navigation is network-only unless a separately reviewed,
  encrypted offline design is approved.
- Service workers may cache versioned public shell assets and a non-personal
  offline page, never authenticated child, guardian, school, message, or health
  responses.
- Browser-local drafts are account/workspace/object/tab scoped, encrypted where
  feasible, expire quickly, clear on sign-out, and are disclosed.
- The app never displays a successful send/save based only on an optimistic
  local state.

## Audit

Material events include:

- guardian/organization/role verification;
- child workspace activation or transition;
- relationship invitation, acceptance, renewal, pause, revocation, and
  suspension;
- scope and authority/consent changes;
- reads of protected school/health domains;
- disclosure preview/confirmation/delivery;
- child signal delivery and acknowledgement;
- planning/feedback/medication creation and correction;
- export, deletion, recovery, and break-glass access; and
- safety/dispute decisions.

Audit content is minimized and separately protected. It does not duplicate
free text unnecessarily. Child-facing history is a projection of authorized
events, not direct access to security metadata.

## Search, analytics, and observability

Search indexes are workspace- and field-scope aware and exclude protected
domains unless separately approved. Removing a relationship or object removes
future search access and schedules index deletion.

Analytics record only content-free operational events approved in the data
inventory. No diagnosis, message kind, medication, feedback, task text,
recipient, school, or child behavior enters analytics dimensions.

Logs and traces use opaque IDs, structured error classes, and redaction tests.
Support tooling does not expose content by default.

## Export, import, and migration

Exports:

- are workspace-scoped and purpose/version specific;
- require strong reauthentication and authority;
- separate child-readable, guardian, school/health, consent, and audit
  packages where rights differ;
- exclude password hashes, session secrets, provider credentials, raw
  verification evidence, unrelated workspaces, and operational keys;
- use encrypted transport/storage, short artifact expiry, and download audit;
  and
- never overwrite an existing destination silently.

Import is not part of the first child release. Any future import must be
atomic, idempotent, relationship-aware, policy-version aware, and fail closed
for foreign ownership, invalid authority, unknown domains, conflicts, or
unsupported retention.

## Backup, restore, and deletion

- Backups are encrypted, access-controlled, tested, and tenant/workspace
  restorable without exposing another workspace.
- Restore retains revisions, attribution, deletion state, consent, relationship
  status, and audit integrity.
- Deletion jobs enumerate active database, index, object storage, caches,
  outbox, processors, backups, and analytics.
- Backup expiry is part of the user-visible deletion contract.
- Legal/safety holds are narrow, authorized, reviewed, and do not reactivate
  user access.

## Production gates

No real child data until:

- threat models and DPIA/child-best-interests assessment are approved;
- identity, guardian, school, and role verification are implemented;
- server field-level authorization and negative tests pass;
- sensitive-data redaction fixtures pass across all sinks;
- backup/restore, revocation, deletion, role termination, and incident response
  are tested;
- accessibility and child comprehension gates pass;
- penetration and independent security reviews close blockers;
- operational owners and on-call/incident procedures exist; and
- the exact build and market are authorized in the release record.
