# Complex-work prototype walkthrough

Status: usability protocol for synthetic prototype

Updated: 2026-07-28

## Run locally

```bash
TIMEMANAGER_ENABLE_PROTOTYPES=1 uv run timemanager
```

Open <http://127.0.0.1:5000/prototypes/complex-work>. The route uses synthetic
browser-memory state, makes no database writes, and is unavailable unless the
environment flag is enabled.

## Participant mix

Use at least five participants: at least two who prefer minimalist planning
tools, at least two who prefer feature-rich tools, and one additional
participant from either group. Use synthetic scenarios only.

## Walkthrough tasks

Do not explain the interface before each task.

1. Capture “Sort this out,” then add detail without first classifying it.
2. On Today, change the tax task and its next action without leaving the list.
3. Open the task, add three steps rapidly, edit one, and mark one complete.
4. Turn a step into a project task after reading the preview.
5. Find the project, return to its partially organised state, and add three
   project tasks rapidly.
6. Explain preferred order, which task is next, and why “Submit the return” is
   not ready.
7. Add a prerequisite and an external wait; explain how a follow-up differs
   from the wait.
8. Complete the displayed prerequisite and describe what changed in Today.
9. For the blocked Today task, choose between Keep here, Replace, and Remove
   blocker. Confirm that newly ready work did not enter Today.
10. Repeat the task-workspace flow at a narrow mobile viewport and in Low
   Capacity presentation.

## Gate

Proceed to implementation only when:

- participants add task detail and project tasks without coaching;
- at least four of five distinguish preferred order from a blocker and identify
  the next-ready task;
- nobody expects newly unblocked work to enter Today automatically; and
- no blocking keyboard, focus, contrast, or screen-reader issue remains.

Record observed behavior rather than inferred motivation. Do not treat this
small formative study as clinical or efficacy evidence.
