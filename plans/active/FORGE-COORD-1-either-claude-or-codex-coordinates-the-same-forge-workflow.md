---
issue: FORGE-COORD-1
title: Either Claude or Codex coordinates the same Forge workflow
status: approved
saved: 2026-09-11T22:35:17+00:00
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
  - 0066-closeout-binds-to-the-diff
  - 0067-combined-review-generation
  - 0068-sol-specialized-workflow-models
  - 0069-empty-frontier-grill-proof
  - 0070-staged-platform-proof
---

# Symphony Forge: lean delivery

Draft revised against the independent requirements and plan reads. Decisions 0064, 0066, 0067, 0069 and 0070 authorize the simpler workflow, diff-bound closeout, one-generation review, empty-frontier proof and executable platform sequence; the user's prior explicit one-time approval authorizes branch, push, and PR work for the exact client migration set. Existing recording and admission gates still apply. The corrected specification is confirmed, and the user approved all amended story and task plans on 2026-09-12; each approval is bound only after its exact grill-clean digest is saved.

## Problem

Repeated plans, approvals and review launches slow delivery and lose settled answers. The developer should decide once when necessary, then let authorized work continue through tests, review, PR and green CI. Fresh workers and reviewers must receive the same ruling. Overnight work returns a compact account of completed PRs, real blockers and decisions needed.

## Transition before delegation

The current protected plan, decomposition and First task plan remain in force until this amendment completes the normal gates. Main records this single fresh plan read after resolving every finding, saves the exact amended plan, binds the user's 2026-09-12 approval, records the matching eight-task decomposition, then saves, grills and binds that same standing approval to the corrected First task plan. Only then may the First stage start and delegate D-0032. Deferral D-0032 is resolved and its stale lesson is corrected before any worker receives the new contract.

## Validated main baseline

The task branch includes merge commit `db03a5708ca292d0e7e918d385748eb5b60008e5`, whose second parent is validated `origin/main` commit `c9a705bc315d4677309815eb03b58e61e7957e50`. That baseline already supplies Decision 0066's `delta_id` and resumable `forge task close`, rendered task-contract blocks with stable plan digests, task-aware proof readers, the current three-helper lens runner with concurrent execution, and the related board and CI readers. The merge keeps complete task-owned automated and conditional functional proof ahead of stage closure, preserves marker-only sealing, and validates native launches against their recorded scope. Its parallel-review regression and story-proof fallback regression describe the incumbent runtime; First must rewrite both when it replaces those behaviours.

Those inherited bytes and behaviours are baseline, not a contribution of `NATIVE-FOREGROUND-ACTIVATE`. The current three concurrent helpers remain the interim review runtime. First still owns Decision 0067's replacement: one helper call, one immutable raw-plus-three-lens generation, and one selected pointer. First reuses the inherited closeout, proof, board, and CI seams rather than reimplementing them.

## Scope / Non-goals

Keep the complete native and Claude coordinator outcome, original preparation, all Python quality work, required local Mac and Linux/Windows CI proof with unavailable live-platform limitations, separate installed-client dogfood and all ten audited client failures. Replace the unapproved 39-task graph with eight coherent tasks. Preserve unrelated work, client configuration and MyClaw hotfixes. No fabricated approval/proof, manual protected-state repair, new coordinator or ruling ledger, blanket generated-file exclusion, or additional review ceremony.

## Acceptance Criteria

The owner labels refer to the exact task IDs in Task Decomposition. Each owner supplies its own task-bound evidence; Integration must verify the complete outcome.

| Spec criterion | Owners | Required evidence |
|---|---|---|
| AC1: real human answers | First, Shared, Integration | Host-permitted main decisions; structured rounds bind runtime/session/event/question index, exact scope/input/content/answer; replay, cancellation and malformed answers refuse. |
| AC2: protected writes | First, Native lifecycle, Integration | Denied coordinator/unregistered writes, admitted bounded contribution and stale/revoked authority refusal. |
| AC3: native independence | First, Native lifecycle, Portable, Integration | Launch/status/recovery/setup without Claude dependencies; existing Claude route and Decision 0060 signal-mask behavior pass. |
| AC4: workers and gates | First, Lean, Native lifecycle, Shared | Shared model/effort policy and the same approval/admission/test/review/PR proof for both coordinators. |
| AC5: hook delivery | First, Native lifecycle, Shared, Portable, Integration | Exact committed hook/tool matrix and real blocking capability; focused tests plus automated logs prove success/failure, sanitized error, metric, trace, and refusal behavior. |
| AC6: honest evidence | First, Lean, Integration | Preparation and diagnostics stay labelled; only current task-bound recorder proof passes; required platform rows use actual logs and evidence kind. |
| AC7: genuine native task | First, Integration | One qualifying hunk in the existing task branch diff correlates with admitted write, terminal evidence, criterion/finding, verification, review, PR, and CI; prepared bytes earn no contribution. |
| AC8: setup and preservation | Portable | Setup/doctor choose per invocation; init/adopt/upgrade preserve both adapters plus client ownership/history; review migration and late-event refusal are proved. |
| AC9: continuation and context | Lean, Shared | Settled rulings survive fresh workers; authorized work resumes without repeated prompts; optional unanswered questions do not block it. |
| AC10: coordinator change | Shared, Integration | Change only between completed tasks after the old session stops, marker and green CI reach refreshed trunk, and no worker or synchronous question call remains active; the new session resumes through `forge next`. |
| AC11: developer journey | First, Lean, Shared, Integration | Real source/target binding, workspace-first task ownership, safe attach/retry/reconciliation, empty-dependency fallback, and board functional proof. |
| AC12: full quality and platform proof | Format, Quality, Portable, Integration | Pinned full source/test lint, format and types; required Mac and Linux/Windows evidence; dogfood and authorized rollout proof; missing or failed required evidence blocks. |

