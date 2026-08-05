---
status: accepted
confirmed_by: "vrknetha"
date: 2026-08-05
stories: []
---

# Evidence Lifetime Split

## Context

`.factory/` holds two kinds of artifact under one policy, and both are
committed, archived and vendored into every client repo.

**Working state** exists to run a task and means nothing once it ships:
`run.json`, `stages.json`, the composed briefs, `delegations.jsonl`, resolved
signals. **The durable record** answers "why is this the way it is" long after:
decisions, lessons, outcomes, review findings, plans, verify results.

A read-only audit of `main` measured the cost of treating them alike:
`delegations.jsonl` plus shipped and diagnostic briefs occupy **222,819 bytes,
48.13% of `.factory/`**, with no reader after completion. `delegations.jsonl`
is the third-largest tracked file in the repo, nothing prunes it, and nothing
reads it once a stage closes. Several recorded fields — a test record's
`commands_run`, `remaining_gaps`, `manual_validation_steps`, `residual_risks`;
a review's `residual_risks` and `skills_used` — have no downstream consumer at
all.

This is not one repo's housekeeping problem. Symphony Forge is a template
clients vendor, so the per-story cost is paid in every project built on it,
forever. Four shipped stories currently average roughly 70KB of retained
process bytes each.

The evidence for which half earns its keep is unusually direct. Across a long
session of reconstructing earlier decisions, the artifacts actually read were
commit messages, decision records, the lessons ledger, outcomes, and a plan's
Problem and Risks sections. No completed brief, no `delegations.jsonl`, no
archived `stages.json` or `run.json` was opened once. The self-improvement loop
— lessons injected into briefs, decisions preventing re-litigation, recurring
findings escalating to refactors — runs almost entirely on the *smallest*
artifacts, while the bulk feeds nothing back.

Keeping everything also has costs beyond size, all observed rather than
theorised: oversized review bundles that refuse to review, secret-scanner false
positives on opaque ledger ids, duplicated records through the merge driver,
and rename/rename conflicts that corrupted two shipped stories' archived JSON.

## Decision

`.factory/` is split by LIFETIME, not by phase.

**Ephemeral working state is not committed.** `run.json`, `stages.json`,
`.factory/briefs/`, `.factory/diagnostic-briefs/`, `delegations.jsonl` and
resolved signals live only in the worktree and are gitignored. They die with
the task that created them.

**The durable record stays committed and stays small**: decisions, lessons,
plans, the decomposition, `verify.json`, the three review artifacts, and the
outcome. A recorded field must have a reader — a consumer in code, or a named
human question it answers — or it is not recorded.

## Consequences

- A client repo carries roughly 10–15KB per shipped story instead of ~70KB,
  and a handful of files a person will actually read instead of dozens they
  will scroll past.
- Auditability is preserved where it ever existed. `verify.json`, the review
  findings and the outcome are the proof a story shipped correctly; a brief is
  an instruction to a worker that has since finished, and `delegations.jsonl`
  is a lock ledger. Nothing that evidenced a gate is dropped.
- **Completeness and readability are in tension and this chooses readability.**
  A record that is half unread is not more auditable — the signal is diluted,
  and the reader six weeks later has to wade. Making the durable record smaller
  makes it more useful for self-evolution, not less.
- Ephemeral state must survive a worktree, not a merge. Anything a parallel
  story needs to see stays durable; anything one worktree needs alone stops
  being everyone's problem, which also removes it from the review bundle, the
  secret-scanner surface and the merge surface.
- `pr_ready` stops archiving what it cleans. Its archive keeps the durable
  record and drops working state rather than copying it into
  `.factory/history/<issue>/`.
- Recording commands must refuse a field with no consumer, or this decays back
  the moment a field is easy to capture. New fields arrive with their reader.
- Decision 0022 (one ledger record per file) still applies to durable ledgers.
  Ephemeral ledgers do not merge at all once they are uncommitted, which
  removes the problem rather than managing it.
