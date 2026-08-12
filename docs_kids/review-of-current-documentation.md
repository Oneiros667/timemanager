# Review of current Timemanager documentation

Status: completed repository documentation review for child-product planning

Reviewed: 2026-07-28

## Review method

Every Markdown document then present under `docs/` and `docs/decisions/` was
reviewed for:

- evidence population and whether it applies to children;
- implemented adult behavior versus proposed behavior;
- reusable interaction or technical contracts;
- child safety, school, health, medication, privacy, and authorization
  conflicts;
- accepted adult architecture decisions that must not be inherited; and
- open validation or release gates.

The review also checked current official guidance from the FTC, European
Commission, UK ICO, South African Information Regulator, US Department of
Education/HHS, and Australian OAIC. This is product research, not legal advice.

## Main conclusion

The repository contains a useful adult planning foundation and two synthetic
child-support prototypes, but it does not contain a child application.

Timemanager Kids must be a separate product because ages 8–17 introduce:

- guardian authority and disputes;
- the child's evolving capacity, privacy, participation, and right to be heard;
- school, carer, and school-health roles;
- education, health, medication, and safeguarding information;
- external messaging and delivery-state obligations;
- jurisdiction-specific age/consent routing; and
- a much stronger risk from covert monitoring, coercion, oversharing, and
  incorrect adult authority.

Child-only source documents identified by this review were consolidated into
`docs_kids/` and subsequently removed from the adult `docs/` root. The table
records the source set and disposition rather than claiming that every path
still exists.

## Document-by-document disposition

| Existing document | Review result for Timemanager Kids |
| --- | --- |
| Repository `README.md` | Preserve its precise implemented adult-pilot baseline and link to this separate specification. The adult quick-start and runtime do not start a child application. |
| `docs/README.md` | Reuse its evidence/status vocabulary. Do not treat its adult research index as child validation. |
| `docs/AGENTS.md` | Reuse evidence discipline, current-source verification, non-clinical language, and implemented/proposed separation. |
| `docs/assets/*.png` | The synthetic screenshots document adult application views. They are not child designs or evidence of child usability. |
| `adhd-time-management-domain-research.md` | Adapt immediate capture, concrete next action, visible time, small plans, low-capacity recovery, and non-shaming language. Evidence review is adult-centered; child efficacy remains unverified. |
| `reference-systems-analysis.md` | Treat daily focus, progressive disclosure, recovery, and simplicity as hypotheses. Marketplace repetition is not child evidence. |
| `reddit-app-experience-analysis.md` | Reuse counterexamples about notification fatigue, autonomy, novelty, phone distraction, and complex app stacks. The sampled adult discussions do not establish child preferences. |
| `high-level-product-design.md` | Adapt the core day loop, fixed/flexible distinction, reversible state, sensitive notifications, and status language. Replace adult ownership, commercial assumptions, phases, and assistance topology. |
| `documentation-review-and-next-steps.md` | Reuse its evidence gates and implementation/validation distinction. Its current priorities track the adult repository only. |
| `ui-ux-friction-audit-and-requirements.md` | Reuse draft preservation, explicit destructive-action confirmation, focus order, contrast, target size, progressive disclosure, specific feedback, Low Capacity, and no-cache personal pages. Add child comprehension, AAC/low-language, adult-role visibility, and supervised child research. |
| `task-detail-and-complex-work-requirements.md` | Reuse shallow project → task → optional step, separate preferred order/dependency/waiting, and no silent Today promotion. Simplify child-facing presentation and validate limits. |
| `repeatable-activity-history-requirements.md` | Reuse schedule-versus-execution and “missing is unknown.” Do not include health or medication activity history in the foundational child release. Caregiver medication management needs a new clinical/school workflow. |
| `day-context-history-requirements.md` | Defer. Mood, focus, food, sleep, sensory, and disruption histories can become health or inferred-health surveillance when adults can access them. Any later child self-report must be purpose-limited and private by default. |
| `medication-context-support-requirements.md` | Do not transplant the private adult design. Child medication requires guardian authority, prescriber/pharmacy source fidelity, school administration roles, child notice, clinical ownership, and market review. No dose advice remains reusable. |
| `quick-help-mood-energy-design.md` | Adapt deliberate entry, few reversible choices, non-AI playbooks, uncertainty, and human-help routes. Do not reuse adult medication examples or treat it as crisis care. |
| `ai-body-doubling-and-voice-design.md` | Defer AI and voice. Reuse only the principles that non-AI flows remain useful, external transfer is explicit, credentials stay server-side, and model suggestions cannot mutate data silently. |
| Former `assisted-planning-and-guardian-support.md` | Child requirements were consolidated here; adult trusted-person requirements now live in [Adult trusted-person support](../docs/trusted-person-support.md). The former mixed document was removed. |
| Former `calm-break-prototype.md` | The non-punitive calm-break contract was consolidated here and the child-only adult-root document was removed. The executable screen remains synthetic and stores nothing. |
| Former `school-support-sharing-prototype.md` | Teacher/health roles, field-level disclosure, neutral feedback, and child signals were consolidated here. The child-only adult-root document was removed; real sharing remains blocked. |
| `complex-work-prototype-walkthrough.md` | Reuse synthetic-data, task-based, same-device formative research mechanics. Create child-specific protocols before involving minors. |
| `complex-work-prototype-findings-template.md` | Reuse observation, accessibility, and gate-result separation. Add assent, safeguarding, distress, and adult influence fields for child research. |