| Roadmap criterion | Owners and closing proof |
|---|---|
| 1. Both coordinators preserve existing worker policy and every Forge gate. | First/Lean/Native lifecycle/Shared; Integration closes policy parity, identity-bound proof and the real lifecycle. |
| 2. Codex records real human grill provenance and runs without Claude or plugin state. | First/Shared/Native lifecycle/Portable; Integration closes actual permitted answers/events and native-only launch/setup with required local Mac/CI proof and honest live-platform limitations. |
| 3. Approved bounded bootstrap, registered contributions, predecessor markers, complete review, mandatory quality and final parity chain. | All eight tasks: exact preparation inputs, actual contribution/proof/PRs, sequential trunk markers, complete quality, separate client lifecycle and required local Mac/CI proof with honest live-platform limitations. “Existing review limits” means the installed safeguards under accepted 0064, not the superseded byte caps. |

| Parity label | Existing owners | Concrete closing evidence and source |
|---|---|---|
| C1 setup selection/refusal | Portable, Integration | `./setup` and `forge doctor` select for one invocation; init/adopt/upgrade install both adapters; focused refusal/preservation tests and client logs pass. |
| C2 exact question/answer identity | Shared, Integration | Existing question recorder/schema plus focused tests prove runtime/session/event/index identity, exact scope/input/content/answer, eligibility, and single use. |
| C3 complete adapter hook registration | First, Native lifecycle, Shared, Portable, Integration | `.codex/hooks.json`, `.claude/settings.json`, `factory/scripts/check_dual_runtime.py`, installed hook sources, setup/omission regressions, and final local Mac/client observations. |
| C4 truthful process-bound lifecycle | First, Native lifecycle, Integration | Existing launch/admission paths and focused tests prove launch, signal mask, terminal/revocation truth, sanitized structured errors, one bounded metric increment, and trace correlation. |
| C5 native assets and 15-agent distribution | First, Portable, Integration | `.codex/config.toml`, `.codex/explore.config.toml`, all `.codex/agents/*.toml`, init/upgrade and vendor-integrity paths; exact fresh/adopt/upgrade preservation tests and client migration logs. |
| C6 grounded cold-reader context without new authority | Lean, Shared, Integration | `factory/scripts/forge_cli/grill.py`, `grill_gates.py`, `record_grill_from_json.py`, current brief/phase readers; actual ledgered gate launches, exact input digests, reread/refusal and no-forced-question cases. |
| C7 approved task lifecycle and coordinator change | First, Native lifecycle, Shared, Integration | Protected task ownership through green CI, conditional functional proof, board state, workspace-first attach, and between-task change/refusal regressions. |
| C8 genuine native contribution and required platform proof | First, Quality, Integration | Qualifying task branch-diff hunk tied to a criterion/finding and assessed by selected review; task PR/CI, required local Mac evidence, required Ubuntu/native-Windows jobs, and honest live limitations. |
| C9 complete task-specific review input | First, Lean, Integration | `factory/scripts/forge_cli/review_brief.py`, `review.py`, task-owned automated report and approved plan; focused complete-input/staleness/task-identity regressions and final bound review artifacts. |
| C10 shared proof/readiness and task-scoped review selection | First, Lean, Shared, Portable, Integration | `factory/scripts/factory_lib.py`, `check_task_proof.py`, `plans.py`, `tasks.py`, `upgrade.py`, board consumers; task proof/refusal/zero-mutation, metadata-save freshness, conditional functional, selected-set migration and local/CI agreement tests. |

No roadmap-field edit is needed. Criterion 1 already owns worker policy and every gate, including the exact design-review predicate and Decision0068 registry. Criterion 3 owns the delivery chain, and accepted0064 explicitly amends it with exact event compaction and the client migration. The AC1–AC12 table, roadmap table, and C1–C10 table are a closure crosswalk, not authority over the active decision corpus. Every active decision and deterministic gate remains binding even when a table omits it. The ten retained client failures keep their explicit owner/source/acceptance rows in the bound ownership graph. The platform contract and separate dogfood client close through AC6–AC8, C8, and roadmap criterion 3.

The graph retains the exact three roadmap strings, original 39-row mapping, ten client-failure owners, task-level `user_facing` values and complete preparation allocation. Its digest below binds those details to this plan; changing ownership afterward requires the existing contract amendment route.

## Technical Approach

### One brief and proportionate scrutiny

Use the existing task plan as the current brief: behavior, boundaries, owner, checks and rulings. Keep story/specification intent and client sign-off; derive execution and review inputs from existing records. Main presents a real new decision with its recommendation, tradeoff, consequence and concrete artifact. Carry actual standing authorization through in-scope corrections and retries using existing approval commands. Lean records the correction/reason/technical classification/authority in the current brief, saves the new digest so stale approval drops, then fresh-binds the concrete revision with actual developer identity/time without claiming a new answer or reread. Material intent, scope, permission, migration, security, lifecycle, ownership or missing authority still requires display and explicit approval. Accepted0064 narrows 0057's pause-all wording: an unanswered required question pauses the addressed task/artifact and every causally affected contract; separately owned dependency-ready unaffected work continues, while missing/canceled answers grant no authority. This is the user's selected “Wait for all” handoff rule: independent work may continue, but coordinator transfer waits until every required exchange closes or is canceled.

Lean adds optional explicit `--context-file`. Open the selected regular file once without following unsafe links, validate and capture immutable UTF-8 bytes, SHA256 and byte count, then launch only those bytes as untrusted supplemental context. The file cannot alter primary artifact/gate/task identity or authority. Missing/non-regular/non-UTF8 input refuses, with no search, reopen, repo-only root, truncation or arbitrary cap. Limits must be known in UTF-8 bytes. Partition only a consumer with an approved ordered aggregation contract; exact captured bytes are covered once in order, and any missing/reordered/conflicting/failed part invalidates the whole result.

