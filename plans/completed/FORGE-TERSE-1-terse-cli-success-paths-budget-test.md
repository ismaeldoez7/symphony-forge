---
issue: FORGE-TERSE-1
title: Terse CLI success paths + budget test
status: approved
saved: 2026-08-10T13:24:33+00:00
story: FORGE-TERSE-1
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
  - 0028-path-boundary-invariant
  - 0029-plan-approval-in-plan-mode
  - 0030-harness-source-is-product-in-its-own-repo
  - 0031-workflow-modes-lite
  - 0032-jit-task-planning
  - 0033-gate-a-declares-all-work-records
  - 0034-vendored-docs-are-client-safe
  - 0035-commit-belt-keeps-ledger-fresh
  - 0036-client-gates-arm-on-roadmap
---

# Plan — FORGE-TERSE-1: Terse CLI success paths + budget test

> Story FORGE-TERSE-1, epic `terse-output` (story 1 of 2), spec
> `docs/specs/terse-output.md`. Branch
> `feat/FORGE-TERSE-1-terse-cli-success-paths-budget-test`.

## Problem

Operator feedback: nobody reads the commentary. Every chatty forge command
lectures on success (`stage done` recaps the whole loop, `plan save` explains
the approval flow, `decision new` reminds about trailers), so the one line
that matters drowns and operators learn to skip output — which is how real
warnings get missed. A full inventory (planning exploration) found: 12 sites
printing pure coaching duplicated in `forge next`, 7 mixed result+coaching
lines, 4 multi-result successes, 5 coaching messages that exist NOWHERE else
(moving them is required or they're lost), 2 deliberate exceptions, only 4
test assertions in the blast radius, and zero machine consumers of any
trimmed line.

## Scope / Non-goals

**In scope:** one result line per success across the chatty commands; 5 new
`forge next` steps so no guidance is lost; the convention stated in
`forge_cli/common.py`'s docstring; the output-budget gate test; 4 test
updates.

**Non-goals:** error/refusal messages byte-identical (spec); `forge next`
keeps full coaching; report commands (`sanitise` failing runs, `doctor`
check rows, `roadmap parallel`, `audit`, `project audit`, `context list`)
keep their bodies; agent narration is FORGE-TERSE-2; NO `result()` print
wrapper (one indirection over `print()` with one implementation — the
docstring plus the budget test is the enforcement); NO flags or env vars.

## Acceptance Criteria

1. Each touched command's success path prints exactly one line: state change
   + identifiers. Two documented exceptions: `signal raise` keeps its
   worker-facing `PAUSE this thread` line (workers never run `forge next` —
   the coaching has no other route to its audience), and `stage done`'s
   conditional contract-change NOTE stays (it is ledgered evidence, not
   coaching).
2. The five otherwise-lost messages move into `forge next` as steps in the
   right phase branches: commit-the-evidence (post-ship), commit-the-pin
   (signed-off), decision hygiene (trailer + supersedes handoff), spec-debt
   clearance. Machine contracts preserved: `doctor`'s failure last-line
   (sanitise parses it), `context list`'s one-line-per-entry (gardener
   `wc -l`), the `forge doctor: ready` prefix (monkeypatched tests).
3. Folded lines keep the substrings the 11 fragile tests assert (`marked
   active`, `PR_READY`, `Accepted`, `Superseded`, `pinned to`, `Write
   access:`, argv, `not launched`, `pending: 1`, `stages.json`, `debt
   cleared`); the 4 breaking assertions are updated to the new one-line
   shapes.
4. `test_success_output_budget`: drives the touched commands' success paths
   in a scaffolded repo and asserts each prints its budgeted line count
   (1, with the two documented exceptions) — lecture-creep cannot return
   silently.
5. Errors and refusals: zero diff.

## Technical Approach

All sites from the inventory, by treatment (file:line refs verified):