## Accepted adult ADR disposition

Adult ADRs remain accepted only for the adult application. They are inputs, not
child-product decisions.

| Adult ADR | Child-product treatment |
| --- | --- |
| ADR 0001 — Local PWA | Reuse server rendering, progressive enhancement, CSRF, public-shell-only caching, and testability. Reject local Flask/SQLite as a real multi-person child pilot boundary. |
| ADR 0002 — Local account topology | Do not inherit. Co-resident adult accounts provide no guardian or school authority. Timemanager Kids requires explicit child workspaces and relationships. |
| ADR 0003 — Migrations/hosted target | Reuse ordered migrations, stable IDs, provenance, fail-closed unknown schema, and PostgreSQL direction. Define child-specific tenancy and audit requirements first. |
| ADR 0004 — Export/import | Reuse account/workspace scope, secret exclusion, atomicity, versioning, and conflict rejection. Add child, guardian, disclosure, audit, retention, and legal-hold boundaries. |
| ADR 0005 — Small Today plan | Adapt one anchor plus up to three optional actions as a prototype default. Validate with each age band and do not silently increase or auto-promote. |
| ADR 0006 — Complex-work relationships | Reuse shallow hierarchy, readiness/placement separation, blocker visibility, and no automatic promotion. |
| ADR 0007 — Drop recovery | Reuse confirmed reversible Drop and safe restoration. Child data retention and deletion need a child-specific schedule rather than indefinite inheritance. |

## Cross-document conflicts resolved

### Adult versus child target

The current product design describes adults as the main user and assistance as
a future addition. Timemanager Kids reverses this: the child is the supported
person, and verified adult relationships are foundational.

### Ages 13+ versus ages 8–17

The earlier guardian design intentionally limited its first hosted child pilot
to 13+. Extending to age 8 is not a copy change. It activates an under-13
guardian-operated product gate, stronger age-appropriate transparency, and
market-specific authority/consent controls. Under-13 real data cannot be used
until those controls are independently authorized.

### Excluded school/health data versus requested school/medication support

The earlier assistance design excluded school and health information. The new
product direction intentionally introduces them as separate, later domains.
They remain off by default and blocked behind school verification,
field-specific consent/authority, clinical safety, retention, safeguarding,
and jurisdiction review. Planning permission never implies school or health
permission.

### Private adult medication versus child medication administration

An adult's private medication list cannot model a child's guardian- and
school-mediated medication workflow. The child product separates:

- guardian-provided information;
- current prescriber/pharmacy instructions;
- a school-authorized administration plan;
- a planned occurrence;
- a factual administration record;
- a child's report; and
- an unknown or discrepancy.

It never infers ingestion or gives dose advice.

## Reusable invariants

- Only the minimum input required for the immediate job is mandatory.
- The default daily surface stays small.
- Fixed commitments and flexible actions are distinct.
- Readiness, Today placement, scheduling, and completion are distinct states.
- Missing information remains unknown.
- Consequential actions are previewed, confirmed, reversible where possible,
  account/workspace scoped, and auditable.
- Sensitive content does not enter notification text, analytics, logs, model
  prompts, or public caches.
- Recommendations and generated text are editable suggestions, never facts.
- Recovery does not create shame, punishment, forced catch-up, or silent
  rollover.
- Accessibility and manual assistive-technology validation are release gates.

## Evidence gaps

Before accepting the product design, research must address:

- whether one anchor plus three options is understandable and helpful across
  ages 8–17;
- whether the proposed child signals cover real needs without stigmatizing;
- how children understand guardian, teacher, carer, and health-role access;
- how to present privacy and change history at different developmental levels;
- whether calm-break language feels supportive rather than disciplinary;
- delivery-failure comprehension for children who rely on the help signal;
- unsafe-family, custody-dispute, bullying, staff misuse, and coercion cases;
- accessible alternatives for speech, reading, motor, vision, hearing,
  attention, sensory, and cognitive differences; and
- the effect of school feedback on anxiety, shame, autonomy, and family-school
  conflict.
