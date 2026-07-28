# Documentation review and next steps

Status: active project tracking

Updated: 2026-07-28

## Purpose

This note records the 2026-07-24 review of the repository documentation against
the implemented local PWA. It turns the review findings into an ordered,
evidence-gated work plan.

The product design remains proposed unless this note or an accepted decision
document identifies behavior as implemented. Statuses in this note must be
updated from repository, test, research, or release evidence rather than from
intent.

## Review outcome

The research and product documentation have a strong evidence model, clear
safety language, useful source provenance, and an explicit distinction between
the local application and later product phases. The original review identified
execution clarity as the main gap; this tracking note now provides the
operational view of what is implemented, partial, blocked, and gated by further
evidence.

No broken local Markdown links, anchors, or reference definitions were found in
the review. A current-source revalidation at commit `47000ad` passed all 72
automated tests on 2026-07-28. The interrupted-draft implementation added eight
browser tests, and the Drop-recovery implementation added seven more tests; the
current implementation passes all 87 automated tests. The suite covers
server-side account isolation, schema upgrades, migration recovery,
export/import behavior, representative real-browser complex-work flows,
Chromium interruption recovery, and JavaScript-disabled Drop recovery. This
closes UX-001 and UX-002's automated implementation findings, but not their
manual accessibility, broader-browser, real-device, or participant-usability
gates. Contrast, assistive-technology timer, and complete mobile focus-order P0
findings remain open. Complete timer and service-worker behavior still need
broader browser coverage.

## Confirmed implementation baseline

The following behavior is implemented:

- local account registration, login, and logout;
- password hashing, signed sessions, and CSRF-protected state-changing forms;
- per-user SQLite task isolation;
- SQLAlchemy Core persistence and ordered Alembic schema revisions;
- automatic upgrade of the exact legacy users/tasks database with
  pre-migration snapshot recovery;
- stable public UUIDs, installation origin, and positive revisions for users
  and tasks;
- versioned account-scoped JSON export/import for the current profile and task
  model, with operator CLI commands, secret exclusion, provenance retention,
  and fail-closed revision conflicts;
- capture to Today or Later;
- a separate three-item Remember list for short-term context-switching cues;
- one changeable daily highlight and at most three optional active Today
  actions;
- explicit recoverable Today overflow with user-controlled activation,
  highlight replacement, and save-for-later actions;
- task completion, restoration, move-to-Today, server-confirmed named Drop,
  immediate Drop Undo, and newest-ten account-scoped recovery;
- inline task editing and task workspaces with next action, definition of done,
  notes, and ordered components;
- account-, object-, form-, revision-, and tab-scoped browser-local task and
  project drafts with 24-hour expiry, sign-out clearing, and explicit stale
  revision handling;
- lightweight projects, preferred ordering, next-ready computation,
  prerequisites, external waits, follow-up tasks, and explicit overrides;
- explicit task-to-project conversion that preserves the task’s details,
  relationships, and Today placement as the first project task;
- workflow/readiness state kept separate from active/overflow Today placement;
- v5 account transfer with v1/v2/v3/v4 import compatibility, dropped-task
  timestamps, Remember items, and atomic relationship validation;
- a browser-local Low Capacity display toggle;
- a 5/15/25-minute client-side focus timer;
- responsive server-rendered pages;
- an installable PWA shell whose authenticated navigation remains network-only.

The following product-design capabilities are not implemented:

- fixed commitments or calendar objects;
- a Review destination or recovery/reset flow;
- transition or leave-by protection;
- persisted focus sessions or estimate-versus-actual learning;
- authenticated self-service export/restore, credential recovery, or an
  application-managed general backup/restore flow;
- Last Done tracked activities, schedules, occurrences, or execution history;
- Google Calendar integration;
- guardian or trusted-person assistance;
- hosted accounts, local-to-online migration, native applications, or AI.

The following behavior is partial and must not be described as the full proposed
capability:

