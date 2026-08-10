---
issue: FORGE-ALIGN-2
title: Emptiness and coverage are audit failures
status: approved
saved: 2026-08-10T10:08:02+00:00
story: FORGE-ALIGN-2
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
---

# Plan — FORGE-ALIGN-2: Emptiness and coverage are audit failures

> Story FORGE-ALIGN-2, epic `strict-alignment` (story 2 of 3), spec
> `docs/specs/strict-alignment.md`. Branch
> `feat/FORGE-ALIGN-2-emptiness-and-coverage-are-audit-failures`.

## Problem

Every detector reports OK on emptiness. `project_gaps()`
(`forge_cli/project.py:25-39`) composes done-story + pending-story +
vendor-drift over items that EXIST, so an absent or empty roadmap yields
"Project audit OK". `doctor`'s `legacy_roadmap_gaps` (`doctor.py:153-157`)
early-returns `[]` when `plans/roadmap.json` is missing. The one real coverage
check — confirmed specs must be referenced by roadmap stories — lives only
inside sign-off (`record_signoff.py:65-78`) and runs exactly once. And the
migrate skill never mentions specs, epics, or the roadmap, which is how
minegate migrated with 20 decisions' worth of discovery, zero specs, and no
roadmap without a single command saying a word.

## Scope / Non-goals

**In scope:** two new gap kinds in `project_gaps` (`no-roadmap`,
`spec-coverage`); a shared `unreferenced_confirmed_specs()` helper reused by
sign-off; the doctor early-return fix; the migrate-skill capability-gap step;
the adopt closing-hint line; tests.

