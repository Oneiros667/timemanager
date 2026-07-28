# Delivery and validation plan

Status: proposed gated delivery plan; no production authorization

Updated: 2026-07-28

## Status model

Each capability has four independent questions:

1. Is it documented?
2. Is it implemented and technically verified?
3. Has it passed human, accessibility, safety, clinical, privacy, legal, and
   operational evidence gates?
4. Is the exact build authorized for the exact market and pilot?

Passing one does not imply the next.

## Current baseline

As of 2026-07-28:

- the separate Timemanager Kids application does not exist;
- no real child account, guardian relationship, school connection,
  medication workflow, or hosted child service exists;
- the adult repository has implemented planning components that may inform
  future work but do not provide child authorization;
- `/prototypes/calm-break` is a synthetic, disabled-by-default, no-store
  same-device interaction;
- `/prototypes/school-support-share` is a synthetic, disabled-by-default,
  no-store disclosure/help-signal interaction; and
- no usability findings with children have been recorded.

## Milestones

### K0 — Product and risk definition

Deliver:

- complete documentation set;
- child-best-interests assessment;
- initial DPIA/data inventory;
- unsafe-family/coercion and safeguarding threat models;
- age/market/authority matrix;
- clinical boundary and medication hazard analysis;
- product topology and no-cross-product-access decision;
- research protocol drafts; and
- accountable product, privacy, safety, security, accessibility, clinical, and
  legal owners.

Exit:

- every planned data field has purpose, classification, role, retention, and
  deletion behavior;
- no unresolved critical product-policy conflict;
- independent review agrees which K1 prototypes may be tested synthetically.

### K1 — Synthetic child/guardian prototype

Scope:

- guardian setup using fictional roles;
- child Today with one anchor and up to three options;
- task responses and visible adult attribution;
- Low Capacity;
- calm-break agreement;
- low-language child help signals;
- child-visible `who can see` history; and
- same-device role switching and reset.

Prohibitions:

- no persistent personal data;
- no real child account or invitation;
- no external messaging/calendar/notification;
- no school, diagnosis, medication, family-conflict, or location data;
- no AI or voice.

Exit:

- synthetic data only verified;
- keyboard, screen reader, zoom/reflow, reduced-motion, and real-device checks;
- formative research across age bands under approved protocol;
- no unresolved blocking comprehension, coercion, distress, or accessibility
  findings.

K1 does not authorize K2.

### K2 — Foundational guardian-operated private pilot

Scope:

- geographically limited hosted child workspaces;
- guardian verification and protected recovery;
- child Today/Later/fixed commitments/capture;
- child-visible guardian changes;
- Low Capacity, calm break, task help requests;
- no external adult beyond verified guardian;
- export, correction, revocation, deletion, retention, and incident response.

Prohibitions:

- no school/carer sharing;
- no medication/health structured data;
- no external calendar;
- no AI, voice, third-party analytics, or precise location.

Exit:

- exact market legal/privacy authorization;
- child-best-interests and DPIA approval;
- server authorization and cross-workspace negative tests;
- external penetration test;
- backup/restore/deletion/recovery evidence;
- incident exercise;
- supervised limited pilot evidence and stop criteria review.

### K3 — Verified school/carer communication pilot

Scope:

- verified organization and named roles;
- field-level classroom/carer support cards;
- child signals with delivery/acknowledgement evidence;
- neutral daily feedback;
- role expiry, termination, correction, dispute, and audit.

Still excluded:

- medication administration;
- broad diagnosis/history disclosure;
- behavior scoring;
- open messaging/files;
- AI.

Exit:

- school/education record legal and contract review;
- role verification and termination evidence;
- notification/outbox failure tests;
- unsafe-school/staff misuse threat-model tests;
- child comprehension of recipient and delivery states;
- school transfer and revocation drills;
- authorized named institutions and market only.

### K4 — Medication administration pilot

Scope is limited to a separately authorized designated school-health workflow.

Prerequisites:

- clinical safety case and accountable clinical owner;
- exact medication/formulation/source model;
- verified prescriber/pharmacy instruction provenance;
- school administration policy integration;
- guardian authority and child notice;
- Protected/Sensitive data isolation;
- discrepancy, correction, unknown, and fail-closed behavior;
- no-dose-advice fixtures;
- applicable health/education/child-data legal authorization; and
- incident and urgent human-routing procedures.

Exit requires clinical, school-health, privacy, security, legal, and
operational authorization for the exact build. Planning, K2, or K3 evidence
cannot substitute.

### K5 — Broader markets and optional surfaces

Potentially:

- additional countries;
- external calendar;
- native mobile/wearable;
- reviewed child Quick Help;
- printable/ambient surfaces; and
- optional AI or voice only after a new product decision.

Every surface has separate data-flow, processor, accessibility, safety, and
market gates.

## Verification layers

### Automated

- unit tests for state and policy rules;
- workspace/tenant isolation and guessed-ID negative tests;
- role/purpose/field/expiry authorization matrix tests;
- CSRF and session security;
- concurrency, revision, and idempotency;
- delivery-state and provider-failure fixtures;
- migration upgrade/downgrade/fail-closed checks;
- export/import/deletion scope and secret exclusion;
- sensitive-data sink tests for notifications, analytics, logs, traces, cache,
  support, search, and AI;
- medication no-advice and missing-is-unknown fixtures;
- contrast, focus semantics, accessible names, and reduced-motion checks; and
- dependency/software supply chain gates.

### Manual technical

- assistive-technology matrix;
- real-device layouts and touch;
- network loss, provider outage, clock/timezone changes;
- compromised/expired role and account recovery;
- school transfer and staff role termination;
- backup/restore and deletion;
- notification lock-screen privacy;
- operational dashboards without content leakage; and
- penetration/security review.

