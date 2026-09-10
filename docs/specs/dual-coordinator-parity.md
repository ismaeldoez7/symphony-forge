---
slug: dual-coordinator-parity
title: Either Claude or Codex can coordinate the same Forge workflow
status: confirmed
saved: 2026-09-10T20:45:49+00:00
---

# Either Claude or Codex can coordinate the same Forge workflow

This revision retains the coordinator contract and acceptance coverage while
applying accepted Decision 0064. Its managed frontmatter and confirmation
records determine approval status. Specification text supplies neither an
implementation claim nor a task marker or proof artifact.

## What changed in this revision

Compared with the confirmed 824baed4 revision of the source specification,
this draft applies accepted 0064: one current task brief, risk-based coherent
task boundaries, carried standing authorization, one combined lossless review,
and durable event/client retention. It also applies accepted 0066's current
execution lanes and committed team-agent distribution contract. It removes only
repeated ceremony and the obsolete fixed 120000/180000-byte clauses. It also
carries the ten audited client failures into explicit owner obligations. The prior confirmed revision
and its comparison remain recoverable through the existing Git artifact and
approval records; this revision does not replace those records.

## Why

Developers must be able to use Claude Code with its existing Codex
rescue/companion route or native Codex CLI/Desktop as the Forge interface.
Changing the coordinator must not change the phase engine, human approvals,
worker policy, protected authority, tests, review, evidence, or shipping gates.
Native preparation exposed missing human-answer provenance, runtime
registration, setup ownership, worker admission, and task-proof paths. Prepared
native bytes retain their source and review provenance. An approved support
task reviews and delivers them completely, but they are never credited as that
worker's new contribution.

Decision 0064 makes one current task brief the working contract. Main retains
project/story intent, dependency graph, scheduling, and required human
decisions. Each task owner takes its own worktree through JIT planning,
delegated implementation, tests, verification, review, PR, and green CI.
Existing approval, admission, proof, and trunk-marker records remain the
authority. Repeated story/task grills, approval ceremonies, and separate review
launches are removed only when they duplicate the same current binding. A
material new choice, changed intent or scope, missing authority, or
contradiction still stops dependent work for the developer.

The installed autoreview helper has an observed 512000-byte prompt capacity
and lossless chunking. This is tool capacity, not a new Forge policy. The old
120000-byte product and 180000-byte review limits are removed from this
contract. Boundaries follow coherent behavior, ownership, changed file/line
risk, and actual complete review capacity. In the roadmap and 0058, "existing
review limits" means the installed helper's enforced safeguards and complete
lossless coverage, as amended by 0064; 512000 is an observation, not a pinned
replacement limit. Do not edit or override helper capacity to admit a task.
Remeasure the entire final input, use supported chunks, and split the task if
complete input cannot fit the helper's actual safeguards. No input may be
truncated, omitted, or declared clean without all three assessments.

## Behaviour

### One contract and shared authority

Main owns confirmed intent, story planning, the frozen decomposition,
dependency scheduling, story decisions, and the human conversation. Each task
owns one current brief containing behavior, boundaries, owner, tests, review
focus, relevant decisions, and settled rulings. Derive execution and review
inputs from that brief and existing digest-bound plan, approval, and proof
records. Do not add another plan, approval ledger, review registry,
coordinator registry, or protected-ruling database.

Standing authorization covers unchanged in-scope work, technical corrections,
and retries. Bind concrete revisions through existing commands and recorders.
When a decision is needed, present the changed artifact with one concise
recommendation, tradeoff, and consequence. Silence, continuation, workflow
status, mode change, or technical pass is not approval. Accepted Decision 0064
narrows Decision 0057's older pause-all wording: while a required question is
unanswered, pause the addressed task, gate, or artifact and every task whose
authorized facts, dependencies, scope, or contract could change with the answer.
Continue only separately owned dependency-ready work whose bounded contract is
unaffected. Shared intent, scope, authority, or contradiction questions pause
every affected task. Cancellation or a missing answer grants no authority and
leaves that dependent set paused; an optional factual question does not stop
already authorized work. Carry settled rulings through the existing task
brief/contract and recorder family into every fresh worker and reviewer.

For this story, accepted Decision 0053 is the targeted amendment to the
BRIEF's Claude-only coordinator wording, and accepted Decisions 0047 and 0059
replace its one-story-worktree/sequential-task wording with task-owned
worktrees and dependency-ready scheduling. The rest of the BRIEF remains in
force. SHARED-COORDINATOR-JOURNEY owns the later wording alignment in
`docs/product/BRIEF.md`; the stale literals grant no competing runtime
authority in the meantime.

Both adapters use the same Forge phases and protected state. Coordinator
product/canon writes remain locked. Planning/docs, recorder-mediated evidence,
prototypes, and normal Git operations retain their existing exceptions. A
delegated worker writes only when registered admission, stage, brief, task
digest, process identity, and derived scope match. Environment claims, copied
workspace state, and role names cannot grant authority.

Decision 0066 supersedes Decision 0062's model policy. Read-only exploration
uses Sol/low. Planning, decomposition, architecture, plan validation, and every grill
use Sol/high. All implementation and autoreview fixes use Sol/medium, except
formal Lite, which uses Luna/max. Formal autoreview and functional checking use
Sol/high. No new execution actor may use Terra. Claude coordination keeps the
same `codex-plugin-cc` route, including Luna/max Lite; `forge doctor` proves
that exact official installation supports max or repairs only a recognized
official source and otherwise refuses before mutation. Forge remains the
launcher; direct native writer or certifying-griller transport is deferred.
Decision 0066 also amends only Decision 0057's three-agent removal and omitted-
delivery clauses: all 15 definitions remain shipped. It amends only Decision
0065's existing-First-scope clause and the matching recorded scope lesson for
the later explicit model/team overlay; every original prepared path/hunk owner,
the source/target binding, and the eight-task graph remain unchanged. Decision
0057's other question requirements, as narrowed by accepted 0064, plus its
roadmap-edit, phase-role, and gate requirements and all other Decision 0065
obligations remain active.

