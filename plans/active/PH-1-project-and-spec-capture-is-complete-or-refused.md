---
issue: PH-1
title: Project and spec capture is complete or refused
status: approved
saved: 2026-08-04T13:36:38+00:00
story: PH-1
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


# PH-1 — Project and spec capture is complete or refused

## Problem

`record_signoff.py` checks that confirmed specs exist and that each is
referenced by a roadmap story. It never opens `docs/product/BRIEF.md`. A project
can be signed off with a brief that says nothing, and the board then has no
project identity to render — no name, no problem statement, no target outcome.

This is not hypothetical. This repository's own brief was the unfilled scaffold
until three commits ago: `## Summary` read *"One paragraph on what is being
built and why now."* The sign-off gate passed it without looking.

`forge spec confirm` has the same shape of hole. It requires Forge frontmatter
and a fresh digest-bound grill, but not one body heading. Two of the specs on
disk happen to use `Why` / `Behaviour` / `Acceptance criteria`; nothing required
it, and the retired `repo-system-of-record` draft used none of them.

The reading layer cannot be built on optional content. An Overview over a brief
with no required sections renders blanks and calls them a project.

## Scope / Non-goals

**In scope.** One shared heading parser; a single canonical brief heading set
including `Target Outcome`; sign-off refusing an incomplete brief; `spec
confirm` refusing a spec without its three required headings; `forge doctor`
reporting both gaps on projects captured before the contract.

**The two heading sets already disagree.** `harness/nestjs-react/BRIEF_TEMPLATE.md`
scaffolds `What` / `Who` / `Flows` / `Domain Concepts` / `Constraints` /
`Out of Scope (v1)`; `docs/product/BRIEF.md` uses `Summary` / `Users` /
`Key Flows` / `Domain Concepts` / `Constraints` / `Out of Scope`. A contract
cannot be enforced against both. The live brief's set is canonical; the template
is realigned onto it. The template only feeds new scaffolds, so no heading in a
brief any project has already written is renamed.

**Non-goals.** No roadmap, plan or decomposition validation — PH-2 and PH-3 own
those. No board or API change — PH-4. No change to what `spec save` accepts:
drafts stay free-form, because a draft is where thinking happens. No retro-fitting
of capability specs for already-shipped harness machinery.

## Acceptance Criteria

- `record_signoff.py` refuses when `docs/product/BRIEF.md` is missing a required
  heading, or when a required heading's body is empty, and names the heading.
- `forge spec confirm` refuses a spec without an H1 title, `## Why`,
  `## Behaviour`, or `## Acceptance criteria`, and names what is missing.
- `forge spec save` still accepts an incomplete draft.
- `harness/nestjs-react/BRIEF_TEMPLATE.md`, its conventions doc, and
  `docs/product/BRIEF.md` all carry the same canonical heading set including
  `## Target Outcome`, and no heading in the live brief is renamed.
- A brief or spec captured before this contract is reported by `forge doctor`
  and refused by nothing that already passed.
- One parser produces the heading map, and both the gate and (later) the board
  call it.

## Technical Approach

- A single `parse_sections(text) -> dict[str, str]` returning heading → body,
  placed in `factory/scripts/factory_lib.py`. It has to live there and not in a
  `forge_cli` module, because `record_signoff.py` is a top-level script that
  already imports from `factory_lib`, while PH-4's board code imports from
  `forge_cli` — `factory_lib` is the only module both sides already depend on.
  Both gates call it; PH-4 imports the same function, so the board's warning and
  the gate's refusal cannot disagree. This is the only new shared surface.
- `record_signoff.workflow_input_problems` gains a brief check appended to the
  problem list it already builds, so a missing heading is reported next to
  missing specs rather than through a second refusal path.
- `specs.cmd_confirm` checks headings *before* `require_grill`, so an incomplete
  spec is refused for the cheap, obvious reason first rather than after a grill.
- `doctor` gains two checks built with the existing `_check(..., required=False)`
  shape, so old projects are reported and never blocked.

## Decisions

No new decision is required; this story implements the capture half of the
confirmed `project-hierarchy` spec. Four active decisions bear on it directly.

**0014 — confirmed specs and derived roadmap gate client sign-off.** This story
tightens that existing gate rather than adding a parallel one; the brief check
joins the problem list `record_signoff` already builds.

