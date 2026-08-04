---
issue: FORGE-UPG-1
title: Legacy repo upgrade: one command, no residue
status: approved
saved: 2026-08-04T10:10:21+00:00
story: FORGE-UPG-1
decisions_reviewed:
  - 0001-determinism-contract
  - 0002-concurrency-one-task-per-branch
  - 0003-model-tiers-terra-explore-sol-implement
  - 0005-recurring-findings-escalation
  - 0006-lessons-ledger
  - 0007-stage-commit-loop
  - 0008-loop-health-audit
  - 0009-frozen-gate-integrity
  - 0011-orchestrator-runs-autoreview
  - 0012-project-level-memory
  - 0013-always-armed-planning-lock
  - 0014-specs-before-signoff
  - 0015-plan-contradiction-gate
  - 0016-machinery-dir-rename
---


# FORGE-UPG-1 — Legacy repo upgrade: one command, no residue

Spec: `docs/specs/legacy-upgrade.md` (confirmed). Roadmap story: `FORGE-UPG-1`.

## Context

The ask was "make `~/Workdir/agentstats` symphony forge ready". It already is
— adopted, vendored at `symphony-forge @ 8c68d27`, twelve stories shipped.
What it is not is *current*: that commit predates decision 0016, so its
machinery lives at `.agents/`, and `forge upgrade` cannot carry it across.

Decision 0016 closes with "client repos vendored from earlier harness versions
migrate on the next `forge upgrade`". No such migration was ever written.
Four repos are waiting on it — `agentstats`, `agentstats-AGS-12`,
`knacklabs-ats`, `myclaw`. Only `toolshed` is on `factory/`.

Running `forge upgrade` on agentstats today produces a repo carrying **two**
copies of the gate surface. `UPGRADE_TREES` (`upgrade.py:23`) vendors
`factory/` and never looks at `.agents/`; `write_manifest` hashes only
`GATE_TREES = ("factory/scripts", "factory/schemas", "factory/prompts")`
(`check_vendor_integrity.py:23`). The second copy is an unfrozen, unchecked
duplicate of every script the gates depend on — precisely the condition
decision 0009 exists to prevent. The preserve loop (`upgrade.py:83-101`) also
reads `factory/skills/{proposed,rejected}`, which in a pre-rename repo do not
exist, so skill-evolution state and installed project skills are stranded in
a tree that should not survive.

Separately, agentstats has an open story: `AGS-13` at phase `implementing`,
stage `AGS-13.2` still `active`. `forge stage migrate` adopts legacy stage
state into protected authority but records no base commit, and stage close
refuses without one (`stages.py:651`). Re-starting re-baselines to `HEAD`, and
AGS-13.2's work is already committed at `3d42674` — so it would then close on
an empty diff and be refused again. The repo would upgrade into a state where
its open story can never ship.

## Scope / Non-goals

**In scope.** `forge upgrade` retires a legacy `.agents/` tree; `forge stage
migrate` takes an explicit base commit.

**Non-goals.**
- Rewriting project-owned files. The upgrade *reports* stale `.agents/`
  references and the human fixes them inside the same reviewable diff. That
  boundary is what makes an upgrade diff readable (`upgrade.py:5`).
- Rewriting archived evidence under `.factory/history/`. Decision 0016 already
  designates itself the read-key for historical artifacts.
- Converting legacy task contracts. Prose `verify_commands` and opaque
  `required_tests` stay refused at record time; `forge doctor` already reports
  them (shipped in FORGE-DELEG-1) and the human re-records.
- Upgrading `knacklabs-ats` and `myclaw`. They become possible; running them
  is a separate decision per client repo.

## Acceptance Criteria

Taken verbatim from the roadmap story:

1. Upgrading a repo that carries `.agents/` leaves no `.agents/` tree and a
   complete `factory/` tree.
2. Skill-evolution state (`proposed`, `rejected`) and client-added skills
   under `.agents/skills/` survive at `factory/skills/`.
3. A path under `.agents/` with no counterpart in the vendored `factory/` tree
   aborts the upgrade and is named; nothing under it is deleted.
4. The upgrade output names every project-owned file still referencing
   `.agents/`, excluding archived evidence under `.factory/history/`.
