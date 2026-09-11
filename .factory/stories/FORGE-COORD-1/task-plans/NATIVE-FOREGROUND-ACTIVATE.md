# Symphony Forge process-loop recovery

## Current authority and boundary

Let `T=/Users/dev/Workdir/symphony-forge-native-dogfood-FORGE-COORD-1-NATIVE-FOREGROUND-ACTIVATE` and `A=/Users/dev/.codex/reviews/forge-lean-20260910`. The current reviewed product tip is `5b745bdd914c1a6cc5842db82f130dc5f6c21ae4`; the blocking review metadata commit is `ce4e233e881a39b5771f07569b9f6fa64cf5e155`.

`A/formal-review-ce4e233-blocking/sources.json` SHA256 `b7a01a468c564d5ce62bdb1d85a6792c18aafd8a436e1349fb08fa974f074b23` preserves the exact quality, performance and security artifacts, review-run binding and host log. `A/formal-review-remediation-plan.md` SHA256 `f21b30ef3a2403a18852b34561a3e9da414527f1aff46183ebfb582c2ec0db98` consolidates the seven recorded findings into six distinct issues and verifies the affected code and existing selectors.

Five repairs belong to First under the unchanged criteria and 66-path scope. The sixth, one combined helper result with atomic three-lens publication, is D-0032 and remains owned by `LEAN-WORKFLOW`; the active story plan explicitly keeps First on the current three-lens runner. Prior bootstrap, recovery, process-loop, model-policy, review-dataset, fixture, C8, proof and patch artifacts are immutable history. They are never payloads or recipes to replay. Decision 0064 authorizes these bounded in-scope corrections without changing the accepted contract.

## Goal and bounded changes

Repair only the five First-owned formal-review findings:

- Deny literal raw `codex exec` launches behind `env`, `/usr/bin/env`, `nohup`, `xargs`, shell `-c`, and other non-display wrappers while preserving exact help and existing safe prose/heredoc cases.
- Require independent PreToolUse matcher coverage for `apply_patch`, `Edit`, and `Write` in both `check_dual_runtime.py` and official Codex hook readiness. One tool must never certify another.
- Preflight every detached review dataset/prompt destination before the first write, reject symlinked or invalid ancestors/leaves, then use the existing no-follow factory byte writer. Do not claim atomic proof publication.
- Reuse one strict native grill-label parser in worker admission and dead-grill status: suffixes are legal only for `grill-task-<SAFE_TASK_ID>`; non-task gates are exact labels.
- Strengthen `test_native_launch_registers_before_stdin_and_records_terminal_identity` so it observes the `starting,running` ledger before the first stdin write. Production already appends `running` before `proc.stdin.write`, so this repair changes only the test and may be green before any production edit.

The first four bullets change behavior and their existing required selectors must demonstrate RED against the reviewed product tip before their production fixes. The fifth closes a proof gap around already-correct production ordering; do not manufacture a RED by changing working code.

Excluded: D-0032's combined helper/raw-result/candidate/pointer-last publication; background/status/resume; signal-origin or durable-output reconciliation; native questions; zero-human-round changes; story singleton changes; evidence schemas; CI parsers; new hook registrations; and any historical patch replay. `LEAN-WORKFLOW`, `NATIVE-LIFECYCLE`, and `SHARED-COORDINATOR-JOURNEY` retain their successor responsibilities.

Write scope remains the existing 66 paths. No path is added or removed. Budget remains `max_changed_files=180` and `max_changed_lines=18000`; measure the complete result and stop on overrun.

## Acceptance contracts

1. **NATIVE-FOREGROUND-ACTIVATE-C1.** NATIVE-FOREGROUND-ACTIVATE preserves the full target hook configuration and Claude parity: native hook JSON stays scoped, `.claude/settings.json` gains clear registration, `check_dual_runtime.py` verifies independent and both-adapter omissions, and official hook readiness remains trusted. As an explicitly additional user-requested overlay, First owns every current model-policy hunk without moving any of the original 40 prepared path/hunk allocations: its owning harness/launcher, active project profiles and guidance, all 15 committed team agent definitions, exact init/upgrade distribution proof, and same-plugin Luna/max doctor compatibility. Exploration uses Sol/low; planning, decomposition, architecture, plan validation and every grill use Sol/high; all implementation, technical test verification and autoreview fixes use Sol/medium, with formal Lite as the Luna/max exception; formal autoreview and functional checking use Sol/high; no new actor may run on Terra. Decision 0066 supersedes Decision 0062's model policy and amends only Decision 0031's model clause while preserving its Lite lifecycle. The original C8 Luna/max launch, receipt and transcript remain unchanged historical proof against the original approved task plan, not current selector authority. Review execution pins Codex to Sol/high and refuses an unreadable or known Terra-fallback helper before review-brief publication or process launch, with update-helper guidance and no doctor mutation.