### Human interaction and exact question identity

Required decisions and approvals use the host's permitted interface. In Codex
Default, main asks required questions and approvals in ordinary chat; the
synchronous request-user-input tool is optional and host-permitted. Claude
keeps AskUserQuestion. No manual Plan-mode switch, asynchronous approval
tool, private host patch, or repeated “continue” is required. Optional
unanswered questions do not stop work supported by existing facts.

After SHARED-COORDINATOR-JOURNEY ships, every newly captured structured-question round must preserve and consume the
full identity `(runtime, session_id, event_id, tool_call_id, question_id, story,
gate, task_id)` together with the exact question, ordered offered options, and
submitted answer text. Bind gate/story/task at capture: task ID is required and
exact only for the task gate, story is exact for story-scoped gates, and
inapplicable values are empty. Never infer or rebind identity at consumption.
Native certification reads the completed PostToolUse payload. One completed
multi-question call produces one candidate round per unique question ID; each
question must resolve through `tool_response.answers[question_id].answers` to
exactly one nonblank answer. Answers for sibling question IDs are not multiple
answers for that round, and consuming one question cannot consume or reserve a
sibling. The raw request notification, serverRequest/resolved event,
cancellation, error, cleanup acknowledgment, empty result, duplicate identity,
or zero/multiple answers for one question cannot certify it. Retain exact
submitted offered-option or free-text text without coercion; free text is not
approval. Eligibility and single-use consumption compare the whole identity and
exact content. Replay, mismatch, wrong gate/story/task, malformed payload,
cancellation, and missing event refuse. Question age adds no expiry. Previously
completed grill artifacts remain readable under their historical contract;
legacy raw records missing the full tuple are not synthesized, upgraded, rebound,
or newly consumed. Shared owns the additive schema, capture, migration,
eligibility, and consumption work; Lean cannot reassign this provenance.

After LEAN-WORKFLOW ships, each approval-bound artifact records
`design_review: required|routine` and `design_review_rationale: <text>` in its
existing frontmatter. Missing/unknown classification or a blank rationale
means required. Required is mechanical when the proposed behavior changes any
allowed actor/write/read/sandbox/credential/network boundary; deletion,
overwrite, move, external side effect, or other non-reversible operation;
stored-data schema or migration; public CLI/API/evidence schema; lifecycle
state machine; or ownership boundary. Routine rationale must state that none
of those exact triggers changes. The grill checks the artifact against that
list and refuses an incorrect routine claim; workers cannot downgrade the
human-approved value. Signoff is always required because it commits product
scope, so the legacy BRIEF needs no new classification frontmatter. Epics is
required if any referenced capability is required or missing classification.
Both adapters use the same phase-engine predicate. Classification and its
rationale are authored, digest-bound content, never excluded managed metadata.
The following existing inputs own the classification and proof binding:

| Gate | Classification input | Existing record and binding |
|---|---|---|
| spec | Selected capability Markdown | Global grills/spec.json; exact spec SHA256. |
| requirements | Story-linked confirmed capability | Story grills/requirements.json; requirements_digest(spec, product tree). |
| epics | All capability specs referenced by the proposed roadmap; any required/missing classification requires review | Global grills/epics.json; exact proposed roadmap SHA256 plus cited spec digests. No new JSON classification authority. |
| signoff | Product BRIEF and participating capability specs; always required | Global grills/signoff.json; existing commit/guarded-input freshness plus SHA256 of the complete Gate.locate handover text. |
| plan | Story-plan Markdown | Story grills/plan.json; existing authored plan digest. |
| task | Current task-plan Markdown | Story grills/tasks/<id>.json; task-plan digest plus existing protected-contract/product grounding digest. |

Use the existing evidence_path layout, Gate.locate readers and recorder digest
functions; the table adds no registry. A shared read must explicitly name every
gate, include each complete located input and grounding, and return a separate
assessed verdict/frontier for each. Each existing record retains its own exact
input binding, with the actual launch and inspected paths/digests in its
existing summary/inspected_refs. Missing inputs, unassessed gates or a changed
binding refuse. Reading common context never certifies another gate. The
current one-gate launcher grants no shared-read capability; LEAN-WORKFLOW must
implement and test this behavior before it is usable. Routine work skips
duplicate cold reads, not authorization, admission, tests, review or CI. No new
risk ledger is introduced. First retains current prerequisites until Lean ships.
The six existing grill types retain freshness, finding resolution, artifact/grounding digest,
and explicit empty-frontier checks. Top-level frontier_empty: true is canonical
for empty or populated rounds. An existing round-bearing payload may retain
final-round frontier_empty: true when the top-level field is absent; explicit
top-level false refuses. Empty rounds without canonical true refuse. Structured
rounds are eligible and single-use. A shared read shares assessment work only;
it does not share, reassign, or newly consume legacy structured-question
provenance across gates. Until SHARED-COORDINATOR-JOURNEY ships complete
question identity, a structured round used for a gate stays on the current
single-gate provenance path and can satisfy at most that gate. Decision-free
grills may pass from their grounded assessment and canonical empty frontier
without an invented question. There is no compulsory human round and no
invented answer.

For a first approval-bound artifact or material revision, save the exact draft,
identify the last confirmed revision, preserve its artifact/commit/body digest
through the existing scratchpad and committed event, show the full artifact
and comparison, and display it in main chat or a supported fallback. A
queued/stale/failed/wrong reader is not presentation. Ask explicit approval
only after display through the existing host interface; a grill or technical
pass is not approval. Ambiguous, refused, canceled, or missing answers remain
awaiting approval. An in-scope technical correction uses the existing
amendment/save and approval record family: record its reason, technical
classification, and standing-authority source in the current brief; saving the
new digest invalidates and removes the former approval tuple; then rebind the
concrete revision through the existing approval command with the actual
developer identity, explicit standing-authority attribution, current brief
digest, and fresh binding time. That records use of already granted authority
and must not claim a new answer or reread. A material choice, intent/scope,
authority, permission, migration, security, lifecycle, ownership change, or
unresolved contradiction cannot use technical classification; dependent work
remains paused until the changed artifact is displayed and explicitly approved.
The first 0063 native task keeps current source/target gates until
LEAN-WORKFLOW ships.

