# Dual-coordinator parity architecture

This document owns the shared technical boundaries used by the confirmed dual-coordinator capability. The approved story decomposition and each approved task plan still own delivery order, exact paths, tests, and implementation scope.

## Coordinator and writer boundary

Claude Code and native Codex are adapters to the same Forge phase engine. The active coordinator owns orchestration and the human conversation. Product writes flow through an admitted task worker whose process, task, worktree, stage, brief, and scope all match. The ledgered five-file degraded window remains the bounded outage path.

Both adapters register the same lifecycle owners for SessionStart, PreCompact, PreToolUse, PostToolUse, and Stop. Adapter-specific tool names are mapped to those owners by `check_dual_runtime.py`; the adapters do not implement separate phase or authority rules.

## Review publication

The story-level `review-run.json` is an input and run token. It never selects proof.

Each task selects exactly one review generation through:

`.factory/stories/<story>/tasks/<task>/reviews/selected.json`

A combined publication stores exact raw helper bytes and three schema-valid lens candidates below `reviews/candidates/<publication-id>/`. The selected pointer uses `origin=combined` and binds the candidate paths and hashes, review run, brief, task input, branch diff, classified product, helper, story, and task. All candidates validate and read back before a same-directory atomic pointer replacement. Failure before replacement may leave unreferenced candidates but cannot change the selected set.

Pre-seal readers resolve the current task pointer. Sealed readers resolve the task pointer at the marker's sealed commit. Every readiness, board, CI, seal, and rejection consumer calls the same resolver. Missing, fixed-only, unsafe, malformed, incomplete, mixed, copied, stale, or tampered proof refuses. Runtime readers do not inspect fixed review paths.

A single-lens run is diagnostic and cannot select proof or stamp a stage. Rejecting one finding republishes a complete selected set with the cited projection changed and the other bindings preserved.

## One-time upgrade migration

Before replacing client harness machinery, `forge upgrade` enumerates fixed three-lens review sets reachable from the active task or committed task markers. A set is eligible only when all three artifacts have coherent task, run, brief, diff, base, marker, and seal provenance. Upgrade writes no-clobber candidates and an `origin=upgrade` selected pointer that hash-binds the original artifact bytes and provenance without inventing raw combined-helper output. It reads the complete result back before replacement and runs the new resolver over every migrated pointer afterward.

Malformed, incomplete, ambiguous, colliding, symlinked, or otherwise unsafe input stops before target mutation. A byte-identical retry is idempotent. Old fixed files remain inert, and unbound archives remain display-only.

## Successor extensions

`NATIVE-LIFECYCLE` extends the shared launcher with detached lifecycle, recovery, correlated structured errors, metrics, and cancellation truth. `SHARED-COORDINATOR-JOURNEY` extends question identity, handoff, board, and owner recovery. `PORTABLE-DELIVERY-MIGRATION` implements the upgrade migration above. Each extension updates this architecture before its implementation when it changes an enduring boundary.
