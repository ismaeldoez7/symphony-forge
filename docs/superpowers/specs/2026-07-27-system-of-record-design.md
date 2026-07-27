# Repo as System of Record — capture completion + board reading layer

## Context

The complaint moved past styling: the board's content doesn't help a human
decide anything, and the repo cannot answer "what was the issue, what was
built a month ago, which decisions were taken for this feature, what
contradictions arose." Three audits (capture schemas, board rendering,
decisions/history) plus two independent lifecycle validations (Opus subagent
and a Codex gpt-5.6-sol@high rescue, each role-playing a PM and an engineer
from discovery through production/support) produced the diagnosis and
hardened the design below. Verified against the code, not taken on faith:
`cmd_add` exists gated on confirmed `--spec`; `pr_ready.py` has no argparse;
the union-merge driver skips `.factory/`; header counts already render;
`story_detail` mis-binds live evidence.

**The record is incomplete** — no outcome is written after work (every field
is authored *before* implementation); no structural decision↔story link
(frontmatter is `status`/`confirmed_by`/`date` only; the plan's
`## Decisions` section is parsed by nothing).

**Actively destroyed** — `pr_ready.py:277-281` deletes
`.factory/grills/plan.json` at ship and the archive copy list omits it; the
story timeline is one mutable `updated_at` overwritten ~5×.

**Discarded by the renderer** — `acceptance_criteria`, the `story`
narrative, epic `objective`, `assignee`/`skill` all arrive and never render;
task rows stripped to id+title at `board.py:67-71`; decision titles render
empty (real bug).

**Hollow or wrong where it matters (validation findings)** — 13 of 15 real
decisions are `proposed`/unconfirmed and the accepted-only filter hides
them; `decision new --supersedes` leaves *neither* version active until
acceptance; reviews are overwritten until clean so "what reviewers flagged"
never survives; `story_detail` attaches the active task's live evidence to
any unplanned story you click; board gate flags are file-existence, not the
`pr_ready` predicates; the planning-lock hook frees product writes on plan
approval alone, before decomposition exists; re-recording a decomposition
wipes completed stage timestamps; "shipped" in this harness means PR-ready,
not deployed.

Grilled decisions (user-locked), amended by validation:

| Decision | Choice |
|---|---|
| Record shape | Complete the existing ledgers in place — no new store |
| Outcome | Required at ship — a recorded artifact `pr_ready` checks (not a CLI flag; bare runs stay a readiness check) |
| Decision↔story | `stories: [...]` flow-list in decision frontmatter, seeded by `decision new`, appended by `decision link` |
| Timeline | Append-only `.factory/events.jsonl` with actor, union-merge registered, discovery instrumented, archived per story |
| Task contract | Recorder enforces non-empty `objective` + `acceptance_criteria` per task |
| Ad-hoc intake | Extend existing `roadmap add`; `--no-spec --reason` captures debt visibly, but `plan save` still requires a confirmed spec — capture ≠ build authorization (keeps decision 0014 intact) |
| Sequencing UI | In place: enrich existing header counts + cards; no second strip, no DAG canvas, no tree, no Gantt |

Reviewer suggestions **rejected**, with reasons: criterion-by-criterion
outcome evidence (ceremony — AC are attested by tests/functional artifacts;
outcome is the human paragraph); deployment tracking (out of harness scope —
Ship log labels dates "PR-ready" honestly instead); inverting the decision
backlink onto stories (user-grilled choice stands; flow-style single-line
list keeps the parser trivial and merges clean); a separate Start-now strip
and counts strip (both duplicate what `progress-line` + ★ marks + leverage
sort already render).

---

## Part 1 — Capture (harness scripts)

### 1a. Events ledger — `forge_cli/events.py` (new)

`append_event(base, event, actor, story=None, detail=None)` → appends
`{"at", "event", "actor", "story"?, "detail"?}` to `.factory/events.jsonl`.
Schema `factory/schemas/event.json`, validated in the helper (follow
`signal.py`). `actor` required — script role or `--by` human name; `story`
optional (discovery events are project-level). No event ids (nothing
references an event).

Call sites (one line each):
- post-signoff: `intake.py`, `update_run.py` (phase changes), `plans.py`
  plan save, `record_signoff.py`, `record_decomposition_from_json.py`,
  `verify.py` (pass/fail), `record_test_from_json.py`,
  `record_review_from_json.py`, `pr_ready.py` (`pr-ready`)
- execution: `stages.py` stage start / stage done, `signal.py` raise /
  resolve (stage and signal transitions currently record no actor at all)
- discovery: `specs.py` spec save + confirm, `roadmap.py`
  derive/import/add, context harvest

