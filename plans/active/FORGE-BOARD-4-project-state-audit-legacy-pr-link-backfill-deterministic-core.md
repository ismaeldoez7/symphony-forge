---
issue: FORGE-BOARD-4
title: Project-state audit + legacy pr-link backfill (deterministic core)
status: approved
saved: 2026-08-08T16:31:28+00:00
story: FORGE-BOARD-4
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

# Plan — FORGE-BOARD-4: Project-state audit (the constant detector) + legacy backfill

> Story FORGE-BOARD-4, epic `traceable-board`, spec `docs/specs/traceable-board.md`.
> Worktree `/Users/dev/Workdir/symphony-forge-UPGRADE`, branch off main.
> The deterministic half of the upgrade split; FORGE-BOARD-5 (the skill) applies it.

## Problem

Upgrading a client is not a one-time event — it is a **constant process driven by
changes to Symphony itself**. As the harness gains gates and contract
requirements (this session alone added the JIT grill gate, Gate A, stories-only
mirror), every vendored client drifts behind on TWO axes: machinery (already
handled — `harness-health.yml` detects `VENDORED_FROM` vs upstream HEAD and opens
a `forge upgrade` PR) and **project-management state** (new required fields, new
completeness rules) — for which there is **no detector at all**.

Concretely on this harness repo (measured): of 17 done stories only 4 carry a
`pr-linked` event, so **11 would red `check_board_complete`** — which is why
**D-0011** keeps `board-invariant.yml` dispatch-only. And any backfill must be
**honest** — recovered from evidence, never invented (`docs/specs/project-record.md`).

## Scope / Non-goals

**In scope:** a **contract-driven** `forge project audit` (the always-on detector
that auto-reflects whatever the current harness requires), wired into the
existing continuous cadence so project-state drift surfaces alongside machinery
drift; a `forge project backfill` that recovers legacy `pr-link`s from real
GitHub merge records and reconstructs done-story card fields from committed
evidence (marking true gaps); and running it here to close D-0011.

**Non-goals:** NOT the skill (FORGE-BOARD-5 — machinery-upgrade orchestration +
guided re-authoring of *pending* stories, human-confirmed). NOT synthesizing
outcomes/ACs for shipped stories (mark, never fabricate). NOT auto-APPLYING
backfill in CI (detection is continuous; writes stay human-gated). NOT changing
`forge upgrade`/`doctor`/`check_vendor_integrity`.

## Acceptance Criteria

1. `forge project audit` is **contract-driven**: it composes the harness's
   current validators (`check_board_complete`, `check_story_contract`,
   `check_vendor_integrity`) so a NEW harness requirement is detected with no
   change to the audit. It reports per repo: done stories missing
   `pr-link`/`outcome`/`history`; pending stories missing
   `epic`/`skill`/`acceptance_criteria`/`spec`; vendor/gate drift. Pure/local
   (no network); exit non-zero iff gaps.
2. The audit runs on the **existing continuous cadence** — `harness-health.yml`
   (scheduled) runs it alongside the machinery version-check, so project-state
   drift is surfaced continuously (report/PR-comment), not only on demand.
   Detection is automatic; APPLYING the backfill stays human-gated.
3. `forge project backfill` recovers each unlinked done story's PR from the real
   GitHub merge record (`gh`) and records it via `forge pr-link`; ZERO matches →
   `predates_outcome_contract`; TWO+ ambiguous → reported+skipped (never guessed).
   Card fields (`story`/`skill`/`acceptance_criteria`) are reconstructed ONLY from
   committed evidence (archived plan / history decomposition); evidence-less stubs
   stay marked. **No PR number or card field is fabricated.** Idempotent.
4. On this harness repo, the 11 legacy done stories are pr-linked or marked so
   `check_board_complete` passes; `board-invariant.yml` is enabled on `push:
   main`; deferral **D-0011** is resolved.

## Technical Approach

### `forge project audit` — the constant, contract-driven detector (new)

New `factory/scripts/forge_cli/project.py`, `cmd_audit`, registered in `forge.py`.
It COMPOSES the harness's current validators rather than hardcoding a checklist —
this is what makes it constant as Symphony changes:

- **Done-story completeness** — reuse `check_board_complete.py`'s per-item logic
  (pr-linked set, `outcome`, `.factory/history/<key>/`, `predates_outcome_contract`).
- **Pending-story shape** — a NON-FATAL collector factored from
  `roadmap.py:check_story_contract` (the same field list, not a copy — so when the
  contract adds a field, the audit sees it too) + the `spec`/`spec_debt_reason` rule.
- **Vendor/gate drift** — reuse `check_vendor_integrity.integrity_problems()`.
- Human summary + structured list; exit 1 iff any gap. Pure/local.

### Continuous cadence — surface PM drift where machinery drift already surfaces

