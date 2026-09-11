---
issue: FORGE-COORD-1
title: Either Claude or Codex coordinates the same Forge workflow
status: awaiting-approval
saved: 2026-09-11T17:22:30+00:00
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
  - 0067-combined-review-generation
---

# Symphony Forge: lean delivery

Draft revised against the independent requirements and plan reads. Decisions 0064 and 0067 authorize the simpler workflow, one-generation review, and retention; the user's prior explicit one-time approval authorizes branch, push, and PR work for the exact four-client migration set. Existing recording and admission gates still apply. The corrected specification is confirmed before this plan is saved and approved, and the final digest is bound below.

## Problem

Repeated plans, approvals and review launches slow delivery and lose settled answers. The developer should decide once when necessary, then let authorized work continue through tests, review, PR and green CI. Fresh workers and reviewers must receive the same ruling. Overnight work returns a compact account of completed PRs, real blockers and decisions needed.

## Transition before delegation

The current protected plan, decomposition and First task plan remain in force until this replacement completes the normal gates. In order: save and confirm the corrected specification; record the requirements pass; run and record the user-requested final grill of this simplified plan; save it awaiting approval, obtain the digest-bound human approval, and save the unchanged plan again; record the matching eight-task decomposition; save, grill and approve the new First task plan. Only then may the existing First stage continue and delegate the D-0032 work. This explicitly replaces the old D-0032 deferral and Shared draft-PR wording before any worker receives the new contract.

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
| AC5: hook delivery | First, Shared, Portable, Integration | Exact committed hook/tool matrix and real blocking capability; focused tests plus automated logs prove success/failure, sanitized error, metric, trace, and refusal behavior. |
| AC6: honest evidence | First, Lean, Integration | Preparation and diagnostics stay labelled; only current task-bound recorder proof passes; required platform rows use actual logs and evidence kind. |
| AC7: genuine native task | First, Integration | One qualifying hunk in the existing task branch diff correlates with admitted write, terminal evidence, criterion/finding, verification, review, PR, and CI; prepared bytes earn no contribution. |
| AC8: setup and preservation | Portable | Setup/doctor choose per invocation; init/adopt/upgrade preserve both adapters plus client ownership/history; review migration and late-event refusal are proved. |
| AC9: continuation and context | Lean, Shared | Settled rulings survive fresh workers; authorized work resumes without repeated prompts; optional unanswered questions do not block it. |
| AC10: coordinator change | Shared, Integration | Change only between completed tasks after the old session stops, marker and green CI reach refreshed trunk, and no worker or partial structured question remains; the new session resumes through `forge next`. |
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

No roadmap-field edit is needed. Criterion 1 already owns worker policy and every gate, including the exact design-review predicate and Decision0066 registry. Criterion 3 owns the delivery chain, and accepted0064 explicitly amends it with exact event compaction and four-client migration. The AC1–AC12 table, roadmap table, and C1–C10 table together are the required closure crosswalk. The ten retained client failures keep their explicit owner/source/acceptance rows in the bound ownership graph. The platform contract and separate dogfood client close through AC6–AC8, C8, and roadmap criterion 3. An obligation absent from those bound rows cannot silently become a shipping blocker.

The graph retains the exact three roadmap strings, original 39-row mapping, ten client-failure owners, task-level `user_facing` values and complete preparation allocation. Its digest below binds those details to this plan; changing ownership afterward requires the existing contract amendment route.

## Technical Approach

### One brief and proportionate scrutiny

Use the existing task plan as the current brief: behavior, boundaries, owner, checks and rulings. Keep story/specification intent and client sign-off; derive execution and review inputs from existing records. Main presents a real new decision with its recommendation, tradeoff, consequence and concrete artifact. Carry actual standing authorization through in-scope corrections and retries using existing approval commands. Lean records the correction/reason/technical classification/authority in the current brief, saves the new digest so stale approval drops, then fresh-binds the concrete revision with actual developer identity/time without claiming a new answer or reread. Material intent, scope, permission, migration, security, lifecycle, ownership or missing authority still requires display and explicit approval. Accepted0064 narrows 0057's pause-all wording: an unanswered required question pauses the addressed task/artifact and every causally affected contract; separately owned dependency-ready unaffected work continues, while missing/canceled answers grant no authority.

