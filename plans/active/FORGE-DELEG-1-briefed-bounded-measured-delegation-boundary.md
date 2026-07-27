---
issue: FORGE-DELEG-1
title: Briefed, bounded, measured delegation boundary
status: approved
saved: 2026-07-27T12:10:13+00:00
story: FORGE-DELEG-1
decisions_reviewed:
  - 0001-determinism-contract
  - 0002-concurrency-one-task-per-branch
  - 0003-model-tiers-terra-explore-sol-implement
  - 0005-recurring-findings-escalation
  - 0006-lessons-ledger
  - 0007-stage-commit-loop
  - 0008-loop-health-audit
  - 0009-frozen-gate-integrity
  - 0011-orchestrator-runs-autoreview
  - 0012-project-level-memory
  - 0013-always-armed-planning-lock
  - 0014-specs-before-signoff
  - 0015-plan-contradiction-gate
  - 0016-machinery-dir-rename
---


# Gating the delegation boundary

## Context

Four reported failures in the Claude→Codex loop:

1. Claude follows the harness inconsistently and cannot say why.
2. Codex is sometimes launched without write permission, stalls silently, and
   nobody knows until someone asks.
3. On large changes Codex does part of the job, reports clean, and Claude
   believes it — because Claude reads the tail of the output.
4. Codex ignores existing components and design rules.

Two read-only audits found mechanical causes for three of them, and a
contract conflict for the fourth. Verified at file:line:

**Write permission is genuinely nondeterministic.** Three layers disagree:
the companion defaults read-only (`codex-companion.mjs:782`), this repo says
read-only unless `--write` (`pre_tool_use.py:275`, `harness.yaml:54`), and
the *plugin's own subagent* says "Default to a write-capable Codex run by
adding `--write` unless…" (`agents/codex-rescue.md:34`). A sonnet subagent
arbitrates per request. When it lands read-only the run gets
`sandbox: "read-only"` with `approvalPolicy: "never"` — Codex cannot write
**and cannot ask**, so it narrates a plan and exits 0.

**"Done" means "the model stopped talking."** Success is
`finalTurn.status === "completed" ? 0 : 1` (`lib/codex.mjs:754`). The
companion *collects* `touchedFiles` (`lib/codex.mjs:1152`) and never renders
it — the one fact that would expose half-work is gathered and discarded.

**Nothing injects context.** `factory/prompts/implementer.md` is referenced
by five docs and read by **zero scripts**; no `--prompt-file` wiring exists.
The rescue subagent is instructed "Do not inspect the repository"
(`agents/codex-rescue.md:27`). Repo `.codex/config.toml` is shadowed by
`~/.codex`, so the pinned model/effort never apply.

**The design rules are not installed for Codex.** `harness.yaml:86-91`
requires `emil-design-eng` + `frontend-design` for user-facing work;
`~/.codex/skills/` has `frontend-design` only. `emil-design-eng`,
`apple-design`, `animation-vocabulary` and `review-animations` are absent.
Every `skills_used` attestation naming them on a Codex-built artifact is
false.

**The task contract is decoration.** `write_scope`, `verify_commands` and
`required_tests` are declared per task and consumed only by the board's HTML
and a markdown renderer. Nothing compares the diff to `write_scope`, nothing
executes `verify_commands`, nothing resolves `required_tests` against disk.
`forge stage done` checks exactly one thing — that the stage was started
(`stages.py:96-105`) — so a half-done job passes, signed by the same actor
who misread the output. Every diff-based check in the repo fires when *too
much* changed; nothing fires when too little did.

**The composite path:** Codex does 3 of 8 criteria → `stage done` needs no
evidence → `verify.py` passes because the repo still compiles → the tester
self-reports `status: "passed"` with `commands_run` never executed → no
signal raised → `pr_ready` prints `PR_READY`.

Decisions, grilled and locked:

| Decision | Choice |
|---|---|
| Completion gate | `stage done` measures the diff and REFUSES |
| Delegation | `forge delegate` composes brief + invocation; `--write` derived from state |
| Brief | Hook-gated: a `--write` run without a recorded brief is denied |
| Visibility | `forge codex status` reads the plugin's job registry |
| Per-task verify | `verify_commands` must be runnable; prose refused; `stage done` runs them |

---

## 1. Completion becomes a measurement — `forge_cli/stages.py`

`cmd_start` records the base commit (`git rev-parse HEAD`) on the stage.
`cmd_done` then refuses unless:

- **Something changed.** `git diff --name-only <base>..HEAD` plus the working
  tree is non-empty. An empty diff is the silent-stall signature.
- **Changes are in scope.** Every changed product path is covered by the
  task's `write_scope` (prefix match; `EVIDENCE_PATHS` from `pr_ready.py:33`
  are exempt, as they already are for freshness). Out-of-scope paths are
  named in the refusal.
