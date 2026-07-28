# Timemanager high-level product design

Status: proposed product direction

Updated: 2026-07-28

## Implementation status

Timemanager is currently a **partial Phase 1 local pilot**. The application
implements registration/login, local SQLite task persistence, Today and Later
capture, one daily highlight, completion/restoring, server-confirmed Drop with
newest-ten recovery, a minimum-safe Today-scoped Low Capacity view, and a
client-side focus timer with transition-only assistive announcements. Low
Capacity shows the saved highlight or one deterministic actionable fallback
without mutating task state, retains compact Remember and Capture, reports
hidden Today work, and provides a full-view escape. Functional-control,
placeholder, and focus-indicator contrast have automated thresholds, and mobile
Today no longer reorders a focusable card ahead of its DOM position.
Persistence now uses SQLAlchemy Core and ordered Alembic revisions with stable
public identifiers, installation provenance, and pre-migration SQLite
recovery. A versioned operator CLI can export one account's current
profile/task data, including dropped-task recovery timestamps, and import its
tasks into an explicit existing local account with idempotent revision
handling. Today now enforces one highlight plus at most three optional active
actions, with excess assigned tasks retained as explicit, user-controlled
overflow.

Task detail, ordered components, lightweight projects, preferred task order,
prerequisites, external waits, next-ready computation, and separate Today
placement are now implemented as a local-pilot slice. Later links to an
account-scoped project collection showing active outcomes and next-ready work,
with completed and dropped projects in a collapsed restorable archive.
Existing-project assignment and new-project creation are separate task actions,
and local return context is preserved. Its synthetic prototype and evaluation
materials exist, but no participant findings have been recorded. Manual
screen-reader, keyboard, zoom, forced-colors, and real-device verification also
remains open.
Self-service restore and credential recovery, Google Calendar, adult
trusted-person support, the Phase 3 hosted release,
local-to-online migration, AI, and native mobile applications remain
unimplemented.

### Canonical milestones and statuses

These milestone names are authoritative across the project:

| Milestone | Meaning | Current state |
| --- | --- | --- |
| Phase 0 — Prototype validation | Interviews and clickable validation of the core day loop | Evidence unverified |
| Phase 1 — Local pilot | Usable local PWA implementing and testing the non-integrated core | Partial |
| Phase 2 — Integrated local pilot | Calendar, privacy-safe notifications, adult trusted-person prototype, and complete-loop evaluation | Blocked by Phase 1 |
| Phase 3 — Hosted release | Production hosted accounts, security, operations, migration, and authorised integrations | Blocked by Phases 1–2 |
| Phase 4 — Later extensions | Native clients, optional AI, additional providers, and other deferred capabilities | Deferred |

Delivery status and validation evidence are separate:

- **Implemented:** present in code with proportionate automated verification.
- **Partial:** a useful slice exists, but its milestone exit criterion is
  incomplete.
- **Not started:** no executable slice exists.
- **Blocked:** work cannot pass its exit gate until a named dependency or
  decision is resolved.
- **Deferred:** deliberately outside the current delivery sequence.
- **Verified evidence:** the required validation artifact exists and is linked.
- **Unverified evidence:** the required validation artifact is absent or has
  not been linked.

An implementation status does not establish that a product hypothesis has been
validated with users. A synthetic complex-work prototype is recorded, but its
five-participant gate has not been run, so Phase 0 evidence remains Unverified.

## Purpose

Timemanager is a day companion for adults who need external support with
remembering, choosing, starting, switching, and recovering. Its first job is not
to manage an entire life or maximise completed tasks. It is to make the current
day understandable and help the user take the next useful action without losing
fixed commitments.

The product supports day-to-day functioning. It is not an ADHD diagnostic tool,
clinical treatment, crisis service, employee-monitoring system, or substitute
for a clinician, coach, carer, or trusted person.

## Design basis

This design translates the repository's research into a product hypothesis:

- **Supported foundation:** external capture, calendar/task separation,
  prioritisation, task decomposition, time awareness, distraction management,
  and review.
- **Plausible product design:** the exact daily dashboard, recommendation
  model, recovery flow, estimate-learning method, and notification budget.
- **Experiential options:** energy matching, body doubling, strict focus
  controls, ambient surfaces, and some forms of gamification.

Related research:

- [ADHD-friendly time-management domain research](adhd-time-management-domain-research.md)
- [Reference-system analysis](reference-systems-analysis.md)
- [Reddit app-experience analysis](reddit-app-experience-analysis.md)
- [Optional AI body-doubling and voice design](ai-body-doubling-and-voice-design.md)
- [Day Context and within-day history requirements](day-context-history-requirements.md)
- [Private medication context and schedule support requirements](medication-context-support-requirements.md)
- [Future Quick Help, mood, energy, and focus support](quick-help-mood-energy-design.md)

