---
issue: FORGE-ALIGN-1
title: Self-updating context ledger
status: approved
saved: 2026-08-10T08:39:33+00:00
story: FORGE-ALIGN-1
decisions_reviewed:
  - 0001-determinism-contract
  - 0002-concurrency-one-task-per-branch
  - 0003-model-tiers-terra-explore-sol-implement
  - 0005-recurring-findings-escalation
  - 0006-lessons-ledger
  - 0007-stage-commit-loop
  - 0008-loop-health-audit
  - 0009-frozen-gate-integrity
  - 0010-client-signoff
  - 0011-orchestrator-runs-autoreview
  - 0012-project-level-memory
  - 0013-always-armed-planning-lock
  - 0014-specs-before-signoff
  - 0015-plan-contradiction-gate
  - 0016-machinery-dir-rename
  - 0017-repo-as-system-of-record
  - 0018-delegation-gates
  - 0021-derived-ordering
  - 0022-conflict-free-ledgers
  - 0023-stage-delta-by-ref
  - 0025-evidence-lifetime-contract
  - 0026-bundled-example-validated-by-production-validators
  - 0027-responsive-proof-without-a-browser
  - 0028-path-boundary-invariant
  - 0029-plan-approval-in-plan-mode
  - 0030-harness-source-is-product-in-its-own-repo
  - 0031-workflow-modes-lite
  - 0032-jit-task-planning
  - 0033-gate-a-declares-all-work-records
  - 0034-vendored-docs-are-client-safe
---

# Plan — FORGE-ALIGN-1: Self-updating context ledger

> Story FORGE-ALIGN-1, epic `strict-alignment` (story 1 of 3), spec
> `docs/specs/strict-alignment.md`. Branch
> `feat/FORGE-ALIGN-1-self-updating-context-ledger` in the main checkout.

## Problem

`docs/context/ledger.json` is the harness's only self-fresh ledger: every inbox
file is sha256-fingerprinted and `context scan --check` hard-fails client CI on
drift. But `forge context scan` is manual and the harness registers no post-edit
hook (only SessionStart / PreCompact / PreToolUse / Stop exist), so the
deterministic outcome of an agent editing a context doc is a red PR, not an
updated ledger — minegate PR #69 failed this check three times in one morning.

