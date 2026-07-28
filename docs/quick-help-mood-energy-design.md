# Future Quick Help, mood, energy, and focus support

Status: proposed Phase 4 product direction; not implemented or clinically
validated

Updated: 2026-07-28

## Purpose

**Quick Help** is a proposed, user-invoked surface for moments when the user
knows that something is wrong or difficult but has little capacity to work out
what to do next.

Its first job is to help the user choose one small, low-risk, reversible action
and decide when to reassess. It is not intended to identify the cause of a
feeling, optimise medication, diagnose a condition, provide crisis care, or
replace a clinician, pharmacist, dietitian, coach, or trusted person.

The useful core should work through short, reviewed, non-AI playbooks. An
optional AI integration may later accept a free-text question and phrase a
contextual response, but it remains disabled by default and subject to the
[optional AI guardrails](ai-body-doubling-and-voice-design.md). The existing
planner, Low Capacity view, timer, and recovery paths must remain useful
without Quick Help, a network connection, or an AI account.

Quick Help may integrate with the separate, user-owned
[Day Context history](day-context-history-requirements.md). That future
capability records mood, energy, focus ability, activities, and disruptions so
the user can inspect what happened without reconstructing the day from memory.
Quick Help remains usable without saving or disclosing that history.

The user may also add a private
[Medication Context profile and schedule](medication-context-support-requirements.md).
Quick Help may use explicitly selected medication context to choose exact,
current, clinically reviewed support content. It must not treat a schedule as
proof of ingestion or turn that context into model-generated dose, missed-dose,
interaction, or treatment advice.

## Evidence and status boundary

The feature is a **plausible product-design hypothesis**. Its exact prompts,
response structure, check-in vocabulary, and ability to help someone recover
from a difficult moment have not been validated.

The source material has three distinct roles:

- **Lived-experience input:** the user-supplied lunchtime-slump question below
  identifies a useful job and desired response shape. One person's example
  does not establish prevalence, causation, or efficacy.
- **Supported safety context:** clinical and medicine-information sources
  confirm that decreased appetite is a recognised lisdexamfetamine adverse
  effect, describe food-related strategies when weight loss is a concern, and
  identify medicine-use and urgent-symptom boundaries.
- **Plausible interaction design:** offering a few reversible actions followed
  by a bounded reassessment is a product hypothesis to test, not a clinical
  protocol.

Any shipped health-related playbook requires an identified clinical owner,
source review, jurisdiction review, versioning, and an expiry/re-review date.
An AI-generated answer does not become approved clinical content merely
because it cites a source.

## Product decisions

1. Quick Help is opened deliberately by the user. It is never an always-on
   monitor and never interrupts because the product inferred a mood or energy
   state.
2. The immediate objective is a safe next step, not a confident explanation
   of why the user feels a certain way.
3. The first useful version is a small, local, deterministic set of reviewed
   playbooks. Free-text AI is an optional later enhancement, not the
   foundation.
4. The response offers no more than three immediate choices and one explicit
   reassessment point. It does not create a new checklist to manage.
5. Suggestions remain suggestions. Starting a timer, saving a check-in,
   creating a task, changing Today, sending a message, or contacting another
   service requires the user's explicit choice and the normal confirmation
   boundary.
6. A one-off Quick Help interaction is ephemeral by default. The prompt,
   response, selected state, and outcome are not added to task history, AI
   memory, analytics content, or a helper workspace automatically.
7. Any saved mood, energy, focus, symptom, eating, caffeine, sleep,
   medication, activity, or disruption context belongs to Day Context, is
   **Sensitive** by default, and follows the strongest applicable privacy
   classification.
8. Quick Help may show clinically reviewed, source-provenanced, non-dose
   support matched through the Medication Context rules. It does not generate
   dose, missed-dose, interaction, supplement, caffeine, treatment, or
   medication-timing advice and never recommends taking more, taking less,
   skipping, doubling, stopping, or changing a medicine.
9. Quick Help does not diagnose a "crash", dehydration, low blood sugar,
   depression, mania, anxiety, burnout, or another cause from sparse context.
10. Severe physical symptoms, possible self-harm or harm to others, severe
    deterioration, or other urgent-risk signals leave the normal productivity
    flow and use reviewed urgent-support routing.
11. Mood and energy check-ins, if added, are self-reports rather than inferred
    measurements. They do not produce a wellness score, streak, diagnosis,
    productivity grade, or automatic priority.