Lean adds optional explicit `--context-file`. Open the selected regular file once without following unsafe links, validate and capture immutable UTF-8 bytes, SHA256 and byte count, then launch only those bytes as untrusted supplemental context. The file cannot alter primary artifact/gate/task identity or authority. Missing/non-regular/non-UTF8 input refuses, with no search, reopen, repo-only root, truncation or arbitrary cap. Limits must be known in UTF-8 bytes. Partition only a consumer with an approved ordered aggregation contract; exact captured bytes are covered once in order, and any missing/reordered/conflicting/failed part invalidates the whole result.

After Shared ships, each successful structured call gets one fresh event ID and zero-based question index. Eligibility binds runtime, session, exact story/gate/task scope, current input digest, requiredness, question, ordered options, and nonblank answer. Each question is consumed once; optional non-gate questions cannot satisfy a gate. If an answer changes an approval-bound artifact, its normal decision or approval records the final revision and the grill covers that revision. No revision-mapping protocol or new ledger is added. Incumbent grill floors remain until Shared ships; a native cold read with no human frontier may then record zero rounds only from its ledgered launch and complete empty-frontier result.

A required ordinary-chat question holds its current turn; abandonment grants no authority and a later session asks again. Coordinator changes happen only between completed tasks after the old session stops, the marker and green CI are on refreshed trunk, and no worker or partial structured question remains. The new coordinator resumes through `forge next`. There is no live handoff command, snapshot, fencing token, or concurrent coordinator ownership.

Lean makes `design_review: required|routine` and nonblank `design_review_rationale` explicit in the existing approval-bound brief/frontmatter. Missing/unknown/blank means required. Required is mechanical for a changed actor/write/read/sandbox/credential/network boundary; deletion, overwrite, move, external side effect or other non-reversible operation; stored-data schema/migration; public CLI/API/evidence schema; lifecycle state machine; or ownership boundary. A routine rationale must state that none of those exact triggers changes; the grill checks the artifact and refuses a false downgrade. Signoff is always required, so the legacy BRIEF needs no classification frontmatter. Epics is required when any referenced capability is required or missing classification. One genuine assessment may cover several applicable existing gates only when it explicitly reviewed every complete input and each record remains independently bound to its own artifact. This does not permit copied passes. The confirmed specification names each gate's exact classification input, record and digest. Shared reads must explicitly assess each complete input; current one-gate launches cannot certify other gates. Classification and rationale remain authored digest-bound content, not excluded managed metadata. Incumbent prerequisites remain until Lean ships.

### Review and measurable cleanup boundaries

The owner of each task carries that task in its worktree through implementation, review fixes, PR and green CI. The coordinator invokes the review there under accepted 0011; Main schedules the story and owns only the separate story-level client rollout. For the current First task, the active task owner and Main coordinator are the same session. Proposed 0049 supplies no authority. The user explicitly moved complete D-0032 ownership to First because three helper calls cost too much time; Lean consumes it and does not reimplement it.

Each default `./forge review <task-id>` calls the installed helper once. It writes one immutable generation containing the raw result and three genuine lens records, validates and reads it back, then publishes the small task pointer last. `factory/schemas/review-set.json` distinguishes `combined`, citation-based `rejection`, and one-time `upgrade` origins. Blocking generations select and revoke clean status; failure leaves the prior pointer unchanged. Fixed lens paths are never runtime fallback.

Every actual provider pass uses exact full-line quality, performance, and security assessment markers once and in order. Quality retains the existing contract-verdict syntax. Forge preflights their minimum size against the helper's 3,000-character explanation limit. Unchunked output is the top-level pass; chunked output requires exact `chunk 1/N` through `chunk N/N` labels. Each finding has one lowercase lens tag. Cross-lens duplicates use the architecture's deterministic path/line/title fingerprint. Existing score, recommendation, and worst quality-verdict functions remain. One shared classifier supplies review scope and current/historical branch-diff hashing, including genuine-contribution hunks; no product-tree digest exists.

A rejected finding creates an immutable successor bound to the selected combined generation, its exact finding, reason, citation, and actor, preserving raw output and unaffected lenses. A single-lens run remains diagnostic. Decision 0067 permits an early draft PR only when required platform CI needs it; the draft is transport, and formal review runs after platform evidence passes.

