# Roles, permissions, and sharing

Status: proposed authorization model; not implemented

Updated: 2026-07-28

## Governing rule

Access is granted to a verified relationship for a named purpose, specific
fields, direction, and time. No role receives the whole child workspace merely
because an adult knows the child, pays, works at a school, possesses an email
invitation, shares a device, or is listed as a contact elsewhere.

Authorization evaluates:

```text
authenticated actor
  + verified organization/relationship
  + supported child workspace
  + role
  + purpose
  + object and field scope
  + direction
  + time/expiry
  + market/consent policy
  + safety/dispute state
  = permit or deny
```

Every missing, expired, conflicting, or unverified element fails closed.

## Roles

### Child

The child is the supported person and a participant, not a passive data object.
Depending on age, ability, market, and approved preferences, the child may:

- view their day, relevant fixed commitments, shared items, and accessible
  history;
- capture thoughts, choose actions, record their own responses, and ask for
  help;
- use calm-break and low-language communication;
- see which adults currently have access and for what purpose;
- raise a concern, request correction, or object to a disclosure;
- manage non-legal presentation and accessibility preferences; and
- participate in renewal, transition, or closure decisions.

Child participation does not make the child responsible for administering
legal consent or resolving adult disputes.

### Primary verified guardian

The primary guardian may, within an authorized workspace:

- maintain ordinary shared planning and fixed commitments;
- configure age-appropriate child presentation;
- review child requests and respond;
- invite a school/carer recipient only after the required verification and
  disclosure confirmation;
- grant, narrow, renew, pause, or revoke scopes;
- request export, correction, or deletion subject to applicable rights and
  record obligations; and
- view child-visible history and guardian-specific security/consent records.

The guardian cannot:

- conceal ordinary planning changes from the child;
- grant blanket access to the whole workspace;
- authorize prohibited profiling, advertising, surveillance, or unsafe
  medication behavior;
- erase audit history;
- use billing as proof of authority; or
- use Timemanager to adjudicate custody or legal disputes.

### Additional guardian

An additional guardian is a separate verified relationship, not a seat copied
from the primary guardian. Adding, changing, or recovering this role requires
stronger assurance and notice to existing authorized parties. Conflicting
claims suspend access expansion.

### Teacher

A teacher may receive only the child and guardian-approved classroom-support
scope. Typical permitted fields are:

- current classroom supports;
- selected fixed school commitments;
- approved help signals while responsible for the child;
- factual daily-feedback form; and
- a follow-up request channel.

A teacher cannot see medication, diagnosis, family notes, full task history,
private child captures, other teachers' notes, guardian verification, or data
outside the class/purpose/time scope.

### Designated carer

A carer scope is tied to a named care context and period. It may include current
support instructions, relevant commitments, and approved child signals. It
does not inherit guardian, teacher, or health-professional authority.

### School health professional

This role is separately verified and scoped to the school's approved health or
medication process. It may receive only the minimum authorized medication
administration plan and create factual administration records where the later
health release is authorized.

It cannot change prescriber instructions, give authority to a teacher, inspect
unrelated planning, or use the application for diagnosis or treatment changes.

### Product operations

Operations staff have no standing access to child content. Break-glass access,
if the hosted architecture requires it, must be purpose-limited, time-limited,
approved, strongly authenticated, fully audited, visible to an independent
review function, and disclosed where lawful and safe. Routine support uses
metadata and user-supplied redacted evidence rather than browsing content.

## Permission matrix

`Selected` always means individually disclosed within an active scope.

| Capability | Child | Guardian | Teacher | Carer | School health |
| --- | --- | --- | --- | --- | --- |
| View child Today | Yes | Yes | No | No | No |
| View selected support card | Yes | Yes | Selected | Selected | Selected |
| Create ordinary shared action | Request/when enabled | Yes | Proposal only | Proposal only | No |
| Change ordinary shared action | Allowed fields | Yes with visible history | Own unaccepted proposal | Own unaccepted proposal | No |
| Complete own action | Yes | Yes with attribution | No | No | No |
| Drop/delete action | Request or allowed fields | Confirmed action | No | No | No |
| Send child support signal | Yes | No | Receive only while on duty | Receive only while on duty | Receive if selected |
| Submit daily feedback | Own response | Guardian response | Factual fields | Factual fields | Health fields only |
| View diagnosis summary | Child-visible version | Selected | Separate explicit field only | Separate explicit field only | Selected health scope |
| View medication plan | Child-visible version | Selected | Never by default | Never by default | Selected, separately gated |
| Record medication administration | Report only | Report only unless separately authorized | Never | Never unless specifically authorized | Yes, when health release permits |
| Invite another adult | No | Confirmed and verified | No | No | No |
| Broaden own scope | No | Confirmed under policy | No | No | No |
| View disclosure/audit history | Age-appropriate | Full authorized view | Own access events | Own access events | Own access events |

