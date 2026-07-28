---
issue: FORGE-DELEG-1
title: Briefed, bounded, measured delegation boundary
status: approved
saved: 2026-07-27T15:21:02+00:00
story: FORGE-DELEG-1
decisions_reviewed:
  - 0001-determinism-contract
  - 0002-concurrency-one-task-per-branch
  - 0003-model-tiers-terra-explore-sol-implement
  - 0005-recurring-findings-escalation
  - 0006-lessons-ledger
  - 0007-stage-commit-loop
  - 0008-loop-health-audit
  - 0009-frozen-gate-integrity
  - 0011-orchestrator-runs-autoreview
  - 0012-project-level-memory
  - 0013-always-armed-planning-lock
  - 0014-specs-before-signoff
  - 0015-plan-contradiction-gate
  - 0016-machinery-dir-rename
---


# FORGE-DELEG-1 delegation-boundary amendment

## Problem

Shell inference could not authorize arbitrary companion commands, and source
search could not prove a required test ran. The user approved replacing both
with executable, measured contracts.

## Scope / Non-goals

- In: direct `forge delegate` argv execution, diagnostic print-only mode,
  protected launch authority/locking, literal-command routing, executable
  `{id,path,command}` test proof, stage-close execution, and legacy diagnosis.
- Out: board/UI work, nested review, shell/test-language parsing, shipped
  history migration, runner abstraction, and runner whitelist.

## Acceptance Criteria

- Delegate composes the brief, resolves the installed companion, launches
  without a shell, and points missing installs to `forge doctor --fix`.
- Print-only has no authority; background is read-only; write launches are
  foreground, single-writer, fully reaped, and bound to stage/task/brief/argv.
- Stage close is serialized through persisted done state and trusts only the
  protected ledger. Literal companion calls route to delegate.
- Required proof has normalized path plus `{path}`, `{id}`, `{report}` argv;
  fresh JUnit must match id/path exactly and leave content/Git metadata intact.
- Doctor reports legacy strings without rewriting history.

## Technical Approach

- Delegate resolves canonical plugin metadata, writes the brief, launches a
  fixed Node argv, and records running/terminal rows under one launch id.
- Authority and atomic per-task/shared-state locks live in Git control data;
  `.factory/delegations.jsonl` is diagnostic. Every terminal path empties the
  observed process tree on TERM/HUP/QUIT; unresolved descendants keep
  authority locked, and unverified reused process groups are never signalled.
- The hook routes every literal companion token through `forge delegate`.
- The recorder rejects malformed, unsafe, shell/env-wrapped proof commands.
  Stage close substitutes the three placeholders, checks exact JUnit
  `name`/`file`, and wraps the complete proof set in one exact snapshot of
  tracked content, modes, symlinks, status, index flags, protected authority,
  and descendant processes. Broader `verify_commands` run first.

## Surface Impact

| Surface | Status | Reason |
|---|---|---|
| Runtime/data | Changed | Direct delegation, protected launch rows/locks, measured proof. |
| CLI | Changed | Delegate executes; print-only diagnoses; direct calls route. |
| API/UI | Unchanged | No API or board work. |
| Docs/tests | Changed | Contracts and gate regressions cover the boundary. |

## Task Decomposition

- **DELEG-7:** delegate/hook/stage launch boundary, docs and regressions.
- **DELEG-8:** required-test schema/recorder/executor/doctor and regressions.

## Risks

- Plugin drift fails closed to doctor.
- Background proves queuing; gates prove completion.
- Decomposition commands are trusted but constrained, shell-free task content.
- Tests use a fake companion; production paths are fixed.

## Verify Plan

1. `uvx --with pytest python3 -m pytest factory/tests/test_gates.py -q -k "delegate or companion or required_test or stage_done"`
2. `python3 factory/scripts/check_dual_runtime.py`
3. `python3 factory/scripts/check_agents_hygiene.py`
4. Deterministic `factory/scripts/verify.py` with recorded command overrides.
5. One complete autoreview pass; rerun after accepted fixes until clean.