After Shared ships, each successful structured call gets one fresh event ID and zero-based question index. Eligibility binds runtime, session, exact story/gate/task scope, current input digest, requiredness, question, ordered options, and the exact nonblank submitted answer. A free-form answer outside the offered labels is valid and preserved verbatim; choosing a label also preserves that exact label. Each question is consumed once; optional non-gate questions cannot satisfy a gate. If an answer changes an approval-bound artifact, its normal decision or approval records the final revision and the grill covers that revision. No revision-mapping protocol or new ledger is added. Incumbent grill floors remain until Shared ships. Decision0069 then permits zero rounds only for a successful ledgered cold read bound to the exact artifact/gate/task input that explicitly reports an empty human frontier; any question or missing authority retains Decision0051's ledger matching and single-use rules.

A required ordinary-chat question holds its current turn; abandonment grants no authority and a later session asks again. Required structured exchanges use only a synchronous question tool that returns the answer in the same call. An async question tool is optional clarification only and cannot satisfy a gate, approval, or required exchange. A coordinator cannot change while a synchronous question call is executing; after it returns or is canceled, the old coordinator stops, and cancellation grants no authority. Coordinator changes happen only between completed tasks after the marker and green CI are on refreshed trunk and no worker remains. The new coordinator resumes through `forge next`. There is no durable pending-question ledger, live handoff command, snapshot, fencing token, or concurrent coordinator ownership.

Lean makes `design_review: required|routine` and nonblank `design_review_rationale` explicit in the existing approval-bound brief/frontmatter. Missing/unknown/blank means required. Required is mechanical for a changed actor/write/read/sandbox/credential/network boundary; deletion, overwrite, move, external side effect or other non-reversible operation; stored-data schema/migration; public CLI/API/evidence schema; lifecycle state machine; or ownership boundary. A routine rationale must state that none of those exact triggers changes; the grill checks the artifact and refuses a false downgrade. Signoff is always required, so the legacy BRIEF needs no classification frontmatter. Epics is required when any referenced capability is required or missing classification. One genuine assessment may cover several applicable existing gates only when it explicitly reviews every complete input and each gate record remains independently bound to that artifact's own digest. This does not permit copied passes. This approval-bound plan and Lean's rendered task contract are the classification producer; the confirmed capability spec does not claim these fields. Shared reads must explicitly assess each complete input; current one-gate launches cannot certify other gates. Classification and rationale remain authored digest-bound content, not excluded managed metadata. Incumbent prerequisites remain until Lean ships.

### Review and measurable cleanup boundaries

The owner of each task carries that task in its worktree through implementation, review fixes, PR and green CI. The coordinator invokes the review there under accepted 0011; Main schedules the story and owns only the separate story-level client rollout. For the current First task, the active task owner and Main coordinator are the same session. Proposed 0049 supplies no authority. The user explicitly moved complete D-0032 ownership to First because three helper calls cost too much time; Lean consumes it and does not reimplement it.

Each default `./forge review <task-id>` calls the installed helper once. It writes one immutable generation containing the raw result and three genuine lens records, validates and reads it back, then publishes the small task pointer last. `factory/schemas/review-set.json` distinguishes `combined`, citation-based `rejection`, and one-time `upgrade` origins. The lowercase `generation_id` is the SHA256 of canonical sorted compact UTF-8 JSON for every generation field except `generation_id`; `reviews/generations/<generation_id>.json` includes that ID, and every read recomputes it. Every existing ancestor must be a real non-symlink directory, and every existing or newly published leaf must be a regular single-link file. Generation publication uses an exclusive same-directory temporary, complete flush/readback, and atomic hard-link/no-overwrite; an existing byte-identical generation is an idempotent success, while the same ID with unequal bytes refuses as a collision. Blocking generations select and revoke clean status; failure leaves the prior pointer unchanged. Fixed lens paths are never runtime fallback. Remove the inherited `--sequential` option and `FORGE_REVIEW_SEQUENTIAL` branch: one helper has nothing to sequence, and no named consumer justifies a no-op compatibility surface.

Every actual provider pass stores its assessment in `overall_explanation` and uses exact full-line `BEGIN FORGE ASSESSMENT <lens>` and `END FORGE ASSESSMENT <lens>` markers once for each lowercase lens, in quality, performance, and security order. Quality retains the existing contract-verdict syntax. The helper schema's 3,000-character `overall_explanation` maximum is an output-field bound, not prompt capacity; preflight only the required marker/verdict boilerplate against it and reject oversized output. Unchunked output is the top-level report only when `pass_reports` is absent. Chunked output recursively validates and projects each `pass_reports[*].report` with exact `chunk 1/N` through `chunk N/N` labels; the synthesized top-level summary is never treated as a lens assessment. Each finding title starts with exactly one of `[quality] `, `[performance] `, or `[security] `; the helper supplies one integer `line`, so the normalized start and end lines both equal that value. Cross-lens duplicates use the architecture's deterministic path/line/title fingerprint. Only `VERDICT` lines inside each validated quality assessment block count; performance/security blocks and finding bodies never supply a quality verdict. Existing score, recommendation, and worst quality-verdict functions remain. Reuse `product_excluded_prefixes` and `product_delta_digest`; any compatibility field named `branch_diff_digest` stores that exact `delta_id`, so review and closeout have one identity and no product-tree or second diff digest.

A rejected finding creates one immutable successor from the selected `origin=combined` generation, bound to that source generation file SHA256 and ID. It preserves raw output, ordered passes and unaffected lenses, and records the exact finding/reason/citation/actor without claiming a new helper assessment. Rejection, `origin=upgrade`, fixed-only and unrelated sources refuse. The public complete-set recorder accepts only `origin=combined`, rederives its three lens records from raw helper bytes plus authoritative task state, and refuses a mismatch before publication; citation rejection and Portable upgrade use their owned routes into the shared internal publisher. A single-lens run remains diagnostic and cannot publish, stamp, revoke, or otherwise compete with the selected complete generation. `forge task close` may skip review only when the selected clean generation is bound to the same current `delta_id`; a fixed-only, story-level, missing, blocking or stale selection runs or refuses the one-helper review before stage mutation. Decisions0067 and0070 permit one early draft PR only when required platform CI needs it; Main pushes the exact task branch and creates or reuses its matching draft with `gh pr create --draft`, records the PR identity, and grants it no proof, review, readiness, seal, or merge authority.

