---
slug: delegation-boundary
title: Delegation boundary: briefed, bounded, measured
status: confirmed
saved: 2026-07-27T12:06:47+00:00
---

# Delegation boundary: briefed, bounded, measured

## Capability

The Claude→Codex handoff becomes an instrumented boundary. Three facts that
are today decided by judgement — *may this run write?*, *did it finish?*,
*what does it know?* — become artifacts a script can check and refuse on.

## Why

Four reported failures, each traced to a mechanical cause:

1. **The harness gets skipped and nobody can say why.** The delegation step
   has no command, so there is no deterministic record of what should have
   happened.
2. **Codex is launched read-only and stalls silently.** Three layers disagree
   about the default (the companion, this repo's hook, and the plugin's own
   subagent), and a `read-only` sandbox with `approvalPolicy: never` cannot
   write *and* cannot ask — so it narrates a plan and exits 0.
3. **Partial work reports clean.** Success is "the model stopped talking".
   Nothing compares what changed against what the task declared.
4. **Codex ignores existing components and design rules.** No script composes
   context for it, and the design skills the harness demands it attest are not
   installed for that runtime.

## Behaviour

**A delegation is a briefed, recorded act.** `forge delegate <task-id>`
composes a brief from artifacts that already exist — the task's objective,
acceptance criteria, `write_scope`, `required_tests`, `reviewer_focus`, the
implementer prompt, the active decisions, the lessons matching the task's
paths, and the modules already present in that scope — writes it to
`.factory/briefs/<task-id>.md`, prints the exact invocation, and records the
delegation with the brief's digest.

**Write permission is derived, not typed.** An active stage with a non-empty
`write_scope` is a write run. `--read-only` is the explicit exception.

**A brief is not skippable.** A `--write` companion call with no matching
recorded brief is denied by the pre-tool hook, and editing the brief on disk
invalidates the record.

**Completion is a measurement.** `forge stage done` refuses unless the diff
since the stage's base commit is non-empty, every changed product path is
covered by the task's `write_scope`, every `required_tests` entry resolves to
a file, and every `verify_commands` entry runs green. `verify_commands` must
therefore be runnable — prose is refused at record time.

**Partial delivery is sayable.** `forge stage done --incomplete "<what is
missing>"` leaves the stage open and records the gap, so a worker that
finished 60% has vocabulary other than silence.

**A stalled run is visible without being asked for.** `forge codex status`
reads the plugin's job registry and reports each job's status, phase, write
flag and age, flagging a long-running job with no phase change and a
`write: false` job launched while a stage was active.

**A skill the harness demands must be loadable where it is attested.**
`forge doctor` checks the required and advised skills against every runtime
expected to attest them, and `--fix` installs what is missing.

## Acceptance criteria

- A stage cannot be closed on an empty diff, an out-of-scope change, a
  missing declared test, or a failing per-task verify command.
- `--parallel` is checked: two stages claiming parallelism must have disjoint
  `write_scope`.
- A decomposition recording prose where a command belongs is refused.
- A `--write` delegation without a fresh recorded brief is denied by the hook,
  and the refusal names the command that fixes it.
- The generated brief carries the acceptance criteria, the write scope with
  its existing modules, and — for user-facing work — the design rules inline.
- `forge codex status` reports the write flag per job and flags a stalled one.
- `forge doctor` reports a required skill that a runtime cannot load.
- `forge next` names the delegation step.

## Boundaries

`forge codex status` reads a third-party path; it is a diagnostic and must
never be able to block a ship. The board stays read-only — delegation state is
CLI-surfaced this round. Existing shipped history keeps its prose
`verify_commands`; only new decompositions are refused.
