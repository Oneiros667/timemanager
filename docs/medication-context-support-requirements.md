# Private medication context and schedule support requirements

Status: proposed Phase 4 product requirement; not implemented, clinically
validated, or authorised for release

Updated: 2026-07-28

## Purpose

Timemanager should let a user add a private medication profile and
user-recorded schedule so that future Quick Help responses can offer support
appropriate to the medicine and formulation the user identified.

Different medicines and formulations can have different duration, adverse
effects, administration instructions, and support considerations. A generic
model must not guess which guidance applies from a brand-like string or from
the user's symptoms alone.

This feature therefore separates:

- the user's medication record;
- the user's record of the schedule they were given or follow;
- a user-confirmed record that a scheduled or unscheduled dose was taken;
- the user's observed mood, energy, focus, food, caffeine, sleep, and other Day
  Context;
- versioned, clinically reviewed support content for an exact medication
  identity, formulation, and jurisdiction; and
- treatment, dose, missed-dose, and interaction decisions that remain with the
  medicine instructions, pharmacist, prescriber, or another appropriate
  healthcare professional.

The feature is a private record and support context, not a prescribing,
dispensing, adherence, or clinical decision-support system.

It extends but does not replace:

- [Last Done](repeatable-activity-history-requirements.md), whose generic
  activity schedule and execution history can record what the user says
  happened;
- [Day Context](day-context-history-requirements.md), which places confirmed
  events beside self-reported state without claiming causation; and
- [Quick Help](quick-help-mood-energy-design.md), which may select approved
  support content but must not improvise medication instructions.

## Evidence and status boundary

The FDA recommends keeping a current medication list that includes medicine
name, strength, purpose, and instructions for when, how, and how much is taken.
That supports a user-owned record. It does not establish that Timemanager can
verify a prescription, detect errors, or safely advise on changes.

NICE states that stimulant effect size, duration, and adverse effects vary from
person to person and recommends monitoring and recording adverse effects.
Those points support medication- and person-specific context rather than one
generic ADHD-medication response. They also reinforce that treatment is
initiated, titrated, monitored, and reviewed by appropriately trained
healthcare professionals.

NHS Specialist Pharmacy Service guidance directs people to medicine-specific
sources such as the supplied Patient Information Leaflet for missed-dose
instructions and notes that the consequences of timing errors differ between
medicines. Timemanager must therefore fail closed rather than generate a
missed-dose answer from a schedule.

Medication names, strengths, instructions, schedules, executions, observed
effects, and linked state history reveal health information. The complete
feature is **Sensitive** by default. Legal basis, clinical-safety ownership,
medical-device/regulatory applicability, medicine-dictionary licensing, and
jurisdiction-specific release approval remain unresolved gates.

## Product decisions

1. Adding medication context is optional and initiated by the user.
2. A medication profile records what the user entered or imported. It is not
   labelled verified unless a future approved source and verification flow
   actually establish that status.
3. A user-recorded schedule is a plan. It never proves that a dose was taken
   or that the plan was clinically verified.
4. Only an explicit user confirmation creates a medication execution. Absence
   of an execution is unknown, not evidence of a missed dose.
5. The user may privately record name, active ingredient, formulation,
   strength, prescribed instructions, schedule, and other information useful
   for maintaining their medication list.
6. Strength and dose information may be stored and displayed as part of the
   user's record, but the first support engine does not calculate from them or
   use them to generate a dose action. An exact strength may only determine
   whether a reviewed content rule is eligible; an unsupported value fails
   closed.
7. Quick Help may select medication-specific support only from versioned,
   clinically reviewed content matched to an unambiguous medicine identity,
   formulation, supported population, and jurisdiction.
8. If identity, formulation, instructions, content currency, or jurisdiction
   is ambiguous, medication-specific support fails closed to generic support
   and a medicine-information/pharmacist/prescriber route.
9. A generative model may simplify the wording of approved content within a
   tested template. It may not create new medication advice, change the
   clinical meaning, select a dose action, or expand beyond the approved
   content.
10. Timemanager never recommends taking, skipping, delaying, repeating,
    doubling, reducing, increasing, stopping, restarting, or switching a
    medicine.