**0001 — determinism contract.** The heading contract is enforced in code at the
recorder, not stated in a prompt an agent can reason past.

**0009 — frozen gate integrity.** `record_signoff.py`, `forge_cli/specs.py` and
`forge_cli/doctor.py` are vendored gate surface. Client repos receive this at
re-vendoring, never retroactively.

**0013 — always-armed planning lock.** Noted rather than relied upon: the lock
does not currently classify `factory/` as product in this repo, which is why
`FORGE-LOCK-1` exists. This story is planned and decomposed regardless.

## Surface Impact

| Surface | Classification |
|---|---|
| Runtime behavior | **Changed** — two gates refuse more than they did |
| API | **N/A** — this story has no HTTP surface; the board projection is PH-4 |
| Data / schema | **Unchanged by design** — briefs and specs are markdown; no `factory/schemas/` file governs their bodies, and inventing one would make a document a record |
| CLI / ops | **Changed** — `spec confirm` and `record_signoff.py` refusals; two advisory `doctor` checks |
| UI | **Unchanged by design** — the Overview that consumes this lands in PH-4; shipping a projection with no consumer is scope this story does not own |
| Docs | **Changed** — `BRIEF_TEMPLATE.md`, `conventions/plans.md`, `docs/product/BRIEF.md` |
| Tests | **Changed** — refusal and tolerance cases in `factory/tests/test_gates.py` |

## Task Decomposition

1. **PH-1.1 — the shared parser and the canonical brief contract.** Add
   `parse_sections`; realign `BRIEF_TEMPLATE.md` and `conventions/plans.md` onto
   the live brief's heading set; add `## Target Outcome` to all three.
2. **PH-1.2 — sign-off refuses an incomplete brief.** Extend
   `workflow_input_problems`; cover a missing heading, a present-but-empty
   heading, and a complete brief.
3. **PH-1.3 — spec confirm refuses an incomplete spec.** Heading check before
   the grill; `spec save` unaffected.
4. **PH-1.4 — doctor reports capture gaps without blocking.** Two advisory
   checks against a legacy fixture.

Tasks run in this order in one `PH-1` worktree. PH-1.1 must land before PH-1.2,
because PH-1.2 makes the heading set a refusal and the template must already
satisfy it.

## Risks

- **Locking every scaffolded project — and the test suite — out of the gate.**
  This is the story's real risk and it is larger than task ordering. The `repo`
  fixture in `factory/tests/test_gates.py` builds each test repo with
  `forge.py init`, which copies `harness/nestjs-react/BRIEF_TEMPLATE.md` into
  `docs/product/BRIEF.md`; the shared `sign_off()` helper then runs
  `record_signoff.py` and asserts it exits 0. Dozens of tests call `sign_off`.
  So the moment PH-1.2's refusal exists, an unrealigned template does not fail
  one scaffold — it fails most of the suite at once.

  This cuts both ways and is the reason the ordering is safe: the suite is
  already the regression test for template drift. PH-1.1 lands the template and
  the parser; PH-1.2 lands the refusal. If the template is ever changed away
  from the canonical set later, `sign_off()` goes red across the board rather
  than a client discovering it at their own sign-off.
- **Heading-casing drift.** The contract uses the casing on disk. A test asserts
  the exact strings, so any future rename is a deliberate, failing change rather
  than a silent one.
- **Refusing a brief that is merely terse.** "Empty body" must mean no
  non-whitespace content, not "shorter than N characters". A word-count
  threshold would refuse a legitimately short constraint list; the check tests
  emptiness only.
- **Doctor noise.** Two more lines on every run. Kept non-required and emitted
  only when a gap exists.

## Verify Plan

Deterministic sequence, with this repo's real commands:

```bash
FACTORY_STRUCTURAL_CMD="python3 factory/scripts/check_dual_runtime.py" \
FACTORY_TYPECHECK_CMD="python3 factory/scripts/check_factory_scaffold.py" \
FACTORY_TEST_CMD="uv run --with pytest python -m pytest factory/tests -q" \
python3 factory/scripts/verify.py
```

Per task, the focused check:

```bash
uv run --with pytest python -m pytest factory/tests/test_gates.py -q \
  -k "brief or signoff or spec_confirm or doctor"
```

Then one autoreview pass across quality, performance and security, and
`./forge outcome set` before `pr_ready.py`. No functional check: this story has
no user-facing surface — the decomposition records `user_facing: false`.
