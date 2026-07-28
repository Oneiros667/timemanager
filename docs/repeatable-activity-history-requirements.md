# Repeatable activity and execution-history requirements

Status: proposed product requirement

Updated: 2026-07-28

## Purpose

Timemanager must let a user define an activity that may happen repeatedly,
record each time it happens, and retrieve exact, low-friction answers from that
history.

Representative questions include:

- "Did I have my meds today?"
- "Did I have my 7am meds today?"
- "When did I last exercise?"
- "When did I last buy groceries?"

The feature's working user-facing name is **Last Done**. The underlying domain
objects are a **tracked activity**, an optional **scheduled occurrence**, and an
explicitly recorded **execution**.

This is a record of what the user logged, not proof of what happened and not a
medical-adherence system. Medication is an intentional private use case, which
means some activity titles, schedules, notes, reflection markers, user tags,
and histories are health data. The privacy, safety, and release gates in this
document are therefore requirements rather than optional hardening.

## Product decisions

1. A repeatable activity is not an ordinary to-do. The activity describes a
   kind of action; an execution records that the user says it happened.
2. A scheduled occurrence describes an expectation. It never proves execution.
3. Every positive answer must trace to one or more explicit execution records.
4. Absence of a log is **unknown**, not evidence that the user did not perform
   the activity.
5. Medication may be represented using user-authored generic activity records,
   but Timemanager does not provide dose, interaction, treatment, adherence, or
   missed-dose advice.
6. New tracked activities are Sensitive by default. The user may deliberately
   change a non-sensitive activity to Standard.
7. Notes, reflection markers, and user tags are optional. Logging the current
   time remains a one-action path.
8. Task completion and calendar attendance never create an execution silently.
   Every cross-object mutation requires an explicit user confirmation.
9. The useful core must not depend on AI or natural-language interpretation.
10. Personal execution history is not shared with assistance workspaces in the
    first implementation.

## Goals

The feature must:

- make a new repeatable activity quick to create;
- make "log now" available in one action from the relevant daily view;
- support on-demand, day-scoped, and time-specific activities;
- distinguish when an activity occurred from when it was logged;
- support backdated logging and correction;
- provide optional short notes, shared reflection markers, and user-defined
  tags;
- answer "logged today," "last logged," and named-occurrence questions exactly;
- make ambiguous, missing, duplicate, and corrected data visible;
- remain useful offline within the local application's existing constraints;
- preserve user isolation, privacy classifications, exportability, and
  deletion.

## Non-goals for the first implementation

The first implementation does not include:

- medical instructions, dose calculation, refill advice, drug-interaction
  checks, adherence scoring, or recommendations after a missed or uncertain
  dose;
- automatic claims that an activity did or did not happen;
- automatic execution inferred from time, location, calendar presence, device
  sensors, purchases, or task completion;
- streaks, compliance scores, shame-oriented overdue states, or rewards based
  on health behavior;
- shared household or assistance-workspace histories;
- AI-generated health interpretation or automatic sensitive-data
  classification;
- arbitrary iCalendar recurrence rules;
- permanent generation of distant future occurrence rows;
- automatic external-calendar writes.

## Domain terminology

| Term | Meaning |
| --- | --- |
| Tracked activity | A user-owned definition such as "Morning medication," "Exercise," or "Buy groceries" |
| Schedule slot | A named recurring expectation, such as "07:00" or "Evening" |
| Scheduled occurrence | One date-specific instance of a schedule slot |
| Execution | A user-confirmed record that the activity happened |
| Occurrence resolution | The current status of an expected occurrence: unresolved, performed, skipped, or unsure |
| Log time | When Timemanager received the record |
| Occurrence time | When the user says the activity happened |
| Source | The user action or object from which an execution was created |
| Reflection marker | A short, system-defined annotation about how an event felt or went, with the same meaning across supported event types |
| User tag | A user-owned label for organising or retrieving records |
| Sensitive | A privacy classification that prevents details leaving the authenticated application through notifications or default sharing |