Merge safety: `.factory/*.jsonl merge=jsonl-append` added to
`.gitattributes` (driver exists; covers only `.gstack/`+`plans/` today) —
with a real three-way merge test. At ship, story-scoped lines move to
`history/<issue>/events.jsonl`, project lines stay; `run.json` stub stays
byte-identical (test_gates.py:262 untouched).

### 1b. Outcome — `forge outcome set` + `pr_ready` gate

`forge_cli/outcome.py`: `./forge outcome set "<paragraph>"` (or `--from
<file>`) → `.factory/outcome.json`, schema-validated, `generated_by` pinned,
`commit`-stamped. The voice contract is CODED, not advisory: refuse < 12
words or > 800 chars (a command line or a dumped diff can't pass; an essay
can't either). Help text carries the voice guidance on top.

`pr_ready.py` (still zero arguments): outcome joins `missing[]` — a bare
run answers "not ready: outcome not recorded"; the idempotent shipped-state
early exit is unchanged. At ship: outcome text → roadmap item `outcome` +
archived `run.json`; live file removed like signals. `outcome` joins
`LIFECYCLE_FIELDS` (`roadmap.py:27`) so import/derive can never overwrite a
shipped outcome. Legacy archives without outcome: defined absent, board
shows fallback text.

### 1c. Decisions — multi-story backlink, honest corpus, atomic supersede

- `decision new` writes `stories: [<issue_key>]` (flow style, one line —
  the scalar parser extends trivially) from the active run; `forge decision
  link <slug> --story <key>` appends (real case: one decision governs three
  stories).
- `decision_records()` gains `title` (parse `# Heading` as `cmd_list`
  already does), `stories`, `superseded_by`.
- **Atomic supersede (pre-existing flaw)**: `decision new --supersedes`
  stamps only the successor's `supersedes:`; the predecessor stays
  `accepted` until `decision accept` of the successor flips both in one
  step. No more window where neither version is active.
- Board ships all records: accepted plain (the only *binding* corpus —
  attestation math unchanged), proposed labelled "proposed — unconfirmed",
  superseded struck-through with pointer. `pr_ready` warns (not blocks) on
  linked unaccepted decisions — the repair path for the 13-of-15 corpus.
- No ship-time decision snapshot (no consumer); Ship log derives "decisions
  created" from `stories`.
- `check_dual_runtime.py` (the standing structural gate) learns the new
  shape: every decision record must carry `stories` as a list (hand-created
  files can't silently omit it), and an accepted record with `supersedes:`
  whose predecessor is not `superseded` is a violation — the atomic-flip
  invariant is checked, not trusted.

### 1d. Archive the plan grill — `pr_ready.py`

Copy `grills/plan.json` specifically (not the directory — it holds
project-level `epics.json`/`signoff.json`) before the unlink.
`board.py:329-332` already reads the destination.

### 1e. Task contract + stage reconcile

`record_decomposition_from_json.py:35-41`: each task requires non-empty
`objective` (str, **≤ 500 chars — coded cap**, the real anti-example was a
900-char implementation dump) and `acceptance_criteria` (non-empty list of
non-empty str). Decomposer prompt: "should" → "must" plus the voice line —
but the recorder refusal is the enforcement; the prompt is only the
explanation.

**Stage reconcile (pre-existing flaw)**: re-recording a decomposition
currently recreates every stage as pending, destroying completed
timestamps. `stages.write_skeleton` → merge by task id: keep status +
timestamps for surviving ids, add new as pending, drop removed (event
records the delta).

**Lock alignment (pre-existing flaw)**: the planning-lock hook
(`pre_tool_use.py:219-229`) frees product writes on `plan_status: approved`
alone; AGENTS.md says implementation requires plan *and* decomposition.
Hook gains the decomposition check.

### 1f. Ad-hoc intake — extend `cmd_add` (`roadmap.py:329-353`)

Add `--story` + `--ac` (repeatable, both required for new adds),
`--depends-on` validated through `check_dag` after append (add currently
skips graph validation entirely), and `--no-spec --reason "<why>"` →
`origin: "adhoc"` + recorded reason, story sits in "Needs spec" as visible
debt. **The 0014 gate holds downstream**: `plan save` gains a check — the
story's roadmap item must carry a confirmed spec (today it checks only key
existence, which would have made the escape a full bypass). New
`roadmap link-spec <key> --spec <path>` attaches the spec later and clears
the debt. `roadmap heal` learns the new fields (deterministic per-field
union) and revalidates the DAG after healing.

### 1g. Ship archive completeness — `pr_ready.py`

Snapshot the story's `plans/assumptions.md` rows (matched on the existing
`issue` column) into `history/<issue>/assumptions.json`. `defer add` gains
optional `--issue` (defaulted from the active run) so future deferrals carry
provenance; rows matching the story are snapshotted too. Residual risks are
NOT duplicated — they already live in archived reviews; the gap is
rendering.

