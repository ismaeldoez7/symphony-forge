---
issue: PH-3
title: Plan and task contract
status: approved
saved: 2026-08-04T17:54:15+00:00
story: PH-3
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



# PH-3 — Plan and task contract

## Problem

`plan save` requires exactly one of the nine sections the planner prompt
mandates: `## Surface Impact`. The other eight are a convention the prompt
states and nothing checks, so a plan can be saved — and approved — with no
Risks, no Verify Plan, and no Task Decomposition.

The decomposition has a different problem, and it is worse than trusting the
wrong field — it is not bound to the plan at all. `factory/schemas/decomposition.json`
has no `plan_file`, no plan digest and no `story`: the story is read from
`run.json`'s `issue_key` only when the event is appended, and `project` and
`epics` arrive from the agent unchecked against the roadmap. So a decomposition
recorded from one plan while another is active is indistinguishable from the
right one. Every other handover gate in this harness is digest-bound; this one
is not. Meanwhile `verify_commands` is not checked for runnability, which is how
a task shipped with a shell-wrapped command missing its `{path}` placeholder.

And `build_waves` is still authored. `decomposer.md` asks for it, `griller.md`
grills on it, and its only reader is `render_linear_task_graph.py`. A wave list
is a second, hand-written ordering of work whose real order is the array index
and the dependency edges — two sources of truth for one fact, and the authored
one cannot be recomputed when anything moves.

## Scope / Non-goals

In scope: the nine-section check, decomposition provenance stamping, task field
validation, and retiring authored waves.

Out of scope, deliberately:

- **The stage engine is untouched.** One active task, sequential within a
  story. This story changes what a decomposition must contain, never how it
  executes.
- **Semantic acceptance-criteria coverage stays with the plan grill.** A
  section check proves a heading has content, never that the content is right;
  claiming otherwise would put a judgment call behind a deterministic gate.
- **`build_waves` stays `optional` in the schema.** Three shipped artifacts
  under `.factory/history/` carry it, and they must keep parsing. This removes
  the field as an *authored* input, not as a readable one.

## Acceptance Criteria

1. `plan save` refuses a plan missing any of the nine sections, or carrying one
   with an empty body, and names every missing section rather than the first.
2. `project`, `story`, `epic`, `plan_file` and the plan digest are stamped into
   the decomposition from `.factory/run.json` and the roadmap, and the schema
   carries them. Agent-supplied values for those fields are ignored, not merged
   and not trusted. A decomposition whose digest does not match the active plan
   is refused, which is what makes this handover as bound as the others.
3. Every task's `verify_commands` is runnable, reusing `doctor.unrunnable_reason`
   so one definition of "this is a command, not prose" serves both callers.
4. `required_tests` may be `[]` — work with no focused automated test is real —
   but runnable verification is still required.
5. A task's `dependencies` may only name an earlier task; array order is the
   execution sequence.
6. Nothing authors `build_waves`: it is gone from `decomposer.md` and
   `griller.md`, `render_linear_task_graph.py` is deleted, and the schema field
   stays optional so historical artifacts still parse.

## Technical Approach

The section check replaces a substring test — `plans.py` currently asks whether
the literal string `## Surface Impact` appears anywhere in the body, which a
fenced example satisfies — with `factory_lib.parse_sections`, the function PH-1
made the single answer to "does this document have this section, with content".

That is a real ordering constraint, not a stylistic preference: `parse_sections`
does not exist on this story's base. PH-3 is independent of PH-1 by FILE set,
not by symbol, so PH-3.1 cannot land until PH-1 merges. The alternative —
writing a second section matcher here — is precisely the duplicate parser PH-1
spent four review cycles removing, so this story waits rather than forks.

Provenance stamping inverts the current trust direction. The recorder reads
`.factory/run.json` for the active story and the roadmap for its epic, writes
those, and drops the agent's copies. This is decision 0014's shape applied to a
different artifact: capture is not authorization, so a field an agent supplies
about the harness's own state is a claim, not a fact.

Deleting `render_linear_task_graph.py` belongs in the same task that stops
authoring the field. Split across tasks it is an orphan by construction —
either a reader with nothing to read, or a writer with no consumer.

