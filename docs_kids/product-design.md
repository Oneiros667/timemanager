# Timemanager Kids product design

Status: proposed separate child product; not implemented or authorized for real
child data

Updated: 2026-07-28

## Purpose

Timemanager Kids should help a child or young person understand what is
happening, communicate what they need, begin or transition between manageable
actions, and coordinate limited support from trusted adults.

It is intended solely for ages 8–17. It supports functioning and communication;
it is not:

- a diagnostic, treatment, therapy, crisis, safeguarding, or clinical
  decision-support service;
- a behaviour-management, discipline, attendance-enforcement, surveillance, or
  school-performance system;
- a replacement for a guardian, teacher, carer, clinician, pharmacist, school
  safeguarding process, individualized education plan, or medication
  administration record;
- a social network, messaging platform for unverified contacts, or advertising
  product; or
- an adult productivity application presented with simpler copy.

The design must be useful without an ADHD, autism, anxiety, or other diagnosis.
Children may have different communication, executive-function, sensory,
learning, physical, emotional, language, or accessibility needs. The
application supports expressed needs without inferring a condition.

## Product topology

Timemanager Kids is a separate application from adult Timemanager.

| Adult Timemanager | Timemanager Kids |
| --- | --- |
| Independent adult owns the account and plan | Verified guardian creates a child workspace |
| Adult helper proposes by default | Guardian, teacher, carer, and health roles have different scopes |
| Private adult planning and optional later health context | Child-visible planning plus separately gated school and health domains |
| Adult controls disclosure | Guardian authority is balanced with age-appropriate child notice, voice, privacy, and concern routes |
| Local pilot currently exists | Only synthetic child-support prototypes currently exist |

Shared infrastructure, if any, is limited to reviewed generic components such
as design tokens, accessibility utilities, build tooling, and cryptographic
libraries. Product data and authority never flow between the applications by
default.

## Intended users

### Primary supported person

A child or young person aged 8–17 whose own plan, requests, and selected support
information are represented.

### Adult support roles

- a verified parent or legal guardian;
- a verified teacher with a current school role;
- a designated carer with a specific purpose and expiry;
- a school nurse or other designated school health professional; and
- trained product safety/privacy support staff acting under audited, limited
  operational access.

Adults do not receive a personal planning workspace inside the child product.
An adult who wants their own Timemanager plan uses the separate adult product.

## Age and evolving capacity

Calendar age alone does not decide comprehension, capacity, legal authority, or
support needs. The product uses age bands to select a starting presentation,
then supports individual accessibility and communication preferences.

| Age band | Starting presentation | Authority and participation baseline |
| --- | --- | --- |
| 8–10 | Concrete language, one question per screen, strong visual structure, minimal reading | Guardian-operated; child receives clear notice, sees relevant changes, and can express preferences, needs, and objections |
| 11–12 | Short explanations, more choice, visible reasons and history | Guardian-operated; child participation is expected and recorded where appropriate |
| 13–15 | Greater direct control over daily planning and disclosure conversations | Guardian authority remains jurisdiction-specific; child privacy and assent/objection carry increasing weight |
| 16–17 | Near-adult planning controls with explicit transition preparation | Legal capacity and guardian rights vary; the product applies market rules and never assumes full adult authority early |

The youngest intended age governs the clarity of a shared flow unless the
interface reliably selects another tested presentation. Birthdays do not
silently change permissions, disclose data, remove guardians, or migrate the
workspace.

## Product outcomes

The application should help the child:

- see what is happening now and what fixed commitment comes next;
- capture a thought or request without organizing it first;
- choose from a deliberately small plan;
- see a concrete next action and what “done” means;
- ask for help, more time, a quiet space, clarification, or a trusted adult;
- communicate “I'm overwhelmed” or “I can't talk right now” with low language
  demand;
- coordinate a calm, non-punitive break with agreed supports and a check-in;
- return after interruption, absence, conflict, or a difficult day without
  overdue debt or shame;
- understand what a guardian or school adult created, changed, saw, or sent;
- correct or challenge inaccurate information through an age-appropriate
  route; and
- know when a message is queued, delivered, acknowledged, unavailable, or
  failed.

The application should help an authorized adult:

- support rather than monitor the child's day;
- share only the minimum information needed for a named purpose;
- distinguish a suggestion, request, fixed commitment, medication plan, and
  factual observation;
- see when authorization is absent, expired, disputed, or insufficient;
- coordinate without duplicate reminders or hidden changes; and
- hand off or revoke access safely when a role ends.

Task count, compliance, streak length, disclosure volume, app-open frequency,
and time under adult observation are not success outcomes.

## Product principles

1. **Best interests first.** Commercial, guardian, school, and engagement goals
   never override the child's safety, privacy, development, or voice.
2. **Support without surveillance.** No covert location, hidden tasks, secret
   monitoring, or invisible guardian/teacher access.
3. **The child can communicate with little language.** Help requests must not
   depend on composing a detailed explanation.
