---
status: accepted
confirmed_by: "vrknetha"
date: 2026-08-06
stories: [FORGE-APPROVE-1]
supersedes: ""
---

# Plan Approval In Plan Mode

## Context

`forge plan save` writes a plan with `status: approved` and sets
`plan_status = "approved"` in one step. It refuses without a recorded grill
(PH-3), but two things it does NOT enforce:

- The grill's content is self-authored. An agent can record a "pass" grill
  whose questions it answered itself, never putting a genuine open question to
  the human.
- The approval itself is an agent action — running a command — not an explicit
  human confirmation. Nothing structurally stops an agent from planning and
  approving its own plan and proceeding straight to implementation.

`update_run.py` already refuses to set `plan_status = approved` via its flag,
precisely so a locked worker cannot hand-write a plan and flip the field. But
the same trust is placed in `plan save` itself.

Claude Code already provides the deterministic human gate this is missing:
**plan mode**. In plan mode the harness physically blocks product-code actions
until the agent calls `ExitPlanMode` and the *human approves it*. That approval
is unforgeable by the agent — it is a human decision the harness enforces,
exactly like `decision accept` and client sign-off require human chat
confirmation.

## Decision

A plan is approved by a human in plan mode, proven by an approval marker the
agent cannot forge.

- A hook on `ExitPlanMode` writes `.factory/plan-approval.json` when — and only
  when — the human approves the plan: the approved plan's digest, the approver,
  and a timestamp.
- `plan save` sets `plan_status = "awaiting-approval"`, not `approved`. It
  refuses to record an approved plan unless a **fresh** `plan-approval.json`
  marker matches the plan it is saving (digest-bound, the same freshness rule
  the grill already uses). A stale or absent marker means the plan was never
  human-approved, and save refuses.
- The grill runs before the plan-mode presentation, and its genuine open
  questions are put to the human (`AskUserQuestion`), so the human approves a
  plan whose questions they have actually answered — not one the agent both
  asked and answered.
- A documented fallback exists for environments without plan mode (headless,
  cron): an explicit human-confirmed CLI approval, attributed and audited like
  `decision accept`. It is the exception, not the path.

## Consequences

- Self-approval becomes structurally impossible: no product write without an
  approved plan (the always-armed lock, 0013), and no approved plan without a
  human's plan-mode approval marker. The agent cannot mint the marker.
- The grill stops being a self-graded formality: its questions reach the human
  before approval, and the human's ExitPlanMode approval is the answer.
- Cost accepted: every plan now requires a real human approval step. That is the
  point — it is the same deliberate friction as decision acceptance, applied to
  the plan that authorizes implementation.
- This composes with, and does not replace, the grill (PH-3) or the
  contradiction gate (0015): those still run; this adds the human gate they
  assumed but did not enforce.
- The marker is ephemeral working state (0025), gitignored, per-worktree — it
  authorizes one save and is not project history.
