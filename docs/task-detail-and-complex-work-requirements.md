# Task detail and complex-work requirements

Status: core Phase 1 engineering slice and project discovery implemented;
usability evidence incomplete

Updated: 2026-07-28

## Purpose

Timemanager must help a user turn a short capture into work that can be started
without requiring them to construct or maintain a complex project-management
system.

Milestone 1.2 adds two related capabilities:

- **1.2a — Task clarity:** optional task detail, next action, definition of
  done, and a short component checklist; and
- **1.2b — Complex work:** lightweight project/outcome grouping, ordered tasks,
  explicit prerequisites, external waiting, and one visible next-ready task.

The decomposition principle is supported by ADHD-focused CBT and metacognitive
therapy. The exact hierarchy, checklist limits, dependency presentation, and
state model are plausible product-design choices that require usability
validation. They must not be presented as clinically validated.

The local pilot now implements title-only capture, task and project workspaces,
components, preferred ordering, prerequisites, external waits, readiness,
project collection/archive navigation, and separate Today placement through
migrations `0004` and `0005`. Export format v3 preserves the relationships and
import retains v1/v2 compatibility. This is implementation evidence, not
usability or clinical validation: the synthetic prototype exists, but the
required five participant sessions have not been run.

## Product decisions

1. Capture continues to require only a short title. Project, component,
   dependency, next-action, and definition-of-done fields are never required
   before saving.
2. Complex work uses a shallow hierarchy:
   **project/outcome → task → optional component**.
3. Arbitrary nesting, goal trees, project portfolios, Gantt charts, and a
   general dependency-graph interface are out of scope.
4. A component that may need its own schedule, blocker, assignee, Today
   selection, focus session, or independent completion history is a task, not a
   checklist item.
5. Today contains actionable tasks. A project and its checklist components do
   not consume additional Today capacity.
6. A project exposes one next-ready task by default, plus a small number of
   other currently actionable tasks when useful. It does not expand the full
   project into Today.
7. A displayed sequence is a preferred order. A prerequisite is a hard
   dependency recorded separately. Reordering tasks must not silently create or
   remove dependencies.
8. Internal prerequisites and external waiting are different:
   a prerequisite points to another task; external waiting records what or whom
   the user is waiting for.
9. Completing a prerequisite may make another task actionable, but it never
   silently promotes that task into Today or makes it the highlight.
10. Dependencies are user-authored planning information, not facts imposed by
    Timemanager. The user may explicitly override or remove a blocker.
11. Completing every linked task does not automatically complete a project.
    The user confirms whether the desired outcome was achieved.
12. The useful manual flow must not depend on AI. Any future decomposition
    suggestion is editable, initially shows no more than one to three proposed
    actions, and requires confirmation before changing saved work.

## Domain terminology

| Term | Meaning |
| --- | --- |
| Capture | Original, minimally processed text saved without clarification requirements |
| Project/outcome | A lightweight grouping for a result that requires multiple independently manageable tasks |
| Desired outcome | The user-authored condition that would make the project complete |
| Task | A meaningful, independently completable unit of work |
| Next action | The next observable physical or digital action that starts or advances a task |
| Definition of done | The user-authored condition that establishes task completion |
| Component | A short checklist step inside one task that does not need independent planning |
| Preferred order | Display order that guides work but does not block it |
| Prerequisite | Another task that the user says must be completed first |
| External wait | A non-task blocker such as waiting for a person, provider, delivery, or decision |
| Follow-up task | An actionable task such as “Ask Sam again on Thursday”; it is distinct from the waiting record |
| Actionable | Open work with no unresolved prerequisite or external wait |
| Today placement | Whether an actionable task is unplanned, selected in the active Today plan, or recoverable Today overflow |

## Capture and clarification

Capture remains a one-field path. Saving a title must not open a compulsory
classification form.

From Later or task detail, the user may:

