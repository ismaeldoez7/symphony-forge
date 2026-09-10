---
issue: FORGE-COORD-1
title: Either Claude or Codex coordinates the same Forge workflow
status: approved
saved: 2026-09-10T20:54:03+00:00
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
  - 0063-first-native-task-workspace-bootstrap
  - 0064-lean-delivery-and-durable-history
  - 0065-ci-platform-evidence
  - 0066-sol-specialized-workflow-models
---

# Symphony Forge: lean delivery

Draft revised against the completed independent requirements and plan reads. Accepted Decision 0064 authorizes the simpler workflow and retention; the confirmed specification plus the bound client inventory authorize the exact four-client migration set. Existing recording and admission gates still apply. The specification is confirmed at SHA256 `439cfc38c4939fdf3e7e62e2ac07aa413cb3954920fca2fb151d8ebe71c8b970`. Main publishes the exact planning inputs below before plan approval.

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

| Parity label | Existing owners | Concrete closing evidence and source |
|---|---|---|
| C1 setup selection/refusal | Portable, Integration | `factory/scripts/forge_cli/scaffold.py`, `doctor.py`, `forge.py`; setup/native fixtures in `factory/tests/test_native_setup.py` and `test_gates.py`; final clean client install and platform logs. |
| C2 exact question/answer identity | Shared, Integration | `factory/scripts/post_tool_use.py`, `record_grill_from_json.py`, `factory/schemas/grill-round.json`, `factory/tests/test_native_questions.py`; actual eligible/consumed event identities and refusal cases. |
| C3 complete adapter hook registration | First, Native lifecycle, Shared, Portable, Integration | `.codex/hooks.json`, `.claude/settings.json`, `factory/scripts/check_dual_runtime.py`, installed hook sources, setup/omission regressions, and final local Mac/client observations. |
| C4 truthful process-bound lifecycle | First, Native lifecycle, Integration | `factory/scripts/forge_cli/codex_runtime.py`, `delegate.py`, `worker_admission.py`, `stages.py`; `test_native_launch.py`, `test_worker_admission.py`; actual launch/terminal/lock/revocation logs. |
| C5 native assets and 15-agent distribution | First, Portable, Integration | `.codex/config.toml`, `.codex/explore.config.toml`, all `.codex/agents/*.toml`, init/upgrade and vendor-integrity paths; exact fresh/adopt/upgrade preservation tests and client migration logs. |
| C6 grounded cold-reader context without new authority | Lean, Shared, Integration | `factory/scripts/forge_cli/grill.py`, `grill_gates.py`, `record_grill_from_json.py`, current brief/phase readers; actual ledgered gate launches, exact input digests, reread/refusal and no-forced-question cases. |
| C7 approved task lifecycle and handoff | First, Native lifecycle, Shared, Integration | Protected task plan/grill/approval, delegation, task-owned verify/tests/reviews/conditional functional proof, board/owner state, completed-boundary handoff, and active/incomplete refusal regressions. |
| C8 genuine native contribution and required platform proof | First, Quality, Integration | Current-plan admitted First contribution and C8 receipt; task verify/review/PR/CI; Quality-owned Ubuntu/native-Windows jobs; Integration's four required passing rows plus explicit unavailable live limitations. |
| C9 complete task-specific review input | First, Lean, Integration | `factory/scripts/forge_cli/review_brief.py`, `review.py`, task-owned automated report and approved plan; focused complete-input/staleness/task-identity regressions and final bound review artifacts. |
| C10 shared proof/readiness and historical fallback | First, Lean, Shared, Integration | `factory/scripts/factory_lib.py`, `check_task_proof.py`, `plans.py`, `tasks.py`, board consumers; task proof/refusal/zero-mutation, metadata-save freshness, conditional functional, whole-bundle legacy and local/CI agreement tests. |