## Required answer contract

### General rules

Every answer must:

- use the user's current date and timezone context unless a different date or
  timezone is explicitly selected;
- state that it is based on logged history;
- link to or reveal the supporting execution records;
- distinguish occurrence time from log time when they differ materially;
- report multiple executions rather than silently choosing one;
- use neutral language;
- never convert missing information into a negative fact.

### Required examples

| Question | Required answer when found | Required answer when absent |
| --- | --- | --- |
| Did I have my meds today? | "Logged today at 07:08." If there are several, list or count them. | "No execution has been logged today." |
| Did I have my 7am meds today? | "The 07:00 occurrence was logged as performed at 07:08." | "No execution is linked to today's 07:00 occurrence." |
| When did I last exercise? | "Last logged Tuesday at 18:20, three days ago." | "No execution history yet." |
| When did I last buy groceries? | "Last logged 12 July at 10:35." | "No execution history yet." |

When no execution is found for a medication-related activity, the interface must
also state:

> A missing log does not establish whether you took it. Timemanager cannot tell
> you whether to take another dose; follow your medication instructions or ask
> an appropriate healthcare professional if you are unsure.

Timemanager must not generate medicine-specific instructions.

### Time-specific matching

A question about the "07:00" activity refers to the identity of the schedule
slot, not merely an execution timestamp close to 07:00.

- An execution explicitly linked to the 07:00 occurrence satisfies the query
  even if the user records that it happened at 07:20.
- An unlinked execution at 07:05 does not silently resolve the 07:00
  occurrence.
- If exactly one unresolved occurrence is a plausible match, Timemanager may
  preselect it during logging but must show the selection before saving.
- If more than one occurrence is plausible, the user must choose the occurrence
  or choose "Unscheduled execution."

## Functional requirements

### Create a tracked activity

The minimum creation flow requires only a title. It must then offer optional,
progressively disclosed choices:

- occurrence pattern;
- days of the week;
- one or more schedule slots;
- timezone;
- Sensitive or Standard privacy;
- default user tags;
- whether it may appear in Today.

Defaults:

- privacy is Sensitive;
- recurrence is on demand;
- timezone is the account's current timezone;
- no notification is created automatically;
- no task, calendar event, helper share, or AI context is created.

The title follows the application's existing short-title limit. Schedule-slot
labels may be generated from their time or named by the user.

### Supported recurrence

The first implementation must support:

| Pattern | Example | Occurrence behavior |
| --- | --- | --- |
| On demand | Buy groceries | No expected occurrence; executions only |
| Once per day | Exercise | One date-scoped expectation without a required clock time |
| Selected weekdays | Put bins out on Thursday | One expectation on selected local weekdays |
| One time per selected day | Morning medication at 07:00 | One named time-specific occurrence |
| Multiple times per selected day | Medication at 07:00 and 13:00 | Independent named occurrences |

A simple every-N-days interval may be added after the above behavior is
validated. Full recurrence-rule compatibility is deferred until calendar
integration requires it.

### Occurrence materialisation

The system must not generate unlimited future database rows. It may:

- derive occurrences during reads;
- materialise only a bounded operational window; or
- create an occurrence when it first becomes visible, resolved, or linked.

Whichever strategy is implemented must provide stable occurrence identifiers
for retries, linking, synchronization, and idempotent import.

Changing a schedule must not rewrite historical occurrence or execution times.
The user must see whether a pending occurrence follows the old or new schedule.

### Log an execution

The primary action is **Log now**.

On activation, Timemanager must:

1. identify the activity and current user;
2. show any preselected scheduled occurrence;
3. record the current occurrence time and timezone;
4. record a separate server log timestamp;
5. save through a CSRF-protected, user-scoped mutation;
6. acknowledge the execution and offer immediate Undo;
7. offer optional details without blocking the fast path.

Optional details:

- change the occurrence date/time;
- attach or change the scheduled occurrence;
- add a note of at most 500 characters;
- add zero or more reflection markers;
- add zero or more user-owned tags;
- link the execution to an eligible task or commitment.

### Duplicate protection

Before adding an execution to an occurrence already marked performed, the
interface must show the existing execution time and require confirmation:

> The 07:00 occurrence was already logged at 07:08. Log another execution
> anyway?

The user may still confirm another execution. Duplicate protection is a warning,
not an irreversible block.

For an on-demand activity, an implementation may warn about a very recent
execution but must not assume it is a duplicate.

### Backdate, correct, undo, and delete

The user must be able to:

- backdate an execution;
- correct its occurrence time, occurrence link, note, reflection markers, and
  user tags;
- undo a newly created execution;
- delete a personal execution;
- see when a record was corrected if that affects interpretation.

Correction must never change the server's original log timestamp. A corrected
record retains revision metadata sufficient for sync conflict handling.

Deleting an execution linked to a performed occurrence returns that occurrence
to unresolved unless the user explicitly chooses another resolution. Deleting
an activity requires a preview of the affected history and offers archive as
the safer default. Data-deletion rights must still allow permanent deletion.

### Notes, reflection markers, and user tags

These are three different annotation mechanisms:

- a note is optional private free text;
- a reflection marker is selected from a small, shared vocabulary describing
  the user's experience of an event; and
- a user tag is a user-owned label used to organise or retrieve records.

All three are optional and treated as potentially sensitive. Each annotation
defaults to Sensitive even when its target is Standard; a less restrictive
target classification never relaxes the annotation. The primary logging or
completion action remains available without opening annotation controls.

#### Curated reflection markers

The first implementation uses the following stable catalogue. The stored value
is the marker key, not the emoji or display text.

| Dimension | Stable key | Display |
| --- | --- | --- |
| Overall | `went_well` | 🌟 Went well |
| Effort | `easier_than_expected` | 🪶 Easier than expected |
| Effort | `harder_than_expected` | 🧗 Harder than expected |
| Timing | `early` | ⏩ Early |
| Timing | `on_time` | 🎯 On time |
| Timing | `late` | 🕒 Late |
| Friction | `unexpected_problem` | 🧩 Unexpected problem |
| Friction | `needs_preparation` | 🧰 More preparation next time |
| Friction | `flow_disrupted` | 🌊 Broke my flow |
| Energy | `good_energy` | ⚡ Good energy |
| Energy | `low_energy` | 🪫 Low energy |
| Future preference | `do_more` | ➕ Do more |
| Future preference | `do_less` | ➖ Do less |

This is one cross-product vocabulary, not a separate catalogue for each
feature. The same stable key and meaning apply wherever a marker is supported,
including activity executions, task completions, focus-session outcomes, and
calendar or occurrence resolutions. A feature may limit the catalogue by
applicability, but it must not redefine a marker.

The dimensions are compact alternatives, not a questionnaire:

- effort, timing, energy, and future-preference selections are mutually
  exclusive within their dimension for one event;
- timing markers are offered only when the event has a visible expected time,
  schedule window, or deadline;
- no marker is preselected or automatically inferred, including timing markers
  that appear mechanically calculable;
- the quick annotation surface shows no more than four context-relevant
  choices;
- **More reflections** opens the grouped catalogue instead of placing all
  choices in the primary flow;
- a user may select at most three markers for one event in the first
  implementation;
- markers can be added, changed, or removed later; and
- history summarizes markers compactly and reveals the full labels on demand.

Initial quick choices are deterministic:

| Outcome context | Quick choices |
| --- | --- |
| General activity or task completion | 🌟 Went well; 🪶 Easier than expected; 🧗 Harder than expected; 🧩 Unexpected problem |
| Event with an expected time or deadline | ⏩ Early; 🎯 On time; 🕒 Late; 🌟 Went well |
| Focus-session outcome | 🌟 Went well; 🌊 Broke my flow; ⚡ Good energy; 🪫 Low energy |