## Confirmed direction and working assumptions

The delivery direction is:

1. build and validate the Phase 1 local pilot as one trusted local installation
   with multiple isolated accounts in a home-lab environment;
2. use a responsive web/PWA interface from the beginning;
3. release the product as the Phase 3 hosted PWA with user accounts;
4. add native mobile application clients after the Phase 3 hosted release;
5. let a local user optionally perform a one-time migration of selected
   Timemanager data into an online account;
6. integrate Google Calendar first, with explicitly confirmed event creation
   and editing, and add other calendar providers later;
7. validate an adult trusted-person prototype in the Phase 2 integrated local
   pilot using synthetic data and same-device role simulation;
8. exclude AI decomposition, voice, AI body doubling, health-oriented Quick
   Help, Day Context state/event tracking, and structured medication context
   through the Phase 3 hosted release.

The Phase 1 local pilot is a development stage, not a supported self-hosted
edition or a permanent promise that the released product will be local-first or
fully offline. The core product remains designed so that AI is never required.

## Commercial model

The Phase 3 hosted product uses a simple subscription per adult primary user.

- A monthly subscription and a discounted annual subscription provide the same
  product entitlements; the annual option changes price and billing period, not
  feature access.
- The base subscription includes access to the web application and, when
  released in Phase 4, the native mobile applications. A primary user is not
  charged a separate platform subscription.
- The subscription includes one trusted-support companion seat.
- A companion seat grants only the permissions approved by the adult primary
  user. It does not include an independent
  personal planning workspace; a companion who uses Timemanager for their own
  plan needs their own primary-user subscription.
- Phase 1 local-pilot use has no payment dependency.

Future advanced capabilities may be offered as clearly identified, optional
one-off purchases. Such purchases must be additive. Core capture and planning,
web/mobile access, the included companion seat, accessibility, privacy and
security controls, export, deletion, and safety functionality remain part of
the base subscription. A one-off offer must state whether it depends on an
active hosted subscription and must not imply perpetual third-party or compute
service where that cannot be sustained.

Exact prices, discount percentage, taxes, trials, refunds, regional billing,
additional companion seats, and the first eligible one-off capabilities remain
commercial decisions to make before billing launches.

Payment establishes a billing relationship only. It is not proof of identity,
trust, consent, or authority over another user. The product does not use
advertising, behavioural profiling, data brokerage, or personal planning data
as a revenue source.

