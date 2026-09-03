---
id: 0050
title: Plan authoring is mode-agnostic; the grill is the provenance
status: accepted
date: 2026-09-03
supersedes: 0048 (plan-mode marker requirement only)
---

## Context

Decision 0048 required a **plan-mode marker** before a plan or task plan could
be saved or approved: the `post_tool_use` hook records a marker whenever a
Claude session writes a plan file while in plan mode, and
`require_plan_mode_marker` refused the save/approve unless a marker's
`sha256_body` matched the plan body exactly.

The intent was provenance — evidence that a plan was authored deliberately
rather than generated in passing. In practice the marker does not deliver that,
and it costs something real:

- **It forces an IDE mode change the operator did not ask for.** An operator
  running in auto mode is pushed into plan mode purely to satisfy the marker,
  then pushed back. The harness is dictating editor state to get a file
  written, which is not its business.
- **It is trivially satisfiable and therefore proves nothing.** Entering plan
  mode and touching the file produces a marker. The marker attests to a mode,
  not to thought.
- **It is redundant.** The real provenance already exists and is far stronger:
  the task grill is bound to the plan's exact digest, requires a floor of
  recorded `AskUserQuestion` rounds that only the hook can write, and must be
  **fresh** — recorded against the current plan text — before the board will
  show the plan or a human can approve it. A plan that survives that has
  demonstrably been examined; a plan-mode marker has demonstrated only that a
  mode was entered.
- **Its digest is fragile across platforms.** `plan_body_digest` exists solely
  to normalise line endings so a marker written on Windows still matches a plan
  checked out under `core.autocrlf` — complexity that only the marker needs.

## Decision

**Plan authoring is mode-agnostic.** The plan-mode marker is no longer required
to save or approve a plan or a task plan. `require_plan_mode_marker` is
removed, along with its four call sites in `plans.py` and `tasks.py`.

**The grill is the provenance, and it is now enforced where it was only
implied.** `task approve` previously carried a comment claiming a fresh passing
grill was required; no code checked it. Approval now refuses unless the task
grill's verdict is `pass` **and** it was recorded against the current plan
digest — the same predicate the board uses to decide whether to show a task
plan at all. Approving a plan the board would refuse to display was the gap
that let a stale or failing grill through.

The `post_tool_use` hook keeps recording plan-mode markers. They remain useful
provenance in the event log, and the hook is the only thing that can write
them; nothing gates on them.

## Consequences

- An operator in auto mode stays in auto mode. No forced mode switch.
- Approval is gated on the thing that actually carries meaning, and the board
  and the approval gate can no longer disagree about whether a plan is ready.
- `plan_body_digest` and the plan-mode marker schema stay (the hook still
  writes them), but nothing depends on their cross-platform stability for a
  gate to open.
- 0048's other provisions — grill-round provenance and the ledger-matched
  round floors — are untouched and remain in force.