12. A user can use Quick Help without saving a check-in and can use a manual
    check-in without sending it to an AI provider.

## Intended jobs

Quick Help may support:

- getting unstuck when the user cannot choose a next action;
- checking a few ordinary basics such as food, water, rest, sensory load,
  movement, or the immediate environment without claiming one is the cause;
- moving into Low Capacity mode or a short recovery break;
- turning an overwhelming task into one user-approved starting action;
- using a short timer and returning for a factual reassessment;
- opening a user-authored "what usually helps me" plan;
- deciding that the situation needs a pharmacist, clinician, trusted person,
  or urgent service rather than another productivity suggestion; and
- optionally recording what the user felt, tried, and later reported as useful.

## Non-goals

Quick Help must not become:

- a symptom checker, diagnostic chatbot, clinical decision-support system, or
  medication manager;
- a replacement for emergency, crisis, or professional care;
- passive mood recognition from voice, camera, typing, app usage, location,
  wearable signals, or task completion;
- a hidden recommendation engine that changes the user's plan;
- a feed of generic wellness content or an engagement surface that encourages
  repeated disclosure;
- an adherence, calorie, hydration, sleep, mood, or productivity score;
- a tool for a trusted person, employer, clinician, or insurer to monitor the
  user;
- evidence that a particular food, activity, medicine, routine, or suggestion
  caused a later change; or
- a way to conceal cloud AI processing inside an otherwise local application.

## Core interaction

### 1. Deliberate entry

The user opens **Quick Help** from Today, Low Capacity, or Focus. The entry
point uses neutral wording such as "Need a small reset?" rather than detecting
or announcing that the user appears tired, distressed, or unproductive.

The first screen provides two equivalent routes:

- choose a short state such as **stuck**, **overwhelmed**, **low energy**,
  **restless**, or **something feels wrong**; or
- ask a short free-text question when the optional AI connector is enabled.

No state is preselected. Text and manual choices remain available without
voice.

### 2. Minimum necessary context

Ask only questions that materially change the next safe route. Do not turn the
interaction into an assessment questionnaire.

Examples of useful context are:

- what the user wants help with right now;
- whether a severe or urgent symptom is present;
- which ordinary basics the user already knows may be relevant;
- whether they want a two-minute action, a short break, or human help; and
- whether they want to use a previously saved personal playbook.

Medication names, doses, diagnoses, detailed symptom histories, and full task
history are not required for the ordinary productivity route. The user may
explicitly select the minimum fields from a private Medication Context profile
when medication-specific reviewed support is relevant. If the user's text
already contains health details, the system treats the whole interaction as
Sensitive rather than asking for more.

### 3. Safety route before suggestions

A deterministic, reviewed safety layer runs before any generative response.
It identifies requests that are outside Quick Help, including:

- changing, adding, skipping, or repeating medication;
- interpreting a possible medication interaction or adverse reaction;
- chest pain, fainting, serious breathing difficulty, a markedly fast or
  irregular heartbeat, or another configured urgent physical signal;
- thoughts or plans of self-harm, suicide, or harm to another person;
- severe confusion, loss of contact with reality, inability to stay safe, or
  another configured acute mental-health signal; and
- an immediate safeguarding risk.

The urgent route gives concise, jurisdiction-appropriate, clinically reviewed
instructions to seek human help. It must not depend on a model inventing a
local telephone number, and it must be tested for the jurisdictions in which
the feature is released. The user can always open the urgent-support route
directly; keyword detection is not presented as a complete risk assessment.

### 4. Acknowledge facts and uncertainty

The response reflects only information the user supplied. It distinguishes:

- **observed input:** "You said you have not eaten since breakfast";
- **a possibility:** "That can be one contributor to feeling depleted"; and
- **an unknown:** "This alone does not establish what is causing the slump."

It must not silently promote a possibility into wording such as "the most
likely cause" unless an approved clinical protocol explicitly supports that
conclusion for the collected context.

### 5. Offer a very small response

The primary response contains:

1. one sentence acknowledging the situation and uncertainty;
2. one recommended low-effort option plus at most two alternatives;
3. an explicit **Try this** action;
4. a bounded **Check again** point; and
5. a visible **Get human help** path when health or safety is in scope.

Examples of non-clinical actions include switching to Low Capacity, reducing
sensory input, choosing a familiar easy meal or drink, stepping away briefly,
getting ordinary daylight or movement, opening a window, or defining the first
visible action for a task. Exact health-related wording and food examples must
come from the reviewed content library rather than ad hoc model reasoning.