11. Timemanager does not answer interaction questions about medicines,
    caffeine, food, alcohol, supplements, or other substances from model
    reasoning.
12. Medication schedule and history are always Sensitive in the first
    implementation. They cannot be reclassified as Standard.
13. Medication data is excluded from trusted people, calendars, notification
    details, analytics content, and AI context by default.
14. Every external disclosure requires a specific preview and confirmation;
    adding a profile never grants ongoing AI or third-party access.
15. The user can correct, version, export, and permanently delete the profile,
    schedule, and linked history.
16. The feature remains useful without AI. The medication list, schedule,
    official-source links, reminders, and execution log use deterministic
    local behavior.
17. Medication Context is deferred Phase 4 work. It does not change the
    generic Phase 1 Last Done scope or authorise implementation in the local
    pilot or Phase 3 hosted release.

## Goals

The feature should:

- let the user maintain an accurate private list without depending on memory;
- preserve the medicine and formulation distinctions needed to select the
  correct reviewed content;
- distinguish user-recorded schedule, reminder delivery, user-confirmed
  execution, and observed context;
- make schedule changes prospective and historically traceable;
- let the user review the instructions they recorded and open the source
  medicine information;
- provide reviewed support strategies relevant to the recorded medicine when
  exact matching and release gates pass;
- let Quick Help use only the minimum medication context the user selected;
- support correction, export, deletion, timezone changes, and offline access;
- keep private content out of notifications and unrelated integrations; and
- make every unsupported or ambiguous case obvious.

## Non-goals

The first Medication Context implementation does not include:

- prescription verification;
- prescribing, dispensing, titration, or treatment planning;
- deciding whether a dose is due, late, missed, duplicated, or safe to take;
- dose calculation, dose conversion, splitting, tapering, or maximum-dose
  checks;
- interaction checking;
- contraindication or allergy checking;
- refill management or pharmacy ordering;
- adherence scoring, compliance reports, or caregiver monitoring;
- automatic medication recognition from symptoms;
- automatic extraction from packaging, a photograph, PDF, email, or health
  record without an explicit review-and-confirm flow;
- automatic causation claims between medication and mood, energy, focus,
  appetite, sleep, heart rate, or another state;
- automatic calendar writes;
- clinician, trusted-person, or employer access;
- emergency identification or a promise that the stored list is complete; or
- replacement for the current prescription label, Patient Information
  Leaflet, pharmacist, prescriber, or emergency medication list.

## Domain terminology

| Term | Meaning |
| --- | --- |
| Medication profile | The user's private record for one medicine or formulation |
| Medication identity | A confirmed mapping to a licensed jurisdiction-appropriate medicine identifier, distinct from display text |
| Display name | The user-visible brand, generic, or personal label |
| Formulation | The relevant release form and route, such as immediate-release tablet or extended-release capsule |
| Regimen version | One historical version of user-recorded instructions and schedule |
| Schedule slot | A named planned local time or user-described timing rule within a regimen |
| Scheduled occurrence | One date-specific planned instance of a schedule slot |
| Medication execution | The user's explicit record that they say a dose was taken |
| User-recorded instructions | Text the user says came from their label, leaflet, pharmacist, or prescriber; not verified by Timemanager |
| Approved support content | Versioned guidance reviewed for a specific medicine/formulation, population, and jurisdiction |
| Support strategy | A non-dose action or information item allowed by approved content |
| Clinical decision | A dose, timing, interaction, treatment, diagnostic, or escalation judgment outside Timemanager's ordinary support scope |
| Sensitive | A mandatory privacy classification preventing details leaving the authenticated application by default |

## Medication profile

### Minimum profile

The minimum profile requires:

- a user-visible medication name;
- an explicit **user entered** provenance label; and
- confirmation that the record is private and does not replace the medicine
  label or professional instructions.

The user can save a private list entry without creating a schedule, reminder,
execution history, Day Context link, or AI permission.

### Optional fields

The user may add:

- brand/display name;
- active ingredient or generic name;
- medicine identifier from an approved jurisdiction-specific dictionary;
- formulation, release type, and route;
- strength as printed;
- user-recorded prescribed dose;
- what the user says the medicine is for;
- user-recorded instructions for when and how it is taken;
- schedule slots and timezone;
- start date, end date, or inactive state;
- source type, such as manual, label, leaflet, pharmacist, prescriber, or
  future approved import;
- the date the user last checked the record against its source;
- an official Patient Information Leaflet or regulator-approved medicine
  information link;
- a private note; and
- a user-authored support plan.

No diagnosis, prescriber, pharmacy, dose, purpose, or note is required. Data
collection remains limited to what the user finds useful.

### Identity and formulation matching

Medication-specific content requires more than a display-name string.

- Brand names may differ between jurisdictions.
- One brand may have multiple strengths or formulations.
- Immediate- and extended-release formulations may require different content.
- Similar names must not be resolved through fuzzy matching without user
  confirmation.
- A user label such as "morning meds" never selects medication-specific
  content.
- A medicine-dictionary match records its dictionary, identifier, version,
  jurisdiction, and confirmation provenance.
- Changing identity or formulation creates a new profile/regimen version when
  needed; it does not rewrite historical content provenance.

When no supported identity match exists, the profile remains a useful private
free-text record but receives only generic support.

## Regimen and schedule

### Schedule creation

A regimen may contain one or more named schedule slots. A slot may record:

- local time;
- selected weekdays or daily recurrence;
- user-recorded relation to waking, sleep, food, or another event;
- timezone;
- effective start/end dates; and
- the exact user-recorded instruction shown when the slot is opened.

The schedule is copied from the user's own instructions. Timemanager does not
generate, optimise, or recommend it.

### Schedule changes

- Editing a regimen creates a new effective version.
- Historical occurrences and executions retain the regimen version in effect
  at their occurrence time.
- A future change does not rewrite earlier records.
- A timezone or travel change never silently moves a medicine time.
- The user sees both the stored local time and timezone before confirming a
  travel-related schedule change.
- Timemanager does not advise how to adapt a regimen for travel, daylight
  saving, sleep changes, fasting, illness, or a missed dose.

### Schedule is not execution

The interface uses separate language:

- **Scheduled at 05:30** means the plan contains a 05:30 occurrence.
- **Logged at 05:34** means the user recorded that they say it was taken.
- **No execution logged** means only that Timemanager has no execution record.
- **Reminder delivered** means only that a notification attempt occurred.

It must never convert these into:

- "Taken" from the schedule;
- "Missed" from an absent execution;
- "Late" without the user selecting or confirming that meaning; or
- a recommendation about the next dose.

Medication executions use the exactness, duplicate-warning, correction, and
missing-log contract in Last Done.

## Medication-specific support

### Allowed support sources

Support content may come from:

- the user's own recorded prescription/label instructions, displayed as
  user-entered text;
- the current regulator-, health-service-, manufacturer-, or
  clinician-approved Patient Information Leaflet for the exact medicine and
  jurisdiction;
- a versioned Timemanager content rule approved by a qualified clinical owner;
  or
- a human-help route to a pharmacist, prescriber, urgent service, or other
  appropriate professional.

The interface distinguishes user-entered instructions, quoted or paraphrased
source content, and Timemanager interface copy.

### Allowed strategy scope

Subject to exact content approval, Quick Help may offer:

- a reminder to follow the user's recorded instructions;
- a link to the exact approved medicine information;
- a small non-dose support action for a recognised issue, such as a reviewed
  meal/appetite, sleep-routine, or low-capacity strategy;
- a user-authored personal playbook;
- a suggestion to record the current state or context;
- a bounded reassessment;
- a prompt to discuss a recurring pattern with the pharmacist or prescriber;
  and
- reviewed urgent-symptom routing.

Support wording must state uncertainty. A recognised adverse effect does not
prove that the medicine caused the user's current experience.

### Prohibited advice

Quick Help must not generate or infer:

- whether to take a scheduled, late, missed, or additional dose;
- whether two doses are too close together;
- a different time, dose, formulation, or administration method;
- whether to stop, restart, taper, split, crush, open, or switch a medicine;
- whether a medicine is working;
- whether a symptom is an adverse effect or interaction;
- whether caffeine, food, alcohol, an over-the-counter medicine, or a
  supplement is safe with the user's medicine;
