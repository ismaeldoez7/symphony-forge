---
issue: FORGE-BOARD-7
title: knacklabs-sanitise-project skill (deterministic repo hygiene)
status: approved
saved: 2026-08-09T03:31:09+00:00
story: FORGE-BOARD-7
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
---

# Plan — FORGE-BOARD-7: knacklabs-sanitise-project + update-triggered health cadence

> Story FORGE-BOARD-7, epic `traceable-board` (its final story), spec
> `docs/specs/traceable-board.md`. Worktree `/Users/dev/Workdir/symphony-forge-SANITISE`.

## Problem

Two things:
1. **No deterministic repo hygiene.** A vendored client silently rots: orphaned
   mode/quickfix windows, stale task-scoped `.factory` state from a crash, roadmap
   drift, incomplete/unlinked done stories, committed cruft (`.DS_Store`) or leaked
   secrets. Detectors exist and compose (`doctor`, `roadmap heal`, `project
   audit`/`board_problems`), but there is no single `forge sanitise`, and three
   actions have no primitive: closing a crashed window, standalone stale-state
   detection, a repo-wide secret/cruft scan.
2. **The daily health CI wastes tokens.** `harness-health.yml` runs on a daily cron
   in every client — cloning the harness and running audits/upgrade even when
   nothing changed. The value only exists when the harness has *actually* updated,
   so the check should be **update-triggered, not calendar-daily**.

The crux for both: fix only what is unambiguously safe and **REPORT the rest, never
auto-deleting evidence or fabricating** (`project-record`, 0025).

## Scope / Non-goals

**In scope:** a deterministic `forge sanitise` (with `--check` report-only mode) run
**on demand** (via its skill), composing existing detectors + three new primitives;
the `knacklabs-sanitise-project` skill; and **removing `harness-health.yml`'s daily
cron**, replacing it with an update-triggered run (client CI events + manual
dispatch; cheap version-compare first, heavy work only when behind).

**Non-goals:** NO daily/scheduled sanitise or health job; NO machinery upgrade /
re-authoring here (upgrade skill); NO `doctor --fix` machine mutation inside
sanitise; NO auto-delete of task-scoped `.factory` evidence, auto-close of a
possibly-live window, or fabrication.

## Acceptance Criteria

1. `forge sanitise` **fixes only unambiguously-safe things** (roadmap heal drift;
   remove TRACKED cruft `.DS_Store`/`__pycache__`/`*.pyc`) and **REPORTS everything
   needing judgment** (board gaps + missing pr-links via `project_gaps`; secrets;
   stale task-scoped `.factory` state; open windows; untracked cruft; doctor
   advisories). Never auto-deletes evidence, never fabricates.
2. `forge sanitise --check` fixes nothing (read-only, CI-safe) and exits nonzero iff
   any issue exists; plain `forge sanitise` applies the safe fixes and exits nonzero
   iff any UNRESOLVED issue remains.
