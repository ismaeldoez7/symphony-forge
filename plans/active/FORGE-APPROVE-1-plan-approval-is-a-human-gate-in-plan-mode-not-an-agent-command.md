---
issue: FORGE-APPROVE-1
title: Plan approval is a human gate in plan mode, not an agent command
status: approved
saved: 2026-08-06T07:56:34+00:00
story: FORGE-APPROVE-1
decisions_reviewed:
  - 0001-determinism-contract
  - 0002-concurrency-one-task-per-branch
  - 0003-model-tiers-terra-explore-sol-implement
  - 0005-recurring-findings-escalation
  - 0006-lessons-ledger
  - 0007-stage-commit-loop
  - 0008-loop-health-audit
  - 0009-frozen-gate-integrity
  - 0010-client-signoff
  - 0011-orchestrator-runs-autoreview
  - 0012-project-level-memory
  - 0013-always-armed-planning-lock
  - 0014-specs-before-signoff
  - 0015-plan-contradiction-gate
  - 0016-machinery-dir-rename
  - 0017-repo-as-system-of-record
  - 0018-delegation-gates
  - 0021-derived-ordering
  - 0022-conflict-free-ledgers
  - 0023-stage-delta-by-ref
  - 0025-evidence-lifetime-contract
  - 0026-bundled-example-validated-by-production-validators
  - 0027-responsive-proof-without-a-browser
  - 0029-plan-approval-in-plan-mode
---


# FORGE-APPROVE-1 — Plan approval is a human gate in plan mode

## Problem

`forge plan save` records a plan and sets `plan_status = "approved"` in one
agent-run step. It requires a grill (PH-3), but the grill is self-authored and
the approval is a command the agent runs — so an agent can plan, grill, and
approve its own work, then implement. The always-armed lock (0013) blocks
product writes without an *approved* plan but trusts whatever set the field.
Decision 0029 states the fix: approval is a human's plan-mode decision, proven
by a marker the agent cannot forge.

Grounding (read against the code): `plan save` (`plans.py:180,186`) writes
`status: approved` and sets `plan_status`. `update_run.py:68` already refuses to
set `approved` via its flag, and already knows an `awaiting-approval` status
(`update_run.py:24`). Hooks are wired in `.claude/settings.json` (PreToolUse for
Bash and Edit/Write; a Stop hook). A PostToolUse hook on `ExitPlanMode` receives
the plan content (`tool_input.plan`) and the approval result — it fires after
the human decides, so it can write the marker on approval and skip it on reject.

## Scope / Non-goals

In scope: the ExitPlanMode approval hook, the `plan save` gate change, the
digest binding, the CLI fallback, and tests.

Out of scope, deliberately:

- **The other plan-save gates are untouched.** Grill freshness,
  decisions_reviewed coverage, contradiction signals, Surface Impact all still
  run — this adds the human gate, it does not replace them.
- **No retro-approval of existing plans.** PH-4/PH-5 shipped under the old flow;
  this governs plans from here.
- **Decision-number / roadmap-file merge collisions** (surfaced setting this up)
  are the known merge-fragility class, a separate decision — not folded in.
- **Codex/headless plan-mode parity** is handled by the CLI fallback, not by
  making Codex emulate plan mode.

## Acceptance Criteria

Verbatim from the story, each with its proof:

1. `plan save` sets `plan_status` to `awaiting-approval` and refuses `approved`
   without a fresh `.factory/plan-approval.json` whose digest matches the plan's
   body. Proof: a test saves a plan with no marker and asserts refusal naming
   the missing approval; with a matching marker, it reaches approved.
2. A hook writes the marker on human ExitPlanMode approval and not on reject or
   edit. Proof: a unit test drives the hook with an approval payload (marker
   written) and a rejection payload (no marker).
3. The marker binds the exact plan: saving a plan whose body digest differs from
   the marker is refused. Proof: a test approves body A, edits to body B, saves,
   and asserts refusal.
4. Implementation stays blocked (`update_run` refuses the implementing phase)
   until `plan_status` is `approved`. Proof: the existing IMPL_PHASES gate, now
   reachable only through the marker; a test asserts awaiting-approval blocks it.
5. A documented human-confirmed CLI fallback records an attributed approval,
   refused without `--by`. Proof: a test runs the fallback with and without
   `--by`.
6. Every existing plan-save gate still runs unchanged. Proof: the existing
   plan-save gate tests stay green with no weakening.

## Technical Approach

