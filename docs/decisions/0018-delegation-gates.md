---
status: proposed
confirmed_by: ""
date: 2026-07-27
stories: [FORGE-DELEG-1]
---

# Delegation Gates

## Context

The Claude to Codex handoff was governed by prose. Four reported failures each
traced to something a script could have checked and did not:

- Write permission was decided per request by a subagent, and three layers
  disagreed on the default (the companion defaulted read-only, this repo's hook
  said read-only unless `--write`, the plugin's own subagent said default to
  `--write`). A `read-only` sandbox with `approvalPolicy: never` cannot write
  *and* cannot ask, so a run narrated a plan and exited 0.
- Completion meant "the model stopped talking": `forge stage done` checked only
  that the stage had been started, so a run that did three of eight acceptance
  criteria closed clean and `pr_ready` printed PR_READY.
- Nothing composed context for the executing runtime. `factory/prompts/
  implementer.md` was referenced by five docs and read by zero scripts.
- The design skills `harness.yaml` demands for user-facing work were not
  installed for the runtime asked to attest them, so those attestations were
  false.

The task contract already carried `write_scope`, `verify_commands` and
`required_tests`. All three were consumed only by the renderer.

## Decision

The delegation boundary is instrumented rather than described. Six gates:

1. `stage start` records the stage's base commit and the dirt already in the
   tree; `stage done` measures against them and refuses on an empty product
   diff, an out-of-scope path, an unresolvable `required_tests` entry, or a
   failing `verify_commands` entry.
2. `stage done --incomplete "<what is missing>"` gives partial delivery a
   vocabulary: the stage stays open and the gap enters the timeline.
3. `forge delegate` composes the brief and the invocation, derives write
   permission from stage state, and records the delegation with the brief's
   digest.
4. The pre-tool hook denies a `--write` companion call with no fresh recorded
   brief.
5. `verify_commands` must be runnable; prose is refused at record time.
6. `forge doctor` checks that every skill the harness demands is loadable by
   each runtime expected to attest it.

`forge codex status` is deliberately advisory: it reads a third-party plugin
path, and a diagnostic over data this repo does not own must never be able to
block a ship.

## Consequences

A stage can now fail to close. That is the point — the previous behaviour was
that it could not. Two costs are accepted:

- Emptiness is judged on product paths only (`.factory/` and `plans/` are
  exempt), because the workflow writes those itself on every command. This
  exemption is deliberately narrower than `pr_ready`'s `EVIDENCE_PATHS`, which
  exempts all of `factory/` and `docs/` — in the harness's own repo that is the
  product, and reusing it would make the scope check vacuous exactly where it
  is dogfooded.
- A path already dirty when the stage started is not attributed to the stage,
  compared by CONTENT rather than name — otherwise a worker could keep editing
  an out-of-scope dirty file invisibly, and work confined to an in-scope dirty
  file would read as an empty diff.
- The decomposition may still be re-recorded mid-stage (the sanctioned repair
  for a scope that turns out to be wrong), but closing over a contract rewritten
  after the stage started is refused: `stage start` again to re-baseline, on the
  record. Re-baselining discards credit for work already in the tree, so it is
  the first move after a scope correction, not the last.
- Parallel stages share a worktree and a HEAD, so a sibling's commit falls
  inside this stage's window. Disjointness is verified at `stage start`, so a
  path in a sibling's `write_scope` is that sibling's to answer for. Without
  this, the parallel workflow the harness advertises could never complete.

Existing shipped history is untouched: the `verify_commands` refusal applies at
record time only, and `forge doctor` reports an active decomposition still
carrying prose so it is fixed before the next stage closes.