No roadmap-field edit is needed. Criterion 1 already owns worker policy and every gate, including the exact design-review predicate and Decision0066 registry. Criterion 3 owns the delivery chain, and accepted0064 explicitly amends it with exact event compaction and four-client migration. The AC1–AC12 table, roadmap table, and C1–C10 table together are the required closure crosswalk. The ten retained client failures keep their explicit owner/source/acceptance rows in the bound ownership graph. The platform contract and separate dogfood client close through AC6–AC8, C8, and roadmap criterion 3. An obligation absent from those bound rows cannot silently become a shipping blocker.

The graph retains the exact three roadmap strings, original 39-row mapping, ten client-failure owners, task-level `user_facing` values and complete preparation allocation. Its digest below binds those details to this plan; changing ownership afterward requires the existing contract amendment route.

## Technical Approach

### One brief and proportionate scrutiny

Use the existing task plan as the current brief: behavior, boundaries, owner, checks and rulings. Keep story/specification intent and client sign-off; derive execution and review inputs from existing records. Main presents a real new decision with its recommendation, tradeoff, consequence and concrete artifact. Carry actual standing authorization through in-scope corrections and retries using existing approval commands. Lean records the correction/reason/technical classification/authority in the current brief, saves the new digest so stale approval drops, then fresh-binds the concrete revision with actual developer identity/time without claiming a new answer or reread. Material intent, scope, permission, migration, security, lifecycle, ownership or missing authority still requires display and explicit approval. Accepted0064 narrows 0057's pause-all wording: an unanswered required question pauses the addressed task/artifact and every causally affected contract; separately owned dependency-ready unaffected work continues, while missing/canceled answers grant no authority. Lean also adds optional explicit `--context-file`: the authorized caller selects one inside/outside regular UTF-8 file, read once as complete untrusted supplemental context that cannot alter primary artifact/gate/task identity or authority; missing/non-regular/non-UTF8 input refuses, with no search, reopen, repo-only root, truncation or new arbitrary cap. After Shared ships, each new question binds runtime/session/event/tool-call/question/story/gate/task plus exact content at issuance; one multi-question call creates one independently single-use round per unique question ID with exactly one answer, and legacy missing tuples are never synthesized or rebound. Reuse brief/contract/ruling recorders, not a new ledger.

Lean makes `design_review: required|routine` and nonblank `design_review_rationale` explicit in the existing approval-bound brief/frontmatter. Missing/unknown/blank means required. Required is mechanical for a changed actor/write/read/sandbox/credential/network boundary; deletion, overwrite, move, external side effect or other non-reversible operation; stored-data schema/migration; public CLI/API/evidence schema; lifecycle state machine; or ownership boundary. A routine rationale must state that none of those exact triggers changes; the grill checks the artifact and refuses a false downgrade. Signoff is always required, so the legacy BRIEF needs no classification frontmatter. Epics is required when any referenced capability is required or missing classification. One genuine assessment may cover several applicable existing gates only when it explicitly reviewed every complete input and each record remains independently bound to its own artifact. This does not permit copied passes. The confirmed specification names each gate's exact classification input, record and digest. Shared reads must explicitly assess each complete input; current one-gate launches cannot certify other gates. Classification and rationale remain authored digest-bound content, not excluded managed metadata. Incumbent prerequisites remain until Lean ships.

### Review and measurable cleanup boundaries

Main runs one `./forge review <task-id>` operation per task and loops fixes/review until clean. Accepted 0053, 0054 and 0064 establish the interchangeable-coordinator, task-proof and review contracts; accepted 0011 keeps the invocation with the orchestrator. Proposed 0049 supplies no authority. First uses the current three-lens runner inside that operation. Lean changes the implementation to a combined operation with explicit quality, performance and security assessments. Preserve the three existing `reviews/{quality,performance,security}.json` artifacts, all linked by `review_run_id`, `brief_sha256` and `branch_diff_digest` for the same task. Every supplied chunk and every actual assessment must finish successfully. No unassessed lens may inherit a copied pass; no nested or second story-wide review.

