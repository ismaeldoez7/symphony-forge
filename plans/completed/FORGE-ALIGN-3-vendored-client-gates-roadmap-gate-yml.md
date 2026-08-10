---
issue: FORGE-ALIGN-3
title: Vendored client gates: roadmap-gate.yml
status: approved
saved: 2026-08-10T12:03:54+00:00
story: FORGE-ALIGN-3
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
---

# Plan — FORGE-ALIGN-3: Vendored client gates (roadmap-gate.yml)

> Story FORGE-ALIGN-3, epic `strict-alignment` (final story), spec
> `docs/specs/strict-alignment.md`. Branch
> `feat/FORGE-ALIGN-3-vendored-client-gates-roadmap-gate-yml`.

## Problem

Clients have no CI teeth for the roadmap: Gate A (`pr-ticket-check.yml`),
`pr-link.yml`, and `board-invariant.yml` are harness-internal, and of the
three vendored workflows only factory-scaffold can red a PR — it never reads
the roadmap. `feat: add offline feature` PRs merged untraced in minegate.

Planning exploration also surfaced two pre-existing defects the gate would
trip over on day one:

1. **`check_pr_ticket.py` crashes on a client's first roadmap PR** —
   `roadmap_at()` runs `git show <base>:plans/roadmap.json` and the shared
   `git()` raiser dies on a base ref that predates the file (exactly the PR
   that introduces the roadmap).
2. **Branch inference only knows `feat/{key}-`** — the KnackLabs constitution
   mandates Git Flow `feature/*`, so every convention-compliant client branch
   fails inference and silently depends on a `Ticket:` body line.

And a third, deferred rather than fixed here: vendored push-triggered
workflows hardcode `branches: [main]`, so on a `develop`-default client their
push legs never fire (pre-existing, own story).

## Scope / Non-goals

**In scope:** the vendored `.github/workflows/roadmap-gate.yml` (PR job +
default-branch push job, both behind one arming step); the `COPY_WORKFLOWS`
entry; the two `check_pr_ticket.py` root-cause fixes; decision 0036 (arming);
the WORKFLOW.md gates-section rewrite; tests; one deferral.

**Non-goals:** the harness's own internal gate workflows are untouched (spec
boundary); NO default-branch retrofit of factory-scaffold/harness-health
(deferral with trigger); NO new `forge` subcommand for the arming read (a
one-line step reads the file); NO client rollout in this story — the myclaw
pilot runs via `forge upgrade` after merge.

## Acceptance Criteria

1. `roadmap-gate.yml` is vendored (joins `COPY_WORKFLOWS`,
   `scaffold.py:29-33` — all ten consumers are list-driven, so one line is
   the whole vendoring change). PR job: checkout `fetch-depth: 0`, the same
   three-env invocation of `check_pr_ticket.py` as the internal workflow, NO
   pytest self-test step (clients have no `factory/tests`). Push job: guarded
   `if: github.event_name == 'push' && github.ref_name ==
   github.event.repository.default_branch`, runs `forge project audit` —
   **full audit** (grilled 2026-08-10: the human chose full severity over
   alignment-only; incomplete pending stories, missing outcomes, and vendor
   drift red the client main along with the coverage gaps).
2. **One arming step, two conditions:** armed iff
   `constitution/VENDORED_FROM` exists (client, not the harness — the
   discriminator factory-scaffold.yml already uses) AND `plans/roadmap.json`
   parses with ≥1 epic (python3 one-liner writing `armed=` to
   `$GITHUB_OUTPUT`; job-level `if:` cannot read workspace files). Both jobs
   skip when unarmed: an unprepared client stays green, and the harness repo
   (no VENDORED_FROM, despite its 3-epic roadmap) never double-runs its
   internal gates. A malformed roadmap.json fails the step loudly — fail
   closed, not silently unarmed.
3. `check_pr_ticket.py`: a base ref with no `plans/roadmap.json` resolves to
   `{}` instead of a git fatal (the first-roadmap PR works); branch
   inference accepts `feature/{key}-*` alongside `feat/{key}-*`.
4. Decision **0036** records the arming contract: vendored-only +
   roadmap-with-epics = opt-in; default-branch guard with the stated Git
   Flow caveat (default may be `main` while integration is `develop` — the
   gate follows the default branch, by design); full-audit severity on push.
5. `WORKFLOW.md:267-279` rewritten: the *contract* is now vendored as
   `.github/workflows/roadmap-gate.yml` (named by path — legal under 0034
   the moment it joins `COPY_WORKFLOWS`), while the harness's own
   implementations stay internal; the Project Roadmap section gains the
   arming sentence. `test_vendored_docs_do_not_reference_unvendored_workflows`
   stays green.
6. `test_scaffold_delivers_factory_workflows` asserts the new file; upgrade
   refresh needs no change (list-driven, pinned by the existing
   `test_upgrade_refreshes_factory_workflows_and_keeps_project_ones`).

## Technical Approach

### `.github/workflows/roadmap-gate.yml` (new, vendored)

`on: pull_request:` + bare `push:`. Two jobs, each: checkout (PR job with
`fetch-depth: 0`), setup-python 3.11, the arming step, then the gate step
guarded `if: steps.arm.outputs.armed == 'true'`:

- `pr-contract` (`if: github.event_name == 'pull_request'`): env
  `BASE_SHA`/`HEAD_BRANCH`/`PR_BODY` from the event →
  `python3 factory/scripts/check_pr_ticket.py --base --head-branch --pr-body`
  (mirrors `pr-ticket-check.yml:23-32`).
- `coverage` (push-to-default-branch guard above): `python3
  factory/scripts/forge.py project audit`.

Conditional-step style follows the house pattern (`factory-scaffold.yml:19-28`
`is_harness` step output). A header comment states the both-places contract
the same way factory-scaffold.yml:13-18 does — here: "vendored to clients;
no-ops in the harness (no VENDORED_FROM) and in clients that have not
authored a roadmap with epics yet."

### `check_pr_ticket.py` fixes

- `roadmap_at()`: missing path at the base ref → `{}` (fix at the
  `git show` call site, not by weakening the shared `git()` raiser other
  callers depend on).
- `branch_ticket()` (`:55-60`): accept `feature/{key}-` as well as
  `feat/{key}-` — one prefix tuple, covered by tests both ways.

### Decision + docs + deferral

- `forge decision new client-gates-arm-on-roadmap` → 0036, content per AC4.
- WORKFLOW.md rewrite per AC5.
- `forge defer add`: default-branch generality for
  `factory-scaffold.yml`/`harness-health.yml` push legs — trigger: "a client
  whose default branch is not main reports a never-firing push workflow, or
  the myclaw/minegate pilot lands on a non-main default branch."

### Tests (`factory/tests/test_gates.py`)

- Workflow-shape test in the style of `:5435-5443`/`:5803-5810`: parse
  `roadmap-gate.yml`; assert both jobs exist, the arming step checks
  VENDORED_FROM and epics, the push job carries the default-branch guard,
  the PR job passes the three env vars, and there is no pytest self-test
  step.
- `test_scaffold_delivers_factory_workflows` gains the one assert.
- `check_pr_ticket` unit tests: PR introducing `plans/roadmap.json`
  (base-absent) passes instead of dying; `feature/KEY-1-slug` branch infers
  the ticket.

## Decisions

One new record, **0036 `client-gates-arm-on-roadmap`** (created right after
approval, before decomposition; grilled at spec level 2026-08-10 and the
severity grilled at plan level): arming = `VENDORED_FROM` present AND
roadmap has ≥1 epic; disarmed repos are green by design and the `no-roadmap`
audit gap is the pressure to author; push gate = full `project audit`
severity; gate follows the repository default branch (Git Flow caveat
stated). Simpler shape rejected and stated: hardcoding `main` like the other
vendored workflows would silently never fire for Git Flow clients — that
defect is real, deferred for the two existing workflows, and not worth
replicating in a brand-new one.

## Surface Impact

| Surface | Class | Notes |
|---|---|---|
| Runtime behavior | Changed | new vendored workflow; Gate A script fixes |
| API | N-A | — |
| Data/schema | Unchanged by design | no artifact changes; VENDOR_MANIFEST unaffected (workflows not hashed) |
| CLI/ops | Read-only | audit/check_pr_ticket invoked, not changed in surface |
| UI | N-A | — |
| Docs | Changed | WORKFLOW.md gates section + roadmap arming sentence; decision 0036 |
| Tests | Changed | workflow-shape, scaffold-delivery, two Gate A unit tests |

## Task Decomposition

One bounded task (disjoint scope, one worker):

1. **FORGE-ALIGN-3.1 — vendored gate + fixes + decision + docs + tests** —
   `roadmap-gate.yml`; `COPY_WORKFLOWS` line; `check_pr_ticket.py` fixes;
   WORKFLOW.md; deferral entry; tests.

## Risks

- **Workflow logic is only shape-tested locally** — Actions semantics
  (event payloads, `$GITHUB_OUTPUT`) run nowhere but CI. Mitigation: the
  jobs reuse the exact invocation shapes of the proven internal workflows,
  and the myclaw pilot is the first live validation before minegate.
- **Full-audit severity reds legacy client mains at pilot** — intended and
  chosen; the arming rule means only repos that opted in (roadmap authored)
  feel it.
- **The harness's own PRs run the new workflow file** — both jobs no-op via
  the VENDORED_FROM condition; the shape test pins that condition so it
  cannot be dropped silently.
- **`git show` fix must not weaken other `git()` callers** — the fallback
  lives at the one call site; existing Gate A tests plus the two new ones
  hold the contract.

## Verify Plan

- **Gate tests:** new + existing `-k "pr_ticket or gate_a or
  scaffold_delivers or roadmap_gate"` green; full suite via `verify.py`
  (structural + scaffold + tests).
- **Live dogfood:** this repo's PR for this story runs the new workflow —
  both jobs must show as skipped/green (unarmed in the harness) while the
  internal `pr-ticket-check` still passes; `python3 -c` YAML-parse the new
  workflow file locally.
- **Vendor check:** `forge init` smoke into a temp dir delivers
  `roadmap-gate.yml` (covered by the extended scaffold-delivery test).