**The digest is over the plan BODY**, not the file. `plan save` adds machine
frontmatter (issue, status, saved, decisions_reviewed); the human approves the
body. So the marker and the gate both digest the body (`plans.py` already
separates body from header), and the agent presents that exact body in
ExitPlanMode. A summary that differs from the saved body fails the digest bind —
which is correct: you approve what gets saved.

**Task 1 — the approval hook + marker.** A new `plan_approval_hook.py`
(PostToolUse, matcher `ExitPlanMode`), wired in `.claude/settings.json`. On an
*approved* result it writes `.factory/plan-approval.json`
`{plan_sha256, approver, at}` where `plan_sha256` is the sha256 of the plan
content it was shown; on a rejected/edited result it writes nothing. The marker
is gitignored ephemeral state (0025).

**Task 2 — the plan-save gate + fallback.** `plans.py`: `plan save` computes the
body digest, reads `.factory/plan-approval.json`, and sets `approved` only when a
marker exists and its `plan_sha256` matches; otherwise it writes the plan as
`awaiting-approval` and refuses to mark it approved, with a message that says to
present the plan in plan mode and approve it. The CLI fallback,
`forge plan approve --by <name>`, writes a human-attributed marker for the
current plan's body digest (refused without `--by`), for headless runs. Every
other gate in `plan save` runs first, unchanged.

**Rejected:** digesting the whole file (the machine frontmatter would never
match what the human saw); a marker without a digest (an edit after approval
would ride it — AC3 forbids); making the CLI fallback the primary path (defeats
the plan-mode gate 0029 chose); emulating plan mode in Codex (the fallback
covers headless honestly).

## Decisions

Decision `0029-plan-approval-in-plan-mode` (proposed) is the design authority and
must be **accepted** before decomposition — human chat confirmation. Its two
design choices (ExitPlanMode marker as the gate; a CLI fallback) were put to the
human via AskUserQuestion and answered. No other new decisions.

## Surface Impact

| Surface | Classification | Notes |
| --- | --- | --- |
| Runtime behavior | Changed | plan save no longer self-approves; approval requires the human marker. |
| API | N-A | No HTTP surface. |
| Data/schema | Changed | New ephemeral `.factory/plan-approval.json` (gitignored, 0025); no committed-artifact shape changes. |
| CLI/ops | Changed | `plan save` semantics change; new `forge plan approve --by` fallback. |
| UI | Unchanged by design | The board does not approve plans. |
| Docs | Changed | The planner prompt and CLAUDE.md adapter describe the plan-mode approval step and the fallback. |
| Tests | Changed | Hook approve/reject; digest bind; awaiting-approval blocks implementation; fallback with/without --by; existing gates stay green. |

## Task Decomposition

Two sequential tasks (0002):

1. **The ExitPlanMode approval hook and marker** → AC2. Scope:
   `factory/scripts/plan_approval_hook.py` (new), `.claude/settings.json`,
   `.gitignore`, `factory/tests/test_gates.py`.
2. **The plan-save gate, digest bind, and CLI fallback** → AC1, AC3, AC4, AC5,
   AC6. Scope: `factory/scripts/forge_cli/plans.py`,
   `factory/scripts/forge.py` (the `plan approve` subcommand),
   `factory/prompts/planner.md`, `.claude/CLAUDE.md`,
   `factory/tests/test_gates.py`.

`user_facing: false` — a process/gate change, no user-visible product surface.

## Risks

- **Digest mismatch between what's shown and what's saved.** Mitigation: digest
  the body only, and the discipline is to present the saved body in
  ExitPlanMode; AC3's test locks the bind.
- **A hook that writes the marker on presentation, not approval.** Mitigation:
  the hook keys on the approval RESULT in the PostToolUse payload; AC2's
  rejection test fails if it writes on reject.
- **Locking myself out.** This changes the very gate this plan will later pass
  through. Mitigation: the CLI fallback exists precisely so an approval can
  always be recorded; and this story's own plan is approved in plan mode before
  the enforcement lands, so the bootstrap is clean.
- **Recurring-findings tripwire.** No RECURRING class touches plans.py/hooks;
  the two open classes are in upgrade.py (repository-escape, now FORGE-BOUNDARY-1)
  and review provenance. If review flags one here, escalate, don't fold in.

## Verify Plan

Deterministic, the same commands CI runs:

```bash
python3 factory/scripts/verify.py
```

running structural, typecheck slot, and `pytest factory/tests -q`. Per-task
verify commands are runnable pytest selections. What falsifies the work: a
`plan save` that reaches approved with no marker; a marker written on rejection;
an edited plan riding a stale marker; implementation proceeding at
awaiting-approval; a fallback approval with no `--by`. Each has a test. Review is
one autoreview pass, three lenses (0011).