The reconciled specification removes the old 120,000-byte product and 180,000-byte review caps under accepted 0064, including the obsolete 0058 clause. The corrected revision completes the normal save, one change-scoped grill and confirmation sequence before this plan is saved. The current resolved autoreview helper has no implicit patch-size cap; its observed 512,000-byte limit covers each complete rendered prompt, including instructions, evidence and framing. It is a tool safeguard, not a new task-size policy. Bind one immutable input snapshot before counting or launch. Use supported evidence partitioning only where the helper's ordered aggregation contract preserves every captured byte and invalidates the whole result on a missing, reordered, conflicting or failed part; never trim authoritative input or change its limit.

Format measures the actual pinned formatter output after Portable ships. Quality measures the actual remaining diagnostics and repair diff after Format ships. Each JIT records exact files, changed lines, total input bytes and rendered partition sizes, then binds positive file/line budgets to that complete scope. Recheck before review and seal. Stop if the actual scope exceeds those budgets, any full prompt cannot be partitioned within the installed limit, any input/chunk is missing or failed, or Format introduces semantic changes. Use the existing amendment route; split only a genuinely independent behavior/proof boundary after a material contradiction. Bytes or chunk count alone do not create new tasks. Format retains exact reproduction, AST and comment/directive preservation, full tests and reviewed exceptions. Generated SQL, snapshots and journals remain counted and reviewed for semantics and security.

### Reproducible preparation and first worker

Main publishes these exact bytes under `plans/exploration/coordinator-parity-preparation/` before approving this plan:

| Artifact | SHA256 | Purpose |
|---|---|---|
| `docs/specs/dual-coordinator-parity.md` | `7b2bdc79bb5d9bc0163f22ad1fcf7f557db7f53102bdc288a6d0633e6e2a4f7e` | Confirmed capability and acceptance boundary, including First-owned D-0032 and Portable-owned one-time migration. |
| `docs/specs/strict-role-split.md` | `610673976b1fc66ca335e54d2c60e49771411d4cb4f0cf27541e24c41dc796d3` | Confirmed coordinator-neutral writer and degraded-mode boundary. |
| `docs/architecture/dual-coordinator-parity.md` | `e69807c742a3d7317d9b766caf6bb140815b11c1a2bb43fa0eea8aaf64f6a0e4` | Shared review publication, exact hook matchers, between-task coordinator changes, and one-time migration architecture. |
| `lean-delivery-graph.json` | `605936a0e91ac5cfcf629a1e1ea66e0515428ca445c4e39f3732d208e24d091a` | AC/roadmap/owner crosswalk plus the explicit new model-policy and combined-review allocation annexes plus `prepared_hunk_owners`: all 40 original paths and 201 hunk identities, hashes and allocations. |
| `native-original-40-path.patch` | `09cd2ec4826e407541cc4fe75d6d604f9ce6b8bb9f1c8b734aef23e2e42ad54f` | Exact 342,596-byte original donor history; distinct from older `original-bootstrap.patch`. |
| `native-foreground-preparation.patch` | `bee122bb370177ededefb5fe81a82f8c600f69af8502e151956ec7b8afed29e2` | Exact 109,953-byte, 16-path first import against `824baed4a657a83a6a7583e85ee67d2907e7c172`. |
| `native-foreground-preparation-inventory.json` | `3874bb1a3e698c340c19b419d22cad897d12c80d2314bd4b5142d5c3656fa48f` | Existing per-path source/trunk/prepared hashes and first selection. |
| `client-ledger-migration-inventory.json` | `aac7772f212217d4bbd2d5ef288600eb644b0f1338982533d51ce600649e6df5` | Dated five-checkout snapshot, deduplicated into four common directories and refreshed with the bound repository identities. |

The graph has no reverse plan hash, avoiding a circular binding. Its hunk mapping inherits each path's remainder owner unless an explicit hunk override differs. Exact foreground-selected material belongs only to First; the remainder belongs to its named successor. Archived superseded bytes require an explicit equivalent/corrected/retired disposition in that owner's complete review. Nothing is silently dropped or credited twice. There is no second mapping registry.

Preserved S `/Users/dev/Workdir/symphony-forge-native-dogfood` drives the existing 0063 source ceremony. Existing task start creates real T from fetched trunk; validate any newer baseline before import. Import only the bound foreground allocation, then freshly ground and bind T before stage start and registered admission. Source proof cannot certify T. C `/Users/dev/Workdir/symphony-forge-lean` remains the captured destructive-resume reproduction; do not manually repair its pointer or create another bootstrap exception.

First owns an amended 76-path task envelope: the prior 75-path contract remains intact and adds `factory/tests/test_close_binds_to_the_diff.py` after the full post-implementation verify proved its direct legacy fixture cases need selected-generation migration. That total envelope measures and reviews all prior committed First work; it is not permission to revisit it. The one remaining registered worker may edit only the following 17 existing paths plus the one new schema, with at most 3,200 added-plus-deleted lines: `docs/QUALITY.md`, `factory/scripts/check_task_proof.py`, `factory/scripts/factory_lib.py`, `factory/scripts/forge.py`, `factory/scripts/record_review_from_json.py`, `factory/scripts/forge_cli/close.py`, `factory/scripts/forge_cli/review.py`, `factory/scripts/forge_cli/review_brief.py`, `factory/scripts/forge_cli/stages.py`, `factory/scripts/forge_cli/tasks.py`, `factory/tests/test_gates.py`, `factory/tests/test_close_binds_to_the_diff.py`, `factory/tests/test_proof_read_path.py`, `factory/tests/test_review_lenses_in_parallel.py`, `factory/tests/test_review_settled_contracts.py`, `factory/tests/test_review_task_delta.py`, `harness.yaml`, plus new `factory/schemas/review-set.json`. Every other in-envelope path is preserve-byte-for-byte input to this delegate. It stops on any other edit or larger remaining delta and returns the contradiction for amendment. The task-level 180-file/18,000-line review budget remains only the seal-time ceiling over the entire accumulated First task delta and grants no additional edit authority.

