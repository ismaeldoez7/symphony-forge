---
issue: FORGE-COORD-1
title: Either Claude or Codex coordinates the same Forge workflow
status: approved
saved: 2026-09-10T08:28:23+00:00
story: FORGE-COORD-1
decisions_reviewed:
  - 0001-determinism-contract
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
  - 0035-commit-belt-keeps-ledger-fresh
  - 0036-client-gates-arm-on-roadmap
  - 0037-strict-role-split
  - 0038-portable-fail-closed-hooks
  - 0040-windows-user-scope-first-elevation-deferred
  - 0041-sandboxed-workers-default
  - 0042-psutil-cross-platform-process-model
  - 0044-accountable-engineering-loop
  - 0045-conflict-free-story-state
  - 0046-scoped-layout-activation-ordering
  - 0047-task-level-worktree-and-pr
  - 0048-plan-mode-and-grill-provenance
  - 0050-plan-authoring-is-mode-agnostic
  - 0051-every-grill-gate-is-ledger-matched
  - 0052-approval-to-pr-is-the-agents
  - 0053-interchangeable-coordinator-shared-forge-contract
  - 0054-native-questions-and-task-proof
  - 0055-enforced-static-quality-baseline
  - 0056-staged-quality-baseline-rollout
  - 0057-coordinator-operation-simplification
  - 0058-bounded-native-bootstrap-support
  - 0059-task-owned-jit-workspaces
  - 0060-child-signal-mask-restoration
  - 0061-host-native-human-interaction
  - 0062-luna-max-exploration-and-implementation
  - 0063-first-native-task-workspace-bootstrap
  - 0064-lean-delivery-and-durable-history
  - 0065-ci-platform-evidence
---

# Symphony Forge: lean delivery

Draft revised against the completed independent plan read. Accepted Decision 0064 authorizes the simpler workflow and client migration; existing recording and admission gates still apply. The specification is confirmed at SHA256 `bb3c94c137c7f1ec56d4e5f5814ee634a1683997a906b66600d476063929b557`. Main publishes the exact planning inputs below before plan approval.

## Problem

Repeated plans, approvals and review launches slow delivery and lose settled answers. The developer should decide once when necessary, then let authorized work continue through tests, review, PR and green CI. Fresh workers and reviewers must receive the same ruling. Overnight work returns a compact account of completed PRs, real blockers and decisions needed.

## Scope / Non-goals

Keep the complete native and Claude coordinator outcome, original preparation, all Python quality work, required local Mac and Linux/Windows CI proof with unavailable live-platform limitations, separate installed-client dogfood and all ten audited client failures. Replace the unapproved 39-task graph with eight coherent tasks. Preserve unrelated work, client configuration and MyClaw hotfixes. No fabricated approval/proof, manual protected-state repair, new coordinator or ruling ledger, blanket generated-file exclusion, or additional review ceremony.

## Acceptance Criteria

The owner labels refer to the exact task IDs in Task Decomposition. Each owner supplies its own task-bound evidence; Integration must verify the complete outcome.

| Spec criterion | Owners | Required evidence |
|---|---|---|
| AC1: real human answers | First, Shared, Integration | Host-permitted main decisions; exact optional question/session/tool/story/answer identity; replay, cancellation and malformed answers refuse. |
| AC2: protected writes | First, Native lifecycle, Integration | Denied coordinator/unregistered writes, admitted bounded contribution and stale/revoked authority refusal. |
| AC3: native independence | First, Native lifecycle, Portable, Integration | Launch/status/recovery/setup without Claude dependencies; existing Claude route passes. |
| AC4: workers and gates | First, Lean, Native lifecycle, Shared | Shared model/effort policy and the same approval/admission/test/review/PR proof for both coordinators. |
| AC5: hook delivery | First, Shared, Portable, Integration | Startup/resume/clear/compact/question/Stop observations; individual and shared omission regressions. |
| AC6: honest runtime proof | Integration | Four required local Mac/CI rows pass with actual logs and evidence kind; failures or missing required proof block. Accepted0065 live-platform limitations remain explicit. |
| AC7: genuine native task | First, Integration | Actual admitted new contribution, task verification/review/PR/CI; imported preparation earns no contribution. |
| AC8: setup and preservation | Portable | Fresh/adopted/upgraded destinations, selection/refusal and repair parity; client ownership and history preserved. |
| AC9: continuation and context | Lean, Shared | Settled rulings survive fresh workers; authorized work resumes without repeated prompts; optional unanswered questions do not block it. |
| AC10: handoff | First, Native lifecycle, Shared, Integration | Completed-task boundary, actual question state, active-worker/incomplete-proof refusal and correct owner. |
| AC11: developer journey | First, Lean, Shared, Integration | Real source/target binding, current artifact display, task-owned workspaces, safe queue/retry/reconciliation and board functional proof. |
| AC12: full quality | Format, Quality, Portable, Integration | Pinned full source/test lint, format and types; missing-configuration and deliberate-violation failures; meaningful client checks. |