The subscription structure is a product decision, not evidence that users will
find its eventual price fair or sustainable. Research signals include both
willingness to pay for a useful tool and strong resistance to recurring or
surprising charges. Before billing launches, validate pricing clarity and
willingness to pay, show terms before data import, and make cancellation,
account-scoped export, and deletion straightforward. See the
[Reddit app-experience analysis](reddit-app-experience-analysis.md#14-price-and-trust-affect-retention).

## Product outcomes

The product should help the user:

- capture a commitment before it is lost;
- see appointments, leave-by times, deadlines, and available capacity together;
- choose a small, credible active plan;
- convert ambiguous work into a visible first action;
- begin with less activation effort;
- remain aware of elapsed time and the next fixed commitment;
- stop, switch, or continue deliberately;
- recover after an interruption, changed day, or absence without backlog debt;
- learn from estimated and actual duration without being surveilled or graded;
- let an adult invite a partner, friend, or other trusted person to help with
  selected tasks, appointments, reminders, and check-ins;
- trust that the system reflects current commitments.

Primary success is improved functioning and reduced planning burden. Task count,
hours logged, streak length, and app-open frequency are not primary outcomes.

## Product principles

1. **Capture first, classify later.** Only a title is required to save.
2. **One home, several views.** Today, Later, Low Capacity, and Review are views
   over the same objects.
3. **The present is deliberately small.** The active plan is not the backlog.
4. **Fixed commitments remain visible.** Capacity can change the plan but does
   not hide consequences.
5. **Starting, switching, and recovering are explicit product moments.**
6. **Recommendations explain themselves.** The user can always override them.
7. **Time is visible and empirical.** Estimates are ranges; missing actuals
   remain unknown.
8. **Recovery is normal operation.** No automatic punishment, forced catch-up,
   or silent rollover.
9. **Support intensity is chosen.** Gentle cues are the default; stricter modes
   are temporary and reversible.
10. **The core works without AI.** AI may assist but never owns the plan.

## Core experience

```text
Capture
   |
   v
Orient ---- changed day / return ----> Recover
   |                                  |
   v                                  |
Commit to a small plan <--------------+
   |
   v
Launch -> Focus -> Transition
   ^         |          |
   |         v          v
   +---- resume      Close / next action
                         |
                         v
                  Weekly learning
```

### 1. Capture: "Do not let me lose this"

The global capture action is available from every primary screen and can save
in one interaction.

Core functionality:

- require only a short title;
- preserve the original text and capture timestamp;
- allow optional quick choices: task, fixed event, note, or "decide later";
- accept text first, with voice, share-sheet, widget, and watch capture later;
- place ambiguous items in one inbox;
- allow an immediate undo;
- never require project, priority, duration, energy, date, or category before
  saving.

If date/time language is detected, the system may propose structured fields but
must show the interpretation before treating it as a real deadline or event.

### 2. Orient: "What is real today?"

Today is the default screen. It combines fixed commitments with a deliberately
small flexible plan while preserving their different meanings.

It shows:

- current time and day progress;
- the next fixed commitment and any prepare/leave-by boundary;
- calendar commitments on a compact timeline;
- unresolved consequence-bearing deadlines;
- the chosen daily highlight;
- up to three optional active actions by default;
- inbox items that need urgent clarification;
- available focus windows and explicit buffer;
- one persistent capture control.

The timeline must visually distinguish imported calendar events, user-created
fixed commitments, and intended flexible work. A planned focus session must
never look like an immovable appointment.

### 3. Commit: "What would make today count?"

The user chooses:

- one **highlight**: the meaningful win or stabilising action for the day;
- genuine **musts**: fixed or consequence-bearing commitments;
- a small set of **options**: ready next actions that fit remaining time and
  capacity.

The system can recommend candidates using facts kept separate in the data:

- deadline and consequence;
- calendar fit and leave-by protection;
- readiness and dependencies;
- estimated duration;
- current capacity/context;
- value or outcome link;
- recent deferral or failed starts.

Every recommendation includes a short reason such as "Due tomorrow, ready,
about 20-30 minutes." The system does not invent urgency, and the user can
choose another action without penalty.

### 4. Launch: "Help me cross the start line"

Opening an active task prioritises action over metadata.

The launch view shows:

- the observable next action;
- a definition of done;
- required material, location, file, or link;
- an optional two-to-five-minute starter;
- expected duration as a range;
- the next fixed commitment;
- a prominent Start action.

For vague work, the user may request decomposition. Manual or AI-assisted
decomposition initially reveals one to three proposed actions, keeps the rest
collapsed, and requires confirmation before changing the task.

### 5. Focus: "Keep me with this"

A focus session is a bounded work container, not just a countdown.

At start, the user chooses or accepts:

- session intention;
- initial duration;
- preferred cue intensity;
- whether optional distraction blocking or body doubling is active.

During the session, the product shows:

- task and intended outcome;
- elapsed and remaining time;
- next fixed commitment and safe stopping boundary;
- pause, continue, stop, and end controls;
- one-tap distraction capture that returns focus immediately;
- a low-stimulation display mode.

At the boundary, the system asks the user to continue, pause, stop, or capture a
next step. Continuing must not suppress a transition or leave-by alert.

### 6. Transition: "Help me stop and switch"

Transitions protect commitments and reduce the mental cost of resuming later.

The system may issue staged cues for:

- prepare;
- save and close;
- leave;
- arrive or start.

The transition view offers:

- record what changed;
- capture the next visible action;
- mark done, waiting, paused, or deliberately dropped;
- snooze within a safe range;
- move to the next commitment.

Dismissing a sound does not resolve the underlying intention. It remains
visible until the user makes a choice or the consequence is re-triaged.

### 7. Recover: "The day changed"

Recovery is available at any time and becomes the default return path after a
long absence or a large stale plan.

The flow:

1. acknowledge that circumstances changed without scoring failure;
2. show the current time and next fixed commitment;
3. surface only unresolved items with real consequences;
4. let the user do, renegotiate, delegate, replace, or drop them;
5. choose one "now" action or stabilising action;
6. move everything else to Review rather than Today.

No flexible task automatically rolls into the next day. "Overdue" is a
time-relative condition, not a permanent identity or accumulating red list.

### 8. Close: "Let me trust tomorrow"

The optional end-of-day close is short and can be deferred.

It asks:

- what was completed, changed, or intentionally dropped;
- which unresolved consequences need a decision;
- whether a next action should be saved;
- what the first fixed commitment tomorrow is.

The close does not require journaling, complete time logs, or inbox zero.

### 9. Learn: "Help plans become more realistic"

A five-minute weekly review presents a small number of patterns:

- estimates compared with actual focused and elapsed time;
- commitments met or consciously renegotiated;
- repeated start friction;
- transition collisions;
- stale inbox or review items;
- successful returns after interruptions.

The user selects one experiment for the next week, such as adding more travel
buffer or using a smaller first focus interval. There is no grade, leaderboard,
punitive streak, or task-count target.

## Modes and support intensity

### Standard mode

Shows the full Today view, active plan, timeline, and optional planning detail.

### Low-capacity mode

Uses the same data and retains only:

- current time;
- next fixed commitment and leave-by time;
- user-designated essential and consequence-critical items;
- one highlight or stabilising action;
- one smallest next action;
- capture and Reset.

Hidden information is not deleted or forked into another plan.

### Support intensity

The user can choose a default and override it per task/session:

| Level | Behaviour |
|---|---|
| Quiet | Visual state only; interruptive cues only for explicitly protected commitments |
| Gentle | One start cue and one boundary cue with ordinary snooze choices |
| Structured | Staged prepare/start/transition cues and a required visible decision |
| Strict | Temporary user-configured blocking or accountability with a clear safe exit |

Strict support is never enabled globally without explicit setup and must be easy
to stop.

## Information architecture

The Phase 3 hosted release has four primary destinations:

| Area | Purpose |
|---|---|
| Today | Orient, choose, launch, transition, and recover |
| Later | Clarify captured items and find work outside Today |
| Review | Revisit deferred work and run the weekly learning loop |
| Settings | Calendar, cues, accessibility, privacy, data, and optional integrations |

Task detail and Focus are contextual views reached from Today, Later, or Review.
Projects are initially lightweight outcome groupings inside task detail, not a
separate primary destination. The current local pilot provides a lightweight
collection reached from Later, so active and archived projects are discoverable
without adding another place the user must routinely check. Existing-project
assignment and new-project creation are separate task actions. Search is a
utility, not a fifth place the user must check.

## Feature catalogue and phasing

Statuses describe the current repository, not the intended milestone scope.

| Capability | Target milestone | Current status | Later extension | Confidence |
|---|---|---|---|---|
| Universal text capture and task clarification | Phase 1 | Implemented | Voice, widget, watch, share-sheet | Supported foundation |
| Today timeline with fixed commitments | Phase 1 | Partial | Multi-calendar reconciliation | Supported foundation |
| Highlight plus small active plan | Phase 1 | Implemented | Learned capacity limit | Supported method; plausible interface |
| Three-item Remember cues | Phase 1 | Implemented | Usability validation | Plausible context-switching aid |
| Manual next action and definition of done | Phase 1 | Partial — functional slice implemented; validation open | Suggested decomposition | Supported foundation |
| Short task components and lightweight projects | Phase 1 | Partial — model, workspaces, collection, navigation, and archive implemented; validation open | Richer project views | Supported decomposition; plausible interface |
| Dependencies and external waiting | Phase 1 | Partial | Richer dependency analysis | Supported readiness question; plausible state model |
| Flexible focus session | Phase 1 | Partial | Stronger blocking and AI body doubling | Supported elements; experiential options |
| Adult trusted-person support | Phase 2 | Blocked by Phase 1 | Additional scoped planning and focus-support controls | Plausible/experiential; privacy-sensitive |
| Transition and leave-by cues | Phase 1 | Not started | Location/event-triggered cues | Plausible interface |
| Recovery/reset without rollover | Phase 1 | Not started | Personalised recovery suggestions | Plausible product design |
| Estimate versus actual | Phase 1 | Not started | Reference-class duration ranges | Supported mechanism; plausible algorithm |
| Last Done repeatable activity history | Phase 1 | Not started | Task/calendar links and natural-language retrieval | Plausible product design; privacy-sensitive |
| Weekly review and one experiment | Phase 2 | Not started | Longer-term pattern comparison | Supported components |
| Low-capacity mode | Phase 1 | Partial — minimum-safe Today slice implemented; commitments, Reset, and validation open | User-defined low-capacity layouts | Plausible product design |
| Account data portability | Phase 1 | Partial | Authenticated self-service restore and hosted adapter | Required trust and migration foundation |
| Google Calendar integration | Phase 2 | Blocked by Phase 1 | Other providers | Supported need; integration behavior to test |
| AI voice/body doubling | Phase 4 | Deferred | Opt-in connector | Experiential/early research |
| Day Context state and event history | Phase 4 | Deferred | Mood, energy, focus, food, caffeine, exercise, and disruption timeline with descriptive summaries | Plausible product design; health-data and interpretation sensitive |
| Private medication context and schedule | Phase 4 | Deferred | User-owned medication list, versioned user-recorded schedule, explicit executions, and reviewed non-dose support | Plausible product design; clinical-safety, privacy, and regulatory sensitive |
| Quick Help | Phase 4 | Deferred | Reviewed playbooks, Day Context integration, optional AI phrasing, and user-authored personal plans | Plausible product design; health-data and clinical-safety sensitive |
| Goals, habits, journaling, social features | Deferred | Deferred | Only after core validation | Unproven for the core job |

## Core information model

### Entities

- **Capture item:** original input, source, timestamp, and clarification state.
- **Task:** title, next action, definition of done, workflow status, Today
  placement, consequence, true deadline, estimate range, context, capacity fit,
  value link, dependencies, external waiting, and provenance.
- **Task component:** an optional short checklist step that cannot contain
  components or dependencies and does not independently enter Today.
- **Project/outcome:** optional shallow grouping with a desired outcome,
  preferred task order, and one next-ready task.
- **Task dependency:** an account-owned prerequisite relationship, distinct
  from preferred order and from external waiting.
- **Commitment:** fixed time interval, source calendar, preparation/leave-by
  boundaries, and sync provenance.
- **Daily plan:** date, highlight, selected actions, capacity mode, and explicit
  user choices. It references tasks rather than copying them.
- **Focus session:** intention, planned range, elapsed/focused time, pauses,
  outcome, and optional interruption labels.
- **Tracked activity:** a user-owned repeatable action with optional schedules,
  privacy classification, and Last Done retrieval.
- **Scheduled occurrence:** a date-specific expectation for a tracked activity;
  it is not evidence that the activity happened.
- **Activity execution:** an explicit user record of when an activity happened,
  when it was logged, optional notes, reflection markers, user tags, and source
  provenance.
- **Experience annotation:** zero or more optional selections from a compact,
  system-defined reflection-marker vocabulary attached to a user-confirmed
  outcome such as an activity execution, task completion, or focus-session
  outcome.
- **Cue:** trigger, importance, privacy classification, channel, status, snooze
  choices, generic-preview policy, and linked intention.
- **Review decision:** keep, schedule, renegotiate, delegate, replace, or drop,
  with an optional reason.
- **Experiment:** one temporary behavior change and a review date.
- **Support session:** explicit invitation, shared intention, presence/check-in
  state, expiry, revocation, and the minimum task/session fields disclosed.
- **Assistance workspace:** the adult owner, approved helpers, relationship
  type, permission scope, and audit history.
- **Assistance proposal:** a helper-created task, appointment, reminder, or
  assignment suggestion with its proposer, recipient, status, and explicit
  acceptance/rejection history.
- **Installation/account provenance:** stable object identifiers, source
  installation/account, revision, and migration/import state used when local
  data is moved online.

### Task states

```text
Captured -> Ready -> Active -> Done
           |        |
           v        v
        Waiting   Paused
           |        |
           +--> Ready

Any unresolved state -> Dropped
Ready/Paused -> Scheduled -> Active
```

Dates and views do not silently change task state. Completion, dropping, and
external calendar writes are auditable user actions.

## Functional rules

- Title is the only required field at capture.
- A fixed commitment and a flexible task remain different object types.
- Today contains references to tasks; it is not another task database.
- Flexible tasks do not automatically roll over.
- Imported objects retain source and last-sync provenance.
- Conflicting external changes are shown for user resolution.
- Assistance access is scoped, expires, is auditable, and can be revoked.
  Adult helpers cannot silently complete, drop, reschedule, or broaden access
  to another adult's plan.
- Recommendations expose the facts used and label inferred values.
- AI-generated content is marked as suggested until accepted.
- The product does not solicit, infer, categorise, or provide specialist
  functionality for diagnosis, medication, treatment, or other health
  information in the Phase 1 local pilot or Phase 3 hosted release.
- Generic tracked activities intentionally allow private, user-authored labels
  and execution history, including medication as a supported record-keeping use
  case. This does not add dose, treatment, adherence, or missed-dose advice.
- Users may enter sensitive information in private free-text tasks and tracked
  activities. All such content is treated as potentially sensitive and remains
  private by default.
- A scheduled occurrence or missing execution is not proof that an activity did
  or did not happen. Positive answers cite explicit executions; missing history
  is reported as unknown.
- Task completion and calendar presence do not create an activity execution
  without explicit user confirmation.
- Reflection markers use the same stable meanings across supported outcome
  types. The primary flow shows no more than four context-relevant choices,
  never preselects or infers one, and keeps notes and user-owned organisational
  tags separate.
- Reflection markers are optional private annotations, not scores or evidence
  for diagnosis, automatic prioritisation, helper disclosure, or performance
  judgment.
- Missing duration or completion data remains unknown, not zero or failure.
- Notification delivery and intention resolution are separate states.
- Notification importance and notification privacy are independent. A
  high-consequence cue can still suppress all details on the device.
- Time calculations preserve timezone and daylight-saving semantics.
- The active day remains readable during temporary network or provider failure.
- Local and hosted records use stable identifiers and schema versions so a
  migration can be retried safely.
- The current local operator CLI can export one account's implemented
  profile/task model without credential material and retry an import into an
  explicit existing local account. Authenticated self-service export, deletion,
  credential recovery, complete future-object coverage, and hosted migration
  remain required.
- The eventual user-facing product must support export and deletion; optional
  AI memories and transcripts have separate controls.

## Notifications and attention budget

Notifications have two independent classifications: **importance**, which
controls interruption and persistence, and **privacy**, which controls what may
leave the authenticated application.

Importance is allocated by consequence rather than independently requested by
every feature:

- **Protected:** user-designated essential reminders, selected appointments,
  travel, or real deadlines; may use staged interruptive cues.
- **Actionable:** starts, transitions, and review prompts; grouped and limited.
- **Ambient:** Later counts, suggestions, and weekly patterns; visible in-app,
  not interruptive by default.

Privacy is selected separately:

- **Standard:** the account's notification-preview preference applies.
- **Sensitive:** the device notification contains only the Timemanager
  identity, generic wording such as "Private reminder," and an opaque cue
  identifier. It contains no task title, notes, health details, people,
  location, calendar details, or revealing action labels.

`Hide notification details` is enabled by default at account level. A user may
opt out and allow details for standard notifications. The account setting never
overrides a cue marked Sensitive; the user must deliberately remove the
Sensitive classification before details can appear.

Sensitive content is not placed in a push payload and is retrieved only after
the user opens the authenticated application. Generic snooze or open actions
may be offered only when they reveal no task information. This contract applies
to Timemanager-generated notifications, notification history, and mirrored
notifications such as a connected watch.

The product shows the user when a day has become cue-heavy and suggests
consolidation. Muting a channel is respected; the related intention remains
visible in Today or Review.

## Integrations

### Calendar

Initial behavior:

- connect Google Calendar;
- import events from the selected calendars;
- refresh and cache upcoming fixed commitments;
- preserve source calendar, event identifier, timezone, and sync status;
- allow local preparation and leave-by cues without modifying the source event;
- let the user create or edit a Google Calendar event only after previewing and
  explicitly confirming the destination calendar, date, time, timezone, title,
  and affected recurrence scope;
- retain an audit record and surface provider failures without falsely showing
  the local action as synchronized.

Timemanager must never silently reschedule an event. Calendar deletion and
attendee-management workflows are outside the initial integration unless
separately designed and approved.

Timemanager can enforce its privacy classification only for notifications it
generates. Google Calendar or another connected client may independently show
an event title, location, attendee, or description. Before a sensitive item is
written to an external calendar, the confirmation view must disclose that
boundary and let the user choose a privacy-safe external title and notification
configuration, or cancel the write.

Other calendar providers should implement the same internal commitment boundary
after the Google integration is stable; provider-specific objects must not leak
into the core task model.

### Adult trusted-person support

Adult trusted-person support is a Phase 2 prototype capability, not merely a
body-doubling session. An adult may invite a partner, friend, family member,
coach, or other chosen helper to assist with selected planning work.

The default helper action is a proposal for the adult to accept, adjust, or
decline. Every scope is explicit, time-limited, auditable, and revocable.
Health histories and private state/context records remain excluded by default.

The detailed role, permission, workflow, privacy, and release-gate design is in
[Adult trusted-person support](trusted-person-support.md).

### Local-to-online data transfer

The Phase 1 local pilot and Phase 3 hosted service should share versioned domain
schemas and stable object identifiers from the start. When the hosted PWA is
available, a pilot user may explicitly connect or sign in to an online account
and preview the data to transfer.

The local installation may contain multiple isolated accounts. Export,
deletion, restore, and migration initiated through the application are scoped
to the authenticated account. A migration never selects another local
account's data. An operator-level `instance/` backup is different: it contains
the shared database, generated secret, and every account, and must be protected
as a whole.

Eligible data includes:

- tasks, projects, capture items, and daily plans;
- user-entered commitments and calendar-link provenance;
- focus-session summaries, cues, review decisions, and experiments;
- user preferences that are safe and meaningful across environments.

The transfer must:

- be opt-in and show its scope before upload;
- use encrypted transport and an authenticated destination account;
- preserve source installation, timestamps, revisions, and dropped/completed
  states;
- be idempotent so a retry does not create duplicates;
- preview conflicts and never overwrite newer data silently;
- provide a completion report and retain a local export/backup;
- exclude local secrets, Google tokens, server configuration, raw operational
  logs, and any unselected sensitive content;
- require Google authorization again in the hosted account.

This is a one-way, resumable migration from local to online:

- the user chooses a cutover point and the hosted account becomes authoritative
  after successful migration;
- retries are idempotent, but completing a migration does not establish an
  ongoing synchronization link;
- the local database is retained as a backup until the user deliberately
  archives or deletes it;
- the Phase 1 local pilot receives no supported self-hosted
  release lifecycle after the hosted cutover;
- the product warns that edits made in the local instance after cutover will
  not appear online;
- the migration completion report identifies anything skipped or requiring
  manual resolution.

Ongoing bidirectional synchronization between the home-lab and hosted
installations is explicitly out of scope. Mobile and PWA clients may later
synchronize through the hosted service; that is a separate online-client
contract.

### Optional AI

The AI boundary follows the
[AI body-doubling and voice design](ai-body-doubling-and-voice-design.md):

- disabled by default;
- narrow task/timer tools;
- minimum session context;
- proposed mutations require confirmation;
- raw audio and transcripts are not retained by Timemanager by default;
- the planner and local focus timer work without the provider.

### Future surfaces

Native mobile applications follow the online PWA and use the hosted account and
the same domain identifiers. Widgets, wearables, ambient displays, print, and
native clients show or capture the same current state. They do not introduce
independent task stores.

## Accessibility, privacy, and resilience

- Offer low visual density, reduced motion, readable contrast, keyboard
  operation, screen-reader semantics, and non-colour status cues.
- Avoid urgency-coded red except where a real consequence justifies it.
- Let the user control animation, sound, haptics, cue density, and default
  session intensity.
- Minimise collected data and make sync/AI boundaries visible.
- Treat task and commitment text as potentially sensitive even when the product
  does not request sensitive categories.
- Keep private notification details out of push payloads. Require
  authentication before displaying a Sensitive cue's content.
- Keep credentials server-side and out of clients and source control.
- Provide data export, deletion, backup, and restore before relying on the
  system as the only trusted store.
- Preserve local-version data through restarts. In the hosted PWA, preserve a
  safe last-known view and clearly indicate lost connectivity; offline mutation
  guarantees require a separate synchronization design.
- Never use personal task or focus data for employee scoring or undisclosed
  model training.

## Evaluation plan

### First prototype questions

Test whether a user can:

1. capture an appointment, flexible task, and vague project without training;
2. understand what is fixed versus optional today;
3. choose a credible highlight and small active plan;
4. start a vague task with or without decomposition;
5. notice and act on a transition boundary;
6. recover from 20 stale items after a week away;
7. use Low Capacity mode without losing trust in hidden information;
8. complete a session with all nonessential notifications disabled;
9. create and log a repeatable activity quickly, then distinguish "no log" from
   "did not happen" when retrieving its history.

### Pilot measures

- time from task choice to first action;
- commitments met or consciously renegotiated;
- late departures or missed fixed commitments;
- estimate-versus-actual calibration;
- number of silent rollovers, which should remain zero;
- successful return after interruption or absence;
- planning effort, overwhelm, and perceived control;
- inbox age and maintenance time;
- notification dismissal/muting;
- repeatable-activity logging effort, answer accuracy, corrections, and
  duplicate-warning rate;
- trust that current commitments are represented.

Measure abandonment and return after the novelty period. Qualitative reports of
pressure, shame, surveillance, sensory load, or unwanted data use are guardrail
signals, not acceptable costs of higher task completion.

## Delivery sequence

### Phase 0: prototype validation

- clickable prototypes for Capture, Today, Launch, Focus, Transition, and Reset;
- interviews and moment-by-moment walkthroughs of difficult days;
- explicit testing with both minimalist and feature-rich-tool users;
- record the required evidence before treating Phase 0 as complete or expanding
  beyond the current implementation.

### Phase 1: local pilot

- one trusted local installation with multiple isolated accounts;
- responsive web/PWA client backed by the home-lab service;
- text capture and inbox;
- manually entered commitments;
- Today, highlight, and small active plan;
- task detail, next action, definition of done, and short components;
- lightweight projects, preferred ordering, prerequisites, external waiting,
  and one next-ready task;
- local focus session and transition protection;
- Low Capacity and Reset;
- basic optional estimate-versus-actual recording;
- generic Last Done tracked activities, schedules, manual executions, exact
  history retrieval, optional notes, shared reflection markers, user tags, and
  Sensitive-by-default privacy;
- protected operator backup and versioned account-scoped export/import
  foundation;
- stable object identifiers and versioned schemas suitable for later transfer;
- no AI features.

### Phase 2: integrated local pilot

- authenticated Google Calendar read plus confirmed event creation/editing;
- fixed-event sync, provenance, caching, and conflict visibility;
- adult trusted-person support prototype using synthetic data, same-device role
  simulation, scoped proposals, and start/end check-ins;
- supervised usability sessions may use real participants under an approved
  protocol, but participants interact with synthetic scenarios and create no
  persistent assistance workspace;
- notification budget, independent importance/privacy controls, private
  previews, and staged leave-by cues;
- short weekly review and one experiment;
- diary study and post-novelty retention evaluation;
- extend the current export/import fixture rehearsal through a staged hosted
  adapter without uploading pilot data to a production service.

### Phase 3: hosted release

- authenticated hosted accounts and tenant isolation;
- PostgreSQL persistence with production migration, backup, restore, monitoring,
  and recovery evidence;
- monthly and discounted annual billing per adult primary user, including one
  trusted-support companion seat;
- production Google authorization, event reads, and explicitly confirmed event
  creation/editing;
- authenticated, expiring trusted-person invitations and server-side
  permission enforcement;
- stage real adult trusted-support relationships only after authorization,
  audit, expiry, revocation, disclosure, and abuse-response gates pass;
- optional, user-previewed one-time migration from the local version;
- backup, export, deletion, rate limiting, and operational recovery;
- online PWA deployment with clear connectivity state;
- no dependency on AI.

### Phase 4: later extensions

- native mobile applications using the hosted backend and included in the
  primary user's existing subscription;
- push notifications and mobile capture surfaces;
- an explicit mobile offline/synchronization contract;
- additional calendar providers;
- stronger temporary focus controls;
- user-confirmed decomposition suggestions and opt-in AI body-doubling features
  only after separate validation;
- user-owned Day Context history for mood, energy, focus ability, activities,
  and disruptions only after privacy, interpretation, and usability gates;
- private medication profiles and schedules with reviewed non-dose support
  only after clinical-safety, privacy, security, medicine-identity, and
  jurisdiction gates;
- user-invoked Quick Help with a non-AI path and optional Day Context
  and medication-context integration only after separate clinical-safety,
  privacy, and usability gates.

## Explicitly out of the Phase 3 hosted release

- a general notes or knowledge-management system;
- complex project portfolios or goal trees;
- habit streaks and life-score dashboards;
- automatic calendar rescheduling;
- opaque AI prioritisation or silent task mutation;
- public social feeds, leaderboards, or default sharing;
- employer, clinician, or caregiver surveillance;
- clinical diagnosis, treatment recommendations, or symptom-efficacy claims.

## Resolved product decisions

- The Phase 1 local pilot runs in a local home-lab environment.
- SQLite remains the Phase 1 database behind SQLAlchemy Core and Alembic.
  PostgreSQL is the Phase 3 hosted target; SQLite-to-PostgreSQL transfer uses
  account-scoped export/import rather than direct file conversion.
- One trusted local installation may contain multiple isolated accounts.
  Co-residency creates no sharing or assistance permission; the installation
  operator remains able to access the local database and backups.
- The Phase 3 hosted release is the first production release.
- The hosted commercial model is a monthly subscription per adult primary
  user, with a discounted annual option providing the same entitlements. It
  includes web access, future native mobile access, and one trusted-support
  companion seat.
- Optional advanced capabilities may later use transparent one-off purchases,
  but core functionality, accessibility, privacy, safety, export, deletion, and
  included companion access remain in the base subscription.
- Native mobile applications follow the Phase 3 hosted release.
- Local users have an optional one-time, resumable migration to the hosted
  account; the two installations do not remain synchronized.
- Google Calendar is the first calendar provider and allows explicitly
  confirmed event creation/editing; other providers follow later.
- Phase 2 trusted-person validation uses synthetic data and same-device role
  simulation. It creates no remote invitation or persistent assistance
  workspace.
- Supervised Phase 2 sessions may involve real participants under an approved
  protocol, but use synthetic scenarios and keep consented, de-identified
  research notes outside Timemanager.
- Real adult trusted-support relationships require a gated hosted pilot.
- Adult trusted helpers are proposal-only by default, with only explicit,
  narrow, time-limited delegation.
- The Phase 1 local pilot and Phase 3 hosted release do not solicit, infer,
  categorise, or
  provide specialist functionality for diagnosis, medication, treatment, or
  other health information. Generic Last Done activity tracking intentionally
  supports private user-authored medication labels and execution history, but
  provides no dose, adherence, treatment, or missed-dose advice.
- The detailed Last Done behavior, information model, task/calendar
  integration, privacy contract, and medication-safety gates are defined in
  [Repeatable activity and execution-history requirements](repeatable-activity-history-requirements.md).
- Notification importance and privacy are separate. Account-wide notification
  details are hidden by default and may be enabled for Standard cues; a cue
  marked Sensitive always uses a generic, detail-free notification until the
  user deliberately removes that classification.
- Timemanager does not promise privacy for notifications generated by an
  external calendar provider. Sensitive calendar writes require a disclosure
  preview and a privacy-safe external-title choice.
- Worldwide availability remains subject to applicable country/region privacy,
  security, consumer-protection, and health-data release review.
- AI decomposition, voice, AI body doubling, Day Context, Medication Context,
  and Quick Help are deferred to Phase 4. Day Context's factual-history,
  privacy, and interpretation gates are defined in
  [Day Context and within-day history requirements](day-context-history-requirements.md).
  Medication Context's record, identity, support-content, privacy, and
  clinical-safety gates are defined in
  [Private medication context and schedule support requirements](medication-context-support-requirements.md).
  Quick Help's separate clinical-safety, privacy, AI, and release gates are
  defined in
  [Future Quick Help, mood, energy, and focus support](quick-help-mood-energy-design.md).
- The Phase 1 local pilot is a development predecessor, not a supported
  self-hosted edition after the Phase 3 hosted release.

None of these choices changes the requirement that the daily loop remain usable
without AI.