### Workspaces, first native task, and worker lifecycle

Under 0059, create or safely attach a dependency-ready task worktree at
refreshed trunk before that task's detailed plan or grill. Require the approved
story, its matching decomposition, exact story/task identity, fetched trunk
commit and all effective dependency markers on that trunk. An open PR, green
CI or worker message does not satisfy a dependency. Preserve the approved IDs,
order and dependency graph. `Git-registered` means the canonical target appears exactly once in the
repository Git worktree registry and resolves to the expected branch and
absolute Git common directory. `Forge-unowned` means no valid protected
`git_control_dir(target)/run.json` claims it for a task. The existing protected
`run.json` is the owner record: create or validate the worktree and hydrate its
permitted inputs first, then atomically publish that file last with the exact
story, task, branch, base commit, approved-plan digest, decomposition digest,
and task digest. An interruption before publication leaves an unowned candidate
that a retry may adopt only after complete revalidation; a malformed, partial,
stale, or conflicting record refuses without overwrite. A verified retry
returns the existing owner without resetting it or creating a duplicate.
Creation grants no product write authority. Omitted/empty dependencies follow
the immediate predecessor; an explicit list names dependencies. Concurrent
tasks require distinct worktrees and disjoint protected scopes. A task enriches
only its permitted fields.

The resolved location is part of admission identity. On attachment, launch,
recovery, and each admission check, resolve the target canonical worktree path,
absolute Git directory, and absolute Git common directory; require owner, stage,
delegation, lock, revocation, and run records from that exact worktree
Git-control directory and expected common directory. The protected ledger
location is authoritative; duplicate location fields and a new owner ledger are
unnecessary.
After trunk integration, refresh non-owner rows from incorporated trunk while
retaining the owner's contract, approvals, and stage baseline.

The first native foreground support task is the only 0063 exception. In the
planning checkout it needs a complete source contract, independent grill, and
actual approval before the existing task-start command creates its worktree.
In that target, freshly ground behavior, scope, tests, and dependencies are
written, grilled, and approved before stage start or native delegation. A
placeholder/incomplete source contract refuses; source-bound proof cannot
satisfy target proof. The first task repairs successor workspace creation
ordering. Later tasks use the normal 0059 workspace-first route. A
forge stage start --trunk route is not an alternative.

Accepted 0058 permits explicitly scoped native bootstrap support tasks to use
the validated isolated candidate. Validate exact scope, target preparation,
baseline, predecessor markers, and review boundaries before implementation.
Preserve sequential merges and normal task PR gates. Original prepared bytes
retain source, commit, and review provenance but do not count as the worker's
delegated contribution. Native write-hook activation and legitimate worker
admission land together. A preparation patch, draft graph, temporary path, or
diagnostic receipt never authorizes writes or proves release. Versioned
`plans/exploration/coordinator-parity-preparation/lean-delivery-graph.json`
assigns every original path/hunk to its complete-review owner and names the
exact reproducible preparation artifacts. The approved story plan binds its
SHA256 before any support-task contract is recorded. The committed
`native-foreground-preparation-inventory.json` in that directory binds the
first allocation to trunk 824baed4, its 109953-byte patch SHA256
bee122bb370177ededefb5fe81a82f8c600f69af8502e151956ec7b8afed29e2
and all 16 prepared file hashes. Revalidate against fetched trunk in the actual
target; local paths and source approvals do not replace target proof.

Forge is the sole launcher. An admitted worker binds launch ID, live process
identity, target worktree, stage incarnation, task contract, brief, and
derived write scope in protected Git-control state. It starts unadmitted;
registration must complete before writes. Registration/startup/process
discovery failure grants no authority. Failure before process creation records
failure without invented PID or exit code; verified cleanup precedes terminal
publication once a process exists. Cancellation creates the existing durable
revocation marker before cleanup, and failed cleanup leaves that marker.
Successful or failed completion revokes through the protected terminal row,
dead process and released matching lock; stage closure revokes through its
non-active stage incarnation. Admission checks require a starting/running row,
live matching process ancestry, held matching lock, active matching stage and
no explicit revocation, so no new completion or stage-close tombstone is needed.
Resume requires fresh preflight and launch; session identity/history never
revives authority. Companion workers still pass admission with native hooks.
Retain existing POSIX signal-mask restoration and Windows process guards.

Both routes expose the same start/running/terminal lifecycle, status, recovery,
logs, proof, and scope checks. Background success requires protected
registration; detached readers remain observable/cancelable. Read-only work
cannot satisfy a write launch. Startup, resume, clear, compaction, question,
and Stop interception use installed registrations; removing one fails
validation. CLI evidence does not certify Desktop.

NATIVE-LIFECYCLE emits one durable structured JSON record whenever an accepted,
starting, running, retrying, cancel-requested, canceled, failed, or succeeded
transition occurs. Each record uses the constitution's `timestampUtc`, `level`, static
`message`, concise `context`, `environment`, `serviceName`, `module`,
`correlationId`, and nullable `accountId` fields, plus `requestId`/`eventId` when
applicable. The stable correlation binds story, task, launch, session, process,
and stage identities without logging prompts, tokens, credentials, raw
environment values, PII, or whole request objects. Existing retries remain bounded and
idempotent, record attempt and cause, and never hide the prior failure.
Cancellation publishes revocation before signals and reaches one truthful
terminal result. Unexpected terminal errors surface with a stable
`errorId`/internal code and sanitized user-facing message; they are neither
swallowed nor returned with raw stack/provider data. Focused tests validate
field presence, correlation continuity, redaction, retry/cancel ordering,
terminal uniqueness, and failure propagation. Integration cites the resulting
native logs and separately produced Mac CLI/Desktop and Task tracker interaction
logs; one producer's logs cannot certify another surface.