## Part 2 — Display (`factory/board/index.html` + `board.py`)

Server:
- `_plan_evidence()` joins the immutable task contract from
  `decomposition.json` (`objective`, `acceptance_criteria`,
  `reviewer_focus`) to mutable stage status/timestamps by task id. The stage
  skeleton remains execution state, not a duplicate task store.
- **Evidence binding fix (real bug)**: `story_detail` uses live `.factory/`
  only when `run.json`'s `issue_key` matches the requested story; otherwise
  history or nothing — today clicking any unplanned story shows the active
  task's evidence as its own.
- **Gate truth**: extract pure readiness predicates into
  `forge_cli/readiness.py`; both `pr_ready.py` and the board reuse them
  (status/score/blocking findings), never file existence or duplicated
  conditionals.
- `plan_by_story` gets the `story or issue` fallback `story_detail` already
  has — without it every legacy project renders unplanned and task numerals
  stay blank.
- `story_detail()` ships `events` + archived assumptions; decisions payload
  per 1c (all statuses + titles + stories). Activity uses event-ledger
  entries when present; raw signal/stage timestamps are the legacy fallback,
  never a second source rendered beside the same transitions. Decisions
  without `stories` render once as project-level legacy context rather than
  being repeated as story-specific decisions.

Header: extend the existing `progress-line` (counts already render — no new
strip): append a project task rollup (`14/23 tasks`) and, when nonzero, an
`N unassigned` cell. Ready cards enrich the existing ★ mark with
`@assignee [skill]` — `assignee` and `skill` currently render nowhere.

Cards: building cards gain a task-progress numeral (`2/5`) from
`lifecycle.stages`. Motion budget untouched.

Drawer (narrow) — reordered to lead with meaning:
1. Key + title, **story narrative**, **AC** as a glyph checklist
2. **Decisions** — records whose `stories` include this key: accepted
   plain, proposed labelled, superseded struck with pointer; plus "attests
   N active"
3. **Activity** — render-time merge of events + signals + stage stamps,
   one ruled timeline with actor (serif labels, small mono timestamps)
4. Tasks — glyph + id + title; `objective` + per-task AC behind `<details>`
5. Readiness (humanized labels; `fix` commands mono, labelled "run:")
6. Shipped stories lead with the **outcome**, then residual risks (read
   from archived reviews) and archived assumptions — the forensics block

Wide drawer: prose `<dt>` labels ("Verification", "Quality review", "Plan
grill" — not `grill:plan`); findings as sentences; raw-JSON toggles stay.

Library: **Ship log** — reverse-chron by month: date (labelled
**PR-ready**, not "shipped" — deployment is outside the harness), key,
title, outcome, decisions created. Decisions tab: every record, real title,
status, origin stories. Epic objectives in lane tooltip + Library.

Graceful degradation: agentstats/myclaw predate every new field — outcome
fallback text, timeline degrades to stage stamps, `stories`-less decisions
read project-level. No backfill.

## Part 3 — Docs, skills, self-governance

- `factory/skills/forge.md` — intents: "add a story", "what shipped" →
  Ship log, "record the outcome" → `forge outcome set`; pr-ready notes the
  outcome gate + unaccepted-decisions warning.
- `docs/decisions/README.md` — rewrite to match the real CLI scheme.
- `AGENTS.md` — one line: phase 8 → "mark PR ready (outcome recorded
  first)".
- `docs/decisions/0017-repo-as-system-of-record.md` (status `proposed`,
  human acceptance): outcome-at-ship, events+actors, multi-story backlink,
  proposed/superseded rendering, adhoc capture with confirmed-spec-at-plan
  gate, atomic supersede, lock alignment.

## Enforcement matrix — every rule is a coded gate, never an instruction

Standing rule for this whole plan: prompts and skill docs may *explain* a
rule, but every rule is *enforced* by a script refusal, a hook denial, or a
`check_dual_runtime` violation. Foundation already in place and verified:
`pre_tool_use.py:37-53,158-170,300` denies hand-writes into `.factory/`
(edit tools AND bash redirects), so evidence can only enter through the
validating scripts.

| Rule | Coded enforcement |
|---|---|
| Outcome exists before PR-ready | `pr_ready` `missing[]` refusal |
| Outcome is prose, not a dump | `outcome set` refuses < 12 words / > 800 chars |
| Task has objective + AC | recorder refusal |
| Objective is brief | recorder cap ≤ 500 chars |
| Story has confirmed spec before build | `plan save` refusal (closes the 0014 bypass) |
| Ad-hoc debt is explicit | `cmd_add` refuses `--no-spec` without `--reason` |
| Roadmap graph stays valid | `check_dag` on add + post-heal revalidation |
| No product writes before decomposition | `pre_tool_use.py` hook denial |
| Timeline is written | scripts append events themselves — agents can't skip a ledger they don't write |
| Event has an actor | `event.json` schema (required field) |
| Ledger merges cleanly | `.gitattributes` union driver + automated three-way merge test |
| Decision shape (stories list, titles, statuses) | `check_dual_runtime` violations |
| Supersede is atomic | `decision accept` performs the flip; `check_dual_runtime` flags any record pair violating it |
| Decision acceptance is human | existing: non-empty `confirmed_by` + commit-trailer check |
| Evidence never hand-written | existing hook denial (verified above) |
| Board stays read-only | GET-only server + test asserting no mutation route |