The complete catalogue remains available for every supported outcome type
through **More reflections**; context changes only the initial four choices.
The product may tune these quick sets after usability evaluation, but the
selection must remain predictable and must not be personalized through hidden
health, mood, or performance inference.

Emoji supplement the text; they never replace it. Every control and stored
selection has a readable label, and meaning must not depend on emoji rendering
or color. Localization may change the label but not the stable key or meaning.

If one confirmation both completes a task and logs an activity execution, the
interface asks for one reflection selection and associates it with the shared
user-confirmed outcome. It must not prompt twice or create contradictory copies
without making that distinction visible.

Reflection markers must not:

- produce a score, grade, streak, diagnosis, health inference, or automatic
  priority;
- be shared with a helper, AI provider, analytics-content system, or external
  calendar by default;
- become less private because the task, occurrence, or activity is Standard; or
- turn `late`, `low_energy`, or another marker into blame-oriented language.

#### User tags

- User tags remain free-form, user-owned labels rather than global clinical or
  experiential categories.
- Tag comparison is case-insensitive while preserving the user's display case.
- Tags must not cause automated diagnosis, health inference, prioritisation, or
  disclosure.
- A user may use tags for retrieval without adopting reflection markers, and
  vice versa.

### History

The activity detail view must show:

- whether the activity was logged today;
- last occurrence time and relative age;
- the next or current expected occurrence, if applicable;
- reverse-chronological execution history;
- occurrence status and source provenance;
- correction state;
- notes, reflection markers, and user tags behind progressive disclosure;
- controls to filter by date, reflection marker, or user tag;
- controls to correct, delete, or undo an execution.

Archived activities remain searchable and retain their history until the user
deletes it.

### Query and retrieval

The first implementation does not require free-form natural language. It must
expose deterministic actions that answer:

- Logged today?
- When last?
- What happened on a selected date?
- Was a selected schedule slot performed?

If natural-language query is added later:

- parsing and activity matching must be deterministic where possible;
- ambiguous activity names or schedule slots require clarification;
- the answer contract in this document remains unchanged;
- AI is not required;
- the query must not send Sensitive activity text to an external provider by
  default.

## Information requirements

The logical data model must represent the following. Exact table names are an
implementation decision.

### Tracked activity

- stable public identifier and local database identifier;
- owner user identifier;
- title and optional aliases;
- active/archived state;
- privacy classification;
- whether it may appear in Today;
- created, updated, and archived timestamps;
- source installation/account and revision.

### Schedule

- stable identifier and activity identifier;
- pattern type;
- selected weekdays;
- schedule-slot label and local time, if present;
- IANA timezone identifier;
- effective-from and optional effective-until boundary;
- revision and active state.

Multiple time-specific slots may belong to one activity.

### Occurrence

- stable identifier;
- activity and schedule-slot identifiers;
- expected local date/time and timezone;
- optional window start/end;
- resolution state;
- resolved timestamp and responsible user action;
- linked execution, if performed;
- revision.

### Execution

- stable identifier;
- activity identifier and owner user identifier;
- optional occurrence identifier;
- occurrence timestamp in UTC;
- occurrence timezone identifier and offset as recorded;
- server log timestamp;
- source type and optional source-object identifier;
- optional note;
- correction/revision metadata;
- deletion state where needed for synchronization.

### Reflection-marker catalogue and selections

Catalogue definitions require:

- stable marker key;
- dimension;
- localized text label and supplemental symbol;
- display order;
- applicability flags for supported outcome-event types;
- active state and catalogue version.

Each selection requires:

- owner user identifier;
- marker key;
- target outcome-event identifier, or an equivalent target type and identifier;
- created and updated timestamps; and
- revision/deletion state where needed for synchronization.

