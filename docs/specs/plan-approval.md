---
slug: plan-approval
title: A plan is approved by a human, not by the agent that wrote it
status: confirmed
saved: 2026-08-06T07:50:29+00:00
---

# A plan is approved by a human, not by the agent that wrote it

## Why

`forge plan save` records a plan AND marks it approved in one agent-run step. It
requires a grill (PH-3), but the grill is self-authored — an agent can record a
"pass" whose questions it answered itself — and the approval is a command the
agent runs, not a human decision. Nothing structurally stops an agent from
planning, grilling, and approving its own plan, then implementing. The always-
armed lock (0013) blocks product writes without an *approved* plan, but it
trusts whatever set `approved`.

The harness needs a human approval it cannot forge. Plan mode is where the human
reviews the plan (`ExitPlanMode`), but Claude Code fires no hook on that
transition (#21282), so plan mode cannot be the enforcement signal. The
enforcement is an explicit human-attributed approval command — the same trust
model `decision accept` and client sign-off already use. Decision 0029 states
the design and records this correction.

## Behaviour

A plan reaches `approved` only through an explicit human approval, proven by a
marker the agent cannot mint.

- `forge plan approve --by <name>` writes `.factory/plan-approval.json`: the
  approved plan's BODY digest, the approver, a timestamp. It is refused without a
  human `--by` — a human chat confirmation, exactly like `decision accept`.
- `forge plan save` sets `plan_status` to `awaiting-approval`, never directly to
  `approved`. It refuses to record an approved plan unless a fresh
  `plan-approval.json` marker matches the plan being saved (digest-bound over the
  BODY, the same freshness rule the grill uses). Absent, mismatched, or stale
  marker → refused.
- The grill's genuine open questions are put to the human (`AskUserQuestion`)
  before approval, so the human approves a plan whose questions they answered.
  Presenting the plan in plan mode is the recommended review step; the attributed
  `plan approve` is the recorded gate.
- The marker is ephemeral working state (0025): gitignored, per-worktree, good
  for one save.

## Acceptance criteria

- `plan save` sets `plan_status` to `awaiting-approval` and refuses to set
  `approved` unless a fresh `.factory/plan-approval.json` matches the plan's body
  digest; a stale, mismatched, or absent marker is refused with a message naming
  the missing approval.
- `forge plan approve --by <name>` writes the approval marker for the current
  plan's body digest and is refused without a human `--by`.
- The marker binds the exact plan approved: saving a plan whose body digest
  differs from the marker (an edit after approval) is refused.
- Implementation stays blocked (`update_run` refuses the implementing phase)
  until `plan_status` is `approved`, which now requires the human marker.
- Every existing plan-save gate (grill freshness, decisions_reviewed coverage,
  contradiction signals, Surface Impact) still runs unchanged.