Protected Git-local stage settings must be genuinely readable by the admitted
worker through an existing protected seam. A writable mirror, copied token,
environment claim, or instruction to skip lifecycle/recorders is not a fix.
A host brief snapshot is informational and cannot replace protected admission
or closeout; reproduce and test the actual denial/read path before claiming
repair.

### Setup, ownership, upgrade, and team profiles

Setup precedence is explicit --coordinator, FORGE_COORDINATOR, unambiguous
detection, then TTY choice. Empty/canceled/EOF/invalid/ambiguous/unattended
no-choice refuses before install and prints both commands. CODEX_THREAD_ID or
CODEX_SHELL detects Codex; CLAUDECODE detects Claude; both is ambiguous. Pass
the choice to both doctors without persisting it. POSIX stays ./setup; Windows
keeps forge.cmd and user-scope behavior. Codex setup does not start Claude.

Fresh, adopted, and upgraded clients receive both adapters; inert .claude is
not a runtime dependency. Existing COPY_CODEX, GATE_FILES, ownership,
conflict, replacement, and vendor-integrity rules remain authoritative.
Preserve client settings, skills, agents, CI, local configuration, history,
hotfixes, and dirty state. Refuse unsafe targets, report conflicts, and never
silently delete client files.

Commit the complete 15-definition `.codex/agents` team registry together with
`.codex/config.toml` and `.codex/explore.config.toml`. Fresh and adopted clients
receive the complete tree through the existing init copy path. Upgrade uses its
existing harness-owned name/config refresh behavior: a same-name definition is
refreshed, while distinct client-added agent files remain. It never deletes
`.codex/agents` recursively. Preserve logical phase roles, prompts, producer
identities, model policy, and gates; add no per-file merge or provenance format.

### Review, quality, dogfood, and delivery

Every task keeps deterministic verification, implementer-owned tests,
conditional functional proof, independent review, PR, and green CI. Main
launches one `forge review <task-id>` operation under accepted 0053, 0054, and
0064; accepted 0011 keeps that review invocation with the orchestrator. The
implementer cannot self-certify and nested reviewers are prohibited. On
findings, main delegates fixes and repeats review until every assessment is
clean. Proposed 0049 is not authorization for changing review execution. The first
native task uses the current three-lens execution. After LEAN-WORKFLOW ships,
one combined review has explicit quality, performance, and security
assessments bound to the same diff/input and uses the installed lossless chunk
helper. Every chunk must finish. Include formatting/AST/comments/directives,
tests, generated semantic output, and exceptions in the review. Mechanical
formatting and semantic repairs may be separate coherent tasks where risk
requires. No truncation, blanket suppression, artificial clean result, cap
override, or unassessed lens pass is permitted. Use coherent capability and
file/line risk bounds instead of obsolete byte splitting. One `./forge review <task-id>` invocation is one logical review operation.
It invokes the installed autoreview helper once with a combined prompt that
requires separately tagged quality, performance, and security assessments;
supported internal chunks do not become separate Forge reviews. The exact
validated helper JSON result retains the ordered chunk results and is the source
for three genuine task-owned lens projections. A JSON file may exist even after
the helper exits 2; `review_status: incomplete`, any missing/non-contiguous pass,
or any missing lens refuses publication regardless of file existence. Forge writes the raw result and
all three schema-valid projections as unique candidates in the existing task
review family, validates and reads back their complete input/helper/run/diff/
product bindings, then atomically publishes the existing `review-run.json`
pointer last. Readiness and seal consume only the complete candidate set named
and hashed by that pointer. An interrupted, missing, malformed, copied-lens, or
mixed-binding attempt cannot publish or replace the last complete pointer; a
preserved pointer whose branch diff or classified product changed remains stale
and cannot pass. Legacy fixed three-lens proof remains readable as one complete
legacy set. No parallel manifest, review registry, reconstructed private chunk
manifest, or hostile-worker containment is introduced.

After normal contribution and deterministic verification, run one
preliminary independent inspection through the installed autoreview helper.
While required platform results are missing, the sole durable checkpoint is a
machine-readable `forge-preliminary-inspection/v1` block in the existing GitHub
draft PR body; it records the verified origin/head-repository/head-branch/base/
current-remote-head tuple, inspected commit, exact inspected branch-diff digest,
classified-product digest, helper identity, exact raw helper result (inline or
by path, containing commit, byte count, and SHA256 to an immutable candidate
under the existing diagnostic review-brief family), findings, missing required
platform rows, and accepted unobserved limitations. Exactly one matching open
draft is reused; zero permits one create; multiple, mismatched, failed, or
uncertain lookups refuse, and an uncertain create is re-queried before retry.
Later workflow/proof-only commits may advance the head when the inspected commit
remains its ancestor and classified product content is unchanged; whole-HEAD
and recorder-commit equality are not required, and any product change requires
a fresh preliminary inspection. This checkpoint records no clean Forge proof,
creates no task marker, and never runs `forge task pr-ready`. After the required
platform report passes, generate a fresh complete brief, run the normal formal
Forge review, then reuse and promote the same PR through normal readiness while
preserving the eventual marker identity and timestamp. The PR body is the only
checkpoint authority; scratchpads and candidate payloads are diagnostic, and no
new registry or proof family is introduced.

