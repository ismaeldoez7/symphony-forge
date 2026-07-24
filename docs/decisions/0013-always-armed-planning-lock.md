---
status: accepted
confirmed_by: "vrknetha"
date: 2026-07-24
supersedes: 0004-mandatory-plan-mode
---

# Always-armed planning lock with quickfix escape hatch

## Context

Decision 0004 armed the product-code lock only for an active, signed-off,
unplanned task and explicitly excluded Bash-level writes. In practice the
main skip path was exactly that gap: devs (and drifting agent sessions)
edited product code with no task active, or wrote files via shell
redirects, and small-to-medium fixes routinely bypassed plan mode.
Confirmed in chat (workflow-enforcement design, 2026-07-24): threat model
is agent drift, small fixes need a deliberate recorded exit, not a silent
judgment call.

## Decision

The planning lock is ALWAYS armed: product-code writes are denied unless
the active plan_status is approved OR an explicit quickfix window is open
(`forge quickfix start "<reason>"` — bounded file budget, durably ledgered
in plans/quickfixes.jsonl, closed with `forge quickfix done`). The
PreToolUse hook also heuristically denies Bash write commands (redirects,
tee, sed -i, cp, mv, touch) that target product paths while locked.

## Consequences

- The "no active task" and "shell write" bypasses of 0004 are closed;
  missing or reset run state now means locked, never unlocked.
- Skipping plan mode becomes a deliberate, recorded act with a scope cap;
  exceeding the quickfix budget forces plan mode.
- The Bash guard is a drift defense, not an adversarial sandbox: it is a
  heuristic and may need pattern tightening; artifact gates
  (verify/review/pr_ready) remain the backstop, as under 0004.
- Allowlisted planning surfaces (plans/, docs/, .factory/, factory/,
  prototype/, harness files) stay freely writable, keeping discovery and
  prototyping ceremony-free.
