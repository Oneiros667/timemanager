# Day Context and within-day history requirements

Status: proposed Phase 4 product requirement; not implemented or clinically
validated

Updated: 2026-07-28

## Purpose

Timemanager should let a user build a low-friction, factual record of how their
day unfolded without having to reconstruct it from memory later.

The working name is **Day Context**. It combines:

- brief self-reported check-ins for mood, energy, ability to focus, and other
  user-selected state dimensions;
- timestamped activities such as food, caffeine, exercise, rest, and focus
  sessions;
- events such as distractions, interruptions, task switches, emotional
  disruptions, social interactions, and environmental changes; and
- explicit, editable user reflections about what may have helped, made
  something harder, or seemed unrelated.

The result is one inspectable timeline. It can help the user remember what was
happening around a difficult or productive period and prepare a factual summary
for their own reflection or a conversation with a professional.

Day Context records what the user logged. It does not prove that an unlogged
event did not happen, establish why a state changed, diagnose a condition,
measure treatment effectiveness, or replace clinical assessment.

The feature complements:

- [Last Done](repeatable-activity-history-requirements.md), which records
  explicit executions of repeatable activities;
- [Quick Help](quick-help-mood-energy-design.md), which helps choose one small
  action and reassess; and
- the existing Today, Low Capacity, task, and focus flows, which must remain
  useful without Day Context.

## Evidence and status boundary

Capturing a state or event close to when it occurs can create a different and
more inspectable record than asking someone to summarise the whole day from
memory. Research comparing momentary and retrospective affect reports shows
that the two can diverge, while also warning that momentary measurement has its
own validity, burden, and interpretation limits.

That supports testing low-friction near-time capture. It does not establish
that Timemanager's proposed vocabulary is accurate, that frequent tracking is
beneficial for a particular user, or that a sequence of logged events reveals
causation.

NICE guidance encourages people taking ADHD medication to monitor and record
adverse effects, but Timemanager is not a clinical adverse-effect checklist or
a substitute for follow-up with the responsible healthcare professional.

Mood, focus, energy, symptom, medication, eating, sleep, and inferred-pattern
records may reveal physical or mental health information. They are therefore
Sensitive product data by default. Exact legal classification and processing
authority remain jurisdiction-specific launch questions rather than claims
settled by this product note.

## Product decisions

1. Day Context is a user-owned external memory aid. It records the user's
   observations and confirmed events rather than monitoring the user.
2. A state check-in can record any subset of mood, energy, ability to focus,
   overload/capacity, and optional free text. No dimension is mandatory.
3. The user can log relevant activities and events with one short action and
   add detail only when useful.
4. The first capture defaults to **now**, but the user can backdate it. Every
   record distinguishes occurrence time from log time.
5. Absence of a record means **not logged**, not "did not happen".
6. The timeline may place records next to one another in time. Temporal
   proximity is not labelled as influence or causation automatically.
7. Only the user can assert that something may have helped, made the day
   harder, disrupted focus, or seemed unrelated. That attribution remains
   visibly a self-report and is editable.
8. Day Context may reference existing Last Done executions, focus outcomes,
   task completions, and confirmed calendar outcomes. It does not duplicate
   them or infer that a planned activity occurred.
9. Caffeine, food, exercise, sleep, medication, and symptom records never
   produce dose, intake-limit, interaction, dietary, treatment, or causal
   advice.
10. Day Context provides exact timelines, counts, and transparent
    co-occurrence summaries. It does not produce hidden scores, diagnoses,
    adherence measures, or treatment-effect estimates.
11. The complete manual flow works locally without AI, voice, sensors, a
    wearable, or an external network.
12. Passive mood recognition, health inference, automatic event detection,
    and continuous sensor ingestion are out of scope.
13. Day Context data is Sensitive by default and excluded from helpers,
    calendars, notification details, analytics content, and AI context unless
    a later, narrowly scoped disclosure is explicitly approved.
14. Tracking is optional. Gaps, pauses, disabled reminders, and deletion carry
    no penalty, broken streak, warning state, or loss of functionality.
15. Day Context is deferred Phase 4 work. This document does not authorise
    implementation in the local pilot or Phase 3 hosted release.

## Goals

The feature should:

- make a useful state or context event recordable in seconds;
- let the user capture information at the time instead of depending on
  end-of-day recall;