An outcome event may be an activity execution, task completion, focus-session
outcome, or another explicit user-confirmed result. Exact table names and
whether this is represented as a common event table are implementation
decisions. A selection is Sensitive by default and may inherit a stricter
future target classification; it can never weaken the target or become less
private merely because the target is Standard.

### User tags

- stable user-owned tag identifier;
- normalized comparison key and display label;
- many-to-many execution/tag relationship.

No structured medication-name, strength, dose, diagnosis, prescriber,
interaction, refill, or treatment-purpose field is part of the generic model.
The user-authored activity title remains generic free text.

## Task integration

A task may reference one tracked activity. When the user completes that task,
the confirmation flow may offer:

> Complete this task and log "Exercise" at 18:20?

Requirements:

- the task completion and execution creation are shown as two effects;
- both use the authenticated user's identifiers;
- a retry is idempotent and cannot create duplicate executions;
- the execution stores `task_completion` provenance and the task identifier;
- restoring the task does not silently delete the execution;
- after restore, the user may keep, correct, or remove the log;
- logging an execution does not complete an unrelated task automatically.

A scheduled occurrence may be projected into Today without copying the tracked
activity into a new permanent task. The UI must distinguish an expected
occurrence from an ordinary task.

## Calendar integration

A calendar event indicates reserved time, not proof that an activity occurred.
Timemanager must never infer execution from event existence, elapsed event time,
or provider attendance state.

A tracked activity or occurrence may link to a calendar commitment. After the
event, Timemanager may ask:

> Did this happen?

Available responses:

- Log performed;
- Skipped;
- Not sure;
- Leave unresolved.

Requirements:

- performed creates an execution only after confirmation;
- skipped and unsure resolve the occurrence without creating an execution;
- source provider, calendar-event identifier, and recurrence-instance
  identifier are retained as provenance;
- unnecessary attendee, description, location, and provider content are not
  copied into the execution;
- Sensitive activity titles and notes do not enter an external calendar without
  the existing privacy-boundary preview and privacy-safe external-title choice;
- provider notifications remain outside Timemanager's privacy guarantee.

Calendar linking is deferred until the internal commitment boundary is
implemented and stable.

## Future Day Context integration

The deferred Phase 4
[Day Context feature](day-context-history-requirements.md) may place an
explicit Last Done execution beside mood, energy, focus, and other
user-confirmed events on a within-day timeline.

The integration must:

- reference the execution by stable identifier rather than copying it;
- preserve the execution as the authoritative occurrence/log-time record;
- never infer an execution from a state check-in, nearby event, calendar
  commitment, or model output;
- never infer that the execution helped, harmed, caused, or treated a state;
- store any possible-influence label as the user's editable attribution;
- update or remove the timeline reference when the source is corrected or
  deleted; and
- keep Last Done useful without Day Context, Quick Help, or AI.

This future integration does not change the first Last Done implementation or
authorise health interpretation.

## Privacy and security requirements

### Sensitive by default

New tracked activities default to Sensitive because a repeated behavioral
history may reveal health, religion, relationships, location patterns, finances,
or other private information even when the title appears ordinary.

For a Sensitive activity:

- device and push notifications contain no title, notes, reflection markers,
  user tags, schedule, occurrence state, people, location, or revealing action
  labels;
- push payloads contain only an opaque identifier and generic event type;
- details are retrieved only inside the authenticated application;
- account-wide notification-preview settings cannot weaken the classification;
- it is excluded from helper access, AI context, analytics content, and external
  integrations by default;
- any later share or external write requires a specific disclosure preview.

### User isolation

Every activity, schedule, occurrence, execution, note, reflection-marker
selection, user tag, query, export, and mutation is scoped to the signed-in
user. Guessing another object's identifier must return no data and must not
reveal whether it exists.

Every state-changing form retains CSRF protection. Hosted APIs additionally
require tenant isolation, authorization checks, rate limits, and auditable
access.

### Notification content