The interface never requires the user to do every suggestion. "None of these"
and "Stop" are first-class choices.

### 6. Reassess without claiming an outcome

If the user chooses, Quick Help can start a short local timer. At the agreed
point it asks a factual question such as:

> Is this better, the same, worse, or do you want human help?

No answer is preselected. A missing response means only that no response was
recorded. It does not mean the suggestion failed, the user deteriorated, or the
action was not taken.

## User-supplied lunchtime-slump scenario

The supplied example was:

> Best remedies for lunch time slump for ADHD. Had Vyvanse at 5:30 with
> breakfast, haven't had lunch.

This is useful because it combines a low-capacity moment, an ordinary unmet
need, a named medicine, and the risk of interpreting a feeling as a medication
"crash".

### Required handling

For this scenario, Quick Help should:

- reflect that the user reports having had breakfast, taken a named medicine,
  and not eaten lunch;
- avoid asserting that skipped lunch or the medicine is the cause;
- offer a small, familiar food-and-water action only as a low-risk first
  option, with alternatives if eating is difficult or inappropriate for the
  user's existing care instructions;
- keep examples short and practical, such as a familiar sandwich, yoghurt and
  fruit, eggs on toast, or a tolerated smoothie, subject to clinical content
  review;
- provide a bounded reassessment rather than promising that the action will
  fix the slump;
- state that Quick Help cannot recommend an extra dose or any medicine change;
- route questions about caffeine, interactions, or recurring medication
  effects to the user's medicine information, pharmacist, or prescriber; and
- show the reviewed urgent route for symptoms such as chest pain, fainting,
  serious breathing difficulty, or a fast or irregular heartbeat.

If the user has a private Medication Context profile:

- the saved 05:30 schedule remains a plan and does not prove the medicine was
  taken;
- a linked explicit execution may be reported as logged;
- the profile may select lisdexamfetamine-specific support only when identity,
  formulation, population, jurisdiction, and content currency match; and
- unsupported or ambiguous matching falls back to generic support plus the
  medicine-information/pharmacist/prescriber route.

### Illustrative response shape

The following is a content-review candidate, not approved shipped copy:

> You have not eaten since breakfast. I cannot tell from that alone what is
> causing the slump, but food and water are a small first thing you can check.
>
> **Try this:** have water and one familiar, easy food you normally tolerate.
> Starting small is fine if a full meal feels difficult.
>
> **Check again:** reassess after a short break. If this keeps happening,
> discuss the pattern with your prescriber rather than changing your medicine
> yourself.
>
> Quick Help cannot tell you to take more, skip, or change Vyvanse. Seek urgent
> medical help for chest pain, fainting, serious trouble breathing, or a fast
> or irregular heartbeat.

Before release, a qualified reviewer must decide whether this exact response,
its food examples, its reassessment interval, and its escalation wording are
appropriate for each supported jurisdiction. The product must not generate a
more specific medicine answer merely because the user provided a dose or time.

## Day Context and personal playbooks

The canonical tracking requirements are defined in
[Day Context and within-day history](day-context-history-requirements.md).
That feature lets the user explicitly record:

- mood, energy, focus ability, and overload/capacity check-ins;
- food, caffeine, exercise, rest, and other user-selected activities;
- distractions, interruptions, task switches, emotional or social events, and
  environmental changes;
- existing Last Done executions and confirmed focus outcomes by reference;
- a private medication schedule in the planned lane and explicit medication
  executions as separately labelled events; and
- the user's own editable belief that an event may have helped, made something
  harder, had no noticeable effect, or remains unclear.

Quick Help may offer **Save this check-in**, **Log context**, or **Show what
happened around this time**, but only after the user chooses the action. It does
not save the conversation, inspect the whole timeline, or send history to an AI
provider automatically.

Timeline answers remain descriptive:

- "You recorded low energy on four afternoons this month" is a count;
- "An interruption was logged 38 minutes before this check-in" is temporal
  context;
- "You marked that interruption as possibly making focus harder" is a
  user-authored attribution;
- "Low energy was caused by your medicine" is an unsupported causal claim; and
- a missing activity or reassessment is unknown, not a negative outcome.

The user may save a short, editable personal playbook such as:

> When I notice an afternoon slump, first check whether I have eaten and had
> water. Then choose Low Capacity for 20 minutes and reassess.

