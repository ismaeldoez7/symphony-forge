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

Claude Code already has the deterministic human gate this is missing: plan mode.
The harness blocks product actions until the agent calls `ExitPlanMode` and the
human approves — an approval the agent cannot forge, exactly like `decision
accept` and client sign-off. Decision 0029 states the design.

## Behaviour

A plan reaches `approved` only through a human's plan-mode approval, proven by a
marker the agent cannot mint.

- A hook fires on `ExitPlanMode` and, only when the human approves, writes
  `.factory/plan-approval.json`: the approved plan's digest, approver, timestamp.
- `forge plan save` sets `plan_status` to `awaiting-approval`, never directly to
  `approved`. It refuses to record an approved plan unless a fresh
  `plan-approval.json` marker matches the plan being saved (digest-bound, the
  same freshness rule the grill uses). Absent or stale marker → refused.
- The grill's genuine open questions are put to the human before the plan-mode
  presentation, so the human approves a plan whose questions they answered.
- A documented, human-confirmed CLI fallback exists for headless/cron runs where
  plan mode is unavailable — attributed and audited like `decision accept`, the
  exception not the path.
- The marker is ephemeral working state (0025): gitignored, per-worktree, good
  for one save.

## Acceptance criteria

- `plan save` sets `plan_status` to `awaiting-approval` and refuses to set
  `approved` unless a fresh `.factory/plan-approval.json` matches the plan's
  digest; a stale or absent marker is refused with a message naming the missing
  approval.
- A hook writes the approval marker on human ExitPlanMode approval and does not
  write it when the plan is rejected or edited.
- The marker binds the exact plan approved: saving a plan whose digest differs
  from the marker is refused, so an edit after approval cannot ride a stale
  marker.
- Implementation stays blocked (`update_run` refuses the implementing phase)
  until `plan_status` is `approved`, which now requires the human marker.
- A documented CLI fallback records a human-attributed approval for a plan when
  plan mode is unavailable, and it is refused without a `--by` human.
- Every existing plan-save gate (grill freshness, decisions_reviewed coverage,
  contradiction signals, Surface Impact) still runs unchanged.