The inherited board already uses `task_proof_problems` for per-task progress; its separate story summary remains story-scoped display and cannot satisfy task proof, so `board.py` needs no change. First changes `stamp_is_fresh` into the selected-generation/current-delta predicate shared by closeout and stage consumers, and removes the public `--sequential` arguments plus environment/internal plumbing from `forge.py`, `close.py`, and `review.py`. Harness schema declarations and `docs/QUALITY.md` move to the one-generation contract in this task. The two inherited test files are rewritten in place: one proves a single helper and coherent generation instead of three concurrent helpers, and one proves a task with missing proof does not fall back to story proof. The user's explicit D-0032 request moves the complete combined-review behavior plus necessary specification/graph canon hunks to First as a new overlay; the Decision0068 model-policy overlay remains separate, and all original 40 prepared path/hunk owners remain unchanged. First supplies C9/C10 complete review/proof, the one-helper combined review, minimal workspace creation, unshipped-operation guards, foreground revocation/cleanup/refusal tests, Claude clear parity, and the complete current Decision0068 policy. The audit proved successful protected reads and false pending wording; Lean owns `phase.py`'s wording fix. Diagnose only an observed target failure; add no speculative read-root repair, snapshot authority or recorder ban.

C10 has no fixed-path fallback. First makes the current task publish a fresh selected combined generation before readiness or seal. Portable performs the only compatibility transition. Before any target write, upgrade enumerates regular, non-linked task-scoped triples at `.factory/stories/<story>/tasks/<task>/reviews/{quality,performance,security}.json`; each must match that exact story/task and a current active task or immutable task marker. It also enumerates story-scoped triples only when their own fields and shipped history identify exactly one task marker; incomplete, multiply-bound, unshipped, or unidentifiable story sets remain display-only and never become proof. The inventory is sorted by story/task/path/hash, covers every matching root before mutation, and its digest is the migration sentinel. An existing valid selected pointer is the per-task completion sentinel. Active proof binds current task state; sealed proof binds the immutable marker commit and exact old artifact bytes. Only after the whole inventory passes may upgrade write content-addressed `origin=upgrade` generations and pointers. A sealed reader accepts that later pointer only when its sealed-commit binding exactly equals the marker. Malformed, mixed, colliding, linked, or ambiguous input refuses; byte-identical retry passes and unbound archives stay display-only.

Admission uses the resolved target worktree, Git directory, and common directory as identity. `run.json` publishes only after Git registration and hydration pass. First enforces foreground writers. Shared adds safe attach before JIT planning; a clean registered unowned worktree must match fetched trunk, branch, story, task, decomposition, and dependency markers. Empty dependencies inherit the immediate predecessor, while a nonempty list selects exactly those dependencies. Native later adds detached read-only helpers plus status, cancel, resume, and recovery. Background writers remain refused. Cancellation revokes before cleanup; terminal state and stage closure revoke the matching admission. No new owner ledger is added.

### Current model-policy amendment

Accepted Decision0068 and the user's explicit model/team request add new work to First without moving the original preparation allocation. First updates every executable project selector and active guidance surface, commits all 15 project agent definitions, proves the existing init full-tree copy and upgrade same-name refresh while preserving distinct client-added agents, and hardens the same Claude plugin route for Luna/max through an exact-source doctor capability check. No new actor may use Terra. Exploration is Sol/low; planning, decomposition, architecture, plan validation and grills are Sol/high; all implementation, technical test verification and autoreview fixes are Sol/medium except formal Lite at Luna/max; formal autoreview and functional checking are Sol/high.

The old project profiles are currently executable, so they cannot be described as deferred or inactive. First must finish the complete 76-path scope before it ships. The amended graph carries the model-policy and combined-review requests as separate overlays and leaves every original prepared hunk record unchanged. Lean retains its workflow simplification and separately found `pr-link.yml` event-staging fix while consuming First's combined-review proof; Shared no longer owns Remaining0062 model selection, and Portable preserves/distributes the team registry instead of retiring it.

### Safe installation, retention and client migration

Setup and `forge doctor` choose a coordinator for one invocation by the first applicable tier: one valid explicit argument; otherwise one valid `FORGE_COORDINATOR`; otherwise exactly one detected host; otherwise an interactive TTY choice. A valid higher tier suppresses every lower tier, so argument/environment or chosen-value/detection disagreement is an override, not a conflict. Multiple explicit values, an invalid selected value, cancellation, EOF, or no TTY choice refuse before repair; detecting both or neither host simply reaches TTY and refuses only when no interactive answer exists. Never persist the selection. `init`, `adopt` and `upgrade` install and preserve both adapters.

Decision0068 explicitly amends only Decision0057's instruction to retire and omit the three project agent definitions; 0057's question requirements remain active as narrowed by accepted0064, and its other roadmap, phase-role and gate requirements remain active. Decision0068 also amends only Decision0065's existing First-scope clause and matching recorded scope lesson for this later explicit model/team overlay; it preserves every original prepared hunk owner, source/target binding, eight-task graph, and all other 0065 duties. First commits and proves all 15 team definitions through existing distribution behavior: init copies the complete tree, upgrade refreshes harness-owned same-name definitions/configs, and distinct client-added agents remain. No new TOML merge or provenance mechanism is required. Portable later exercises that behavior during client rollout with existing safe path handling; it never deletes `.codex/agents` recursively. Existing legacy `.agents` migration grants no deletion authority.