Extend `.github/workflows/harness-health.yml` (already scheduled; already clones
upstream + runs `forge upgrade` when behind) to ALSO run `forge project audit` and
surface project-state gaps in the same run/PR. No new schedule, no auto-write —
the constant DETECTION rides the existing cadence; APPLICATION stays the skill's
human-gated job (5b).

### `forge project backfill` — honest recovery (new, needs `gh`)

`cmd_backfill` in the same module. For each `done` story lacking a `pr-linked`
event: recover via `gh pr list --state merged --json number,title,headRefName,url`,
matching the key as PR-title prefix or `feat|fix/<key>-*` branch → unique match
records `forge pr-link <key> <url>`; ZERO → mark `predates_outcome_contract`; TWO+
→ report+skip. Reconstruct missing card fields only from the archived plan /
history decomposition; absent evidence → leave marked. The `gh` call is an
injectable seam so tests use fixtures. Idempotent.

### Dogfood + close D-0011

Run backfill here, review the `roadmap.json`/`events.jsonl` diff, confirm
`check_board_complete` passes on HEAD, flip `board-invariant.yml` to `push:
branches: [main]`, `forge defer resolve D-0011`.

## Decisions

No new decision. All 28 active reviewed (frontmatter). Load-bearing: **project-record**
(mark-don't-fabricate — honored), the traceable-board spec, **0011** (board
invariant), **0009** (vendor integrity — the audit reads, never patches gates),
**0025** (evidence lifetime). No contradiction with an active decision.

## Surface Impact

- `factory/scripts/forge_cli/project.py` — NEW: `cmd_audit`, `cmd_backfill`,
  non-fatal shape collector, injectable `gh` recovery.
- `factory/scripts/forge.py` — register `forge project audit|backfill`.
- `factory/scripts/forge_cli/roadmap.py` — factor `check_story_contract`'s field
  list for reuse (no behaviour change).
- `.github/workflows/harness-health.yml` — run the audit on the existing cadence.
- `.github/workflows/board-invariant.yml` — enable `push: branches: [main]`.
- `plans/roadmap.json`, `.factory/events.jsonl` — the harness-repo backfill data.
- `plans/deferrals.md` — resolve D-0011.
- `factory/tests/test_gates.py` — audit + backfill tests (fixtures for `gh`).

## Task Decomposition

1. **FORGE-BOARD-4.1 — `forge project audit` (contract-driven detector)** (no
   deps) — composes board-completeness + story-shape + vendor-drift; non-fatal
   collector factored from `check_story_contract`. Tests.
2. **FORGE-BOARD-4.2 — `forge project backfill` + continuous cadence** (dep: 4.1)
   — honest pr-link recovery (injectable `gh`), `predates`/report+skip, evidence-only
   card reconstruction, idempotent; wire the audit into `harness-health.yml`. Tests.
3. **FORGE-BOARD-4.3 — Dogfood + close D-0011** (dep: 4.2) — run backfill here,
   enable `board-invariant` on `main`, resolve D-0011.

## Risks

- **`gh`/network in backfill.** Injectable seam → unit tests use fixtures; the
  real run (4.3) needs `gh` auth. A worker lacking `gh` → the orchestrator runs
  4.3's command; the stage measures the committed data diff. Decide at build.
- **Honesty is the correctness bar.** Never fabricate a PR number or a card field
  with no evidence — reviewer_focus + a test that an evidence-less stub is MARKED.
- **D-0011 ordering.** `board-invariant` on `main` flips only AFTER the 11 are
  linked/marked, in the same PR; verify `check_board_complete` passes on HEAD first.
- **Base-off-#59.** Built off pre-#59 main; the only `roadmap.py` overlap is the
  factored field list — reconcile at merge if #59 lands first.

## Verify Plan

- **Gate tests** (`factory/tests/test_gates.py`): audit reports each gap class and
  exits non-zero iff gaps; the harness-health workflow invokes the audit; backfill
  links a recoverable story (fixture `gh`), marks a zero-match `predates`,
  reports+skips an ambiguous one, reconstructs a card field only from evidence and
  leaves an evidence-less stub marked; idempotent re-run is a no-op.
- **Determinism:** `check_dual_runtime.py` + `verify.py` green.
- **Live (4.3):** `forge project audit` lists the 11; `forge project backfill`
  links/marks them; `check_board_complete.py` exits 0; `board-invariant.yml`
  enabled; D-0011 resolved.

## Implementation Assumptions

<!-- Made during implementation, NOT part of the approved plan. Dev: review these before merge; promote any that matter to docs/decisions/. -->
- 2026-08-08: Project backfill marks an evidence-less done card with backfill_evidence_missing=true and reconstructs only fields explicitly represented in its archived plan or history decomposition.