| Capability | Implemented slice | Missing contract |
| --- | --- | --- |
| Low Capacity | CSS hides secondary Today content and stores a browser preference | No per-account state, current-time/commitment view, critical-item routing, smallest-action selection, or Reset |
| Focus | A non-persisted countdown can start, pause, continue, and reset | No session intention record, distraction capture, transition protection, next commitment, or actual-time history |
| Complex work | Task/project workspaces, conversion, existing-project assignment, components, order, blockers, readiness, and relationship transfer | No project collection/index, project navigation entry point, or completed/dropped project archive; assignment remains nested in task detail; five-participant prototype gate plus manual screen-reader and contrast review remain unverified |
| Backup and portability | Operator `instance/` backup, automatic pre-migration recovery, and versioned account/task CLI export/import | No self-service flow, credential recovery, full-account-type coverage, full operational restore rehearsal, or hosted adapter |

### Known project-workflow functional gaps

The current project data model and individual project workspace are
implemented, but the surrounding navigation is incomplete:

- there is no `/projects` collection route or other place to browse projects;
- no primary or contextual navigation control exposes a project list;
- a project is discoverable only through a linked task, the redirect after
  task conversion or component promotion, or a previously known direct URL;
- assigning a captured task to an existing project is implemented only inside
  task detail, nested under the project disclosure, and candidates are limited
  to active projects;
- the same disclosure presents both creating a new project and assigning an
  existing one, so the two distinct actions are not sufficiently visible;
- completed and dropped projects have no browsable archive or restoration
  entry point; and
- project pages return to Today rather than preserving the user’s originating
  Later or task context.

Closing this gap should add a lightweight project collection reachable from
Later, show each active project’s desired outcome and next-ready task, provide
a collapsed completed/dropped archive, and present **Add to existing project**
and **Turn into a new project** as separate task actions. This is a
discoverability and navigation slice, not authority to add Projects as another
mandatory primary destination or to expand whole projects into Today.

## Current priority interlock

The numbered milestone sequence remains authoritative, but it is subject to a
risk-based implementation interlock. Confirmed risk of data loss, an
inaccessible operation, or an unrecoverable destructive action must be resolved
before the next ordinary roadmap item. This does not renumber Phase 1 or mark a
later milestone complete.

The [UI/UX friction audit](ui-ux-friction-audit-and-requirements.md) was
originally run against commit `3cea2d1`. UX-001's interrupted-draft
implementation and automated Chromium gate are now complete in the current
source. Its manual accessibility, broader-browser, and participant-usability
evidence remains open. UX-002's Drop recovery implementation and automated
no-JavaScript gate are also complete. The remaining three P0 implementation
findings now have automated coverage: functional control, placeholder, and
focus-indicator contrast meet their documented thresholds; the focus countdown
is non-live and announces only meaningful transitions; and mobile Today visual
and sequential focus order agree.

Manual accessibility verification remains open. Participant validation,
attended screen-reader checks, 200% zoom, forced-colors, real-device touch
checks, and the complete Phase 1 day-loop gate remain unverified.

### Ranked development slices and current status

| Rank | Status | Slice | Why now | Smallest coherent exit gate |
| --- | --- | --- | --- | --- |
| 1 | Implemented; manual validation remains | Preserve interrupted task and project drafts | P0 data-loss risk in the exact interruption scenario the product is intended to support | Automated Chromium coverage passes for reload, Back, page close/reopen, failed and delayed saves, expiry, sign-out, and stale and concurrent-tab revisions; manual cross-browser, accessibility, and participant gates remain |
| 2 | Implemented; manual validation remains | Make Drop server-confirmed and recoverable | P0 destructive-action and recovery risk | Named server confirmation, dropped timestamp, newest-ten account-scoped recovery, restore-to-Later default, separate Add-to-Today, CSRF/ownership enforcement, and migration/transfer coverage pass automated tests; manual touch, keyboard, and participant gates remain |
| 3 | Implemented; manual validation remains | Close the remaining P0 accessibility blockers | Contrast, timer announcements, and mobile focus order can prevent predictable operation and would invalidate later participant evidence | Automated contrast, timer-transition, and mobile-order gates pass; manual keyboard, zoom, forced-colors, screen-reader, and real-device evidence remains |
| 4 | Not started | Complete minimum safe Low Capacity behavior | The current partial mode can hide every route to a startable task | Show the highlight or, without mutation, the first active Today task; retain compact Remember/Capture, hidden count, and Show full Today; no hidden work changes |
| 5 | Not started | Close milestone 1.2 discovery and validation | This is the remaining functional contract in the ordered plan once the safety interlock is clear | Later exposes a lightweight project collection and archive; assignment and creation are distinct; return context, ownership, CSRF, revision, browser/accessibility, and participant gates pass |