- **Delete pure coaching (12):** `stages.py:695-697,1109-1110`;
  `plans.py:218-221,333-335`; `context.py:161`; `delegate.py:1162-1166`;
  `intake.py:117-120`; `pr_ready.py:368-371,377-379`; `roadmap.py:811`;
  `decisions.py:197`.
- **Trim coaching tails from mixed lines (7):** `stages.py:1072-1076`;
  `plans.py:266-269`; `record_decomposition_from_json.py:336-337`;
  `pr_ready.py:54-55`; `signal.py:91-92`; `doctor.py:921` (keep the
  `forge doctor: ready` prefix).
- **Fold multi-result into one line (4):** `decisions.py:178+192`
  (`Accepted: … (confirmed_by: X); superseded Y`); `intake.py:110+115`;
  `pr_ready.py:351+380-381` (one `PR_READY …; roadmap: {key} done` line);
  `sanitise.py:177+191` (clean run = one line).
- **Delegate chrome:** collapse `delegate.py:960,963,964,966` to one line
  preserving `Write access:`, the argv, and `not launched`:
  `Brief {rel} ({n} lines) | Write access: {YES|NO} | {argv}`.
- **`forge next` additions (phase.py):** post-ship branch (`:84-135`) gains
  commit-the-evidence and commit-the-pin steps; a decision-hygiene step
  (trailer command, supersedes flip, `confirmed_by` requirement) appears
  when an accepted-but-uncommitted or superseding decision exists; a
  spec-debt step (`roadmap.py:562-565` content) in the post-sign-off
  branches. Each is one `steps.append(...)` in the existing structure.
- **Convention:** module docstring on `forge_cli/common.py` above `fail()`:
  success = one line, state change + identifiers; coaching lives in
  `forge next`; `fail()` messages stay full.
- **Tests:** update `test_gates.py:3653,7025,7038,8915`; add
  `test_success_output_budget` (matrix of command → max lines, exercising
  the scaffold-repo fixtures already used by the existing command tests).

## Decisions

No new decisions — the one-line contract, the coaching homes, and the
full-error rule are all written in the confirmed spec (grilled with the
human 2026-08-10). Stated judgment calls: the two output exceptions in AC1,
and rejecting a shared `result()` helper (simplicity: the ladder rejects an
abstraction with one behavior; the budget test is the pin).

## Surface Impact

| Surface | Class | Notes |
|---|---|---|
| Runtime behavior | Changed | success output shrinks; forge next grows 5 steps |
| API | N-A | — |
| Data/schema | Unchanged by design | no artifact changes |
| CLI/ops | Changed | the visible output contract; exit codes untouched |
| UI | N-A | — |
| Docs | Unchanged by design | spec already documents the contract; no doc edits needed |
| Tests | Changed | 4 updates + the budget test |

## Task Decomposition

One bounded task (disjoint scope, one worker):

1. **FORGE-TERSE-1.1 — trim + move + budget test** — the 23 output sites,
   the 5 `forge next` steps, the common.py docstring, 4 test updates, the
   budget test.

## Risks

- **A trimmed line was secretly load-bearing** — inventory found zero
  machine consumers of trimmed lines and the three real output contracts
  (doctor failure last-line, context list, doctor-ready prefix) are named
  and preserved; the full suite is the net.
- **Guidance lost rather than moved** — the five lost-message sites are
  explicitly enumerated with their target `forge next` branches; the plan
  grill checked the mapping.
- **Substring drift breaks the 11 fragile tests** — folded lines keep the
  asserted substrings verbatim; the focused suite runs before commit.

## Verify Plan

- **Gate tests:** the budget test + the 4 updated assertions + the full
  suite via `verify.py` (structural + scaffold + tests).
- **Live dogfood:** run the loop's own commands in this repo during the
  story (`stage start/done`, recorders, `pr_ready`) and confirm one-line
  successes; `forge next` shows the new steps in the right phases; error
  paths spot-checked byte-identical (`plan save` unapproved, `stage done`
  refusals).
