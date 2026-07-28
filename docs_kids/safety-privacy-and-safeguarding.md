# Safety, privacy, and safeguarding

Status: proposed mandatory release controls; not legal advice and not
authorization for real child data

Updated: 2026-07-28

## Safety position

Timemanager Kids processes children's planning, communication, family, school,
and potentially health information. The child's best interests, safety,
privacy, development, and ability to be heard are primary design constraints.

The product is not a crisis, emergency, safeguarding, medical, or therapeutic
service. It must not create reliance by promising that a guardian, teacher,
carer, nurse, or operator is continuously available.

## Non-negotiable prohibitions

The application must not:

- use advertising, targeted content, data brokerage, sale/sharing, social
  discovery, or commercial profiling;
- collect precise location, continuous background sensor data, raw voice,
  camera, biometric, or emotion-recognition data in the initial product;
- infer diagnosis, mood, medication effect, dangerousness, compliance,
  attendance, or family quality from app behavior;
- create hidden tasks, hidden adult access, covert monitoring, or invisible
  location/check-in reports;
- score, rank, shame, punish, reward medication behavior, or expose child
  performance leaderboards;
- use deceptive or manipulative nudges to obtain more data, weaken privacy,
  prolong engagement, or discourage revocation;
- make a child responsible for adult conflict, legal consent, medication
  decisions, or emergency response;
- permit open messaging, unverified contacts, file exchange, social profiles,
  or public content;
- use sensitive content in notification text, analytics, logs, traces, support
  screenshots, public caches, or model prompts; or
- present compliance labels as proof that an individual disclosure is lawful,
  safe, necessary, or clinically correct.

## Data classes

| Class | Examples | Default |
| --- | --- | --- |
| Core planning | Task title, next action, fixed commitment | Private to child workspace |
| Shared support | Selected classroom support, carer instruction | Sensitive; explicit field disclosure |
| Child communication | Help signal, message, acknowledgement | Sensitive; named on-duty recipient |
| School feedback | Factual observation, support offered | Sensitive; purpose- and term-limited |
| Health/medication | Condition summary, administration plan/record | Protected and Sensitive; later gated domain |
| Authority/consent | Guardian verification result, notice version, scope | Restricted security/privacy data |
| Audit/security | Access, disclosure, change, revocation, incident events | Restricted; append-only and purpose-limited |
| Operational metrics | Route success/failure without content | Content-free and minimized |

Free text may contain unexpected sensitive information. The product treats
free-text content as Sensitive even when the surrounding object is ordinary.
It does not claim to detect and reclassify every sensitive detail.

## Privacy defaults

- Collect only data needed for an enabled, documented purpose.
- Disable school, carer, health, external calendar, AI, voice, third-party
  analytics, and additional guardian access by default.
- Keep child content invisible to other users until a field-level scope is
  active.
- Use generic device notifications and fetch details only after
  authentication.
- Do not place authenticated responses or child content in public service
  worker caches.
- Do not use personal content for product analytics, model training, support
  browsing, or marketing.
- Make retention finite and purpose-specific before collection starts.
- Make privacy explanations available in tested 8–10, 11–12, 13–15, 16–17,
  and guardian/adult versions.

## Child voice and parental controls

Guardian controls are visible to the child in age-appropriate language. The
child can see active adult roles and ordinary disclosures, express preferences,
request correction, and raise a concern.

Parental controls must not become covert surveillance. Where law or an approved
safeguarding decision permits limiting immediate disclosure, the exception must
have:

- a named policy and authority;
- a recorded reason category without unnecessary detail;
- a narrow data/action scope;
- a review and expiry;
- an accountable human decision; and
- a later child-notice assessment.

## Safeguarding boundary

### Ordinary support signal

Messages such as `I'm overwhelmed` or `I need a quiet space` are ordinary
support requests. They have honest delivery states and a nearby-human fallback.
They are not emergency monitoring.

### Concern or unsafe-access report

The child and authorized adults need a separate route to report:

- the wrong person has access;
- an adult is using information to punish, shame, or pressure;
- a message or record is inaccurate;
- a guardian, teacher, or carer relationship feels unsafe;
- a device/account may be compromised; or
- the normal support route is inappropriate.

The report flow minimizes detail, explains who will receive it, allows a safe
contact preference, and avoids notifying a possibly unsafe party automatically.

### Urgent and emergency situations

The application provides reviewed, market-specific instructions for contacting
a nearby trusted adult or the institution's emergency/safeguarding process. It
does not generate emergency advice, continuously monitor the child, or promise
response. Any hotline information must come from an authoritative, maintained
routing service at use time rather than hard-coded global numbers.

## Unsafe-family and coercion threat model

Pre-launch review must cover at least:

- a person falsely claiming guardianship;
- conflicting guardians or custody restrictions;
- a guardian forcing disclosure or using tasks/calm breaks as punishment;
- a child using a shared device while an unsafe adult observes;
- coercion to withdraw an objection or mark an action complete;
- a teacher or carer retaining access after role termination;
- a school administrator granting overbroad organizational access;
- staff viewing private child messages out of curiosity;
- an adult fabricating child responses or medication events;
- notification previews exposing sensitive information;
- account recovery used to replace a guardian or child device;
- export used to extract an entire child history;
- deletion used to erase evidence of access or misuse;
- a school transfer leaving old staff connected; and
- an operator or processor accessing content outside a support purpose.

Controls include least privilege, strong authentication, role re-verification,
child-visible history, safe-device guidance, session/device review, delayed
high-risk changes, independent dispute handling, anomaly detection without
content profiling, and rapid suspension.

## School and health record boundaries

A disclosure from Timemanager may become a school or health record under the
recipient's law and policies. The product must establish controller/processor
roles, contracts, correction routes, retention, redisclosure, incident
responsibility, and parent/child access rights before integration.

In the United States, student health records maintained by a FERPA-covered
school or a party acting for it are generally education records under FERPA,
not HIPAA protected health information. Other providers and contexts may differ.
The product must not advertise a generic `HIPAA-compliant teacher sharing`
claim.

Medication administration is a separate safety domain. General guardian
permission, a teacher connection, or a planning task never authorizes access,
administration, or dose changes.

## Jurisdiction routing

Worldwide intent does not create one worldwide consent flow. Every market is
disabled until the release record identifies:

- child-data and age-assurance requirements;
- lawful basis and guardian/competent-person authority;
- child notice, assent/objection, and rights;
- education and health-record obligations;
- special-category/sensitive-data conditions;
- processor/controller contracts and international transfers;
- retention, deletion, correction, and legal holds;
- breach and safeguarding reporting;
- accessibility and consumer-protection obligations; and
- accountable legal/privacy approval for the exact product build.

### Current design baseline

| Market | Product gate |
| --- | --- |
| United States | COPPA applies to covered under-13 collection and requires notice, verifiable parental consent, parent rights, minimization, security, and retention controls. The amended COPPA Rule adds current requirements including separate consent for certain third-party disclosures and limits on indefinite retention. FERPA/state rules require separate school review. |
| European Union | GDPR child-consent ages vary by Member State from 13–16 where consent is the basis. Maintain a country/lawful-basis matrix, clear child language, verified authority, DPIA, minimization, rights, processor, and transfer controls. |
| United Kingdom | Apply the Children's Code/UK GDPR best-interests, DPIA, high-privacy, minimization, transparency, parental-control, profiling, sharing, and nudge standards. |
| South Africa | Treat POPIA child processing and health/education information as launch blockers requiring competent-person/section 35 analysis, security safeguards, rights, and Information Officer/legal review. |
| Australia | Apply existing Privacy Act/APP obligations and track the Children's Online Privacy Code. As of 2026-07-28 the Code is still an exposure draft planned for registration by 10 December 2026; it must not be described as current final law. |

This table is planning context, not a legal determination.

## Consent, authority, and assent records

Each authority record includes:

- child workspace and age band;
- market and applicable product policy;
- adult identity and verified relationship result;
- purpose and exact data/permission scope;
- direction and recipients;
- notice and consent-language versions;
- method, time, expiry, renewal, withdrawal, and revocation;
- child notice/participation status appropriate to the flow;
- evidence-minimization and raw-evidence deletion status; and
- disputes or safety restrictions.

Consent is not bundled. Ordinary planning, school support, carer support,
medication, external calendar, research, optional AI, and any analytics beyond
essential operations are separate decisions.

## Retention and deletion

Before collecting an object, define:

- purpose;
- active retention period;
- event that starts expiry;
- user-visible archive period if any;
- backup expiry;
- processor deletion;
- audit/security retention;
- legal or school/health record exceptions;
- correction and dispute holds; and
- evidence of completion.

The COPPA baseline prohibits indefinite retention and requires retaining child
information only as long as reasonably necessary for its specific purpose.
The product adopts that principle globally unless a stricter rule or documented
record obligation applies.

Revocation stops future access. Deletion must not silently erase access,
disclosure, safety, or medication provenance that must be retained; the user
receives a precise explanation instead of an impossible promise.

## Security baseline

Before real data:

- production hosted deployment with TLS and secure session configuration;
- passkeys or MFA for every adult role;
- protected child-device authentication appropriate to age and risk;
- tenant/workspace isolation and field-level server authorization;
- encryption in transit and at rest with managed key rotation;
- secrets outside source/client code;
- append-only security/disclosure audit with restricted access;
- content-free logs, traces, analytics, crash reports, and support tooling;
- dependency, processor, and software-supply-chain review;
- rate limiting, invitation abuse controls, session/device management, and
  recovery protections;
- tested encrypted backups and workspace-scoped restore;
- incident detection, containment, notification, and evidence preservation;
- penetration testing and independent authorization review; and
- deletion and role-termination tests.

## AI, voice, analytics, and research

AI and raw voice are disabled in the first real-data release. Adding either
requires a separate product decision, child/guardian disclosure, provider and
retention assessment, non-AI fallback, content boundaries, safety evaluation,
and market authorization.

Essential operational metrics exclude child content and sensitive categories.
Product research is separate from normal use. Research with minors requires an
approved protocol, guardian permission where applicable, child assent,
minimized/de-identified notes, trained facilitators, stop/withdraw routes, and
synthetic scenarios until a real-data protocol is independently approved.

## Blocking findings

Release review stops for:

- unverified guardian or school authority;
- cross-workspace or out-of-scope access;
- concealed external transfer;
- sensitive content in notification, analytics, log, trace, support, cache, or
  model fixtures;
- medication advice or unverified administration claims;
- a help signal that reports delivery without evidence;
- covert tracking or punitive/compliance mechanics;
- missing correction, revocation, retention, deletion, or dispute behavior;
- documentation describing proposed or synthetic behavior as live; or
- a market enabled without recorded authorization.

## Primary sources reviewed

Checked 2026-07-28:

- [FTC: Children's Online Privacy Protection Rule](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- [FTC: 2025 COPPA Rule amendments](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-finalizes-changes-childrens-privacy-rule-limiting-companies-ability-monetize-kids-data)
- [European Commission: safeguards for children's data](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/are-there-any-specific-safeguards-data-about-children_en)
- [UK ICO: Age Appropriate Design Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/)
- [UK ICO: Children's Code design guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/designing-products-that-protect-privacy/childrens-code-design-guidance/)
- [South African Information Regulator: guidance notes](https://inforegulator.org.za/guidance-notes/)
- [US Department of Education: FERPA guidance on student health records](https://studentprivacy.ed.gov/resources/family-educational-rights-and-privacy-act-guidance-school-officials-student-health)
- [HHS/Department of Education: FERPA and HIPAA guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/ferpa-hipaa/index.html)
- [Australian OAIC: draft Children's Online Privacy Code](https://www.oaic.gov.au/news/media-centre/oaic-releases-exposure-draft-of-the-childrens-online-privacy-code)
