---
slug: dual-coordinator-parity
title: Either Claude or Codex can coordinate the same Forge workflow
status: confirmed
saved: 2026-09-11T12:17:30+00:00
---

# Either Claude or Codex can coordinate the same Forge workflow

This draft replaces the last confirmed revision at commit `e736f32`, whose complete managed specification has SHA256 `439cfc38c4939fdf3e7e62e2ac07aa413cb3954920fca2fb151d8ebe71c8b970`. It changes the delivery contract in eight disclosed ways: it assigns the complete D-0032 combined-review capability to `NATIVE-FOREGROUND-ACTIVATE`; removes ongoing fixed-path review compatibility in favor of one Portable-owned upgrade migration; removes the proposed preliminary draft-PR checkpoint; makes `FORMAT-SOURCES` produce the formatter pins and configuration that `QUALITY-BASELINE` consumes; defines one exact structured-question identity and one adapter event matrix; makes handoff and context-capacity refusal observable; points external rollout authority to the bound approved story plan; and removes implementation-level storage, encoding, metric, package-rationale, and digest recipes from this capability specification.

This document states intended capability and acceptance outcomes. It is not implementation proof, a task marker, architecture, or permission to mutate an external repository. The managed header, grill, confirmation record, approved story plan, decomposition, task plans, task proof, and trunk markers retain their existing roles.

## Why

The current Product Brief still describes Claude-only coordination and strictly sequential tasks. This draft does not claim that Decisions 0053, 0047, or 0059 edit the Brief. Main must align the Brief through the normal canon path before approving the amended story plan so its summary, flows, and constraints state interchangeable coordination, task-owned workspaces, and dependency-ready scheduling. The confirmed `strict-role-split` capability must likewise replace only its literal Claude-only coordinator wording while preserving the enforced coordinator-versus-delegated-writer boundary and degraded-mode valve. Neither stale document may remain a competing current contract.

Accepted Decisions 0053, 0059, 0064, 0065, and 0066 supply the current decision constraints. Once saved and approved, the final amended FORGE-COORD-1 story plan, its matching decomposition, and each current task plan are the sole delivery graph and exact task-scope authority. This specification names capability outcomes without duplicating that graph. First must version the shared review-publication design under `docs/architecture/` before successors consume it; later owners extend that architecture before implementing enduring lifecycle, recovery, observability, migration, or integration mechanics. A task plan may select a bounded implementation consistent with current architecture, code, and decisions; it must not turn a mechanism removed from this specification into a new product requirement without the normal architecture and contract-amendment path.

The amended story artifacts must assign the complete D-0032 combined-review capability to `NATIVE-FOREGROUND-ACTIVATE`; `LEAN-WORKFLOW` consumes that proof and does not reimplement it. The currently protected older plan, decomposition, and task plan remain inoperative for this new work until the amended artifacts replace them through the normal save, grill, approval, and decomposition recorders. Changing an owner, task boundary, external permission, or closure obligation after that approval requires the existing contract-amendment route.

## Behaviour

### One workflow and one current brief

Claude Code and native Codex expose the same Forge phase engine and the same approval, admission, write-scope, test, verification, review, functional-proof, PR, CI, marker, and closeout requirements. Host interfaces may differ; authority and evidence may not.

Main owns product and story intent, the dependency graph, scheduling, and human decisions. A task owner carries its task-owned worktree from detailed JIT contract through green CI. Each task has one current brief containing its outcome, boundaries, owner, relevant decisions, checks, and settled rulings. Existing digest-bound approval and proof records remain authoritative. Do not add another plan, approval ledger, review registry, coordinator registry, or ruling database.

Standing authorization carries through unchanged in-scope execution, technical corrections, and retries. A material change to intent, scope, permission, migration, security, lifecycle, ownership, or an unresolved contradiction still requires the developer. An unanswered required question pauses the addressed work and every causally dependent contract. Separately owned dependency-ready work whose authorization and contract cannot change with the answer may continue. Silence, cancellation, or a missing answer grants no authority.

