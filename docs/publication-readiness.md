# Publication-readiness audit

Status: **READY FOR SOURCE-ONLY PUBLICATION AFTER FINAL-CANDIDATE CI AND EXPLICIT OWNER VISIBILITY APPROVAL**

Audit date: 2026-08-11; evidence updated 2026-08-13

Audit lineage: the initial review started on branch `master` at
`faed91edbc3a81e87becf1a5d95f15f0840b9f4d`. The final refresh started from a
clean `main` at `9412082509a3810f035dc3eed66519719d6d802d`, even with
`origin/main`. Publication must use the reviewed final candidate associated
with a passing hosted Quality run, not one of these earlier snapshots by name
alone.

## Scope and evidence boundary

This audit covers the current tracked tree, reachable local Git history,
application/security boundaries, documentation claims, committed assets,
dependency metadata available in the locked local environment, and local
verification, and the hosted GitHub Actions evidence recorded below. It does
not authorize a visibility change, establish legal ownership, rewrite history,
perform a penetration test, or complete manual accessibility/usability
acceptance.

The repository remains an early local Flask/SQLite pilot. It is not a public
multi-tenant service, clinical product, completed child application, AI
assistant, calendar integration, hosted migration product, or supported
self-service restore system.

## Owner decisions recorded 2026-08-12

- **Licence:** Apache License 2.0, recorded in `LICENSE` and package metadata.
- **Reachable history:** retain it without rewriting. The owner accepts that
  public visibility would expose the previously identified screenshots,
  documentation wireframe name, and Git author identity/email preserved in the
  repository history.
- **Ownership and redistribution:** the owner attests that they own or have
  authority to publish the application source, original assets, screenshots,
  documentation, and adapted research under Apache-2.0.
- **Project contact:** the owner designated the address published in
  `SECURITY.md` for private security contact and other repository email-contact
  requirements.

## Publication scope and open validation gates

The proposed visibility change is **source-only publication** of the documented
local development/pilot repository. It does not deploy the application, create
a hosted service, establish production security, or validate accessibility,
usability, or clinical outcomes.

Independent security review and penetration testing remain required before an
internet-facing deployment or production-security claim. Manual keyboard and
screen-reader review, 200%/400% zoom, forced-colors, broader-browser and
real-device checks, and participant usability testing remain required before
the corresponding accessibility, compatibility, or validated-usability claims.
These open gates do not block source-only publication while the README and this
audit keep the limitations prominent and precise. Automated checks must not be
described as WCAG conformance or product validation.

## Privacy and security findings

### Remediated in the current tree

- Replaced identifying screenshots with repeatable synthetic captures from
  a temporary database and browser profile; PNG text/time metadata is rejected
  by the repository checker.
- Replaced the personal first name in the documentation wireframe.
- Removed debug mode from the legacy `python main.py` path by routing it through
  the same loopback-only CLI entry point as `uv run timemanager`.
- Restricted login and return-path redirects to origin-local absolute paths,
  including rejection of scheme-relative and backslash forms.
- Added `no-store` for dynamic HTML, while retaining the public offline shell,
  and added restrictive object, camera, microphone, and geolocation policies.
- Expanded ignore rules for databases, backups, exports, environment files,
  logs, coverage, and browser artifacts.
- Added a local checker for tracked/untracked sensitive filenames,
  credential-shaped strings, non-example emails, private absolute paths,
  Markdown links, PNG metadata, and immutable GitHub Action pins.

### Confirmed safeguards

- Werkzeug password hashing; signed, HTTP-only, SameSite=Lax sessions; global
  CSRF validation on POST forms; and generic login failure text.
- Account ownership predicates on task, project, component, wait, Remember, and
  transfer paths, backed by negative tests.
- Account-scoped export excludes password hashes, application/session secrets,
  internal database IDs, and other accounts. Export uses mode `0600` and refuses
  overwrite.
- Import validates exact supported shapes and relationships, resolves revisions
  fail-closed, and applies changes atomically.
- SQLite schema upgrades recognize only the exact supported legacy shape,
  create pre-migration backups, and restore on failure.
- The service worker caches only public shell/static assets and fetches
  authenticated navigation from the network.
- Browser-local drafts are account/object/form/tab scoped, expire after 24
  hours, and are cleared for the account on sign-out.
- Prototypes are disabled by default, `no-store`, browser-memory-only, and use
  fictional content.

### Remaining local-pilot limitations

- The installation operator and host/browser administrators can read local
  account data and drafts.
- The supported local HTTP flow cannot set Secure cookies; it must remain on a
  trusted loopback installation.
