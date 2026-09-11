# Dual-coordinator parity architecture

This document owns the shared technical boundaries used by the confirmed dual-coordinator capability. The approved story decomposition and each approved task plan still own delivery order, exact paths, tests, and implementation scope.

## Coordinator and writer boundary

Claude Code and native Codex are adapters to the same Forge phase engine. The active coordinator owns orchestration and the human conversation. Product writes flow through an admitted task worker whose process, task, worktree, stage, brief, and scope all match. The ledgered five-file degraded window remains the bounded outage path.

Both adapters register the same lifecycle owners for SessionStart, PreCompact, PreToolUse, PostToolUse, and Stop. Adapter-specific tool names are mapped to those owners by `check_dual_runtime.py`; the adapters do not implement separate phase or authority rules.

Each invocation writes an `adapter-event-result` through the existing event
family when repository identity is available. It binds the runtime, event row,
installed owner, outcome, host blocking capability, session, story, and task.
The shared task-proof reader consumes current results. If the hook cannot write
the result, it emits the same stable sanitized identity to the host error
channel and cannot supply successful hook proof. A host may fail open where its
API requires that behavior, including Stop owner failures, but the adapter may
not report a successful lifecycle observation.

## Review publication

The story-level `review-run.json` is an input and run token. It never selects proof.

Each task selects exactly one review generation through:

`.factory/stories/<story>/tasks/<task>/reviews/selected.json`

A task has one review lifecycle with immutable generations. Every initial or
post-fix default invocation creates one generation and calls the helper once.
A combined publication stores exact raw helper bytes and three schema-valid
lens candidates below `reviews/candidates/<publication-id>/`. The selected
pointer uses `origin=combined` and binds the candidate paths and hashes, review
run, brief, task input, branch diff, classified product, helper, story, and
task. All candidates validate and read back before a same-directory atomic
pointer replacement. Failure before replacement may leave unreferenced
candidates but cannot change the selected set. A blocking generation is still
selected and revokes clean status; only the selected clean generation
certifies task proof.

Every finding begins with one exact lens tag. Its untagged fingerprint uses the
specification's RFC 8785 and Unicode normalization contract, and one
fingerprint may have only one owning finding record. Other affected lens blocks
refer to it with the exact `AFFECTS <fingerprint> BLOCKING|NONBLOCKING` grammar.

Pre-seal readers resolve the current task pointer. Sealed readers resolve the task pointer at the marker's sealed commit. Every readiness, board, CI, seal, and rejection consumer calls the same resolver. Missing, fixed-only, unsafe, malformed, incomplete, mixed, copied, stale, or tampered proof refuses. Runtime readers do not inspect fixed review paths.

A single-lens run is diagnostic and cannot select proof or stamp a stage. Rejecting one finding republishes a complete selected set with the cited projection changed and the other bindings preserved.

## One-time upgrade migration

Before its first target write, `forge upgrade` globally enumerates and
preflights fixed three-lens review sets reachable from the active task or
committed task markers. An active unsealed set binds the current task plan,
grill, approval, stage incarnation, base, diff, run, and brief and has no marker
or seal. A sealed set additionally binds its committed marker, seal, and
inspected commit. Mixed state refuses. After the complete inventory passes,
upgrade writes no-clobber candidates and an `origin=upgrade` selected pointer
that hash-binds the original artifact bytes and available provenance without
inventing raw combined-helper output. It reads every complete result back
before replacing machinery and runs the new resolver over every migrated
pointer afterward.

Malformed, incomplete, ambiguous, colliding, symlinked, or otherwise unsafe input stops before target mutation. A byte-identical retry is idempotent. Old fixed files remain inert, and unbound archives remain display-only.

## Successor extensions

`NATIVE-LIFECYCLE` extends the shared launcher with detached lifecycle, recovery, correlated structured errors, metrics, and cancellation truth. `SHARED-COORDINATOR-JOURNEY` extends question identity, handoff, board, and owner recovery. `PORTABLE-DELIVERY-MIGRATION` implements the upgrade migration above. Each extension updates this architecture before its implementation when it changes an enduring boundary.

The shared handoff path refreshes trunk and holds one protected-state lock used
by every relevant state mutator. It captures one monotonic generation plus the
exact task, worker, stage, approval, selected-review, CI, and marker identities.
Transfer requires the marker on refreshed trunk, green CI for that commit, no
active worker, and every required question exchange closed. Unsafe paths,
generation drift, or inconsistent identities refuse before transfer.
