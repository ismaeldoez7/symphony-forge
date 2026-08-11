---
issue: FORGE-ROLE-1
title: Write lockout + degraded window + routing docs
status: approved
saved: 2026-08-10T19:09:02+00:00
story: FORGE-ROLE-1
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

# Plan — FORGE-ROLE-1: Write lockout + degraded window + routing docs

> Story FORGE-ROLE-1, epic `strict-role-split`, spec
> `docs/specs/strict-role-split.md`. Branch
> `feat/FORGE-ROLE-1-write-lockout-degraded-window-routing-docs`.
> Planning-fact provenance, stated honestly: the Codex-rescue exploration
> path is BLOCKED by the companion guard (its own canonical invocation
> fails the "no shell metacharacters" test — observed twice today), so this
> plan is built from facts established and verified earlier this session;
> the JIT task grill binds the worker to re-verify every ref against HEAD.
> Un-blocking read-only rescue is in scope — the routing rule is dead
> letter without it.

## Problem

The role split runs on discipline: with an approved plan, the orchestrating
session may edit product freely (five direct edits yesterday, none
prevented), discovery drifted to Claude subagents, and the sanctioned
rescue path is blocked by its own guard. The operator's instruction:
Claude orchestrates only; Codex writes; make it a gate.

## Scope / Non-goals

**In scope:** the always-on write lockout in `pre_tool_use.py` with a
shared product/canon classifier seam; the `degraded` window kind on the
existing quickfix machinery; the companion-guard fix admitting read-only
rescue; adapter/AGENTS.md/degraded-mode.md updates; decision 0037; tests.

**Non-goals:** NO read fencing (0011's direct review stands — spec
boundary); NO full D-0007 harmonization (the lockout uses the NEW shared
classifier; migrating the four existing classifiers onto it stays deferred
— D-0007 gets a progress note, not a resolve); NO change to worker-side
write mechanics (companion writes bypass Claude hooks by construction —
worker re-verifies this claim first); NO unbounded degraded windows (same
5-file budget as quickfix: the valve is a bounded escape hatch, big
outages are multiple ledgered windows).

## Acceptance Criteria

1. With an approved plan and active stage, a session Edit/Write/Notebook
   or Bash write-shape to a product/canon path is DENIED with a message
   naming `forge delegate` and `forge mode degraded start`. Locked set
   (via the new shared classifier, repo-kind-aware): code and tests,
   `factory/` machinery incl. prompts and skills, `.github/`,
   `constitution/`, `AGENTS.md`, `WORKFLOW.md`, vendored adapters
   (`.claude/`, `.codex/`, `forge`, `harness.yaml`). Note: `.github/` and
   `AGENTS.md` move OUT of today's `PLANNING_WRITE_OK` exemption — the
   lockout's exempt set is deliberately narrower.
2. Exempt and unchanged: `docs/`, `plans/`, `.factory/` (recorders),
   `prototype/`, `.gstack/`, scratchpad, and git operations on
   worker-produced diffs (add/commit/merge; the commit belt ordering is
   untouched).
3. `forge mode degraded start --reason "<named failure>"` opens a ledgered
   window (same `plans/quickfixes/` ledger, kind `degraded`, 5-file claim
   budget); the lockout honors it; `mode done` closes it; the done record
   in the PR diff satisfies Gate A declare-all unchanged.
4. The companion guard admits provably read-only rescue invocations
   (status/resume-candidate/`task` without write flags) even when quoted,
   while still refusing write-shaped or wrapped-executor calls — the
   exploration route works again; verified live post-implementation.
5. Adapter (40-line cap, currently 39) and AGENTS.md (110-line cap, full)
   state the routing within their caps — each pays for its line by
   tightening an existing one. `docs/degraded-mode.md` documents the
   window as the single exception. Decision **0037** records the four
   grilled boundaries + the budget and classifier-seam choices.
6. Tests pin: deny-under-approved-plan (incl. AGENTS.md and `.github/`),
   allow-inside-degraded-window with claims, exemption surfaces still
   writable, the window ledger record, and the guard's read-only
   admission. `test_harness_repo_keeps_docs_and_planning_surfaces_writable`
   is updated (AGENTS.md moves sides deliberately).