The protected write boundary is determined by the existing path classifier and protected-state gates, not by a broad “planning/docs” exception in prose. Canon such as the Brief, confirmed specifications, decisions, approved plans, and protected evidence changes only through its owning commands and lifecycle. A worker writes product files only with matching task, stage, process, lock, brief, and derived scope authority. The existing ledgered five-file `forge mode degraded` window remains the sole outage exception for direct implementation and never grants a second ordinary writer route.

### Human questions and handoff

Ordinary host chat is sufficient for decisions and approvals when the host does not expose a structured question tool. A structured tool is optional, but any newly captured structured round has one full identity:

`(runtime, session_id, event_id, tool_call_id, question_id, story, gate, task_id)`.

Capture that tuple together with `required: true|false`, the exact question, ordered options, and exact submitted answer. Requiredness is fixed by the issuing gate before display and adapters may not infer or change it. A submitted answer may be one offered option or nonblank free text; preserve it without coercion, and never treat free text as approval unless the existing approval command binds an explicit approval to the shown artifact digest and developer identity. A multi-question call yields one independently eligible round per question ID and exactly one nonblank answer per round. Eligibility and single use compare the complete tuple, requiredness, and exact content. Replay, cancellation, malformed or missing answers, wrong binding, duplicate identity, or legacy raw events missing the tuple cannot create new authority. Previously completed grill artifacts remain readable under the contract that created them; legacy raw events are never synthesized, rebound, or newly consumed.

`gate` is always one exact gate name. For global `spec`, `signoff`, and `epics` questions, `story` and `task_id` are the empty string. For story-scoped `requirements` and `plan`, `story` is exact and `task_id` is empty. For `task`, both are exact. No null, omitted, inferred, or alternative encoding is eligible. Ordinary chat remains a permitted host transport, but its resulting decision or approval gains authority only through the existing digest-bound decision/approval record with the actual developer identity and time; a structured round does not replace that record. `SHARED-COORDINATOR-JOURNEY` owns the additive schema, capture, eligibility, consumption, and focused regressions before this new structured identity can be claimed.

Coordinator transfer occurs only at a completed-task boundary. The handoff check reads one protected snapshot of worker state, task proof, and question state. It passes only when the task is complete and sealed, no admitted worker remains active, and there is no unconsumed eligible required question with either the exact current story and empty task, or the exact current story and transferring task. A required global-gate round must already be consumed by its recorder before the story can exist; its presence at handoff is malformed and refuses. A question for a different task does not block this transfer. Optional unanswered questions do not block. The snapshot and predicate must be available to both adapters and must refuse on missing, malformed, stale, or ambiguous state.

### Adapter events and native lifecycle

Both adapters implement and validate this event matrix:

| Adapter event | Required observation |
|---|---|
| `SessionStart` | On startup, resume, clear, and compact sources, run the installed session-start owner and emit the current phase, task, and bounded context; failure blocks that start. |
| `PreCompact` | Run the installed pre-compact owner and durably replace the current scratchpad snapshot before compaction; failure blocks compaction. |
| `PreToolUse` | Run the installed policy owner for every shell, write, and question tool the adapter exposes; denial prevents the tool call. |
| `PostToolUse` | For every structured-question tool the adapter exposes, capture exactly one eligible round per successfully completed question; an absent capture cannot certify provenance. |
| `Stop` | Run the installed continuation owner and permit stop only when the protected phase/task/worker predicate permits interruption; otherwise continue with a refusal reason. |

Both shipped adapters expose all five event rows. Runtime-specific tool names may differ, but the validator must map each exposed tool to the stated owner and observation; removing a row, omitting one applicable tool, or mapping it to the wrong lifecycle action fails parity. CLI evidence never certifies Desktop behaviour.