Retention uses existing decision/event readers, shipped proof and upgrade. Generate the active-decision view on demand. Existing payloads have no ID field, so the validated lowercase 32-hex source filename stem is authoritative. Each bundle member is exactly `{"id":"<source filename stem>","payload":<validated original event object>}` sorted by ID; compare ID plus deterministic sorted compact UTF-8 payload. Equal pairs deduplicate, an existing member with the same ID and unequal payload refuses, and distinct IDs remain distinct. Only validated live `.factory/events/<id>.json` with exact shipped identity may mutate: scoped requires matching done roadmap/history pointer, shipped.json, complete task markers/proof, merged PR identity and green required CI; legacy requires archived outcome/shipped evidence plus merged-PR and green-CI proof, never the old `pr-ready` phase alone. A legacy record without those facts remains loose. Do not invent retroactive markers. Root JSONL and every pre-existing history file remain byte-immutable. Preview prints the exact eligible inventory SHA256; apply requires it through `--expected-digest` and refuses drift before mutation. First publication uses a complete temporary file and atomic no-overwrite. An existing bundle is immutable: retry removes only regular unchanged loose sources whose exact pairs already appear; it never unions/replaces/truncates, and unseen late IDs remain untouched and refuse. Before deletion, re-read each regular non-linked source path, require its stem to equal the durable member ID, and compare canonical payload bytes with the just-read durable entry. Keep partial-failure evidence, `format: forge-event-bundle/v1`, exact top-level format/story/events, no sidecar/heuristic, legacy-idless no-op, and the existing 0025 untracking allowlist.

The user's prior explicit one-time approval names four common directories. This plan binds the three currently verifiable GitHub identities below. The user selected **Pause Toolshed** through the structured question tool on 2026-09-11 because that checkout has no configured remote; D-0033 records the zero-mutation deferral and exact revisit trigger, so Toolshed no longer makes this story unfinishable. Refresh remote/default-branch, HEAD, dirty state and resolved absolute `git rev-parse --git-common-dir` at each safe boundary. A mismatch refuses that row. Deduplicate by common directory, never checkout name.

| Common directory | Bound repository / branch | Required outcome |
|---|---|---|
| `/Users/dev/Workdir/cadence/.git` | `knacklabs/cadence` / `main` | One isolated upgrade PR; migration result, checks and CI recorded. |
| `/Users/dev/Workdir/toolshed/.git` | **Deferred D-0033: missing** | Zero mutation. Revisit only after the user supplies and approves exact `owner/repository`, default branch, and mutation authority. |
| `/Users/dev/Workdir/myclaw/.git` | configured alias `vrknetha/myclaw`, resolved canonical `knacklabs/gantry` / `main` | One upgrade for both dirty checkouts; preserve distinct heads, hotfixes and files. Never upgrade them separately. |
| `/Users/dev/Workdir/knacklabs-ats/.git` | `knacklabs/knacklabs-ats` / `develop` | One isolated upgrade PR with migration result, checks and CI recorded. |

Portable first implements, verifies, reviews, merges and marks the client-safe upgrade/compaction capability on trunk. Format and Quality then land the final pinned vendored workflow and declaration bytes. Main runs each authorized, identity-bound client row only from that final Quality-or-later trunk revision; these PRs are story evidence and create no ninth harness task. For each runnable row, fetch the bound default-branch tip, create the ticket-bearing branch `feature/FORGE-COORD-1-forge-upgrade` in a sibling worktree, run upgrade and history compaction, then run vendor integrity, the client's declared checks and CI. Cadence and Gantry deliberately branch from and return to their verified `main` defaults because those repositories do not use `develop`; KnackLabs ATS uses its verified `develop`. This approval-bound paragraph is the written constitution deviation for external repos whose established default is `main`; the ticket prefix and `feature/` type remain compliant. Never use a dirty MyClaw checkout head, stash, reset, force, or touch Toolshed while deferred. Record harness revision, source revision, base, migration result, PR, commit and logs. An unsafe row stops that row; D-0033 remains a visible deferred limitation and does not block the three configured client proofs or Integration.

Portable captures `./forge findings patterns` before and after work. The historical `reviewed-separately ×3` and `repository-escape ×3` classes already have the accepted 0005/0028 consolidation: `_preflight_upgrade`, checked `_replace_path`/`_keep_path`, and `assert_target_destination`/`assert_target_file_destination`. Audit every changed read/copy/delete against those helpers; retain the raw-write tripwire and leaf/ancestor/malformed-state refusal tests with unchanged external sentinels. Historical aggregation has no resolved flag, so zero old rows is not an acceptance condition. Any new/changed recurring class, unresolved current finding, raw-write violation or escape failure stops affected mutation and uses the existing scope-change/deferral route. Preserve the hard-link/TOCTOU deferral; do not invent another refactor merely to erase historical counts.

The committed Claude and Codex hook configurations are the normative tool inventory. Claude captures completed `AskUserQuestion`; Codex captures completed synchronous `request_user_input`. PostToolUse completion coverage applies only to a tool that can return completed answers in that call. Asynchronous issuance is PreToolUse-guarded optional clarification, cannot carry gate authority, and is neither a completed exchange nor completion evidence. `check_dual_runtime.py`, focused hook tests, and the recorder-produced automated report are proof. Existing event writes remain best-effort diagnostics under Decision 0017 and cannot certify a gate.

Native lifecycle observability follows constitution 05, 06 and 07. `forge_cli.codex_runtime` owns one shared structured logger used by the launcher and supervisor rather than direct ad hoc writes. The local Forge CLI emits human-readable status to stderr and the same redacted structured record to the existing durable task-local JSONL transport; no non-local service exists in this repository, so centralized transport is explicitly not applicable. Whenever an accepted, starting, running, retrying, cancel-requested, canceled, failed or succeeded transition occurs, the logger emits one record with the required timestamp/level/static-message/context/environment/service/module/correlation/account fields and request/event IDs when applicable. Correlation binds story/task/launch/session/process/stage; prompts, tokens, credentials, raw environment values, PII and whole request objects are redacted. Existing retries remain bounded and idempotent and retain prior failures; cancellation records revocation before signals and reaches one truthful terminal result. A top-level native launcher/supervisor `Exception` boundary converts every otherwise-unhandled exception into one sanitized stable-ID terminal failure and nonzero result, and increments durable structured `forge_native_unexpected_errors_total` exactly once with bounded service/module/outcome labels and matching correlation. Native lifecycle tests prove fields, both local transports, correlation, redaction, retry/cancel ordering, terminal uniqueness, boundary propagation, nonzero failure and metric increments. Integration cites separately produced native, Mac CLI/Desktop and Task tracker logs; one source cannot certify another.