4. **Now is deliberately small.** Show one anchor and no more than three
   optional actions in the default day plan; validate this adaptation with
   children rather than assuming the adult limit is optimal.
5. **Fixed commitments and flexible actions remain different.**
6. **A schedule is not proof.** Missing feedback, a missing log, or a planned
   medication time never establishes what happened.
7. **Facts, reports, and inferences stay distinct.** Do not turn a teacher
   observation or child self-report into a diagnosis or causal claim.
8. **Consequential actions are previewed and confirmed.** Sharing, deleting,
   rescheduling, inviting, and external calendar changes require explicit
   authorized confirmation.
9. **Recovery is ordinary operation.** No shame, punishment, forced streak,
   silent rollover, or automatic escalation after a hard day.
10. **High privacy is the default.** Collect, retain, and disclose only what a
    specific feature requires.
11. **The useful core works without AI, voice, precise location, or third-party
    analytics.**
12. **Adults have roles, not ownership of the child's whole inner life.**

## Core experience

```text
Guardian creates authorized workspace
             |
             v
Child sees Today -> chooses/starts -> focuses/transitions -> closes
      |                  |                    |
      |                  +-> asks for help ---+
      |
      +-> calm break / low-capacity route
      |
      +-> selected school or carer communication

All adult-created and externally shared changes
remain visible in age-appropriate history.
```

### Orient

Show:

- current part of the day;
- next fixed commitment and necessary transition;
- one guardian/child-agreed anchor;
- up to three optional actions;
- any active support or communication status; and
- a persistent “Tell someone what I need” route.

### Choose and start

The child may choose an optional action, accept the suggested anchor, request a
different action, say “not now,” or ask for help. A task reveals one concrete
next action before secondary detail.

### Focus and transition

A bounded timer may make time visible, but it does not lock the child in,
penalize stopping, or report distraction. Transition cues protect fixed
commitments without implying that flexible work is compulsory.

### Low Capacity

Low Capacity keeps the next fixed commitment, one safe actionable item, quick
capture, and the help/communication route. It hides other work without
deleting, completing, reporting, or reprioritizing it.

### Calm break

A calm break is an agreed supportive pause, not a “time-out” punishment. The
plan can include grounding, mindfulness, music, water, food, a quiet activity,
or another family-approved option. These are choices, not completion
requirements. The child can say ready, need help, or talk about the plan.

### Recover

After a missed day, interruption, or changed plan:

1. show the next real commitment;
2. identify only consequence-bearing decisions;
3. choose one current action;
4. move the remainder to later review; and
5. preserve an intelligible change history.

## Capability scope

### Foundational child release

- guardian-created workspace and age/market routing;
- child Today, Later, fixed commitments, one anchor, small optional plan;
- child capture, help requests, neutral task detail, and recoverable Drop;
- child-visible history of guardian changes;
- Low Capacity, calm-break agreement, and same-device accessibility;
- export, correction, revocation, deletion-request, and retention controls;
- no school connection, medication, AI, voice, or external calendar.

### Later gated capabilities

- verified school or carer relationships;
- low-language child messages with delivery and acknowledgement evidence;
- field-level classroom-support sharing;
- neutral daily feedback;
- designated school-health-professional workflows;
- external calendar connection;
- native mobile or wearable surfaces; and
- clinically reviewed health support.

Each is independently gated. A later capability never becomes authorized
because the foundational release exists.

## Explicit exclusions

The product does not include:

- independent child email registration, billing, advertising, social
  discovery, public profiles, friend lists, or open chat;
- targeted advertising, data brokerage, behavioral profiling, or sale/sharing
  of personal data;
- precise location, continuous device tracking, background microphone/camera,
  emotion recognition, voice-stress analysis, or passive diagnosis;
- behavior points, demerits, rewards contingent on medication, compliance
  rankings, guardian/teacher leaderboards, or “good child” scores;
- automatic attendance, medication-adherence, mood, productivity, or
  treatment-effect inference;
- a teacher's general access to diagnosis, medication, family, task, mood, or
  private child communication history;
- dose calculation, missed-dose advice, treatment changes, or prescribing;
- hidden safety monitoring presented as ordinary planning; or
- AI in the first real-data release.

## Commercial model

The product is subscription-only with no advertisements. The guardian is the
billing contact, but payment does not establish identity, guardianship,
consent, or authority.

Core planning, accessibility, child communication, privacy controls, export,
correction, deletion requests, and safety functionality cannot be paywalled as
premium extras after a workspace is active. Pricing, trials, hardship access,
institutional purchasing, refunds, and additional adult seats require separate
decisions and child-best-interests review.

## Evidence boundary

The adult ADHD research supports several general executive-function design
mechanisms, but its adult evidence does not validate an 8–17 product. The exact
Today limit, calm-break workflow, child signals, teacher feedback, age-band
presentation, and guardian interaction are **plausible** designs requiring
research with children, guardians, educators, accessibility specialists,
child-development expertise, clinicians where health content is involved, and
privacy/safeguarding reviewers.
