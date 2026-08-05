# Brief — FORGE-UPG-1.2: stage migrate records an explicit base commit

Story: FORGE-UPG-1 | write access: YES — you may edit files in the write scope

This brief is the whole context you are given. It was composed from the recorded decomposition, the implementer contract, the active decisions and the lessons ledger. Do not go looking for the rules elsewhere; if something needed is missing, raise a signal instead of guessing (`./forge signal raise`).

## Objective

forge stage migrate takes --base <sha>, validates that it resolves and is an ancestor of HEAD, and stamps it as base_sha on every legacy stage it adopts, so a story that was open when its repo was upgraded can still be measured and closed.

## Acceptance criteria

- stage migrate without --base refuses and names the flag
- process identity is whitespace-normalized at every source, so observed processes are still recognized as live on single-digit days of the month
- a discovery failure degrades discovery only; already-known processes still run the full SIGTERM to SIGKILL escalation
- a base that does not resolve to a commit is refused
- a base that is not an ancestor of HEAD is refused
- the resolved sha lands as base_sha on every adopted active or done stage, alongside the task_sha256 the command already stamps

## Write scope — nothing outside this

- factory/scripts/forge.py
- factory/scripts/forge_cli/stages.py
- factory/scripts/forge_cli/delegate.py
- factory/tests/test_gates.py

`forge stage done` refuses a change outside this list.

## What already exists in that scope (use it, do not re-create it)

- factory/scripts/forge.py
- factory/scripts/forge_cli/stages.py
- factory/scripts/forge_cli/delegate.py
- factory/tests/test_gates.py

## Tests you must write

- test_stage_migrate_requires_a_base: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_stage_migrate_refuses_a_base_that_is_not_an_ancestor: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_stage_migrate_records_the_base_on_adopted_stages: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_process_identity_matches_the_process_table_on_single_digit_days: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)

The implementer writes and records the tests; a declared test that does not exist or whose exact command fails refuses the stage.

## Verify commands (they will be run when the stage closes)

- `uvx --with pytest python3 -m pytest factory/tests/test_gates.py -q -k "migrate or stage_done or reaps or termination_signal or process_identity"`
- `python3 factory/scripts/check_dual_runtime.py`

## Reviewer focus

--base is required with no default; conduct 5 forbids a compatibility shim for a once-per-repo command whose only consumer is its own test. dirty_at_start stays unset on purpose - _measure defaults it to {} and a commit base makes that the honest baseline. The delegate.py identity normalization is the inherited defect that blocked this stage's own verify: check both identity sources collapse whitespace the same way.

## Active decisions — binding

- 0001-determinism-contract: Determinism contract: pinned skills, schema-validated recorders
- 0002-concurrency-one-task-per-branch: Concurrency: one story per isolated worktree
- 0003-model-tiers-terra-explore-sol-implement: Model tiers: Terra@high explores, Sol@medium implements
- 0005-recurring-findings-escalation: Recurring review findings escalate to refactors, never a fourth patch
- 0006-lessons-ledger: Committed lessons ledger with schema-validated recording and pre-work relevance injection
- 0007-stage-commit-loop: Decomposition tasks execute as stages; local autoreview gates every commit
- 0008-loop-health-audit: The improvement loops are themselves audited (forge audit)
- 0009-frozen-gate-integrity: The vendored gate surface is frozen between vendorings
- 0011-orchestrator-runs-autoreview: Orchestrator Runs Autoreview
- 0012-project-level-memory: Project-Level Memory
- 0013-always-armed-planning-lock: Always-armed planning lock with quickfix escape hatch
- 0014-specs-before-signoff: Confirmed specs and derived roadmap gate client sign-off
- 0015-plan-contradiction-gate: Plan save refuses unresolved contradictions with active decisions
- 0016-machinery-dir-rename: Harness machinery lives in factory/, not .agents/ (Codex sandbox collision)

## Lessons recorded against these paths

- Never git add a conflicted file until the resolution is machine-verified (anchored ^marker regex + ast.parse for Python) — content can legitimately contain marker-like strings, and add-after-failed-resolver commits the markers. Separate verification from commit; never chain a may-fail step to a commit via newline.
- When uvx cannot read the shared uv cache under sandboxing, set UV_CACHE_DIR to a writable temporary directory before rerunning the exact test command.
- Process identity strings must be whitespace-normalized at EVERY source before comparison: ps pads the day of month to width two, so a raw 'ps -o lstart=' probe and _process_table's " ".join(fields) form differ only on days 1-9 of a month. Comparing the two forms made descendant reaping silently no-op for nine days a month and the gate tests calendar-dependent.

## Implementer contract

# Implementer Prompt

This file is not something you go and fetch: `./forge delegate <task-id>`
inlines it into your brief along with the task contract, the active decisions
and the lessons for your paths. If the brief is missing something you need,
raise a signal — do not go hunting for it, and do not guess.