- whether to change treatment because of mood, energy, focus, appetite, sleep,
  weight, blood pressure, heart rate, or another observation; or
- advice for pregnancy, breastfeeding, older age, kidney/liver
  impairment, eating disorders, cardiovascular conditions, or another
  clinical circumstance unless a separately approved clinical product
  explicitly supports it.

These questions use the exact medicine information or a pharmacist/prescriber
route. Urgent symptoms use the reviewed urgent-support route.

### Content rule requirements

Every medication-specific rule requires:

- canonical medicine identifier;
- brand applicability where relevant;
- formulation, release type, and route;
- supported strength range if strength changes the content;
- supported population and exclusions;
- jurisdiction and language;
- user question/context category;
- allowed response and actions;
- prohibited inferences;
- primary source title, URL, version/date, and access date;
- clinical owner and reviewer;
- approval date and re-review/expiry date;
- content version and change history; and
- deterministic tests.

Expired, withdrawn, mismatched, ambiguous, or unavailable content fails closed.
The fallback is generic support plus the medicine-information and human route,
not model improvisation.

## Quick Help resolution flow

```text
User asks for help
        |
        v
Urgent / dose / missed-dose / interaction boundary
        | ordinary support request
        v
User explicitly selects medication context
        |
        v
Resolve exact identity + formulation + jurisdiction
        | supported and current
        v
Load approved content rule
        |
        v
Optional constrained phrasing
        |
        v
Show provenance, uncertainty, actions, and human-help route
```

The model is not responsible for identity resolution, rule eligibility,
source selection, privacy scope, or permission to disclose a profile.

## Lunchtime-slump scenario

Assume the private profile says:

- display name: Vyvanse;
- matched identity: lisdexamfetamine for the supported jurisdiction;
- formulation: the exact confirmed capsule or chewable formulation;
- schedule: 05:30 with the user's recorded breakfast instruction; and
- an approved appetite-support content rule is current.

Required distinctions:

- A 05:30 scheduled occurrence does not establish that the dose was taken.
- If a linked execution exists, Quick Help may say that the user logged it.
- If the user states in the current prompt that they took it, Quick Help may
  reflect that statement without silently adding an execution.
- The saved profile may select the reviewed lisdexamfetamine support rule only
  if identity, formulation, population, and jurisdiction match.
- The response still cannot claim the medicine or skipped lunch caused the
  slump.
- The response cannot advise another dose or answer a caffeine/interaction
  question.
- The content source and review date remain inspectable.

An appropriate response may combine the reviewed small food/water strategy,
bounded reassessment, user-recorded medicine instructions, and
pharmacist/prescriber follow-up. If the match or rule fails, the response uses
generic food/water support and the human/source route without
medication-specific claims.

## Day Context integration

Day Context may show, as distinct items:

- the planned medication occurrence;
- an explicit medication execution;
- the user's meal, caffeine, exercise, sleep, mood, energy, and focus records;
- a Quick Help action and reassessment; and
- the user's own possible-influence attribution.

Requirements:

- the schedule remains in the planned lane;
- the execution is referenced from Last Done rather than copied;
- private profile details are not repeated on every timeline entry;
- missing executions and missing context remain unknown;
- proximity does not create an influence attribution;
- descriptive summaries do not estimate treatment effect; and
- only user-selected records enter a Quick Help request.

## Privacy and security

### What private means

Medication Context is private to the signed-in user by product default. It is:

- always Sensitive;
- hidden from notification and push-payload details;
- excluded from assistance workspaces, trusted people, calendars,
  analytics content, advertising, and unrelated AI context;
- protected by account and tenant isolation;
- omitted from application/operational log content;
- disclosed externally only through a record-and-field-level preview;
- exportable and permanently deletable by the user; and
- unavailable to another account even on the same installation.

Private does not mean that the current local installation operator cannot read
the SQLite database or backups. The existing local-pilot operator boundary
must be disclosed wherever Medication Context is introduced. A hosted service
must likewise disclose authorised operational access; this document does not
promise end-to-end encryption.

### Storage and access gates

Before implementation:

- complete a health-data threat model and privacy impact assessment;
- define encryption in transit, at rest, and in backups;
- define key management and authorised operational access;
- prevent medication content from entering request, error, analytics, tracing,
  or support logs;
- require reauthentication for account export and destructive bulk deletion;
- define retention, backup expiry, restore, and deletion-completion behavior;
- test cross-account and cross-tenant denial;
- make access auditable without logging medicine content; and
- determine jurisdiction-specific lawful-processing and medical-product
  obligations.

### Notifications

- Medication reminders are off until the user enables them.
- A notification contains only generic private wording and an opaque
  identifier.
- The medicine name, strength, dose, schedule time, instructions, execution
  state, and action labels stay inside the authenticated application.
- A mirrored watch, car display, notification history, or lock screen receives
  no additional detail.
- Dismissing a reminder creates no execution and no missed-dose state.

### AI disclosure

Adding a medication profile does not grant an AI provider access.

For each AI-assisted request:

- the user sees the exact selected profile fields, current statement, and Day
  Context records that would leave the application;
- unneeded strength, dose, purpose, notes, history, and other medicines are
  excluded;
- consent applies to that request, not future sessions;
- the provider, retention terms, and available controls are disclosed;
- the prompt and response are not retained by Timemanager by default; and
- declining disclosure leaves the deterministic support and source links
  usable.

### Export and deletion

The user can export:

- profile and identity provenance;
- every regimen version and schedule slot;
- official-source links and content versions shown;
- linked execution identifiers and corrections;
- user-authored instructions, notes, and playbooks; and
- disclosure/access provenance required by the product contract.

The export is account-scoped, newly created without overwrite, and protected
according to the account-transfer contract. The UI warns that it contains
health information.

The user can delete:

- one medication profile and all its future occurrences;
- selected or all medication executions, subject to a clear relationship
  preview;
- user-authored instructions and notes;
- medication-specific Quick Help history if deliberately retained; and
- all Medication Context data.

Deletion must not silently remove independent Day Context records or rewrite
historical user statements. The preview explains which references will be
unlinked. Hosted backup expiry and deletion completion must be stated
precisely.

## Offline, time, and failure behavior

- The medication list, current regimen, source links already stored, reminders,
  and execution log remain inspectable without AI.
- A confirmed local edit survives restart.
- Failed saves remain failed and never update the displayed regimen.
- Retried mutations are idempotent.
- Schedule versions retain effective dates and timezones.
- Daylight-saving and travel never silently move a slot.
- An unavailable medicine dictionary prevents a new verified match but does
  not hide the user's free-text record.
- An unavailable or expired content rule prevents medication-specific support
  but does not block generic Quick Help or access to the stored profile.
- Provider failure never blocks urgent-support information.

## Accessibility and interaction

- Profile, schedule, execution, source, export, and deletion controls are
  keyboard and screen-reader operable.
- Medicine identity, formulation, provenance, and privacy state use text rather
  than colour alone.
- Similar medicine matches are presented for explicit selection and
  confirmation.
- User-entered and approved-source instructions are visually and semantically
  distinct.
- Schedule and execution use different labels in every view.
- The user can maintain the list without voice, AI, animation, or a network.
- Errors identify the affected field and preserve unsaved private text safely.

## Acceptance criteria

### Profile and schedule

- A user can create a private free-text medication profile without an AI
  disclosure or schedule.
- Optional strength, dose, formulation, instructions, and source provenance
  remain editable.
- Similar names and multiple formulations require explicit identity
  confirmation.
- Unsupported identities remain usable as free-text records but receive no
  medication-specific support.
- A schedule change creates a prospective regimen version and preserves
  history.
- Travel and timezone changes never move a medication time silently.

### Execution semantics

- A scheduled occurrence never creates an execution.
- A reminder delivery or dismissal never creates an execution.
- An absent execution remains unknown and is never labelled missed.
- Duplicate, backdated, corrected, and deleted executions follow the Last Done
  contract.
- Quick Help distinguishes schedule, logged execution, and the user's current
  statement.

### Support safety

- Medication-specific content renders only for an exact supported identity,
  formulation, population, jurisdiction, and current content version.