## Technical Approach

- **Classifier seam:** `forge_cli/repo_kind.py` (already the repo-kind
  home) gains `locked_product_paths(base)`/`is_locked_path(...)` — the
  single source for the lockout's set; existing four classifiers untouched
  (D-0007 note appended: "fifth site consolidated at birth; four legacy
  sites remain").
- **Lockout:** in `pre_tool_use.py`, after root/window resolution and
  BEFORE the approved-plan allowance: if the target is locked and no open
  `degraded` window → deny. The approved-plan path keeps governing the
  exempt surfaces only. Bash write-shape guards reuse the existing
  detection; `git add/commit/merge/restore-on-evidence` stay pass-through.
- **Degraded window:** `quickfix.py` — `mode degraded start/done` reusing
  the lite/quickfix ledger, claim, and budget code with kind `degraded`
  and a required `--reason`; `pre_tool_use` consults it exactly as it
  consults quickfix claims today.
- **Guard fix:** the companion-guard predicate keys on ARGUMENT CONTENT
  (subcommand + absence of `--write`/executor wrapping), not on the
  presence of quoting — read-only `status`/`task-resume-candidate`/`task`
  pass; anything write-shaped or shell-wrapped still refuses toward
  `forge delegate`.
- **Docs:** adapter line tightened in place (no net growth against the
  40-cap); AGENTS.md role-split bullet absorbs the routing clause via one
  reclaim (same technique as the §8 bullet); `degraded-mode.md` rewritten
  around the window; decision 0037 created post-approval, accepted at PR
  time by the human.
- **Delegation, dogfooded:** one task, implemented by Codex via
  `forge delegate`; the orchestrator's own hands touch only the plan
  artifacts and this plan's recording commands.

## Decisions

New record **0037 `strict-role-split`** (post-approval, pre-decomposition):
the four grilled boundaries (product+canon lockout always-on; mandatory
re-delegate with no trivial carve-out; discovery routed to rescue with
0011 gate reads kept; ledgered degraded window as sole exception), plus:
5-file degraded budget (bounded valve), classifier-seam-not-full-D-0007
(scope discipline), guard admission by argument content (the routing rule
is dead letter otherwise).

## Surface Impact

| Surface | Class | Notes |
|---|---|---|
| Runtime behavior | Changed | lockout, window kind, guard admission |
| API | N-A | — |
| Data/schema | Unchanged by design | window reuses the existing ledger record shape |
| CLI/ops | Changed | `forge mode degraded start/done`; new deny messages |
| UI | N-A | — |
| Docs | Changed | adapter, AGENTS.md, degraded-mode.md, decision 0037 |
| Tests | Changed | lockout/window/guard pins + one updated writability test |

## Task Decomposition

One bounded task: **FORGE-ROLE-1.1 — lockout + degraded window + guard
fix + docs + tests** (delegated; write scope: `pre_tool_use.py`,
`repo_kind.py`, `quickfix.py`, `forge.py` registration, `AGENTS.md`,
`.claude/CLAUDE.md`, `docs/degraded-mode.md`, decision 0037 file,
`test_gates.py`).

## Risks

- **Locking the session out of its own loop** — the exempt list must keep
  every recording and command path working; the full suite plus a live
  end-to-end of THIS story's own remaining loop (recorders, stage done,
  pr_ready) is the net, since the lockout lands mid-story and the rest of
  the loop runs under it.
- **Planning-fact staleness** (no fresh exploration) — every ref is
  re-verified by the worker before editing; contract says refs are a map.
- **Guard fix opens too far** — admission is by argument content with
  write-shapes still refused; a test pins both directions.
- **Cap pressure** (40-line adapter, 110-line AGENTS.md) — same reclaim
  technique proven in TERSE-2; hygiene checks run locally pre-push.

## Verify Plan

- Gate tests above; full suite via `verify.py`; `check_agents_hygiene.py`
  and `check_dual_runtime.py` locally.
- **Live self-test:** after the worker lands the lockout, the orchestrator
  attempts a product edit in-session and MUST be denied (the story
  verifies itself); the remaining loop (records, stage done, pr_ready, PR)
  must complete untouched; a real read-only rescue invocation must launch.
