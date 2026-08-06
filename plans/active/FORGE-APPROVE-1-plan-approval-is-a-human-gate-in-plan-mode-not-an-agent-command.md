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

# FORGE-APPROVE-1 — Plan approval is a human gate, not an agent command

## Problem

`forge plan save` records a plan and sets `plan_status = "approved"` in one
agent-run step. It requires a grill, but the grill is self-authored and the
approval is a command the agent runs — so an agent can plan, grill, and approve
its own work, then implement. The always-armed lock (0013) blocks product writes
without an *approved* plan but trusts whatever set the field. No human is in the
loop.

The intended fix was a hook on `ExitPlanMode`. **Verified infeasible**: Claude
Code fires no PreToolUse/PostToolUse hook for plan-mode transitions (#21282);
`ExitPlanMode` fires only `PermissionRequest`, a decision-gate *before* the human
decides, which cannot record that the human approved *this* plan. So plan mode is
the human-review presentation, and the enforcement is an explicit
human-attributed approval command — the same trust model `decision accept` and
client sign-off already use (decision 0029, corrected).

Grounding (read against the code): `plan save` (`plans.py:180,186`) writes
`status: approved` and sets `plan_status`. `update_run.py:68` refuses to set
`approved` via its flag and already knows `awaiting-approval` (`:24`).

## Scope / Non-goals

In scope: the `plan save` gate change, the `forge plan approve --by` command that
writes the digest-bound marker, and tests.

Out of scope, deliberately:

- **The other plan-save gates are untouched.** Grill freshness,
  decisions_reviewed coverage, contradiction signals, Surface Impact all still
  run — this adds the human gate, it does not replace them.
- **No retro-approval of existing plans.** PH-4/PH-5 and this bootstrap plan
  shipped/ship under the old flow; the gate governs plans from here.
- **No plan-mode hook.** Infeasible (#21282); if Claude Code adds one, a
  follow-up can bind the marker to it. The CLI command stays the auditable path.
- **Decision-number / roadmap-file merge collisions** (surfaced in setup) are the
  known merge-fragility class, a separate decision — not folded in.

## Acceptance Criteria

Verbatim from the story, each with its proof:

1. `plan save` sets `plan_status` to `awaiting-approval` and refuses `approved`
   without a fresh `.factory/plan-approval.json` whose digest matches the plan's
   body. Proof: a test saves with no marker (refused, message names the missing
   approval); with a matching marker it reaches approved.
2. `forge plan approve --by <name>` writes the marker for the current plan's body
   digest and is refused without a human `--by`. Proof: a test runs it with and
   without `--by`.
3. The marker binds the exact plan: saving a plan whose body digest differs from
   the marker (an edit after approval) is refused. Proof: approve body A, edit to
   body B, save, assert refusal.
4. Implementation stays blocked (`update_run` refuses the implementing phase)
   while `plan_status` is `awaiting-approval`. Proof: a test asserts it.
5. Every existing plan-save gate still runs unchanged. Proof: the existing
   plan-save gate tests stay green with no weakening.

## Technical Approach

**The digest is over the plan BODY, not the file.** `plan save` adds machine
frontmatter (issue, status, saved, decisions_reviewed); the human approves the
body. Marker and gate both digest the body (`plans.py` already separates body
from header), so what is approved is what gets saved.

One task:
- `factory/scripts/forge_cli/plans.py`: `plan save` computes the body digest,
  reads `.factory/plan-approval.json`, and sets `approved` only when a marker
  exists and its `plan_sha256` matches. Otherwise it writes the plan as
  `awaiting-approval` and refuses to approve, with a message telling the human to
  run `forge plan approve` (after reviewing in plan mode). Every existing gate
  runs first, unchanged. Add `cmd_plan_approve(args)`: refuse without `--by`,
  digest the current active plan's body, write the marker `{plan_sha256,
  approver, at}`.
- `factory/scripts/forge.py`: wire the `plan approve --by` subcommand.
- Docs: `factory/prompts/planner.md` and `.claude/CLAUDE.md` describe the
  review-in-plan-mode-then-`plan approve` step.

**Rejected:** digesting the whole file (machine frontmatter never matches what the
human saw); a marker without a digest (an edit rides it — AC3 forbids); a
plan-mode hook (infeasible, #21282); auto-approval (defeats the gate).

## Decisions

Decision `0029-plan-approval-in-plan-mode` (accepted, with a dated correction of
the hook approach) is the design authority. Its mechanism choices were put to the
human via AskUserQuestion and answered. No other new decisions.

## Surface Impact

| Surface | Classification | Notes |
| --- | --- | --- |
| Runtime behavior | Changed | plan save no longer self-approves; approval requires the human marker. |
| API | N-A | No HTTP surface. |
| Data/schema | Changed | New ephemeral `.factory/plan-approval.json` (gitignored, 0025); no committed-artifact shape changes. |
| CLI/ops | Changed | `plan save` semantics change; new `forge plan approve --by`. |
| UI | Unchanged by design | The board does not approve plans. |
| Docs | Changed | planner.md and CLAUDE.md describe the review-then-approve step. |
| Tests | Changed | no-marker refusal; approve with/without --by; digest bind; awaiting-approval blocks implementation; existing gates stay green. |

## Task Decomposition

One task (0002):

1. **The plan-save gate and `forge plan approve --by` command** → AC1-5. Scope:
   `factory/scripts/forge_cli/plans.py`, `factory/scripts/forge.py`,
   `factory/prompts/planner.md`, `.claude/CLAUDE.md`,
   `factory/tests/test_gates.py`.

`user_facing: false` — a process/gate change, no user-visible product surface.

## Risks

- **Digest mismatch between what's shown and what's saved.** Mitigation: digest
  the body only; AC3's test locks the bind.
- **The approve command reopening self-approval.** Mitigation: it is refused
  without `--by`, and the rule (like decision accept) is human chat confirmation;
  an agent running it without a human's confirmation violates the same
  constitutional rule as self-accepting a decision.
- **Locking myself out.** This changes the gate future plans pass through, not
  this bootstrap plan. Mitigation: the command always lets a human record an
  approval; and this plan was reviewed in plan mode and approved under the old
  flow before the enforcement lands.
- **Recurring-findings tripwire.** No RECURRING class touches plans.py; the open
  classes are in upgrade.py (repository-escape, FORGE-BOUNDARY-1) and review
  provenance. If review flags one here, escalate, don't fold in.

## Verify Plan

Deterministic, the same commands CI runs:

```bash
python3 factory/scripts/verify.py
```

running structural, typecheck slot, and `pytest factory/tests -q`. Per-task
verify commands are runnable pytest selections. What falsifies the work: a
`plan save` reaching approved with no marker; an edited plan riding a stale
marker; a `plan approve` accepted without `--by`; implementation proceeding at
awaiting-approval. Each has a test. Review is one autoreview pass, three lenses
(0011).