### Human evidence

- children in each age band;
- speaking and nonspeaking children;
- children with varied reading, cognitive, sensory, motor, vision, hearing, and
  communication needs;
- guardians with different family structures and access constraints;
- teachers, carers, school health staff, privacy/safeguarding staff;
- accessibility, child-development, clinical, security, privacy, and legal
  reviewers.

Implementation evidence and participant evidence are stored separately.

## Core acceptance scenarios

### Child planning

- capture a thought without classifying it;
- identify the next fixed commitment and chosen anchor;
- predict whether a new action enters Today, overflow, or Later;
- choose `not now` without a penalty;
- ask a guardian for help;
- recover after a week away without an overdue wall;
- restore an accidentally dropped task; and
- use Low Capacity without losing access to help.

### Calm break

- guardian proposes music/grounding/custom support;
- child understands that options are choices;
- child challenges the plan;
- no forced timer or completion gate appears;
- return/check-in does not create a score.

### Child communication

- child selects `I'm overwhelmed` without typing;
- identifies the exact recipient;
- cancels before send;
- distinguishes queued, delivered, seen, unavailable, and failed;
- uses the nearby-human fallback when delivery fails;
- repeats a signal without disciplinary escalation.

### School sharing

- guardian selects one teacher and only classroom supports;
- medication remains unavailable;
- scope expansion requires a new preview;
- child sees who can access what;
- teacher submits a neutral observation;
- child/guardian requests correction;
- teacher role ends and access stops;
- old school cannot access after transfer.

### Medication

- teacher cannot read medication fields;
- designated health role sees only the approved plan;
- planned time does not show `taken`;
- missing administration remains unknown;
- duplicate/discrepant record requires review;
- no prompt produces dose advice;
- expired clinical content fails closed;
- correction preserves provenance.

### Unsafe and failure cases

- false guardian claim;
- conflicting guardian claims;
- unsafe adult may observe the shared device;
- revoked invitation replay;
- role expired during active session;
- provider accepted but did not deliver a message;
- notification mirrored to locked device;
- offline save fails;
- cross-workspace ID guessed;
- export requested during dispute;
- deletion requested while a narrow record hold exists;
- support operator attempts unapproved content access.

## Provisional usability gates

Thresholds are hypotheses to refine with baseline evidence:

- at least 90% of participants in each tested age band identify the next fixed
  commitment and primary action without prompting;
- every participant finds the help signal from Today and Low Capacity;
- every participant distinguishes `not sent`, `delivered`, and
  `acknowledged`;
- at least 90% identify who will receive a disclosure before confirming;
- no participant believes a calm-break support is mandatory;
- no participant believes missing medication history proves a missed dose;
- median cognitive effort no greater than 3/7 for core child flows;
- zero critical child-safety, cross-workspace, hidden-sharing, or
  medication-advice failures;
- successful recovery from every consequential ordinary action; and
- no keyboard trap, inaccessible primary action, or content exposure in
  assistive-technology/device tests.

These thresholds do not establish clinical benefit.

## Success and guardrail measures

Evaluate:

- time to understand what happens next;
- time and effort to express a support need;
- successful adult acknowledgement and real-world support under controlled
  pilot conditions;
- child comprehension of roles, sharing, and message state;
- recovery after interruption or absence;
- planning burden for child and guardian;
- school feedback burden and correction rate;
- reported autonomy, pressure, shame, sensory load, and trust;
- accidental disclosure and access-revocation latency;
- notification dismissal/muting and delivery failure; and
- abandonment and safe return after non-use.

Do not optimize:

- task completion count;
- medication adherence;
- compliance/behavior score;
- app opens, time in app, message volume, or disclosure volume;
- adult response surveillance;
- school performance ranking; or
- reduced use of human support.

## Evidence artifacts

Every milestone stores:

- build/commit identifier;
- exact enabled market and feature flags;
- test and accessibility results;
- threat model and risk acceptance;
- DPIA/best-interests assessment version;
- clinical safety record where applicable;
- legal/privacy authorization;
- participant protocol and de-identified findings;
- security test and remediation;
- backup/restore/deletion/incident exercise;
- open limitations and stop criteria; and
- accountable authorization signatures/records.

Artifacts are immutable for the reviewed build. Runtime, policy, data model, or
feature-flag changes invalidate build-bound authorization and require the
defined re-review.

## Stop and rollback conditions

Stop the pilot or affected feature for:

- wrong-person, wrong-workspace, or out-of-scope access;
- guardian/school role verification failure;
- sensitive content in an unauthorized sink;
- medication advice or false administration state;
- child signal falsely reporting delivery/acknowledgement;
- coercive, punitive, covert-monitoring, or safeguarding misuse;
- critical accessibility failure blocking help;
- missing or expired market authorization;
- incident-response inability;
- deletion/revocation failure; or
- evidence that the child cannot understand or safely use the flow.

Rollback must preserve evidence, prevent new access, communicate limitations,
and avoid deleting records needed for incident, correction, or rights handling.

## Immediate next steps

1. Obtain product-owner approval of the separate-app boundary and explicit
   exclusions.
2. Run an independent child-best-interests and data inventory workshop.
3. Create child-specific unsafe-family, school misuse, safeguarding, and
   medication hazard analyses.
4. Define the K1 synthetic scenarios and research protocol.
5. Design low-fidelity age-band variants for Today, help signals, calm break,
   and `who can see`.
6. Recruit child-development, accessibility, privacy, safeguarding, education,
   and clinical reviewers before participant work.
7. Do not create persistent child schemas or real invitations until K0 exits.
