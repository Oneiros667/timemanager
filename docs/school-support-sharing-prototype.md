# School support and health-information sharing prototype

Status: synthetic disclosure prototype implemented; real sharing is blocked

Updated: 2026-07-28

## Purpose and evidence boundary

This prototype explores a guardian-controlled way to share the minimum
information a school needs to support a child. It covers classroom supports,
a guardian-approved condition summary, neutral daily observations, and a
separate medication-administration channel.

The workflow is a **plausible** product design. It is not evidence that sharing
more information improves a child's health, learning, behaviour, medication
adherence, or family-school relationship.

## Separate recipients and purposes

“The school” is not one recipient. Every disclosure must identify a named,
verified person, their current role, the purpose, individual fields, and an
expiry:

- a class teacher may receive classroom supports and contribute factual daily
  observations;
- a school nurse or other designated health professional may receive the
  minimum guardian-approved medication-administration plan needed for their
  role;
- neither role automatically sees the child's private task history, medication
  log, diagnosis history, mood history, other teachers' notes, or family notes.

Teacher access never implies medication access. A guardian cannot use the
ordinary teacher channel to send dosage instructions. Medication administration
must remain grounded in the school's authorised process and current prescriber
or pharmacy instructions; Timemanager does not let a teacher, guardian, or child
improvise or change a dose or schedule.

## Daily feedback contract

Daily feedback is deliberately small and factual:

- support offered and whether the child used it;
- the child's own “okay / need help” response;
- a brief neutral observation;
- an optional request for guardian follow-up.

The product must not generate or solicit a behaviour score, compliance grade,
diagnosis, medication-effect inference, ranking against classmates, causal
claim, or “good/bad day” label. Missing feedback does not mean the child
struggled, a medication was missed, or a teacher failed to provide support.

## Child-initiated communication

The young person needs a low-language way to communicate without first
explaining a diagnosis or composing a message. The synthetic prototype offers:

- “I'm overwhelmed”;
- “I need a quiet space”;
- “I can't talk right now”;
- “Please get my trusted adult”; and
- “Something else — please check in with me.”

These are communication requests, not symptom measurements or diagnostic
evidence. They must work for any child who finds them useful; the product does
not require an autism, social-anxiety, ADHD, or other diagnosis.

A real implementation must show the exact on-duty recipient before sending,
allow cancellation, provide accessible non-text alternatives where validated,
and visibly distinguish queued, delivered, acknowledged, unavailable, and
failed states. It must never imply that a teacher or carer has received or seen
a message until the server has evidence of that state. A fallback tells the
child how to reach a nearby trusted adult when delivery is unavailable. This
surface does not replace the school's safeguarding or emergency process.

The child gets an age-appropriate view of what is shared and received, subject
to a separately reviewed safety exception. Guardians can correct, dispute,
pause, or revoke future access. Existing records follow the applicable
retention and correction rules rather than being silently erased.

## Consent and authorization model

Before each real share, Timemanager must show:

1. the verified recipient and role;
2. the exact purpose and selected fields;
3. whether the flow is one-way or reciprocal;
4. the start and expiry;
5. the child's age-appropriate notice and available concern route;
6. who can revoke, correct, export, or dispute the record; and
7. the jurisdiction-specific authority or consent record.

Consent to classroom support does not authorize health sharing. Consent to one
medication administration plan does not authorize the full medication history,
future medications, AI processing, analytics, or disclosure to other staff.

## Implemented boundary

With `TIMEMANAGER_ENABLE_PROTOTYPES=1`, a same-device synthetic disclosure
preview is available at `/prototypes/school-support-share`. It uses only fixed
fictional category labels and browser-memory interaction. Refresh discards the
scenario. The route is disabled by default and returns `Cache-Control:
no-store`.

It sends no invitation, email, notification, or record. It creates no school,
teacher, child, guardian, health-professional, consent, audit, medication, or
feedback object. Real child, family, school, diagnosis, medication, or
prescriber information must not be entered during formative testing.

## Product topology: separate adult and child apps

The school-age product should be a separate guardian-operated application, not
a mode inside the current adult Timemanager PWA.

The two products may share reviewed, non-user-facing platform packages such as
design tokens, generic accessibility utilities, deployment tooling, and
cryptographic primitives. They must not share session cookies, databases,
analytics identities, search indexes, notification topics, exports, support
access, or default API authorization.

| Adult Timemanager | Guardian-operated child support app |
| --- | --- |
| Independent adult account and private planning | Guardian-created child workspace with age-appropriate child access |
| Trusted helpers propose by default | Verified guardian, teacher, carer, and school-health roles with distinct scopes |
| No school or medication sharing in the initial app | Separately gated school, health, safeguarding, and medication workflows |
| Adult controls disclosure and revocation | Guardian authority plus child notice, voice, concern routes, and market-specific consent/assent |

If the products later share backend infrastructure, every request still needs
an explicit product audience, tenant/workspace, role, scope, purpose, and
subject check. An adult account must never be converted in place into a child
workspace, and reaching a birthday must not silently migrate or broaden access.
Cross-product transfer requires a separately designed, previewed, consented,
audited process.

## Release gates

Persistent sharing requires all child-workspace gates plus:

- verified school organization, recipient identity, employment/role, and
  continuing role status;
- field-level server authorization and separate classroom/health scopes;
- guardian authority and child notice/assent appropriate to age and market;
- immutable disclosure, access, correction, export, revocation, and dispute
  history;
- secure invitations, expiry, recipient removal, school-transfer handling, and
  rapid access suspension;
- health-data and school-record DPIAs/privacy assessments, a medication-safety
  review, and an unsafe-family/coercion threat model;
- contracts and role allocation for Timemanager, the guardian, and school;
- no sensitive content in notifications, URLs, analytics, logs, traces,
  support tools, or model prompts;
- jurisdiction-specific education, health, child-data, safeguarding, records,
  and breach-response review; and
- supervised usability work using synthetic scenarios before any real-data
  pilot.

In the United States, school-maintained student health records are generally
education records protected by FERPA rather than HIPAA. Which law applies
depends on who maintains the record and in what capacity; Timemanager must not
present a generic “HIPAA compliant” label as authorization to share.

## Sources reviewed

Research checked 2026-07-28:

- [US Department of Education: FERPA guidance for school officials on student health records](https://studentprivacy.ed.gov/resources/family-educational-rights-and-privacy-act-guidance-school-officials-student-health)
- [US HHS and Department of Education: FERPA and HIPAA student-health-record guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/ferpa-hipaa/index.html)
- [UK ICO: Children's code and education technologies](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/the-children-s-code-and-education-technologies-edtech/)

These sources establish privacy and role boundaries; they do not validate the
product interaction or replace country/state/province-specific legal advice.