- preserve a chronological view of state, activities, disruptions, and
  environmental context;
- support correction, backdating, deletion, export, and source provenance;
- let users create a small set of favourite one-tap event types;
- connect an existing activity execution or focus outcome without creating a
  duplicate record;
- answer factual questions from the underlying records;
- let the user mark a possible influence without presenting it as established
  causation;
- reveal gaps and uncertainty rather than filling them with inference;
- remain calm and useful when the history is incomplete; and
- provide a privacy-safe bridge into Quick Help and user-authored personal
  playbooks.

## Non-goals

Day Context must not become:

- a medical diary prescribed or monitored by Timemanager;
- a diagnostic, symptom-severity, mood-disorder, or medication-response tool;
- a calorie, caffeine, hydration, sleep, exercise, or productivity target;
- automatic causal analysis such as "coffee improves your focus" or "this
  medicine caused your slump";
- passive surveillance through the microphone, camera, typing pattern,
  location, app usage, task completion, calendar, or wearable;
- a promise to detect deterioration, crisis, self-harm, mania, adverse
  reactions, or another urgent state;
- a continuous questionnaire that interrupts the user's day;
- a compliance score, streak, life score, or performance report;
- a helper, parent, employer, school, clinician, or insurer dashboard;
- automatic modification of Today, Low Capacity, focus duration, medication,
  meals, exercise, or calendar commitments; or
- a prerequisite for using Quick Help, tasks, timers, or Last Done.

## Domain terminology

| Term | Meaning |
| --- | --- |
| Day Context | The user-owned feature and combined within-day timeline |
| State check-in | A self-report of one or more current or backdated state dimensions |
| State dimension | A separately optional description such as mood, energy, focus ability, or overload/capacity |
| Context event | A user-confirmed activity, disruption, exposure, interaction, or environmental change |
| Source record | An existing Last Done execution, focus outcome, task completion, or confirmed calendar outcome referenced by the timeline |
| Occurrence time | When the user says the state or event occurred |
| Log time | When Timemanager received the record |
| Context attribution | The user's editable statement that an event may have helped, made something harder, had no noticeable effect, or remains unclear |
| Co-occurrence | Records present within a stated time window; not proof of influence or causation |
| Personal playbook | A short, user-approved set of actions the user may choose in a similar context |
| Sensitive | The privacy classification that prevents details leaving the authenticated application through default sharing or notifications |

## State check-ins

### Minimum capture

A state check-in requires at least one user-entered value but never requires
every dimension. The minimum flow is:

1. choose **Check in**;
2. select one state label or add a short note;
3. confirm the occurrence time, defaulting to now; and
4. save.

The primary flow does not ask for a cause, explanation, diagnosis, or
recommended action. Additional dimensions and context sit behind progressive
disclosure.

### Proposed state dimensions

The first usability prototype should test the following independent
dimensions:

| Dimension | Candidate labels | Meaning boundary |
| --- | --- | --- |
| Mood | User-chosen feeling words, with a small editable favourite set | A present self-description, not a diagnosis or global good/bad score |
| Energy | Very low; low; steady; high; wired/restless | Perceived energy, not productivity or physical fitness |
| Focus ability | Unavailable; difficult; variable; steady; strong | Perceived ability to direct/maintain attention, not measured performance |
| Overload/capacity | Plenty of room; manageable; near capacity; overloaded | Current perceived capacity, not a clinical stress scale |

These labels are product hypotheses, not an approved clinical instrument.
Participant testing must determine whether they are understandable, neutral,
and sufficiently distinct.

Rules:

- each dimension is optional;
- no numeric total or composite state score is calculated;
- a label is never preselected or inferred;
- **wired/restless** remains distinct from high usable capacity;
- mood words are user-owned and do not become diagnostic categories;
- the user can hide a dimension that is not useful;
- a check-in may be corrected or deleted; and
- a backdated check-in displays both occurrence and log time.

The curated reflection markers in the Last Done requirements describe how a
particular outcome felt or went. A Day Context state check-in describes the
user's state at a point in time. The two concepts may share readable language,
but they must not silently reuse a stored marker when the meanings differ.

## Context events

### Minimum capture

A context event requires only an event type and occurrence time. Optional
details include:

- a user label;
- start/end time or approximate duration;
- a short note;
- user tags;
- an existing source record;
- an optional amount and user-selected unit where relevant; and
- a later context attribution.

