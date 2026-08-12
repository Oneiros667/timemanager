---
name: reconcile-time-manager-evidence
description: Reconcile Time Manager implementation, documentation, validation evidence, and Git state to report current status, rank the next safe work, update status documentation, or produce a continuation handoff. Use for requests such as "review project status", "what should we do next?", "rank priorities", "bring the docs up to date", "verify this capability is complete", or "generate a continuation prompt" in the Time Manager repository.
---

# Reconcile Time Manager Evidence

Produce a current, evidence-bounded project assessment. Keep implementation,
automated validation, manual validation, hosted evidence, and proposals distinct.

## Expected inputs

Identify:

- the requested outcome: report, documentation update, implementation choice, or
  continuation handoff;
- the decision lane: product roadmap, validation, publication, or another named
  operational lane;
- the allowed mutation scope;
- the checkout and any named baseline, branch, commit, or worktree constraints;
- the capability, milestone, or publication claim under review.

Treat an audit, review, prioritization request, or prompt-generation request as
read-only unless the user separately authorizes edits or implementation.

## Workflow

1. Establish the baseline.
   - Run `pwd`, `git status --short --branch`, `git rev-parse --show-toplevel`,
     `git rev-parse HEAD`, and a short decorated log.
   - Stop if the checkout is not Time Manager or a required baseline cannot be
     resolved.
   - Record pre-existing modifications and preserve them. Do not use a dirty
     file as comparable committed evidence without labeling it.

2. Load current authority.
   - Read every applicable `AGENTS.md`, then `README.md` and `docs/README.md`.
   - Read `docs/documentation-review-and-next-steps.md`,
     `docs/high-level-product-design.md`, and the accepted decisions relevant to
     the claim.
   - For a whole-project review, read every accepted decision. For a bounded
     capability review, read the decision documents governing that capability
     and its persistence, ownership, migration, and recovery boundaries.
   - For publication questions, also read `docs/publication-readiness.md` and
     current repository controls.
   - Inspect `docs_kids/` directly only when the child-product boundary is in
     scope. Keep it separate from the adult product.

3. Verify claims against the current tree.
   - Trace the owning routes, models, templates, JavaScript, migrations,
     transfer formats, and tests rather than trusting status prose or commit
     titles.
   - Check current Git history and retained validation artifacts when a claim
     depends on a particular revision.
   - Use chat history, summaries, and memory only as discovery leads. If the
     request specifically depends on chat history and no actual transcript or
     explicit export is available, stop and request it.

4. Build an evidence ledger before choosing status or priority. For each claim
   or candidate, record:
   - governing source or accepted decision;
   - current implementation evidence;
   - automated evidence and the exact checkout it covers;
   - manual, participant, hosted, or operational evidence;
   - conflicts, missing gates, and the defensible status.

5. Classify evidence conservatively.
   - `Implemented` requires current executable behavior plus proportionate
     automated verification.
   - `Partial` means a useful slice exists but a named contract or exit gate is
     still open.
   - `Verified` requires the named evidence artifact; configured checks,
     fixtures, synthetic prototypes, and historical results are not substitutes.
   - A committed workflow is not hosted CI evidence. Automated accessibility
     checks are not WCAG conformance. Synthetic walkthroughs are not participant
     validation. Local accounts are not production multi-tenancy.
   - Keep AI, medication, calendar, trusted-person, hosted, migration, mobile,
     and child capabilities proposed or deferred unless current accepted source,
     implementation, and evidence prove otherwise.

6. Select the next work only after reconciliation.
   - Keep product implementation, outstanding validation, and publication
     readiness as separate lanes with separate authority and exit gates. If a
     broad request spans lanes, report the next step in each lane and identify
     which lane controls the requested outcome; do not invent one total order.
   - Follow the current canonical execution order and named exit gates.
   - Apply any documented safety interlock before ordinary roadmap work.
   - Prefer the smallest coherent slice that closes a demonstrated gap without
     silently changing user data, Today placement, account scope, recovery, or
     product boundaries.
   - Do not turn an external/manual validation gate into code work merely to
     keep implementation moving.

7. Apply only authorized changes.
   - For a status-documentation update, change only claims justified by the
     ledger and update nearby cross-references when necessary.
   - For implementation, preserve CSRF, signed-in ownership scope, reversible
     user actions, network-only authenticated HTML, and accepted migration and
     transfer contracts.
   - Keep unrelated dirty files and hunks unstaged and unchanged.

8. Validate proportionately.
   - Confirm tests use temporary paths before running them. Never start the
     normal application or a CLI command against an existing `instance/`
     database for validation. A repository browser test may start its own
     loopback test server only when its application, database, account data,
     browser profile, and artifacts are isolated and synthetic.
   - Use synthetic accounts and tasks only. For direct CLI checks, allocate an
     explicit temporary database and set `TIMEMANAGER_DATABASE` to it.
   - Prefer current repository commands, including focused tests, the full test
     suite when warranted, coverage, compilation, repository hygiene, supported
     migration/CLI checks, and `git diff --check`.
   - Report pass, fail, skip, and unrun results separately. Never carry forward
     an old test count as current evidence.

9. Review the final diff and worktree. Confirm every changed file is in scope
   and distinguish pre-existing changes from this task's changes.

## Output contract

Return, in this order:

1. baseline: checkout, branch, HEAD, divergence, and pre-existing work;
2. concise evidence ledger or capability matrix;
3. defensible status decisions and any documentation changes;
4. ranked next work with the reason and smallest exit gate;
5. validation run with exact results;
6. open manual, hosted, participant, legal, or owner gates;
7. final Git status and untouched pre-existing changes.

For a continuation prompt, include the exact checkout and baseline, one bounded
objective, mutation authority, protected files, current verified evidence,
required validation, stop conditions, and the expected handoff. Do not include
personal data, raw chats, credentials, databases, or screenshots.

## Stop or escalate

Stop and request direction when:

- the required transcript, artifact, checkout, or authority source is absent;
- dirty work overlaps a necessary edit and cannot be preserved safely;
- current code and accepted decisions conflict in a way that changes product
  behavior or migration semantics;
- the next gate requires real personal, health, child, school, account, or
  production data;
- completion depends on manual/participant evidence, an external owner decision,
  publication, deployment, or another state-changing action not authorized by
  the user.
