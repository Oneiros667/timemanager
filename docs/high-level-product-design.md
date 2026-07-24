# Timemanager high-level product design

Status: proposed product direction

Updated: 2026-07-24

## Implementation status

The first basic local PWA now implements registration/login, local SQLite task
persistence, Today and Inbox capture, one daily highlight, completion/restoring,
deliberate dropping, a Low Capacity view, and a client-side focus timer.

Google Calendar, trusted-person support sessions, the hosted online PWA,
one-time local-data migration, AI, and native mobile applications remain
unimplemented. The phases below describe intended scope, not shipped behavior.

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

## Confirmed direction and working assumptions

The delivery direction is:

1. build and validate the first working version as a single-user application in
   a local home-lab environment;
2. use a responsive web/PWA interface from the beginning;
3. release the product as a hosted online PWA with user accounts;
4. add native mobile application clients after the online PWA;
5. let a local user optionally perform a one-time migration of selected
   Timemanager data into an online account;
6. integrate Google Calendar first, with explicitly confirmed event creation
   and editing, and add other calendar providers later;
7. include narrowly scoped trusted-person sharing/body doubling in the first
   pilot;
8. exclude AI decomposition, voice, and AI body doubling from the first pilot.

The local working version is a development/pilot stage, not a supported
self-hosted edition or a permanent promise that the released product will be
local-first or fully offline. The core product remains designed so that AI is
never required.

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
- invite a trusted person into a deliberately limited support session without
  exposing the whole plan;
- trust that the system reflects current commitments.

Primary success is improved functioning and reduced planning burden. Task count,
hours logged, streak length, and app-open frequency are not primary outcomes.

## Product principles

1. **Capture first, classify later.** Only a title is required to save.
2. **One home, several views.** Inbox, Today, Low Capacity, and Review are views
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
- safety-, health-, and consequence-critical items;
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

The first release has four primary destinations:

| Area | Purpose |
|---|---|
| Today | Orient, choose, launch, transition, and recover |
| Inbox | Clarify captured items in a short, bounded queue |
| Review | Revisit deferred work and run the weekly learning loop |
| Settings | Calendar, cues, accessibility, privacy, data, and optional integrations |

Task detail and Focus are contextual views reached from Today, Inbox, or Review.
Projects are initially lightweight outcome groupings inside task detail, not a
separate dashboard. Search is a utility, not a fifth place the user must check.

## Feature catalogue and phasing

| Capability | First validation | Later extension | Confidence |
|---|---|---|---|
| Universal text capture and inbox | Yes | Voice, widget, watch, share-sheet | Supported foundation |
| Today timeline with fixed commitments | Yes | Multi-calendar reconciliation | Supported foundation |
| Highlight plus small active plan | Yes | Learned capacity limit | Supported method; plausible interface |
| Manual next action and definition of done | Yes | Suggested decomposition | Supported foundation |
| Flexible focus session | Yes | Stronger blocking and AI body doubling | Supported elements; experiential options |
| Trusted-person support session | First pilot | Additional sharing controls | Experiential/early research |
| Transition and leave-by cues | Yes | Location/event-triggered cues | Plausible interface |
| Recovery/reset without rollover | Yes | Personalised recovery suggestions | Plausible product design |
| Estimate versus actual | Basic and optional | Reference-class duration ranges | Supported mechanism; plausible algorithm |
| Weekly review and one experiment | Yes | Longer-term pattern comparison | Supported components |
| Low-capacity mode | Yes | User-defined low-capacity layouts | Plausible product design |
| Google Calendar integration | Read plus confirmed create/edit | Other providers | Supported need; integration behavior to test |
| AI voice/body doubling | No | Opt-in connector | Experiential/early research |
| Goals, habits, journaling, social features | No | Only after core validation | Unproven for the core job |

## Core information model

### Entities

- **Capture item:** original input, source, timestamp, and clarification state.
- **Task:** title, next action, definition of done, state, consequence, true
  deadline, estimate range, context, capacity fit, value link, and provenance.
- **Project/outcome:** optional grouping with a desired outcome and next task.
- **Commitment:** fixed time interval, source calendar, preparation/leave-by
  boundaries, and sync provenance.
- **Daily plan:** date, highlight, selected actions, capacity mode, and explicit
  user choices. It references tasks rather than copying them.
- **Focus session:** intention, planned range, elapsed/focused time, pauses,
  outcome, and optional interruption labels.
- **Cue:** trigger, importance, channel, status, snooze choices, and linked
  intention.
- **Review decision:** keep, schedule, renegotiate, delegate, replace, or drop,
  with an optional reason.
- **Experiment:** one temporary behavior change and a review date.
- **Support session:** explicit invitation, shared intention, presence/check-in
  state, expiry, revocation, and the minimum task/session fields disclosed.
- **Installation/account provenance:** stable object identifiers, source
  installation/account, revision, and migration/import state used when local
  data is moved online.

### Task states

