# Documentation review and next steps

Status: active project tracking

Updated: 2026-07-24

## Purpose

This note records the 2026-07-24 review of the repository documentation against
the implemented local PWA. It turns the review findings into an ordered,
evidence-gated work plan.

The product design remains proposed unless this note or an accepted decision
document identifies behavior as implemented. Statuses in this note must be
updated from repository, test, research, or release evidence rather than from
intent.

## Review outcome

The research and product documentation have a strong evidence model, clear
safety language, useful source provenance, and an explicit distinction between
the local application and later product phases. The original review identified
execution clarity as the main gap; this tracking note now provides the
operational view of what is implemented, partial, blocked, and gated by further
evidence.

No broken local Markdown links, anchors, or reference definitions were found in
the review. The automated suite now covers server-side account isolation,
schema upgrades, migration recovery, and export/import behavior, but it does
not exercise the client-side timer, Low Capacity behavior, or service-worker
behavior in a real browser.

## Confirmed implementation baseline

The following behavior is implemented:

- local account registration, login, and logout;
- password hashing, signed sessions, and CSRF-protected state-changing forms;
- per-user SQLite task isolation;
- SQLAlchemy Core persistence and ordered Alembic schema revisions;
- automatic upgrade of the exact legacy users/tasks database with
  pre-migration snapshot recovery;
- stable public UUIDs, installation origin, and positive revisions for users
  and tasks;
- versioned account-scoped JSON export/import for the current profile and task
  model, with operator CLI commands, secret exclusion, provenance retention,
  and fail-closed revision conflicts;
- capture to Today or Inbox;
- one changeable daily highlight and at most three optional active Today
  actions;
- explicit recoverable Today overflow with user-controlled activation,
  highlight replacement, and save-for-later actions;
- task completion, restoration, deliberate dropping, and move-to-Today;
- a browser-local Low Capacity display toggle;
- a 5/15/25-minute client-side focus timer;
- responsive server-rendered pages;
- an installable PWA shell whose authenticated navigation remains network-only.

The following product-design capabilities are not implemented:

- fixed commitments or calendar objects;
- a task detail view, next action, or definition of done;
- a Review destination or recovery/reset flow;
- transition or leave-by protection;
- persisted focus sessions or estimate-versus-actual learning;
- authenticated self-service export/restore, credential recovery, or an
  application-managed general backup/restore flow;
- Last Done tracked activities, schedules, occurrences, or execution history;
- Google Calendar integration;
- guardian or trusted-person assistance;
- hosted accounts, local-to-online migration, native applications, or AI.

The following behavior is partial and must not be described as the full proposed
capability:

| Capability | Implemented slice | Missing contract |
| --- | --- | --- |
| Low Capacity | CSS hides secondary Today content and stores a browser preference | No per-account state, current-time/commitment view, critical-item routing, smallest-action selection, or Reset |
| Focus | A non-persisted countdown can start, pause, continue, and reset | No session intention record, distraction capture, transition protection, next commitment, or actual-time history |
| Backup and portability | Operator `instance/` backup, automatic pre-migration recovery, and versioned account/task CLI export/import | No self-service flow, credential recovery, full-account-type coverage, full operational restore rehearsal, or hosted adapter |

## Findings that require decisions

### D1: Health-data boundary

Priority: scope resolved; privacy/legal release gate remains

The resolved boundary is:

- the Phase 1 local pilot and Phase 3 hosted release do not solicit, infer,
  categorise, or
  provide specialist health, diagnosis, medication, or treatment
  functionality;
- generic Last Done tracking intentionally supports private user-authored
  medication labels and execution history, but provides no dose, adherence,
  treatment, or missed-dose advice;
- medication-labelled histories are intentional health-data processing and
  require an applicable lawful basis/condition, privacy assessment, security
  controls, and jurisdiction review before hosted release;
- users may enter sensitive information in private free-text tasks and tracked
  activities, so all such content is treated as potentially sensitive and
  private by default;
- assistance workspaces do not provide health-specific fields or workflows and
  do not bulk-share private task content;
- every shared item receives an explicit disclosure preview; automatic
  detection of sensitive free text is not promised;
- notification importance and privacy are independent;
- account-wide notification details are hidden by default and users may opt out
  for Standard cues;
- a cue marked Sensitive always emits a generic, detail-free notification and
  contains no sensitive text in its push payload; the user must deliberately
  remove the classification before details can appear;
- external calendar providers control their own notifications, so every
  sensitive calendar write requires a boundary disclosure and a privacy-safe
  external-title choice.

The product scope is resolved. Implementation, privacy/legal, medication-safety,
and release evidence remain required before hosted activity tracking,
notification delivery, or assistance features can ship. Detailed requirements
are in
[Repeatable activity and execution-history requirements](repeatable-activity-history-requirements.md).

### D2: Milestone terminology and status

Priority: resolved in product design on 2026-07-24

The canonical product milestones are:

- Phase 0 — Prototype validation;
- Phase 1 — Local pilot;
- Phase 2 — Integrated local pilot;
- Phase 3 — Hosted release; and
- Phase 4 — Later extensions.

Delivery uses `Implemented`, `Partial`, `Not started`, `Blocked`, and `Deferred`.
User-research evidence is tracked separately as `Verified` or `Unverified`.
This prevents implementation progress from being presented as evidence that a
product hypothesis has been validated.

The capability catalogue records a target milestone and current delivery status
instead of using `Yes` or `No`. No Phase 0 interview, prototype, or usability
artifact is currently recorded in the repository, so its evidence status is
Unverified. The authoritative definitions and current capability statuses are
in the
[high-level product design](high-level-product-design.md#canonical-milestones-and-statuses).

### D3: Local account topology

Priority: resolved in product design on 2026-07-24

One trusted Phase 1 local installation may contain multiple isolated accounts,
matching the implemented registration and per-user ownership model.

- Every user-owned object, query, mutation, export, deletion, restore, and
  hosted migration is scoped to one authenticated account.
- Co-residency creates no household, guardian, helper, or sharing relationship.
- Registration is not evidence of guardianship or trust.
- The installation is limited to a trusted machine and local network; it is not
  a public multi-tenant service.
- The installation operator can access the database, generated secret, and
  backups at the filesystem level.
- An `instance/` backup contains every account, while user-facing export and
  migration remain per-account.

The durable rationale and consequences are recorded in
[ADR 0002: Local account topology](decisions/0002-local-account-topology.md).

### D4: Product and feature phase naming

Priority: resolved in product design on 2026-07-24

The optional AI rollout uses `AI deployment stage A`, `B`, and `C`, all within
product Phase 4. These stages no longer collide with the canonical product
milestones and do not create separate delivery commitments.

The authoritative commercial structure is:

- subscription per primary user;
- monthly billing or discounted annual billing with the same entitlements;
- web and future native-mobile access in the base subscription;
- one guardian companion seat for a child or one trusted-support companion seat
  for an adult;
- a companion seat provides scoped support access, not an independent personal
  workspace; and
- optional advanced or future capabilities may be transparent one-off
  purchases, but core, accessibility, privacy, safety, export, deletion, and
  companion access remain in the base subscription.

Payment is never evidence of identity, age, guardianship, consent, or authority.
Exact prices and other billing mechanics remain decisions for implementation.
The authoritative detail is in the
[high-level product design](high-level-product-design.md#commercial-model).

### D5: Assisted-planning pilot topology

Priority: resolved in product design on 2026-07-24

The approved topology separates interface validation from live shared
relationships:

- Phase 2 uses synthetic family, relationship, and task data with same-device
  role simulation. It creates no remote invitations or persistent real child
  or assistance workspaces.
- Supervised sessions may involve real participants under an approved protocol,
  but use synthetic scenarios. Consented, minimised, de-identified research
  notes remain outside Timemanager.
- Real adult trusted-support relationships require a hosted, server-authorized
  pilot after authentication, authorization, audit, expiry, revocation,
  disclosure, and abuse-response gates pass.
- Real child workspaces additionally require country-specific legal/privacy
  approval, guardian-authority verification, a child-data impact assessment,
  an unsafe-family/coercion threat model, child-visible privacy, and tested
  deletion and incident-response procedures.

Email, payment, local-account co-residency, and possession of an invitation
never prove guardianship. The detailed topology and release evidence are in
[Assisted planning and guardian support](assisted-planning-and-guardian-support.md#validation-and-release-topology).

## Ordered execution plan

| Order | Work item | Current status | Exit gate |
| --- | --- | --- | --- |
| 0.1 | Resolve D1-D5 and align the documentation | Completed 2026-07-24 | No contradictory product boundaries; one milestone/status model |
| 0.2 | Add schema migrations and installation/public object provenance | Completed 2026-07-24 | Existing database upgrades without data loss; schema revision is inspectable |
| 0.3 | Add export, restore, and migration-fixture foundations | Completed 2026-07-24 | Export/import round trip is idempotent and tested; secrets are excluded |
| 1.1 | Enforce a deliberately small active Today plan | Completed 2026-07-24 | One highlight plus the chosen optional-task limit; overflow remains recoverable |
| 1.2 | Add task detail, next action, and definition of done | Not started | Capture remains title-only; added structure is optional and editable |
| 1.3 | Add Review and consequence-aware Reset/recovery | Not started | No silent rollover; stale items can be kept, renegotiated, delegated, replaced, or dropped |
| 1.4 | Add manually entered fixed commitments and transition boundaries | Not started | Fixed and flexible objects remain distinct; next commitment stays visible |
| 1.5 | Complete Low Capacity semantics | Not started | Same underlying data; critical commitments, one action, capture, and Reset remain available |
| 1.6 | Extend focus into an optional bounded session record | Not started | Intention, boundary, interruption-tolerant actuals, and next-step outcome are user-controlled |
| 1.7 | Add generic Last Done activities and execution history | Not started | Manual create/log/query/correct/export passes exactness, privacy, time, and medication-safety criteria |
| 1.8 | Validate the complete non-AI day loop | Not started | Browser/accessibility tests plus recorded user-research evidence |
| 2.1 | Implement the notification attention/privacy contract | Blocked by 1.8 | Independent importance/privacy; private default; Sensitive payload and device views contain no details |
| 2.2 | Add Google Calendar behind explicit confirmation | Blocked by 1.8 | Provenance, timezone, recurrence scope, conflicts, provider failures, and external-notification privacy boundaries are visible |
| 2.3 | Prototype assisted planning under the approved topology | Blocked by 1.8 | Synthetic same-device roles, proposals, audit, expiry, revocation, disclosure previews, and safety gates pass |
| 3 | Build hosted accounts and rehearse one-time migration | Blocked by phases 1-2 | Tenant isolation, production operations, and migration evidence pass |
| 4 | Consider native clients and optional AI | Deferred | Separate validation and privacy/cost/safety approval |

## Verification work required

Maintain the current server-side test coverage and add proportionate tests as
each slice lands:

- migration tests starting from every supported prior schema;
- export/import idempotency, conflict, and secret-exclusion tests;
- task ownership and assistance-permission tests for every new query or
  mutation;
- assisted-prototype tests proving that Phase 2 uses synthetic same-device
  roles, sends no remote invitation, calls no external provider, and can reset
  the simulated workspace;
- hosted assistance-gate tests proving that real adult relationships require
  server authorization and that real child workspaces remain unavailable
  without the applicable market and guardian-authority approval;
- browser tests for capture, highlight limits, Low Capacity, focus boundaries,
  Reset, and offline navigation;
- an assertion that authenticated task pages are never stored in the service
  worker cache;
- notification tests proving that Sensitive titles, notes, people, locations,
  calendar details, and revealing action labels never enter push payloads,
  device previews, notification history fixtures, or mirrored-device fixtures;
- account-setting tests proving that opting out of generic previews affects
  only Standard cues and cannot override a Sensitive cue;
- external-calendar tests proving that a sensitive write requires the provider
  boundary disclosure and a privacy-safe external-title decision;
- repeatable-activity tests proving explicit execution provenance, exact
  day/time-slot answers, no-log-as-unknown semantics, duplicate warnings,
  backdating, timezone behavior, correction, export, and deletion;
- reflection-marker tests proving stable meanings across activity executions
  and task completions, no more than four quick choices, per-dimension
  exclusivity, the event selection limit, accessible text labels, no automatic
  selection, and Sensitive-default privacy;
- medication-safety tests proving that missing logs never become claims of a
  missed dose and never produce dose advice;
- keyboard, focus-order, screen-reader, reduced-motion, and contrast checks;
- timezone and daylight-saving tests before calendar integration;
- explicit-preview and failure-state tests for every external calendar write.

Python coverage alone is not evidence that the progressive client-side behavior
or PWA privacy boundary works in a browser.

## Research and review gates

Before expanding the feature set:

1. run or document the Phase 0 prototype tasks for capture, launch, transition,
   recovery, and Low Capacity;
2. test both minimalist and feature-rich-tool users;
3. record post-novelty and return-after-absence evidence, not only onboarding
   reactions;
4. preserve functional outcomes and wellbeing guardrails rather than optimizing
   task count, app opens, or streaks;
5. treat assistant-, calendar-, and helper-generated changes as editable
   proposals until the user explicitly confirms them.

The targeted source check performed for this review found the central clinical
and current regulatory/API claims consistent with the cited primary sources:

- [NICE NG87 recommendations](https://www.nice.org.uk/guidance/ng87/chapter/recommendations)
- [Komatsu et al. CBT component network meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11683884/)
- [BMJ ADHD interventions umbrella review](https://www.bmj.com/content/391/bmj-2025-085875)
- [OAIC draft Children's Online Privacy Code status](https://www.oaic.gov.au/news/media-centre/oaic-releases-exposure-draft-of-the-childrens-online-privacy-code)
- [ICO Children's Code introduction](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- [European Commission safeguards for children's data](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/are-there-any-specific-safeguards-data-about-children_en)
- [ICO special-category and health-data guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/)
- [OpenAI API data controls](https://developers.openai.com/api/docs/guides/your-data#default-usage-policies-by-endpoint)

This was a targeted validation of high-risk and time-sensitive claims, not a new
systematic review of every cited source. Recheck current legal, regulatory, and
provider-specific claims before implementing or releasing the affected feature.

## Maintenance rule

Update this note whenever a tracked item changes state. Link the commit, test,
research artifact, decision document, or release evidence that justifies the
change. Do not mark a phase complete because code exists; mark it complete only
when its stated exit gate passes.