One `./forge review <task-id>` invocation is one logical review operation. It invokes the installed autoreview helper once with a combined prompt that requires separately tagged quality, performance and security assessments; supported internal chunks do not become separate Forge reviews. The exact validated helper JSON result retains the ordered chunk results and is the source for three genuine task-owned lens projections. A JSON file may exist after helper exit 2; `review_status: incomplete`, a missing/non-contiguous pass, or a missing lens refuses publication regardless of file existence. Forge writes the raw result and all three schema-valid projections as unique candidates in the existing task review family, validates and reads back their complete input/helper/run/diff/product bindings, then atomically publishes the existing `review-run.json` pointer last. Readiness and seal consume only the complete candidate set named and hashed by that pointer. An interrupted, missing, malformed, copied-lens or mixed-binding attempt cannot publish or replace the last complete pointer; a preserved pointer whose branch diff or classified product changed remains stale and cannot pass. Legacy fixed three-lens proof remains readable as one complete legacy set. No parallel manifest, review registry, reconstructed private chunk manifest or hostile-worker containment is introduced.

The reconciled specification removes the old 120,000-byte product and 180,000-byte review caps under accepted 0064, including the obsolete 0058 clause. The prior spec provenance is exact: normal save produced the draft input, the SOURCE recorder accepted a zero-question frontier under accepted0064, and normal confirmation changed only the status field. The corrected revision must complete that same normal save, grill and confirmation sequence before this plan is saved. The current resolved autoreview helper has no implicit patch-size cap and supports lossless partitions; its observed 512,000-byte limit covers each complete rendered prompt, including instructions, evidence and framing. It is a tool safeguard, not a new task-size policy. Use its supported evidence batching when the fixed preamble would leave insufficient room; never trim authoritative input or change its limit.

Format measures the actual pinned formatter output after Portable ships. Quality measures the actual remaining diagnostics and repair diff after Format ships. Each JIT records exact files, changed lines, total input bytes and rendered partition sizes, then binds positive file/line budgets to that complete scope. Recheck before review and seal. Stop if the actual scope exceeds those budgets, any full prompt cannot be partitioned within the installed limit, any input/chunk is missing or failed, or Format introduces semantic changes. Use the existing amendment route; split only a genuinely independent behavior/proof boundary after a material contradiction. Bytes or chunk count alone do not create new tasks. Format retains exact reproduction, AST and comment/directive preservation, full tests and reviewed exceptions. Generated SQL, snapshots and journals remain counted and reviewed for semantics and security.

### Reproducible preparation and first worker

Main publishes these exact bytes under `plans/exploration/coordinator-parity-preparation/` before approving this plan:

| Artifact | SHA256 | Purpose |
|---|---|---|
| `lean-delivery-graph.json` | `a476fa5cee0ca2c3f6d465349a28448ef389339499c0b1eb2c591c94c8e518a9` | AC/roadmap/owner crosswalk plus the explicit new model-policy allocation annex plus `prepared_hunk_owners`: all 40 original paths and 201 hunk identities, hashes and allocations. |
| `native-original-40-path.patch` | `09cd2ec4826e407541cc4fe75d6d604f9ce6b8bb9f1c8b734aef23e2e42ad54f` | Exact 342,596-byte original donor history; distinct from older `original-bootstrap.patch`. |
| `native-foreground-preparation.patch` | `bee122bb370177ededefb5fe81a82f8c600f69af8502e151956ec7b8afed29e2` | Exact 109,953-byte, 16-path first import against `824baed4a657a83a6a7583e85ee67d2907e7c172`. |
| `native-foreground-preparation-inventory.json` | `3874bb1a3e698c340c19b419d22cad897d12c80d2314bd4b5142d5c3656fa48f` | Existing per-path source/trunk/prepared hashes and first selection. |
| `client-ledger-migration-inventory.json` | `58ceca629e89aa1a213451f1c9fbe6e6ce27d91492a658c538dc4190ce4c8e05` | Dated five-checkout snapshot, deduplicated into four common directories. |