- **Declared tests exist.** Every `required_tests` entry resolves to a file.
- **Per-task verify passes.** Each `verify_commands` entry runs (reusing
  `factory_lib.run_cmd`); a non-zero exit refuses.

`--parallel` keeps its meaning but stops being an unchecked assertion: it now
verifies the two stages' `write_scope` lists are genuinely disjoint.

New `forge stage done --incomplete "<what is missing>"` records a partial
delivery: the stage stays open, the note lands in the events ledger, and
`forge next` surfaces it. Today a worker that finishes 60% has no vocabulary
for it — the signal kinds all presume it wants to continue.

## 2. Delegation becomes a command — `forge_cli/delegate.py` (new)

`./forge delegate <task-id> [--read-only] [--background]`:

1. **Builds the brief** into `.factory/briefs/<task-id>.md` — the task's
   objective, acceptance criteria, `write_scope`, `required_tests`,
   `reviewer_focus`; the body of `factory/prompts/implementer.md`; the active
   decisions (`decision list --active`); lessons matching the task's
   `write_scope` (`forge_cli/lessons.py` already does this); and the design
   rules **inlined** for user-facing work, because Codex cannot load them.
2. **Derives write permission** from state: a stage that is `active` with a
   non-empty `write_scope` is a write run. `--read-only` overrides for
   exploration. The flag stops being a sonnet's judgement.
3. **Prints the exact invocation**, including `--prompt-file` pointing at the
   brief and the pinned `--model`/`--effort` from `harness.yaml` (which the
   repo `.codex/config.toml` cannot enforce because `~/.codex` shadows it).
4. **Records it** — `.factory/delegations.jsonl`, schema-validated:
   `{at, task, brief_sha256, write, model, effort, generated_by}`. Union-merge
   per the ledger rule established in 0017.

Existing-component context: the brief lists the modules already present in
the task's `write_scope` (a file listing plus exported symbols where cheap),
so "use what exists" is data rather than an instruction.

## 3. The brief becomes non-skippable — `factory/scripts/pre_tool_use.py`

Extend the existing companion rule (`:320-325`): a `--write` companion call
is denied unless `.factory/delegations.jsonl` holds a brief for the **active**
stage whose `brief_sha256` still matches the file on disk. Also closes the
current hole where the whole check is skipped in plan mode.

The refusal names the command that fixes it (`./forge delegate <task-id>`).

## 4. Visibility — `forge_cli/codex_status.py` (new)

`./forge codex status` reads
`~/.claude/plugins/data/codex-openai-codex/state/<slug>/jobs/*.json` and
reports, per job: status, phase, the **write flag**, age, and log path.
Flags two conditions loudly — a job `running` with no phase change for N
minutes, and a job that ran `write: false` while a stage was active (the
silent-stall signature). Degrades to "unknown" if the plugin path moves; it
is a diagnostic, never a gate. Wired into `forge next` so a stalled run
surfaces without being asked for.

## 5. The skills gap — `forge_cli/doctor.py`

`forge doctor` gains a check: every skill `harness.yaml` requires or advises
must be loadable by **each runtime that has to attest it** — i.e. present in
`~/.codex/skills/` as well as `~/.claude/skills/`. `--fix` installs the
missing ones. Today the harness refuses an artifact that doesn't attest
`emil-design-eng` while the runtime being asked to attest it cannot load it.

## 6. Why the harness gets skipped — `factory/scripts/forge_cli/phase.py`

`forge next` already prints the current phase and exact next actions. It
gains the delegation step explicitly (brief → delegate → watch → verify),
so "what should I have done" has a deterministic answer to point at rather
than a recollection.

## Enforcement matrix

Prompts may explain; these refuse.

| Rule | Coded gate |
|---|---|
| A stage is done only if something changed | `stage done` refusal |
| Changes stay inside `write_scope` | `stage done` refusal, out-of-scope paths named |
| Declared tests exist | `stage done` refusal |
| Per-task verify passes | `stage done` runs `verify_commands` |
| `verify_commands` are runnable, not prose | `record_decomposition_from_json.py` refusal |
| `--parallel` means disjoint scopes | `stage start` checks the scopes |
| A write delegation is briefed | `pre_tool_use.py` denial |
| Write permission is derived, not typed | `forge delegate` composes the invocation |
| Required skills are loadable where attested | `forge doctor` check |
| Partial delivery is sayable | `stage done --incomplete` + events ledger |

Deliberately advisory: `forge codex status` (a diagnostic reading a
third-party path must not be able to block a ship).

## Files touched

- new: `forge_cli/delegate.py`, `forge_cli/codex_status.py`,
  `factory/schemas/delegation.json`, `docs/decisions/0018-delegation-gates.md`
  (status `proposed` — acceptance is human)
