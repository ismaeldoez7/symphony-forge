---
status: proposed
confirmed_by: ""
date: 2026-07-27
stories: []
---

# The repo is the system of record: outcomes, timeline, and decision provenance

## Context

A developer returning to a story six weeks later could not answer, from the
repo alone: what was built, which decisions govern it, when it moved, and who
moved it.

The harness captured plenty of prose — story narratives, acceptance criteria,
task objectives, review summaries, signal resolutions — but every field was
authored *before* the work. Nothing recorded the outcome. The story timeline
was a single mutable `updated_at` that each phase overwrote, so transitions
left no trace. Decision records carried no link to the story that produced
them, so "which decisions came out of this feature" was answerable only by
reading prose. `pr_ready` deleted the plan grill at ship without archiving it,
destroying the record of what contradictions were surfaced and how they were
answered. And re-recording a decomposition after a mid-story scope change
rebuilt the stage tracker from scratch, erasing completed timestamps.

Two lifecycle reviews (an Opus pass and a Codex `gpt-5.6-sol` pass, each
walking a PM and an engineer from discovery through production support) also
found that `decision new --supersedes` retired the predecessor immediately,
leaving a window in which neither version governed, and that the planning lock
freed product writes on plan approval alone — before any task bounded them.

## Decision

The repo is the system of record, completed in the ledgers that already exist
rather than in a new store:

- **Outcome at ship.** `forge outcome set` records one paragraph — what
  changed and what someone can now do — schema-validated and length-bounded
  (≥12 words, ≤800 chars). `pr_ready` lists it as missing until it exists, so
  a bare run stays a readiness check. It lands on the roadmap item and in the
  ship archive.
- **A story timeline.** `.factory/events.jsonl` appends one line per
  transition, written by the scripts that change state, with an
  allowlist-pinned `generated_by`. Discovery is instrumented too (spec save,
  spec confirm, roadmap derive/import/add). Story lines archive with their
  story; project lines stay. `.gitattributes` marks it `merge=union` — git's
  built-in driver, so parallel worktrees can never conflict on it.
- **Decision provenance.** Records carry `stories: [...]`; `decision new`
  seeds it and `decision link` appends, because one decision often governs
  several stories. Supersession is atomic at `decision accept`.
- **Nothing is destroyed at ship.** The plan grill, the story's timeline, and
  its assumption rows are archived alongside the existing evidence.
- **Task narrative is contract.** The recorder refuses a task without an
  `objective` (≤500 chars) and non-empty `acceptance_criteria`.
- **Ad-hoc capture without a bypass.** `roadmap add` gains `--story`, `--ac`
  and `--depends-on`, plus `--no-spec --reason` to capture a mid-project ask
  as visible debt; `plan save` refuses to build such a story until its spec is
  confirmed and linked, so decision 0014 still governs what gets built.
- **Implementation is bounded.** The planning lock now requires an approved
  plan *and* a recorded decomposition before product writes.

Every rule above is a coded gate — a script refusal, a hook denial, or a
`check_dual_runtime` violation. Prompts explain the rules; they never enforce
them.

## Consequences

- Shipping costs one more deliberate act: writing the outcome. That is the
  point — it is the only moment the author still has the context.
- `pr_ready` warns, and does not block, when a story's linked decisions are
  still `proposed`. Blocking would freeze existing projects, where most
  records were never formally accepted; the warning plus the board's
  "proposed — unconfirmed" label is the repair pressure.
- Existing decision records needed a one-line `stories: []` migration.
- Deployment is still outside the harness: "shipped" here means PR-ready, and
  the board labels those dates accordingly rather than implying a release.
- Events are best-effort: a failed ledger write never fails the gate that was
  doing real work.
