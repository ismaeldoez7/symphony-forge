---
status: proposed
confirmed_by: ""
date: 2026-08-05
stories: []
supersedes: 0024-evidence-lifetime-split
---

# Evidence Lifetime Contract

## Context

0024 established the right idea and got four things wrong. An adversarial
read-only validation found them before implementation, which is the cheap place
to find them.

The idea that survives: `.factory/` holds two kinds of artifact under one
policy. **Working state** exists to run a task and means nothing once it ships.
**The durable record** answers "why is this the way it is" long after. Both are
committed, archived and vendored into every client repo, and a measured
**222,819 bytes — 48.13% of `.factory/`** has no reader after completion, at
roughly 70KB per shipped story paid in every downstream project forever.

What 0024 got wrong:

1. **`tests.json` was missing from the durable set.** It is a hard-gate
   artifact; omitting it would have deleted the proof that a story's tests ran.
2. **Open signals carry authority.** 0024 called signals ephemeral. An ignored
   `signals.jsonl` silently erases a blocking contradiction: a worker raises
   "this contract is impossible", pauses, and the signal evaporates because
   nothing tracks it — so `pr_ready` passes a story no human ever unblocked.
   Ranked medium likelihood, catastrophic damage.
3. **The plan grill is durable.** It is digest-bound evidence that a gate was
   passed, not scaffolding.
4. **Migration and worktree-loss were unstated.** Existing clients already
   track these files, and a `.gitignore` rule does nothing to a tracked file —
   git keeps tracking it silently. Separately, once state is uncommitted,
   deleting an in-flight worktree becomes unrecoverable.

The validation also found that the board renders completed stories from
archived `stages.json`, so dropping it naively empties shipped history in the
UI; and that a clean checkout is currently misclassified, so CI cannot yet tell
"fresh clone, no task" from "task state missing".

Its strategic correction is the important one: **reduce by writing less, not by
relocating more.** 0024 leaned toward moving artifacts; the cheaper and more
honest reduction is to stop producing what nothing reads.

## Decision

`.factory/` is governed by lifetime, and the reduction comes from writing less.

**Durable — committed, and each item has a named consumer:** decisions,
lessons, plans, `decomposition.json`, `verify.json`, `tests.json`, the three
`reviews/*.json`, `outcome.json`, and the plan grill.

**Live authority — uncommitted, but FAIL CLOSED:** `run.json`, `stages.json`,
`.factory/briefs/`, `.factory/diagnostic-briefs/`, `delegations.jsonl`, and
**resolved** signals. An **open** signal is authority, not working state:
`pr_ready` must refuse when it cannot positively establish that no signal is
open, rather than passing because the file is absent.

**Stop writing what nothing reads,** rather than relocating it: the delegation
ledger, shipped and diagnostic briefs, archived `run.json`/`stages.json`/
resolved signals, the duplicated `outcome.json`, write-only event rows, and
recorded fields with no consumer. A field arrives with its reader or it does
not arrive.

## Consequences

- A client repo carries roughly 10–15KB per shipped story instead of ~70KB, and
  a handful of files a person will read rather than dozens they will scroll past.
- **Absence never means permission.** This is the same rule three separate
  fail-opens broke in `stages.py` this session: a gate that cannot verify must
  refuse. Uncommitting live authority makes that rule load-bearing, so every
  gate reading it needs an explicit "cannot determine" branch.
- **Completeness and readability are in tension and this chooses readability.**
  A half-unread record is harder to audit, not easier — the signal is diluted.
- The board must stop rendering completed stories from archived `stages.json`.
  Either it derives shipped state from the roadmap and `outcome.json`, or a
  minimal shipped summary joins the durable set. Emptying shipped history in the
  UI is not an acceptable side effect.
- **Migration is explicit and part of `forge upgrade`:** `git rm --cached` the
  now-ignored paths so they stop being tracked, refuse to migrate a repo with an
  active task rather than destroying its in-flight state, and report what it
  untracked. A gitignored-but-tracked file is the failure mode to prevent.
- **Worktree loss is stated, not discovered:** with live authority uncommitted,
  removing a worktree mid-story discards it. `forge` refuses to remove a
  worktree with an active task, and the recovery path is re-running intake and
  re-recording the decomposition from the durable plan.
- CI must distinguish a clean clone with no active task from a repo whose task
  state went missing, and prove both, plus linked-worktree authority, in the
  gate tests.
- Decision 0022 still applies to durable ledgers. Ephemeral ones stop merging
  at all once uncommitted, which removes the problem rather than managing it.
- Implementation is five bounded tasks: revise the contract surface; make live
  authority ephemeral and fail-closed; shrink the durable record and remove the
  board's stage-history dependence; implement the client transition; prove it
  with clean-clone and linked-worktree tests.