The platform evidence contract follows accepted 0065-ci-platform-evidence,
which amends 0064's six-live-cell requirement. Require actual local macOS
native CLI and Desktop proof plus Ubuntu 24.04 LTS x64 and native Windows CI.
Keep the six existing labels for platform coverage accounting. Each row says
whether its evidence is live runtime, CI regression/package smoke, or
unobserved; a passed CI row never claims an authenticated live runtime or
Desktop interaction. WSL cannot satisfy native Windows.

The required rows are native-cli-macos and native-desktop-macos with actual
local proof, native-cli-linux-ubuntu-24.04-x64 with Ubuntu CI proof, and
native-cli-windows with native Windows CI proof. CI preserves the full Ubuntu
harness suite and existing native Windows gates, and exercises native
launcher/admission, hooks, recovery and portable-delivery regressions on the
actual runner OS. Install the real Codex CLI package as exact `@openai/codex@0.153.4` and
record its version/help smoke outcome. An authenticated native
task uses only existing authorized CI authentication when available; otherwise
state that live-task behavior is unobserved. Package/help smoke certifies only
package/argument-parser startup. Fixture normalization remains regression
proof. Required CI commands must succeed and collect meaningful tests; empty
or wholly skipped selections cannot pass.

Retain native-desktop-linux-ubuntu-24.04-x64 and native-desktop-windows as
unobserved when no genuine Desktop host is available. Their absence, and
unavailable authenticated CLI observations beyond required CI coverage, are
accepted limitations under 0065 and do not block this delivery. Record those
limitations explicitly; never mark an unrun Desktop observation passed or
infer it from CLI/CI. Any actually observed correctness/security failure,
including in a normally unobserved path, still blocks readiness.

Each row records actual OS/CPU, tested revision, runtime/build where installed,
evidence kind, commands/interactions and durable logs. Live Mac observations
identify trusted hook registrations, startup/resume/clear/compact, denied
coordinator writes, admitted work and truthful terminal outcomes. Include
completed question/event identity and mapping when an optional structured
interaction is supported and actually used; otherwise use the permitted
main-chat route and state the unavailable optional mechanism. Missing required
behavior or an observed failure blocks; optional interactions are not invented.

The final integration implementer authors the existing
`factory/schemas/test-automated.json` payload with `generated_by: implementer`;
`record_test_from_json.py --kind automated` writes
`.factory/stories/FORGE-COORD-1/tasks/FORGE-COORD-1.1/tests.json`. Use only the
existing fields `status`, `summary`, `commands_run`, `pass_fail_summary`,
`remaining_gaps`, and `blocking_findings`. Encode `pass_fail_summary` as a JSON
array string containing exactly six row objects in this order:
`native-cli-macos`, `native-desktop-macos`,
`native-cli-linux-ubuntu-24.04-x64`,
`native-desktop-linux-ubuntu-24.04-x64`, `native-cli-windows`, and
`native-desktop-windows`. Every row has exactly `label`, `status`,
`evidence_kind`, `os`, `cpu`, `revision`, `runtime`, `commands`, and `logs`;
status is `passed`, `failed`, or `unobserved`, unavailable runtime is null with
an explicit remaining-gap explanation, and commands/logs are arrays. Actual
commands also appear in `commands_run`.

The Integration-owned producer/validator uses `json.loads`, requires those exact
labels, order, fields and states, resolves every nonempty durable log reference
against the tested revision, validates required versus accepted-unobserved
rules, requires the separate client proof, and derives aggregate status. It
refuses malformed/duplicate/missing/contradictory rows, nonexistent or
mismatched evidence, missing required observations, or a blocker. Every failure
and accepted unobserved limitation appears in `remaining_gaps`; actual failures
and missing required evidence also appear in `blocking_findings`. Independent
review checks the complete report against the same logs. C10 consumes the
task-specific review-bound aggregate; it does not parse this encoding. This is
one deterministic representation inside the existing string field, with no
schema property, matrix registry, second report, or second authority.

The user's approved dogfood exception authorizes Main to create one separate
fresh Task tracker client under `/tmp`, one private origin through the existing
authenticated Git/GitHub path, and its CI solely as acceptance proof for this
story. It adds no hosted application, deployment, or reusable client-CI
infrastructure to Forge, so the rest of the BRIEF's infrastructure exclusion
stands. The client follows the normal confirmed-spec/story/task lifecycle. Main starts
that separate client only after the `QUALITY-BASELINE` task marker is on trunk.
Integration refuses until the exact client task marker, reviewed PR, green CI,
and functional proof exist and match the cited client repository/commit; this
adds no ninth harness task or cross-repository surrogate ID. Its CI is
meaningful only when a clean checkout installs the client, runs its
declared lint/type/build checks, and executes automated create/list/complete-
task persistence tests with no wholly skipped selection. It is a dogfood
consumer, not harness-task contribution. Its UI task is user_facing true and
must show real functional proof. Its admitted worker contributes real code,
tests, verification, review, functional evidence, PR, and green CI.
Forge parity integration is user_facing false under the current per-task
definition but still needs the required platform results and lifecycle proof. Record exact
client repository, commits, PR, and logs in the existing report; missing
client proof blocks the claim.

Accepted 0055/0056 quality rollout has bounded mechanical predecessors,
separately reviewed semantic repairs, then the user-approved exact pins
`ruff==0.16.6` and `pyright==1.1.411`. Harness coverage is exactly every tracked
`*.py` below `factory/scripts/` and `factory/tests/`, including tracked fixtures
in those roots; generated/client-owned Python outside those roots is excluded
and uses its owning client's declared stack checks. Ruff check, Ruff format
check, and Pyright use that same explicit set locally and in CI. Missing
configuration, a missing covered path, and deliberate lint/format/type
violations fail. Staging delays activation but never weakens final coverage.
Full quality and parity ship only after activated quality, AC1-AC12, C1-C10,
and the required local Mac and Linux/Windows CI results pass, with unobserved live-platform limitations stated.

### Durable decisions, events, and client migration