| Roadmap criterion | Owners and closing proof |
|---|---|
| 1. Both coordinators preserve existing worker policy and every Forge gate. | First/Lean/Native lifecycle/Shared; Integration closes policy parity, identity-bound proof and the real lifecycle. |
| 2. Codex records real human grill provenance and runs without Claude or plugin state. | First/Shared/Native lifecycle/Portable; Integration closes actual permitted answers/events and native-only launch/setup with required local Mac/CI proof and honest live-platform limitations. |
| 3. Approved bounded bootstrap, registered contributions, predecessor markers, complete review, mandatory quality and final parity chain. | All eight tasks: exact preparation inputs, actual contribution/proof/PRs, sequential trunk markers, complete quality, separate client lifecycle and required local Mac/CI proof with honest live-platform limitations. “Existing review limits” means the installed safeguards under accepted 0064, not the superseded byte caps. |

The graph retains the exact three roadmap strings, original 39-row mapping, ten client-failure owners, task-level `user_facing` values and complete preparation allocation. Its digest below binds those details to this plan; changing ownership afterward requires the existing contract amendment route.

## Technical Approach

### One brief and proportionate scrutiny

Use the existing task plan as the current brief: behavior, boundaries, owner, checks and rulings. Keep story/specification intent and client sign-off; derive execution and review inputs from existing records. Main presents a real new decision with its recommendation, tradeoff, consequence and concrete artifact. Carry actual standing authorization through in-scope corrections and retries using existing approval commands. New intent, scope or missing authority blocks dependent work; independent ready work continues. Reuse brief/contract/ruling recorders, not a new ledger.

Lean makes `design_review: required|routine` explicit in the existing approval-bound brief/frontmatter. Missing or unknown means required. Permissions, security boundaries, destructive operations, data migration, substantial architecture changes and material changes to them require design scrutiny. Routine work needs an explicit no-trigger rationale. A worker cannot downgrade the classification. One genuine assessment may cover several applicable existing gates only when it explicitly reviewed every complete input and each record remains independently bound to its own artifact. This does not permit copied passes. The confirmed specification names each gate's exact classification input, record and digest, including roadmap classification derived from capability specs. Shared reads must explicitly assess each complete input; current one-gate launches cannot certify other gates. Classification and rationale remain authored digest-bound content, not excluded managed metadata. Incumbent prerequisites remain until Lean ships.

### Review and measurable cleanup boundaries

Main runs one `./forge review <task-id>` operation per task and loops fixes/review until clean. Accepted 0064 and 0011 authorize this procedure; proposed 0049 supplies no authority. First uses the current three-lens runner inside that operation. Lean changes the implementation to a combined operation with explicit quality, performance and security assessments. Preserve the three existing `reviews/{quality,performance,security}.json` artifacts, all linked by `review_run_id`, `brief_sha256` and `branch_diff_digest` for the same task. Every supplied chunk and every actual assessment must finish successfully. No unassessed lens may inherit a copied pass; no nested or second story-wide review.

The reconciled specification removes the old 120,000-byte product and 180,000-byte review caps under accepted 0064, including the obsolete 0058 clause. The actual specification save, grill and confirmation are complete. The current resolved autoreview helper has no implicit patch-size cap and supports lossless partitions; its observed 512,000-byte limit covers each complete rendered prompt, including instructions, evidence and framing. It is a tool safeguard, not a new task-size policy. Use its supported evidence batching when the fixed preamble would leave insufficient room; never trim authoritative input or change its limit.

