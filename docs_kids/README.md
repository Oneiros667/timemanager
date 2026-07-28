# Timemanager Kids documentation

Status: proposed separate product; no real child account, guardian relationship,
school connection, medication workflow, or hosted child service is implemented

Research snapshot: 2026-07-28

## Product boundary

**Timemanager Kids** is the working name for a separate application intended
solely for children and young people aged **8 through 17**. Adults participate
only in support roles such as verified guardian, teacher, designated carer, or
school health professional. It is not an adult planner with a child mode.

The current Timemanager repository implements an adult-oriented local pilot.
Its calm-break and school-support screens are synthetic, disabled-by-default
prototypes. They save and transmit no child, family, school, health, or
medication data. Nothing in this folder changes that implementation status.

The child application requires its own hosted authorization, data, safety,
privacy, safeguarding, operational, and market-release boundaries. It may reuse
reviewed generic components, but it must not share the adult application's
sessions, database, exports, analytics identity, notification topics, support
access, or implicit permissions.

## Documents

- [Product design](product-design.md) defines the intended users, outcomes,
  experience, age bands, product principles, scope, and explicit exclusions.
- [Functional requirements](functional-requirements.md) defines testable
  requirements for planning, calm breaks, child-initiated communication,
  school/carer coordination, feedback, and medication boundaries.
- [Roles, permissions, and sharing](roles-permissions-and-sharing.md) defines
  guardian authority, child voice, least-privilege roles, disclosure previews,
  expiry, revocation, and audit behavior.
- [Safety, privacy, and safeguarding](safety-privacy-and-safeguarding.md)
  defines the child-best-interests baseline, sensitive-data controls,
  jurisdiction gates, unsafe-family handling, and prohibited product behavior.
- [Architecture and data](architecture-and-data.md) defines the separate-app
  topology, conceptual information model, authorization checks, notification
  boundary, portability, and operational requirements.
- [UX and accessibility](ux-and-accessibility.md) defines the child-facing
  information hierarchy, evolving-capacity presentation, low-language
  communication, accessibility requirements, and age-appropriate research
  rules.
- [Delivery and validation](delivery-and-validation.md) defines gated
  milestones, verification evidence, usability and safety research,
  acceptance criteria, and launch authorization.
- [Review of current documentation](review-of-current-documentation.md) records
  how every document under `docs/` was assessed and whether its content is
  reused, adapted, deferred, or excluded.

## Evidence and status language

These documents retain the evidence labels used by the adult-product research:

- **Supported:** aligned with a cited clinical guideline, controlled study,
  systematic review, statutory standard, or authoritative technical guidance.
- **Plausible:** a reasoned product hypothesis that still requires validation.
- **Experiential:** a lived-experience or practitioner signal without strong
  controlled evidence.
- **Commercial claim:** a vendor or creator assertion, not efficacy evidence.

Implementation and validation are reported separately:

- **Proposed:** documented but not executable.
- **Synthetic prototype:** executable only with fictional data; no live
  relationship or persistent child data.
- **Implemented:** present in the child application with proportionate tests.
- **Verified:** the named human, safety, clinical, legal, or operational gate
  has recorded evidence.
- **Authorized:** an accountable owner has approved a specific build and market
  after every required gate passed.

No implemented adult feature, synthetic prototype, automated test, or general
legal review authorizes a real child-data pilot.

## Reading order

Start with the product design, then roles and permissions, safety/privacy, and
functional requirements. Architecture follows those policy decisions rather
than defining them. Delivery and validation is the release-control document.
