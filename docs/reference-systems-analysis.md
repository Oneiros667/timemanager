# Analysis of the supplied ADHD and Kaizen systems

Research snapshot: 2026-07-24

## How this analysis should be read

The supplied pages are product pages and marketplace listings, not evaluation
studies. Their mechanics can be excellent design hypotheses without proving
that the product improves ADHD symptoms or daily functioning. Testimonials,
ratings, user counts, and creator outcomes are commercial evidence only.

The two products called "Kaizen ADHD System" are treated separately:

- **Ruri Ohama's Kaizen System** is the system marketed at
  [ruriohama.com](https://ruriohama.com/).
- **Kaizen ADHD System by Heytahaaa** is the separate
  [Notion Marketplace template](https://www.notion.com/templates/kaizen-adhd-system)
  supplied by the user.

## Comparative map

| System | Core mechanics visible in the supplied material | Strongest idea to test | Main caution |
|---|---|---|---|
| Ruri Ohama's Kaizen System | Brain dump, daily highlight, two-minute micro-commitment, Must/Should/Could, flexible sprints, estimate vs actual time, weekly reports, Simple/Advanced modes | A shared data model with a genuinely small low-capacity view | Advanced dashboard and tracking may recreate the complexity Simple Mode solves |
| Kaizen ADHD System by Heytahaaa | Daily brain dump, one highlight, micro-habit, energy-based sprints, onboarding/sample data, weekly review | Small daily ritual plus guided onboarding | Listing is very close in vocabulary to Ruri's model; effectiveness is unvalidated |
| ADHD Operating System | Five layers, energy-aware sorting, micro-chunked tasks, guilt-free reset, daily command centre | Reset as normal operation and task matching by current capacity | "Five layers" may become navigation and maintenance overhead |
| ADHD Daily Planner | One-line intention, emoji mood check, top three tasks, priority and energy | Extremely compact daily orientation | Top three can hide fixed commitments and mood can become unused tracking |
| ADHD Focus Flow | One task database, eight smart views, energy-based rather than priority-based routing | One canonical database with contextual views | Energy cannot replace deadlines, consequences, or value |
| ADHD Planner: Built for the Way Your Brain Works | Daily dashboard, focus tracker, habit streaks, brain-dump inbox | A clear capture-to-focus path | Habit streaks can punish interruption and a feature bundle can dilute the day loop |
| Kaizen: Your Life Blueprint | Identity, ikigai, dreams, goals, progress, focus tools, journaling, small improvements | Linking daily action to chosen values | Life architecture creates a large setup burden and can turn reflection into avoidance |

Descriptions of some Notion templates are short marketplace summaries. The
analysis does not assume features that are not shown or described.

## Ruri Ohama's Kaizen System

### What the system claims to solve

The page accurately names several common failure experiences:

- endless lists and loss of the big picture;
- feature overload and complicated setup;
- forgetting to return to the tool;
- repeated high-motivation starts followed by missed days;
- guilt, reduced self-trust, and another total restart.

That framing is product-relevant because it describes failure over time, not
just a missing planner feature. The site positions the problem as a mismatch
between a consistency-dependent system and variable human capacity.

### Daily loop

The marketed Simple Mode has three practices taking about five minutes:

1. **Brain dump** to move mental clutter into the system.
2. **Daily highlight** to choose one task that would make the day successful.
3. **Micro-commitment**: a two-minute action toward a habit.

This is the strongest part of the design. It maps well to external capture,
limited work in progress, values-based selection, and a low activation
threshold. It also provides a success definition that is not "clear the list."

Questions to test:

- Does the brain dump end with enough triage to prevent an accumulating inbox?
- Is the highlight allowed to be a health, relationship, rest, or recovery
  action?
- Does the micro-commitment help launch meaningful behaviour, or become an easy
  box that displaces it?
- What happens when a true must and the chosen highlight compete?

### Must / Should / Could model

The screenshots and copy distinguish:

- **Must Do**: clear deadlines and consequences for not acting;
- **Should Do**: meaningful, fulfilling activities without a fixed deadline;
- **Could Do**: enjoyable, non-urgent, lower-priority activities.

This is notably better than treating "Should" as externally imposed guilt. It
reserves the middle category for important-but-not-urgent life enrichment.

The limitation is that one category combines consequence, value, timing, and
choice. A user may also interpret "must" emotionally rather than factually.
For our system, preserve the plain-language view but base it on separate facts:
deadline, consequence, value, readiness, duration, and capacity. Show the reason
for the recommendation.

### Simple and Advanced modes

Both modes reportedly share and synchronise the same data. Simple Mode keeps the
daily essentials; Advanced Mode adds project management and time tracking. The
user can switch without losing progress.

This is the most important architectural lesson from the site. Low capacity
should change the amount of interface, not fork the user's reality. There
should be one task store with different levels of disclosure.

The screenshots also expose a risk. Even the simplified Notion page contains
multiple coloured panels, database controls, tabs, help sections, filter
buttons, and horizontal scrolling. It is simplified relative to the advanced
page, but not necessarily perceptually simple. A purpose-built product can keep
the same conceptual model while removing database chrome and configuration
controls from the daily path.

### Sprint Sessions

The page describes work blocks that adapt to energy: continue when in flow or
take a break when distracted, without rigid time slots.

Useful:

- avoids treating one interval length as universally correct;
- acknowledges fluctuating focus and capacity;
- reduces guilt around a needed break.

Missing:

- protection from hyperfocus overrunning an appointment;
- an explicit session intention and definition of done;
- transition and leave-by cues;
- a place to capture distractions;
- guidance for choosing a first interval.

Borrow flexibility, then add edges. "Continue" should be a conscious choice,
and the next fixed commitment should remain visible.

### Reality-based time tracking

Comparing estimated and actual task duration is unusually relevant. It can
build a personal evidence base instead of demanding better intuition.

Implementation cautions:

- focus time and elapsed time are not the same;
- exact manual tracking is fragile during interruptions;
- estimates should become ranges based on similar tasks;
- setup, switching, travel, and cleanup need representation;
- missing tracking data must remain unknown rather than count against the user.

### Weekly insights and progress

The system reports daily-highlight and micro-commitment completion, urgent-task
share, estimate-versus-actual time, and project progress. It tries to redirect
attention from busyness to meaningful outcomes.

Useful:

- closes the learning loop;
- makes invisible accomplishments visible;
- can reveal when urgent work crowds out important work;
- supports small, evidence-based adjustments.

Risks visible in the screenshots and copy:

- streaks make a missed day look like lost progress;
- percent complete treats tasks as equal units;
- "0 days" and "still pending" create a deficit-oriented first impression;
- task-based project progress can advance without the outcome advancing;
- the review may become another dashboard to maintain.

Our review should focus on patterns, recovery, estimate calibration, and one
next experiment. Rest days and deliberate dropping must not break progress.

### Values, goals, and "Energy > time"

Connecting daily actions to values and goals can make distant outcomes more
salient. The system also says energy management matters more than time
management.

The useful principle is **energy and time**, not energy instead of time.
Capacity affects feasibility; the clock, medication windows, transport,
meetings, caregiving, sleep, and deadlines remain real. The product should find
a feasible task for the current state while protecting consequence-bearing
commitments.

### Tone and behaviour design

Strong:

- explicitly allows mistakes;
- frames tiny steps as rebuilding self-trust;
- offers a survival mode rather than demanding ideal behaviour;
- uses fulfilment rather than raw completion as the goal.

Concerning:

- urgency-based sales language such as "stop wasting your potential" and
  "tomorrow you'll wake up with the same life";
- unverified satisfaction, ratings, and transformation testimonials;
- "1% every day" can still imply uninterrupted compounding;
- the creator's success does not establish causal effectiveness for users.

The product itself should keep the compassionate mechanics and reject
shame-adjacent acquisition language.

### Verdict

Borrow:

- one capture → one highlight → one tiny commitment daily ritual;
- shared data beneath Simple and Advanced modes;
- meaningful/non-urgent work as a protected category;
- flexible work sessions;
- estimate-versus-actual calibration;
- weekly learning and explicit permission to recover.

Adapt:

- replace category-only priority with explainable factors;
- turn sprints into bounded sessions with transition protection;
- replace streaks and completion percentage with rolling patterns and outcomes;
- reduce visual/database chrome;
- make triage and return after absence explicit.

Do not assume:

- that Kaizen branding itself is effective;
- that a Notion template has clinical benefit;
- that five minutes of planning is enough for every context;
- that energy matching can safely govern all work.

## Other supplied Notion systems

### Kaizen ADHD System by Heytahaaa

The marketplace description promises a daily brain dump, one highlight, a
micro-habit, energy-following sprint tasks, sample data, onboarding, and a
weekly review.

This is a coherent compact loop and guided onboarding is valuable. It is,
however, mechanically and linguistically very similar to Ruri Ohama's offering.
Treat it as a separate product comparison, not independent validation of the
same concepts. Inspecting a purchased/duplicated template would be necessary
before comparing its databases, workflows, or originality in more detail.

### ADHD Operating System by Wisdom for Life

The listing describes five layers, energy-aware task sorting, micro-chunked
to-dos, guilt-free resets, and a daily command centre.

Borrow the reset and micro-chunking concepts. Test whether "five layers" are
progressive disclosure or five places the user must remember. A good daily
command centre should assemble the current state automatically rather than
require users to populate multiple source pages.

### ADHD Daily Planner by Jacob's Creations

The listing presents a minimal morning page: one-line intention, emoji mood
check-in, and a top-three focus list with priority and energy information.

The minimalism is useful. Mood should change a decision—such as suggesting
lower-friction actions—or it is extra logging. Fixed appointments, true
deadlines, and transition time must sit alongside the top three so that a calm
dashboard does not hide reality.

### ADHD Focus Flow by NotoMantra

The listing uses one task database and eight views, routing tasks by current
brain/energy state rather than priority.

One database with multiple computed views is structurally strong. The
"energy instead of priority" framing is too absolute. Combine current
feasibility with consequence and value. Eight views may be useful as optional
lenses, but the system should provide one obvious default and never require the
user to check all eight.

### ADHD Planner by Anmar

The listing combines a daily dashboard, focus tracker, habit streaks, and
brain-dump inbox.

Capture plus a direct focus path is promising. Habit and streak machinery is
less compelling for a day-support MVP: it adds maintenance, creates another
source of failure, and can reward app interaction rather than life outcomes.
If habits are later added, use flexible frequency and return-oriented feedback.

### Kaizen: Your Life Blueprint by Yugen

The listing covers identity, ikigai, dreams, goals, progress, focus, and
journaling, framed as steady daily improvement.

This is a life-design system rather than primarily a day-navigation system.
Values can help decide what deserves protection, but extensive identity and
goal setup is costly before first value. It should be an optional reflective
layer after the core daily loop is trusted, not onboarding.

## Cross-system findings

The repeated ideas are:

- a brain dump or inbox;
- one main daily focus or a top three;
- energy-aware selection;
- decomposition into small actions;
- flexible focus sessions;
- visible progress;
- habit or micro-commitment tracking;
- a daily dashboard;
- periodic review;
- compassionate reset language.

Repetition across marketplace products shows product-market resonance, not
scientific replication. The concepts that also map to ADHD-focused CBT—external
capture, prioritisation, task decomposition, time awareness, distraction
management, and review—deserve the highest confidence. Energy labels,
body-doubling, gamification, streaks, and elaborate life dashboards should be
treated as testable options.

The [supplied Reddit discussions](reddit-app-experience-analysis.md) reinforce
the same core mechanics but warn against assuming one presentation will fit
everyone. Some people valued rich integrated tools; others abandoned them for a
calendar, native reminders, a watch, paper, or a whiteboard. This strengthens
the case for one shared data model, progressive disclosure, non-phone surfaces,
and user-controlled support intensity.

## Synthesis for our system

The defensible combination is:

1. Ruri's low-capacity architecture and daily ritual;
2. the one-database principle from Focus Flow;
3. the minimal daily orientation of ADHD Daily Planner;
4. guilt-free reset from ADHD Operating System;
5. values as a quiet tie-breaker from the Kaizen life systems;
6. organisation, planning, problem solving, time awareness, and distraction
   skills from evidence-based ADHD-focused CBT.

The product should not begin as another "life operating system." It should first
prove that it can help someone answer four questions under real-world pressure:

- What is real today?
- What should I do now?
- How do I start it?
- What happens when the day goes off plan?

## Supplied sources

- [Ruri Ohama: Kaizen System](https://ruriohama.com/)
- [Kaizen ADHD System by Heytahaaa](https://www.notion.com/templates/kaizen-adhd-system)
- [ADHD Operating System](https://www.notion.com/templates/adhd-operating-system-daily-planner-for-neurodivergent-min)
- [ADHD Daily Planner](https://www.notion.com/templates/adhd-daily-planner-567)
- [ADHD Focus Flow](https://www.notion.com/templates/adhd-focus-work)
- [ADHD Planner: Built for the Way Your Brain Works](https://www.notion.com/templates/adhd-planner-built-for-the-way-your-brain-works)
- [Kaizen: Your Life Blueprint](https://www.notion.com/templates/kaizen-life-blueprint)

For clinical and research sources supporting the cross-system assessment, see
[ADHD-friendly time-management domain research](adhd-time-management-domain-research.md#sources).
