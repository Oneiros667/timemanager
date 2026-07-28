# UX and accessibility requirements

Status: proposed interaction requirements; synthetic prototypes only

Updated: 2026-07-28

## Design objective

The interface should reduce the language, memory, sequencing, sensory, and
decision burden required to understand the day or ask for support. It must not
assume that age, diagnosis, speech, reading ability, or apparent independence
predict a child's actual access needs.

WCAG 2.2 AA is a minimum technical baseline, not the full child-accessibility
standard. Child comprehension, low-language access, assistive technology,
sensory load, and safe adult support require additional validation.

## Global interaction requirements

- **KID-UX-01:** Each screen MUST have one obvious purpose and one primary
  action.
- **KID-UX-02:** The primary path MUST avoid requiring more than one decision
  per step where a sequence is safer and clearer.
- **KID-UX-03:** Optional detail MUST use progressive disclosure and MUST NOT
  block capture, help, or a safe exit.
- **KID-UX-04:** Controls MUST use visible text. Icons, color, emoji, animation,
  sound, and haptics are supplementary.
- **KID-UX-05:** A child MUST be able to stop, go back, ask for help, or say
  `none of these` without causing a negative state.
- **KID-UX-06:** Consequences MUST be concrete. Supportive copy MUST NOT obscure
  what changed, who receives information, or how to recover.
- **KID-UX-07:** No interface may use shame, disappointment, moral judgment,
  manipulative urgency, streak loss, or dependency-oriented praise.
- **KID-UX-08:** Drafts and safe entered values MUST survive recoverable errors.
  Secret fields MUST not be repopulated.
- **KID-UX-09:** Focus MUST move predictably after validation, disclosure,
  dialog close, save, message state change, and error.
- **KID-UX-10:** The child-facing interface MUST show which role is currently
  speaking or changing data.

## Age-appropriate presentation

### Ages 8–10 starting presentation

- familiar, concrete words and short sentences;
- one main question per screen;
- maximum three immediate choices plus `something else` where possible;
- clear pictures/symbols only when validated with text equivalents;
- visible adult name/role and reason;
- examples before abstract privacy terms;
- immediate confirmation and obvious undo/cancel; and
- no dense tables, dashboards, policy text, or hidden gesture dependency.

### Ages 11–12 starting presentation

- short explanations of purpose and consequences;
- visible choice between common options;
- simple disclosure and change history;
- optional additional detail without leaving the current task; and
- explicit difference between `sent`, `seen`, and `answered`.

### Ages 13–15 starting presentation

- more direct planning control;
- concise but complete privacy/disclosure previews;
- role and field-level access review;
- visible objection, correction, and concern routes; and
- no assumption that teenage presentation means adult legal authority.

### Ages 16–17 starting presentation

- near-adult information density as an option;
- transition-to-adult explanation and data choices;
- direct participation in renewal and sharing decisions where applicable; and
- continued simplified, low-language, and supported modes when preferred.

Age bands select defaults only. A 17-year-old may use the simplest interface;
an 8-year-old may use more detail when tested and appropriate.

## Proposed information hierarchy

### Child Today

1. Current part of day and next fixed commitment.
2. `Tell someone what I need`.
3. Quick capture.
4. Agreed anchor with one next action and Start.
5. Up to three optional actions.
6. Hidden/overflow summary.
7. Small history/recovery route.

### Low Capacity

1. Low Capacity status and `Show full day`.
2. Next fixed commitment.
3. `Tell someone what I need`.
4. Quick capture.
5. One safe action and next step.
6. Hidden-work count stating nothing changed.

### Task

1. Return and save state.
2. Task title and who added it.
3. Why it matters now.
4. One next action.
5. `Done`, `not now`, `need help`, `talk about this`.
6. Optional steps, project, blockers, and history.

### Calm break

1. Reason for the proposed pause.
2. Support options the child may choose.
3. Music/comfort availability stated explicitly.
4. Check-in agreement.
5. `Ready`, `need help`, `talk about the plan`.
6. Clear statement that it is not a score or punishment.

### Child communication

1. Trusted adult currently available.
2. Low-language message choices.
3. Exact preview.
4. Confirm or cancel.
5. Honest delivery state.
6. Fallback when unavailable or failed.

### Who can see my information

1. Adult name, organization, and role.
2. Why they have access.
3. Exact information categories.
4. Whether they may add information.
5. Expiry.
6. Recent access/change summary.
7. Ask, correct, object, or report concern.

## Low-language communication

The initial child signals are:

- `I'm overwhelmed`;
- `I need a quiet space`;
- `I can't talk right now`;
- `Please get my trusted adult`; and
- `Something else—please check in with me`.

Requirements:

- do not require free text, diagnosis, speech, or eye contact;
- let the child preview and cancel;
- show recipient before sending;
- show `waiting to send`, `sent to Timemanager`, `delivered`, `seen`,
  `could not send`, and `no adult available` as distinct states;
- provide validated symbols/pictures with text, not symbol-only assumptions;
- support keyboard, touch, switch, screen reader, and alternative input;
- avoid automatically escalating repeated use into discipline or diagnosis;
- never hide the signal because Today is full or the child is in Low Capacity;
  and
- offer a nearby-human fallback without implying the app contacted someone.