- gates: `forge_cli/stages.py`, `record_decomposition_from_json.py`,
  `pre_tool_use.py`, `forge_cli/doctor.py`, `forge_cli/phase.py`, `forge.py`
- docs: `factory/prompts/implementer.md` (it becomes brief *input*, so it must
  read as instructions to Codex rather than about it), `AGENTS.md` (one line
  in the phase contract; watch the 110-line cap), `factory/skills/forge.md`
  (intents: "delegate this task", "is Codex stuck?"), `.gitattributes`
- tests (`factory/tests/test_gates.py`): stage-done refusals (empty diff,
  out-of-scope path, missing required test, failing verify command);
  `--parallel` disjointness; prose `verify_commands` refused at record time;
  unbriefed `--write` denied by the hook and allowed once briefed; brief
  contains AC + write_scope + inlined design rules for user-facing tasks;
  write derived from stage state; `codex status` parses a fixture job dir and
  reports a stalled job; doctor flags a missing Codex-side skill.

## Migration

`verify_commands` prose exists in real projects (`agentstats`: `"package
test script"`). The recorder refuses it only for **new** decompositions;
shipped history is untouched. `forge doctor` reports any active decomposition
carrying prose so it is fixed before the next `stage done`.

## Build

Implement directly in this session (Codex delegation is the thing under
repair — using it to repair itself risks the exact failure being fixed), then
ONE autoreview pass, three lenses, run directly per decision 0011.

## Surface Impact

| Surface | Status | Note |
|---|---|---|
| Runtime behavior | Changed | `stage done` becomes a measurement and can refuse; `stage start` records a base commit and checks `--parallel` disjointness; the pre-tool hook denies unbriefed `--write` companion calls |
| CLI/ops | Changed | new `forge delegate` and `forge codex status`; new `stage done --incomplete`; `forge doctor` gains a per-runtime skills check; `forge next` names the delegation step |
| Data/schema | Changed | new `factory/schemas/delegation.json`; new append-only `.factory/delegations.jsonl` (union-merge per 0017) and `.factory/briefs/<task-id>.md`; `stages.json` entries gain `base_sha`. No existing schema loosened; evidence still enters `.factory/` only through recorders (0001) |
| Docs | Changed | `factory/prompts/implementer.md` rewritten as brief input; one line in `AGENTS.md` (110-line cap holds); `factory/skills/forge.md` intents; `docs/decisions/0018-delegation-gates.md` recorded as `proposed` — acceptance is human chat confirmation |
| Tests | Changed | new cases in `factory/tests/test_gates.py` for every refusal listed in the enforcement matrix |
| API | N/A | no programmatic API surface in the harness |
| UI | Unchanged by design | the board is read-only by contract; delegation state is CLI-surfaced this round. Rendering `delegations.jsonl` on the board is deferred — it needs the display-layer work already listed as outstanding on PR #24 |

## Verification

1. `pytest factory/tests/` green; `check_dual_runtime.py` clean; AGENTS
   hygiene OK.
2. Scratch-clone rehearsal: `stage start` → touch nothing → `stage done`
   refuses "no change"; touch an out-of-scope file → refuses, names it;
   delete a `required_tests` file → refuses; break a `verify_commands`
   target → refuses; satisfy all four → passes.
3. Hook: a `--write` companion call with no brief is denied; `forge delegate`
   then the same call is allowed; editing the brief on disk invalidates it.
4. `forge delegate` on a user-facing task produces a brief containing the AC,
   the write_scope file listing, and the inlined design rules; the printed
   invocation carries `--write` and the pinned model/effort.
5. `forge codex status` against the real plugin state dir lists today's job
   with its write flag; against a fixture with an old `running` job, flags it.
6. `forge doctor` reports `emil-design-eng` missing for the Codex runtime;
   `--fix` installs it and the check goes green.
7. Demo project (`toolshed`) still ships a story end to end under the new
   gates.

## Implementation Assumptions

<!-- Made during implementation, NOT part of the approved plan. Dev: review these before merge; promote any that matter to docs/decisions/. -->
- 2026-07-27: stage done exempts only .factory/ and plans/, NOT pr_ready's EVIDENCE_PATHS as the plan said — that list exempts all of factory/ and docs/, which in this repo is the product, so reusing it would make the write_scope check vacuous exactly where it is dogfooded
- 2026-07-27: required_tests entries are test NAMES by existing convention (see any recorded decomposition), not file paths as the plan assumed — resolution is a fixed-string search across tracked and untracked files, excluding .factory/ and plans/ so the declaration cannot match itself
- 2026-07-27: stage start also records dirty_at_start and stage done subtracts it: a file already dirty when the stage began is not that stage's work, and blaming it for one would refuse honest runs over unrelated edits