2. **NATIVE-FOREGROUND-ACTIVATE-C2.** Process-bound admission remains truthful: foreground launch registers before stdin with terminal identity, zero-exit without completed turn is failed, and native write admission covers add/update/delete/move only after registration. Cancellation writes the existing durable revocation marker before cleanup signals; terminal success/failure plus dead process and released matching lock revoke completion; non-active stage incarnation revokes stage closure. Admission requires an exact starting/running row, live matching process ancestry, held matching lock, active matching stage and no explicit revocation; failed cleanup never invents success and no new completion tombstone is introduced.

3. **NATIVE-FOREGROUND-ACTIVATE-C3.** C9 review inputs are complete and task-specific: task, branch, and all three review lenses receive the full approved target task plan, approval/grill fields, digest identity, and resolved automated report; missing, unapproved, stale, summarized, truncated, or future-row-substituted inputs refuse.

4. **NATIVE-FOREGROUND-ACTIVATE-C4.** C10 proof uses one task-aware predicate for local worktree, committed CI, task-board/readiness through `task_proof_problems`, and pre-seal gating: verify ok, automated passed with no blockers, review scores/bindings clean, conditional functional proof clean, whole-bundle legacy fallback only with genuine task marker/history, and zero marker/Git/PR mutation on refusal; story singleton summary remains successor-owned.

5. **NATIVE-FOREGROUND-ACTIVATE-C5.** Workspace-before-JIT honors incumbent0063 first bootstrap and successor starts: source save/grill/approval and existing task-start refusals precede first preparation import; later `cmd_task_start` checks approved story/plan/decomposition, digest/task identity, fetched trunk, dependencies, protected path/owner, and then requires fresh target grounding/JIT/grill/approval, stage, and registered admission before writes.

6. **NATIVE-FOREGROUND-ACTIVATE-C6.** Unsupported native operations refuse before side effects: native background/read-only background, general status, live/dead worker status, cancel/resume/jobs, explore, and native question delivery do not compose briefs, spend question eligibility, append ledgers, signal processes, or dispatch children until their successor owners ship. The only native status exception renders already-dead registered native grill rows through existing dead_launches, restricted to strict grill gate/task labels and starting/running rows proven dead; it does not call the general status handler. Preserve unchanged Claude dispatch.

7. **NATIVE-FOREGROUND-ACTIVATE-C7.** Own-task review preflight uses `proof_path(base, story, artifact, task_id=args.id)` for the active task, accepts only own-task proof, and refuses story or other-task proof without helper fallback.

8. **NATIVE-FOREGROUND-ACTIVATE-C8.** The real admitted native worker proves protected-state read by executing forge next against the correct story/task/stage, then exercises the actual native tool hook against the protected task plan with harmless absent patch context. Only an actual correlated PreToolUse deny event counts: the existing automated report receipt, protected registered terminal row and durable tool log must identify the same native launch/session/tool call and actual hook-denial response. The existing implemented plan-contract review verdict checks that correlation; unchanged bytes, context/patch failure or a synthetic payload never certify denial. No new schema or CI/C10 evidence parser is introduced.

## Task graph and model policy

- `NATIVE-FOREGROUND-ACTIVATE` depends on nothing; `user_facing=false`.
- `LEAN-WORKFLOW` depends on `NATIVE-FOREGROUND-ACTIVATE`; `user_facing=false`.
- `NATIVE-LIFECYCLE` depends on `LEAN-WORKFLOW`; `user_facing=false`.
- `SHARED-COORDINATOR-JOURNEY` depends on `NATIVE-LIFECYCLE`; `user_facing=true`.
- `PORTABLE-DELIVERY-MIGRATION` depends on `SHARED-COORDINATOR-JOURNEY`; `user_facing=false`.
- `FORMAT-SOURCES` depends on `PORTABLE-DELIVERY-MIGRATION`; `user_facing=false`.
- `QUALITY-BASELINE` depends on `FORMAT-SOURCES`; `user_facing=false`.
- `FORGE-COORD-1.1` depends on `QUALITY-BASELINE`; `user_facing=false`.