## Decisions

Frontmatter attests every active decision, including 0069 and 0070. Accepted 0066 owns diff-bound review stamps and the resumable proof-to-PR closeout. Accepted 0067 owns physical review publication and the CI-transport-only draft rule; every other accepted rule remains active. Decision 0053 keeps coordinator changes between tasks, 0059 owns workspace-first tasks and empty-dependency fallback, 0060 retains narrow POSIX signal restoration, 0065 owns final platform proof, 0068 owns the current model/team policy, 0069 narrowly permits proven empty-frontier zero-round grills after Shared, and 0070 stages mandatory new CI at Quality without weakening final closure. The inherited three-helper runner remains valid until First ships the 0067 one-helper generation. Decision 0011 keeps review with the orchestrator; proposed 0049 remains historical context. First and Lean use the incumbent gates until their replacements ship. No fabricated record skips an existing prerequisite.

## Surface Impact

| Surface | Impact and reason |
|---|---|
| Runtime | Changed: native lifecycle/admission; preserve Claude. |
| API | Unchanged by design: no external service/API added. |
| Data/schema | Changed: existing brief/proof metadata and stable-ID event bundle. |
| CLI | Changed: gates, review, phase wording, resume and upgrade. |
| UI | Changed: Shared owns the existing board/owner journey; the separate client has its own UI task. |
| Docs | Changed: First's task-owned branch already contains the Main-authored pre-approval canon and concise AGENTS pointers; the implementation worker preserves those bytes unless a tested runtime correction requires the same task-owned file. |
| Tests | Changed: targeted regressions, mandatory quality, client and required local Mac/Linux/Windows CI evidence. |

Retain Python 3.11 and uv. Pin the existing toolchain in one file: Ruff 0.16.6, Pyright 1.1.411, pytest 9.1.1, pytest-xdist 3.8.0, and psutil 7.2.2. Ruff supplies the required linter and formatter; Pyright is the existing type checker; pytest, xdist and psutil are already used by the suite and lifecycle code. Follow `constitution/README.md`, the applicable conduct rules in `constitution/09-agent-conduct.md`, exception handling and the shared path-boundary invariant; apply ponytail to each edit. No new framework or duplicate abstraction is needed.

## Task Decomposition

These overlapping tasks remain sequential, each with its own scope, tests, proof, PR and real predecessor marker. This table controls harness-task UI ownership; the separate client is described in Verify Plan.

| Label / exact task ID | Complete boundary | Depends on | user_facing |
|---|---|---|---|
| First / NATIVE-FOREGROUND-ACTIVATE | Exact foreground allocation plus the Decision0068 model-policy overlay; C9/C10, one helper call, one immutable raw-plus-three-lens generation and one pointer, workspace, guards, cleanup, clear and live boundary proof. | none | false |
| Lean / LEAN-WORKFLOW | Single brief/authorization/design applicability, complete inputs, phase/workflow ownership, rulings and generated budgets. | NATIVE-FOREGROUND-ACTIVATE | false |
| Native lifecycle / NATIVE-LIFECYCLE | Detached read-only helpers plus jobs/status/cancel/resume/explore and process-tree recovery; implementation writers stay foreground and stage-bound; structured correlated/redacted lifecycle logs, bounded retry and truthful terminal errors. | LEAN-WORKFLOW | false |
| Shared / SHARED-COORDINATOR-JOURNEY | Structured-question identity, Decision0069 empty-frontier proof, workspace-first attach, owner/board/queue, safe resume/seals, PR retry, and between-task coordinator changes. | NATIVE-LIFECYCLE | true |
| Portable / PORTABLE-DELIVERY-MIGRATION | Client-safe setup/adopt/upgrade and retention capability preserving the First-owned project agent registry; it ships before the separate configured-client rollout. | SHARED-COORDINATOR-JOURNEY | false |
| Format / FORMAT-SOURCES | Commit exact pinned requirements and final Ruff config, then perform full pure mechanical Python formatting with equivalence/preservation/test proof. | PORTABLE-DELIVERY-MIGRATION | false |
| Quality / QUALITY-BASELINE | Consume Format's pins/config byte-for-byte; own Pyright config, semantic Ruff/Pyright repairs and mandatory identical local/CI source/test enforcement. | FORMAT-SOURCES | false |
| Integration / FORGE-COORD-1.1 | Integrated AC1–12, completed three configured-client rollout plus explicit Toolshed D-0033 limitation, required local Mac/CI proof on the final harness with live-platform limitations and referenced separate-client marker, one formal combined review, functional proof and ordinary PR/CI. | QUALITY-BASELINE | false |

## Risks

An absent or ambiguous task owner must not downgrade task proof to story proof. Preserve owner/base/seal fields on resume and refuse cross-task proof selection. Hydrate actual grill rounds, not withdrawn plan-mode markers. Missing required runtime/CI evidence and unresolved client migration are proof gaps; unavailable Linux/Windows live observations are explicit accepted0065 limitations. No fixture, historical marker or preparation test substitutes for actual target/platform evidence.

## Verify Plan

Each task owner runs and records the declared regressions and repository verifier, then carries that task's review/fix loop through PR and green incumbent CI in its own worktree. Decision0070 permits pre-Quality tasks to record the unavailable new Ubuntu/Windows jobs as a scheduled gap; Quality installs those jobs and final Quality/Integration closure requires them. Local, committed-CI and board readers must agree before marker/PR mutation. Shared's actual UI receives functional proof; other internal harness tasks do not acquire UI scope just because their CLI is visible.

```sh
UV_CACHE_DIR=/tmp/forge-lean-uv-cache UV_TOOL_DIR=/tmp/forge-lean-uv-tools uv run --python 3.11 --with-requirements requirements-quality.txt python factory/scripts/verify.py
```