The only deliberate non-blocking control: `pr_ready`'s *warning* on linked
unaccepted decisions — blocking would freeze the 13-of-15-proposed legacy
corpus; the warning plus the board's "proposed — unconfirmed" label is the
repair pressure.

## Files touched

- new: `forge_cli/{events,outcome}.py`, `factory/schemas/{event,outcome}.json`,
  `docs/decisions/0017-repo-as-system-of-record.md`
- capture: `pr_ready.py`, `intake.py`, `update_run.py`,
  `record_{decomposition,test,review}_from_json.py`, `verify.py`,
  `record_signoff.py`, `pre_tool_use.py`,
  `forge_cli/{decisions,roadmap,plans,specs,context,stages,signal,deferrals,readiness}.py`,
  `forge.py` (wire `outcome set`, `decision link`, `roadmap link-spec`,
  extended `add`), `.gitattributes`
- display: `factory/board/index.html`, `forge_cli/board.py`
- docs: `factory/prompts/decomposer.md`, `factory/skills/forge.md`,
  `docs/decisions/README.md`, `AGENTS.md`
- structural gate: `factory/scripts/check_dual_runtime.py` (decision
  `stories` list + atomic-supersede consistency)
- tests (`test_gates.py`): outcome gate (missing → listed; recorded →
  roadmap+archive; rerun idempotent; too-short/too-long refused);
  objective-cap refusal; task-contract refusal; stage
  reconcile preserves completed; lock requires decomposition; `stories`
  seeded/linked; atomic supersede; events (actor required, archived,
  three-way union merge); grill file archived; extended `roadmap add`
  (missing story/AC, `--no-spec` sans `--reason`, dup key, bad dep, cycle,
  DAG-validated); plan save refuses unspecced story; `link-spec` clears;
  heal revalidates; evidence-binding (unplanned story ≠ active run's
  proof); shared gate-truth predicates including failed/low-score/blocking
  evidence; decomposition-task/stage join; event timeline de-duplication;
  all decision statuses/titles; archived forensics; legacy `issue` fallback;
  board anchors (task rollup, unassigned, ship log). Existing fixtures gain
  outcome + objective/AC (`test_gates.py:35-38`, `:2143-2146`).

## Build

Per the user's standing instruction: opus subagents (two tracks — capture,
display), then ONE autoreview pass (quality, performance, security) run
directly, loop until clean. `factory/` is on the planning-lock allowlist.
Commit the design spec to
`docs/superpowers/specs/2026-07-27-system-of-record-design.md` first.

## Verification

1. `pytest factory/tests/` green; `check_dual_runtime.py` clean.
2. Scratch-clone rehearsal: intake → plan save (unspecced story refused →
   `link-spec` → passes) → decompose (missing objective refused; re-record
   preserves done stages) → product write blocked until decomposition →
   stage done → bare `pr_ready` reports "outcome not recorded" →
   `outcome set` → ship: roadmap gains `outcome`, history gains
   `grills/plan.json` + `events.jsonl` + `assumptions.json`, run stub
   byte-stable, live outcome/events cleaned.
3. `roadmap add --no-spec --reason` lands in "Needs spec" with origin
   adhoc; plan save for it refuses until spec confirmed+linked.
4. `decision new` seeds `stories`; `link` appends; supersede leaves
   predecessor accepted until successor accepted; agentstats' 13 proposed
   records visible and labelled.
5. Board vs agentstats: task numerals via `issue` fallback; clicking an
   unplanned story no longer shows the active run's evidence; outcome
   fallback; timeline degrades to stage stamps.
6. Parallel-merge: two branches appending `.factory/events.jsonl` merge
   cleanly under the union driver (automated test + manual check).
7. Screenshots light/dark/760px: enriched progress-line, @assignee on
   ready marks, drawer order, task disclosures, proposed/superseded decision
   styling, Ship log ("PR-ready" labels), keyboard focus/close, and polling
   without duplicate cards/timeline rows. No horizontal scroll; hidden
   scrollbars preserved.
8. Read-only invariant: GET-only server; POST unavailable; a before/after
   filesystem digest is unchanged; `grep -nE "https?://"` clean.
