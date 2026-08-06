---
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
---

# FORGE-BOUNDARY-1 — Every client-writing command obeys one path-boundary check

## Problem

`repository-escape` is a RECURRING finding class, escalated at FORGE-UPG-1 and
patched five times since — each in one command's own idiom. `forge audit` flags
it as an ignored escalation (6 ships, no consolidating decision or refactor).
Decision 0005 says stop patching and consolidate; decision 0028 states the
invariant; this story applies it.

A read-only map of every filesystem-mutating site across the three
client-writing commands found ~60 write sites and the following coverage:

- **`adopt`**: almost every site is unguarded. `vendor_file` has a partial
  check (leaf symlink + `dst.parent` only when it exists, no ancestor walk, no
  `resolve()` on a missing parent); ~18 other sites check nothing.
- **`upgrade`**: almost every site is unguarded. Only the `.agents` rmtree and
  the `harness.yaml` leaf-symlink check are partial; the replacement
  `copytree`/`rmtree` roots and ~15 direct writes check nothing.
- **`init`**: sites are only *conditionally* guarded by `_collisions`, which
  runs solely for an existing non-empty target without `--force` — not a
  universal boundary preflight.

The shared helper that exists, `check_record_origin_writable`, guards one file
and still misses a non-existent tail below a symlinked ancestor — so even the
most recent fix has the gap this story closes.

Python floor is 3.10 (`forge:22`), so `Path.is_relative_to` and
`resolve(strict=False)` are available; `forge_cli` is stdlib-only.

## Scope / Non-goals

In scope: one shared boundary helper, applied at every write site in `init`,
`adopt` and `upgrade`, validated in each command's preflight, with per-command
escape tests and a regression test for the recurring class.

Out of scope, deliberately:

- **No behaviour change for a legal, in-boundary run.** This is a consolidation
  (0028): a write that lands inside the target behaves exactly as today. Every
  existing upgrade/adopt/init test must stay green unchanged.
- **Not a sandbox for untrusted worker code.** That is D-0001's container
  question, not this. This governs the harness's own writes into a target.
- **No new dependency, no non-stdlib path library.** One helper in the existing
  scaffold module (already imported by adopt) or a small sibling.
- **The source tree is trusted.** `copytree` following *source* symlinks copies
  the harness's own referents; the escape vector is the *destination* root or a
  dest ancestor being a symlink, which is what the root check covers.
- **`roadmap.json` merge fragility and the review-drift / decayed-lesson
  loop-health items are separate work**, not folded in here.

## Acceptance Criteria

Verbatim from the roadmap story, each with its proof:

1. `init`, `adopt` and `upgrade` route every write into the target through ONE
   shared boundary check that refuses a destination resolving outside the target
   root, including through a symlinked ancestor or `..`. Proof: the helper is
   the single validator, and a test asserts each command refuses a symlinked
   destination and a symlinked ancestor.
2. The check runs in each command's preflight, before the first mutation, so an
   escape stops the command clean rather than mid-write. Proof: a test asserts
   an escape leaves the target unmodified (no partial write).
3. Every `copytree` validates its root destination before the walk and does not
   follow symlinks into the tree. Proof: a test with a symlinked tree-root
   destination is refused; tree copies preserve rather than follow source links.
4. Each command has a per-site escape test, and the recurring repository-escape
   class has a regression test it cannot silently reopen. Proof: the tests exist
   and fail if the helper is bypassed at any site.
5. A legal in-boundary run of each command produces the same result as before.
   Proof: the full existing suite stays green with no test weakened.

## Technical Approach

**The helper (Task 1), stdlib-only, in `scaffold.py`** (already imported by
`adopt` and `upgrade`), so all three share one import:

```
def assert_target_destination(target: Path, dst: Path) -> Path:
    # Resolve target once; resolve dst with strict=False (the tail may not
    # exist yet). Reject symlink loops (OSError/RuntimeError) and any resolved
    # path not inside the resolved target. Return dst unchanged for chaining.
```

It follows the existing sign-off-path pattern (`factory_lib.py:388`) for loop
rejection. `check_record_origin_writable` is reimplemented on top of it, closing
its own missing-tail-below-symlinked-ancestor gap.

**Applying it (Tasks 2–4), one command per task** because each command's sites
are disjoint and one file plus its tests is a bounded session:

- Direct writes/mkdirs/deletes/copies: wrap the destination in
  `assert_target_destination(target, dst)` at the site, and hoist the checks
  into the command's preflight where the destination set is known before the
  first mutation.
- `copytree`/`rmtree`: validate the ROOT destination before the walk/delete. For
  `init`'s `dirs_exist_ok=True` merges, preflight each destination leaf. Tree
  copies preserve source symlinks (`symlinks=True`) rather than follow them, so
  a link in the source is copied as a link, not its referent.