No amount, duration, note, or attribution is required to preserve the
one-action path.

### Initial event catalogue

The catalogue is a capture aid, not a clinical ontology. Users may hide
irrelevant categories and create neutral custom events.

| Category | Example events | Boundary |
| --- | --- | --- |
| Food and drink | Meal, snack, water, missed/late meal as explicitly reported | No calorie target, nutritional judgment, or inference from absence |
| Caffeine | Coffee, tea, energy drink, other user label | Optional amount/unit; no safe-limit, interaction, or dose advice |
| Movement | Exercise, walk, stretch, physical work | Optional duration; no fitness score |
| Rest and recovery | Sleep, nap, break, quiet time, daylight | A user record, not a measured sleep or recovery score |
| Focus and work | Focus session, deep-work period, meeting, task transition | May reference a confirmed focus/task outcome; no performance grade |
| Attention disruption | Distraction, interruption, unexpected context switch | User-recorded event, not passive app surveillance |
| Emotional or social context | Difficult interaction, supportive interaction, conflict, unexpected news, worry | Neutral user wording; no sentiment or relationship inference |
| Environment | Noise, crowding, lighting, temperature, location change, connectivity problem | User observation; no automatic sensor collection |
| Medication or symptom context | Link to a Sensitive generic Last Done execution or add a private note | No structured dose advice, adherence inference, or treatment analysis |
| Custom | Any user-owned label | Remains subject to the Sensitive and non-causal boundaries |

The first screen should show no more than the user's six favourite event types.
**More context** opens the grouped catalogue. This limit is a usability
hypothesis to validate, not a requirement to restrict what the user may log.

### Disruptions

A disruption may have:

- an occurrence time;
- an optional end time or approximate duration;
- one or more user-selected context labels, such as emotional, social,
  environmental, digital, or task-related;
- an optional note describing what happened; and
- an optional later attribution about focus, mood, energy, or capacity.

The product must not require the user to label a disruption as positive or
negative. An interruption may be necessary, welcome, neutral, or difficult.

## Context attributions

The user may explicitly connect a context event to a check-in or later state
using one of these candidate meanings:

- **May have helped**
- **May have made this harder**
- **No noticeable effect**
- **Not sure**

The exact labels require usability testing. Whatever wording is selected:

- it is stored as the user's attribution, not a Timemanager conclusion;
- the linked records and their times remain visible;
- the user can change or remove it;
- Timemanager does not create it from timing, a model, or a statistical
  association;
- one attribution does not become a general rule; and
- repeated attributions may be counted but are not called proof.

A user-authored free-text hypothesis such as "I think late lunch affects my
afternoon focus" may be saved separately from the underlying records. The
interface labels it **My hypothesis** and never silently turns it into a fact,
medical conclusion, notification rule, or recommendation.

## Relationship to existing records

### Last Done activities

An existing Last Done execution can appear in Day Context by reference. For
example, an explicit "Exercise" execution can appear on the timeline without
creating a second exercise event.

Requirements:

- the source execution remains authoritative;
- the timeline stores its source type and stable identifier;
- correcting the execution updates its rendered occurrence time;
- deleting the execution removes the timeline reference without deleting
  unrelated check-ins or attributions;
- an unperformed scheduled occurrence is not displayed as an activity that
  happened; and
- Day Context does not add an execution without the existing explicit
  confirmation.

### Focus, tasks, and calendar

- A confirmed focus-session outcome may appear by reference.
- A task completion may appear as work context only when the user enables that
  source or explicitly links it.
- A calendar commitment remains a plan, not proof of attendance or effect.
- After a calendar outcome is explicitly resolved, the confirmed outcome may
  appear with source provenance.
- Event titles, attendees, locations, and notes are not copied merely to make
  the timeline richer.
- Deleting or unlinking a source does not silently rewrite the user's separate
  state check-ins.

No source becomes Day Context or AI input merely because it exists elsewhere
in the account.

## Capture surfaces and reminders

### Capture surfaces

Day Context should be reachable from:

- Today;
- Low Capacity;
- the Focus completion surface;
- an activity execution acknowledgement;
- Quick Help; and
- the Day Context timeline itself.

The user can pin up to six favourite state/event actions. A capture should not
open a full form unless the user requests more detail.

### Optional reminders

