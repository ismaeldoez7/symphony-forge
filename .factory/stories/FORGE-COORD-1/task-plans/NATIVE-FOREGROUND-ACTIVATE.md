# Symphony Forge process-loop recovery

## Current authority and boundary

Let `A=/Users/dev/.codex/reviews/forge-lean-20260910`. The user prioritized removing repeat-work loops first; Decision 0064 authorizes bounded corrections under unchanged criteria. Current target product HEAD: `d0237a56cac6de3fa5946a84b0e26171035ecf98`.

`A/before-process-loop-recovery-7af551b/sources.json` SHA256 `6ffaabfea27007e04350f8bad50c7f685b3b120a08ce610d6606e73e8474bfc3` preserves the prior plan, decomposition, five-finding grill, C8 and proof. Full host proof belongs to `66233ea`; the statement that `7af551b` needed full verify belongs only to that archived preceding state. The current `d0237a5` full-verification failure is recorded separately below.

Current evidence: `A/process-recovery-full-verify-d0237a5-failure/sources.json` records the full-host result at `d0237a5` as 1016 passed, one failed, and three platform skips; the only failure is `test_forge_next_routes_requirements_round_first`, whose old Claude fixture inherited the native host identity. `A/stale-fixture-delegate-864a7c5/sources.json` preserves the interrupted stale replay, including its uncommitted patch and terminal ledger rows: that worker re-applied already committed work and appended duplicate test definitions. These archives are diagnostic evidence, not payloads to replay.

Audits: `A/process-loop-worker-routing-audit.md` SHA `e4fe2a8e03d3608b857f2515d06d38e6553ea531d3c675b9616c9a66d403c717`; `A/process-loop-early-phases-audit.md` SHA `e73038809187f65aeaa3b7df74270a9fd6cd354c06b9eb7d5f2087677520a1d7`; `A/process-loop-late-phases-audit.md` SHA `5bd8b2277123d85a0d443428964363607a6f75ab93364a441a7073aa0a522009`. Preparation only.

Patches are historical references, never standing replay instructions. The worker may inspect the prior `process-loop-combined.apply_patch` to understand committed history. For the immediate corrective launch it may also inspect `A/fixture-recovery.apply_patch` and `A/fixture-recovery-receipt.json` if present; their current contents and hashes are not enduring recipe authority. Every remediation derives its edits from the actual tree, current failed verification, current review, and archived attempts. Amend the contract only for changed criteria, authority, graph, or 66-path scope.

## Goal and bounded changes

For `NATIVE-FOREGROUND-ACTIVATE`, remove:

- An authenticated registered child or authenticated native read-only grill can return its bounded handoff without inheriting Main's Stop persistence rule. Untrusted, malformed, terminal, or non-grill launches remain blocked.
- An active task routes from current delegation/proof: delegate once, watch live work, inspect a failed/dead handoff, then route through proof and closure. `forge next` does not blindly relaunch completed work or describe an active stage as pending.
- Native early-gate guidance states unsupported question delivery honestly, uses the current gate-floor rule, and offers sign-off grilling only after its full input set is ready. Implementing native questions and changing the zero-human-round floor remain successor-owned.
- Docs use the executable order: implement/test, commit, verify/record tests, one task review, conditional functional proof, stage closure, seal/publish, then task-proof-based story closeout. Recorded non-blocking follow-ups have a reason and revisit trigger without forcing an unchanged full review.
- An unchanged action/model failure with the same inputs and cause stops after two attempts. The next action is the cheapest diagnostic capable of going RED; retry only after a changed fix. External waits use bounded status checks.
- An unchanged sealed task retries PR publication without manufacturing another marker commit, while any changed proof or product still passes the full seal gate and reseals.

Excluded: background/status/resume, signal-origin or durable-output reconciliation, native questions, zero-human-round changes, story singleton changes, evidence schemas, and CI parsers. `NATIVE-LIFECYCLE`, `SHARED-COORDINATOR-JOURNEY`, and `LEAN-WORKFLOW` retain those successor responsibilities and retire any overlapping temporary wording when they ship.

Write scope is the prior 64 paths plus `factory/scripts/forge_cli/phase.py` and `factory/scripts/stop_continue.py`. No other path may change. Budget: `max_changed_files=180` and `max_changed_lines=18000`; measure the complete output before delegation and after implementation; stop on overrun.

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