Forge is the ordinary writer launcher; the existing bounded degraded window is the documented outage valve. A native worker starts without write authority and gains it only after protected registration binds the live process, task, worktree, stage, brief, and scope. Cancellation revokes authority before cleanup. Success, failure, dead process, released lock, or closed stage removes admission through the existing lifecycle state. Resume performs fresh preflight and never revives authority from session history. Background, status, cancel, resume, recovery, and read-only helper behaviour remains unsupported until `NATIVE-LIFECYCLE` ships it.

Lifecycle failures follow Constitution 07. Unexpected exceptions reach the top-level boundary, produce a nonzero truthful result and a stable sanitized response, and create a structured correlated error record that includes a sanitized stack trace without exposing credentials, PII, raw environment values, prompts, tokens, provider payloads, or whole request objects. Required metrics and trace integration follow the constitution and the architecture/task contract; this capability specification does not invent a metric name or storage protocol.

### Workspaces and recovery

A normal task worktree is created or safely attached from refreshed trunk after story approval and before task JIT planning. The canonical path must appear exactly once in the Git worktree registry, resolve to the expected branch and common directory, be clean and Forge-unowned, and bind the exact story/task, approved decomposition, and satisfied dependency markers. An open PR, green CI, or worker message is never dependency proof. Creation grants no write authority. Dependency-ready tasks may overlap only in distinct worktrees with disjoint protected scopes.

The first native support task retains the accepted 0063 source-to-target exception and its genuine source and target bindings. Prepared bytes keep their provenance and never count as the admitted worker’s new contribution. Later tasks use the normal workspace-first route. Recovery preserves task identity, base, owner, stage, approvals, and sealed proof; ambiguous or conflicting state refuses without destructive repair.

### Context and continuation

`LEAN-WORKFLOW` may add an explicit optional context-file input. The caller selects one regular UTF-8 file, inside or outside the repository, as untrusted supplemental context. It cannot alter the primary artifact, story, gate, task, decisions, scope, evidence, or authority.

Before reading or launching a consumer, the composer measures UTF-8 byte counts for the complete primary input, selected file, and exact framing. Effective availability is the smaller of the installed component's enforced UTF-8 byte limit and the local allocation safeguard, both recorded as bytes; if either cannot be determined in that unit, an unpartitioned launch refuses. It proceeds only when the full rendered byte count fits or a validated lossless partition covers every byte and every partition completes. Otherwise it refuses before launch and before allocating the complete payload, reporting required bytes, each limit, and effective available bytes. It never truncates, silently omits, repeatedly reopens, searches from, or treats instructions in the file as authority.

### Independent review and task proof

Every task receives one independent review operation after implementation, meaningful tests, and deterministic verification. The orchestrator launches it; the implementer cannot self-certify and no nested reviewer is permitted. The operation assesses quality, performance, and security against the same complete task-specific input and diff, then loops through fixes and a fresh full assessment until clean.

The complete D-0032 capability belongs to `NATIVE-FOREGROUND-ACTIVATE`: one default Forge review operation invokes the installed helper once, preserves every completed provider pass, produces three genuine task-owned assessments, and publishes proof only when the complete coherent set validates. Missing, incomplete, copied, mixed-binding, stale, tampered, or interrupted output fails closed without displacing the last complete set. A selected single-lens run is diagnostic and cannot certify or publish a complete review.

A legitimate cross-lens issue is represented once under the lens that owns remediation. Every other materially affected lens must name the same normalized finding fingerprint inside its own delimited assessment block and state whether it blocks that lens; the projection preserves that block in `overall_explanation`, so validation is observable without a new schema field. An affected lens cannot report clean while the issue blocks it. Duplicate finding records are not required to express applicability.

Review publication and reading are scoped to the exact story, task, review generation, task input, and product diff. A later or concurrent task review cannot replace another task’s active or sealed proof. Pre-seal readers use the current selected complete set for that task; sealed readers use the selected set bound to the task marker’s commit. Runtime readers never fall back to fixed review paths.