## Decisions

No new decisions. The derived-ordering decision that justifies removing
`build_waves` is recorded by PH-2; this story consumes it. If PH-2 has not
landed it when decomposition is recorded here, that ordering claim is restated
in this plan's Technical Approach rather than assumed.

## Surface Impact

| Surface | Classification |
|---|---|
| Runtime behavior | **Changed** — `plan save` and the decomposition recorder refuse more |
| API | **N/A** — no HTTP surface in this story |
| Data / schema | **Changed** — `factory/schemas/decomposition.json` gains `story`, `plan_file` and the plan digest; `build_waves` stays optional |
| CLI / ops | **Changed** — refusal messages; `render_linear_task_graph.py` deleted |
| UI | **Unchanged by design** — the task view that consumes this is PH-4 |
| Docs | **Changed** — `factory/prompts/decomposer.md`, `factory/prompts/griller.md` |
| Tests | **Changed** — section refusals, provenance override, unrunnable commands, dependency ordering |

## Task Decomposition

1. **PH-3.1 — nine sections, not one.** Generalize the `plan save` check;
   name every missing section; cover an empty body as missing.
2. **PH-3.2 — provenance and task fields.** Stamp from run/roadmap state;
   reuse `unrunnable_reason` for `verify_commands`; allow `required_tests: []`;
   enforce backward-only `dependencies`.
3. **PH-3.3 — retire authored waves.** Remove from `decomposer.md` and
   `griller.md`, delete `render_linear_task_graph.py`, keep the schema field
   optional, and prove a historical artifact still parses.

Sequential in one worktree. PH-3.1 additionally waits on PH-1 reaching main,
because the parser it calls is added there.

## Risks

- **Refusing the repo's own plans.** The nine-section rule applies to plans
  this repo has already written. PH-3.1 runs the check against every file under
  `plans/` before it lands; any that fail are fixed in that task or the rule is
  wrong.
- **Stamping the wrong story.** Provenance is only as good as `run.json`. The
  recorder refuses when the roadmap has no matching story rather than inventing
  one.
- **`unrunnable_reason` was written for doctor.** Reusing it changes its
  blast radius from advisory output to a refusal. PH-3.2 covers a prose
  "command" and a real one at both call sites.
- **Blocked on PH-1 by symbol, not by file.** `parse_sections` is added by
  PH-1 and does not exist on this base, so PH-3.1 cannot land until PH-1
  merges. The rev2 plan called these three stories independent; that holds for
  file sets and for PH-3.2 and PH-3.3, but not for PH-3.1. Named here because
  an unstated cross-story dependency is how a parallel worktree stalls without
  anyone knowing why.
- **Digest-binding the decomposition is a contract change, not a field add.**
  Every decomposition recorded before this story lacks the digest, so the
  refusal applies to newly recorded artifacts and the historical ones under
  `.factory/history/` must still parse — the same compatibility line
  `build_waves` sits on.

## Verify Plan

```
FACTORY_STRUCTURAL_CMD="python3 factory/scripts/check_dual_runtime.py" \
FACTORY_TYPECHECK_CMD="python3 factory/scripts/check_factory_scaffold.py" \
FACTORY_TEST_CMD="uv run --with pytest python -m pytest factory/tests -q" \
python3 factory/scripts/verify.py
```

The env vars are not optional: `verify.py` falls back to `pnpm check:all` when
they are unset and reports red against a Node stack this repo does not have.

Plus `python3 factory/scripts/check_agents_hygiene.py` — this story edits
prompts — and one branch-wide autoreview at the review phase.

Deterministic tests, all in `factory/tests/test_gates.py`:

- `plan save` refuses a plan missing each of the nine sections in turn, and
  names all of them when several are absent
- a section present with an empty body is missing
- every plan under `plans/` passes the check
- an agent-supplied `story` that contradicts `run.json` is overridden, not
  merged
- a decomposition whose `verify_commands` is prose is refused; a runnable one
  passes with `required_tests: []`
- a `dependencies` entry naming a later task is refused
- a `.factory/history/` artifact carrying `build_waves` still parses, and one
  recorded before digest-binding is still readable
- a decomposition whose plan digest does not match the active plan is refused