The reconciled specification removes the old 120,000-byte product and 180,000-byte review caps under accepted 0064, including the obsolete 0058 clause. The corrected revision completes the normal save, one change-scoped grill and confirmation sequence before this plan is saved. The current resolved autoreview helper has no implicit patch-size cap; its observed 512,000-byte limit covers each complete rendered prompt, including instructions, evidence and framing. It is a tool safeguard, not a new task-size policy. Bind one immutable input snapshot before counting or launch. Use supported evidence partitioning only where the helper's ordered aggregation contract preserves every captured byte and invalidates the whole result on a missing, reordered, conflicting or failed part; never trim authoritative input or change its limit.

Format measures the actual pinned formatter output after Portable ships. Quality measures the actual remaining diagnostics and repair diff after Format ships. Each JIT records exact files, changed lines, total input bytes and rendered partition sizes, then binds positive file/line budgets to that complete scope. Recheck before review and seal. Stop if the actual scope exceeds those budgets, any full prompt cannot be partitioned within the installed limit, any input/chunk is missing or failed, or Format introduces semantic changes. Use the existing amendment route; split only a genuinely independent behavior/proof boundary after a material contradiction. Bytes or chunk count alone do not create new tasks. Format retains exact reproduction, AST and comment/directive preservation, full tests and reviewed exceptions. Generated SQL, snapshots and journals remain counted and reviewed for semantics and security.

### Reproducible preparation and first worker

Main publishes these exact bytes under `plans/exploration/coordinator-parity-preparation/` before approving this plan:

| Artifact | SHA256 | Purpose |
|---|---|---|
| `docs/specs/dual-coordinator-parity.md` | `9fc1e4579d040e1115743c592a967a75d24f214b64b566f3fe4175a7046c432e` | Confirmed capability and acceptance boundary, including First-owned D-0032 and Portable-owned one-time migration. |
| `docs/specs/strict-role-split.md` | `610673976b1fc66ca335e54d2c60e49771411d4cb4f0cf27541e24c41dc796d3` | Confirmed coordinator-neutral writer and degraded-mode boundary. |
| `docs/architecture/dual-coordinator-parity.md` | `e69807c742a3d7317d9b766caf6bb140815b11c1a2bb43fa0eea8aaf64f6a0e4` | Shared review publication, exact hook matchers, between-task coordinator changes, and one-time migration architecture. |
| `lean-delivery-graph.json` | `728f895ef80f4b32bc9ef7e0535cd9b301f85e4296d8a1de06b3946d7efdb709` | AC/roadmap/owner crosswalk plus the explicit new model-policy and combined-review allocation annexes plus `prepared_hunk_owners`: all 40 original paths and 201 hunk identities, hashes and allocations. |
| `native-original-40-path.patch` | `09cd2ec4826e407541cc4fe75d6d604f9ce6b8bb9f1c8b734aef23e2e42ad54f` | Exact 342,596-byte original donor history; distinct from older `original-bootstrap.patch`. |
| `native-foreground-preparation.patch` | `bee122bb370177ededefb5fe81a82f8c600f69af8502e151956ec7b8afed29e2` | Exact 109,953-byte, 16-path first import against `824baed4a657a83a6a7583e85ee67d2907e7c172`. |
| `native-foreground-preparation-inventory.json` | `3874bb1a3e698c340c19b419d22cad897d12c80d2314bd4b5142d5c3656fa48f` | Existing per-path source/trunk/prepared hashes and first selection. |
| `client-ledger-migration-inventory.json` | `aac7772f212217d4bbd2d5ef288600eb644b0f1338982533d51ce600649e6df5` | Dated five-checkout snapshot, deduplicated into four common directories and refreshed with the bound repository identities. |

The graph has no reverse plan hash, avoiding a circular binding. Its hunk mapping inherits each path's remainder owner unless an explicit hunk override differs. Exact foreground-selected material belongs only to First; the remainder belongs to its named successor. Archived superseded bytes require an explicit equivalent/corrected/retired disposition in that owner's complete review. Nothing is silently dropped or credited twice. There is no second mapping registry.

Preserved S `/Users/dev/Workdir/symphony-forge-native-dogfood` drives the existing 0063 source ceremony. Existing task start creates real T from fetched trunk; validate any newer baseline before import. Import only the bound foreground allocation, then freshly ground and bind T before stage start and registered admission. Source proof cannot certify T. C `/Users/dev/Workdir/symphony-forge-lean` remains the captured destructive-resume reproduction; do not manually repair its pointer or create another bootstrap exception.

