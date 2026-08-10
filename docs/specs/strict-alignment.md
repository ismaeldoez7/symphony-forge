---
slug: strict-alignment
title: The record updates itself, and clients are held to the roadmap
status: confirmed
saved: 2026-08-10T08:19:57+00:00
---

# The record updates itself, and clients are held to the roadmap

> Captured 2026-08-10 from operator feedback on the first real client migration
> (knacklabs/minegate-mineops). Every gap below was reproduced live in that repo.

## Why

Four failures, in the order they hurt:

1. **The context ledger check fires, but nothing updates the ledger.**
   `docs/context/ledger.json` is the only self-fresh ledger (sha256 per file,
   `context scan --check` hard-fails client CI), yet `forge context scan` is a
   manual step and the harness registers no post-edit hook seam at all — so the
   deterministic outcome of editing a context doc is a red PR, not an updated
   ledger. Minegate PR #69 failed this check three times in one morning.
2. **Migration is silent about specs, epics, and the roadmap.** The migrate
   skill never mentions them; `forge adopt` creates an empty `docs/specs/` and
   no `plans/roadmap.json`. Minegate migrated with 20 decisions' worth of
   discovery (office hours, eng/design/CEO reviews) and zero specs, zero epics,
   no roadmap — and no command said a word.
3. **Every detector reports OK on emptiness.** `forge doctor` early-returns
   when `plans/roadmap.json` is absent; `project audit` on an empty roadmap
   prints "Project audit OK"; `sanitise --check` composes those same
   detectors. The one real coverage check (confirmed specs must be referenced
   by roadmap stories) lives only inside sign-off and runs exactly once; a spec
   confirmed later sits unreferenced forever, painted grey on the board.
4. **Clients have no CI teeth for the roadmap.** Gate A (every PR declares its
   completed work record) and the board invariant are harness-internal
   workflows, deliberately un-vendored (decision 0034). Of the three vendored
   workflows, only factory-scaffold can red a PR and it never reads specs or
   the roadmap; harness-health runs `project audit` under `set +e` and files an
   issue at most. Result: `feat: add offline feature` PRs merged untraced, and
   the operator had to reconstruct alignment by hand.

The contract this capability enforces: **what the ledger check already does for
the context inbox, the harness must do for the roadmap — automatically updated
where mechanical, hard-failed in CI where it needs a human.**

## Behaviour

**Determinism is non-negotiable (decision 0001).** Every rule below is a
deterministic mechanism — a hook, a detector with an exit code, or a CI check —
never agent discipline. Detection never fabricates content: gaps are named and
refused, and authoring stays with a human (project-record stance).

### The context ledger updates itself

- A post-edit hook seam is added to the vendored hook set (today only
  SessionStart / PreCompact / PreToolUse / Stop exist). When an agent writes a
  file under `docs/context/`, the hook runs `forge context scan` — cheap,
  idempotent — so the ledger diff rides in the same commit as the doc change.
- The existing `git commit` interception gains the same auto-scan as a belt:
  a commit that includes `docs/context/` changes re-scans first, covering
  human-made edits committed through an agent session.
- `context scan --check` in CI stays exactly as-is: the backstop for edits made
  entirely outside sessions.

### Emptiness and coverage are audit failures, not grey prose

`project_gaps` (already the composition point feeding `project audit`,
`sanitise --check`, and the harness-health issue) gains two gap kinds:

- **no-roadmap**: discovery material exists (any of: harvested context,
  decisions, confirmed specs) but `plans/roadmap.json` is absent, empty, or has
  no epics. `doctor`'s early-return on a missing roadmap is fixed the same way.
- **spec-coverage**: a confirmed spec no roadmap story references — the exact
  set the board already computes and sign-off already blocks on, now checked
  continuously instead of once.

Both exit non-zero from `project audit` and `sanitise --check`. Neither
auto-creates anything.

### Migration and adoption name the gap

- The migrate skill gains an explicit step after harvest: state whether
  confirmed specs / epics / a derived roadmap exist; when they do not, say so
  and offer the existing paths (spec save+confirm → roadmap derive) — never
  fabricating content from harvested material without the human in the loop.
- `forge adopt`'s closing hint names specs and roadmap alongside context scan.

### Clients get the same teeth the harness has

- A vendored **`roadmap-gate.yml`** workflow (joins `COPY_WORKFLOWS`) with two
  jobs: a PR job that hard-fails a client PR landing work without declaring
  its completed roadmap story or ledgered work window — the client profile of
  Gate A, same strict declare-all contract as decision 0033, no docs-only
  exemption (quickfix/lite windows are the escape hatch) — and a push-to-main
  job that hard-fails on the coverage gaps above, so a client main cannot stay
  silently non-compliant.
- **Arming is the roadmap itself** (grilled 2026-08-10): both jobs arm only
  when `plans/roadmap.json` exists with at least one epic — the repo has opted
  into the board. A client without a roadmap does not go red by pulling the
  upgrade; it gets the `no-roadmap` audit gap pushing it to author. Recorded
  as a decision record when story 3 is planned.
- Vendoring the workflow is what makes referencing it client-safe: decision
  0034's rule is unchanged, and the vendored-docs test keeps passing because
  the workflow ships with the docs that name it.

## Acceptance criteria

- Editing or adding a file under `docs/context/` in an agent session updates
  `ledger.json` without any manual command; the CI freshness check is
  unchanged and stays green for such commits.
- A repo with discovery material but no roadmap (or no epics) fails
  `project audit` and `sanitise --check` with a named `no-roadmap` gap;
  `doctor` reports it instead of returning clean.
- A spec confirmed after sign-off with no referencing story is a named
  `spec-coverage` gap with a non-zero exit, not only grey board prose.
- Migrating a repo with prior discovery docs surfaces "no specs / no epics /
  no roadmap yet" in the skill flow, with the authoring commands named;
  nothing is auto-generated.
- In a client whose roadmap has at least one epic, a PR that lands work with
  no declared completed story or window fails the vendored `roadmap-gate.yml`
  PR job, and a coverage gap on main fails its push job (not issue-only).
- A client with no roadmap does not go red by pulling the upgrade — the gates
  stay disarmed and the `no-roadmap` audit gap is the visible pressure.
- Every rule is a deterministic mechanism (hook, exit code, or CI check); the
  vendored-docs client-safety test (0034) still passes.

## Boundaries

- Detection and refusal only — no auto-generation of specs, epics, roadmap
  entries, or history (project-record: mark, never fabricate).
- No external tracker; the in-repo roadmap stays the board of record (0017).
- The harness repo's own internal gates (pr-ticket-check, board-invariant,
  pr-link) are untouched; this adds a client profile, it does not move them.
- Legacy clients reach the bar via `forge upgrade` + the upgrade skill, not
  silent auto-migration. Pilot client: **myclaw** (grilled 2026-08-10) — its
  roadmap exists, so the gates arm immediately and its known authoring gaps
  (epic-less and incomplete stories) become the red list that drives
  completion; minegate follows once the pilot holds.

## Decomposition (epic → stories)

1. **Self-updating context ledger** — the post-edit hook seam + commit-time
   auto-scan; CI check unchanged. (Smallest; ships first.)
2. **Coverage detectors + migration prompts** — `no-roadmap` and
   `spec-coverage` gap kinds in `project_gaps`, doctor fix, migrate-skill step,
   adopt hint.
3. **Vendored client gates** — the roadmap-gate workflow (client Gate A +
   coverage invariant) into `COPY_WORKFLOWS`, the arming decision for legacy
   clients, upgrade-skill rollout.