## Relationship lifecycle

Every relationship has:

- stable public ID and child workspace ID;
- actor identity and verified organization where applicable;
- role and purpose;
- field-level read/write scopes;
- direction: receive, contribute, or both;
- start, expiry, renewal, and last verification;
- authority/consent record and notice version;
- status: pending, active, paused, expired, revoked, disputed, or suspended;
- creation, verification, scope-change, access, and revocation audit events; and
- child-visible explanation.

### Invitation

1. Guardian chooses a recipient role and purpose.
2. The application shows data fields and direction before requesting contact
   information.
3. The organization and adult role are verified.
4. The recipient reviews the exact scope and accepts.
5. The guardian confirms the resolved identity, role, scope, and expiry.
6. The child sees an age-appropriate explanation.
7. Server authorization activates only the confirmed fields.

Possession of an invitation link never proves role or authority.

### Renewal

Renewal rechecks role, purpose, organization, child relationship, and current
need. It is not automatic. Expired access remains denied while renewal is
pending.

### Revocation and suspension

Revocation immediately prevents future reads, writes, and delivery. It records
who revoked and why at the minimum safe detail. Suspension is used for
organization de-verification, suspected compromise, unsafe-family reports,
role disputes, or incident response.

The product must distinguish stopping future access from recalling data already
disclosed. It must not promise deletion from a school's lawful records without
evidence and authority.

## Guardian assurance

Guardian verification answers:

1. does this adult control the account; and
2. does this adult have authority to act for this child for this purpose?

Email, phone, payment, app-store family membership, shared surname, shared
address, and an existing adult account may support risk assessment but do not
alone answer the second question.

### Progressive levels

| Level | Controls | Maximum outcome |
| --- | --- | --- |
| Account assurance | Verified contact, passkey/MFA, protected recovery | Pending guardian profile only; no child data |
| Standard guardian assurance | Versioned declaration, age band, country, notice, independent confirmation, risk checks | Limited child planning where market policy permits |
| Strong guardian assurance | Minimal verified authority attribute or trained review; raw evidence promptly deleted | Additional guardian, disputed recovery, high-risk sharing |
| Dispute state | Fresh strong checks and trained review | No access expansion until resolved |

The application stores the verification result, method class, time, provider,
scope, and expiry—not raw documents, selfies, or video unless an approved
exception requires temporary handling.

## School and carer verification

Verification must establish:

- the organization exists and is approved for the launch market;
- the adult controls the account;
- the adult currently holds the stated role;
- the adult currently has responsibility for this child and purpose;
- the organization accepts applicable processor/controller, security,
  retention, safeguarding, and incident obligations; and
- there is a current route to report role termination.

School email alone is insufficient. Organization administrators may attest
roles, but their authority and changes are also audited and periodically
revalidated.

## Disclosure preview

Before every first disclosure or scope expansion, show:

- child and workspace;
- resolved recipient name, organization, and role;
- purpose in plain language;
- exact fields with example values or redacted preview;
- whether the recipient can contribute;
- notification behavior;
- start and expiry;
- child-facing explanation;
- authority/consent record;
- correction, dispute, and revocation effects; and
- any external processor or cross-border transfer.

Unchecked fields are absent from the payload, recipient API response, search
index, notification, export, and analytics context. Hiding a field in the
interface is not authorization.

## Child-visible history

The child history answers:

- Who can see something about me?
- What can they see or add?
- Why?
- What changed?
- Did my message arrive?
- When does access end?
- How can I ask, correct, or tell someone it feels wrong?

History uses age-appropriate summaries backed by immutable audit events. Safety
exceptions that temporarily limit disclosure require a documented policy,
authorized decision, review time, and later disclosure assessment; they cannot
become a general hidden-monitoring feature.

## Feedback and disagreement

Adult observations are attributed observations, not facts about the child's
condition or motivation. The child and guardian may add a response or correction
request. The original, correction, and resolution remain linked.

The product does not resolve custody, school discipline, safeguarding, or
clinical disputes. It suspends unsafe access changes, preserves minimum
evidence, and routes to trained human processes.