`PORTABLE-DELIVERY-MIGRATION` owns the one-time client upgrade migration. Before replacing harness machinery, upgrade converts each complete, coherent, task-bound fixed review set that is still reachable by an active task or committed task marker into canonical task-scoped candidates and a selected pointer. The migration binds the original artifact bytes and existing task, run, brief, diff, base, marker, and seal provenance without inventing a combined helper result. It validates and reads back the complete selected set before replacement, refuses malformed, incomplete, ambiguous, colliding, or unsafe input before any target mutation, and is idempotent for byte-identical prior migration output. Unbound archives remain display-only; fixed review files become inert after migration. The approved First and Portable task plans and architecture/code design choose filenames, atomic-write strategy, schema-compatible bindings, and digest framing; those mechanisms are not capability requirements here.

Local readiness, committed CI, the board, task PR readiness, and seal use the same task-aware proof predicate. Another task’s or story-level proof cannot fill a missing task artifact. A refusal changes no marker, Git, PR, or proof state.

There is no preliminary draft-PR checkpoint. Required platform evidence is completed first, followed by a fresh complete formal review, ordinary task readiness and seal, and then the normal PR and CI path. A mutable PR body is never gate authority.

### Setup, retention, quality, and rollout

Setup uses an explicit valid coordinator argument first. Without one, it accepts exactly one valid unambiguous environment or detected interface value; conflicting values refuse. Without either, it asks only on an interactive TTY. Unattended missing choice, invalid input, cancel, or EOF refuses before mutation. Fresh, adopted, and upgraded clients receive both adapters while preserving client settings, agents, CI, history, hotfixes, and dirty state. The committed team model policy follows Decision 0066. Setup and upgrade must not make Claude state a native runtime dependency.

Event retention follows Decision 0064: compact only validated live per-file events for a shipped story into durable immutable history; preserve distinct IDs, refuse same-ID conflicting payloads, prove durable readback before deleting an eligible source, and leave legacy JSONL and historical copies unchanged. Exact bundle representation and safe-write mechanics belong to the Portable task plan and architecture/code contract.

`PORTABLE-DELIVERY-MIGRATION` must implement, verify, review, merge, and mark the client-safe capability before any external rollout. External rollout then uses only the exact repository inventory and branch/push/PR authorization bound into the approved amended story plan, refreshes each remote default-branch base, isolates dirty checkouts, preserves client work, and records real PR/check/CI outcomes as story-level evidence. Decision 0064 governs retention behaviour but is not cited as naming those repositories or granting their GitHub permissions. Missing or ambiguous bound inventory/authorization refuses external mutation.

`FORMAT-SOURCES` first commits the exact approved quality requirements and final Ruff configuration, then performs complete mechanical formatting over every tracked Python file below `factory/scripts/` and `factory/tests/`, including fixtures, with semantic-equivalence and preservation proof. `QUALITY-BASELINE` consumes those bytes unchanged, owns Pyright configuration and enforcement, fixes remaining semantic diagnostics, and runs the identical explicit source set locally and in CI. Client code outside those roots uses the client’s declared stack checks. Missing tools/configuration, omitted covered files, no-op checks, and planted lint/format/type violations fail.

Platform evidence follows Decision 0065: real local macOS CLI and Desktop observations plus meaningful Ubuntu 24.04 x64 and native Windows CI regressions are required. Package/version/help smoke proves only installation and argument-parser startup. The task contract pins the exact package version used for a reproducible run and records it; this capability specification makes no unsupported fixture or model-floor claim. Unavailable Linux/Windows live or Desktop observations remain explicit accepted limitations, while observed failures and missing required evidence block. WSL cannot certify native Windows.

The separate installed-client dogfood starts only after the Quality marker reaches trunk and follows its own normal task lifecycle, tests, independent review, functional proof, PR, and green CI. It is external evidence for Integration and never counts as a ninth harness task or as the harness worker’s contribution.