1. Main records the matching decomposition, saves this compact plan, source-compat records the same completed five-finding grill plus the separate current technical check, then binds standing approval once. No new cold read, invented round, or question is needed.
2. The stage is already active since `2026-09-10T09:12:51`; never start or rebaseline it. Main delegates once to a registered Sol/medium worker. Before editing, the worker reads the protected plan and inspects the actual tree, current failed verification, current review, and archived attempt. It applies only remaining in-scope work or the narrow fix supported by that evidence; it never replays a committed historical payload or repeats a cold plan/grill while criteria and scope are unchanged. For the current corrective launch, restore `factory/tests/test_worker_admission.py` byte-exact to HEAD, remove the interrupted worker's duplicate additions from `factory/tests/test_gates.py`, and pin `FORGE_COORDINATOR=claude` inside `test_forge_next_routes_requirements_round_first` with pytest `monkeypatch`. Then run the actual failing selector and the adjacent native unsupported-delivery boundary with the command environment explicitly set to `FORGE_COORDINATOR=codex`; the in-test Claude pin, rather than a global proof workaround, must repair the old fixture. Later review fixes follow this same evidence-derived rule rather than reapplying the fixture reference. The worker proves that both touched test files contain no duplicate top-level helper or test definitions, runs `./forge next`, and invokes the real native PreToolUse probe against the protected task plan with a small literal absent-context marker containing `THIS PATCH MUST NEVER EXECUTE`.
3. The worker returns concise prose only. It writes no handoff/receipt file, reads no raw logs or session history, and runs no commit/lifecycle/proof/review/publication/CI command or self-delegation.
4. After terminal return, Main commits the complete product and runs one full host verify. Main then uses outside `capture-process-recovery-proof.py` and `compact-first-report.py` helpers to derive existing-shape C8 and the compact report from actual public records, correlating the terminal row and keeping missing links blocking. Helper recipes are not authority; no schema or parser is added.
5. Main records proof and runs one complete independent three-lens Sol/high task review with lossless inputs. Blocking findings loop through Sol/medium fixes and another task review; unchanged non-blocking follow-ups do not force a review solely to erase them.
6. Main closes the already-active stage, then performs seal, task PR, and CI. Story closeout consumes task proof and does not run a second story review.

Retain all 41 `required_tests` declarations/templates for gate evidence. A corrective worker runs only the selectors that can prove the actual current failure and its closest boundary; Main's later full host verify and stage proof still cover all 41. For the current fixture repair, use a fresh output file and exactly these two selectors:

```sh
UV_CACHE_DIR=/tmp/forge-lean-uv-cache UV_TOOL_DIR=/tmp/forge-lean-uv-tools FORGE_COORDINATOR=codex uv run --python 3.11 --with pytest --with psutil python -m pytest factory/tests/test_gates.py -k 'test_forge_next_routes_requirements_round_first or test_next_native_requirements_question_stops_at_unsupported_delivery' --junitxml=/tmp/forge-native-c8-fixture-recovery-focused.xml
```

Verification remains encoding hygiene, the native launch/setup/admission suite, and `factory/scripts/verify.py`, using task-local uv caches.

## Manual Verification

In the admitted worker, confirm `./forge next` names the actual current story, task, and active stage and routes from the current handoff/proof state without asking to repeat completed work. Exercise the actual native hook with a harmless absent-context patch against the protected task plan whose literal marker contains `THIS PATCH MUST NEVER EXECUTE`. Passing requires the real PreToolUse denial response, correlated launch/session/tool identifiers, unchanged pre/post plan SHA256, and `patch_executed=false`; a context failure, unchanged bytes alone, fixture, or worker prose does not pass C8.

After product commit, confirm one full host verify passes and the current automated report contains the focused selectors, terminal correlation, and C8 source lines. Review all three lenses against the complete approved plan and current report. For PR retry, reproduce an initial publication failure or existing-PR response, rerun with unchanged sealed product/proof, and confirm no new marker commit or changed branch tip occurs (a same-tip push is harmless); then mutate proof in an isolated fixture and confirm resealing remains mandatory.