- `adopt.vendor_file`'s local check is replaced by the shared helper; the two
  partial `upgrade` checks (`.agents` root, `harness.yaml` leaf) route through it
  while keeping their existing legacy-content validation.

**Rejected:** a per-command idiom (the exact pattern that recurred five times);
a decorator/monkeypatch over `shutil` (too clever, hides the check at the call
site where a reviewer must see it); validating only leaf paths (misses symlinked
ancestors, the actual escape); a new path library (stdlib suffices at 3.10).

## Decisions

Decision `0028-path-boundary-invariant` (proposed) is the design authority for
this story and must be **accepted** before the decomposition is recorded —
acceptance is human chat confirmation. It states the invariant and the shared-
check requirement. No other new decisions: every choice here derives from 0028
or an existing record (0005 the escalation trigger, 0017 the repo as the thing
being protected, 0009 the frozen gate surface unaffected).

## Surface Impact

| Surface | Classification | Notes |
| --- | --- | --- |
| Runtime behavior | Changed | init/adopt/upgrade refuse an out-of-boundary destination; a legal write is unchanged. |
| API | N-A | No HTTP surface. |
| Data/schema | Unchanged by design | No artifact shape changes; the helper validates paths, writes nothing new. |
| CLI/ops | Changed | The three commands gain a preflight refusal; their success path and flags are unchanged. |
| UI | Unchanged by design | The board does not write into a target. |
| Docs | Unchanged by design | Behaviour for legal runs is identical; no user-facing workflow changes. A code comment at the helper is the durable explanation. |
| Tests | Changed | Helper unit tests; per-command symlinked-destination and symlinked-ancestor escape tests; a partial-write-leaves-target-clean test; the recurring-class regression test. |

## Task Decomposition

Four sequential tasks in one worktree (0002). Task 1 is the foundation the other
three consume; each command task is disjoint and bounded.

1. **The shared boundary helper** → AC1 (foundation), AC-loop regression. Scope:
   `factory/scripts/forge_cli/scaffold.py`, `factory/tests/test_gates.py`.
   `assert_target_destination`, `check_record_origin_writable` reimplemented on
   it (closing its own gap), and the helper's unit tests (symlinked ancestor,
   `..`, symlink loop, legal path passes through).
2. **init routes every site through the helper** → AC1–5 for init. Scope:
   `factory/scripts/forge_cli/scaffold.py`, `factory/tests/test_gates.py`.
   Preflight all destinations; fix the three `copytree` roots and their
   `dirs_exist_ok` leaves; per-site escape tests.
3. **adopt routes every site through the helper** → AC1–5 for adopt. Scope:
   `factory/scripts/forge_cli/adopt.py`, `factory/tests/test_gates.py`. Replace
   `vendor_file`'s local check; cover the ~18 unguarded sites; per-site tests
   (adopt has no escape test today).
4. **upgrade routes every site through the helper** → AC1–5 for upgrade. Scope:
   `factory/scripts/forge_cli/upgrade.py`, `factory/tests/test_gates.py`.
   `copytree`/`rmtree` root checks, the ~15 direct writes, the two partial
   checks routed through the helper; per-site tests.

`user_facing: false` — these are CLI setup commands, not a user-visible product
surface; no functional check required.

## Risks

- **A weakened existing test.** The temptation under a big refactor is to relax
  a test that now trips the boundary check. Mitigation: AC5 forbids it; every
  existing init/adopt/upgrade test must pass unchanged, and the reviewer focus
  says a weakened test is a blocking finding.
- **Missing a site — the exact failure that recurred.** Mitigation: the map
  enumerates all ~60 sites; each task's test asserts the helper is reached at
  its command's sites, and a bypass fails. A site added later inherits the
  preflight or fails its command's escape test.
- **copytree following source symlinks.** Mitigation: tree copies use
  `symlinks=True` so a source link is preserved, not followed; the destination
  root is boundary-checked before the walk.
- **Recurring-findings tripwire.** This story IS the consolidation of the
  `repository-escape` class per 0005 and 0028. The other RECURRING class,
  `reviewed-separately`, is a review-provenance artifact, not a code defect, and
  is out of scope; if review flags it here, note it, do not fold it in.

## Verify Plan

Deterministic, the same commands CI runs (`.envrc` names them, harness-only):

```bash
python3 factory/scripts/verify.py
```

running `check_dual_runtime.py`, `check_factory_scaffold.py`, and
`pytest factory/tests -q`. Per-task verify commands are runnable pytest
selections. What falsifies the work: any of the three commands writing to a
symlinked destination or through a symlinked ancestor; a partial write left
behind after a refused escape; a `copytree` root unchecked before its walk; or
any existing legal-run test needing to be weakened. Each has a test. Review is
one autoreview pass, three lenses (0011).
