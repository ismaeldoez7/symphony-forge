---
issue: FORGE-TERSE-2
title: Narration budget in the constitution + prompt pointers
status: approved
saved: 2026-08-10T15:28:19+00:00
story: FORGE-TERSE-2
decisions_reviewed:
  - 0001-determinism-contract
  - 0002-concurrency-one-task-per-branch
  - 0003-model-tiers-terra-explore-sol-implement
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
---

# Plan — FORGE-TERSE-2: Narration budget in the constitution + prompt pointers

> Story FORGE-TERSE-2, epic `terse-output` (final story), spec
> `docs/specs/terse-output.md`. Branch
> `feat/FORGE-TERSE-2-narration-budget-in-the-constitution-prompt-pointers`.
> Operator escalation folded in: the rule must ALSO be a strict AGENTS.md
> non-negotiable, not constitution-only.

## Problem

FORGE-TERSE-1 silenced the CLI; agents still narrate freely. Conduct §7
already mandates "Report progress as you go; never pause for it" but never
bounds the report's size — so mid-execution commentary is unbounded by
contract. Nothing in AGENTS.md, the constitution, or the delegated-worker
brief limits narration volume.

## Scope / Non-goals

**In scope:** conduct §8 (the full rule), one strict AGENTS.md
non-negotiable (with a one-line reclaim — the file sits exactly at its
110-line CI cap), self-sufficient clauses in `implementer.md` /
`planner.md` / `harvester.md`.

**Non-goals:** NO doc-shape test — no test in the repo pins doc content
today, and §1–§7 are enforced by human review; §8 joins them rather than
setting a doc-pinning precedent (stated judgment call). NO edits to
`reviewer.md`/`griller.md`/`decomposer.md` (each already states the
equivalent rule in its own vocabulary — a §8 cite would be duplication).
NO `delegate.py` change (the brief already inlines `implementer.md`
verbatim, which is exactly why that file's clause must be self-sufficient).
NO `.claude/CLAUDE.md` edit (one line of cap headroom, wrong altitude).
NO cap bump in `check_agents_hygiene.py` — the 110-line discipline stands;
the bullet pays for itself by tightening an existing wrapped bullet.

## Acceptance Criteria

1. `constitution/09-agent-conduct.md` gains `## 8. Narration budget` after
   §7 (before the closing `---`), in the exact house shape (§6 is the
   template): one dense prose paragraph, ~72-col wrap, imperative voice,
   closing epigram. Content: during execution, at most one line per state
   change — what was done, what changed; findings, contradictions, and gate
   results are ALWAYS reported in full; process narration ("now I will run
   the tests") never; full prose belongs only at gates and deliverables
   (plan presentations, review summaries, PR bodies, direct answers).
   Completes §7's "report progress as you go" with the bound it lacked.
2. AGENTS.md Non-Negotiables gains one strict single-line bullet citing
   conduct §8, and the file stays ≤110 lines (`check_agents_hygiene.py`
   green) by tightening one existing two-line bullet without losing
   content.
3. `factory/prompts/implementer.md` extends its existing conduct sentence
   with the §8 clause stated self-sufficiently (rule + cite, not a bare
   path — the delegation brief forbids workers from fetching rules
   elsewhere). `planner.md`'s "Conduct is constitutional" bullet gains the
   clause plus the named exception (gate output is full prose by design).
   `harvester.md`'s Rules block gains one line (the loudest un-governed
   narrator).
4. Honest reach, stated where the user sees it: the constitution + prompts
   reach ALL clients on `forge upgrade` (`UPGRADE_TREES` includes
   `constitution` and `factory`); AGENTS.md is PROJECT-OWNED on upgrade, so
   its bullet reaches new clients at `forge init` only — existing clients
   (myclaw, minegate) get their AGENTS.md bullet during their pilot work,
   by hand, marked as such.

## Technical Approach

- **§8 text** (drafted here, worker lands verbatim modulo wrap):

  > ## 8. Narration budget
  >
  > Report progress as one line per state change: what was done, what
  > changed, nothing about what you are "about to" do. Findings,
  > contradictions, refusals, and gate results are never rationed — report
  > them in full the moment they exist. Everything else between actions is
  > noise that trains the reader to skip output, which is how real warnings
  > die unread. Full prose belongs at the gates and deliverables a human
  > actually reads: plan presentations, review summaries, PR bodies, grill
  > rounds, and direct answers to direct questions. When in doubt, ask
  > whether the sentence changes what the reader does next; if it does not,
  > it does not ship. Narration is a budget, not a diary — spend it where
  > it buys attention, because attention is the scarcest gate in the loop.

- **AGENTS.md bullet** (one line, after the autoreview bullet):
  `- Narration budget (conduct §8): one line per state change; findings always; process chatter never.`
  Reclaim: tighten the two-line evidence bullet (`Evidence enters .factory/
  only via a recording command validating factory/schemas/ (incl. a pinned
  generated_by) — never by hand.`) to one ≤76-col line preserving every
  fact (`Evidence enters .factory/ only via schema-validated recorders
  (pinned generated_by), never by hand.`).
- **implementer.md:9-10**: append `; narration budget — one line per state
  change, findings always, process chatter never (conduct §8)`.
- **planner.md:57-61**: append `; narration budget (conduct §8) — plan
  presentation and grill rounds are the full-prose gate surfaces, the
  exploration between them is one line per state change`.
- **harvester.md Rules**: `- One line per file processed (conduct §8);
  the harvest artifacts carry the detail, not the narration.`
- Canon markers: not added — `check_canon_markers` only validates
  `.claude/`/`.codex/` files; a marker in AGENTS.md/prompts is decorative.
  The `conduct §8` cite convention (already used by prompts and phase.py)
  is the reference form.

## Decisions

No new decisions — the rule's content and homes are in the confirmed spec
plus the operator's explicit AGENTS.md escalation (chat, 2026-08-10).
Stated judgment calls: no doc-shape test (precedent), no cap bump
(discipline), three prompts not five (duplication).

## Surface Impact

| Surface | Class | Notes |
|---|---|---|
| Runtime behavior | Unchanged by design | docs and prompts only; no code |
| API | N-A | — |
| Data/schema | N-A | — |
| CLI/ops | Unchanged by design | no command output changes |
| UI | N-A | — |
| Docs | Changed | constitution §8; AGENTS.md bullet + reclaim; 3 prompts |
| Tests | Unchanged by design | no doc-shape test (stated); hygiene check covers the cap |

## Task Decomposition

One bounded task: **FORGE-TERSE-2.1 — §8 + AGENTS.md + prompt clauses**.

## Risks

- **AGENTS.md cap regression** — the reclaim must keep every fact of the
  tightened bullet; `check_agents_hygiene.py` (CI-only, not in verify.py)
  is run locally as part of verify commands to catch it pre-push.
- **Rule restated inconsistently across surfaces** — each surface carries
  the same three clauses (one line per state change / findings always /
  process never) with §8 as the single full text; the cite convention
  keeps them from drifting into parallel canons.
- **Instruction-level enforcement only** — named honestly in the outcome:
  §8 binds agents the way §1–§7 do (review + culture), not the way the
  budget test binds the CLI.

## Verify Plan

- `python3 factory/scripts/check_agents_hygiene.py` green (≤110 lines);
  `check_dual_runtime.py` green; full suite via `verify.py` (no test
  changes expected — the suite proves nothing broke).
- Read-back review: §8 matches the house shape against §6; every cite says
  `conduct §8`; the delegation brief (compose via `forge delegate
  --print-only` on this task) shows the implementer clause reaching the
  worker verbatim.