5. The migration modifies no project-owned file.
6. Upgrading a repo already on `factory/` behaves exactly as before.
7. `forge stage migrate --base <sha>` records that base for each legacy stage
   it adopts, and refuses a base that does not resolve or is not an ancestor
   of `HEAD`.

## Technical Approach

### 1. `forge_cli/upgrade.py` — retire the legacy tree (AC 1, 2, 3, 5)

`legacy = (target / ".agents").is_dir()` is the whole detection rule.

**Preserve reads from wherever the machinery currently is.** The loop at
`upgrade.py:83-101` hardcodes `target / "factory" / "skills"`. Give it a
source root — `".agents" if legacy else "factory"` — while destinations stay
`factory/skills/<name>`. `PRESERVE_IN_AGENTS` keeps its name (it is stale
from the rename, but renaming it is not this story's diff).

**Retire by carry-then-verify, after the restore step (`upgrade.py:146-157`),
never before.** Preserved skills are already back under `factory/skills/` by
then, so their `.agents/` originals have counterparts and delete cleanly:

```
unknown = [rel for every file under .agents/ (skipping __pycache__ and *.pyc)
           if not (target / "factory" / rel).exists()]
if unknown: fail(naming them, and saying what to do)
shutil.rmtree(target / ".agents")
```

The refusal must name the repair, because the benign cause is a harness
release that *retired* a script: "if this is retired machinery, delete it and
re-run". Verified today against the real target — all 65 files under
agentstats' `.agents/` have a counterpart among the harness's 77, so the check
passes rather than aborting spuriously.

### 2. `forge_cli/upgrade.py` — report stale references (AC 4, 5)

After the migration, `git grep -l -F ".agents/"` in the target, dropping
`.factory/history/`. `git grep` searches **tracked** files only — which is the
point: agentstats carries `node_modules/` and `dist/`, and a `rglob` walk
there would be pathological. Print the survivors under a heading that says
they are the human's to fix. Write nothing.

Harness-owned files do not appear in that list because they were just
replaced: `.claude/settings.json`, `.codex/hooks.json`, `WORKFLOW.md`,
`docs/FACTORY.md`, `docs/QUALITY.md`, `constitution/` and the three factory
workflows all come from the harness. For agentstats the survivors are
`AGENTS.md` (9 references) and the active `.factory/decomposition.json` (2).

### 3. `forge_cli/stages.py` — an explicit base for a migrated stage (AC 7)

In `_cmd_migrate_locked` (`stages.py:1052`), beside the existing
`--confirm-workspace-state` guard: require `--base`, resolve it with
`git rev-parse --verify <base>^{commit}`, and require
`git merge-base --is-ancestor <base> HEAD`. Stamp the resolved sha onto every
stage the loop at `stages.py:1085-1091` already touches for `active`/`done` —
the same stages that get `task_sha256`.

`dirty_at_start` is deliberately left unset: `_measure` reads it with a `{}`
default, and `{}` is the honest baseline when the base is a commit —
everything since it is the story's work.

`--base` is required, not optional. `stage migrate` is a once-per-repo command
whose only consumer is
`test_stage_migrate_requires_confirmation_and_adopts_legacy_state`
(`test_gates.py:4030`); conduct §5 says a breaking replacement with no live
consumers deletes the old path rather than shimming it.

## Decisions

**No new decisions.** Both non-obvious choices were put to the human during
the spec grill and are recorded in the confirmed spec plus the grill artifact:

- Carry-then-verify instead of a wholesale delete — follows from decision 0009
  and the mixed-ownership contract already stated at `upgrade.py:29`.
- An explicit `--base` instead of inferring the merge-base with a default
  branch — agentstats has no remote to probe, and inferring would decide what
  counts as the story's work without saying so.

Reconciled against every ID in `./forge decision list --active`: 0016 is the
promise being kept; 0009 is why the duplicate tree is a defect rather than
untidiness; 0002 (one story per branch) is why a branch merge-base *would*
have been a defensible base and is named in the spec as the rejected option.
The remaining eleven do not bear on this diff. No contradictions.

## Surface Impact

| Surface | Status | Note |
|---|---|---|
| Runtime behavior | Changed | `forge upgrade` retires a legacy `.agents/` tree and can now refuse; `stage migrate` records a base |
| CLI/ops | Changed | `stage migrate` gains a required `--base <sha>`; upgrade output gains a stale-reference report |
| Data/schema | Changed | migrated stage entries carry `base_sha`. No schema loosened; no new artifact |
| Docs | Changed | `docs/specs/legacy-upgrade.md` (confirmed, already committed at `006a23b`) |
| Tests | Changed | new cases in `factory/tests/test_gates.py` for each refusal and for the retire/preserve/report path |
| API | N-A | no programmatic API surface in the harness |
| UI | Unchanged by design | the board is read-only by contract and renders story state, not vendoring state; an upgrade is a one-time CLI act with a reviewable diff as its output |

## Task Decomposition

Two tasks, split by file so each owns its boundary. Sequential (task-level
`--parallel` is refused).

| Task | Write scope | Serves |
|---|---|---|
| `FORGE-UPG-1.1` — retire the legacy tree and report what survives | `factory/scripts/forge_cli/upgrade.py`, `factory/tests/test_gates.py` | AC 1–6 |
| `FORGE-UPG-1.2` — an explicit base for a migrated stage | `factory/scripts/forge_cli/stages.py`, `factory/tests/test_gates.py` | AC 7 |

Both are `user_facing: false` — no design skills.

## Risks

- **A future harness release that retires a script aborts the upgrade for
  older repos.** A known ceiling, not a bug: the file has no counterpart, so
  carry-then-verify cannot tell it from client content. The refusal names the
  file and the repair. Not building an escape flag until a real retirement
  demands one.
- **`git grep` misses untracked project files that mention `.agents/`.** It
  also misses `node_modules/`, which is why it was chosen. An untracked file
  is not in the reviewable diff either, so it is out of the report's remit.
- **agentstats' AGS-13 needs more than this story, in a specific order.**
  `stage migrate` stamps `base_sha` AND `task_sha256` together. Migrating
  before the decomposition is re-recorded is a dead end: the new digest makes
  `_measure` refuse "contract changed after the stage started", `stage start`
  is the only sanctioned repair, and it re-baselines `base_sha` to `HEAD` —
  destroying the base and closing on an empty diff. **Re-record first, then
  migrate.** That is agentstats' work, done in agentstats, and it is why the
  Verify Plan ends there rather than at the harness test suite.

## Verify Plan

1. `python3 -m pytest factory/tests/` green; `check_dual_runtime.py` clean;
   AGENTS hygiene OK. AC 6 is carried by the existing suite —
   `test_upgrade_replaces_machinery_preserves_project`,
   `test_upgrade_refreshes_factory_workflows_and_keeps_project_ones`,
   `test_upgrade_preserves_client_claude_and_codex_surfaces` and
   `test_adopt_and_upgrade_refreeze_the_manifest` all run the non-legacy path
   and fail if it moved. No duplicate test for it.
2. Scratch-clone rehearsal on a synthetic legacy repo: `.agents/` mirroring
   the harness plus a client skill and `proposed/rejected` → upgrade → no
   `.agents/`, skills present at `factory/skills/`; then add
   `.agents/notes/mine.md` → upgrade aborts, names it, `.agents/` intact.
3. **The real target.** On a branch in `~/Workdir/agentstats`:
   `forge upgrade --target ~/Workdir/agentstats` → no `.agents/`;
   `check_vendor_integrity.py` and `check_factory_scaffold.py` green;
   `check_dual_runtime.py` green (its thin-adapter rule at line 346 requires
   hook scripts under `factory/scripts/`, which the old `settings.json`
   violated); the gate tests pass inside agentstats; the report names
   `AGENTS.md`, which is then fixed by hand in the same branch.

   Then, **in this order**: re-record AGS-13's decomposition with
   `required_tests: []` and `verify_commands: ["pnpm test"]` (the repo's real
   runner — the production transcript stays in the recorded testing artifact,
   which is what it was always evidence for), and only then
   `forge stage migrate --base $(git merge-base HEAD main) --confirm-workspace-state`,
   so the base and the current task digest are stamped together and
   `stage done AGS-13.2` measures the story's committed work. Nothing is
   merged — the branch is left for review.