The graph has no reverse plan hash, avoiding a circular binding. Its hunk mapping inherits each path's remainder owner unless an explicit hunk override differs. Exact foreground-selected material belongs only to First; the remainder belongs to its named successor. Archived superseded bytes require an explicit equivalent/corrected/retired disposition in that owner's complete review. Nothing is silently dropped or credited twice. There is no second mapping registry.

Preserved S `/Users/dev/Workdir/symphony-forge-native-dogfood` drives the existing 0063 source ceremony. Existing task start creates real T from fetched trunk; validate any newer baseline before import. Import only the bound foreground allocation, then freshly ground and bind T before stage start and registered admission. Source proof cannot certify T. C `/Users/dev/Workdir/symphony-forge-lean` remains the captured destructive-resume reproduction; do not manually repair its pointer or create another bootstrap exception.

First owns an amended 64-path scope: the original 24; three already authorized technical amendments; two selector fixtures; Decisions 0062/0066; the versioned ownership graph; and 32 additional active specification, profile, guidance, agent and distribution paths listed in the amended graph. This is an additional user-requested model-policy overlay; all original 40 prepared path/hunk owners remain unchanged. It supplies C9/C10 complete review/proof, minimal workspace creation, unshipped-operation guards, foreground revocation/cleanup/refusal tests, Claude clear parity, and the complete current Decision0066 execution policy. The audit proved successful protected reads and false pending wording; Lean owns `phase.py`'s wording fix. First proves actual admitted-native protected reads and denied unauthorized mutation, with the normal recorder route still usable. Diagnose a real target failure if observed; no speculative read-root repair, snapshot authority or recorder ban.

C10 historical fallback is the whole bundle selected by an existing legitimate committed task marker naming task, branch, base and seal commit; it never mixes individual files or reads the current story singleton. Matching task plan/grill/approval, artifact task identity, base-to-seal recorder ancestry, coherent review bindings and unchanged classified product content are mandatory. Any partial modern bundle disables fallback. Pre-marker local seal cannot use it; already sealed committed markers remain eligible for pre-merge CI, and merged/reconciled markers retain their existing treatment.

Admission uses the resolved target worktree, Git directory and common directory as identity. The existing protected `git_control_dir(target)/run.json` is published last as owner record after complete Git registration and hydration validation; all stage, delegation, lock, revocation and run records must resolve from that exact target control location. First enforces the foreground boundary. Shared owns attachment, atomic owner publication and recovery; Native later extends admission to background launches. Cancellation uses the durable revocation marker before cleanup. Success/failure revoke through protected terminal state, dead process and released matching lock; stage close revokes by leaving the active stage incarnation. No new owner ledger, duplicate location fields or completion tombstone is added.

### Current model-policy amendment

Accepted Decision0066 and the user's explicit model/team request add new work to First without moving the original preparation allocation. First updates every executable project selector and active guidance surface, commits all 15 project agent definitions, proves the existing init full-tree copy and upgrade same-name refresh while preserving distinct client-added agents, and hardens the same Claude plugin route for Luna/max through an exact-source doctor capability check. No new actor may use Terra. Exploration is Sol/low; planning, decomposition, architecture, plan validation and grills are Sol/high; all implementation, technical test verification and autoreview fixes are Sol/medium except formal Lite at Luna/max; formal autoreview and functional checking are Sol/high.

The old project profiles are currently executable, so they cannot be described as deferred or inactive. First must finish the complete 64-path scope before it ships. The amended graph carries the new-request portion as a separate `model_policy_amendment` annex and leaves every original prepared hunk record unchanged. Lean retains its original workflow simplification and the separately found `pr-link.yml` event-staging fix; Shared no longer owns Remaining0062 model selection, and Portable preserves/distributes the team registry instead of retiring it.

### Safe installation, retention and client migration

