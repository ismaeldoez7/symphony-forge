# Branch-wide plan-contract review brief

For each contract, emit a verdict — implemented | partial | missing — with file:line evidence, recorded as contract_verdicts in the quality artifact. Then review the diff normally; the contract check does not replace the quality/performance/security lenses.

## Task ACC1-T1

### Plan contracts

- **ACC1-C1**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: Recording execution detail (write_scope, required_tests, verify_commands) on a pending non-frontier task is refused with the task id and field named
- **ACC1-C2**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: The frontier task records detail successfully and completed tasks keep theirs (legacy cutover)
- **ACC1-C3**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: Existing suite is green after fixture migration with original refusal coverage preserved

### Reviewer focus

Frontier resolution is the risky seam: the recorder's earliest-pending-leaf computation must agree with the protected stage authority in stages.py (status source of truth), or recorder and gates will disagree about which task may carry detail. Second seam: the done-task exemption is the legacy-cutover path - refusing a completed task's existing detail would brick every historical re-record. Refusal messages must name the offending task id and field. Fixture migration must not weaken existing gate coverage (tests that deliberately record full decompositions must still exercise their original refusal).

## Task ACC1-T2

### Plan contracts

- **ACC1-C4**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: stage start refuses an incomplete or ungrilled frontier contract, naming the missing piece
- **ACC1-C5**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: delegate re-checks readiness on write runs and refuses an active empty-scope stage
- **ACC1-C6**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: explicit --read-only delegation still passes and cannot close a stage

### Reviewer focus

Ordering is the risky seam: the readiness refusal in _cmd_start_locked must fire BEFORE any stage-state mutation and before the task_sha256 baseline stamp, or a refused start still pollutes measurement state. Second seam: delegate's write derivation - readiness re-check must precede launch for every write run; an active stage with empty write_scope refuses with a message naming the missing piece and the producing command; explicit --read-only stays exploration-only and must not satisfy stage done. Lite/quickfix/degraded behavior untouched. Self-application: this story's own T3 stage start runs through the new gate live - a wrong refusal wedges the loop.

## Task ACC1-T3

### Plan contracts

- **ACC1-C7**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: forge next reports author-contract (with plan-mode instruction) / grill / stage-start / delegate as the single next action per frontier state
- **ACC1-C8**
  - Source: plans/active/FORGE-ACC-1-jit-frontier-is-enforced-not-advisory.md#acceptance-criteria
  - Statement: docs/FACTORY.md, WORKFLOW.md, and factory/prompts/decomposer.md state the enforced JIT contract with no upfront-contract instruction remaining

### Reviewer focus

Single-action invariant is the risky seam: for the earliest unfinished task, forge next emits exactly ONE next action per state - skeleton contract -> enter plan mode, author the JIT contract, re-record (decisions 0029/0032); complete-but-ungrilled or stale -> run the task griller; fresh pass -> forge stage start; active -> forge delegate - never the current start+delegate pair. State must be DERIVED from the same primitives require_ready_task uses (a small non-raising task_frontier_state helper in factory_lib beside it; ACC-2's board rows consume the same helper), not recomputed independently. forge board's next_actions re-parse must keep working. Docs edits (FACTORY.md upfront-contract list, WORKFLOW/decomposer digest wording, forge skill task-loop, AGENTS.md narration line sharpened per conduct s8) must remove the contradiction without weakening any other stated contract.