First owns an amended 72-path scope: the live 66-path contract remains intact and adds only `factory/scripts/record_review_from_json.py`, `factory/schemas/review-set.json`, `docs/product/BRIEF.md`, `docs/architecture/dual-coordinator-parity.md`, `docs/specs/strict-role-split.md`, and `docs/degraded-mode.md`. Main aligns the four canon documents before plan approval; the worker implements only the scoped runtime/test delta. The user's explicit D-0032 request moves the complete combined-review behavior plus necessary specification/graph canon hunks to First as a new overlay; the Decision0066 model-policy overlay remains separate, and all original 40 prepared path/hunk owners remain unchanged. First supplies C9/C10 complete review/proof, the one-helper combined review, minimal workspace creation, unshipped-operation guards, foreground revocation/cleanup/refusal tests, Claude clear parity, and the complete current Decision0066 policy. The audit proved successful protected reads and false pending wording; Lean owns `phase.py`'s wording fix. Diagnose only an observed target failure; add no speculative read-root repair, snapshot authority or recorder ban.

C10 has no fixed-path fallback. First makes the current task publish a fresh selected combined generation before readiness or seal. Portable performs the only compatibility transition. Before any target write, upgrade preflights every eligible fixed set. Active proof binds current task state; sealed proof binds the immutable marker commit and exact old artifact bytes. After the full inventory passes it writes and reads back `origin=upgrade` generations and pointers. A sealed reader accepts that later pointer only when its sealed-commit binding exactly equals the marker. Malformed, mixed, colliding, linked, or ambiguous input refuses; byte-identical retry passes and unbound archives stay display-only.

Admission uses the resolved target worktree, Git directory, and common directory as identity. `run.json` publishes only after Git registration and hydration pass. First enforces foreground writers. Shared adds safe attach before JIT planning; a clean registered unowned worktree must match fetched trunk, branch, story, task, decomposition, and dependency markers. Empty dependencies inherit the immediate predecessor, while a nonempty list selects exactly those dependencies. Native later adds detached read-only helpers plus status, cancel, resume, and recovery. Background writers remain refused. Cancellation revokes before cleanup; terminal state and stage closure revoke the matching admission. No new owner ledger is added.

### Current model-policy amendment

Accepted Decision0066 and the user's explicit model/team request add new work to First without moving the original preparation allocation. First updates every executable project selector and active guidance surface, commits all 15 project agent definitions, proves the existing init full-tree copy and upgrade same-name refresh while preserving distinct client-added agents, and hardens the same Claude plugin route for Luna/max through an exact-source doctor capability check. No new actor may use Terra. Exploration is Sol/low; planning, decomposition, architecture, plan validation and grills are Sol/high; all implementation, technical test verification and autoreview fixes are Sol/medium except formal Lite at Luna/max; formal autoreview and functional checking are Sol/high.

The old project profiles are currently executable, so they cannot be described as deferred or inactive. First must finish the complete 72-path scope before it ships. The amended graph carries the model-policy and combined-review requests as separate overlays and leaves every original prepared hunk record unchanged. Lean retains its workflow simplification and separately found `pr-link.yml` event-staging fix while consuming First's combined-review proof; Shared no longer owns Remaining0062 model selection, and Portable preserves/distributes the team registry instead of retiring it.

### Safe installation, retention and client migration

Decision0066 explicitly amends only Decision0057's instruction to retire and omit the three project agent definitions; 0057's question requirements remain active as narrowed by accepted0064, and its other roadmap, phase-role and gate requirements remain active. Decision0066 also amends only Decision0065's existing First-scope clause and matching recorded scope lesson for this later explicit model/team overlay; it preserves every original prepared hunk owner, source/target binding, eight-task graph, and all other 0065 duties. First commits and proves all 15 team definitions through existing distribution behavior: init copies the complete tree, upgrade refreshes harness-owned same-name definitions/configs, and distinct client-added agents remain. No new TOML merge or provenance mechanism is required. Portable later exercises that behavior during client rollout with existing safe path handling; it never deletes `.codex/agents` recursively. Existing legacy `.agents` migration grants no deletion authority.

