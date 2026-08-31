# Japanese work and cultural practices: product inspiration

Status: product research and inspiration; no new behavior implemented or
participant-validated

Research snapshot: 2026-08-31

## Purpose and evidence boundary

This note evaluates a small set of Japanese industrial practices and cultural
ideas as possible inspiration for Timemanager. The goal is not to assemble
Japanese-themed productivity features. It is to identify simple mechanisms that
could reduce planning, starting, switching, and recovery friction without
creating another system to maintain.

The sources establish the original industrial practice, management framework,
laboratory result, or cultural concept. They do not establish that the proposed
Timemanager translation helps adults with ADHD. Under this repository's evidence
model, the exact product translations remain **Plausible** unless explicitly
identified as **Experiential**. None is evidence of treatment or clinical
effectiveness.

"Japanese work" is not one uniform method. This review distinguishes:

- Toyota Production System mechanisms such as kanban, pull, Just-in-Time, and
  jidoka;
- wider workplace practices such as 5S and pointing and calling;
- Mike Rother's later Improvement Kata framework, derived from his study of
  Toyota rather than documented as Toyota's own named routine; and
- *ma* as a broad cultural concept of interval or in-between space, not an
  industrial productivity method.

## Evidence ledger and recommendation

| Candidate | Source establishes | Proposed Timemanager use | Evidence status | Recommendation |
| --- | --- | --- | --- | --- |
| Kanban, pull, and work-in-progress limits | Toyota uses kanban cards to support a pull system in which the next process requests what it needs [1] | Keep Later as the backlog, Today as a bounded buffer, and one task as the current work | Plausible translation; Today already implements part of it | Retain the mechanism; do not add a large board |
| *Genchi genbutsu* | Toyota describes going to the source to find facts before deciding [3] | A ten-second **What is true now?** orientation using current time, commitments, capacity, and blockers | Plausible translation | Use as an internal design principle |
| Pointing and calling | Japanese railway and industrial research found fewer errors in controlled choice and checking tasks [4][5] | Optional embodied confirmation for two or three consequential transition checks | Plausible translation from non-ADHD safety research | Prototype narrowly; never require voice recording |
| 5S | JICA describes Sort, Set, Shine, Standardize, and Sustain as workplace-organization practices [6] | Remove one obstruction, return needed items, and stage the first item for the next context | Plausible translation | Test one micro-reset, not a five-part audit |
| Kaizen and Improvement Kata | Toyota documents continuous improvement; Rother formalizes a current-condition, target-condition, experiment pattern [2][7] | Select one small, reversible weekly experiment based on observed friction | Plausible translation | Keep one experiment at a time |
| Jidoka and poka-yoke | Toyota describes stopping when an abnormality appears; Shingo's mistake-proofing work designs around predictable human error [2][8][9] | Let the user stop an invalid plan, preserve work, and make the safe next choice obvious | Plausible translation; some safety behavior already exists | Treat as a system-wide safety principle |
| *Ma* | Research describes *ma* as an interval or in-between space in Japanese arts and daily-life practices [10] | Preserve a short buffer that closes one context before presenting the next | Experiential/cultural inspiration | Use as a design metaphor, not an efficacy claim |

## 1. Kanban: pull only when capacity exists

Toyota's Just-in-Time explanation describes a pull system: the following
process takes what it needs from the preceding process, and kanban cards help
coordinate replenishment [1]. The transferable idea is not the familiar
software board. It is that work enters the active system only when capacity is
available.

The smallest Timemanager interpretation is:

- Later remains the backlog;
- Today remains a deliberately bounded buffer;
- no more than one task is treated as current work;
- finishing or deliberately parking that task creates capacity to pull another;
  and
- overflow remains visible but is never promoted automatically.

The accepted small-Today decision already implements one highlight, no more
than three optional active actions, recoverable overflow, and no silent
promotion. Kanban therefore reinforces the current direction; it does not
justify replacing Today with a draggable multi-column board.

Potential later experiment: when bounded focus sessions are implemented, test a
single explicit **Working now** container with **Finish**, **Park safely**, and
**Pull another** actions.

## 2. *Genchi genbutsu*: plan from present facts

Toyota describes *genchi genbutsu* as going to the source to find the facts
needed for correct decisions [3]. Personal planning cannot literally copy a
factory practice, but it can adopt a fact-first orientation:

> **What is true right now?**

A compact orientation could show only facts Timemanager can support accurately:

- current time;
- the next fixed commitment and transition boundary, once implemented;
- the user's selected capacity mode, without inferring health or mood;
- the selected task's saved next action and visible blocker; and
- whether the earlier plan still fits the remaining time.

This should not become another form to complete. Its purpose is to reduce the
gap between an idealized plan and the current situation. It fits the proposed
Orient and consequence-aware Reset experiences.

## 3. Pointing and calling: an embodied critical check

