# Guardian-supported calm-break prototype

Status: synthetic prototype implemented; real child feature blocked by child-workspace release gates

Updated: 2026-07-28

## Purpose

This prototype explores how a guardian and a young person could coordinate a
short, supportive pause after conflict, overload, or escalating emotion. The
interface calls this a **calm break**, not a punishment or measure of
compliance. Its exact benefit is a **plausible** product hypothesis and has not
been validated.

A guardian can suggest options such as mindfulness, breathing, grounding,
music, water, a snack, a quiet activity, or a custom family guideline. The
young-person view shows the reason, the available choices, the agreed check-in,
and three responses: ready, need help, or talk about the plan.

## Safety contract

- The plan is shown before the break begins.
- Guidelines are choices and supports, not a checklist that must be completed.
- Music may be explicitly allowed; the design does not silently treat ordinary
  comforts as privileges to be earned.
- There is no forced countdown, locked screen, compliance score, streak,
  escalating penalty, or automatic report to a guardian.
- The young person always has visible ways to ask for help or challenge the
  plan.
- The interface must not be used for seclusion, restraint, isolation from
  necessary supervision, or emergencies.
- The tool does not provide therapy, diagnosis, crisis management, or parenting
  instructions.

## Implemented boundary

With `TIMEMANAGER_ENABLE_PROTOTYPES=1`, the same-device synthetic interaction is
available at `/prototypes/calm-break`. Browser input exists only in the current
page and is discarded on refresh. The route is disabled by default and returns
`Cache-Control: no-store`.

It creates no child account, guardian relationship, invitation, audit record,
notification, saved plan, or cross-account permission. Real family data must
not be entered during formative testing.

## Required before real use

A persistent version belongs only in a guardian-created child workspace. It
requires the authorization, guardian-verification, child-visible history,
revocation, deletion, export, coercion/unsafe-family review, jurisdiction
routing, and child-data release gates defined in
[Assisted planning and guardian support](assisted-planning-and-guardian-support.md).
Research with young people also requires an approved protocol, guardian consent
where applicable, young-person assent, and synthetic scenarios.

Before implementation, formative testing should establish whether the language
feels supportive rather than punitive, whether young people understand that
options are choices, and whether “talk about the plan” works as a meaningful
way to object.