Format measures the actual pinned formatter output after Portable ships. Quality measures the actual remaining diagnostics and repair diff after Format ships. Each JIT records exact files, changed lines, total input bytes and rendered partition sizes, then binds positive file/line budgets to that complete scope. Recheck before review and seal. Stop if the actual scope exceeds those budgets, any full prompt cannot be partitioned within the installed limit, any input/chunk is missing or failed, or Format introduces semantic changes. Use the existing amendment route; split only a genuinely independent behavior/proof boundary after a material contradiction. Bytes or chunk count alone do not create new tasks. Format retains exact reproduction, AST and comment/directive preservation, full tests and reviewed exceptions. Generated SQL, snapshots and journals remain counted and reviewed for semantics and security.

### Reproducible preparation and first worker

Main publishes these exact bytes under `plans/exploration/coordinator-parity-preparation/` before approving this plan:

| Artifact | SHA256 | Purpose |
|---|---|---|
| `lean-delivery-graph.json` | `a226f10f82ca29dad76546f2bf19c3c52b2b392ff0669dd4dc2439555c735323` | AC/roadmap/owner crosswalk plus `prepared_hunk_owners`: all 40 original paths and 201 hunk identities, hashes and allocations. |
| `native-original-40-path.patch` | `09cd2ec4826e407541cc4fe75d6d604f9ce6b8bb9f1c8b734aef23e2e42ad54f` | Exact 342,596-byte original donor history; distinct from older `original-bootstrap.patch`. |
| `native-foreground-preparation.patch` | `bee122bb370177ededefb5fe81a82f8c600f69af8502e151956ec7b8afed29e2` | Exact 109,953-byte, 16-path first import against `824baed4a657a83a6a7583e85ee67d2907e7c172`. |
| `native-foreground-preparation-inventory.json` | `3874bb1a3e698c340c19b419d22cad897d12c80d2314bd4b5142d5c3656fa48f` | Existing per-path source/trunk/prepared hashes and first selection. |
| `client-ledger-migration-inventory.json` | `58ceca629e89aa1a213451f1c9fbe6e6ce27d91492a658c538dc4190ce4c8e05` | Dated five-checkout snapshot, deduplicated into four common directories. |

The graph has no reverse plan hash, avoiding a circular binding. Its hunk mapping inherits each path's remainder owner unless an explicit hunk override differs. Exact foreground-selected material belongs only to First; the remainder belongs to its named successor. Archived superseded bytes require an explicit equivalent/corrected/retired disposition in that owner's complete review. Nothing is silently dropped or credited twice. There is no second mapping registry.

Preserved S `/Users/dev/Workdir/symphony-forge-native-dogfood` drives the existing 0063 source ceremony. Existing task start creates real T from fetched trunk; validate any newer baseline before import. Import only the bound foreground allocation, then freshly ground and bind T before stage start and registered admission. Source proof cannot certify T. C `/Users/dev/Workdir/symphony-forge-lean` remains the captured destructive-resume reproduction; do not manually repair its pointer or create another bootstrap exception.

First owns the exact 24-path scope: prior 23 plus `factory/scripts/forge_cli/review.py` for task-specific `proof_path` preflight. It supplies C9/C10 complete review/proof, minimal workspace creation, unshipped-operation guards, foreground revocation/cleanup/refusal tests and Claude clear parity. The audit proved successful protected reads and false pending wording; Lean owns `phase.py`'s wording fix. First proves actual admitted-native protected reads and denied unauthorized mutation, with the normal recorder route still usable. Diagnose a real target failure if observed; no speculative read-root repair, snapshot authority or recorder ban.

### Safe installation, retention and client migration

Portable retires only `.codex/agents/planner-high.toml`, `.codex/agents/docs-decomposer.toml` and `.codex/agents/functional-checker.toml`. Delete a regular non-symlink file only when its raw bytes match verifiable harness-owned content at that client's recorded vendoring revision. A familiar name or similarity to today's template is insufficient. Preserve modified, unverifiable and custom copies and report their exact disposition. Omit only those three from new deliveries and obsolete scaffold requirements; preserve logical roles, prompts, producer identities and custom agents. Never recursively delete `.codex/agents`; existing legacy `.agents` migration grants no such permission. Test unchanged removal, modified/unverifiable/custom preservation, leaf/ancestor symlink refusal before any mutation, empty/new destinations and idempotent upgrades.