Active decision output is generated from the existing parser and remains a
view, never a second authority. Keep numeric IDs, paths, references,
supersession links, and decision files. Each bundle member has exactly
`{"id":"<source filename stem>","payload":<validated original event object>}`.
The payload remains the existing event-schema object and gains no synthetic ID.
Its comparison identity is `(id, canonical_payload)`, where canonical payload
is `json.dumps(payload, sort_keys=True, separators=(",", ":"),
ensure_ascii=False).encode("utf-8")`. The same ID and canonical payload
deduplicate; the same ID with different canonical payload is a collision and
refuses; different IDs remain distinct even when their payloads are equal.

The only compaction source eligible for mutation is a validated live
`.factory/events/<id>.json` whose payload story exactly matches the target key
and whose story has durable shipped proof. Require the exact target roadmap row
done and its history pointer to match the chosen scoped or legacy location. A
scoped story requires matching validated `shipped.json` plus the existing
complete task-marker/proof predicate. A legacy story requires matching archived
`run.json` in its original `pr-ready` state and complete archived proof; require
task markers only when that historical run used task-level delivery
(`base_main_sha`). Do not impose retroactive task markers on legitimately
shipped story-level history. Missing, partial, ambiguous, or conflicting
identity refuses mutation. `.factory/events.jsonl` and every pre-existing file
below `.factory/history/` are immutable legacy inputs: retain their bytes,
never select them as loose migration sources, and never delete or rewrite them.
Legacy-only idless streams remain a no-op. There is no sidecar, database,
heuristic deduplication, Git history rewrite, or legacy JSONL rewrite.

Preview prints the exact eligible filename/ID/canonical-payload inventory and
its SHA-256. Apply requires that value through `--expected-digest`, recomputes
the same inventory including shipped-proof identities and any existing bundle
bytes, and refuses mismatch before publication or deletion. Use
`.factory/stories/<KEY>/events.bundle.json` for scoped stories and
`.factory/history/<KEY>/events.bundle.json` for eligible live sources attributed
to legacy shipped stories, with top-level keys exactly `format`, `story`, and
`events`, where `format` must equal `forge-event-bundle/v1`; events are the exact
member shape above sorted lexically by ID. An
existing validated bundle is immutable. A retry may delete only eligible loose
sources whose exact pairs are already present. It cannot union, replace, or
truncate the bundle; unseen late IDs remain untouched and produce a concrete
refusal. A first compaction writes a complete sibling temporary file and uses a
portable atomic no-overwrite publication primitive, refusing unsupported
publication. Before deleting each source, re-read its regular-file identity and
bytes and compare its exact pair with the durable bundle. Changed, replaced,
symlinked, or new sources stay untouched. Partial failure preserves durable
evidence and every source not already safely represented; rerunning the same
validated inventory is safe. The existing reader adds only validated bundles
while preserving legacy JSONL and loose-file behavior.

Use existing forge upgrade for one isolated migration per Git common
directory. A dirty client gets an isolated upgrade worktree when its common
directory can be safely resolved; preserve the original dirty checkout and
hotfixes. Defer only that client's unsafe, shared, ambiguous, or unresolvable
migration and continue independent authorized client migrations. Upgrade only
owned machinery/doc contracts; client decisions, settings, CI, and evidence
remain intact. The existing three-path ephemeral run-log allowlist is
unchanged. Event cleanup cannot waive proof, markers, readiness, or shipping.

## Ten retained client failures and owner obligations

The following audit findings are implementation obligations, not completion
claims. Each owner adds focused positive, negative, tamper, and recovery
regressions where relevant.

1. Review preflight reads story proof while producers write task proof.
   NATIVE-FOREGROUND-ACTIVATE owns the first-task fix: review resolves
   verify/tests through proof_path with exact task ID and refuses story,
   sibling, absent, or stale proof. Add review.py as path 24 to the existing
   23-path first scope.
2. The actual question ledger can be omitted during task hydration.
   SHARED-COORDINATOR-JOURNEY carries exact existing story/task question
   records and identities into target ceremony context, without reviving a
   plan-mode gate or inventing a ledger.
3. Generated snapshots and migration input can consume complete-review
   capacity. LEAN-WORKFLOW keeps generated SQL/snapshots/journals in semantic
   and security review with an explicit measured risk contract, never blanket
   exclusion or truncation.
4. Git-local stage wording can make protected state appear invisible to an
   admitted sandbox. The current production probe can read the Git control
   directory and run forge next, so no read denial is claimed. LEAN-WORKFLOW
   owns the phase/status wording repair; NATIVE-FOREGROUND-ACTIVATE only
   probes actual native read and protected-write denial in its existing tests.
   No writable snapshot/token, environment claim, or recorder bypass is a fix.
5. Broad .github ownership hides client CI. LEAN-WORKFLOW treats only the
   four exact factory-owned workflows as harness machinery and all other
   .github paths as product input in measurement, review, readiness staleness,
   scaffold/upgrade, and vendor integrity.
6. Settled lint/engineering rulings disappear in fresh workers.
   LEAN-WORKFLOW propagates each current task ruling through the existing
   brief/contract and recorders, bound to story, task, contract, and signal.
   Material scope/acceptance changes still amend, re-grill, and re-approve.
7. Resume can choose the wrong proof chain when base_main_sha is absent.
   SHARED-COORDINATOR-JOURNEY preserves task, owner, branch, worktree, base
   commit, and task-level closeout mode; ambiguous recovery refuses.
8. An older task can fall back to another task or story proof.
   NATIVE-FOREGROUND-ACTIVATE owns task-bound readers and C10: an unqualified
   T2 or story singleton cannot satisfy T1. Valid historical proof remains
   readable only when its owner, task identity, and historical binding are
   established; a legitimate shipped marker cannot pollute a current T3
   singleton.
9. Resume/migration can rewrite sealed records. SHARED-COORDINATOR-JOURNEY
   preserves sealed task/stage/approval/proof bytes and refuses destructive or
   uncertain migration; reconciliation uses existing owner/trunk rules.