Decision0066 explicitly amends only Decision0057's instruction to retire and omit the three project agent definitions; 0057's question requirements remain active as narrowed by accepted0064, and its other roadmap, phase-role and gate requirements remain active. Decision0066 also amends only Decision0065's existing First-scope clause and matching recorded scope lesson for this later explicit model/team overlay; it preserves every original prepared hunk owner, source/target binding, eight-task graph, and all other 0065 duties. First commits and proves all 15 team definitions through existing distribution behavior: init copies the complete tree, upgrade refreshes harness-owned same-name definitions/configs, and distinct client-added agents remain. No new TOML merge or provenance mechanism is required. Portable later exercises that behavior during client rollout with existing safe path handling; it never deletes `.codex/agents` recursively. Existing legacy `.agents` migration grants no deletion authority.

Retention uses existing decision/event readers, shipped proof and upgrade. Generate the active-decision view on demand. Each bundle member is exactly `{"id":"<source filename stem>","payload":<validated original event object>}` sorted by ID; compare ID plus deterministic sorted compact UTF-8 payload. Equal pairs deduplicate, same-ID unequal payload refuses, and distinct IDs remain distinct. Only validated live `.factory/events/<id>.json` with exact shipped identity may mutate: scoped requires matching done roadmap/history pointer, shipped.json and complete task markers/proof; legacy requires its original archived pr-ready run/proof and a task marker only when that run used task-level delivery. Do not invent retroactive markers. Root JSONL and every pre-existing history file remain byte-immutable. Preview prints the exact eligible inventory SHA256; apply requires it through `--expected-digest` and refuses drift before mutation. First publication uses a complete temporary file and atomic no-overwrite. An existing bundle is immutable: retry removes only regular unchanged loose sources whose exact pairs already appear; it never unions/replaces/truncates, and unseen late IDs remain untouched and refuse. Before deletion, re-read source identity/bytes and durable bundle. Keep partial-failure evidence, `format: forge-event-bundle/v1`, exact top-level format/story/events, no sidecar/heuristic, legacy-idless no-op, and the existing 0025 untracking allowlist.

The confirmed specification and `client-ledger-migration-inventory.json` bind the exact four common directories below; accepted0064 governs retention behavior but does not invent the client list. Refresh actual HEAD, branch, dirty state and the resolved absolute `git rev-parse --git-common-dir` at each safe story boundary. Deduplicate by that directory, never checkout name. The inventory is historical evidence, not a claim that clients remain clean:

| Common directory | Required outcome |
|---|---|
| `/Users/dev/Workdir/cadence/.git` | One isolated upgrade PR; applied retention or explicit legacy-only no-op; vendor/client checks and CI recorded. |
| `/Users/dev/Workdir/toolshed/.git` | Same independently recorded outcome. |
| `/Users/dev/Workdir/myclaw/.git` | One upgrade for both `myclaw` and `myclaw-cache-bug-cache-bug-T1`; preserve both dirty checkouts, distinct heads, hotfixes and files. Never upgrade them separately. |
| `/Users/dev/Workdir/knacklabs-ats/.git` | One isolated upgrade PR with the same checks and explicit migration outcome. |

Create `feature/forge-lean-upgrade-<client>` and a sibling worktree from the verified current committed head. Do not stash/reset original work or use `--force`. From the shipped harness run `./forge upgrade --target <upgrade-worktree>`, review owned machinery/doc-contract and vendoring-manifest changes, then run the implemented `./forge history --compact --preview` and `--apply` in that worktree. Legacy-only streams produce a recorded no-op. The smallest integrity check is `uv run --python 3.11 python factory/scripts/check_vendor_integrity.py --repo <upgrade-worktree>`; then run that client's normal verifier and meaningful declared quality/type/test commands plus CI. Record applied/no-op/conflict with exact PR, commit and logs. An unsafe or ambiguous client receives a concrete blocker/deferral and next action while independent clients continue; never claim all four migrated with an unresolved row.

