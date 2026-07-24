# Research and product-documentation guidance

This file supplements the repository-root `AGENTS.md` for all work under
`docs/`.

## Evidence model

Preserve the labels defined in `docs/README.md`:

- **Supported** for conclusions directly aligned with clinical guidance,
  controlled trials, systematic reviews, or tested treatment protocols.
- **Plausible** for reasoned product hypotheses whose exact ADHD use has not
  been validated.
- **Experiential** for lived experience or practitioner/user advice without
  strong controlled evidence.
- **Commercial claim** for creator, vendor, marketplace, testimonial, rating,
  or adoption claims.

Do not silently promote evidence from one category into another. Reddit
discussion is discovery evidence, not prevalence or efficacy evidence.
Marketplace copy can describe a mechanic but cannot validate its outcome.

## Research workflow

- Read the whole relevant section and its reference list before editing a
  conclusion.
- Prefer primary research, systematic reviews, clinical guidelines, and
  first-party technical documentation. Use secondary sources to orient, not to
  replace an available primary source.
- Browse and verify claims that are current, safety-sensitive, medical,
  regulatory, privacy-related, API-specific, or otherwise likely to have
  changed. Record the access or research date when it materially bounds the
  conclusion.
- Follow the citation style already used by the document. Every reference ID
  must resolve to a real entry, and every URL/title must correspond to the
  source actually consulted. Never fabricate a citation, quotation, result, or
  supplied-source detail.
- Paraphrase sources except where a short quotation is necessary. Keep
  quotations accurate, minimal, and clearly attributed.
- Describe disagreements, uncertainty, population limits, short follow-up, and
  low-certainty evidence when they affect the product implication.
- Keep observations, inferences, product decisions, and implementation status
  distinguishable. Use terms such as `proposed`, `to test`, or `implemented`
  deliberately.

## Product language

- Evaluate a time-management product on functional outcomes such as capture,
  initiation, realistic planning, transition support, recovery, and user
  wellbeing. Do not imply that app use reduces core ADHD symptoms without
  suitable evidence.
- Avoid universal statements about people with ADHD. Prefer scoped language
  that reflects heterogeneous needs and variable capacity.
- Preserve the distinction between support that helps someone function and
  clinical treatment.
- For AI or voice features, document consent, data flow, retention, deletion,
  failure modes, non-AI fallback, and the boundary between suggestions and
  user-approved mutations.

## Document maintenance

- Keep `Research snapshot:` dates truthful. Update a date when the evidence or
  analysis was substantively re-evaluated, not for spelling or formatting
  changes.
- Keep `Status:` and `Updated:` metadata accurate in design notes.
- Add new documents to `docs/README.md` with a one- or two-sentence description.
- Preserve useful source provenance even when shortening prose.
- Check headings, tables, Markdown fences, local links, reference identifiers,
  and `git diff --check` before handoff.

In review, treat fabricated or mismatched sources, overstated evidence,
medical-treatment claims, missing material privacy disclosures, and confusion
between proposed and implemented behaviour as blocking findings.