- There is no login rate limiting, credential recovery, production WSGI/TLS
  configuration, production logging policy, hosted authorization layer,
  operational backup service, or penetration-test evidence.

## Repository and history scan

- No tracked SQLite database, migration backup, instance directory, account
  export, environment file, certificate/private key, log, coverage report,
  Playwright trace, or browser profile was found in the current tree.
- Current-tree and revision-by-revision history scans found no private-key,
  common token-prefix, or credential-bearing database-URL pattern. Gitleaks
  8.30.1 independently reported no leaks across 30 reachable commits or the
  candidate directory.
- One historical `DATABASE_URL=` search marker was classified as the benign
  environment-variable configuration key, with no credential value.
- Reserved example-domain email addresses and fictional test password strings
  remain intentionally in tests and examples.
- The largest reachable blobs are the historical screenshots and lock file;
  no unexpectedly large generated archive was found.

The Gitleaks release checksum was verified against its upstream release
checksum before execution. TruffleHog, detect-secrets, and ExifTool were not
run. Pattern scanning reduces risk but does not prove absence of all sensitive
data.

## Licensing and third-party material

Locked runtime/development dependency metadata in the local environment, plus
the pinned build backend's cached package metadata, reports:

| Dependency | Version | Reported license |
| --- | ---: | --- |
| Alembic | 1.18.5 | MIT |
| blinker | 1.9.0 | MIT |
| click | 8.4.2 | BSD-3-Clause |
| coverage | 7.15.2 | Apache-2.0 |
| Flask | 3.1.3 | BSD-3-Clause |
| greenlet | 3.5.4 | MIT AND PSF-2.0 |
| Hatchling (build backend) | 1.32.0 | MIT |
| iniconfig | 2.3.0 | MIT |
| itsdangerous | 2.2.0 | BSD |
| Jinja2 | 3.1.6 | BSD |
| Mako | 1.3.12 | MIT |
| MarkupSafe | 3.0.3 | BSD-3-Clause |
| packaging | 26.2 | Apache-2.0 OR BSD-2-Clause |
| SQLAlchemy | 2.0.51 | MIT |
| Playwright | 1.61.0 | Apache-2.0 |
| pluggy | 1.6.0 | MIT |
| pyee | 13.0.1 | MIT |
| Pygments | 2.20.0 | BSD-2-Clause |
| pytest | 9.1.1 | MIT |
| pytest-cov | 6.3.0 | MIT |
| typing_extensions | 4.16.0 | PSF-2.0 |
| Werkzeug | 3.1.8 | BSD-3-Clause |

The application uses system font stacks and an in-repository SVG/PNG icon set;
no external web font, analytics script, copied icon library, or bundled
third-party research document was found. Research references and short
illustrative quotations still require owner/editorial review as part of the
ownership attestation. This is an engineering inventory, not legal advice or a
complete transitive license opinion.

## Screenshots and synthetic data

The publication images are generated by
`scripts/capture_synthetic_screenshots.py` using a temporary SQLite database,
loopback server, temporary browser context, reserved example-domain account,
and fictional planning content. The procedure does not read `instance/` or an
existing `TIMEMANAGER_DATABASE`.

Expected current outputs:

- `docs/assets/synthetic-today.png`;
- `docs/assets/synthetic-low-capacity.png`;
- `docs/assets/synthetic-later.png`;
- `docs/assets/synthetic-projects.png`;
- `docs/assets/synthetic-recently-dropped.png`; and
- `docs/assets/synthetic-mobile-today.png`.

Every image must be visually reviewed after regeneration. Passing metadata and
content checks does not make a screenshot usability evidence.

## CI and repository controls

`.github/workflows/quality.yml` uses read-only contents permission,
`persist-credentials: false`, immutable full-SHA action references with version
comments, Python 3.11, uv 0.12.3, `uv sync --locked`, the locked Playwright
browser, temporary SQLite, repository/link checks, coverage, compilation,
migration/CLI checks, and no service credentials or artifact uploads.

On 2026-08-13, repository settings were configured to require SHA-pinned GitHub
Actions, enable Dependabot vulnerability alerts and automated security fixes,
and add a portfolio description and relevant repository topics. A branch
ruleset cannot be configured for this private personal repository on the
current GitHub plan; add the required-Quality/no-force-push ruleset immediately
after public visibility makes that control available.

The first hosted run on `313ae7dd98e7241174b1dbce1134e0d09eaa7866` failed
before creating a job because the workflow used a runner-only context in
job-level environment configuration. Commit
`a51d3da26c2d59e710643a8f445c7e3586d71864` moved the temporary database path
configuration onto the runner. GitHub Actions run `31603140723` then completed
successfully on that exact commit. The retained run is
<https://github.com/Oneiros667/timemanager/actions/runs/31603140723>.
Repository hygiene, locked installation, Playwright browser installation, the
coverage test suite, compilation, migration/operator commands, lock
verification, and whitespace checks all passed.

