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
safety language, useful source provenance, and a generally accurate distinction
between the local application and later product phases. The main gap is
execution clarity: the documents do not yet provide one operational view of
what is shipped, what is partial, what decision blocks further work, and what
evidence completes each phase.

No broken local Markdown links, anchors, or reference definitions were found in
the review. The existing test suite passed, but it does not exercise the
client-side timer, Low Capacity behavior, or service-worker behavior in a real
browser.

## Confirmed implementation baseline

The following behavior is implemented:

- local account registration, login, and logout;
- password hashing, signed sessions, and CSRF-protected state-changing forms;
- per-user SQLite task isolation;
- capture to Today or Inbox;
- one changeable daily highlight;
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
- export/import, an application-managed backup flow, or schema migrations;
- stable installation/public object identifiers for hosted transfer;
- Google Calendar integration;
- guardian or trusted-person assistance;
- hosted accounts, local-to-online migration, native applications, or AI.

The following behavior is partial and must not be described as the full proposed
capability:

| Capability | Implemented slice | Missing contract |
| --- | --- | --- |
| Small Today plan | Today and a single highlight exist | No limit or explicit overflow/triage for optional tasks |
| Low Capacity | CSS hides secondary Today content and stores a browser preference | No per-account state, current-time/commitment view, critical-item routing, smallest-action selection, or Reset |
| Focus | A non-persisted countdown can start, pause, continue, and reset | No session intention record, distraction capture, transition protection, next commitment, or actual-time history |
| Backup | The README tells an operator to back up `instance/` | No export format, restore rehearsal, completion report, or migration-safe provenance |

## Findings that require decisions

### D1: Health-data boundary

Priority: resolved in product design on 2026-07-24

The resolved boundary is:

- the local and first hosted pilots do not solicit, infer, categorise, or
  provide specialist health, diagnosis, medication, or treatment
  functionality;
- users may enter sensitive information in private free-text tasks, so all task
  content is treated as potentially sensitive and private by default;
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

The design decision is complete. Implementation and release evidence remain
required before notification delivery or assistance features can ship.

### D2: Milestone terminology and status

Priority: blocking

The documentation uses `first validation`, `first working version`, `local
pilot`, `first pilot`, `first release`, and `hosted release`. The feature table
also uses `Yes` for planned first-validation scope, which can be mistaken for
implementation status.

Define these milestones once and use them consistently. Add a
`Implemented`/`Partial`/`Not started`/`Blocked` status to each current milestone
capability. Record whether the Phase 0 interviews and prototype validation
occurred; if they did, link the evidence. Otherwise keep Phase 0 unverified.

Completion evidence:

- milestone terms have one meaning across the documentation;
- every Phase 1 capability has a current status and exit criterion;
- validation artifacts are linked or explicitly recorded as absent.

### D3: Local account topology

Priority: high

The high-level design describes a single-user local application, while the
implementation supports multiple registered accounts with per-user task
isolation.

Choose and document either:

- one local installation with multiple isolated local accounts; or
- a deliberately single-account pilot, with registration/isolation retained
  only as preparation for hosted accounts.

Completion evidence:

- README, product design, test assumptions, backup scope, and migration scope
  describe the same account model.

### D4: Product and feature phase naming

Priority: medium

The main roadmap defers AI until product Phase 4, while the optional AI design
uses `Phase 1`, `Phase 2`, and `Phase 3` for its own rollout. Rename the latter
to `AI deployment stage` or state explicitly that all of its stages begin only
after the main roadmap's AI release gate.

The assisted-planning note also calls Timemanager a subscription product. Move
that assumption into the high-level product design as a resolved decision or
label it as unconfirmed.

Completion evidence:

- phase numbers cannot be confused across documents;
- the business-model status has one authoritative location.

### D5: Assisted-planning pilot topology

Priority: blocking before assisted-planning implementation

The roadmap includes guardian and trusted-person support in the first pilot, but
the safety design correctly prevents remote invitations and real shared child
workspaces from bypassing hosted authorization, verification, and legal gates.

Define whether early validation uses:

- synthetic family and task data;
- same-device role simulation;
- supervised research sessions with an approved protocol; or
- a hosted, server-authorized pilot after all release gates pass.

An email invitation alone must never be treated as proof of guardianship.

Completion evidence:

- documented research topology and permitted data;
- child-data impact/privacy assessment;
- abuse and unsafe-family threat model;
- jurisdiction and counsel gate for every market using real child data.

## Ordered execution plan

| Order | Work item | Initial status | Exit gate |
| --- | --- | --- | --- |
| 0.1 | Resolve D1-D5 and align the documentation | In progress: D1 resolved; D2-D5 open | No contradictory product boundaries; one milestone/status model |
| 0.2 | Add schema migrations and installation/public object provenance | Not started | Existing database upgrades without data loss; schema version is inspectable |
| 0.3 | Add export, restore, and migration-fixture foundations | Not started | Export/import round trip is idempotent and tested; secrets are excluded |
| 1.1 | Enforce a deliberately small active Today plan | Not started | One highlight plus the chosen optional-task limit; overflow remains recoverable |
| 1.2 | Add task detail, next action, and definition of done | Not started | Capture remains title-only; added structure is optional and editable |
| 1.3 | Add Review and consequence-aware Reset/recovery | Not started | No silent rollover; stale items can be kept, renegotiated, delegated, replaced, or dropped |
| 1.4 | Add manually entered fixed commitments and transition boundaries | Not started | Fixed and flexible objects remain distinct; next commitment stays visible |
| 1.5 | Complete Low Capacity semantics | Not started | Same underlying data; critical commitments, one action, capture, and Reset remain available |
| 1.6 | Extend focus into an optional bounded session record | Not started | Intention, boundary, interruption-tolerant actuals, and next-step outcome are user-controlled |
| 1.7 | Validate the complete non-AI day loop | Not started | Browser/accessibility tests plus recorded user-research evidence |
| 2.1 | Implement the notification attention/privacy contract | Blocked by 1.7 | Independent importance/privacy; private default; Sensitive payload and device views contain no details |
| 2.2 | Add Google Calendar behind explicit confirmation | Blocked by 1.7 | Provenance, timezone, recurrence scope, conflicts, provider failures, and external-notification privacy boundaries are visible |
| 2.3 | Prototype assisted planning under the approved topology | Blocked by D5 | Server-side scope, proposals, audit, expiry, revocation, disclosure previews, and safety gates pass |
| 3 | Build hosted accounts and rehearse one-time migration | Blocked by phases 1-2 | Tenant isolation, production operations, and migration evidence pass |
| 4 | Consider native clients and optional AI | Deferred | Separate validation and privacy/cost/safety approval |

## Verification work required

Maintain the current server-side test coverage and add proportionate tests as
each slice lands:

- migration tests starting from every supported prior schema;
- export/import idempotency, conflict, and secret-exclusion tests;
- task ownership and assistance-permission tests for every new query or
  mutation;
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
