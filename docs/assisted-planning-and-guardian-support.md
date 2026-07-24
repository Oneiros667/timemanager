# Assisted planning and guardian support

Status: proposed product direction

Updated: 2026-07-24

## Purpose and boundary

Timemanager should support help without turning planning into surveillance.
The feature has two different jobs:

1. help a parent or legal guardian record and maintain a child's tasks,
   appointments, reminders, transitions, and small next actions; and
2. let an adult with ADHD invite a partner, friend, family member, coach, or
   other trusted person to assist with selected planning work.

This is planning support, not clinical care, family monitoring, school
discipline, location tracking, behaviour scoring, or a mechanism to pressure a
person into completing tasks. It must not claim to treat ADHD.

Timemanager is a subscription product. It does not use advertising as a revenue
source and must not use children's or adults' data for behavioural profiling,
sale, sharing, or social discovery.

## Non-negotiable data and monetisation boundaries

The product must not collect, infer, sell, share, or enable the following as a
feature or revenue source: advertising identifiers or targeted advertising;
behavioural profiling; social discovery; ADHD diagnosis or treatment data;
health information; precise location; school records; or voice recordings.
These are exclusions, not optional settings. A future proposal to add any of
them requires a separate product decision, privacy/legal assessment, and an
explicit revision of this document before implementation.

## Two support modes

| Mode | Supported person | Helper | Default authority | Primary outcome |
| --- | --- | --- | --- | --- |
| Guardian-supported child planning | Child profile | Verified parent or legal guardian | Guardian can maintain the shared plan within the agreed child workspace | Fewer lost commitments and clearer, calmer daily orientation |
| Adult trusted-person support | Adult account | Invited partner, friend, family member, coach, or other trusted person | Helper proposes; the adult decides by default | Less planning friction and easier recovery without loss of autonomy |
| Focus companion | Child or adult | Invited trusted person | Presence and agreed check-ins only | Easier task initiation and return after interruption |

These modes share data structures but not assumptions about authority. An adult
helper does not receive guardian-like control. A guardian relationship must not
be used to justify hidden monitoring, broad data disclosure, or automatic
medical decisions.

## Roles and permissions

Every relationship is limited to an **assistance workspace**. A helper never
inherits access to the entire account merely because they know the person.

| Role | May see | May create | May change | May complete/drop | May invite others |
| --- | --- | --- | --- | --- | --- |
| Adult owner | Everything in their account | Tasks, appointments, reminders, support scopes | Everything | Yes | Yes |
| Adult trusted planner | Only explicitly shared items and chosen availability | Draft tasks, appointment/reminder proposals, check-ins | Their own unaccepted drafts | No, unless an adult explicitly grants a narrow temporary permission | No |
| Focus companion | Session intention, time boundary, and join/leave status | Check-in messages or distraction captures when invited | No plan data | No | No |
| Guardian | The child workspace and items needed for the agreed care/planning role | Tasks, appointments, reminders, routines, and proposals | Shared child plan, subject to visible history and child-view settings | Can manage plan states, but must not erase the audit trail | No, unless another verified guardian relationship is explicitly established |
| Child | Age-appropriate child view of their plan | Capture/request-help items when enabled | Their responses, preferences, and allowed task fields | May mark items done or ask for help | No |

The final guardian model must distinguish legal guardian, parent, and any other
supporter. Do not label a relationship as verified merely because someone was
invited by email.

## Adult trusted-person workflow

1. The adult chooses a helper and a scope: focus presence, selected tasks,
   appointments/reminders, or a time-limited planning window.
2. Timemanager shows a human-readable disclosure preview before an invitation
   is sent.
3. The helper accepts the invitation and sees only the approved scope.
4. A helper-created task, appointment, reminder, or assignment enters the
   adult's plan as a clearly labelled **proposal**.
5. The adult can accept, edit, schedule, defer, or decline it. Declining does
   not create a failure signal, notify other helpers by default, or alter the
   relationship.
6. Every material change records who proposed it, what changed, when, and
   whether the adult accepted it.
7. The adult can pause a helper, reduce scope, or revoke access immediately.

An adult may explicitly delegate a narrow task—for example, "please add the
dentist appointment after I confirm the date"—but the interface must show the
delegation and its expiry. Helpers cannot silently turn a suggestion into a
deadline, completion, deletion, or recurring reminder.

## Guardian-supported child workflow

The first child-oriented pilot serves young people aged **13 and older**. It is
a guardian-managed workspace with an optional simplified child view, not an
independent child social account. Parent/guardian editing is the default inside
that child workspace, subject to the visible history and privacy boundaries
below.

1. A verified guardian creates or links a child workspace and selects the
   support purpose.