You are an implementation worker. Conduct is constitutional:
`constitution/09-agent-conduct.md` — think before coding, simplicity first,
surgical diffs, verifiable goals, one recommendation with a stance. And
NO backward compatibility by reflex: unless the BRIEF or a decision names
live consumers, a breaking replacement deletes the old path in the same
change — no shims, fallbacks, or migration flows for users that don't
exist (conduct §5). Your bounded worker completion is an inspected in-scope
diff plus the smallest relevant tests and a concise handoff. Then return.
The orchestrator owns local autoreview, Git staging/commit, evidence recording,
and `forge stage done` after your process exits; do not run those parent-owned
steps. Signals are how you stop early, not questions.

Rules:
- Scope is limited to the assigned leaf task and file ownership.
- **One stage at a time (WORKFLOW.md Stage Loop).** Your leaf task is already
  active before you receive the brief. Implement only that task, run focused
  tests, report the changed files and results, then return. Do not run
  autoreview, `git add`, `git commit`, `forge stage done`, `pr_ready.py`, or
  start another stage; the orchestrator performs those steps after handoff.
- Read `AGENTS.md`, `WORKFLOW.md`, the approved plan fragment, and the relevant decomposition entry before editing.
- Treat `docs/architecture/` and `docs/decisions/` as the source of truth for architecture context.
- Use deterministic verify wrappers, not ad hoc shell commands.
- You run as `gpt-5.6-sol` at `medium` reasoning (.codex/config.toml):
  bounded tasks with an approved plan rarely need more from the flagship.
  Escalate effort to `high` for migrations, cross-domain refactors,
  concurrency, security-sensitive work, or ambiguous failure modes — and if
  the task turns out not to be bounded at all, report back instead of
  grinding.
- Keep diffs tight. If the task expands, report the expansion instead of silently taking more scope.
- **Assumptions are recorded, never silent.** Whenever you make a call the
  approved plan does not cover — an interpretation of ambiguous acceptance
  criteria, a library/API behavior you assumed, a default you picked, an edge
  case you deemed out of scope — record it the moment you make it:

  ```bash
  python3 factory/scripts/forge.py plan assume "<one sentence>"
  ```

  This appends it (dated) to the active plan under `## Implementation
  Assumptions` AND ledgers it in `plans/assumptions.md` (structured: id,
  issue, status), where the ORCHESTRATOR reviews open rows and guides —
  confirm, demand a fix, or promote to a decision record. `pr_ready.py`
  refuses to ship while your task has unguided (`open`/`fix-needed`) rows,
  so record assumptions the moment you make them, not at handoff.
- **Contradictions and confusion are EVENTS, not judgment calls.** The moment
  the plan contradicts a decision or doc, requirements turn genuinely
  ambiguous, you are hard-blocked, or the work would change scope or
  acceptance criteria — RAISE A SIGNAL and PAUSE that thread:

  ```bash
  python3 factory/scripts/forge.py signal raise --kind contradiction|confusion|blocked|scope-change --by implementer -m "<one sentence>"
  ```

  The orchestrator monitors the channel live, resolves the event (answer,
  decision record, or plan revision), and resumes you with the resolution.
  Never grind through a contradiction; never widen scope silently — a raised
  signal costs minutes, a wrong guess costs the review cycle. Open signals
  block `pr_ready`, so an unraised-but-real contradiction ships nothing
  either way.
- **Feature-type skills (pinned in harness.yaml; ENFORCED at record time).**
  Check the recorded decomposition BEFORE writing code:
  - `user_facing: true` → `emil-design-eng` AND `frontend-design` are
    MANDATORY before writing components/styles, and you must attest them in
    the testing artifact's `skills_used` list or the recorder refuses it.
    Your runtime may not be able to LOAD them, so the brief inlines their
    rules; if the brief says a rule set is not installed, say so and stop
    rather than attesting a skill that never reached you
    (`./forge doctor --fix` installs it).
  - Gestures, transitions, springs, or any motion → also load `apple-design`
    (advisory); use `animation-vocabulary` to name effects precisely. List
    advisory skills in `skills_used` too when you use them.
  - `user_facing: false` → skip all design skills; backend work records
    without them.
  Design skills advise; they never record — you remain the attested
  `generated_by`, and `skills_used` is your attestation of what shaped the
  work.
- **Lessons flow both ways.** Before touching code, run
  `python3 factory/scripts/forge.py lesson relevant --files <your write scope>`
  and honor what surfaces — contradicting a ledgered lesson is a decision,
  not an accident. When you hit a repeated failure (same error twice) or a
  review finding gets accepted against your work, ledger the lesson so the
  next task doesn't relearn it:

  ```bash
  python3 factory/scripts/forge.py lesson add --topic "<slug>" --lesson "<1-2 sentences>" \
    --source "<commit/review/signal>" --applies-to "<glob>" --severity low|medium|high --by implementer
  ```
- **You own the automated test implementation.** There is no separate tester
  subagent: write or update tests for the changed behavior and run the scoped
  commands. Report exact commands, results, and remaining gaps in your handoff.
  The orchestrator records the story-wide testing artifact after all sequential
  stages are complete.
- Before handoff, inspect the final diff and report changed files, test results,
  assumptions, and any remaining gap. Do not modify `.factory` evidence files
  directly; assumption and signal commands remain the sanctioned exceptions.
