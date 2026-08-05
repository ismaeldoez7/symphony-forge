# Brief — PH-3.2: Bind the decomposition to its plan, and make task fields mean something

Story: PH-3 | write access: YES — you may edit files in the write scope

This brief is the whole context you are given. It was composed from the recorded decomposition, the implementer contract, the active decisions and the lessons ledger. Do not go looking for the rules elsewhere; if something needed is missing, raise a signal instead of guessing (`./forge signal raise`).

## Objective

Stamp project, story, epic, plan_file and the plan digest into the decomposition from run.json and the roadmap, refuse a digest that does not match the active plan, and validate verify_commands and dependencies.

## Acceptance criteria

- The recorder writes project, story, epic, plan_file and plan_sha256 from .factory/run.json and plans/roadmap.json; agent-supplied values for those keys are dropped, not merged.
- plan_sha256 is the digest of the plan the RECORDER read, so it is true at record time without asking a producer to hash a file. A supplied digest that disagrees with the active plan is still refused.
- stage start refuses when the active plan's digest no longer matches the one stamped on the decomposition: the realistic staleness is the plan being edited AFTER the task graph was recorded, which no record-time check can see.
- Artifacts recorded before this change stay readable: the new fields are optional in the schema and .factory/history/ artifacts still parse, including ones with no plan_sha256 at all.
- Every task's verify_commands entry is checked with doctor.unrunnable_reason; prose is refused and a real command passes.
- required_tests may be [] and the task is still accepted, provided verify_commands is runnable.
- dependencies defaults only when ABSENT — false, 0, '' and {} are refused rather than silently read as an empty list — and may only name an earlier task.
- The recorder refuses when the roadmap has no story matching run.json rather than inventing an epic.

## Write scope — nothing outside this

- factory/scripts/record_decomposition_from_json.py
- factory/schemas/decomposition.json
- factory/scripts/forge_cli/stages.py
- factory/tests/test_gates.py

`forge stage done` refuses a change outside this list.

## What already exists in that scope (use it, do not re-create it)

- factory/scripts/record_decomposition_from_json.py
- factory/schemas/decomposition.json
- factory/scripts/forge_cli/stages.py
- factory/tests/test_gates.py

## Tests you must write

- test_decomposition_provenance_overrides_agent_supplied_fields: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_decomposition_refuses_prose_verify_commands: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_decomposition_accepts_empty_required_tests: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_historical_decomposition_artifacts_still_parse: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_stage_start_refuses_a_decomposition_whose_plan_moved: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)
- test_decomposition_refuses_a_falsy_non_list_dependencies: `uvx --with pytest python3 -m pytest {path}::{id} -q -o junit_family=legacy --junitxml={report}` (factory/tests/test_gates.py)

The implementer writes and records the tests; a declared test that does not exist or whose exact command fails refuses the stage.

## Verify commands (they will be run when the stage closes)

- `uv run --with pytest python -m pytest factory/tests/test_gates.py -q -k "decomposition or provenance or unrunnable"`

## Reviewer focus

That promoting doctor.unrunnable_reason from advisory output to a refusal path does not change what it accepts for doctor's existing caller.

## Active decisions — binding

- 0001-determinism-contract: Determinism contract: pinned skills, schema-validated recorders
- 0002-concurrency-one-task-per-branch: Concurrency: one story per isolated worktree
- 0003-model-tiers-terra-explore-sol-implement: Model tiers: Terra@high explores, Sol@medium implements
- 0005-recurring-findings-escalation: Recurring review findings escalate to refactors, never a fourth patch
- 0006-lessons-ledger: Committed lessons ledger with schema-validated recording and pre-work relevance injection
- 0007-stage-commit-loop: Decomposition tasks execute as stages; local autoreview gates every commit
- 0008-loop-health-audit: The improvement loops are themselves audited (forge audit)
- 0009-frozen-gate-integrity: The vendored gate surface is frozen between vendorings
- 0010-client-signoff: Client Signoff
- 0011-orchestrator-runs-autoreview: Orchestrator Runs Autoreview
- 0012-project-level-memory: Project-Level Memory
- 0013-always-armed-planning-lock: Always-armed planning lock with quickfix escape hatch
- 0014-specs-before-signoff: Confirmed specs and derived roadmap gate client sign-off
- 0015-plan-contradiction-gate: Plan save refuses unresolved contradictions with active decisions
- 0016-machinery-dir-rename: Harness machinery lives in factory/, not .agents/ (Codex sandbox collision)
- 0017-repo-as-system-of-record: The repo is the system of record: outcomes, timeline, and decision provenance
- 0018-delegation-gates: Delegation Gates
- 0019-client-signoff: Client Signoff
- 0022-conflict-free-ledgers: Conflict Free Ledgers
- 0023-stage-delta-by-ref: Stage Delta By Ref

## Lessons recorded against these paths

- When uvx cannot read the shared uv cache under sandboxing, set UV_CACHE_DIR to a writable temporary directory before rerunning the exact test command.
- When uvx cannot read the shared uv cache under sandboxing, set UV_CACHE_DIR to a writable temporary directory before rerunning the exact test command.
- Never git add a conflicted file until the resolution is machine-verified (anchored ^marker regex + ast.parse for Python) — content can legitimately contain marker-like strings, and add-after-failed-resolver commits the markers. Separate verification from commit; never chain a may-fail step to a commit via newline.
- When uvx cannot read the shared uv cache under sandboxing, set UV_CACHE_DIR to a writable temporary directory before rerunning the exact test command.
- Upgrading a pre-rename repo: run `forge stage migrate --base <sha>` BEFORE re-recording the decomposition, not after. write_skeleton preserves stage status only from PROTECTED authority, which a legacy repo does not have yet — so re-recording first writes protected state with every stage reset to pending, and stage migrate then refuses because the authority already exists. Recoverable only because .factory/stages.json is committed: restore it, remove the freshly written .git/forge pair, then migrate.

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