Pointing and calling combines looking at an object, pointing to it, and saying
its identity or state. In Haga, Akatsuka, and Shiroto's controlled experiments,
the combined procedure produced the lowest error rate of the tested conditions;
in a second experiment, none of twelve participants using it made the critical
red-signal response error, compared with five of twelve without it [4]. A later
Railway Technical Research Institute report summarizes one mean error-rate
comparison as 0.38% with pointing and calling versus 2.38% without it [5].

These are laboratory and occupational-safety results, not evidence about ADHD
planning or ordinary household routines. The likely value is limited to a
small number of checks where prospective-memory failure has a meaningful
consequence.

Possible examples:

- **Leaving:** keys present; required bag present; departure step confirmed.
- **Closing work:** exact next-start file or object staged; unsaved work handled.
- **Changing location:** the one essential item for the next context present.

Timemanager could display the check while the user points or speaks. It should
not listen, record audio, demand performance, or claim that tapping a checkbox
is equivalent to the researched embodied procedure. Repetition for ordinary
tasks would add friction and should be avoided.

## 4. 5S: a bounded environmental reset

JICA describes 5S as Sort, Set, Shine, Standardize, and Sustain, originating
from the Japanese terms *seiri*, *seiton*, *seiso*, *seiketsu*, and *shitsuke*
[6]. Its full workplace form involves ongoing organization and standards. A
personal productivity product should not reproduce that governance overhead.

The high-value reduction is:

> **Remove one obstruction → return needed things → stage the first thing for
> the next context.**

At the end of work this might mean clearing one surface, closing the current
materials, and opening or placing the exact first item for tomorrow. At lunch it
might mean leaving the current task in a recoverable state and physically
leaving the work surface.

This should be one optional transition ritual, not a cleaning score, recurring
audit, streak, household standard, or expanding checklist.

## 5. Kaizen and Improvement Kata: one experiment

Toyota describes daily incremental kaizen as part of the continuing Toyota
Production System [2]. Mike Rother's Improvement Kata, developed from his study
of Toyota, uses a repeatable pattern: understand the current condition, define a
nearer target condition, and move toward it through experiments that expose new
obstacles [7]. The distinction matters: **Improvement Kata** is Rother's named
framework, not a claim that Toyota uses that exact label or card internally.

Timemanager's proposed weekly learning loop already contains the smallest useful
translation:

1. What friction repeated?
2. What is one small change worth trying?
3. What happened when I tried it?
4. Keep, change, or stop the experiment.

Only one experiment should be active by default. It must be reversible and must
not imply that every difficult day reveals something the user must optimize.
Examples include staging a starting file before stopping work or using a
smaller first focus interval for one week.

## 6. Jidoka and poka-yoke: stop safely and design around slips

Toyota describes jidoka as detecting an abnormality and stopping rather than
allowing the problem to continue through the process [2]. Shigeo Shingo's
poka-yoke work addresses mistake-proofing at the source [9]. The Shingo
Institute emphasizes the non-blaming premise that mistakes are human and that a
useful countermeasure must not burden or disrespect the person using it [8].

Possible Timemanager implications are:

- a prominent **The day changed** or **This plan no longer fits** action;
- blocked work offers **Clarify**, **Park safely**, or **Ask**, rather than
  repeatedly demanding **Start**;
- interrupted edits remain recoverable;
- destructive actions have confirmation and recovery paths;
- invalid capacity or ownership states fail closed; and
- transitions can stage the next required object or action so success depends
  less on remembering later.

These principles already align with recoverable Today overflow, preserved
drafts, dropped-task recovery, explicit ownership, and the proposed Reset flow.
They should guide implementation rather than appear as Japanese-branded user
features.

## 7. *Ma*: preserve the interval

Tseng's qualitative research describes *ma* as a Japanese concept of gap,
interval, or in-between space across arts and daily-life practices [10]. That
work concerns contemporary dance and togetherness; it does not test personal
productivity or transitions for adults with ADHD.

The defensible use is therefore metaphorical:

> A transition needs space; it is not merely the instant when one task replaces
> another.

A product experiment could insert a short neutral boundary between contexts:
close the previous task, hold a brief unfilled interval, and then show the next
commitment or chosen action. The app should not fill that interval with more
content, advice, or notifications.

## Ranked shortlist

| Rank | Smallest high-value idea | Product role | Smallest exit gate before adoption |
| --- | --- | --- | --- |
| 1 | Pull work only when capacity exists | Preserve bounded Today; later test one **Working now** item | Users can finish or park current work and deliberately pull another without losing overflow |
| 2 | Orient from current facts | **What is true now?** summary in Orient/Reset | Synthetic scenario proves facts stay distinct from suggestions and no mood/health state is inferred |
| 3 | Stop safely when the plan is invalid | User-invoked Reset and recoverable state | Day-change scenarios preserve data and require confirmation for every mutation |
| 4 | Reset and stage the environment | One optional transition cue | Participants can complete or skip it without routine debt or checklist growth |
| 5 | Confirm only consequential transitions | Optional point-and-call prompt | Test demonstrates the prompt is understandable, rare, accessible, and usable without recording audio |
| 6 | Run one reversible experiment | Weekly learning | One experiment can be started, reviewed, changed, or stopped without a score or streak |
| 7 | Protect an interval between contexts | Transition presentation principle | Participants experience a clearer boundary without perceiving delay or added work |