The user owns the wording and can disable or delete it. Timemanager may offer a
draft, but the user confirms every saved step. A playbook does not become
medical advice, and a medicine-specific playbook requires the same clinical
review as other health content.

Personalisation may rank options the user explicitly marked as preferred. It
must not infer a treatment response, turn co-occurrence into causation, or learn
a hidden intervention policy from Sensitive history without a separate
product, clinical-safety, privacy, and consent decision.

## Information and privacy boundaries

### Conceptual records

The following names describe product concepts, not an approved database schema:

- **Quick Help interaction:** an ephemeral request, route, content version, and
  optional chosen action;
- **reassessment:** a later user report linked to a check-in;
- **personal playbook:** a user-approved sequence of preferred actions; and
- **content rule:** reviewed copy with source provenance, jurisdiction,
  reviewer, version, and review/expiry dates.

State check-ins, context events, attributions, and timeline summaries use the
concepts defined in the Day Context requirements.

No schema should be added until retention, deletion, export, migration, and
hosted-sync behavior are approved together.

### Sensitive by default

A Quick Help interaction is Sensitive when it contains or solicits mood,
energy, focus, eating, caffeine, sleep, activity, disruption, symptoms,
medication, diagnosis, crisis, or other health context.

Sensitive content:

- is not included in notification text or push payloads;
- is not sent to helpers, calendars, analytics-content systems, advertising,
  or data brokers;
- is not added to general AI memory or task context;
- is not exposed through a general planning-support permission;
- is retrieved only inside the authenticated application;
- requires explicit disclosure before being sent to a cloud AI provider; and
- has user-visible export, correction, retention, and deletion behavior before
  hosted release.

Operational metrics may record that a route completed, failed, or was stopped,
but must not include the prompt, selected mood, medicine name, symptom, chosen
food, playbook text, or response content.

### Optional AI boundary

When free-text AI is enabled:

- disclose the provider, data sent, retention terms, and available data
  controls before the first use;
- send only the current user-approved prompt and the minimum content rules
  needed for the response;
- do not attach task history, Day Context history, medication history,
  calendar, helper data, or AI memory by default;
- disclose and preview every selected Medication Context field for the current
  request;
- keep credentials server-side and issue only short-lived client
  authorization;
- show which parts are reviewed source content and which parts were generated;
- do not retain raw voice, transcripts, prompts, or responses by default;
- degrade to the local reviewed playbooks when the provider is unavailable;
  and
- never let provider failure block the user from reaching urgent-support
  information.

## Safety architecture

The safety design separates responsibilities:

```text
User input
    |
    v
Reviewed urgent/out-of-scope routing
    | ordinary route
    v
Versioned local content and allowed-action catalogue
    |
    v
Optional AI phrasing with narrow context
    |
    v
Rendered uncertainty, actions, sources, and reassessment
    |
    v
Explicit user choice before any save or mutation
```

The model must not be the only mechanism that:

- recognises urgent language;
- decides whether medicine advice is allowed;
- supplies emergency or crisis contact details;
- chooses which personal data to send externally;
- determines whether an action mutates saved data; or
- produces the source citation attached to approved clinical content.

Health-related content rules fail closed when they are expired, unavailable,
unsupported in the user's jurisdiction, or missing required review metadata.
The fallback is a concise scope statement and human-help route, not an
uncited generated answer.

## Accessibility and interaction requirements

- Quick Help is keyboard and screen-reader operable.
- State and outcome choices use text; colour and emoji are supplementary.
- The primary surface presents at most three actions at once.
- "Stop", "None of these", "Back", and "Get human help" remain visible.
- The UI does not use shame, forced urgency, streak loss, celebratory
  overstatement, or dependency-oriented language.
- A timer or reassessment prompt respects reduced-motion, sound, haptic, and
  notification preferences.
- Dismissing Quick Help causes no plan change and no negative state.
- The static path remains usable without sound, voice, AI, or a network
  connection.

## Acceptance gates

### Product and usability

- Users can reach a useful non-AI action without typing sensitive details.
- The user can stop without saving data or changing the plan.
- The first response contains at most three actions and one reassessment point.
- Users can distinguish a reported fact, a possibility, and an unknown.
- Users understand that a suggestion is optional and not a diagnosis.
- A missing reassessment remains unknown.
- Day Context history is separately opt-in and does not block ephemeral use.
- Low Capacity and normal planning remain fully useful without Quick Help.

### Safety