2. The guardian records an appointment, task, routine, reminder, or transition
   in plain language.
3. The child view presents only the relevant current item, its next step, and
   a calm way to respond: done, not now, need help, or talk to my grown-up.
4. Guardian-created changes remain visible in the child's history in an
   age-appropriate form. Do not use hidden task creation, covert reminders, or
   concealed monitoring as a feature.
5. The guardian can adjust reminders and the plan after real-world changes;
   the system preserves the old and new values in the audit history.
6. The child can capture a thought or request help if the guardian enables it.
   Those submissions are clearly marked as the child's input.

For a child, an "assignment" is a shared planning commitment, not a score or
punishment. The child-facing language should describe what is next and who can
help, rather than use deficit labels or overdue debt.

## Shared planning objects

Tasks, appointments, and reminders gain the following fields when they enter an
assistance workspace:

- workspace and supported-person identifiers;
- created-by, proposed-by, and last-changed-by identity;
- helper scope and source relationship;
- proposal state: draft, awaiting response, accepted, adjusted, declined,
  expired, or revoked;
- optional intended recipient and an acknowledgement state;
- reminder recipients and delivery status;
- immutable audit events for creation, material edits, acceptance, completion,
  revocation, and deletion requests.

The ordinary personal task view remains simple. Provenance and permission
detail appear only when a person needs to understand or review a shared item.

## Reminders, appointments, and assignments

### Reminders

- A helper may propose a reminder; the adult decides whether it becomes active
  unless a guardian manages a child's workspace.
- The system shows who will receive each reminder and how often before saving.
- A child or adult should not receive duplicate alerts from every helper.
- Dismissing a reminder does not silently report failure to a helper.

### Appointments

- A helper can record or propose an appointment with source, time, travel, and
  preparation details.
- Google Calendar writes remain explicitly confirmed by the account holder or
  guardian with the relevant permission; no helper can silently create or move
  an external event.
- Calendar detail outside the agreed assistance scope stays private.

### Assignments and requests

- Adults receive assignments as requests/proposals by default; they may accept,
  decline, or negotiate them.
- Guardians can place age-appropriate shared commitments in a child workspace,
  but the child view must make the action, reason, and available help clear.
- Completion is a factual status, not a measure of worth, compliance, or
  parenting quality.

## Privacy, safety, and release gates

This feature processes personal information about children and can expose
highly sensitive family routines. Its first online release requires all of the
following:

- a launch-jurisdiction legal and privacy review, including a child-data
  assessment and guardian-verification approach;
- age-appropriate notice, consent/assent design, and a way to withdraw or
  change access where applicable;
- data minimisation: the prohibited categories in the non-negotiable boundary
  above are not collected or inferred; basic planning needs no diagnosis,
  medication, school, location, voice, or health data;
- authenticated, expiring invitations; scoped server-side authorization; audit
  history; revocation; export; deletion; and breach-response procedures;
- an abuse/threat model covering coercive helpers, unsafe household dynamics,
  account takeover, and accidental over-sharing;
- user testing with families, adults with ADHD, and relevant child-development,
  accessibility, and privacy expertise before broad release.

The regulatory detail depends on launch location and age. For example, US
services covered by COPPA have child-data obligations, and South African POPIA
has specific guidance and authorization context for processing children's
personal information. These sources are design inputs, not legal advice:

- [FTC: Children's Online Privacy Protection Rule](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- [South African Information Regulator: guidance on personal information of children](https://inforegulator.org.za/guidance-notes/)

## First-pilot scope

Build and test the smallest meaningful version:

1. one parent/guardian-managed workspace for a child aged 13 or older, with
   manual task, appointment, and reminder entry;
2. an adult inviting one trusted planner with proposal-only access;
3. a focus-companion session with intention and start/end check-ins;
4. visible change history, immediate revoke, and no hidden tracking;
5. no third-party helper discovery, social feed, school portal, medical data,
   location tracking, automated assignment, or AI-mediated helper action.

The local development pilot must not claim that an email invitation verifies a
guardian relationship. Remote invitations, child accounts, and shared hosted
workspaces require the hosted authorization and safety gates above.

## Evaluation

Test whether the feature improves practical support without adding pressure:

- Can a guardian record and clarify a child's next commitment quickly?
- Does the child understand what is next and how to ask for help?
- Can an adult accept useful planning help while still feeling in control?
- Do helpers understand exactly what they may see and change?
- Are reminders useful without becoming duplicated or punitive?
- Can either person revoke access or recover after a disagreement?
- Do families report less lost information and less planning conflict, without
  more shame, surveillance, anxiety, or maintenance burden?

## Confirmed pilot decisions

- The first guardian-supported child pilot serves young people aged 13 and
  older.
- The pilot uses a parent/guardian-managed child profile, not a separate child
  sign-in.
- A guardian may edit the child workspace by default, while the child sees a
  clear, age-appropriate account of what is next and what changed.
- Adult trusted helpers are proposal-only by default. An adult can grant a
  narrow, time-limited delegation when they explicitly choose to do so.

## Worldwide release gate

Timemanager is intended for worldwide availability, but that is not one
universal compliance setting. Before the hosted product is available in any
country or region, the release process must determine the applicable child-data,
guardian/consent, age-assurance, privacy-notice, data-location, deletion,
security-incident, and cross-border-transfer requirements for that market.

The product must use country/region launch controls until those requirements are
reviewed and implemented. A general parent-managed profile for ages 13+ does
not by itself establish legal authority to process a child's data worldwide.

## Initial jurisdiction baseline (US, EU, UK, South Africa, Australia)

This is a product-design baseline current on 2026-07-24, not legal advice or a
substitute for local counsel. It identifies the controls that must be designed
before a hosted launch; a lawyer must confirm applicability, role allocation,
lawful basis, notices, contracts, and any sector- or state-specific rules for
each actual launch market.

| Market | Child / consent rule most relevant to this product | Practical requirement for Timemanager |
| --- | --- | --- |
| United States | COPPA applies to covered online services directed to children under 13, or services with actual knowledge that they collect personal information from a child under 13. It generally requires verifiable parental consent before collection, use, or disclosure, subject to limited exceptions. | Do not treat a stated 13+ age as enough by itself. Use age assurance, prevent direct under-13 onboarding unless the COPPA flow is ready, give a direct parent notice, obtain and record verifiable parental consent where COPPA applies, provide parent access/deletion controls, minimise retention, and prohibit behavioural advertising or third-party disclosure of child data unless separately permitted. State privacy and consumer-protection rules still need a market review. |
| European Union | Under GDPR Article 8, when consent is the lawful basis for an information-society service offered directly to a child, the default threshold is 16; a Member State may lower it, but not below 13. Other GDPR obligations still apply regardless of the consent threshold. | Maintain a per-country age and lawful-basis matrix; do not ship one EU consent screen. Use clear child-facing notices, a documented lawful basis, age/parent-authority verification proportionate to risk, data minimisation, rights handling, processor and transfer controls, security, and a child-focused DPIA before launch. Avoid profiling, targeted advertising, and unnecessary sharing. |
| United Kingdom | If consent is the lawful basis for an online service, a child can consent from 13; below 13, obtain and reasonably verify parental-authority consent. The ICO Children's Code applies to online services likely to be accessed by children and imposes 15 age-appropriate design standards. | Use high-privacy defaults, a Children's Code assessment/DPIA, age-appropriate explanations, minimal collection, no nudges that weaken privacy, no default precise geolocation or profiling, and clearly presented parental controls. The child workspace must not rely on covert guardian monitoring. |
| South Africa | POPIA generally prohibits processing a child's personal information unless a section 35 exception applies; the ordinary product route is prior consent from a competent person. POPIA also imposes the general conditions for lawful processing. | Treat guardian authority and consent as a launch blocker, not merely an account setting. Record the competent person's consent and scope, minimise data, avoid diagnosis/health data by default, provide access/correction/deletion paths, secure data and suppliers, and prepare incident-response processes. Obtain South African advice before relying on any exception or processing special personal information. |
| Australia | The Privacy Act and Australian Privacy Principles (APPs) protect personal information regardless of age. The OAIC says capacity to consent is assessed case by case; it is generally reasonable to assume capacity from age 15 unless there is doubt, otherwise seek parent/guardian consent. The Children's Online Privacy Code is currently an exposure draft, with registration planned for 10 December 2026. | Assess whether the service is an APP entity and use an age/capacity and parent-authority flow rather than assuming 13-year-olds can always consent. Meet APP notice, purpose, access/correction, security, and deletion obligations. Design now for the proposed Code's child-best-interests, clear notice, minimisation, and parent-consent transparency expectations, but do not describe the draft as current law. |

The first 13+ parent-managed pilot can therefore be designed around a verified
guardian, but it should be geographically limited until the country-specific
matrix is reviewed. It must not collect an under-13 child's information through
an independent child account or weaken the non-negotiable data and monetisation
boundaries above.

### Product controls common to every launch

1. **Age and market routing.** Ask only for the minimum age band and launch
   country necessary to apply the right flow; do not retain identity-document
   data merely to prove age unless counsel approves a proportionate method.
2. **Guardian authority and consent record.** Verify the adult relationship at
   a risk-appropriate level, show what data and permissions the adult is
   authorising, record the method, time, jurisdiction, versioned notice, and
   scope, and support withdrawal/revocation.
3. **Child-visible privacy.** Give the young person an age-appropriate notice
   and an intelligible change history. Tell them when a guardian created or
   changed an item; do not enable hidden tracking.
4. **Least data and least access.** Keep the child workspace separate, default
   to parent-managed planning data only, scope every helper, and exclude
   advertising, data brokerage, social discovery, sensitive notes, and
   unnecessary analytics.
5. **Rights, retention, and security.** Provide an authenticated way to
   access, correct, export, delete, and revoke access as applicable; publish a
   short retention schedule; encrypt data in transit and at rest; log material
   access/changes; vet processors; and maintain incident response and required
   notification procedures.
6. **Pre-launch evidence.** Complete a child-data impact assessment/DPIA or
   equivalent, threat-model coercive or unsafe-family scenarios, test the flows
   with parents and young people, and obtain counsel sign-off for every enabled
   market before switching on hosted child workspaces.

### Guardian verification design

Guardian verification answers two different questions: whether an adult
controls an account, and whether that adult has authority to make privacy
decisions for the child. Email or payment verification supports the first; it
must not alone be treated as proof of the second.

Use progressive assurance: collect only enough evidence for the risk of the
requested action, and do not unlock a child workspace until the applicable
market's required level is met.

| Assurance level | Suitable controls | Permitted outcome |
| --- | --- | --- |
| Account assurance | Verified email, MFA/passkey, confirmed subscription payment, device/session protection, and adult declaration of authority. | Start a pending workspace; no other guardian/helper invitations, external calendar connection, or child-created information. |
| Standard guardian assurance | Versioned guardian declaration; child age band and country; direct guardian notice; independent-channel confirmation (for example, confirmation email plus delayed reconfirmation); fraud/duplicate-account checks; and an audit record of method and result. | Parent-managed planning workspace with the strictly limited data set, where permitted by the country launch policy. |
| Strong guardian assurance | A specialist provider returns a minimal yes/no parental-authority attribute, or trained human review verifies an appropriate document or live video call. Delete raw documents, selfies, and video promptly after the check. | Add a second guardian, recover a disputed account, or resolve a high-risk/conflicting claim. |
| Dispute handling | Pause access changes; perform a fresh strong check; use trained privacy/safety review; retain only the decision and minimum evidence; offer appeal. | No access expansion until resolved. Never adjudicate custody disputes in-product. |

Specific controls:

- Make guardian status an explicit, revocable relationship with scope and
  expiry—not a permanent account label.
- Require passkeys or MFA for every guardian; notify the existing guardian and
  record child-visible history when a guardian, device, or recovery method
  changes.
- Require explicit confirmation before adding another guardian or trusted
  helper. Use strong assurance, or an already verified guardian's approval plus
  a risk review, for a second guardian.
- Bind consent to the child workspace, country, privacy-notice version,
  permitted data, and permissions. Reconfirm after material scope changes.
- Prefer a third-party attribute response (for example, “parental authority
  confirmed”) over storing ID scans, payment data, or biometrics in
  Timemanager. Contract, assess, and monitor that provider.
- Provide an accessible fallback for people without formal ID or credit cards,
  and a way to challenge an incorrect result. Do not let automation be the sole
  decision maker for denial.
- Rate-limit invitations and recovery changes; detect unusual guardian
  additions and failed checks; suspend expansion rather than expose child data.
- Separate verification evidence from planning data, keep it only as long as
  needed for compliance/account security, and never reuse it for analytics,
  marketing, profiling, or age estimation.

For the first parent-managed 13+ pilot, standard guardian assurance is a
reasonable starting point; reserve strong assurance for adding a second
guardian, account recovery, disputes, or a jurisdiction that requires it.
Launch counsel must confirm adequacy per market: a low-risk data set reduces
risk but does not itself prove parental authority.

Primary sources used for this baseline:

- [FTC: COPPA frequently asked questions](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions)
- [European Commission: safeguards for data about children](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/are-there-any-specific-safeguards-data-about-children_en)
- [ICO: Age Appropriate Design Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/)
- [Information Regulator: POPIA guidance on children](https://inforegulator.org.za/wp-content/uploads/2020/07/GuidanceNote-Processing-PersonalInformation-Children-20210628-1.pdf)
- [OAIC: children and young people](https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/children-and-young-people) and [OAIC: draft Children's Online Privacy Code](https://www.oaic.gov.au/news/media-centre/oaic-releases-exposure-draft-of-the-childrens-online-privacy-code)