### Implemented first slice: interrupted-draft preservation

The current implementation adds durable interruption recovery to the existing
task-detail, project-detail, and inline autosave forms.

Implemented scope:

- define account-, object-, form-, revision-, and tab-scoped draft identity,
  expiry, restoration, and clearing rules;
- preserve field values synchronously before the delayed network save;
- retain the exact draft after a failed or delayed request;
- restore a valid matching draft after refresh or navigation;
- distinguish `Unsaved`, `Saving`, `Saved`, and `Could not save` without relying
  on colour alone;
- clear only the draft acknowledged by the server when no newer local edit
  exists;
- warn or preserve while navigation has unresolved changes;
- fail safely when the saved server revision has changed; and
- keep authenticated personal text outside the public service-worker cache.

Out of scope:

- a server-side draft table or export format;
- general offline mutation or cross-device synchronization;
- focus persistence;
- Drop recovery or general Undo;
- project collection, Review, or Reset; and
- caching authenticated pages or drafts in the service worker.

Implementation and verification surfaces are `timemanager/static/app.js`, the
task/project/inline form templates, authenticated account context and sign-out,
`tests/test_browser.py`, and `tests/test_pwa.py`.

Automated Chromium coverage now exercises immediate reload, Back, page
close/reopen, failed and delayed fetches, successful acknowledgement, sign-out
clearing, expiry, and stale and concurrent-tab revision conflicts. The
implementation retains a newer per-tab draft and never places draft text in the
service-worker asset list. Manual checks still need to cover a true offline
return, keyboard focus after restoration and conflict actions, screen-reader
save-state announcements, Firefox/WebKit behavior, Cache Storage inspection,
and participant usability. Those are verification and validation gaps, not
missing implementation behavior.

### Implemented second slice: server-confirmed Drop recovery

Drop now uses a server-rendered confirmation that requires the exact task title
and current revision. A successful Drop records `dropped_at`, redirects to an
account-scoped Recently dropped surface, and offers immediate Undo to Later.
The recovery surface shows the newest ten dropped tasks, restores to Later by
default, and presents Add to Today as a separate action for unblocked tasks.

The approved retention rule keeps older soft-deleted tasks in protected
database storage and account export without adding a deeper user-facing archive
or automatic purge. Export format v5 carries `dropped_at`; v1 through v4 imports
remain supported, with older dropped records receiving their saved
`updated_at` as the recovery timestamp.

Automated verification covers named confirmation, CSRF, ownership,
JavaScript-disabled operation, immediate Undo, repeated submission, stale
revisions, newest-ten ordering, the eleventh retained in export, Later and
Today restoration, migration backfill, and current and v4 transfer round trips.
Manual touch, full keyboard, broader-browser, and participant-usability checks
remain open.

### Implemented third slice: P0 accessibility blockers

Functional colors now use separate semantic tokens for primary and muted text,
placeholder text, active and disabled control boundaries, and focus
indicators. Automated calculations gate active controls and authored focus at
3:1 or better across supported adjacent surfaces and placeholder text at 4.5:1
or better across supported input surfaces.

The visible focus countdown is now a named, non-live timer. A separate atomic
polite status announces start, resume, pause, reset, duration changes,
boundary, and close without changing every second. Mobile Today no longer
moves the start-smaller card ahead of its source position, so DOM, rendered,
and focus-button order agree.

Automated coverage gates the functional color thresholds, timer semantics and
status stability, and mobile card and navigation order; Chromium exercises the
interactive and responsive checks. Manual keyboard, reverse-tab, 200% zoom,
forced-colors, magnifier, real-device, NVDA, VoiceOver, and timer-boundary
checks remain open, as does participant validation.

### Work held behind the interlock

- Review/Reset remains after P0 closure and milestone 1.2's functional gate.
  Validate stale-plan and recovery choices with synthetic scenarios before
  committing to the persistent interaction.
- Same-device focus persistence remains behind Low Capacity and milestone 1.2
  in the ranked development order; its accessible-timer precondition is now
  implemented. Cross-device continuation remains outside the current sync
  contract.
- Fixed commitments, Last Done, Phase 2 integrations, hosted accounts, native
  clients, optional AI, Day Context, and Quick Help retain their documented
  milestone and release gates. Documentation recency is not authority to change
  that order.

