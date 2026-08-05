---
status: proposed
confirmed_by: ""
date: 2026-08-05
stories: [FORGE-UPG-1]
---

# Conflict Free Ledgers

## Context

The harness keeps append-only ledgers in git: lessons, quickfixes, events,
delegations, signals. Several worktrees append to the same file between merges,
which is a conflict at the file tail every time.

Everything built to manage that conflict is downstream of one choice — many
writers, one file:

- `.gitattributes` rules routing five path patterns through merge drivers
- a custom `jsonl-append` driver, registered per clone by the SessionStart hook
- `scaffold.ensure_jsonl_attributes`, writing those rules into every client repo
- part of why `forge roadmap heal` exists at all

None of it worked. The custom driver hung — forked, never ran its payload — so
a merge blocked forever rather than failing, which is indistinguishable from a
hostile conflict. Git's built-in `union` finishes but reorders: it produced a
ledger with `done` before `open` for three quickfixes, which four separate
review rounds then filed as a P1 state bug. The reviewer was reading the file
the way its format invites and the code does not.

So the machinery is not merely broken, it protects a property nothing relies
on. Every consumer reads these ledgers by set membership or by each record's
own timestamp. Line order carries no information.

## Decision

One record per file. A ledger is a directory — `plans/lessons/<id>.json`,
`.factory/events/<id>.json` — not a JSONL file that many writers append to.

Distinct files do not conflict, so there is nothing to merge, nothing to order,
and no driver to register.

## Consequences

- Delete the `.gitattributes` merge rules, `scaffold.ensure_jsonl_attributes`,
  and the SessionStart driver registration. A merge driver this repo depends on
  must be one git already ships; under this decision it depends on none.
- Record ids must be collision-resistant across worktrees. They already are —
  signals and quickfixes mint a hash suffix precisely because
  `roadmap parallel` puts several worktrees on one ledger.
- Readers take a directory glob instead of a line loop. Where a view wants
  order it sorts on the record's own timestamp: explicit, rather than implied
  by file position and silently rewritten by a merge.
- Existing `.jsonl` files stay readable for as long as any repo still has one,
  so history survives and no client repo is forced to migrate mid-story.
- More files. That is the cost, and it buys the deletion of every mechanism
  above plus a class of review finding that has now recurred four times.