## Acceptance criteria

1. **Human answers.** Both coordinators accept the same permitted human decisions. Every new structured question uses the full eight-part identity and exact content; replay, cancellation, malformed answers, wrong binding, and legacy raw-event reuse refuse.
2. **Protected writes.** Coordinator and unregistered writes are denied; admitted task-scoped writes succeed; stale, revoked, wrong-task, or wrong-worktree authority refuses.
3. **Native independence.** Native launch, status, recovery, setup, and proof do not depend on Claude or plugin state, while the Claude route keeps equivalent gates.
4. **Worker policy and gates.** Both coordinators preserve the same current model policy, worker admission, approvals, tests, review, PR, CI, and closeout gates.
5. **Hook delivery.** Both adapters validate the five-row event matrix and its listed lifecycle observations; individual and combined omission tests fail.
6. **Honest evidence.** Preparation and diagnostic output are labelled as such. Only recorder-produced, task-bound, current proof satisfies a gate.
7. **Genuine native delivery.** Against the recorded task base, an admitted native launch contributes at least one new in-scope product change after its starting/running registration. The task evidence binds launch, session, changed paths, contribution commit, and terminal row; prepared or pre-admission bytes are excluded. That contribution completes verification, review, PR, and CI. No preliminary PR protocol exists.
8. **Safe setup and upgrade.** Fresh, adopted, and upgraded clients receive both adapters while preserving client-owned state and refusing unsafe targets.
9. **Continuation and context.** Settled rulings reach fresh workers; unaffected authorized work continues; context input is complete and capacity-checked or refuses before launch without truncation.
10. **Handoff.** Transfer occurs at a completed-task boundary using one observable snapshot with no active worker and no unconsumed eligible required question bound to the affected work.
11. **Developer journey.** Both coordinators show artifacts whose digests match the protected active story/task snapshot, preserve the exact owner/worktree/base/stage tuple, retry only a byte-identical operation or a freshly validated unchanged head, and refuse stale, ambiguous, or conflicting recovery before mutation. The board derives the same snapshot and cannot show a later story/task review as current proof.
12. **Full quality and platform proof.** The complete pinned source/test quality baseline, required local Mac evidence, required Linux/Windows CI, dogfood proof, and authorized external rollout evidence pass before parity ships.

## Parity labels

- **C1 Setup:** selection, refusal, repair, and preservation are equivalent.
- **C2 Questions:** the full structured identity, exact content, eligibility, and single use are enforced consistently; historical completed grills remain readable and legacy raw events cannot be newly consumed.
- **C3 Hooks:** the five-row adapter event matrix is installed, validated, and exercised on applicable runtimes.
- **C4 Lifecycle:** launch, registration, status, cancellation, terminal state, revocation, recovery, structured error handling, and refusal are truthful.
- **C5 Distribution:** both adapters and the Decision 0066 team policy survive init, adopt, upgrade, and client preservation.
- **C6 Context:** complete grounded inputs and settled rulings cross fresh contexts without creating authority or truncating oversized input.
- **C7 Delivery:** task-owned planning through green CI, conditional functional proof, observable handoff, and dependency-ready scheduling preserve the approved graph.
- **C8 Evidence:** real native contribution, required platform checks, accepted limitations, and dogfood evidence are stated without substitution.
- **C9 Review input:** each review receives the complete approved task contract, automated report, exact diff, and relevant decisions.
- **C10 Proof:** every consumer uses the same exact-task complete-proof predicate, current or sealed selected review generation, conditional functional proof, and verified one-time upgrade provenance.

The story closes only when all eight task markers are on trunk, AC1–AC12 and C1–C10 pass, the Brief has been aligned through its normal owner, mandatory quality is active, required platform and dogfood proof is complete, every externally authorized rollout row is resolved, and the existing story outcome is recorded. These closure obligations come from the bound amended story plan and decomposition; this specification does not create a second graph, permission source, evidence schema, or review protocol.