### Resolved dropped-task retention decision

The ordinary account-scoped recovery surface exposes the newest ten dropped
tasks. Older soft-deleted records remain in protected database storage and
account export. No deeper user-facing archive or irreversible purge is included
in this slice; either requires a separate evidence-backed retention decision.

## Findings that require decisions

### D1: Health-data boundary

Priority: scope resolved; privacy/legal release gate remains

The resolved boundary is:

- the Phase 1 local pilot and Phase 3 hosted release do not solicit, infer,
  categorise, or
  provide specialist health, diagnosis, medication, or treatment
  functionality;
- generic Last Done tracking intentionally supports private user-authored
  medication labels and execution history, but provides no dose, adherence,
  treatment, or missed-dose advice;
- medication-labelled histories are intentional health-data processing and
  require an applicable lawful basis/condition, privacy assessment, security
  controls, and jurisdiction review before hosted release;
- users may enter sensitive information in private free-text tasks and tracked
  activities, so all such content is treated as potentially sensitive and
  private by default;
- assistance workspaces do not provide health-specific fields or workflows and
  do not bulk-share private task content;
- every shared item receives an explicit disclosure preview; automatic
  detection of sensitive free text is not promised;
- notification importance and privacy are independent;
- account-wide notification details are hidden by default and users may opt out
  for Standard cues;
- a cue marked Sensitive always emits a generic, detail-free notification and
  contains no sensitive text in its push payload; the user must deliberately
  remove the classification before details can appear;
- external calendar providers control their own notifications, so every
  sensitive calendar write requires a boundary disclosure and a privacy-safe
  external-title choice.

The product scope is resolved. Implementation, privacy/legal, medication-safety,
and release evidence remain required before hosted activity tracking,
notification delivery, or assistance features can ship. Detailed requirements
are in
[Repeatable activity and execution-history requirements](repeatable-activity-history-requirements.md).

### D2: Milestone terminology and status

Priority: resolved in product design on 2026-07-24

The canonical product milestones are:

- Phase 0 — Prototype validation;
- Phase 1 — Local pilot;
- Phase 2 — Integrated local pilot;
- Phase 3 — Hosted release; and
- Phase 4 — Later extensions.

Delivery uses `Implemented`, `Partial`, `Not started`, `Blocked`, and `Deferred`.
User-research evidence is tracked separately as `Verified` or `Unverified`.
This prevents implementation progress from being presented as evidence that a
product hypothesis has been validated.