10. Sibling/trunk integration can overwrite sealed records.
    SHARED-COORDINATOR-JOURNEY reconciles common-directory ownership and
    immutable trunk markers without replacing an owner's sealed contract/proof,
    retaining task identity through refresh and retry.

The eight owners are NATIVE-FOREGROUND-ACTIVATE, LEAN-WORKFLOW,
NATIVE-LIFECYCLE, SHARED-COORDINATOR-JOURNEY, PORTABLE-DELIVERY-MIGRATION,
FORMAT-SOURCES, QUALITY-BASELINE, and FORGE-COORD-1.1. They replace the
unapproved 39-row graph while preserving its preparation. Background lifecycle
belongs to NATIVE-LIFECYCLE; interaction/recovery to
SHARED-COORDINATOR-JOURNEY; decisions/events/clients to
PORTABLE-DELIVERY-MIGRATION; source repairs to FORMAT-SOURCES; staged checks
to QUALITY-BASELINE; integrated parity to FORGE-COORD-1.1. LEAN-WORKFLOW is
user_facing false (backend gates, proof, CLI/docs). SHARED-COORDINATOR-JOURNEY
is user_facing true for the actual board/coordinator UI journey. The separate
Task tracker UI leaf is true; Forge integration is false despite live proof.
These are ownership candidates, not approved wildcard scopes.

## Acceptance criteria

1. Required Codex Default decisions and approvals use ordinary main chat and
   existing revision-bound commands without a tool-round prerequisite. Real
   permitted CLI/Desktop structured questions pass the same provenance checks
   as Claude across pre-story, current-story, other-story, malformed-story,
   and historical eventless cases. Missing/canceled/mismatched/replayed,
   empty/whitespace-only/multiple answers refuse. Offered-option and free-text
   answers preserve exact text. All six grills use canonical frontier_empty:
   true when appropriate, retain stated final-round compatibility, reject
   explicit false/unsupported empty rounds, and add no question expiry.
2. Both coordinators are denied direct locked writes while legitimate
   delegated workers perform approved work. Registration timing, failed
   admission, cancellation, revocation, expiry, resume, cleanup, and terminal
   truth are tested.
3. Codex-only launch, status, recovery, and setup require no Claude executable,
   process, plugin metadata, or environment state. Static vendored Claude files
   and the working companion/rescue route remain supported.
4. Both coordinators select the Decision 0066 execution lanes: exploration
   Sol/low; planning, decomposition, architecture, plan validation, and grills
   Sol/high; implementation and autoreview fixes Sol/medium; formal Lite
   Luna/max; formal autoreview and functional checking Sol/high; no new Terra
   actor. The same Claude plugin route supports Luna/max Lite, and doctor
   refuses unknown or locally modified plugin sources before repair. Every
   approval, admission, verification, review, functional, PR,
   marker, and shipping gate remains coordinator-independent.
5. Startup, resume, clear, compaction, question, and Stop interception use
   installed runtime registrations. Removing a required registration from one
   adapter or both fails parity validation.
6. At the review-only draft checkpoint, delegation, deterministic verification,
   and honest source proof run without fabricated evidence; incomplete platform
   proof remains explicit and no formal Forge review is recorded. After the
   required platform evidence updates the automated report, a fresh complete
   brief and formal independent review are mandatory. Final readiness,
   marker, shipping, and closeout require the local Mac and Linux/Windows CI results and task/worktree/
   shipping checks. Support-task proof remains separate; platform coverage rows
   cover native Codex only, and CI-backed rows state only their observed coverage.
7. After separately approved 0058 support tasks, final integration uses the
   approved stage route, real schema recorders, actual runtime evidence, and
   an unmerged review-only draft with no task marker. Missing required proof blocks
   readiness; accepted unavailable-platform limitations remain explicit, and complete required proof permits the same task's normal closure.
8. Setup honors explicit/environment/detected/interactive selection and
   cancel/EOF refusal before install, passes selection to both doctors, and
   preserves project configuration, historical evidence, and both adapters in
   fresh, adopted, and upgraded clients.
9. Both coordinators continue authorized work and resume after required
   answers without repeated continuation prompts. Optional work continues when
   facts suffice. LEAN-WORKFLOW adds optional explicit `--context-file` to the
   existing grill CLI and brief composer; no such launcher input exists yet.
   The authorized caller may select an inside or outside path. Resolve it once
   to a regular file, read one complete UTF-8 snapshot, and label its content as
   untrusted supplemental context. Missing, unreadable, non-regular, or
   undecodable input refuses. The snapshot cannot alter primary artifact path or
   digest, gate/task identity, decisions, scope, evidence, or read-only
   authority; do not search other files, re-open the path, impose a repo-only
   root, truncate it, or add an arbitrary byte cap. Existing material-shape reread preserves nonblank
   reason and refuses blank reason, missing-reason second read, or beyond-cap
   reread. No new evidence family is added.
10. Coordinator switching occurs only at completed-task boundary after
    active-worker checks and actual no-pending-question observation in the
    existing test report. Active work, incomplete proof, unanswered/canceled
    approval, and conflicting workers refuse; no cross-session registry exists.
11. Shared presentation is required before first approval and every material
    spec/plan revision; unchanged technical corrections within standing
    authorization carry the existing binding without repeated ceremony. Main
    owns story planning, grill, approval, frozen decomposition, scheduling,
    and human questions; each task owns JIT through PR/green CI in its
    worktree. The first native task performs the full 0063 source-contract
    then target-contract sequence and refuses placeholders/source-bound proof;
    its current gates remain until LEAN-WORKFLOW ships. Exercise owner
    reads/retries, disjoint dependency-ready work, task-only enrichment, safe
    trunk reconciliation, real handles, stable/custom titles, scratchpad
    recovery, quiet results, host restrictions, and the unchanged Claude
    route. No new management framework is introduced.