Portable captures `./forge findings patterns` before and after work. The historical `reviewed-separately ×3` and `repository-escape ×3` classes already have the accepted 0005/0028 consolidation: `_preflight_upgrade`, checked `_replace_path`/`_keep_path`, and `assert_target_destination`/`assert_target_file_destination`. Audit every changed read/copy/delete against those helpers; retain the raw-write tripwire and leaf/ancestor/malformed-state refusal tests with unchanged external sentinels. Historical aggregation has no resolved flag, so zero old rows is not an acceptance condition. Any new/changed recurring class, unresolved current finding, raw-write violation or escape failure stops affected mutation and uses the existing scope-change/deferral route. Preserve the hard-link/TOCTOU deferral; do not invent another refactor merely to erase historical counts.

Native lifecycle observability follows constitution 05 and 07. Whenever an accepted, starting, running, retrying, cancel-requested, canceled, failed or succeeded transition occurs, it emits one durable structured JSON record with the required timestamp/level/static-message/context/environment/service/module/correlation/account fields and request/event IDs when applicable. Correlation binds story/task/launch/session/process/stage; prompts, tokens, credentials, raw environment values, PII and whole request objects are redacted. Existing retries remain bounded and idempotent and retain prior failures; cancellation records revocation before signals and reaches one truthful terminal result; unexpected terminal failures surface stable error IDs/internal codes with sanitized messages and are never swallowed. Native lifecycle focused tests prove fields, correlation, redaction, retry/cancel ordering, terminal uniqueness and failure propagation. Integration cites those native logs plus separately produced Mac CLI/Desktop and Task tracker interaction logs; one source cannot certify another.

## Decisions

Frontmatter attests all 56 active decisions. Accepted0053 is the targeted amendment to the BRIEF's Claude-only coordinator wording; accepted0047/0059 replace its one-story-worktree/sequential-task literals, with Shared owning later BRIEF wording alignment. Accepted0064 controls the narrower ceremony, standing authorization, review and retention changes; accepted0065 requires completed platform results and a freshly generated complete review brief before formal review/readiness. Accepted0011 keeps review with the orchestrator; proposed0049 is historical context only. Preserve actual authority, admission, measurements and tests under 0018/0029, durable history under 0022/0025/0045, preparation, signal and workspace ownership under 0058/0060/0063, with model ownership replaced by accepted0066 and the obsolete cap clause amended by0064. First and Lean's implementation use real incumbent gates until Lean ships. No fabricated record skips an existing prerequisite.

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
| First / NATIVE-FOREGROUND-ACTIVATE | Exact foreground allocation plus the additional Decision0066 current model-policy overlay; C9/C10/review preflight, workspace, guards, cleanup, clear and live boundary proof. | none | false |
| Lean / LEAN-WORKFLOW | Single brief/authorization/design applicability/review operation, complete inputs, phase/workflow ownership, rulings and generated budgets. | NATIVE-FOREGROUND-ACTIVATE | false |
| Native lifecycle / NATIVE-LIFECYCLE | Detached supervisor/request/launch, jobs/status/cancel/resume/explore and process-tree recovery; structured correlated/redacted lifecycle logs, bounded retry, truthful cancel/terminal errors; both original cancel tests. | LEAN-WORKFLOW | false |
| Shared / SHARED-COORDINATOR-JOURNEY | Optional questions/grill hydration, interaction under First-owned Decision0066, owner/board/queue, safe resume/seals and PR retry/handoff. | NATIVE-LIFECYCLE | true |
| Portable / PORTABLE-DELIVERY-MIGRATION | Client setup/adopt/upgrade rollout preserving the First-owned project agent registry, retention and four-client boundary tripwires. | SHARED-COORDINATOR-JOURNEY | false |
| Format / FORMAT-SOURCES | Full pure mechanical pinned Python formatting and complete equivalence/preservation/test proof. | PORTABLE-DELIVERY-MIGRATION | false |
| Quality / QUALITY-BASELINE | All semantic Ruff/Pyright repairs and mandatory identical local/CI source/test enforcement. | FORMAT-SOURCES | false |
| Integration / FORGE-COORD-1.1 | Integrated AC1–12, required local Mac/CI proof with live-platform limitations and referenced separate-client marker, review, functional proof and green CI. | QUALITY-BASELINE | false |