- keep the item as a standalone task;
- add or edit a next action and definition of done;
- add a short component checklist;
- create a new project around it;
- link it to an existing project;
- split independently manageable work into project tasks;
- add a prerequisite or external wait; or
- leave it unclarified.

Original title text and capture time remain available after clarification.
Converting a task into project work must preview which record remains the task,
which project will be created, and which components will become separate tasks.
The conversion is explicit and reversible where no later conflicting edits
make automatic reversal ambiguous.

The implemented conversion creates a project with an editable, pre-filled
project name and retains the captured record as its first task. The preview
states that Today placement, task detail, steps, and blockers remain on that
task; no component is promoted automatically. The task’s definition of done
initially supplies the project’s desired outcome and remains editable in both
places.

## Task detail

Task detail is a contextual view reached from Today, Later, Review, or a
project. It is not a new primary navigation destination.

The first implementation supports:

- editable title;
- optional next action;
- optional definition of done;
- optional notes;
- optional project/outcome link;
- a short ordered component checklist;
- preferred position within a project;
- prerequisite and external-wait summaries;
- current workflow status and Today placement;
- existing completion, drop, restore, highlight, and Today actions where
  valid; and
- provenance and timestamps where needed for conflict resolution or export.

Opening an active task prioritises its next action and definition of done over
metadata. Project, blocker, and component detail remains progressively
disclosed.

The user can complete a task even when its checklist is incomplete, after a
neutral confirmation that the checklist still contains unfinished components.
The checklist assists execution; it is not an automatic truth test for the
definition of done.

## Projects and components

A project has:

- title;
- desired outcome;
- state: active, completed, or dropped;
- ordered linked tasks;
- one computed next-ready task, or one explicitly selected from the currently
  actionable project tasks;
- stable public identity, ownership, revision, provenance, and timestamps; and
- optional notes.

Project order is for orientation. A task can appear earlier or later without
being blocked. When order is mandatory, the user adds a prerequisite.

A task component has:

- parent task;
- short title;
- preferred position;
- checked or unchecked state; and
- stable identity, revision, and timestamps sufficient for transfer and
  conflict handling.

Components cannot contain components or dependencies. The interface should
initially reveal no more than one to three components and keep the remainder
collapsed. If a component gains independent planning needs, the user may
promote it to a project task through an explicit preview.

Project progress is described using concrete task and outcome state. The first
implementation does not use completion percentages, velocity, streaks, or
claims that task-count progress equals outcome progress.

### Implemented project discovery slice

Later now links to an account-scoped project collection rather than adding a
mandatory fifth primary destination. The collection:

- lists active projects with their desired outcome, deterministic next-ready
  task, and concrete ready/waiting/done counts;
- keeps completed and dropped projects in a collapsed archive;
- restores an archived project only through a CSRF-protected, revision-checked
  action;
- leaves archived project structure read-only until the project is restored;
- preserves linked task state, placement, ordering, and revisions when a
  project is restored;
- preserves a validated local return path between Later, task detail, project
  detail, and the collection; and
- presents **Add to an existing project** separately from **Turn into a new
  project** in task detail.

Automated server and browser coverage verifies this implementation contract.
Manual screen-reader, keyboard, zoom, forced-colors, and real-device checks for
the new collection remain required, and the five-participant usability gate has
not been run.

## Dependencies, blockers, and ordering

### Internal prerequisites

A task may depend on one or more tasks owned by the same account. A task is
internally blocked while any prerequisite remains incomplete.

The system must:

- reject self-dependencies and direct or indirect cycles;
- reject cross-account dependencies;
- show which tasks are blocking the work;
- distinguish preferred ordering from required prerequisites;
- recalculate readiness when a prerequisite is completed, restored, or
  dropped; and
- preserve an intelligible history through object revisions and timestamps.

Completing the last prerequisite changes the dependent task's computed
readiness. It does not select that task for Today.