### Falsifiable quality activation

Format owns and commits `requirements-quality.txt` with exactly `ruff==0.16.6`, `pyright==1.1.411`, `pytest==9.1.1`, `pytest-xdist==3.8.0`, and `psutil==7.2.2`, plus the final `ruff.toml`, before invoking Ruff format. Quality consumes those files byte-for-byte and cannot change formatter behavior; it owns `pyrightconfig.json`, `factory/scripts/check_python_quality.py`, `verify.py`, `.envrc`, `.github/workflows/factory-scaffold.yml`, `.github/workflows/pr-ticket-check.yml`, affected vendoring declarations and focused tests. Retain Pyright's `factory/scripts` import path. Harness coverage is exactly every tracked `*.py` below `factory/scripts/` and `factory/tests/`, including tracked fixtures in those roots; generated or client-owned Python outside those roots is excluded and uses its owning client's declared stack checks. No blanket suppression or test exclusion.

Local verification and the harness CI job run the same command:

```sh
uv run --python 3.11 --with-requirements requirements-quality.txt python factory/scripts/check_python_quality.py
```

The small runner derives that tracked file set and passes it to Ruff check, Ruff format check and Pyright. `.envrc` and `verify.py` use the exact command above. The scaffold workflow runs it on every branch push and pull request; Ubuntu and Windows installs consume the same requirements file instead of separate unpinned packages. Tests prove missing config/tool/path and deliberate lint, format and type failures. A no-op cannot pass. Vendored clients use their own meaningful stack checks. Current optional verification is not credited as AC12 proof.

Portable additionally runs the existing `test_no_raw_write_primitive_outside_the_boundary_helper`, `test_upgrade_refuses_a_symlinked_destination_before_writing` and `test_upgrade_refuses_a_symlinked_ancestor_and_leaves_the_target_clean`, plus the existing agent-distribution, malformed-state and idempotent bundle cases. Source-harness test selectors remain precise; do not broadly skip a client/harness environment.

### Separate UI and platform evidence

The user's approved dogfood exception authorizes Main, only after the Quality task marker reaches trunk, to create one fresh `/tmp` Task tracker client and the currently absent private repository `vrknetha/symphony-forge-tasktracker-dogfood` with default branch `main`, using the verified authenticated GitHub login `vrknetha`. It creates no hosted application, deployment or reusable client-CI machinery. Before creation, Main requires the repository name and local run directory to be absent. After creation it records the exact repository ID and URL in the client task evidence; a partial retry may reuse only that private repository when its recorded ID, owner, default branch, record-origin marker and task identity all match, otherwise it refuses without deletion or overwrite. The planned client leaf is `TASKTRACKER-1/TASKTRACKER-1.1`, explicitly `user_facing: true`; its implementer owns code/automated proof and its functional-checker owns real UI functional proof with required skills. Acceptance proves a clean final-harness install followed by the client's declared lint, type, build and test commands, then recorded create/list/complete persistence through the UI and storage path. The client owns `tests.json`, `verify.json`, selected review generation and its task PR/CI. Integration remains `user_facing: false` and refuses until the exact client task marker, reviewed PR, green CI and functional proof match the cited client repository/commit. It consumes exact client repository, commits, PR, artifact paths and logs in its own automated report. It cannot copy client authority or credit client code as a harness contribution; the separate lifecycle adds no ninth harness task or fake cross-repository task ID.

Integration uses the existing automated schema/recorder with `generated_by: implementer` and existing `status`, `summary`, `commands_run`, `pass_fail_summary`, `remaining_gaps`, and `blocking_findings`. Encode `pass_fail_summary` as a JSON array string with exactly the six labels in declared order. Every row has exactly `label`, `status`, `evidence_kind`, `os`, `cpu`, `revision`, `runtime`, `commands`, and `logs`; status is passed/failed/unobserved, unavailable runtime is null with an explicit remaining-gap explanation, and commands/logs are arrays. The Integration-owned validator uses `json.loads`, rejects malformed/duplicate/missing/contradictory rows, resolves log references against the tested revision, requires exact client evidence, and derives aggregate status. Independent review checks the same logs. C10 consumes the review-bound aggregate rather than parsing this encoding. No schema property, second report, matrix registry, or second authority is added.

Accepted0065 requires actual local Mac CLI/Desktop observations and meaningful Ubuntu24.04 x64/native Windows CI regressions plus exact `@openai/codex@0.153.4` package/version/help smoke. Version 0.153.4 is the explicitly pinned test input for this story; the contract makes no fixture-backed or minimum model-support-floor claim. A version change requires a plan amendment because all platform rows must use one tested input. Each row states passed/failed/unobserved, evidence kind, exact tested revision, OS/CPU/build, real commands/interactions and durable logs. Linux/Windows CLI-labelled CI rows explicitly state that unavailable authenticated runtime behavior is unobserved; only the Linux and Windows Desktop rows may remain unobserved. Local Mac CLI and Desktop rows are mandatory and cannot be waived as a limitation. Accepted limitations remain in remaining_gaps; actual failures and missing required evidence appear in both gaps and blockers. Aggregate status passes only when the four required rows, other task checks and client proof pass with no blocker. Never claim live Desktop from CLI/CI, nor native Windows from WSL. Observe the required real Mac hooks, protected write boundary, admitted contribution and terminal outcome, plus supported optional questions or the permitted main-chat route. QUALITY-BASELINE implements these OS CI jobs in its existing owned workflow and uses Decision0070's CI-transport-only draft for their first run, retaining existing full-suite and Windows gates; Integration consumes the actual final-harness logs. Preserve Claude regressions.

Close only after all eight task markers reach trunk, all 12 criteria and activated quality pass, required local Mac/Linux/Windows CI proof passes on the final Quality-or-later harness with live-platform limitations stated, the three configured client PRs and dogfood proof/CI are green, Toolshed remains honestly deferred as D-0033, migration outcomes are honest and the existing story outcome is recorded. Closeout adds no second story review.