The vocabulary must be co-designed and tested with speaking and nonspeaking
children, autistic children, children with social anxiety, children with
intellectual/learning disabilities, and children who do not identify with a
diagnosis.

## Adult-facing UX

Adult interfaces must slow down disclosure and authority changes without making
ordinary planning burdensome.

- Show resolved identity and role, not a typed email alone.
- Present field-level disclosure with unchecked optional fields.
- Separate teacher, carer, and school-health purposes.
- Display child-facing explanation beside the adult confirmation.
- Show expiry and revocation effects before activation.
- Use a second confirmation for medication, additional guardian, export, and
  scope expansion.
- Prevent bulk selection of all sensitive fields.
- Keep observations factual and attribute every adult contribution.
- Explain that no-log and missing feedback are unknown.
- Do not show compliance dashboards or response-time rankings.

## Accessibility baseline

### Perceivable

- Meet WCAG 2.2 AA text and non-text contrast.
- Support 200% text zoom and 320 CSS px reflow without two-dimensional scrolling
  except for genuine data tables.
- Do not truncate names, roles, recipients, medication identity, delivery
  status, or safety instructions.
- Provide captions/transcripts for any reviewed media.
- Never require sound, color, animation, or haptic feedback alone.
- Respect reduced motion, forced colors, high contrast, text spacing, and user
  font preferences.

### Operable

- All functions work with keyboard and switch-compatible sequential focus.
- Visible and DOM focus order match.
- Focus is not obscured by sticky controls or dialogs.
- Interactive targets meet at least WCAG 2.2 AA target sizing and SHOULD reach
  44×44 CSS px for primary child touch controls.
- No drag-only, hover-only, gesture-only, time-limited, or rapid-tap-only
  interactions.
- Timers can pause/stop and do not trap the user.
- No flashing content or unnecessary motion.

### Understandable

- Labels remain consistent across roles and screens.
- Errors identify the field, explain the problem, and preserve safe input.
- Delivery, save, and sync states use explicit text.
- Privacy explanations use examples and layered detail.
- `Not now`, `cancel`, `close`, `drop`, `delete`, `revoke`, and `stop sharing`
  remain semantically distinct.
- The interface never describes missing data as failure.

### Robust

- Use native elements and valid accessible names.
- Status announcements occur only for meaningful transitions, not every timer
  tick or retry.
- Dialog focus enters, remains contained, and returns logically.
- Dynamic content exposes programmatic state and relationship.
- Core routes are tested with representative screen reader/browser pairs and
  without JavaScript where the fallback is supported.

## Cognitive and sensory accessibility

- Keep simultaneous primary choices small.
- Avoid decorative motion, noisy backgrounds, dense badges, and competing
  urgency.
- Allow animation, sound, haptic, timer display, and visual density controls.
- Preserve whitespace and predictable placement.
- Keep personal content out of lock-screen previews.
- Do not require remembering information from a previous screen; repeat the
  relevant recipient, reason, or next action.
- Offer a printable or device-independent daily summary in a later,
  privacy-reviewed phase.
- Let the child return after abandonment without onboarding or backlog
  punishment.

## Copy rules

Prefer:

- `What do you need?`
- `Not now`
- `Talk about this`
- `Nothing changed`
- `This message has not been sent`
- `Ms Dlamini has seen your message`
- `No activity was logged`
- `You can choose what helps`

Avoid:

- `You failed`
- `Be good`
- `Non-compliant`
- `Your teacher is watching`
- `Medication missed` when only a log is absent
- `Sent` when only queued
- `Calm down`
- `You must finish these to leave`
- `Your parent owns this account`

## Research with children

Children are not usability instruments. Research must:

- use an approved child-participant protocol;
- obtain guardian permission and child assent as applicable;
- explain stop/withdrawal in child-accessible language;
- avoid collecting real diagnoses, medication, school incidents, family
  conflict, or private task content unless separately authorized;
- start with fictional scenarios and same-device role simulation;
- include a trained facilitator and safeguarding plan;
- minimize and de-identify notes;
- not reward disclosure or completion;
- separate guardian observation from the child's own feedback;
- avoid having a guardian answer on behalf of the child by default; and
- stop when distress, coercion, fatigue, or loss of assent appears.

Participant groups must cover the full age range in narrower bands and include
varied reading, communication, sensory, motor, vision, hearing, cognitive, and
assistive-technology needs.

## Manual verification matrix

Before a changed child flow is accepted, record:

- keyboard-only forward and reverse navigation;
- NVDA with Firefox and Chrome;
- VoiceOver with Safari on supported Apple platforms;
- TalkBack with supported Android browser/app;
- 200% zoom, 320 CSS px reflow, text spacing, and long translated content;
- forced colors/high contrast and reduced motion;
- switch or equivalent alternative-input navigation for child signals;
- one-handed touch on representative real devices;
- slow/offline/failing message delivery;
- screen lock and notification privacy;
- child comprehension in each applicable age band; and
- adult comprehension of recipient, fields, purpose, expiry, and revocation.

Automated tests supplement but do not replace this matrix.

## References

- [W3C Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria/)
- [UK ICO Children's Code design guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/designing-products-that-protect-privacy/childrens-code-design-guidance/)