12. Separately approved quality predecessors retain verification/review. Final
    activation covers authored source/tests with pinned Ruff lint/format and
    Pyright, identical local/CI checks, missing-configuration and deliberate
    violation refusals, and client stack checks. No suppression, truncation,
    review-limit bypass, or artificial clean result is allowed; the activated
    baseline passes on integrated parity before shipping.

## Parity contract labels C1-C10

C1. Setup uses explicit flag, environment, unambiguous detection, then TTY-only
interactive choice. Ambiguous/no-choice unattended runs, cancellation, EOF,
and unknown runtime refuse before installation; both doctor calls receive the
same choice and Codex has no Claude dependency.

C2. New Claude/Codex structured events preserve actual story, session, event,
tool-call, question, and answer identity. Story gates reject other-story or
unbound claims; project gates accept valid pre-story/current-story claims.
Replay, cancellation, malformed, and mismatch fail while completed historical
grills remain valid. Required Codex approvals use ordinary chat; optional
structured rounds and technical passes never imply approval.

C3. Each adapter requires startup, question, compaction, write-policy,
completion, and Stop handlers, including startup/resume/clear/compact
SessionStart. Removing/replacing any required source in one or both adapters
fails validation.

C4. Foreground/background startup failure before process creation publishes
failure without PID or exit code. Registered workers retain process-bound
admission, verified cleanup, revocation, observable status, refusal of expired
authority, and refusal of incomplete output.

C5. Init/adopt/upgrade deliver native assets and the complete 15-definition
team registry through existing ownership and target-boundary checks, preserve
client settings/historical proof, retain Claude, refresh same-name harness
definitions under the existing replacement contract, and preserve distinct
client-added agents without a new merge/provenance mechanism.

C6. Optional untrusted context reaches required cold readers through the
existing launcher without changing artifact identity, finding resolution,
frontier checks, model policy, or read-only authority. The current brief and
recorders carry settled facts; no compulsory round, forced closing question,
clean-next-round instruction, or new evidence family is added. Reread reason
and refusals are preserved. forge next routes active missing/draft specs before
requirements and authorized work continues after answers/gates.

C7. Lifecycle coverage proves approved delegation, task-scoped tests/reviews,
conditional functional proof, completed-task handoff, active-worker refusal,
and actual no-pending-question observation. Unanswered/canceled/replayed
questions do not satisfy approval; no cross-session registry exists.

C8. A real native worker contributes after stage start and before stage done,
passes verification and independent review, and records all required
local Mac and Linux/Windows CI results before final parity readiness/shipping, with unavailable live-platform observations reported honestly.

C9. Task, branch, and autoreview briefs include complete approval-bound task
plan and automated-test report. Prose deliverables remain valid when the
approved plan/contract and actual reports let review assess them. Missing,
unapproved, stale plan text, or incomplete validation refuses. Cleanup retains
required Claude and historical consumers. Review reads proof by exact task
identity.

C10. Managed save metadata preserves an unchanged story-plan grill while
substantive changes invalidate it. Readiness requires task verify, automated
tests, three explicit review assessments, and conditional functional proof.
Shared predicates reject blockers even with passed status and require
functional proof for user-facing tasks. Task readers reject unqualified
cross-task/story fallback while retaining historically bound proof. They retain
history compatibility and never use a legitimate shipped marker as a current
task singleton. Legacy fallback is a whole historical bundle, never per-file
mixing: only an existing legitimate committed task marker naming the task,
branch, base and seal commit may select it, and readers use that marker's
`commit`, never the current story singleton. Require the matching task plan,
grill and approval chain there; every artifact task ID matches, recorder commits
lie between task base and seal, review bindings are coherent, and classified
product content stays unchanged from each proof commit through seal. Missing
identity, ancestry, approval, binding or artifact refuses, and any partial
modern task bundle disables fallback. Pre-marker local sealing never uses
historical fallback. Already sealed committed markers remain eligible for
pre-merge CI, and already merged or reconciled markers keep their existing
treatment. Compatibility is never inferred from dates, Forge-version SHAs, or
historical source substrings.

## Proof and handoff boundary

No roadmap-field edit is required for these closure obligations. Roadmap
criterion 1 already owns worker policy and every Forge gate, so the exact
design-review predicate and Decision 0066's 15-agent registry are part of that
criterion. Roadmap criterion 3 owns the approved delivery chain; accepted
Decision 0064 explicitly amends that chain with exact event compaction and the
four-client migration. The approved story plan must carry the existing
AC/roadmap/task-owner crosswalk, and any obligation absent from that crosswalk
is scope creep and cannot block closure.

The platform evidence contract, separate /tmp Task tracker client, first native
source/target transition, original preparation bytes, ten client failures,
AC1-AC12, and C1-C10 are closure obligations. C1-C10 alone cannot establish
whole-spec closure. Before recording contracts, map each criterion to an
owning task and actual evidence. Support tasks may own complete prepared native
changes, workflow/workspace/delivery changes, or quality predecessors under
0058/0055/0056; final parity owns integrated behavior and confirms activated
quality and required local Mac/Linux/Windows CI proof, with live-platform limitations stated. No omitted or partially reviewed bytes may ship.

The approved roadmap amendment at e218db6 and reviewed proposal digest
c37199034d36f19942d133c691a5bc234df1f756a9c1347ae176640090af27ab remain
history. Preserve story/epic identity, order, unrelated fields, and no task
IDs in story depends_on. Exact scopes/tests are bound by saved story/task
plans; the replaced 39-row graph is not an approved wildcard. Temporary
review, /tmp, and preparation paths are inputs until needed facts are
preserved in repository-owned records. This draft does not authorize
implementation, merge, or release outside the approved task route. Platform evidence follows accepted 0065; CI is never represented as unobserved live Desktop behavior.
