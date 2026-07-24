# ADHD-friendly time-management research

Research snapshot: 2026-07-24

This folder contains the domain research for a time-management system intended
to help an adult with ADHD move through a day. It is research and product-design
guidance, not medical advice or a substitute for ADHD assessment or treatment.

## Documents

- [High-level product design](high-level-product-design.md) translates the
  research into the proposed user journey, feature set, functional rules,
  information model, confirmed deployment path, scope, and delivery phases.
- [Documentation review and next steps](documentation-review-and-next-steps.md)
  records the current implementation gaps, decisions, ordered execution plan,
  and evidence gates used for project tracking.
- [Repeatable activity and execution-history requirements](repeatable-activity-history-requirements.md)
  defines Last Done tracking, exact answer semantics, schedules, execution
  history, shared reflection markers, task/calendar links, privacy, and
  medication-safety gates.
- [Assisted planning and guardian support](assisted-planning-and-guardian-support.md)
  defines guardian-supported child planning and adult trusted-person support,
  including permissions, proposals, privacy boundaries, and release gates.
- [ADR 0001: Local PWA architecture](decisions/0001-local-pwa-architecture.md)
  records the accepted Flask, SQLite, server-rendered UI, authentication, and
  service-worker boundaries for the Phase 1 local pilot.
- [ADR 0002: Local account topology](decisions/0002-local-account-topology.md)
  records the trusted multi-account installation model, account isolation,
  operator-access boundary, and account-scoped export and migration rules.
- [ADR 0003: Database migrations and hosted database target](decisions/0003-database-migrations-and-hosted-target.md)
  records the SQLite/SQLAlchemy local architecture, Alembic upgrade and recovery
  contract, stable provenance, and PostgreSQL hosted target.
- [ADR 0004: Account export and import contract](decisions/0004-account-export-import-contract.md)
  records the implemented versioned JSON boundary, account scope, credential
  exclusions, idempotency rules, conflict policy, and current recovery limits.
- [ADR 0005: Small active Today plan](decisions/0005-small-active-today-plan.md)
  records the highlight-plus-three capacity, active/overflow state semantics,
  explicit recovery actions, migration behavior, and import boundary.
- [ADHD time-management domain research](adhd-time-management-domain-research.md)
  synthesises clinical guidance, cognitive and motivational theories, tested
  behavioural methods, common "life hacks", and their implications for a
  software system.
- [Reference-system analysis](reference-systems-analysis.md) examines Ruri
  Ohama's Kaizen System and each supplied Notion template without conflating the
  separate products. It identifies what to borrow, what to test, and what to
  avoid.
- [Reddit app-experience analysis](reddit-app-experience-analysis.md) extracts
  recurring needs, adoption failures, and conflicting preferences from the
  three supplied r/ADHD discussions. These are lived-experience signals rather
  than efficacy evidence.
- [Optional AI body-doubling and voice design](ai-body-doubling-and-voice-design.md)
  specifies a privacy-controlled AI companion, its safety boundaries, and a
  local-container-to-mobile rollout architecture.

## Reading the evidence labels

- **Supported**: directly aligned with clinical guidance, randomised trials,
  systematic reviews, or tested adult-ADHD treatment protocols.
- **Plausible**: follows from supported mechanisms or general behavioural
  evidence, but the exact product feature has not been validated for ADHD.
- **Experiential**: commonly recommended by practitioners or people with ADHD,
  with little direct controlled evidence.
- **Commercial claim**: asserted by a product creator or marketplace listing;
  useful as a design hypothesis, not evidence of effectiveness.

The most important distinction throughout is between an intervention that helps
someone function and a treatment that reduces core ADHD symptoms. A planning
tool can support the former; it should not claim the latter without clinical
evidence and appropriate regulation.