- Medication prompts never produce a dose or treatment change.
- Medication-specific support renders only through an exact, current,
  clinically reviewed Medication Context rule; unsupported cases fail closed.
- Caffeine, interaction, supplement, adverse-reaction, and recurring-effect
  questions use the approved human/source route rather than free model advice.
- Urgent physical, mental-health, self-harm, harm-to-others, and safeguarding
  fixtures route to reviewed support content before productivity suggestions.
- The urgent route works when the AI provider is unavailable.
- Clinical reviewers approve health content, red-flag wording, source
  provenance, jurisdiction scope, and review dates before release.
- Adversarial and ambiguous prompts are evaluated for false reassurance,
  overconfident causation, unsupported medicine advice, and missed escalation.

### Privacy and security

- A one-off interaction creates no durable personal record by default.
- Saving a check-in is an explicit, CSRF-protected, account-scoped action.
- Sensitive content is absent from push, mirrored notifications, analytics
  content, helper contexts, and unrelated AI contexts.
- AI disclosure and consent precede the first external transfer.
- Export, correction, retention, deletion, and hosted backup expiry are
  documented and tested for saved records.
- Cross-user reads and mutations fail without revealing object existence.

### Resilience and provenance

- Local playbooks work offline.
- Every health-related content block exposes its source/review provenance
  inside the product.
- Expired or unsupported health content fails closed.
- Retried saves and reassessments are idempotent.
- Lost connectivity cannot turn an unsaved check-in into a successful record.

## Delivery order

1. Prototype the ephemeral interaction using synthetic, non-medical scenarios
   and local static playbooks.
2. Validate cognitive load, wording, stop behavior, and usefulness with
   intended users.
3. Define the content-rule format, provenance, expiry, jurisdiction, and
   fail-closed behavior.
4. Obtain clinical-safety and privacy review before adding any health-specific
   playbook or live medication scenario.
5. Validate urgent routing with jurisdiction-specific fixtures and human
   review.
6. Integrate opt-in Day Context check-ins only after its export, deletion,
   retention, account-isolation, and Sensitive-data gates are complete.
7. Integrate private Medication Context only after its profile, identity,
   content, clinical-safety, and privacy gates pass.
8. Consider optional AI phrasing only after the non-AI flow and safety layer
   pass their gates.
9. Consider user-authored personal playbooks only after Day Context capture,
   timeline, and interpretation behavior are usability-tested.
10. Treat passive sensing, automatic health inference, clinician/helper access,
   and medicine-response analysis as separate future decisions, not incremental
   settings.

Quick Help remains deferred Phase 4 work. This document does not authorise
implementation in the local pilot or Phase 3 hosted release.

## Evaluation

Evaluate:

- time and interactions needed to choose one action;
- whether the response reduces choice overload or adds another decision burden;
- user comprehension of uncertainty and scope;
- the rate at which users choose stop, human help, or none of the suggestions;
- whether the reassessment feels supportive rather than intrusive;
- false reassurance and unnecessary escalation rates in reviewed fixtures;
- whether users understand ephemeral versus saved behavior;
- whether optional history helps reflection without encouraging monitoring,
  self-blame, or overinterpretation; and
- privacy comprehension before any AI transfer or saved check-in.

Do not use disclosure volume, number of check-ins, time spent in Quick Help,
streaks, medicine adherence, productivity, or avoidance of human support as
success metrics.

## Sources and review boundary

Sources checked on 2026-07-28:

- [NICE NG87: ADHD diagnosis and management recommendations](https://www.nice.org.uk/guidance/ng87/chapter/recommendations),
  especially recommendations 1.8.1–1.8.8 on monitoring adverse effects and
  weight-related strategies;
- [MedlinePlus: lisdexamfetamine drug information](https://medlineplus.gov/druginfo/meds/a607047.html),
  for recognised adverse effects, taking the medicine as directed, and urgent
  cardiovascular symptoms; and
- [BNSSG national shared care protocol: lisdexamfetamine for adults, version
  12](https://remedy.bnssg.icb.nhs.uk/media/zzupkk4o/lisdexamfetamine-adult-scp-new-template-final-v12-002.pdf),
  the current successor found during review to the version 11 protocol cited
  in the supplied example.

These sources support a cautious medicine-information and escalation boundary.
They do not establish that the illustrative Quick Help response is safe for
every person, that food or water is the cause or remedy for a particular
slump, or that Timemanager can monitor or manage ADHD, mood, energy, or
medication effects effectively.