Restoring a prerequisite makes the dependent task blocked again. If the
dependent task is already in Today, it remains visible with a blocked
explanation and offers explicit choices to keep it visible, replace it, or
remove the dependency. Timemanager does not silently remove or replace a
selected task.

Dropping a prerequisite leaves the dependency unresolved until the user chooses
to:

- restore or replace the prerequisite;
- remove or override the dependency;
- keep the dependent task waiting; or
- deliberately drop the dependent task.

### External waiting

External waiting records:

- a short neutral reason, such as “Waiting for Sam's approval”;
- an optional expected response or review date;
- an optional person or organisation label entered by the user; and
- an optional linked follow-up task.

An expected response date is a review cue, not a claim that the blocked work is
overdue. Missing that date surfaces a neutral decision: continue waiting,
follow up, change the plan, remove the blocker, or drop the work.

“Waiting for Sam” is not actionable. “Ask Sam again on Thursday” is a separate
actionable follow-up task. Completing the follow-up task does not silently
resolve the external wait.

### Explicit overrides

The user may mark a task “can start anyway” or remove a blocker after a preview.
The action updates the task revision and is reversible through another explicit
edit. Timemanager does not infer an override from starting a timer or checking a
component.

## Workflow status and Today placement

The pre-1.2 schema used `active` for an active Today selection and `ready` for
recoverable Today overflow. Migration `0005` retains that legacy compatibility
column but does not reuse those values to mean dependency readiness.

The implemented domain separates:

| Dimension | Implemented values | Purpose |
| --- | --- | --- |
| Workflow status | inbox, open, waiting, done, dropped | What can happen to the work |
| Today placement | unplanned, active, overflow | Whether an actionable task is selected for a date |
| Highlight | true or false for one eligible task per date | Which selected task is the meaningful win |
| Readiness | actionable or blocked, computed from workflow status, prerequisites, and external waiting | Whether the task can currently be acted on |

Implementation may use different storage names, but the domain meanings must
remain separate. Migration from the current task states must preserve:

- captured-work membership;
- active Today selections;
- recoverable Today overflow;
- one highlight per account and date;
- done and dropped tasks;
- the one-highlight-plus-three optional-action capacity; and
- deterministic export/import behavior.

## Today and project presentation

Today shows only the small active plan and recoverable overflow. It does not
render an entire project tree.

For a task linked to a project, Today may show the project title as quiet
context. Starting the task opens its task detail or Launch view, not the whole
project.

Blocked tasks are not offered as new Today candidates by default. If a selected
task becomes blocked, it remains visible until the user makes an explicit
choice. A newly unblocked task may appear as a Review or Later suggestion but
is never automatically promoted, highlighted, or substituted.

Until the Review destination lands, open or waiting work outside the current
Today plan remains discoverable in Later. Blocked work links to its
workspace there instead of offering direct Today placement.

Selecting a project from search or Review opens the project and foregrounds its
next-ready task. Selecting a vague project capture for Today requires the user
to clarify or choose an actionable task first.

## Completion, restoration, and conflicts

- Completing a task records task completion only; it does not complete its
  project or silently advance another task into Today.
- Completing all project tasks prompts the user to confirm whether the desired
  outcome was achieved, needs another task, or should remain open.
- Restoring a completed task restores its dependency effects and uses the
  existing explicit Today-capacity rules if the user also chooses Today.
- A task with unresolved blockers may still be completed through an explicit
  confirmation, because the user may have achieved the result another way.
- Concurrent or imported edits use stable public IDs and positive revisions.
  Divergent same-revision content fails closed under the account-transfer
  contract.
- Deleting or dropping project structure must not silently delete linked tasks.

## Ownership, privacy, and portability

Every project, task, component, dependency, wait, query, and mutation is scoped
to the signed-in account. Sharing one local installation creates no cross-user
linking or visibility.

Account export/import must evolve as a versioned contract. It must:

- include project, component, dependency, and waiting data when implemented;
- retain stable public IDs, origins, revisions, and user-authored content;
- import older supported task-only packages with documented defaults;
- preserve referential integrity and fail closed for missing, cyclic,
  cross-account, or divergently owned relationships;
- remain atomic and retry-safe; and
- continue excluding password hashes, secrets, internal database IDs, and
  unrelated accounts.

Task and project text may contain sensitive personal information. It remains
private authenticated content and must not be stored in the public service
worker cache or disclosed through external integrations.

## Accessibility and low-capacity behavior

- All task-detail and dependency operations are keyboard accessible and have
  explicit text labels.
- Readiness cannot be communicated by colour alone.
- Reordering has non-drag controls and announces the resulting position.
- Blocked explanations name the prerequisite or waiting reason without
  shame-oriented language.
- Low Capacity shows at most the highlight or one chosen actionable task, its
  next action, essential commitments, Capture, and access to Reset.
- Project trees, complete checklists, and dependency editing remain hidden in
  Low Capacity unless the user deliberately opens task detail.

## Non-goals for milestone 1.2

Milestone 1.2 does not include:

- arbitrary nested subtasks or projects;
- complex project portfolios, goal trees, critical-path calculation, Gantt
  charts, resource allocation, or multi-user assignment;
- automatic decomposition or AI-generated project plans;
- automatic rescheduling, Today promotion, highlight replacement, or project
  completion;
- calendar integration, reminders, or external notifications;
- completion percentages, streaks, productivity scores, or earned rewards;
- hosted sharing, guardian workspaces, or trusted-person proposals; or
- treating a preferred order, expected response date, or planned date as a
  hard dependency.

## Delivery slices and exit gates

Implementation status on 2026-07-28: both slices are present in the local pilot
with server and real-browser automation. The participant gate, manual
screen-reader review, and recorded contrast review remain open, so milestone
1.2 is `Partial`, not validated or complete.

### 1.2a — Task clarity

Deliver:

- authenticated task-detail view;
- editable title, next action, definition of done, notes, and short components;
- unchanged title-only capture;
- ownership, CSRF, validation, revision, migration, and transfer behavior; and
- Today, Later, and Low Capacity presentation appropriate to the new fields.

Exit gate:

- every mutation is account-scoped and CSRF-protected;
- all new structure is optional and editable;
- task completion with unfinished components is explicit;
- existing databases migrate without losing Today placement or task history;
- supported export/import fixtures remain deterministic and retry-safe; and
- server, browser, keyboard, focus-order, and accessible-name checks pass.

### 1.2b — Complex work

Deliver:

- lightweight projects and desired outcomes;
- task-to-project linking and preferred ordering;
- task-component promotion;
- internal prerequisites and external waiting;
- computed readiness and one next-ready task;
- account-scoped project collection, archive, and explicit restoration;
- explicit dependency override and lifecycle behavior; and
- versioned account-transfer support for the new relationships.

Exit gate:

- no nested hierarchy or dependency cycle can be created;
- ordering never silently creates a blocker;
- blocked tasks are excluded from new Today suggestions;
- blocking or unblocking never silently changes the active Today plan;
- project completion requires user confirmation;
- cross-account relationship access returns no information;
- migration and import reject invalid relationships atomically; and
- representative complex-work flows pass browser and accessibility checks.

## Validation questions

Prototype and pilot evaluation should test:

- Can a user capture vague work without classifying it immediately?
- Can they tell whether something is a project, task, or component without
  learning project-management terminology?
- Can they find the next actionable task without scanning the whole project?
- Do preferred order, prerequisite, and external waiting have distinct,
  understandable meanings?
- Does a blocked Today task remain understandable without making the day feel
  like a failure?
- Can a user return after an absence and understand what is ready, waiting, or
  no longer relevant?
- Does progressive disclosure reduce clutter for minimalist-tool users without
  hiding necessary structure from feature-rich-tool users?