**Non-goals:** NO CI/workflow changes and NO arming logic — hard-failing
client CI is FORGE-ALIGN-3 (in clients, these gaps surface today via
harness-health's issue-only `project audit` run; local `project audit` /
`sanitise --check` exit 1 — exactly the spec's "visible pressure" tier). NO
board UI change (its grey "unreferenced" prose stays; display-only duplicate
of the computation, accepted). NO auto-generation of specs/epics/roadmap
content anywhere (project-record: mark, never fabricate). NO new decision
records — every semantic below is written in the confirmed spec (gap sources,
gap kinds, severity split).

## Acceptance Criteria

1. A repo with discovery material (any of: harvested context-ledger entries,
   `docs/decisions/` records, confirmed specs) but `plans/roadmap.json`
   absent, empty, or without epics fails `project audit` and
   `sanitise --check` with a named `no-roadmap` gap that cites the authoring
   commands. A fresh `forge init` scaffold (no discovery) stays clean.
2. A confirmed spec no roadmap story references is a named `spec-coverage`
   gap (one per spec) with non-zero exit — checked continuously, not only at
   sign-off. Only reported when the roadmap has items (otherwise `no-roadmap`
   already covers it).
3. `forge doctor` reports the missing-roadmap-with-discovery state instead of
   returning clean (advisory tier, consistent with doctor's role; the exit-1
   teeth live in audit/sanitise).
4. The migrate skill gains an explicit capability-gap step (state what's
   missing, name `forge spec save/confirm` + `roadmap derive`/`epic add`,
   never fabricate); `forge adopt`'s closing hint names specs and roadmap.
5. Sign-off behavior is unchanged (its check now calls the shared helper);
   the harness repo itself audits clean (verified: all confirmed specs are
   referenced; 3 epics, 24 items).

## Technical Approach

### Shared helper — `factory/scripts/forge_cli/specs.py`

`unreferenced_confirmed_specs(base) -> list[str]`: the exact set-difference
from `record_signoff.py:65-78` (confirmed `spec_records` paths minus the
`item["spec"]` posix paths in `plans/roadmap.json`), reading the roadmap with
`load_json` directly — no import of `roadmap.py`, so no cycle.
`record_signoff.workflow_input_problems` swaps its inline block for the
helper (byte-identical problem strings). `board.py`'s `_summary` copy is
deliberately left alone (display-only).

### Gap kinds — `factory/scripts/forge_cli/project.py`

`alignment_gaps(base)` appended inside `project_gaps()` (so `project audit`,
`sanitise --check` — which streams every gap as `board-<kind>` — and the
client harness-health issue all inherit it with zero further wiring):

- **discovery material** = any of: context ledger entries with status
  `harvested`, `docs/decisions/[0-9]*.md` records, confirmed `spec_records`.
- **no-roadmap**: discovery present AND (`plans/roadmap.json` missing OR no
  `items` OR no `epics`) → one gap whose detail names what exists, what is
  missing, and the commands (`forge spec save/confirm`, `forge roadmap
  derive` pre-sign-off / `roadmap epic add` + `roadmap add` after).
- **spec-coverage**: roadmap has items → one gap per
  `unreferenced_confirmed_specs()` path, naming `forge roadmap link-spec` /
  `roadmap add`.

### Doctor — `factory/scripts/forge_cli/doctor.py`

`legacy_roadmap_gaps`: replace the missing-file early-return: when the file
is absent AND discovery material exists → `[("roadmap", "plans/roadmap.json:
absent while discovery material exists — forge roadmap derive (pre-sign-off)
or roadmap epic add + add")]`; absent without discovery → `[]` as today.
Reported through the existing `[opt]` advisory printer; no failure-count
change (AC3).

### Docs

- `install/claude/knacklabs-migrate-project/SKILL.md`: insert step 8
  "Name the capability gap" (existing 8-10 renumber to 9-11): after
  harvest/rehome, check confirmed specs / epics / roadmap; SAY what is
  missing and name the authoring paths; `forge project audit` now names
  these as gaps; never author specs/roadmap content from harvested material
  without the human choosing.
- `forge_cli/adopt.py` closing hint: one added line after the harvest line —
  save/confirm capability specs then derive the roadmap; `forge project
  audit` names what's missing.

## Decisions

No new decisions — gap sources, kinds, and the severity split (local exit 1 +
client CI issue now; hard client CI in FORGE-ALIGN-3 behind the arm-on-roadmap
rule) are all written in the confirmed spec. The one judgment call made here
and stated openly: `board.py`'s duplicate unreferenced-specs computation stays
(display-only, refactoring it is churn outside this story's criteria).

## Surface Impact

| Surface | Class | Notes |
|---|---|---|
| Runtime behavior | Changed | audit/sanitise/doctor report new gap kinds |
| API | N-A | — |
| Data/schema | Unchanged by design | no artifact/ledger format changes |
| CLI/ops | Changed | project audit + sanitise --check exit 1 on the new gaps |
| UI | Unchanged by design | board grey prose stays; ALIGN-3 owns CI teeth |
| Docs | Changed | migrate skill step; adopt hint |
| Tests | Changed | seeded-repo coverage for both kinds + fresh-scaffold guard |

## Task Decomposition

One bounded task (disjoint scope, one worker):

1. **FORGE-ALIGN-2.1 — gap kinds + doctor + docs + tests** — helper
   factoring; `alignment_gaps`; doctor fix; skill step; adopt hint; tests.

## Risks

- **False alarm on fresh scaffolds** — guarded by the discovery-material
  predicate and pinned by a fresh-scaffold test.
- **Sign-off regression from the helper swap** — problem strings kept
  byte-identical; existing sign-off gate tests are the net.
- **Dogfood red on the harness repo** — pre-verified clean (empty
  unreferenced set); a post-implementation `project audit` run in this repo
  is part of verify.
- **Legit pre-roadmap discovery phase now audits red** — deliberate and
  spec'd: the gap IS the visible pressure; the message names the exact
  commands, and `forge next` already prescribes the same steps.

## Verify Plan

- **Gate tests** (`test_gates.py`, seeded scaffold pattern):
  `test_project_audit_flags_discovery_without_roadmap` (decision record
  seeded, no roadmap → exit 1, `no-roadmap` named, commands cited; then epic
  + story added → gap clears); `test_project_audit_clean_on_fresh_scaffold`;
  `test_project_audit_flags_unreferenced_confirmed_spec` (roadmap with items
  + confirmed spec unreferenced → `spec-coverage`; `link-spec` clears);
  `test_doctor_reports_missing_roadmap_with_discovery`; one sanitise
  assertion that the gap streams through as `board-no-roadmap`; existing
  sign-off tests unchanged and green.
- **Determinism:** `check_dual_runtime.py`, `verify.py` (full suite).
- **Live dogfood:** `forge project audit` and `forge sanitise --check` on
  this repo stay green; `forge doctor` output unchanged here (roadmap
  present).