Retention uses existing decision/event readers, shipped proof and upgrade. Generate the active-decision view on demand. Compact actual IDs into `.factory/stories/<KEY>/events.bundle.json` (scoped) or `.factory/history/<KEY>/events.bundle.json` (legacy), with `format: forge-event-bundle/v1`, exact story and explicit IDs. Validate these fields before reading the new bundle and remove loose sources only after identical content is durable. Preserve distinct IDs and legacy idless JSONL/history unchanged. No heuristic deduplication or sidecar. Preview/apply is idempotent; malformed/colliding/unattributed/open-story events refuse. Keep the existing 0025 untracking allowlist.

Refresh actual HEAD, branch, dirty state and the resolved absolute `git rev-parse --git-common-dir` at each safe story boundary. Deduplicate by that directory, never checkout name. The inventory is historical evidence, not a claim that clients remain clean:

| Common directory | Required outcome |
|---|---|
| `/Users/dev/Workdir/cadence/.git` | One isolated upgrade PR; applied retention or explicit legacy-only no-op; vendor/client checks and CI recorded. |
| `/Users/dev/Workdir/toolshed/.git` | Same independently recorded outcome. |
| `/Users/dev/Workdir/myclaw/.git` | One upgrade for both `myclaw` and `myclaw-cache-bug-cache-bug-T1`; preserve both dirty checkouts, distinct heads, hotfixes and files. Never upgrade them separately. |
| `/Users/dev/Workdir/knacklabs-ats/.git` | One isolated upgrade PR with the same checks and explicit migration outcome. |

Create `feature/forge-lean-upgrade-<client>` and a sibling worktree from the verified current committed head. Do not stash/reset original work or use `--force`. From the shipped harness run `./forge upgrade --target <upgrade-worktree>`, review owned machinery/doc-contract and vendoring-manifest changes, then run the implemented `./forge history --compact --preview` and `--apply` in that worktree. Legacy-only streams produce a recorded no-op. The smallest integrity check is `uv run --python 3.11 python factory/scripts/check_vendor_integrity.py --repo <upgrade-worktree>`; then run that client's normal verifier and meaningful declared quality/type/test commands plus CI. Record applied/no-op/conflict with exact PR, commit and logs. An unsafe or ambiguous client receives a concrete blocker/deferral and next action while independent clients continue; never claim all four migrated with an unresolved row.

Portable captures `./forge findings patterns` before and after work. The historical `reviewed-separately ×3` and `repository-escape ×3` classes already have the accepted 0005/0028 consolidation: `_preflight_upgrade`, checked `_replace_path`/`_keep_path`, and `assert_target_destination`/`assert_target_file_destination`. Audit every changed read/copy/delete against those helpers; retain the raw-write tripwire and leaf/ancestor/malformed-state refusal tests with unchanged external sentinels. Historical aggregation has no resolved flag, so zero old rows is not an acceptance condition. Any new/changed recurring class, unresolved current finding, raw-write violation or escape failure stops affected mutation and uses the existing scope-change/deferral route. Preserve the hard-link/TOCTOU deferral; do not invent another refactor merely to erase historical counts.

## Decisions

Frontmatter attests all 56 active decisions. Accepted 0064 controls the narrower ceremony, standing-authorization, review and retention changes; accepted0065 changes only Linux/Windows platform evidence to CI with disclosed live limitations. Accepted 0011 keeps review with the orchestrator; proposed 0049 is historical context only. Preserve actual authority, admission, measurements and tests under 0018/0029, durable history under 0022/0025/0045, preparation and signal/model/workspace ownership under 0058/0060/0062/0063, except the obsolete cap clause expressly amended by 0064. First and Lean's implementation use real incumbent gates until Lean ships. No fabricated record skips an existing prerequisite.

## Surface Impact