Retention uses existing decision/event readers, shipped proof and upgrade. Generate the active-decision view on demand. Existing payloads have no ID field, so the validated lowercase 32-hex source filename stem is authoritative. Each bundle member is exactly `{"id":"<source filename stem>","payload":<validated original event object>}` sorted by ID; compare ID plus deterministic sorted compact UTF-8 payload. Equal pairs deduplicate, an existing member with the same ID and unequal payload refuses, and distinct IDs remain distinct. Only validated live `.factory/events/<id>.json` with exact shipped identity may mutate: scoped requires matching done roadmap/history pointer, shipped.json and complete task markers/proof; legacy requires its original archived pr-ready run/proof and a task marker only when that run used task-level delivery. Do not invent retroactive markers. Root JSONL and every pre-existing history file remain byte-immutable. Preview prints the exact eligible inventory SHA256; apply requires it through `--expected-digest` and refuses drift before mutation. First publication uses a complete temporary file and atomic no-overwrite. An existing bundle is immutable: retry removes only regular unchanged loose sources whose exact pairs already appear; it never unions/replaces/truncates, and unseen late IDs remain untouched and refuse. Before deletion, re-read each regular non-linked source path, require its stem to equal the durable member ID, and compare canonical payload bytes with the just-read durable entry. Keep partial-failure evidence, `format: forge-event-bundle/v1`, exact top-level format/story/events, no sidecar/heuristic, legacy-idless no-op, and the existing 0025 untracking allowlist.

The user's prior explicit one-time approval names four common directories. This plan binds the three currently verifiable GitHub identities below. The user selected **Pause Toolshed** through the structured question tool on 2026-09-11 because that checkout has no configured remote; this grants no Toolshed mutation authority. Refresh remote/default-branch, HEAD, dirty state and resolved absolute `git rev-parse --git-common-dir` at each safe boundary. A mismatch refuses that row. Deduplicate by common directory, never checkout name.

| Common directory | Bound repository / branch | Required outcome |
|---|---|---|
| `/Users/dev/Workdir/cadence/.git` | `knacklabs/cadence` / `main` | One isolated upgrade PR; migration result, checks and CI recorded. |
| `/Users/dev/Workdir/toolshed/.git` | **Paused: missing** | Zero mutation. The user must supply and approve exact `owner/repository` and default branch before this row can run; the unresolved row blocks Integration. |
| `/Users/dev/Workdir/myclaw/.git` | configured alias `vrknetha/myclaw`, resolved canonical `knacklabs/gantry` / `main` | One upgrade for both dirty checkouts; preserve distinct heads, hotfixes and files. Never upgrade them separately. |
| `/Users/dev/Workdir/knacklabs-ats/.git` | `knacklabs/knacklabs-ats` / `develop` | One isolated upgrade PR with migration result, checks and CI recorded. |

Portable first implements, verifies, reviews, merges and marks the client-safe upgrade/compaction capability on trunk. Main then runs each authorized, identity-bound client row from that exact Portable revision; these PRs are story evidence and create no ninth harness task. For each runnable row, fetch the bound default-branch tip, create `feature/forge-lean-upgrade-<client>` in a sibling worktree, run upgrade and history compaction, then run vendor integrity, the client's declared checks and CI. Never use a dirty MyClaw checkout head, stash, reset, force, or touch Toolshed while paused. Record source revision, base, migration result, PR, commit and logs. An unsafe or paused row does not stop independent rows, but Integration refuses while any row remains unresolved.

Portable captures `./forge findings patterns` before and after work. The historical `reviewed-separately ×3` and `repository-escape ×3` classes already have the accepted 0005/0028 consolidation: `_preflight_upgrade`, checked `_replace_path`/`_keep_path`, and `assert_target_destination`/`assert_target_file_destination`. Audit every changed read/copy/delete against those helpers; retain the raw-write tripwire and leaf/ancestor/malformed-state refusal tests with unchanged external sentinels. Historical aggregation has no resolved flag, so zero old rows is not an acceptance condition. Any new/changed recurring class, unresolved current finding, raw-write violation or escape failure stops affected mutation and uses the existing scope-change/deferral route. Preserve the hard-link/TOCTOU deferral; do not invent another refactor merely to erase historical counts.

The committed Claude and Codex hook configurations are the normative tool inventory. Claude captures completed `AskUserQuestion`; Codex captures completed synchronous `request_user_input`; asynchronous issuance is guarded but is not completion evidence. `check_dual_runtime.py`, focused hook tests, and the recorder-produced automated report are proof. Existing event writes remain best-effort diagnostics under Decision 0017 and cannot certify a gate.