C1 model policy: exploration Sol/low; planning, decomposition, architecture, plan validation and grills Sol/high; implementation, technical tests and review fixes Sol/medium; formal Lite Luna/max; formal review and functional checking Sol/high; no Terra execution. All eight task identities and successor objectives stay unchanged.

## Required Workflow

1. Main records the matching decomposition, saves this compact plan, rebinds the same completed five-gap grill with the separate current technical note, and binds standing approval once. The already-active stage is never restarted or rebaselined.
2. One registered Sol/medium worker reads the protected plan and the actual current quality, performance and security artifacts at metadata commit `ce4e233e`, checks the immutable archive, and uses ponytail's minimum-diff ladder for every code or test edit. It derives edits from the current checkout only and never reads or applies a historical patch.
3. Before production edits, the worker runs the four behavior selectors separately or in a pre-fix batch and records their expected failures: `test_codex_exec_ban_matches_invocations_not_prose`, `test_codex_hook_readiness_requires_exact_enabled_trusted_source`, `test_review_consumers_include_complete_approved_inputs`, and `test_native_unshipped_operations_refuse_before_dispatch`. A behavior selector that stays green means the proposed case or diagnosis is wrong; inspect and correct the test rather than editing production blindly. The launch-order selector may already be green because production order is correct.
4. The worker applies only the five repairs above. It does not implement the performance finding: D-0032 stays open for `LEAN-WORKFLOW`. It then runs exactly the five existing required selectors in one focused batch with fresh JUnit output:

```sh
UV_CACHE_DIR=/tmp/forge-lean-uv-cache UV_TOOL_DIR=/tmp/forge-lean-uv-tools uv run --python 3.11 --with pytest --with psutil python -m pytest factory/tests/test_gates.py factory/tests/test_native_setup.py factory/tests/test_native_launch.py -k 'test_codex_exec_ban_matches_invocations_not_prose or test_codex_hook_readiness_requires_exact_enabled_trusted_source or test_review_consumers_include_complete_approved_inputs or test_native_unshipped_operations_refuse_before_dispatch or test_native_launch_registers_before_stdin_and_records_terminal_identity' --junitxml=/tmp/forge-native-c8-formal-review-fixes-focused.xml
```

5. The worker runs `./forge next` and invokes the real native PreToolUse hook against the protected task plan with harmless absent patch context containing the literal marker `THIS PATCH MUST NEVER EXECUTE`. It returns concise prose only. It writes no receipt/handoff file, reads no raw logs or session history, self-delegates, or runs commit/lifecycle/proof/review/publication/CI commands.
6. After terminal return, Main correlates the current C8 public records, commits the bounded fix, runs one full host verify, records the compact current automated report, and runs the normal current three-lens Sol/high task review. Blocking findings loop through Sol/medium fixes and another task review. Main then owns stage closure, seal, task PR and CI.
7. After two identical failures with unchanged inputs and cause, stop expensive retries. Obtain the cheapest diagnostic capable of going RED, change the fix, and only then retry. All 41 required declarations and the three existing verify commands remain binding; Main's full verify covers them unchanged.

## Manual Verification

Confirm the four behavior guards fail for the new cases before their production edits, then confirm the five-selector focused batch passes and writes `/tmp/forge-native-c8-formal-review-fixes-focused.xml`. For the launch-order selector, the stdin proxy must snapshot exactly `starting,running` before forwarding the first byte, followed by the existing final `starting,running,succeeded` assertions.

For detached review writes, exercise both a symlinked ancestor and leaf and prove the outside sentinel is unchanged and neither helper nor recorder launches. For hook coverage, retain `Edit|Write` while omitting `apply_patch` and prove both checker and readiness refuse. For raw Codex execution, prove wrapped launches deny while grep/heredoc/display text remains allowed. For dead grills, prove every non-task suffixed label refuses and exact legal labels still render.

In the admitted worker, confirm `./forge next` names the actual current story/task/stage. The protected-plan probe passes only with a real correlated PreToolUse denial, unchanged plan SHA256 and `patch_executed=false`; unchanged bytes or a context failure alone do not pass C8. After commit, Main runs the unchanged three verification commands and reviews all three current lenses. D-0032 remains open and no combined-review publication code appears in the First diff.