The capability catalogue records a target milestone and current delivery status
instead of using `Yes` or `No`. A resettable synthetic complex-work prototype,
walkthrough, and findings template are recorded. No participant findings are
recorded, so its evidence status remains Unverified. The authoritative
definitions and current capability statuses are in the
[high-level product design](high-level-product-design.md#canonical-milestones-and-statuses).

### D3: Local account topology

Priority: resolved in product design on 2026-07-24

One trusted Phase 1 local installation may contain multiple isolated accounts,
matching the implemented registration and per-user ownership model.

- Every user-owned object, query, mutation, export, deletion, restore, and
  hosted migration is scoped to one authenticated account.
- Co-residency creates no household, guardian, helper, or sharing relationship.
- Registration is not evidence of guardianship or trust.
- The installation is limited to a trusted machine and local network; it is not
  a public multi-tenant service.
- The installation operator can access the database, generated secret, and
  backups at the filesystem level.
- An `instance/` backup contains every account, while user-facing export and
  migration remain per-account.

The durable rationale and consequences are recorded in
[ADR 0002: Local account topology](decisions/0002-local-account-topology.md).

### D4: Product and feature phase naming

Priority: resolved in product design on 2026-07-24

The optional AI rollout uses `AI deployment stage A`, `B`, and `C`, all within
product Phase 4. These stages no longer collide with the canonical product
milestones and do not create separate delivery commitments.

The authoritative commercial structure is:

- subscription per primary user;
- monthly billing or discounted annual billing with the same entitlements;
- web and future native-mobile access in the base subscription;
- one guardian companion seat for a child or one trusted-support companion seat
  for an adult;
- a companion seat provides scoped support access, not an independent personal
  workspace; and
- optional advanced or future capabilities may be transparent one-off
  purchases, but core, accessibility, privacy, safety, export, deletion, and
  companion access remain in the base subscription.

Payment is never evidence of identity, age, guardianship, consent, or authority.
Exact prices and other billing mechanics remain decisions for implementation.
The authoritative detail is in the
[high-level product design](high-level-product-design.md#commercial-model).

### D5: Assisted-planning pilot topology

Priority: resolved in product design on 2026-07-24

The approved topology separates interface validation from live shared
relationships:

- Phase 2 uses synthetic family, relationship, and task data with same-device
  role simulation. It creates no remote invitations or persistent real child
  or assistance workspaces.
- Supervised sessions may involve real participants under an approved protocol,
  but use synthetic scenarios. Consented, minimised, de-identified research
  notes remain outside Timemanager.
- Real adult trusted-support relationships require a hosted, server-authorized
  pilot after authentication, authorization, audit, expiry, revocation,
  disclosure, and abuse-response gates pass.
- Real child workspaces additionally require country-specific legal/privacy
  approval, guardian-authority verification, a child-data impact assessment,
  an unsafe-family/coercion threat model, child-visible privacy, and tested
  deletion and incident-response procedures.

Email, payment, local-account co-residency, and possession of an invitation
never prove guardianship. The detailed topology and release evidence are in
[Assisted planning and guardian support](assisted-planning-and-guardian-support.md#validation-and-release-topology).

## Ordered execution plan

| Order | Work item | Current status | Exit gate |
| --- | --- | --- | --- |
| 0.1 | Resolve D1-D5 and align the documentation | Completed 2026-07-24 | No contradictory product boundaries; one milestone/status model |
| 0.2 | Add schema migrations and installation/public object provenance | Completed 2026-07-24 | Existing database upgrades without data loss; schema revision is inspectable |
| 0.3 | Add export, restore, and migration-fixture foundations | Completed 2026-07-24 | Export/import round trip is idempotent and tested; secrets are excluded |
| 1.1 | Enforce a deliberately small active Today plan | Completed 2026-07-24 | One highlight plus the chosen optional-task limit; overflow remains recoverable |
| 1.2a | Add task detail, next action, definition of done, and short components | Partial — implemented 2026-07-28; validation open | Capture remains title-only; added structure is optional, editable, owned, portable, and accessible |
| 1.2b | Add lightweight projects, ordering, dependencies, and external waiting | Partial — core model implemented 2026-07-28; discovery, navigation, archive, and validation open | One shallow hierarchy; projects and existing-project assignment are discoverable; readiness is separate from Today placement; blockers never silently rearrange Today |
| 1.3 | Add Review and consequence-aware Reset/recovery | Not started | No silent rollover; stale items can be kept, renegotiated, delegated, replaced, or dropped |
| 1.4 | Add manually entered fixed commitments and transition boundaries | Not started | Fixed and flexible objects remain distinct; next commitment stays visible |
| 1.5 | Complete Low Capacity semantics | Partial — browser-local display slice exists; completion work not started | Same underlying data; critical commitments, one action, capture, and Reset remain available |
| 1.6 | Extend focus into an optional bounded session record | Partial — client countdown exists; persisted-session work not started | Intention, boundary, interruption-tolerant actuals, and next-step outcome are user-controlled |
| 1.7 | Add generic Last Done activities and execution history | Not started | Manual create/log/query/correct/export passes exactness, privacy, time, and medication-safety criteria |
| 1.8 | Validate the complete non-AI day loop | Not started | Browser/accessibility tests plus recorded user-research evidence |
| 2.1 | Implement the notification attention/privacy contract | Blocked by 1.8 | Independent importance/privacy; private default; Sensitive payload and device views contain no details |
| 2.2 | Add Google Calendar behind explicit confirmation | Blocked by 1.8 | Provenance, timezone, recurrence scope, conflicts, provider failures, and external-notification privacy boundaries are visible |
| 2.3 | Prototype assisted planning under the approved topology | Blocked by 1.8 | Synthetic same-device roles, proposals, audit, expiry, revocation, disclosure previews, and safety gates pass |
| 3 | Build hosted accounts and rehearse one-time migration | Blocked by phases 1-2 | Tenant isolation, production operations, and migration evidence pass |
| 4 | Consider native clients and optional AI | Deferred | Separate validation and privacy/cost/safety approval |

## Verification work required

Maintain the current server-side test coverage and add proportionate tests as
each slice lands:

- migration tests starting from every supported prior schema;
- export/import idempotency, conflict, and secret-exclusion tests;
- task ownership and assistance-permission tests for every new query or
  mutation;
- task-detail and component tests proving that title-only capture remains
  available, added structure is optional and editable, and completion with
  unfinished components requires an explicit decision;
- project and dependency tests proving that preferred ordering is not a
  blocker, cycles and cross-account relationships fail closed, readiness
  responds to prerequisite lifecycle changes, and project completion is
  user-confirmed;
- Today tests proving that blocked tasks are not newly suggested and that
  blocking or unblocking work never silently promotes, removes, replaces, or
  highlights a task;
- assisted-prototype tests proving that Phase 2 uses synthetic same-device
  roles, sends no remote invitation, calls no external provider, and can reset
  the simulated workspace;
- hosted assistance-gate tests proving that real adult relationships require
  server authorization and that real child workspaces remain unavailable
  without the applicable market and guardian-authority approval;
- browser tests for capture, highlight limits, Low Capacity, focus boundaries,
  Reset, and offline navigation;
- an assertion that authenticated task pages are never stored in the service
  worker cache;
- notification tests proving that Sensitive titles, notes, people, locations,
  calendar details, and revealing action labels never enter push payloads,
  device previews, notification history fixtures, or mirrored-device fixtures;
- account-setting tests proving that opting out of generic previews affects
  only Standard cues and cannot override a Sensitive cue;
- external-calendar tests proving that a sensitive write requires the provider
  boundary disclosure and a privacy-safe external-title decision;
- repeatable-activity tests proving explicit execution provenance, exact
  day/time-slot answers, no-log-as-unknown semantics, duplicate warnings,
  backdating, timezone behavior, correction, export, and deletion;
- reflection-marker tests proving stable meanings across activity executions
  and task completions, no more than four quick choices, per-dimension
  exclusivity, the event selection limit, accessible text labels, no automatic
  selection, and Sensitive-default privacy;
- medication-safety tests proving that missing logs never become claims of a
  missed dose and never produce dose advice;
- keyboard, focus-order, screen-reader, reduced-motion, and contrast checks;
- timezone and daylight-saving tests before calendar integration;
- explicit-preview and failure-state tests for every external calendar write.

Python coverage alone is not evidence that the progressive client-side behavior
or PWA privacy boundary works in a browser.

The detailed milestone 1.2 behavior and separate exit gates are defined in
[Task detail and complex-work requirements](task-detail-and-complex-work-requirements.md).

## Research and review gates

Before expanding the feature set:

1. run or document the Phase 0 prototype tasks for capture, launch, transition,
   recovery, and Low Capacity;
2. test both minimalist and feature-rich-tool users;
3. record post-novelty and return-after-absence evidence, not only onboarding
   reactions;
4. preserve functional outcomes and wellbeing guardrails rather than optimizing
   task count, app opens, or streaks;
5. treat assistant-, calendar-, and helper-generated changes as editable
   proposals until the user explicitly confirms them.

The targeted source check performed for this review found the central clinical
and current regulatory/API claims consistent with the cited primary sources:

- [NICE NG87 recommendations](https://www.nice.org.uk/guidance/ng87/chapter/recommendations)
- [Komatsu et al. CBT component network meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11683884/)
- [BMJ ADHD interventions umbrella review](https://www.bmj.com/content/391/bmj-2025-085875)
- [OAIC draft Children's Online Privacy Code status](https://www.oaic.gov.au/news/media-centre/oaic-releases-exposure-draft-of-the-childrens-online-privacy-code)
- [ICO Children's Code introduction](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- [European Commission safeguards for children's data](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/are-there-any-specific-safeguards-data-about-children_en)
- [ICO special-category and health-data guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/)
- [OpenAI API data controls](https://developers.openai.com/api/docs/guides/your-data#default-usage-policies-by-endpoint)

This was a targeted validation of high-risk and time-sensitive claims, not a new
systematic review of every cited source. Recheck current legal, regulatory, and
provider-specific claims before implementing or releasing the affected feature.

## Maintenance rule

Update this note whenever a tracked item changes state. Link the commit, test,
research artifact, decision document, or release evidence that justifies the
change. Do not mark a phase complete because code exists; mark it complete only
when its stated exit gate passes.
