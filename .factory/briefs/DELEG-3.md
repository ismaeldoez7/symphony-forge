# Brief — DELEG-3: forge delegate composes the brief and the invocation

Story: FORGE-DELEG-1 | write access: YES — you may edit files in the write scope

This brief is the whole context you are given. It was composed from the recorded decomposition, the implementer contract, the active decisions and the lessons ledger. Do not go looking for the rules elsewhere; if something needed is missing, raise a signal instead of guessing (`./forge signal raise`).

## Objective

Delegation becomes a command instead of a judgement. It builds a brief from artifacts that already exist, derives write permission from stage state rather than a per-request opinion, prints the exact invocation, and records the delegation with the brief's digest.

## Acceptance criteria

- forge delegate <task-id> writes .factory/briefs/<task-id>.md carrying the objective, acceptance criteria, write_scope with the modules already in it, required_tests, reviewer_focus, the implementer prompt, the active decisions and the matching lessons
- for user-facing work the brief inlines the design rules, because the executing runtime cannot load them
- write permission is derived: an active stage with a non-empty write_scope is a write run, and --read-only is the explicit exception
- the printed invocation carries --prompt-file, the pinned model and effort, and the derived write flag
- the delegation is recorded in .factory/delegations.jsonl against factory/schemas/delegation.json with the brief's sha256

## Write scope — nothing outside this

- factory/scripts/forge_cli/delegate.py
- factory/schemas/delegation.json
- factory/scripts/forge.py
- factory/prompts/implementer.md
- .gitattributes
- factory/tests/test_gates.py

`forge stage done` refuses a change outside this list.

## What already exists in that scope (use it, do not re-create it)

- factory/scripts/forge_cli/delegate.py
- factory/schemas/delegation.json
- factory/scripts/forge.py
- factory/prompts/implementer.md
- .gitattributes
- factory/tests/test_gates.py

## Tests you must write

- test_delegate_brief_carries_criteria_and_scope
- test_delegate_derives_write_from_stage_state
- test_delegate_records_ledger_entry

The implementer writes and records the tests; a declared test that exists nowhere refuses the stage.

## Verify commands (they will be run when the stage closes)

- `python3 -m pytest factory/tests/test_gates.py -q -k delegate`

## Reviewer focus

the task id must be resolved against the recorded decomposition and never used to build a filesystem path; the ledger is append-only and union-merged

## Active decisions — binding

- 0001-determinism-contract: Determinism contract: pinned skills, schema-validated recorders
- 0002-concurrency-one-task-per-branch: Concurrency: one task per branch
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

## Implementer contract

# Implementer Prompt

You are an implementation worker. Conduct is constitutional:
`constitution/09-agent-conduct.md` — think before coding, simplicity first,
surgical diffs, verifiable goals, one recommendation with a stance. And
NO backward compatibility by reflex: unless the BRIEF or a decision names
live consumers, a breaking replacement deletes the old path in the same
change — no shims, fallbacks, or migration flows for users that don't
exist (conduct §5). The loop is autonomous (conduct §7): within your stage,
run it to completion — a clean local review is the permission to commit;
never pause to ask "proceed?". Signals are how you stop, not questions.

Rules:
- Scope is limited to the assigned leaf task and file ownership.
- **One stage at a time (WORKFLOW.md Stage Loop).** Your leaf task is a stage
  in `.factory/stages.json`. It is started with `forge stage start <id>`
  before you write code, and finished with `forge stage done <id>` only AFTER
  the stage's local autoreview came back clean and the stage is committed.
  Never batch multiple stages into one uncommitted diff.
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
  - `user_facing: true` → loading `emil-design-eng` AND `frontend-design` is
    MANDATORY, before writing components/styles — and you must attest them in
    the testing artifact's `skills_used` list, or the recorder refuses it.
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
- **You own the automated tests.** There is no separate tester subagent:
  write or update tests for the changed behavior, run the scoped test
  commands, and record the artifact yourself — JSON per
  `factory/schemas/test-automated.json` with `"generated_by": "implementer"`,
  recorded via:

  ```bash
  python3 factory/scripts/record_test_from_json.py --kind automated --input <json>
  ```

  Report remaining coverage gaps honestly; autoreview checks coverage as one
  of its lenses.
- Before handoff, run the self-check prompt and update `.factory` artifacts.
  Handoff with unrecorded assumptions is an incomplete handoff.