The user may configure a small number of neutral check-in cues:

- at user-selected times;
- at the end of a focus session;
- after a user-confirmed activity; or
- as part of a user-authored personal playbook.

Defaults:

- reminders are off;
- no reminder is created from a detected pattern;
- notification text is generic because Day Context is Sensitive;
- dismissing or ignoring a cue records nothing;
- missed cues do not accumulate or become overdue; and
- the user can pause all cues immediately.

The feature must be useful without reminders. Prompt frequency and
interruption burden require usability evaluation before release.

## Timeline

### Day view

The timeline merges, in occurrence-time order:

- state check-ins;
- manually logged context events;
- referenced Last Done executions;
- enabled and confirmed focus/task outcomes;
- resolved calendar outcomes; and
- user-authored context attributions.

Each item shows:

- what the user recorded;
- occurrence time;
- log time when materially different;
- source and provenance;
- whether it was corrected or backdated;
- any user attribution; and
- controls to inspect, correct, unlink, or delete it as applicable.

Planned tasks and unresolved calendar/activity occurrences, if shown for
orientation, use a visually and semantically separate **planned** lane. They
must not appear as events that happened.

### Gaps and incomplete days

The timeline does not use empty periods as evidence. It may say:

> No Day Context records between 09:10 and 13:20.

It must not say:

> Nothing happened between 09:10 and 13:20.

The user can backfill an approximate event. Approximate and backdated records
remain visibly labelled and retain their later log time.

## Required answer contract

Every Day Context answer must:

- begin from the signed-in user's selected date and timezone;
- say that it is based on logged records;
- link to or reveal the supporting records;
- distinguish occurrence time from log time when material;
- distinguish a source event, state check-in, user attribution, and calculated
  co-occurrence;
- disclose the time window and filters used for a count or summary;
- treat missing records as unknown;
- use neutral language; and
- avoid causal, diagnostic, treatment, or moral conclusions.

### Representative answers

| Question | Required answer shape |
| --- | --- |
| What happened before my 13:20 slump? | "Based on your logs: breakfast and a medicine activity at 05:30, an interruption at 12:42, then low energy and difficult focus at 13:20. No lunch event is logged in between; that does not establish that you did not eat." |
| Did caffeine improve my focus? | "Timemanager cannot establish that. Here are the caffeine events and nearby focus check-ins you logged. You marked two as 'may have helped' and one as 'not sure'." |
| What disrupted me today? | "You logged three disruptions: a call at 10:05, noise from 11:20–11:45, and an unexpected task switch at 14:10. You linked the call and task switch to difficult focus." |
| Why was my energy low? | "The log cannot establish why. I can show the activities, events, and your own attributions around each low-energy check-in." |
| When was focus easiest this week? | "You recorded 'strong' focus four times. Here are those check-ins and the surrounding records. Days without a check-in are not included." |

If a record contains medicine or symptom context, the answer retains the
medicine-safety boundary from Last Done and Quick Help. It can report what was
logged; it cannot recommend a dose or interpret an adverse effect.

## Descriptive patterns

Pattern summaries are a later slice after the manual timeline is validated.
They may provide:

- exact counts of selected state labels;
- time-of-day distributions;
- user-attribution counts;
- transparent before/after windows around a user-selected event type;
- lists of events commonly co-logged near a selected state; and
- comparisons of recorded periods chosen by the user.

Requirements:

- every summary exposes the underlying records;
- the user chooses or can inspect the date range, timezone, filters, and time
  window;
- logging frequency and missing periods are shown alongside the result;
- small or sparse samples show raw records rather than a confident insight;
- corrected/deleted records update the summary;
- the wording uses **co-logged**, **near**, **before**, **after**, or
  **you marked**, not **caused**, **triggered**, **fixed**, or **works**;
- there is no opaque model-generated score;
- the result never changes the user's plan automatically; and
- AI is not required to calculate or explain the summary.

The user may turn a descriptive pattern into **My hypothesis** or draft a
personal playbook, but both require confirmation and remain editable.

## Quick Help integration

Quick Help may:

- offer to record the current state before suggesting an action;
- show the user-selected recent Day Context records relevant to the current
  question;
- add a context event or reassessment only after explicit confirmation;
- open the timeline at the current time; and
- draft a personal playbook from the user's stated preference.

Quick Help must not:

- require a saved check-in before helping;
- save the prompt or response automatically;
- send Day Context history to an AI provider by default;
- choose an alleged cause from the timeline;
- silently label an event as helpful or harmful; or
- treat a missing record as a completed or missed activity.

If the user explicitly includes Day Context records in an AI request, the
preview identifies every record and field that will leave the application.
Selecting one day's context does not grant ongoing access to history.

## Privacy and security

### Sensitive by default

All Day Context state check-ins, context events, attributions, hypotheses,
personal playbooks, and derived summaries are Sensitive in the first
implementation. A seemingly ordinary meal, coffee, exercise, meeting, or
location-change record can reveal health or behavioral patterns when placed
beside mood and focus.

Sensitive records:

- are scoped to the signed-in user;
- never appear in notification or push-payload details;
- are excluded from assistance workspaces and general planning permissions;
- are excluded from calendar writes and analytics content;
- are not sent to an AI provider without a per-request disclosure preview;
- are not used for advertising, eligibility, pricing, employment, education,
  insurance, or profiling;
- remain protected in export, backup, sync, and deletion workflows; and
- are not exposed through operational logs.

Every state-changing browser request retains CSRF protection. Hosted APIs also
require tenant isolation, authorization checks, rate limits, auditability, and
a reviewed lawful-processing basis before release.

### Export, correction, and deletion

The user can:

- correct occurrence time, state labels, event type, notes, attribution, and
  source link;
- see correction provenance without being shamed for backfilling;
- export the complete Day Context schema with stable identifiers, timezone,
  revisions, source provenance, and deletions as defined by the transfer
  contract;
- delete an individual record, a selected date range, or all Day Context data;
  and
- disable Day Context without losing access to the rest of Timemanager.

Hosted retention, backup expiry, deletion completion, and any de-identified
aggregate use must be disclosed and approved before implementation.

## Safety and burden controls

- Logging food does not count calories or judge food quality by default.
- Logging caffeine does not calculate a safe amount or advise taking more or
  less.
- Logging medicine does not verify ingestion, calculate adherence, or advise
  another dose.
- Logging exercise does not set a fitness target or treat more activity as
  inherently better.
- Mood and focus labels do not trigger a diagnosis or automatic crisis score.
- Day Context does not promise to monitor safety. Urgent support remains a
  deliberate, reviewed Quick Help route rather than passive analysis of a
  diary.
- Users can hide food, caffeine, medicine, weight-related, or other categories
  that feel unhelpful or unsafe.
- The UI never rewards logging volume or penalises gaps.
- Summaries avoid blame-oriented wording such as "failed", "bad day",
  "unproductive", or "non-compliant".
- The user can pause reminders and pattern summaries separately.
- Tracking burden, compulsive use, rumination, reactivity, and choice overload
  are explicit usability and safety evaluation outcomes.

Adding clinician monitoring, treatment-response analysis, structured
medication dose fields, nutrition targets, passive sensing, predictive risk,
or automated crisis detection requires a separate product decision plus
clinical-safety, medical-device/regulatory, privacy, security, and
jurisdiction review.

## Offline, time, and resilience

- Manual capture and the current-day timeline work locally without an external
  provider.
- A confirmed record survives restart.
- A failed save is shown as failed; it never appears as committed.
- Retried submissions are idempotent.
- Future offline queues display unsynchronised state and reconcile without
  duplicates.
- Records retain occurrence timezone and log timezone where needed.
- Daylight-saving and travel behavior follows the Last Done time contract.
- Approximate times remain approximate rather than acquiring false precision.
- A failed source link leaves the user's independent state record intact and
  reports the broken relationship for correction.

## Accessibility and interaction

- Every capture and timeline action is keyboard and screen-reader operable.
- Labels use text; emoji and colour are supplementary.
- A minimum check-in requires one selection and one confirmation.
- Favourite actions reduce choice without hiding the full catalogue.
- State dimensions and event categories can be reordered or hidden.
- The timeline distinguishes state, event, plan, source, and attribution
  without relying on colour alone.
- Approximate, backdated, corrected, and unsynchronised states have readable
  labels.
- Capture remains possible without voice, animation, sound, AI, or a network.

## Acceptance criteria

### Capture and history

- A user can save an energy-only, mood-only, or focus-only check-in.
- A user can capture food, caffeine, exercise, distraction, interruption,
  emotional context, and environmental context with only a type and time.