Native lifecycle observability follows constitution 05 and 07. Whenever an accepted, starting, running, retrying, cancel-requested, canceled, failed or succeeded transition occurs, it emits one durable structured JSON record with the required timestamp/level/static-message/context/environment/service/module/correlation/account fields and request/event IDs when applicable. Correlation binds story/task/launch/session/process/stage; prompts, tokens, credentials, raw environment values, PII and whole request objects are redacted. Existing retries remain bounded and idempotent and retain prior failures; cancellation records revocation before signals and reaches one truthful terminal result. A top-level native launcher/supervisor `Exception` boundary converts every otherwise-unhandled exception into one sanitized stable-ID terminal failure and nonzero result, and increments durable structured `forge_native_unexpected_errors_total` exactly once with bounded service/module/outcome labels and matching correlation. Native lifecycle tests prove fields, correlation, redaction, retry/cancel ordering, terminal uniqueness, boundary propagation, nonzero failure and metric increments. Integration cites separately produced native, Mac CLI/Desktop and Task tracker logs; one source cannot certify another.

## Decisions

Frontmatter attests all 57 active decisions. Accepted 0067 amends only the physical review publication and early draft-PR clauses of 0064 and 0054; every other accepted rule remains active. Decision 0053 keeps coordinator changes between tasks, 0059 owns workspace-first tasks and empty-dependency fallback, 0060 retains narrow POSIX signal restoration, 0065 owns platform proof, and 0066 owns the current model/team policy. Decision 0011 keeps review with the orchestrator; proposed 0049 remains historical context. First and Lean use the incumbent gates until their replacements ship. No fabricated record skips an existing prerequisite.

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

Retain Python 3.11 and uv. Pin the existing toolchain in one file: Ruff 0.16.6, Pyright 1.1.411, pytest 9.1.1, pytest-xdist 3.8.0, and psutil 7.2.2. Ruff supplies the required linter and formatter; Pyright is the existing type checker; pytest, xdist and psutil are already used by the suite and lifecycle code. Follow `constitution/README.md`, the applicable conduct rules in `constitution/09-agent-conduct.md`, exception handling and the shared path-boundary invariant; apply ponytail to each edit. No new framework or duplicate abstraction is needed.

## Task Decomposition

These overlapping tasks remain sequential, each with its own scope, tests, proof, PR and real predecessor marker. This table controls harness-task UI ownership; the separate client is described in Verify Plan.

| Label / exact task ID | Complete boundary | Depends on | user_facing |
|---|---|---|---|
| First / NATIVE-FOREGROUND-ACTIVATE | Exact foreground allocation plus the Decision0066 model-policy overlay; C9/C10, one helper call, one immutable raw-plus-three-lens generation and one pointer, workspace, guards, cleanup, clear and live boundary proof. | none | false |
| Lean / LEAN-WORKFLOW | Single brief/authorization/design applicability, complete inputs, phase/workflow ownership, rulings and generated budgets. | NATIVE-FOREGROUND-ACTIVATE | false |
| Native lifecycle / NATIVE-LIFECYCLE | Detached read-only helpers plus jobs/status/cancel/resume/explore and process-tree recovery; implementation writers stay foreground and stage-bound; structured correlated/redacted lifecycle logs, bounded retry and truthful terminal errors. | LEAN-WORKFLOW | false |
| Shared / SHARED-COORDINATOR-JOURNEY | Structured-question identity, zero-human-round closure, workspace-first attach, owner/board/queue, safe resume/seals, PR retry, and between-task coordinator changes. | NATIVE-LIFECYCLE | true |
| Portable / PORTABLE-DELIVERY-MIGRATION | Client-safe setup/adopt/upgrade and retention capability preserving the First-owned project agent registry; it ships before the separate four-client rollout. | SHARED-COORDINATOR-JOURNEY | false |
| Format / FORMAT-SOURCES | Commit exact pinned requirements and final Ruff config, then perform full pure mechanical Python formatting with equivalence/preservation/test proof. | PORTABLE-DELIVERY-MIGRATION | false |
| Quality / QUALITY-BASELINE | Consume Format's pins/config byte-for-byte; own Pyright config, semantic Ruff/Pyright repairs and mandatory identical local/CI source/test enforcement. | FORMAT-SOURCES | false |
| Integration / FORGE-COORD-1.1 | Integrated AC1–12, completed four-client rollout, required local Mac/CI proof with live-platform limitations and referenced separate-client marker, one formal combined review, functional proof and ordinary PR/CI. | QUALITY-BASELINE | false |

