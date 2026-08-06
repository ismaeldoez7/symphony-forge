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

A plan is approved by a human, proven by a marker the agent cannot forge.

> **Correction, 2026-08-06 (during FORGE-APPROVE-1).** This decision originally
> made a hook on `ExitPlanMode` write the marker. Verification against Claude
> Code's docs proved that infeasible: **no PreToolUse/PostToolUse hook fires for
> plan-mode transitions** (GitHub #21282). `ExitPlanMode` fires only a
> `PermissionRequest` event, which is a permission-DECISION gate fired *before*
> the human decides — it cannot record that the human approved *this* plan.
> Confirmed with the human, the mechanism is the CLI approval below, which the
> harness already trusts for its most critical gates. Plan mode remains the
> human-review presentation; it is not the enforcement signal.

- `forge plan approve --by <name>` writes `.factory/plan-approval.json`: the
  approved plan's body digest, the approver, and a timestamp. It requires an
  explicit human `--by` and is a human chat confirmation, exactly like
  `decision accept` and client sign-off — the same trust model, not a weaker one.
- `plan save` sets `plan_status = "awaiting-approval"`, not `approved`. It
  refuses to record an approved plan unless a **fresh** `plan-approval.json`
  marker matches the plan it is saving (digest-bound over the plan BODY, the
  same freshness rule the grill uses). A stale, mismatched, or absent marker
  means the plan was never human-approved, and save refuses.
- The grill runs before approval, and its genuine open questions are put to the
  human (`AskUserQuestion`), so the human approves a plan whose questions they
  actually answered — not one the agent both asked and answered. Presenting the
  plan in plan mode (`ExitPlanMode`) is the recommended review step; the
  attributed `plan approve` is the recorded gate.
- The approve command is the single path (there is no hook to be primary over);
  it works identically in interactive and headless/cron runs.

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
  authorizes one save and is not project history. A committed
  `plan-human-approved` event records who approved and when.

## The trust ceiling (accepted)

This gate has the **same trust model as `decision accept` and client sign-off**:
the agent runs the command, and the constitutional rule is that a human
confirmed first. It is disciplinary and audited, **not cryptographically
unforgeable** — a misbehaving agent could run `plan approve --by` without a real
human. That is the ceiling of what is achievable while Claude Code fires no hook
on plan-mode approval (#21282); a truly unforgeable gate needs that hook. This
was reviewed (autoreview flagged it) and accepted by the human as parity with
the harness's existing critical gates, not a regression from them. If plan-mode
hooks land, a follow-up binds the marker to the hook and removes the ceiling.