| Surface | Impact and reason |
|---|---|
| Runtime | Changed: native lifecycle/admission; preserve Claude. |
| API | Unchanged by design: no external service/API added. |
| Data/schema | Changed: existing brief/proof metadata and stable-ID event bundle. |
| CLI | Changed: gates, review, phase wording, resume and upgrade. |
| UI | Changed: Shared owns the existing board/owner journey; the separate client has its own UI task. |
| Docs | Changed: canonical procedure and concise AGENTS pointers. |
| Tests | Changed: targeted regressions, mandatory quality, client and required local Mac/Linux/Windows CI evidence. |

Retain Python 3.11, uv/pytest/psutil, Ruff 0.16.6 and Pyright 1.1.411. They fit the existing Python CLI and reuse its current modules and import paths. Follow `constitution/README.md`, the applicable conduct rules in `constitution/09-agent-conduct.md`, exception handling and the shared path-boundary invariant; apply ponytail to each edit. No new technology decision or duplicate abstraction is needed.

## Task Decomposition

These overlapping tasks remain sequential, each with its own scope, tests, proof, PR and real predecessor marker. This table controls harness-task UI ownership; the separate client is described in Verify Plan.

| Label / exact task ID | Complete boundary | Depends on | user_facing |
|---|---|---|---|
| First / NATIVE-FOREGROUND-ACTIVATE | Exact foreground allocation; new C9/C10/review preflight, workspace, guards, cleanup, clear and live boundary proof. | none | false |
| Lean / LEAN-WORKFLOW | Single brief/authorization/design applicability/review operation, complete inputs, phase/workflow ownership, rulings and generated budgets. | NATIVE-FOREGROUND-ACTIVATE | false |
| Native lifecycle / NATIVE-LIFECYCLE | Detached supervisor/request/launch, jobs/status/cancel/resume/explore and process-tree recovery; both original cancel tests. | LEAN-WORKFLOW | false |
| Shared / SHARED-COORDINATOR-JOURNEY | Optional questions/grill hydration, interaction/models, owner/board/queue, safe resume/seals and PR retry/handoff. | NATIVE-LIFECYCLE | true |
| Portable / PORTABLE-DELIVERY-MIGRATION | Setup/init/adopt/upgrade, exact safe retirement, retention and four-client rollout with boundary tripwires. | SHARED-COORDINATOR-JOURNEY | false |
| Format / FORMAT-SOURCES | Full pure mechanical pinned Python formatting and complete equivalence/preservation/test proof. | PORTABLE-DELIVERY-MIGRATION | false |
| Quality / QUALITY-BASELINE | All semantic Ruff/Pyright repairs and mandatory identical local/CI source/test enforcement. | FORMAT-SOURCES | false |
| Integration / FORGE-COORD-1.1 | Integrated AC1–12, required local Mac/CI proof with live-platform limitations and referenced separate-client proof/green CI. | QUALITY-BASELINE | false |

## Risks

An absent or ambiguous task owner must not downgrade task proof to story proof. Preserve owner/base/seal fields on resume; refuse cross-task legacy proof. Hydrate actual grill rounds, not withdrawn plan-mode markers. Missing required runtime/CI evidence and unresolved client migration are proof gaps; unavailable Linux/Windows live observations are explicit accepted0065 limitations. No fixture, historical marker or preparation test substitutes for actual target/platform evidence.

## Verify Plan

Each implementer runs and records the declared regressions and repository verifier. Local, committed-CI and board readers must agree before marker/PR mutation. Main runs the task review/fix loop. Shared's actual UI receives functional proof; other internal harness tasks do not acquire UI scope just because their CLI is visible.

```sh
UV_CACHE_DIR=/tmp/forge-lean-uv-cache UV_TOOL_DIR=/tmp/forge-lean-uv-tools uv run --python 3.11 --with pytest --with psutil python factory/scripts/verify.py
```

### Falsifiable quality activation

Quality owns `requirements-quality.txt` with exactly `ruff==0.16.6` and `pyright==1.1.411`, `ruff.toml`, `pyrightconfig.json`, `factory/scripts/check_python_quality.py`, `verify.py`, `.envrc`, the harness job in `.github/workflows/factory-scaffold.yml`, affected vendoring declarations and focused tests. Retain Pyright's `factory/scripts` import path and explicitly cover all authored Python source and tests. No blanket suppression or test exclusion.

