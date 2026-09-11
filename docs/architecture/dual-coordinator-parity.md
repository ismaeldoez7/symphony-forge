# Dual-coordinator parity architecture

This document owns the shared technical boundaries for dual-coordinator parity. The approved story decomposition and task plans own delivery order, exact paths, tests, and implementation scope.

## Coordinator and writer boundary

Claude Code and native Codex adapt the same Forge phase engine. One coordinator owns the current human conversation; product writes still require an admitted task worker whose process, task, worktree, stage, brief, and scope match. The ledgered five-file degraded window remains the outage path.

A coordinator changes only between completed tasks. The old session stops with no active worker or partial structured question; the new coordinator refreshes trunk and resumes with `forge next`. This story adds no live transfer command, fencing token, coordinator registry, or concurrent coordinator ownership.

After the Decision 0063 first-task exception, `task start` creates the worktree before task-plan save and grill. Its attach option accepts only a clean, registered, unowned worktree from the same Git common directory at the fetched trunk commit, with matching branch, story, task, decomposition, and dependency markers. Empty dependencies inherit the immediate predecessor; a nonempty list selects exactly those dependencies. `stage start --trunk` remains legacy behavior and cannot satisfy the new workspace-owned flow.

`./setup` and `forge doctor [--fix]` select the coordinator for one invocation: explicit argument, `FORGE_COORDINATOR`, one unambiguous detected host, then an interactive TTY question. Failure or ambiguity refuses before repair. Init, adopt, and upgrade install both adapters and never persist a selected coordinator.

## Adapter contract

The committed configurations are the normative current tool inventory:

| Runtime | Hook | Matcher or source |
|---|---|---|
| Claude | `SessionStart` | `startup|resume|clear|compact` |
| Claude | `PreCompact` | the host pre-compact event |
| Claude | `PreToolUse` | `Bash|AskUserQuestion` and `Edit|Write|MultiEdit|NotebookEdit` |
| Claude | `PostToolUse` | completed `AskUserQuestion` plus diagnostic write capture |
| Claude | `Stop` | the host stop event |
| Codex | `SessionStart` | `startup|resume|clear|compact` |
| Codex | `PreCompact` | the host pre-compact event |
| Codex | `PreToolUse` | `Bash|Edit|Write|apply_patch|request_user_input|request_user_input_async` |
| Codex | `PostToolUse` | completed synchronous `request_user_input` |
| Codex | `Stop` | the host stop event |

An asynchronous question call is guarded at issuance but is not completion evidence. A newly exposed tool must be added to the applicable matcher and tests before parity can be claimed. `check_dual_runtime.py`, focused hook tests, and the recorder-produced automated report are task proof. Timeline events remain best-effort diagnostics under Decision 0017.

Unexpected lifecycle exceptions reach one top-level boundary, return nonzero with a stable sanitized error ID, write one correlated structured error, and increment `forge_native_unexpected_errors_total` once with bounded labels. The error ID is the trace join key. Decision 0060's narrow POSIX signal-mask restoration stays in the existing launch path.

## Human-question identity

A successful structured-question hook writes one immutable event. The filename's fresh lowercase 32-hex stem is its event ID; a zero-based index identifies each question in the call. Eligibility binds runtime, session, event ID, question index, exact story/gate/task scope, current input digest, requiredness, question, ordered options, and nonblank answer. The recorder consumes an eligible question once. Historical rounds keep their old contract.

If an answer changes an approval-bound artifact, the owning decision or approval records the changed revision and the grill covers that final revision. No revision-mapping protocol or chat collector is added. Ordinary required questions remain in the host conversation; abandonment grants no authority and a later coordinator asks again.

## Review publication

The story-level `review-run.json` remains only an input/run token. Each task selects one immutable review generation through:

`.factory/stories/<story>/tasks/<task>/reviews/selected.json`

One default review calls the installed helper once and writes one generation below `reviews/generations/`. The generation contains the raw helper result and three schema-valid lens records. Forge validates and reads it back before atomically replacing the pointer. A blocking generation is selected and revokes clean status; only a selected clean generation certifies proof. `factory/schemas/review-set.json` distinguishes `origin=combined`, `origin=rejection`, and `origin=upgrade`.

Each actual provider pass has exactly three full-line blocks, in quality, performance, security order:

```text
BEGIN FORGE ASSESSMENT <lens>
<non-empty body>
END FORGE ASSESSMENT <lens>
```

Quality carries the existing machine-parsed contract verdicts. Forge preflights their minimum size against the helper's 3,000-character explanation limit. Unchunked output is one top-level pass; chunked reports are nonempty and labelled exactly `chunk 1/N` through `chunk N/N`. Every finding has one lowercase lens tag. Cross-lens duplicate detection uses repo-relative NFC POSIX path, integer start/end lines, and the NFC, whitespace-collapsed, case-folded title after removing the tag. Projections preserve pass order and reuse the existing score, recommendation, and worst quality-verdict functions.

One classifier in `factory_lib.py` supplies review scope plus current and historical binary branch-diff hashing. Genuine-contribution proof cites its qualifying path and hunk in that same diff and correlates it with admitted write and terminal evidence. There is no product-tree digest.

Pre-seal readers resolve the current pointer. Normal sealed readers resolve the pointer at the task marker commit. A citation-based rejection reads a selected combined generation and writes an immutable `origin=rejection` successor with source hash, exact finding, reason, citation, and actor; it preserves raw output and unaffected lenses. Fixed-only rejection refuses.

## One-time upgrade migration

Upgrade preflights every eligible fixed three-lens set before any target write. Active proof binds current task state. Sealed proof binds the original marker commit and exact fixed-artifact bytes. Only after the whole inventory passes may upgrade write and read back `origin=upgrade` generations and their pointers.

For already sealed legacy tasks, the current migration pointer is valid only when its generation's sealed-commit binding exactly equals the immutable marker. A replacement, mismatch, malformed set, mixed state, collision, linked path, or ambiguous owner refuses. Byte-identical retry is idempotent. Runtime readers never fall back to fixed paths.

The first event bundle for a shipped story is immutable. A later eligible event makes preview and apply refuse while leaving that event loose and unchanged. Retry may delete only loose events already represented by identical bundle members. V1 adds no successor shard.

## Successor ownership

`NATIVE-LIFECYCLE` owns detached read-only helpers, lifecycle recovery, cancellation, correlated errors, metrics, and signal behavior. `SHARED-COORDINATOR-JOURNEY` owns question identity, workspace-first task ownership, board state, and between-task coordinator changes. `PORTABLE-DELIVERY-MIGRATION` owns setup delivery, review migration, event retention, and client rollout support. Each successor updates this architecture before changing an enduring boundary.