- The user can backdate a check-in or event and see occurrence versus log time.
- The primary surface shows no more than six favourite event actions.
- An existing Last Done execution appears by reference without duplication.
- A planned or unresolved activity/calendar event never appears as performed.
- Corrections, unlinking, and deletion update the timeline predictably.
- Gaps are displayed as no records, not as no events.

### Meaning and retrieval

- Every factual answer links to supporting records.
- Missing records remain unknown.
- User attributions are visibly self-reported and editable.
- Temporal proximity never creates an attribution automatically.
- "What happened before?" returns a timeline, not a causal answer.
- Co-occurrence summaries disclose their range, filters, window, record count,
  and missingness.
- Sparse data never produces a confident personalised insight.

### Privacy and safety

- New Day Context records are Sensitive.
- Cross-user reads and mutations fail without revealing object existence.
- Notification and push fixtures contain no Day Context detail.
- Helpers, calendars, analytics content, and unrelated AI contexts receive no
  Day Context data.
- An AI disclosure preview lists the exact selected records and fields.
- Food, caffeine, exercise, medication, and mood records produce no dose,
  limit, treatment, diagnostic, or adherence advice.
- The user can export, correct, delete, and disable the feature.

### Resilience and accessibility

- Manual capture and history work when external providers are unavailable.
- Failed and retried saves cannot create false acknowledgements or duplicates.
- Timezone, daylight-saving, backdated, and approximate-time fixtures pass.
- Every capture and history action is keyboard and screen-reader operable.

## Delivery order

1. Validate the state vocabulary, event catalogue, one-action capture, and
   timeline with synthetic data.
2. Define stable identifiers, occurrence/log time, source provenance,
   correction, deletion, and export contracts.
3. Implement manual local state check-ins and context events without patterns,
   reminders, AI, or source integration.
4. Add the combined timeline and exact-answer contract.
5. Add explicit reference links to Last Done and confirmed focus outcomes.
6. Validate privacy, account isolation, accessibility, timezone, offline, and
   tracking-burden gates.
7. Add user-configured reminders only after interruption burden is acceptable.
8. Add transparent descriptive summaries and user-authored hypotheses only
   after sufficient usability and interpretation testing.
9. Integrate optional Quick Help context selection and personal playbooks.
10. Consider AI phrasing only after per-request Sensitive-data preview and the
    non-AI flow pass their gates.

Calendar outcomes, hosted sync, helper/clinician sharing, passive sensing,
health inference, and treatment-response analysis are later separate gates,
not prerequisites for a useful manual Day Context record.

## Evaluation

Evaluate:

- time and interactions required for a minimal check-in or event;
- whether capture close to an event is practical during real days;
- whether six favourite actions reduce or increase choice burden;
- correction and backfill rates;
- whether the timeline helps users reconstruct their day;
- comprehension of occurrence time, log time, missingness, attribution, and
  co-occurrence;
- whether users mistake timelines or summaries for causal or medical advice;
- reminder opt-out, pause, and annoyance rates;
- tracking burden, rumination, compulsive logging, and reactivity;
- whether users feel observed or judged;
- privacy comprehension before export or AI transfer; and
- whether users can stop tracking without losing trust in the rest of the
  product.

Do not use number of check-ins, completeness, streak length, disclosure volume,
task output, medicine adherence, or time spent in the feature as success
metrics.

## Sources and review boundary

Sources checked on 2026-07-28:

- Leertouwer, Schuurman, and Vermunt,
  [Are Retrospective Assessments Means of People's Experiences?](https://pmc.ncbi.nlm.nih.gov/articles/PMC9773960/),
  a repeated-person reanalysis comparing momentary and retrospective affect
  reports;
- [NICE NG87: ADHD diagnosis and management recommendations](https://www.nice.org.uk/guidance/ng87/chapter/recommendations),
  especially recommendations 1.8.1–1.8.4 on monitoring and recording
  medication effects; and
- [ICO: what is special-category data?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/),
  including its health-data and inferred-data guidance.

These sources support capture-close-to-experience as a design direction worth
testing, careful interpretation of self-report records, and a strong
sensitive-data boundary. They do not validate Timemanager's proposed labels,
prove that tracking improves functioning or health, establish causal effects
between events and states, or settle legal applicability in a release
jurisdiction.