- Every medication-specific response exposes source and review provenance.
- Ambiguous, expired, withdrawn, mismatched, or unavailable rules fail closed.
- Dose, missed-dose, timing-change, interaction, and treatment prompts never
  produce a model-generated clinical decision.
- Constrained model phrasing cannot add actions or alter approved meaning.
- Urgent fixtures reach the reviewed urgent-support route.
- Generic Quick Help remains available without a medication profile.

### Privacy and security

- Medication Context cannot be changed from Sensitive to Standard.
- Cross-account and cross-tenant reads and mutations fail without revealing
  object existence.
- Notifications, push payloads, service-worker caches, analytics, errors,
  traces, and operational logs contain no medication content.
- Trusted people, calendars, and unrelated AI contexts receive no medication
  data.
- Every external request previews exact fields and requires confirmation.
- Export contains only the signed-in user's selected data and no secrets.
- Correction and deletion behave according to the disclosed retention and
  backup contract.
- Declining AI disclosure leaves non-AI behavior usable.

## Delivery order

1. Approve the clinical scope, privacy impact assessment, threat model,
   jurisdiction, and medicine-dictionary source.
2. Prototype profile entry, identity/formulation confirmation, schedule versus
   execution language, and privacy comprehension with synthetic data.
3. Define stable profile, regimen-version, schedule-slot, content-rule,
   provenance, export, and deletion contracts.
4. Implement the private medication list and schedule without reminders,
   advice, Day Context, or AI.
5. Link explicit executions through Last Done and validate exact missing-log
   semantics.
6. Validate security, account isolation, notifications, offline/timezone
   behavior, accessibility, export, and deletion.
7. Add official-source links and deterministic content resolution.
8. Add clinically approved non-dose support rules for one bounded medicine,
   formulation, population, and jurisdiction.
9. Integrate user-selected Day Context and Quick Help only after content and
   disclosure gates pass.
10. Consider constrained AI phrasing only after deterministic rendering and
    adversarial safety evaluation pass.

No medication-specific support is released until steps 1–8 pass. Interaction
checking, caregiver/clinician access, automatic imports, refill management,
passive sensing, treatment-response analysis, and clinical decision support
remain separate future product decisions.

## Evaluation

Evaluate:

- profile-entry time and identity/formulation error rate;
- user comprehension of user-entered versus verified/source-reviewed content;
- user comprehension of schedule versus execution versus reminder;
- whether the list reduces reliance on memory without displacing the label or
  professional instructions;
- false medication matches and fail-closed behavior;
- whether reviewed support is helpful without being interpreted as dose or
  treatment advice;
- user understanding of why content is unavailable or routed to a human;
- privacy comprehension, including the local-operator boundary;
- external disclosure opt-in and cancellation;
- correction, schedule-change, export, and deletion success;
- notification privacy across lock screens and mirrored devices; and
- whether users can stop using Medication Context without losing core
  Timemanager functionality.

Do not use number of medicines, schedule completeness, execution rate,
adherence, disclosure volume, AI use, or avoidance of professional care as
success metrics.

## Sources and review boundary

Sources checked on 2026-07-28:

- [FDA: Create and Keep a Medication List for Your Health](https://www.fda.gov/consumers/consumer-updates/create-and-keep-medication-list-your-health),
  for user-maintained name, strength, purpose, and instruction fields;
- [NICE NG87: ADHD diagnosis and management recommendations](https://www.nice.org.uk/guidance/ng87/chapter/recommendations),
  especially recommendations 1.7.2–1.7.3, 1.7.21, and 1.8.1–1.8.4 on
  professional medication management, individual variation, and monitoring;
- [NHS Specialist Pharmacy Service: advising on missed or delayed doses](https://sps.nhs.uk/articles/advising-on-missed-or-delayed-doses-of-medicines/),
  for the medicine-specific information and missed-dose boundary; and
- [ICO: what is special-category data?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/),
  for the health and inferred-health data boundary.

These sources support a private medication record, exact source matching, and
professional/medicine-information escalation. They do not validate
Timemanager's interface, establish that its support improves outcomes, make a
user-entered regimen clinically accurate, or authorise medication-specific
guidance in any release jurisdiction.
