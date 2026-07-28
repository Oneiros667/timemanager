# Timemanager Kids functional requirements

Status: proposed requirements; no real child-data implementation is authorized

Updated: 2026-07-28

## Requirement language

`MUST`, `MUST NOT`, `SHOULD`, and `MAY` express product requirements. IDs are
stable traceability keys; renumbering a requirement requires updating tests,
risk records, and delivery gates that cite it.

## Workspace and onboarding

- **KID-ID-01:** A guardian MUST create the child workspace. A child MUST NOT
  independently register using email, payment, social login, or app-store
  credentials.
- **KID-ID-02:** Workspace creation MUST remain pending until the required
  guardian authority, child age band, launch market, notice, and consent/legal
  basis checks pass.
- **KID-ID-03:** The system MUST store age band rather than full birth date
  unless a market requirement or approved feature needs the exact date.
- **KID-ID-04:** The child MUST receive an age-appropriate explanation of the
  workspace, visible adult roles, information use, and available concern route
  before entering personal information.
- **KID-ID-05:** The child MUST be able to choose tested communication,
  reading, contrast, motion, sound, and support preferences without changing
  their legal age or authority.
- **KID-ID-06:** A birthday MUST NOT silently change roles, consent, privacy,
  sharing, retention, or product ownership.
- **KID-ID-07:** The system MUST support a reviewed transition process for age
  18. It MUST NOT convert the child workspace into an adult account in place.
- **KID-ID-08:** Billing status MUST NOT be accepted as evidence of guardian
  identity or authority.

## Daily planning

- **KID-PLAN-01:** The child Today view MUST distinguish fixed commitments from
  flexible actions in storage, semantics, and presentation.
- **KID-PLAN-02:** The default active plan MUST contain at most one agreed
  anchor and three optional active actions until age-band research authorizes a
  different default.
- **KID-PLAN-03:** Excess captures MUST be preserved as visible recoverable
  overflow or Later items. They MUST NOT be rejected, lost, or promoted
  silently.
- **KID-PLAN-04:** Capture MUST require only a short title or one validated
  low-language selection.
- **KID-PLAN-05:** A guardian-created action MUST show who created it and why
  it is relevant in language the child can understand.
- **KID-PLAN-06:** The child MUST be able to choose `done`, `not now`, `need
  help`, or `talk about this` for an ordinary shared action.
- **KID-PLAN-07:** `Not now` MUST NOT create a compliance failure, score,
  punishment, public flag, or automatic diagnosis.
- **KID-PLAN-08:** A task SHOULD expose one concrete next action and an optional
  definition of done before showing steps, projects, blockers, or provenance.
- **KID-PLAN-09:** Complex work MUST use no deeper than
  project/outcome → task → optional step in the first release.
- **KID-PLAN-10:** Preferred order, prerequisite, external waiting, workflow
  status, and Today placement MUST remain distinct.
- **KID-PLAN-11:** Resolving a blocker MUST NOT add an item to Today
  automatically.
- **KID-PLAN-12:** Completing all linked tasks MUST NOT automatically claim
  that a project outcome was achieved.
- **KID-PLAN-13:** Drop MUST be confirmed, reversible, and child/guardian
  visible. Restore MUST default to Later rather than silently consume Today
  capacity.
- **KID-PLAN-14:** Draft text MUST survive reload, navigation, and temporary
  network failure according to a documented retention boundary.
- **KID-PLAN-15:** Conflicting adult and child edits MUST show both versions
  and require an authorized resolution; latest-write-wins MUST NOT silently
  erase either person's contribution.

## Fixed commitments and transitions

- **KID-TIME-01:** A fixed commitment MUST record its time, timezone, source,
  responsible adult, and current sync state.
- **KID-TIME-02:** Preparation, travel, and leave-by cues MUST remain local
  overlays unless an authorized external-calendar write is separately
  confirmed.
- **KID-TIME-03:** Flexible tasks MUST NOT be displayed as compulsory calendar
  events.
- **KID-TIME-04:** External event creation, modification, cancellation, or
  attendee change MUST show a full preview and require an authorized guardian
  confirmation.
- **KID-TIME-05:** The active day MUST remain readable when a calendar or
  notification provider is unavailable.
- **KID-TIME-06:** Time calculations MUST preserve timezone and daylight-saving
  meaning. Travel MUST NOT rewrite historical local times.

## Low Capacity and recovery

- **KID-LOW-01:** Low Capacity MUST show the next fixed commitment, one safe
  actionable item, capture, and the child help/communication route.
- **KID-LOW-02:** Entering Low Capacity MUST NOT complete, drop, reschedule,
  disclose, reprioritize, or hide a safety-critical commitment.
- **KID-LOW-03:** The interface MUST state that additional work is hidden and
  unchanged and offer a clear return to the full view.
- **KID-LOW-04:** Recovery after absence MUST surface consequence-bearing
  decisions without automatically rolling every unfinished item forward.