```text
Inbox -> Ready -> Active -> Done
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
- Trusted-person access is session-scoped, expires, and reveals no calendar or
  backlog data unless the user separately confirms it.
- Recommendations expose the facts used and label inferred values.
- AI-generated content is marked as suggested until accepted.
- Missing duration or completion data remains unknown, not zero or failure.
- Notification delivery and intention resolution are separate states.
- Time calculations preserve timezone and daylight-saving semantics.
- The active day remains readable during temporary network or provider failure.
- Local and hosted records use stable identifiers and schema versions so a
  migration can be retried safely.
- Users can export and delete their data; optional AI memories and transcripts
  have separate controls.

## Notifications and attention budget

Notifications are allocated by consequence rather than independently requested
by every feature.

- **Protected:** selected appointments, medication/health reminders, travel, or
  real deadlines; may use staged interruptive cues.
- **Actionable:** starts, transitions, and review prompts; grouped and limited.
- **Ambient:** inbox counts, suggestions, and weekly patterns; visible in-app,
  not interruptive by default.

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

Other calendar providers should implement the same internal commitment boundary
after the Google integration is stable; provider-specific objects must not leak
into the core task model.

### Trusted-person support

The first pilot includes human support without becoming a household or team
planner.

Minimum behavior:

- the user explicitly starts a support session and chooses what to share;
- the default disclosure is the session intention, agreed duration, and
  start/end status—not the user's backlog, calendar, notes, or history;
- the trusted person can acknowledge presence and participate in agreed start
  and end check-ins;
- either participant can leave, and the user can revoke access immediately;
- invitations expire and cannot silently become permanent account access;
- the user can see when the trusted person joined and what was disclosed;
- task edits, completion, rescheduling, and broader sharing remain user actions.

The local pilot may expose this only within the operator's chosen home-lab
network or secure remote-access setup. The hosted PWA release must use
authenticated, expiring invitations and enforce the disclosure boundary on the
server.

### Local-to-online data transfer

The local development/pilot version and hosted service should share versioned
domain schemas and stable object identifiers from the start. When the hosted
PWA is available, a pilot user may explicitly connect or sign in to an online
account and preview the data to transfer.

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
- the local development/pilot application receives no supported self-hosted
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
8. complete a session with all nonessential notifications disabled.

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
- trust that current commitments are represented.

Measure abandonment and return after the novelty period. Qualitative reports of
pressure, shame, surveillance, sensory load, or unwanted data use are guardrail
signals, not acceptable costs of higher task completion.

## Delivery sequence

### Phase 0: validate the loop

- clickable prototypes for Capture, Today, Launch, Focus, Transition, and Reset;
- interviews and moment-by-moment walkthroughs of difficult days;
- explicit testing with both minimalist and feature-rich-tool users;
- no broad app implementation before the recovery and transition flows are
  understandable.

### Phase 1: local working version

- single local user;
- responsive web/PWA client backed by the home-lab service;
- text capture and inbox;
- manually entered commitments;
- Today, highlight, and small active plan;
- task next action and definition of done;
- local focus session and transition protection;
- Low Capacity and Reset;
- basic optional estimate-versus-actual recording;
- local backup/export;
- stable object identifiers and versioned schemas suitable for later transfer;
- no AI features.

### Phase 2: local pilot

- authenticated Google Calendar read plus confirmed event creation/editing;
- fixed-event sync, provenance, caching, and conflict visibility;
- session-scoped trusted-person presence and start/end check-ins;
- notification budget and staged leave-by cues;
- short weekly review and one experiment;
- diary study and post-novelty retention evaluation;
- transfer rehearsal using export/import fixtures without uploading pilot data
  to a production service.

### Phase 3: hosted online PWA release

- authenticated hosted accounts and tenant isolation;
- production Google authorization, event reads, and explicitly confirmed event
  creation/editing;
- authenticated, expiring trusted-person invitations;
- optional, user-previewed one-time migration from the local version;
- backup, export, deletion, rate limiting, and operational recovery;
- online PWA deployment with clear connectivity state;
- no dependency on AI.

### Phase 4: mobile and later extensions

- native mobile applications using the hosted backend;
- push notifications and mobile capture surfaces;
- an explicit mobile offline/synchronization contract;
- additional calendar providers;
- stronger temporary focus controls;
- user-confirmed decomposition suggestions and opt-in AI body-doubling features
  only after separate validation.

## Explicitly out of the first release

- a general notes or knowledge-management system;
- complex project portfolios or goal trees;
- habit streaks and life-score dashboards;
- automatic calendar rescheduling;
- opaque AI prioritisation or silent task mutation;
- public social feeds, leaderboards, or default sharing;
- employer, school, clinician, or caregiver surveillance;
- clinical diagnosis, treatment recommendations, or symptom-efficacy claims.

## Resolved product decisions

- The first working version runs locally in a home-lab environment.
- The actual release is a hosted online PWA.
- Native mobile applications follow the online PWA.
- Local users have an optional one-time, resumable migration to the hosted
  account; the two installations do not remain synchronized.
- Google Calendar is the first calendar provider and allows explicitly
  confirmed event creation/editing; other providers follow later.
- Trusted-person sharing/body doubling is included in the first pilot.
- AI decomposition, voice, and AI body doubling are not in the first pilot.
- The local version is a development/pilot predecessor, not a supported
  self-hosted edition after the hosted release.

None of these choices changes the requirement that the daily loop remain usable
without AI.