## What not to import

- Do not build a large Kanban board merely because kanban is Japanese. Visual
  columns and drag-and-drop can increase scanning and maintenance without adding
  pull or capacity control.
- Do not turn 5S into an audit of the user's home, discipline, or cleanliness.
- Do not translate kaizen into permanent self-optimization or treat every bad
  day as a process defect.
- Do not make pointing and calling ceremonial, public, or mandatory.
- Do not use *ma*, Zen, *ikigai*, or other broad cultural terms as unsupported
  efficacy claims or decorative branding.
- No separately sourced *hansei* feature is recommended from this review. A
  deficit-first reflection would conflict with the experiential requirement to
  preserve achievements and effort alongside unfinished work.

## Relationship to current roadmap

This research does not change the canonical execution order or implementation
status.

- The implemented small Today plan already provides a Kanban-like work-in-
  progress boundary without claiming to be a complete Kanban system.
- *Genchi genbutsu*, jidoka, and poka-yoke may inform milestone 1.3 Review and
  consequence-aware Reset/recovery.
- Pointing and calling, simplified 5S, and *ma* may inform milestone 1.4
  transition-boundary prototypes.
- A one-item pull state may be tested with milestone 1.6 bounded focus sessions.
- The one-experiment Kaizen/Kata interpretation belongs in the existing weekly
  learning proposal and must not bypass the Phase 1 validation interlock.

Before implementation, each visible feature still needs a synthetic prototype,
manual accessibility review, and participant evidence. Any persisted ritual,
check, experiment, or transition history also needs account ownership,
correction, deletion, retention, export/import, and migration decisions.

## References

1. Toyota Motor Corporation. [Toyota Virtual Plant Tour: Toyota Production
   System](https://global.toyota/en/company/plant-tours/production-system/).
   Official explanation of Just-in-Time, the pull system, and kanban cards.
   Accessed 2026-08-31.
2. Toyota Motor Corporation. [Toyota Production
   System](https://global.toyota/en/company/vision-and-philosophy/production-system/).
   Official explanation of Just-in-Time, jidoka, abnormality stops, and daily
   incremental kaizen. Accessed 2026-08-31.
3. Toyota Motor Corporation. [Toyota Global
   Vision](https://global.toyota/pages/global_toyota/ir/presentation/20110309_presentation_en.pdf).
   2011. See the Toyota Way description of kaizen and *genchi genbutsu*.
4. Haga, Shigeru, Hajime Akatsuka, and Hiroaki Shiroto. [Laboratory experiments
   for verifying the effectiveness of "finger-pointing and call" as a practical
   tool of human error
   prevention](https://doi.org/10.32222/jaiop.9.2_107). *Japanese Association of
   Industrial/Organizational Psychology Journal* 9, no. 2 (1996): 107–114.
5. Shigemori, Masayoshi, Ayanori Sato, and Takayuki Masuda. [Experience-based PC
   Learning System for Human Error Prevention by Point-and-Call
   Checks](https://doi.org/10.2219/rtriqr.53.231). *Quarterly Report of RTRI* 53,
   no. 4 (2012): 231–234.
6. Japan International Cooperation Agency. [JICA President Akihiko Tanaka Visits
   South
   Africa](https://www.jica.go.jp/english/about/president/archives_tanaka/130226_01.html).
   2013. Notes define the five Japanese and English 5S terms. Accessed
   2026-08-31.
7. Rother, Mike. [Toyota Kata introduction and Improvement Kata
   overview](https://www.lean.org/wp-content/uploads/2022/04/toyota_kata.pdf).
   Lean Enterprise Institute presentation based on *Toyota Kata: Managing
   People for Improvement, Adaptiveness and Superior Results* (McGraw-Hill,
   2010).
8. Hamilton, Bruce. [Mistake-Proofing
   Mistakes](https://shingo.org/mistake-proofing-mistakes/). Shingo Institute,
   2020. Discusses non-blaming, usable mistake-proofing and common failure
   modes. Accessed 2026-08-31.
9. Shingo, Shigeo. *Zero Quality Control: Source Inspection and the Poka-yoke
   System*. Portland, Oregon: Productivity Press, 1986.
10. Tseng, Chiahuei. [MA and Togetherness (Ittaikan) in the Narratives of
    Dancers and Spectators: Sharing an Uncertain
    Space](https://doi.org/10.1111/jpr.12330). *Japanese Psychological Research*
    63, no. 4 (2021): 421–433.