3. Three primitives: (a) `forge mode abandon` closes a crashed window (ledgered)
   without `mode done`'s completion gates; (b) a standalone stale-task-state
   detector (reuses intake's stale-file list — reports, never clears); (c) a
   repo-wide secret/cruft scan (reuses `context.SECRET_PATTERNS` over source +
   lists untracked droppings).
4. A `knacklabs-sanitise-project` skill wraps `forge sanitise` (registered in
   `setup`, on demand — NOT scheduled).
5. `harness-health.yml`'s daily `schedule` cron is REMOVED. It triggers on
   `workflow_dispatch` (manual) and the client's `push: main` (its own CI cadence);
   the job does the cheap `VENDORED_FROM` vs upstream-HEAD compare and only runs the
   upgrade/PR when actually behind — no daily token spend.

## Technical Approach

### `forge sanitise` — new `factory/scripts/forge_cli/sanitise.py`

`cmd_sanitise` composes read-only detectors and applies only safe fixes:
- **Report (import seams):** `project.project_gaps(base)` (board+pending+vendor),
  the new secret/cruft scan, the new `stale_task_state` detector,
  `quickfix`/`mode list` open windows, `doctor`'s read-only checks.
- **Fix (safe only):** `roadmap.heal_items` when drift exists; `git rm --cached`
  tracked cruft (reuse `check_repo_budget`'s globs).
- `--check` skips fixes. Structured report + summary; exit 1 iff any issue.

### The three primitives

- **`forge mode abandon`** (`quickfix.py`) — closes the active window with an
  `abandoned` ledger row + reason, bypassing the `mode done` gates; refuses if none open.
- **`stale_task_state(base)`** — factor intake's `stale_files` list
  (`intake.py:65-90`) into a reusable reporter (does NOT clear; clearing stays the
  human-gated `intake --discard-active`).
- **Secret/cruft scan** — repo-wide, reusing `context.SECRET_PATTERNS` over `git
  ls-files` source + an untracked-droppings lister (`git status --porcelain
  --ignored`). Reports; never auto-removes secrets.

### Update-triggered health cadence (`harness-health.yml`)

Remove `schedule:`; keep/add `workflow_dispatch` + `push: branches: [main]`. The
existing steps (clone upstream, compare `VENDORED_FROM` vs HEAD, propose `forge
upgrade` PR if behind) stay — they now run on real client activity or on demand,
cheaply short-circuiting when up-to-date. (`board-invariant.yml` already hard-gates
completeness on push:main; this only changes the *health/upgrade* cadence.)

### The skill

`install/claude/knacklabs-sanitise-project/SKILL.md` — a thin on-demand runbook: run
`forge sanitise` (or `--check`), review the report, act on reported items with the
named commands (`forge pr-link`/`mark-predates`, `forge roadmap fill`, `intake
--discard-active`, `mode abandon`). Registered in `setup`'s loop.

## Decisions

No new decision. All 28 active reviewed. Load-bearing: **project-record** + **0025**
(the fix-vs-report boundary is the honesty rule — report what needs judgment, never
delete evidence or fabricate), **0001** (every action is a deterministic command).
Removing the daily cron doesn't weaken a gate (board-invariant still enforces on
push:main); the health/upgrade check becomes event-driven per the user's cost call.
No contradiction with an active decision.

## Surface Impact

- `factory/scripts/forge_cli/sanitise.py` — NEW: `cmd_sanitise` + the secret/cruft scan.
- `factory/scripts/forge_cli/quickfix.py` — `cmd_mode_abandon`.
- `factory/scripts/intake.py` — factor `stale_task_state` (no behaviour change).
- `factory/scripts/forge.py` — register `forge sanitise` + `forge mode abandon`.
- `install/claude/knacklabs-sanitise-project/SKILL.md` — NEW; `setup` register.
- `.github/workflows/harness-health.yml` — remove daily `schedule`; trigger on
  `workflow_dispatch` + `push: main`.
- `factory/tests/test_gates.py` — seed each defect; assert fix-vs-report + no
  fabrication; assert harness-health has no `schedule:` cron.

## Task Decomposition

1. **FORGE-BOARD-7.1 — the three primitives** (no deps) — `forge mode abandon`,
   `stale_task_state` detector (factored from intake), repo-wide secret/cruft scan.
   Tests.
2. **FORGE-BOARD-7.2 — `forge sanitise` command** (dep: 7.1) — composes reporters +
   safe fixes + `--check`; exit-code semantics. Tests seeding each defect, asserting
   fix-vs-report + no evidence deletion + `--check` mutates nothing.
3. **FORGE-BOARD-7.3 — skill + update-triggered cadence + docs** (dep: 7.2) — the
   `knacklabs-sanitise-project` skill + `setup` registration; remove
   `harness-health.yml`'s daily cron → `workflow_dispatch` + `push: main`; doc rows;
   tests (skill registration; harness-health has no `schedule:`).

## Risks

- **Fix-vs-report boundary is the correctness bar** — auto-fixing anything needing
  judgment violates the honesty rule; tests pin that stale state + open windows are
  REPORTED not touched, and only tracked cruft + heal are auto-fixed.
- **`--check` must be truly read-only** — a test that it writes nothing.
- **Cadence change must not drop the completeness gate** — `board-invariant.yml`
  stays on push:main; only the health/upgrade poll becomes event-driven.
- **`--kind feature`; net-additive** (minus the removed cron line).

## Verify Plan

- **Gate tests** (`test_gates.py` hygiene section): seed an orphaned window, stale
  `.factory` artifacts, a duplicate roadmap key, a tracked `.DS_Store`, a source
  secret, a done story missing its pr-link; `forge sanitise` heals drift + removes
  tracked cruft, REPORTS the rest, touches no evidence; `--check` fixes nothing +
  exits nonzero; `forge mode abandon` closes a crashed window; `harness-health.yml`
  has no `schedule:` cron.
- **Determinism:** `check_dual_runtime.py` + `verify.py` green.
- **Live smoke:** `forge sanitise --check` on this repo reports state + exits
  deterministically; the skill is in `setup`'s loop.