## Risks

An absent or ambiguous task owner must not downgrade task proof to story proof. Preserve owner/base/seal fields on resume and refuse cross-task proof selection. Hydrate actual grill rounds, not withdrawn plan-mode markers. Missing required runtime/CI evidence and unresolved client migration are proof gaps; unavailable Linux/Windows live observations are explicit accepted0065 limitations. No fixture, historical marker or preparation test substitutes for actual target/platform evidence.

## Verify Plan

Each task owner runs and records the declared regressions and repository verifier, then carries that task's review/fix loop through PR and green CI in its own worktree. Local, committed-CI and board readers must agree before marker/PR mutation. Shared's actual UI receives functional proof; other internal harness tasks do not acquire UI scope just because their CLI is visible.

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

The user's approved dogfood exception authorizes Main, only after the Quality task marker reaches trunk, to create one fresh `/tmp` Task tracker client, one private origin through the existing authenticated Git/GitHub route, and its CI solely as acceptance proof for this story. It creates no hosted application, deployment or reusable client-CI machinery. The planned client leaf is `TASKTRACKER-1/TASKTRACKER-1.1`, explicitly `user_facing: true`; its implementer owns code/automated proof and its functional-checker owns real UI functional proof with required skills. Acceptance proves a clean harness install followed by the client's declared lint, type, build and test commands, then recorded create/list/complete persistence through the UI and storage path. The client owns `tests.json`, `verify.json`, `reviews/` and its task PR/CI. Integration remains `user_facing: false` and refuses until the exact client task marker, reviewed PR, green CI and functional proof match the cited client repository/commit. It consumes exact client repository, commits, PR, artifact paths and logs in its own automated report. It cannot copy client authority or credit client code as a harness contribution; the separate lifecycle adds no ninth harness task or fake cross-repository task ID.

Integration uses the existing automated schema/recorder with `generated_by: implementer` and existing `status`, `summary`, `commands_run`, `pass_fail_summary`, `remaining_gaps`, and `blocking_findings`. Encode `pass_fail_summary` as a JSON array string with exactly the six labels in declared order. Every row has exactly `label`, `status`, `evidence_kind`, `os`, `cpu`, `revision`, `runtime`, `commands`, and `logs`; status is passed/failed/unobserved, unavailable runtime is null with an explicit remaining-gap explanation, and commands/logs are arrays. The Integration-owned validator uses `json.loads`, rejects malformed/duplicate/missing/contradictory rows, resolves log references against the tested revision, requires exact client evidence, and derives aggregate status. Independent review checks the same logs. C10 consumes the review-bound aggregate rather than parsing this encoding. No schema property, second report, matrix registry, or second authority is added.

Accepted0065 requires actual local Mac CLI/Desktop observations and meaningful Ubuntu24.04 x64/native Windows CI regressions plus exact `@openai/codex@0.153.4` package/version/help smoke. Version 0.153.4 is locally observed, already used by the frozen cross-platform fixtures and above the required model-support floor, so it minimizes unrelated Mac/Linux/Windows variables; changing it requires a contract amendment. Each row states passed/failed/unobserved, evidence kind, exact tested revision, OS/CPU/build, real commands/interactions and durable logs. Linux/Windows CLI-labelled CI rows explicitly state that unavailable authenticated runtime behavior is unobserved; only the Linux and Windows Desktop rows may remain unobserved. Local Mac CLI and Desktop rows are mandatory and cannot be waived as a limitation. Accepted limitations remain in remaining_gaps; actual failures and missing required evidence appear in both gaps and blockers. Aggregate status passes only when the four required rows, other task checks and client proof pass with no blocker. Never claim live Desktop from CLI/CI, nor native Windows from WSL. Observe the required real Mac hooks, protected write boundary, admitted contribution and terminal outcome, plus supported optional questions or the permitted main-chat route. QUALITY-BASELINE implements these OS CI jobs in its existing owned workflow, retaining existing full-suite and Windows gates; Integration consumes the actual logs. Preserve Claude regressions.

Close only after all eight task markers reach trunk, all 12 criteria and activated quality pass, required local Mac/Linux/Windows CI proof passes with live-platform limitations stated, required client proof/CI is green, migration outcomes are honest and the existing story outcome is recorded. Closeout adds no second story review.