The independent importance/privacy contract in the
[high-level product design](high-level-product-design.md#notifications-and-attention-budget)
applies. A medication-related reminder can be Protected and Sensitive at the
same time.

A missing execution must not cause a notification that claims the user missed
the activity. Safe wording is:

> No execution is logged for this occurrence. Open Timemanager to review.

For Sensitive occurrences, even that status remains inside the application; the
device notification stays generic.

### Sharing

The first implementation provides no assistance-workspace access to tracked
activities or execution history.

Any later sharing design requires:

- per-activity and per-event scope;
- a full disclosure preview;
- explicit owner confirmation;
- expiry and immediate revocation;
- visible access/change history;
- no health-related sharing inferred from a general planning permission;
- a separate child-data and unsafe-family review.

### Export, retention, and deletion

Exports must include activity, schedule, occurrence, execution, note,
reflection-marker selection, user tag, privacy, timezone, revision, and
provenance data in a documented schema. They must exclude secrets and unrelated
provider credentials.

The user can permanently delete personal execution history and tracked
activities. Hosted retention, backup expiry, and deletion completion must be
stated precisely before launch.

## Medication safety requirements

Medication tracking is a private record of user-confirmed events. Timemanager:

- does not verify ingestion;
- does not decide whether a dose was missed;
- does not recommend taking, skipping, doubling, delaying, or changing a dose;
- does not calculate adherence;
- does not treat schedule timing as a prescription;
- does not replace medication packaging, a prescriber, or a pharmacist;
- does not silently convert "no log" into "missed";
- does not use logs for diagnosis, treatment suggestions, or helper scoring.

If a user is uncertain, the product directs them to their medicine-specific
instructions or an appropriate healthcare professional without generating
medicine-specific advice. Guidance on missed doses varies by medicine, and
taking doses too close together may increase risk.

Adding structured medication fields, adherence analytics, dose guidance,
clinical decision support, or caregiver medication management requires a new
product decision plus medical-device/regulatory, clinical-safety, privacy, and
security review.

## Offline, time, and failure behavior

- A locally confirmed execution survives application and device restart.
- A failed save is shown as failed; the UI must not display a successful log
  that was not committed.
- Retried submissions are idempotent.
- If future offline mutation is added, queued executions show an unsynchronized
  state and reconcile without duplicates.
- `Today` uses the user's current timezone; the stored execution retains the
  timezone in which it occurred.
- Daylight-saving transitions must preserve the selected local schedule slot
  and distinguish repeated or skipped wall-clock times.
- Travel does not silently rewrite historical dates or schedule slots.
- An unavailable calendar, notification, or AI provider never prevents manual
  logging or history retrieval.

## Accessibility and interaction requirements

- Log now is keyboard and screen-reader operable.
- The acknowledgement uses text and an accessible live region, not color alone.
- Occurrence status has non-color labels.
- Optional notes, reflection markers, and user tags do not interrupt the
  primary logging flow.
- Duplicate and medical-uncertainty warnings are concise, neutral, and do not
  use shame or urgency.
- Touch targets and controls support the existing responsive PWA layouts.
- The user can complete the core flow without sound, animation, microphone,
  external network, or AI.

## Acceptance criteria

### Core behavior

- A user can create an on-demand activity with only a title.
- A user can create one daily activity with multiple named time slots.
- Log now creates exactly one execution for the signed-in user.
- The user can add a note, reflection markers, and user tags without making
  them mandatory.
- The same reflection-marker keys and meanings are used for activity
  executions and task completions.
- The quick annotation surface shows at most four context-relevant markers;
  the grouped catalogue is available through progressive disclosure.
- Mutually exclusive marker dimensions and the three-marker event limit are
  enforced accessibly.
- Timing markers are neither shown without a timing reference nor selected
  automatically.
- Backdated execution displays both occurrence and log times.
- Last logged and logged-today answers cite the supporting execution.
- No-log answers use unknown language.
- A time-specific query is satisfied only by the selected schedule occurrence.
- Duplicate occurrence logging requires confirmation.
- Correction, undo, archive, export, and deletion behave as specified.

### Integration behavior

- Task completion cannot log an execution without a confirmation showing both
  effects.
- Retrying a confirmed task-plus-log action is idempotent.
- Restoring a task does not silently erase the execution.
- Calendar event existence or elapsed time never creates an execution.
- Sensitive calendar linking uses the external-provider disclosure boundary.

### Privacy and security

- Cross-user reads and mutations fail without revealing object existence.
- Every state-changing browser request has valid CSRF protection.
- Sensitive content never appears in push payload, notification preview,
  notification-history fixture, or mirrored-device fixture.
- Reflection markers inherit the target's privacy and are not shared or sent
  to external analytics by default.
- Standard preview preferences cannot override Sensitive.
- Sensitive history is absent from helper, AI, analytics-content, and calendar
  contexts unless a separately approved explicit disclosure exists.
- Export contains required history and provenance but no secrets.
- Deletion removes data according to the documented local or hosted contract.

### Time and resilience

- Day-scoped queries pass across midnight in the user's timezone.
- Schedule behavior is tested across daylight-saving changes.
- Travel preserves historical local dates and occurrence meaning.
- Failed and retried saves cannot create false acknowledgements or duplicates.
- Manual logging remains available during external-provider failure.

### Medication safety

- The system never says a medication was not taken solely because no log exists.
- It never recommends a dose action.
- It warns before logging a second execution for an already performed
  occurrence.
- Medication-related activity and execution details use the Sensitive contract.

## Delivery and dependency order

1. Complete schema migration, stable identifier, export, restore, and
   installation-provenance foundations.
2. Implement generic tracked activities, schedules, occurrences, and manual
   execution logging.
3. Add deterministic Last Done/today/schedule-slot retrieval.
4. Add correction, archive, export, deletion, notes, reflection markers, and
   user tags.
5. Validate privacy, time, accessibility, and medication-safety acceptance
   criteria.
6. Add explicit task linking.
7. Add notification delivery under the existing importance/privacy contract.
8. Add calendar linking only after the commitment integration is stable.
9. Consider natural-language input or carefully scoped sharing only after
   separate validation.

The first implementation is not complete until steps 1-5 pass. Task,
notification, calendar, AI, and assistance integrations are later gates, not
prerequisites for useful manual tracking.

## Evaluation

Evaluate:

- time and interactions required to create an activity;
- time and interactions required to log now;
- answer accuracy against known fixtures;
- user understanding of "no log" versus "did not happen";
- duplicate, correction, and backfill rates;
- whether optional notes, reflection markers, and user tags add value without
  slowing logging;
- whether four quick choices, grouped expansion, and the three-marker limit
  provide enough range without creating choice overload;
- whether users understand the shared marker meanings across event types;
- whether Sensitive defaults and generic previews are understandable;
- whether users can recover after missed logging without losing trust;
- whether the feature reduces uncertainty without encouraging unsafe reliance.

Do not use medication adherence, activity streaks, task count, or disclosure
volume as success metrics.

## Sources and evidence boundary

This feature is a plausible product design derived from the need for external
memory, visible history, and low-friction capture. Its exact interface and
effectiveness have not been clinically validated.

Current safety and privacy sources checked on 2026-07-24:

- [NHS Specialist Pharmacy Service: advising on missed or delayed doses](https://sps.nhs.uk/articles/advising-on-missed-or-delayed-doses-of-medicines/)
- [FDA: create and keep a medication list](https://www.fda.gov/consumers/consumer-updates/create-and-keep-medication-list-your-health)
- [ICO: what is special-category data?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/)
- [South African Information Regulator: POPIA guidance and applications](https://inforegulator.org.za/popia/)

These sources support cautious record keeping and the sensitive-data boundary;
they do not establish that Timemanager improves medication adherence or health
outcomes. Legal applicability and any medical-device or clinical-safety
obligations require review before a hosted medication use case is released.
