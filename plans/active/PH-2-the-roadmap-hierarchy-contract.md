---
issue: PH-2
title: The roadmap hierarchy contract
status: draft
story: PH-2
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
  - 0019-client-signoff
---


# PH-2 — The roadmap hierarchy contract

## Problem

The roadmap claims a hierarchy it does not enforce. `check_item` requires only
`key` and `title`; `epic` is validated as "a string if present", so a story
with no parent, no narrative, no acceptance criteria and no `depends_on` is a
legal roadmap entry today.

The consequences are not cosmetic. `epic_gating()` derives epic-to-epic order
from story edges, and `leverage()` ranks the frontier by transitive unblocks —
both read fields nothing requires anyone to write. A roadmap whose stories omit
`depends_on` produces an empty dependency graph, so every story looks startable
and `forge roadmap parallel` recommends fanning out work that actually has an
order. PH-4 then presents that as an epic map, which is how a missing field
becomes a wrong answer on a screen.

`roadmap import` is the only route that writes epics, and it requires an
accepted `epics-approved` decision plus a digest-bound grill. So after sign-off
there is no way to add an epic at all — which is why "every story names a known
epic" cannot simply be switched on.

## Scope / Non-goals

In scope: field requirements at the three routes that author story content, a
command to add an epic after sign-off, the schema note, and a doctor report for
legacy roadmaps.

Out of scope, deliberately:

- **`save_roadmap` stays unvalidated.** Content is checked where it is written.
  `mark_status` (intake, pr_ready), `cmd_assign`, `cmd_link_spec` and
  `cmd_heal` do not author story fields, and gating them would break legacy
  roadmaps at exactly the moments recovery is needed. `check_dag` continues to
  run on every save, `heal` included.
- **The `--no-spec` carve-out survives.** Decision 0014 puts authorization at
  `plan save`, not at capture, and `plans.py` already refuses to build
  spec-debt stories. Removing it deletes a designed path rather than closing a
  hole.
- **No board or API work.** That is PH-4, which depends on this.

## Acceptance Criteria

1. A story authored through `roadmap derive`, `roadmap import` or `roadmap add`
   is refused unless it names a known epic and carries a narrative, non-empty
   acceptance criteria, a skill, and an explicit `depends_on` array — `[]`
   included, so "no dependencies" is stated rather than omitted.
2. Every epic carries `id`, `title`, `objective`, and `source_refs` that
   resolve to real repo-relative paths.
3. `forge roadmap epic add <id> --title --objective --source-ref` creates an
   epic after sign-off and refuses a duplicate id.
4. `roadmap add` requires `--epic`; `--no-spec --reason` still produces an
   `origin: adhoc` story with a `spec_debt_reason`, covered by a test.
5. Duplicate ids and keys, unknown epics, unknown and self dependencies, and
   cycles are all refused.
6. A legacy roadmap with no epics still loads, still flips status, and is
   reported by `forge doctor` without incrementing its failure count.
7. This repo's own roadmap carries an epic and its stories point at it.

## Technical Approach

One `check_story_contract(item, known_epics)` and one `check_epic_contract`,
both in `forge_cli/roadmap.py`, called from `cmd_derive`, `cmd_import` and
`cmd_add`. `check_item` keeps its type checks; the contract functions add the
presence requirements, so the two concerns stay separable when a legacy route
needs the weaker one.

Only `depends_on` is ever authored. Everything else is derived from what
already exists, and this story adds no new derivation:

| Derived | Source |
|---|---|
| ready frontier | `ready_pending()` |
| direct `unblocks` | reverse of `depends_on` |
| leverage | `leverage()` |
| epic-to-epic gating | `epic_gating()` |
| progress | `board._summary()` |

`epic add` writes through `save_roadmap`'s existing `epics` parameter. It
requires sign-off like the other authoring routes, but not the `epics-approved`
decision — that gate belongs to `import`, which replaces the whole list.

## Decisions

One new decision: **story dependencies are the only authored ordering.** Epic
order, the frontier, and leverage are derived, and no artifact may carry a
second hand-written ordering of the same work. Recorded as
`docs/decisions/00NN-derived-ordering.md` before decomposition; acceptance is
human confirmation.

This is what makes `build_waves` removable in PH-3 rather than a coincidence —
a wave list is exactly the second ordering this decision forbids.

## Surface Impact

| Surface | Classification |
|---|---|
| Runtime behavior | **Changed** — three authoring routes refuse incomplete stories |
| API | **N/A** — no HTTP surface in this story; the projection is PH-4 |
| Data / schema | **Changed** — `factory/schemas/roadmap.json` `item_fields_note` states the required fields |
| CLI / ops | **Changed** — new `roadmap epic add`; `roadmap add` requires `--epic`; one advisory `doctor` check |
| UI | **Unchanged by design** — the epic map that consumes this is PH-4; a projection with no consumer is not this story's scope |
| Docs | **Changed** — the new decision record; `WORKFLOW.md` roadmap section |
| Tests | **Changed** — refusal cases, the `--no-spec` carve-out, and a legacy epic-less roadmap that still works |

## Task Decomposition

1. **PH-2.1 — the contract functions.** Extract `check_story_contract` and
   `check_epic_contract`; wire into `cmd_derive`, `cmd_import`, `cmd_add`;
   leave `save_roadmap` and the status routes untouched.
2. **PH-2.2 — `roadmap epic add`, and `--epic` required.** Add the command;
   require `--epic` on `add`; cover the `--no-spec` carve-out explicitly.
3. **PH-2.3 — schema note, decision, doctor.** Update `item_fields_note`;
   record the derived-ordering decision; report legacy epic-less roadmaps
   advisory-only.
4. **PH-2.4 — backfill this repo's roadmap.** One epic, its stories pointed at
   it, through the new command rather than by hand.

Sequential in one worktree. PH-2.2 must follow PH-2.1, because requiring
`--epic` without a way to create an epic locks the roadmap.

## Risks

- **Locking a legacy roadmap out of its own recovery.** `cmd_heal` runs at the
  post-merge moment when a roadmap is least well-formed. Mitigated by scoping
  validation to the authoring routes, and by a test that heals a roadmap whose
  stories have no epic.
- **Backfill by hand.** PH-2.4 through the new command, not an editor, or the
  backfill proves nothing about the command.
- **The `--no-spec` path quietly dying.** It is not covered today. PH-2.2 adds
  the test before touching `add`.

## Verify Plan

```
FACTORY_STRUCTURAL_CMD="python3 factory/scripts/check_dual_runtime.py" \
FACTORY_TYPECHECK_CMD="python3 factory/scripts/check_factory_scaffold.py" \
FACTORY_TEST_CMD="uv run --with pytest python -m pytest factory/tests -q" \
python3 factory/scripts/verify.py
```

The env vars are not optional: `verify.py` falls back to `pnpm check:all` when
they are unset and reports red against a Node stack this repo does not have.

Plus `python3 factory/scripts/check_agents_hygiene.py`, and one branch-wide
autoreview at the review phase.

Deterministic tests, all in `factory/tests/test_gates.py`:

- a story with no epic, no acceptance criteria, or no `depends_on` is refused
  at each of `derive`, `import` and `add`
- an epic whose `source_refs` do not resolve is refused
- `epic add` refuses a duplicate id
- `add --no-spec --reason` still produces `origin: adhoc` with the reason
- a self-dependency and a cycle are both refused
- a legacy epic-less roadmap loads, flips status, and heals
- `doctor` reports the legacy roadmap without incrementing failures