**Spec correction found during planning:** the spec says "the existing `git
commit` interception gains the same auto-scan" — no such interception exists.
`pre_tool_use.py` has no `git commit` handling anywhere (only `git rm`/`git mv`
via `git_subcommand()` and a shape denylist). The commit belt is NEW code; the
spec line gets a one-word factual fix ("The existing" → "A new").

## Scope / Non-goals

**In scope:** a new `git commit` belt in the EXISTING `pre_tool_use.py` hook —
re-scan the inbox in-process and stage the refreshed ledger before a commit
proceeds — plus a print-free `scan_inbox()` factoring in `context.py`; tests;
a ledgered deferral for the write-time hook.

**Non-goals — the simplicity cut (grilled):** NO new `PostToolUse` hook, hook
script, or hook-config change. The write-time scan adds no gate value —
`pending_context` counts unscanned files as pending anyway, so scanning at
write time changes no gate outcome; freshness is only ever checked at
commit/CI, which is exactly where the belt sits. The belt rides a hook that
already exists and is already registered for Bash in BOTH runtimes, so Codex
workers are covered for free and `check_dual_runtime` is untouched. The one
missed path (agent writes the doc, human commits from a bare terminal) keeps
the unchanged CI check with its exact fix-it message, and gets a deferral with
a trigger — not speculative code. Also: NO change to `context scan --check`
(byte-identical backstop); NO other ledger gains auto-update (FORGE-ALIGN-2/3);
NO change to what `scan` refuses; NO scaffold/vendor changes (`pre_tool_use.py`
ships inside the already-vendored `factory/scripts` tree).

## Acceptance Criteria

(From the roadmap story, made concrete. The story's AC1 and the spec's
"post-edit hook seam" sentence are amended to be mechanism-neutral — the
promised OUTCOME "the ledger diff rides the same commit with no manual
command" is delivered by the belt; the write-time hook is a recorded deferral,
not a silent drop.)

1. A `git commit` issued through an agent session (either runtime) while the
   inbox has drift re-scans in-process and stages `docs/context/ledger.json`,
   so the ledger diff rides the same commit with no manual command.
2. A commit attempted while a context file is REFUSED (secret-shaped /
   oversized) is DENIED with the refusal reason.
3. `context scan --check` (CI) is unchanged and green immediately after a
   belt-scanned commit; a clean inbox is a pure pass-through.
4. `check_dual_runtime.py` and the full gate suite stay green with zero
   hook-registration changes.

## Technical Approach

### `scan_inbox()` factoring — `factory/scripts/forge_cli/context.py`

Extract the loop body of `cmd_scan` into `scan_inbox(base) -> (drift, refused)`
that mutates and saves the ledger but prints nothing and never exits.
`cmd_scan` wraps it (output byte-identical). The belt calls it in-process —
`forge_cli` is already importable from hook scripts (`pre_tool_use.py` imports
`forge_cli.quickfix` today), no subprocess, no stdout pollution of the hook
JSON protocol.

### Commit belt — `factory/scripts/pre_tool_use.py`

New block placed after `root = repo_root()` (line ~524, beside the sign-off
gate), NOT in the early regex denylist (which runs before `root` exists). On
Bash commands whose `git_subcommand()` is `commit`:

- `scan_inbox(root)`; if `refused` → `deny()` with the refusal lines (the
  commit must not land unredacted secret-shaped context — same stance the plan
  gate already takes).
- If `drift` was found → `subprocess.run(["git", "add",
  "docs/context/ledger.json"], cwd=root)` so the refreshed ledger rides this
  commit, then fall through to allow. No drift → pure pass-through.
- Known hole, accepted: `git commit <pathspec>` bypasses the index, so the
  staged ledger doesn't ride — CI's unchanged `--check` catches it. Noted in
  the decision record.
- No registration changes anywhere: `pre_tool_use.py` is already wired for
  Bash in `.claude/settings.json` AND `.codex/hooks.json`, and ships inside
  the vendored `factory/scripts` tree — clients get the belt on
  `forge upgrade` with zero list changes.

### Deferral (ledgered, not silent)

`forge defer add`: the write-time PostToolUse hook — trigger: "stale-ledger CI
failures recur from out-of-session commits of agent-written context files, or
a second consumer of write-time ledger freshness appears."

### Doc touches

- `docs/specs/strict-alignment.md`: two factual amendments — "the existing
  git commit interception" → "a new git commit interception" (no such
  interception existed), and the "post-edit hook seam" sentence reframed to
  the commit-time belt with the hook as the recorded deferral.
- `plans/roadmap.json` FORGE-ALIGN-1 AC1: same mechanism-neutral rewording
  (authoring correction before implementation, noted in the plan grill).
- `docs/context/README.md`: one sentence — agent-session commits re-scan
  automatically; `scan` remains for out-of-session edits.

## Decisions

One new decision record (created right after plan approval, before
decomposition): **`commit-belt-keeps-ledger-fresh`** — the commit belt is the
single enforcement point for context-ledger freshness in sessions: it
auto-stages the refreshed `ledger.json` (grilled: machine-owned, belongs with
the change) and DENIES a commit while a context file is refused (grilled:
strict, same stance as the plan gate). Accepted holes, CI as backstop:
`git commit <pathspec>` bypasses the index; out-of-session commits see no
hooks. The write-time PostToolUse hook was REJECTED as speculative — write-time
scanning changes no gate outcome (`pending_context` counts unscanned files as
pending already) — and lives in the deferral ledger with a trigger.

No contradiction with the 30 active decisions; 0013's planning lock is
untouched (docs/ writes were already exempt via `PLANNING_WRITE_OK`).

## Surface Impact

| Surface | Class | Notes |
|---|---|---|
| Runtime behavior | Changed | commit belt in the existing pre_tool_use hook |
| API | N-A | — |
| Data/schema | Unchanged by design | ledger.json format and scan semantics untouched |
| CLI/ops | Unchanged by design | `cmd_scan` output byte-identical after factoring |
| UI | N-A | — |
| Docs | Changed | spec two-line amendment; roadmap AC1 wording; context README sentence |
| Tests | Changed | belt coverage in test_gates.py |

## Task Decomposition

One bounded task (disjoint scope, one worker):

1. **FORGE-ALIGN-1.1 — commit belt + tests** — `scan_inbox()` factoring in
   `context.py`; the belt block in `pre_tool_use.py`; deferral entry; doc
   touches; tests.

## Risks

- **Stdout pollution breaks the hook JSON protocol** — mitigated by the
  `scan_inbox()` factoring (prints nothing); a test asserts hook stdout stays
  exactly the decision JSON.
- **Belt latency on every `git commit`** — sha256 over the inbox (~67 files at
  minegate) once per commit; trivial. Clean-inbox path short-circuits.
- **Auto-staging surprises a dev doing partial staging** — staging only
  `ledger.json`, which is machine-owned and belongs with the change by
  definition; documented in the decision record.
- **Index mutation from a deny-or-pass hook** — the belt stages exactly one
  known machine-owned path and only after a successful scan (lesson
  `verify-merge-resolution-before-staging`: verification is separated from,
  and precedes, the stage+commit).

## Verify Plan

- **Gate tests** (`test_gates.py`, patterns: `hook()` helper at :3733, repo
  fixture at :206): drifted inbox + `git commit` payload → ledger re-scanned,
  staged (`git diff --cached` names it), commit allowed, stdout is pure hook
  JSON; refused (secret-shaped) file + `git commit` → deny with the refusal
  reason; clean inbox → pass-through with no index change; non-commit git
  commands → belt not entered; `test_plan_save_blocked_by_unscanned_drop`
  still passes (the state stays reachable out-of-session).
- **Determinism:** `check_dual_runtime.py`, `verify.py`, full pytest suite —
  all with ZERO hook-registration deltas.
- **Live smoke:** in this repo, drop a scratch file under `docs/context/`,
  `git commit` through the session → ledger rides the commit and
  `forge context scan --check` is green; then remove the scratch file and
  re-scan to clean up.