## Risks

An absent or ambiguous task owner must not downgrade task proof to story proof. Preserve owner/base/seal fields on resume; refuse cross-task legacy proof. Hydrate actual grill rounds, not withdrawn plan-mode markers. Missing required runtime/CI evidence and unresolved client migration are proof gaps; unavailable Linux/Windows live observations are explicit accepted0065 limitations. No fixture, historical marker or preparation test substitutes for actual target/platform evidence.

## Verify Plan

Each implementer runs and records the declared regressions and repository verifier. Local, committed-CI and board readers must agree before marker/PR mutation. Main runs the task review/fix loop. Shared's actual UI receives functional proof; other internal harness tasks do not acquire UI scope just because their CLI is visible.

```sh
UV_CACHE_DIR=/tmp/forge-lean-uv-cache UV_TOOL_DIR=/tmp/forge-lean-uv-tools uv run --python 3.11 --with pytest --with psutil python factory/scripts/verify.py
```

### Falsifiable quality activation

Quality owns `requirements-quality.txt` with exactly `ruff==0.16.6` and `pyright==1.1.411`, `ruff.toml`, `pyrightconfig.json`, `factory/scripts/check_python_quality.py`, `verify.py`, `.envrc`, the harness job in `.github/workflows/factory-scaffold.yml`, affected vendoring declarations and focused tests. Retain Pyright's `factory/scripts` import path. Harness coverage is exactly every tracked `*.py` below `factory/scripts/` and `factory/tests/`, including tracked fixtures in those roots; generated or client-owned Python outside those roots is excluded and uses its owning client's declared stack checks. No blanket suppression or test exclusion.

Local verification and the harness CI job run the same command:

```sh
uv run --python 3.11 --with pytest --with psutil --with-requirements requirements-quality.txt python factory/scripts/check_python_quality.py
```

The small runner derives that tracked file set and passes the same explicit set to Ruff check, Ruff format check and Pyright locally and in CI. `.envrc` sets the exact command above as `FACTORY_QUALITY_CMD`; `verify.py` requires it for the source harness. CI installs uv, selects Python 3.11 and invokes the identical command. Tests must demonstrate failure for missing/empty quality configuration, a missing covered path, missing pinned requirements/tool/config files, malformed config, and separate deliberate lint, formatting and type defects. A no-op command cannot certify activation. Prove local/CI command equality and retained structural/full-test gates. A vendored-client fixture must select meaningful client-stack quality/type/test commands instead of the harness Python runner; missing or no-op client checks fail. Current optional verification is not credited as AC12 proof.

Portable additionally runs the existing `test_no_raw_write_primitive_outside_the_boundary_helper`, `test_upgrade_refuses_a_symlinked_destination_before_writing` and `test_upgrade_refuses_a_symlinked_ancestor_and_leaves_the_target_clean`, plus the existing agent-distribution, malformed-state and idempotent bundle cases. Source-harness test selectors remain precise; do not broadly skip a client/harness environment.

### Separate UI and platform evidence

The user's approved dogfood exception authorizes Main, only after the Quality task marker reaches trunk, to create one fresh `/tmp` Task tracker client, one private origin through the existing authenticated Git/GitHub route, and its CI solely as acceptance proof for this story. It creates no hosted application, deployment or reusable client-CI machinery. The planned client leaf is `TASKTRACKER-1/TASKTRACKER-1.1`, explicitly `user_facing: true`; its implementer owns code/automated proof and its functional-checker owns real UI functional proof with required skills. Acceptance proves a clean harness install followed by the client's declared lint, type, build and test commands, then recorded create/list/complete persistence through the UI and storage path. The client owns `tests.json`, `verify.json`, `reviews/` and its task PR/CI. Integration remains `user_facing: false` and refuses until the exact client task marker, reviewed PR, green CI and functional proof match the cited client repository/commit. It consumes exact client repository, commits, PR, artifact paths and logs in its own automated report. It cannot copy client authority or credit client code as a harness contribution; the separate lifecycle adds no ninth harness task or fake cross-repository task ID.