- **KID-LOW-05:** Recovery copy MUST describe facts and choices rather than
  debt, failure, laziness, disappointment, or lost streaks.

## Calm breaks

- **KID-CALM-01:** The child-facing name MUST be neutral and supportive, such as
  `calm break`; the product MUST NOT frame it as punishment or isolation.
- **KID-CALM-02:** The guardian MAY propose supports including grounding,
  breathing, mindfulness, music, water, food, a quiet activity, sensory tools,
  or a custom option.
- **KID-CALM-03:** Supports MUST be presented as choices. The system MUST NOT
  require completion of a calming checklist before the child can return.
- **KID-CALM-04:** The plan MUST show the reason, the proposed options, the
  check-in agreement, and how to ask for help or challenge the plan.
- **KID-CALM-05:** The child MUST be able to respond `ready`, `need help`, or
  `talk about the plan`.
- **KID-CALM-06:** The system MUST NOT use a forced countdown, locked screen,
  confinement instruction, escalating penalty, compliance score, or automatic
  failure report.
- **KID-CALM-07:** The feature MUST NOT be used to authorize seclusion,
  restraint, withdrawal of necessary supervision, or emergency management.
- **KID-CALM-08:** Calm-break history, if retained, MUST record the agreed plan
  and factual responses, not inferred emotional state or adult ratings.

## Child-initiated communication

- **KID-COMM-01:** A persistent, low-language help route MUST be reachable from
  Today, Low Capacity, focus, and calm-break surfaces.
- **KID-COMM-02:** The initial tested messages MUST include:
  `I'm overwhelmed`, `I need a quiet space`, `I can't talk right now`,
  `Please get my trusted adult`, and `Something else—please check in with me`.
- **KID-COMM-03:** The child MUST NOT need to disclose a diagnosis or compose a
  free-text explanation to use a support signal.
- **KID-COMM-04:** Before confirmation, the interface MUST show the exact
  intended recipient or state clearly that no recipient is available.
- **KID-COMM-05:** A message MUST have separate states for local draft, queued,
  accepted by server, delivered to recipient device/account, acknowledged,
  cancelled, expired, unavailable, and failed.
- **KID-COMM-06:** The interface MUST NOT say or imply that an adult received,
  saw, or acted on a message without evidence for that state.
- **KID-COMM-07:** The child MUST be able to cancel before server acceptance.
  Later withdrawal MUST be recorded without pretending already delivered
  content was unseen.
- **KID-COMM-08:** When delivery is unavailable or times out, the app MUST show
  an age-appropriate nearby-human fallback and the school's approved emergency
  process.
- **KID-COMM-09:** The feature MUST NOT claim to be a crisis or safeguarding
  response service.
- **KID-COMM-10:** Message use, frequency, timing, wording, and response time
  MUST NOT feed diagnosis, behaviour scores, discipline, attendance decisions,
  targeted content, or teacher performance measures.
- **KID-COMM-11:** Validated symbol, picture, switch-access, and
  augmentative/alternative communication options SHOULD be available without
  making spoken language mandatory.

## School and carer relationships

- **KID-SCHOOL-01:** “School” MUST NOT be a single recipient. Every connection
  MUST identify a verified organization, named adult, current role, purpose,
  field scope, start, and expiry.
- **KID-SCHOOL-02:** A class teacher MAY receive only selected classroom
  supports, relevant fixed commitments, child-approved help signals, and
  neutral feedback fields.
- **KID-SCHOOL-03:** A designated carer MAY receive only the support fields
  needed for the named care period and purpose.
- **KID-SCHOOL-04:** A teacher or carer MUST NOT automatically receive diagnosis,
  medication, family notes, private task history, mood history, other adults'
  notes, or messages outside their scope.
- **KID-SCHOOL-05:** School access MUST expire at the earliest of its explicit
  expiry, role end, school transfer, guardian revocation, organization
  de-verification, or safety suspension.
- **KID-SCHOOL-06:** The system MUST re-verify continuing school role before
  renewal. Email-domain possession alone MUST NOT prove employment or current
  responsibility for the child.
- **KID-SCHOOL-07:** A guardian MUST see and confirm the exact recipient,
  purpose, fields, direction, and expiry before the first disclosure and each
  material scope expansion.
- **KID-SCHOOL-08:** The child MUST see an age-appropriate explanation of
  school/carer access and have a concern/correction route.
- **KID-SCHOOL-09:** The application MUST preserve who accessed, created,
  changed, disclosed, acknowledged, corrected, or revoked a record.
- **KID-SCHOOL-10:** A school or carer connection MUST NOT expose the entire
  child workspace through a broad `view child` permission.

## Daily feedback

- **KID-FEED-01:** School feedback MUST be limited to factual, purpose-linked
  fields: support offered, whether the child used it, the child's own response,
  a neutral observation, and an optional follow-up request.
- **KID-FEED-02:** Feedback MUST distinguish adult observation, child self-report,
  system delivery event, and guardian response.