Local verification and the harness CI job run the same command:

```sh
uv run --python 3.11 --with pytest --with psutil --with-requirements requirements-quality.txt python factory/scripts/check_python_quality.py
```

The small runner executes `ruff check .`, `ruff format --check .` and `pyright --project pyrightconfig.json` at the repository root. `.envrc` sets that exact `FACTORY_QUALITY_CMD`; `verify.py` requires it for the source harness. CI installs uv, selects Python 3.11 and invokes the identical command. Tests must demonstrate failure for missing/empty quality configuration, missing pinned requirements/tool/config files, malformed config, and separate deliberate lint, formatting and type defects. A no-op command cannot certify activation. Prove local/CI command equality and retained structural/full-test gates. A vendored-client fixture must select meaningful client-stack quality/type/test commands instead of the harness Python runner; missing or no-op client checks fail. Current optional verification is not credited as AC12 proof.

Portable additionally runs the existing `test_no_raw_write_primitive_outside_the_boundary_helper`, `test_upgrade_refuses_a_symlinked_destination_before_writing` and `test_upgrade_refuses_a_symlinked_ancestor_and_leaves_the_target_clean`, plus the retirement, malformed-state and idempotent bundle cases. Source-harness test selectors remain precise; do not broadly skip a client/harness environment.

### Separate UI and platform evidence

Main creates the fresh `/tmp` Task tracker client with its own private origin, meaningful CI and recorded story/task lifecycle. The planned client leaf is `TASKTRACKER-1/TASKTRACKER-1.1`, explicitly `user_facing: true`; its implementer owns code/automated proof and its functional-checker owns real UI functional proof with required skills. The client owns `tests.json`, `verify.json`, `reviews/` and its task PR/CI. Integration remains `user_facing: false` and consumes exact client repository, commits, PR, artifact paths and logs in its own automated report. It cannot copy client authority or credit client code as a harness contribution.

Integration uses the existing automated schema/recorder with `generated_by: implementer` and existing `status`, `summary`, `commands_run`, `pass_fail_summary`, `remaining_gaps`, `blocking_findings`. No new matrix or schema properties. Keep each of the six labels exactly once: native-cli-macos, native-desktop-macos, native-cli-linux-ubuntu-24.04-x64, native-desktop-linux-ubuntu-24.04-x64, native-cli-windows, native-desktop-windows.

Accepted0065 requires actual local Mac CLI/Desktop observations and meaningful Ubuntu24.04 x64/native Windows CI regressions plus explicitly pinned real CLI package/version/help smoke. Each row states passed/failed/unobserved, evidence kind, exact tested revision, OS/CPU/build, real commands/interactions and durable logs. Linux/Windows CLI-labelled CI rows explicitly state that unavailable authenticated runtime behavior is unobserved; the two unavailable Desktop rows stay unobserved. Accepted limitations remain in remaining_gaps; actual failures and missing required evidence appear in both gaps and blockers. Aggregate status passes only when the four required rows, other task checks and client proof pass with no blocker. Never claim live Desktop from CLI/CI, nor native Windows from WSL. Observe the required real Mac hooks, protected write boundary, admitted contribution and terminal outcome, plus supported optional questions or the permitted main-chat route. QUALITY-BASELINE implements these OS CI jobs in its existing owned workflow, retaining existing full-suite and Windows gates; Integration consumes the actual logs. Preserve Claude regressions.

For the accepted review-only draft checkpoint, Shared implements and Integration exercises verified origin/head-repository/head-branch/base/reviewed-commit matching. Use normal Git/gh draft operations while required platform results are missing, never forge task pr-ready. Uncertain or ambiguous lookup stops creation; an uncertain create is re-queried before retry. Reuse one PR and preserve the eventual marker identity/timestamp. The specification carries the full checkpoint contract.

Close only after all eight task markers reach trunk, all 12 criteria and activated quality pass, required local Mac/Linux/Windows CI proof passes with live-platform limitations stated, required client proof/CI is green, migration outcomes are honest and the existing story outcome is recorded. Closeout adds no second story review.