Integration uses the existing automated schema/recorder with `generated_by: implementer` and existing `status`, `summary`, `commands_run`, `pass_fail_summary`, `remaining_gaps`, and `blocking_findings`. Encode `pass_fail_summary` as a JSON array string with exactly the six labels in declared order. Every row has exactly `label`, `status`, `evidence_kind`, `os`, `cpu`, `revision`, `runtime`, `commands`, and `logs`; status is passed/failed/unobserved, unavailable runtime is null with an explicit remaining-gap explanation, and commands/logs are arrays. The Integration-owned validator uses `json.loads`, rejects malformed/duplicate/missing/contradictory rows, resolves log references against the tested revision, requires exact client evidence, and derives aggregate status. Independent review checks the same logs. C10 consumes the review-bound aggregate rather than parsing this encoding. No schema property, second report, matrix registry, or second authority is added.

Accepted0065 requires actual local Mac CLI/Desktop observations and meaningful Ubuntu24.04 x64/native Windows CI regressions plus exact `@openai/codex@0.153.4` package/version/help smoke. Each row states passed/failed/unobserved, evidence kind, exact tested revision, OS/CPU/build, real commands/interactions and durable logs. Linux/Windows CLI-labelled CI rows explicitly state that unavailable authenticated runtime behavior is unobserved; the two unavailable Desktop rows stay unobserved. Accepted limitations remain in remaining_gaps; actual failures and missing required evidence appear in both gaps and blockers. Aggregate status passes only when the four required rows, other task checks and client proof pass with no blocker. Never claim live Desktop from CLI/CI, nor native Windows from WSL. Observe the required real Mac hooks, protected write boundary, admitted contribution and terminal outcome, plus supported optional questions or the permitted main-chat route. QUALITY-BASELINE implements these OS CI jobs in its existing owned workflow, retaining existing full-suite and Windows gates; Integration consumes the actual logs. Preserve Claude regressions.

After normal contribution and deterministic verification, run one preliminary independent inspection through the installed autoreview helper. While required platform results are missing, the sole durable checkpoint is a machine-readable `forge-preliminary-inspection/v1` block in the existing GitHub draft PR body; it records the verified origin/head-repository/head-branch/base/current-remote-head tuple, inspected commit, exact inspected branch-diff digest, classified-product digest, helper identity, exact raw helper result (inline or by path, containing commit, byte count and SHA256 to an immutable candidate under the existing diagnostic review-brief family), findings, missing required platform rows and accepted unobserved limitations. Exactly one matching open draft is reused; zero permits one create; multiple, mismatched, failed or uncertain lookups refuse, and an uncertain create is re-queried before retry. Later workflow/proof-only commits may advance the head when the inspected commit remains its ancestor and classified product content is unchanged; whole-HEAD and recorder-commit equality are not required, and any product change requires a fresh preliminary inspection. This checkpoint records no clean Forge proof, creates no task marker and never runs `forge task pr-ready`. After the required platform report passes, generate a fresh complete brief, run the normal formal Forge review, then reuse and promote the same PR through normal readiness while preserving the eventual marker identity and timestamp. The PR body is the only checkpoint authority; scratchpads and candidate payloads are diagnostic, and no new registry or proof family is introduced. Shared implements lookup, reuse and promotion; Integration exercises the actual checkpoint and post-platform formal review.

Close only after all eight task markers reach trunk, all 12 criteria and activated quality pass, required local Mac/Linux/Windows CI proof passes with live-platform limitations stated, required client proof/CI is green, migration outcomes are honest and the existing story outcome is recorded. Closeout adds no second story review.