GitHub Actions run `31626178186` subsequently completed successfully on exact
commit `9412082509a3810f035dc3eed66519719d6d802d`. It retained the same result:
**103 passed**, **87% total Python coverage**, repository hygiene, compilation,
migration/operator commands, lock verification, and whitespace checks all
passed. The retained run is
<https://github.com/Oneiros667/timemanager/actions/runs/31626178186>.

## Local verification evidence

The following checks ran locally against this uncommitted candidate on
2026-08-11 using Python 3.11.15 and uv 0.12.3:

- `uv sync --locked`: passed with 24 resolved packages;
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest`: **103 passed** in 83.54 s;
- `uv run pytest --cov=timemanager --cov-report=term-missing`:
  **103 passed**, **87% total Python coverage**, in 93.29 s;
- focused auth/PWA regressions: **13 passed**;
- automated browser suite: 21 tests included in the passing full suite;
- migration tests: 15 tests included, covering a fresh database, every
  supported revision `0001` through `0006`, exact legacy recognition, backup,
  restoration, and fail-closed cases;
- account-transfer tests: 15 tests included, covering scope, secret exclusion,
  revision handling, conflicts, constraints, and atomicity;
- `uv run python -m compileall -q main.py timemanager tests migrations scripts`:
  passed;
- isolated `schema-version`: `0007 (latest: 0007)`;
- isolated cross-installation synthetic export/import: one task inserted,
  export mode `0600`, secret exclusion confirmed; a same-installation
  cross-account collision was also rejected fail-closed as designed;
- `python main.py` with an explicit temporary database: loopback listener
  observed, debug/reloader markers absent;
- `uv run python scripts/check_repository.py`: passed for 118 candidate files,
  including local documentation links, action pins, candidate-tree content,
  and PNG metadata;
- all six new screenshots were visually inspected at original resolution and
  contained only fictional/sample content;
- `uv lock --check`: passed; and
- `git diff --check`: passed.

On 2026-08-12, after the owner selected Apache-2.0:

- `LICENSE` was byte-compared with the official Apache License 2.0 text;
- package metadata reported `License-Expression: Apache-2.0`;
- a temporary source distribution included `LICENSE`;
- a temporary wheel included `dist-info/licenses/LICENSE`; and
- locked sync, repository hygiene, lock, and whitespace checks passed again.

On 2026-08-13, during the final-candidate refresh:

- Gitleaks 8.30.1 reported no leaks in 30 reachable commits or the candidate
  directory;
- pip-audit identified `PYSEC-2026-1845` in the development-only pytest 8.4.2
  dependency; the lock was upgraded to pytest 9.1.1, above the fixed 9.0.3
  release, and the refreshed dependency set reported no known vulnerabilities;
- Bandit 1.9.4 reported zero medium/high findings and five reviewed low findings:
  two deliberately fictional screenshot credentials and three fixed-argument
  `git ls-files` subprocess/import warnings in the repository checker; and
- the full browser-inclusive suite passed on pytest 9.1.1: **103 passed** with
  **87% total Python coverage**.

No Ruff configuration or supported standalone formatter exists, so no Ruff or
format claim is made. External-link reachability, TruffleHog/detect-secrets,
broader browsers, manual accessibility, real-device, penetration, and
participant checks were not run and remain open under the scope defined above.

## Exact pre-publication steps

Completed owner-controlled steps are recorded above: Apache-2.0 was selected,
reachable history was retained, ownership and redistribution authority were
attested, a specific private security contact was designated, and the reviewed
publication-preparation changes were committed as `880f6b23d24f`. The contact
and attestation update was committed as `313ae7dd98e`; the corrected hosted
workflow passed on `a51d3da26c2d`; and the later exact-main run passed on
`9412082509a3`. The independent/manual gates are explicitly scoped above.

1. Review and merge the final publication-readiness change only after its exact
   head commit has a passing hosted Quality run and the final current-tree and
   full-history scans remain clean.
2. Confirm the resulting `main` commit remains clean and hosted-verified.
3. Only then obtain a separate, explicit owner instruction to change repository
   visibility. Do not deploy the Flask development server as part of that step.
4. If the repository becomes public, add a required-Quality/no-force-push
   ruleset and enable GitHub private vulnerability reporting, then verify the
   reporting and notification paths immediately. Dependabot vulnerability
   alerts and automated security fixes are already enabled.