- **KID-FEED-03:** Feedback MUST NOT include a behavior score, compliance grade,
  diagnosis, medication-effect inference, class ranking, or `good/bad day`
  label.
- **KID-FEED-04:** Missing feedback MUST remain unknown. It MUST NOT imply that
  the child struggled, support was unused, medication was missed, or staff
  failed.
- **KID-FEED-05:** The child and authorized guardian MUST be able to request a
  correction or add a clearly attributed response without overwriting the
  original record.
- **KID-FEED-06:** Feedback notifications MUST use generic Sensitive previews.
- **KID-FEED-07:** Feedback retention MUST be purpose-limited and shorter than
  general account history unless a documented education-record obligation
  requires otherwise.

## Medication and health

Medication is not part of the foundational child release.

- **KID-MED-01:** Enabling medication functionality MUST require a separately
  authorized clinical-safety, privacy, school-process, and jurisdiction gate.
- **KID-MED-02:** Teacher access MUST NOT imply medication access. Medication
  administration fields MUST be available only to a verified designated school
  health professional or another role explicitly authorized under the school's
  approved process.
- **KID-MED-03:** A medication record MUST distinguish:
  guardian-entered information, current prescriber/pharmacy instruction,
  school administration plan, planned occurrence, factual administration
  record, child report, discrepancy, and unknown.
- **KID-MED-04:** A planned time or missing record MUST NOT establish that
  medication was taken, missed, refused, or administered.
- **KID-MED-05:** Only an authorized human confirmation MAY create an
  administration record. The record MUST retain actor, time, source,
  correction history, and any witnessed discrepancy.
- **KID-MED-06:** Timemanager Kids MUST NOT calculate a dose, recommend taking,
  skipping, delaying, doubling, stopping, or changing medication, or improvise
  missed-dose and interaction advice.
- **KID-MED-07:** A guardian or school adult MUST NOT edit prescriber
  instructions inside the product. A new verified source/version is required.
- **KID-MED-08:** Medication data MUST be Protected and Sensitive, excluded
  from teacher views, ordinary planning helpers, analytics content, AI context,
  public caches, notification text, logs, traces, and support tooling.
- **KID-MED-09:** Medication-specific content MUST have clinical owner, exact
  medicine/formulation scope, authoritative sources, jurisdiction, version,
  review date, and expiry. Unsupported or expired content MUST fail closed.
- **KID-MED-10:** The child MUST receive an age-appropriate explanation and a
  route to report uncertainty or concern. The app MUST direct medication
  uncertainty to current instructions and an appropriate adult or healthcare
  professional without generating dose advice.
- **KID-MED-11:** Medication adherence, treatment response, and school
  performance MUST NOT be inferred or scored.
- **KID-MED-12:** Medication administration MUST NOT be required to earn app
  rewards, unlock planning, preserve a streak, or avoid negative feedback.

## Notifications

- **KID-NOTIFY-01:** Importance and privacy MUST be separate classifications.
- **KID-NOTIFY-02:** Sensitive notifications MUST contain only generic wording
  and an opaque identifier; content is fetched after authentication.
- **KID-NOTIFY-03:** A child or adult MUST NOT receive duplicate alerts from
  every connected role.
- **KID-NOTIFY-04:** Dismissing a notification MUST NOT report failure,
  refusal, or non-compliance.
- **KID-NOTIFY-05:** Notification delivery and the underlying intention MUST
  have separate states.
- **KID-NOTIFY-06:** The system SHOULD expose an attention budget and combine
  lower-priority cues rather than escalate frequency.

## Portability, correction, and deletion

- **KID-DATA-01:** Authorized export MUST be workspace-scoped, versioned,
  documented, encrypted or equivalently protected in transit/storage, and
  exclude credentials and unrelated workspaces.
- **KID-DATA-02:** Child, guardian, school, health, consent, disclosure, and
  audit data MUST have explicit inclusion/exclusion rules rather than one bulk
  export assumption.
- **KID-DATA-03:** The product MUST support correction without silently
  rewriting attributed history.
- **KID-DATA-04:** Revocation MUST stop future access immediately; it MUST state
  what already disclosed data and legally required records cannot be recalled.
- **KID-DATA-05:** Deletion MUST distinguish active data, audit/security
  records, school/health records, backups, legal holds, processor copies, and
  deletion-completion evidence.
- **KID-DATA-06:** Retention MUST be defined per object and purpose before
  collection begins. Indefinite retention is prohibited.
- **KID-DATA-07:** School transfer and guardian dispute MUST have documented
  suspension, export, correction, handoff, and deletion paths.

## Cross-cutting acceptance

Every state-changing request MUST be authenticated, authorized, CSRF-protected
where browser forms apply, revision-aware, idempotent where retry is plausible,
workspace-scoped, and auditable. A guessed identifier MUST reveal neither data
nor object existence.

No requirement in this document is complete based only on a rendered screen.
Server authorization, negative ownership tests, accessibility checks, failure
fixtures, retention behavior, and human validation must pass the gates in
[Delivery and validation](delivery-and-validation.md).
