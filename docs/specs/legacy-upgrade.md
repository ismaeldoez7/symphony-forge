---
slug: legacy-upgrade
title: Legacy repo upgrade: one command, no residue
status: confirmed
saved: 2026-08-04T10:00:36+00:00
---

# Legacy repo upgrade: one command, no residue

## Capability

`forge upgrade` carries a client repo vendored before the `factory/` rename
onto the current harness in one command, leaving no stale machinery, no
orphaned project state, and no story that can no longer be closed.

## Why

Four client repos are vendored at `.agents/`-era commits — `agentstats`,
`agentstats-AGS-12`, `knacklabs-ats`, `myclaw`. Decision 0016 states that
"client repos vendored from earlier harness versions migrate on the next
`forge upgrade`". That promise is not implemented:

1. **The old machinery tree is left behind.** `upgrade.py` replaces
   `factory/`, `constitution/` and `harness/` and never looks at `.agents/`.
   Upgrading today produces a repo carrying *two* copies of the gate surface.
   Only the `factory/` copy is hashed into `constitution/VENDOR_MANIFEST.json`
   (`check_vendor_integrity.GATE_TREES`), so the second copy is an unfrozen,
   unchecked duplicate of every script the gates depend on — the exact
   condition decision 0009 exists to prevent.

2. **Project state under the old tree is orphaned.** The preserve loop reads
   `factory/skills/{proposed,rejected}` and client-added skill directories.
   In a pre-rename repo those live at `.agents/skills/`, so skill-evolution
   state and installed project skills are stranded in a tree that should not
   survive the upgrade.

3. **A story that was in flight cannot be closed.** `forge stage migrate`
   adopts legacy workspace stage state into protected authority but records no
   base commit, and stage close refuses without one (`stages.py:651`).
   Re-starting the stage re-baselines to `HEAD`, and a legacy story whose work
   is already committed then closes on an empty diff — refused again. The repo
   upgrades into a state where its open story can never ship.

## Behaviour

**The legacy layout is detected and retired — without a wholesale delete.**
When the target carries `.agents/` and the harness ships machinery at
`factory/`, `forge upgrade` treats `.agents/` as the previous location of the
same tree. Skill-evolution directories and client-added skills are carried
from `.agents/skills/` into `factory/skills/` under the mixed-ownership rule
that already protects `factory/skills/`. The old tree is then removed only if
every file still in it has a counterpart path in the newly vendored
`factory/` tree — that is, only if it is provably the machinery it replaced.
A path the harness never shipped aborts the upgrade and is named, because the
file performing the delete is the same file that promises never to delete
client additions. A repo already on `factory/` upgrades exactly as it does
today.

**Stale references are reported, never rewritten.** Project-owned files that
still name `.agents/` are listed in the upgrade output so the human fixes them
inside the same reviewable diff. The upgrade does not edit project-owned
content — that boundary is what makes an upgrade diff readable. Archived
evidence under `.factory/history/` is excluded from the report: it is
immutable, and decision 0016 is its read-key.

**A story that was open at upgrade time stays closable.** `forge stage
migrate` records a base commit for each legacy stage it adopts, so the work
the story already did is inside the measurement rather than behind it. The
base is stated, not inferred: the command takes `--base <sha>` and validates
that it resolves and is an ancestor of `HEAD`. Migration is already a
one-time act gated on `--confirm-workspace-state`, so the base belongs to the
same human inspection; guessing it from branch topology would decide what
counts as the story's work without saying so.

## Acceptance criteria

- Upgrading a repo that carries `.agents/` leaves no `.agents/` tree and a
  complete `factory/` tree.
- Skill-evolution state (`proposed`, `rejected`) and client-added skills under
  `.agents/skills/` survive the upgrade at `factory/skills/`.
- A path under `.agents/` with no counterpart in the vendored `factory/` tree
  aborts the upgrade and is named; nothing under it is deleted.
- The upgrade output names every project-owned file still referencing
  `.agents/`, excluding archived evidence under `.factory/history/`.
- The migration modifies no project-owned file.
- Upgrading a repo already on `factory/` behaves exactly as before.
- A story active at upgrade time can be adopted and closed: `stage migrate
  --base <sha>` records that base for each legacy stage it adopts, and refuses
  a base that does not resolve or is not an ancestor of `HEAD`.

## Boundaries

Archived evidence under `.factory/history/` keeps its `.agents/` paths.
Legacy task contracts — prose `verify_commands`, opaque `required_tests` —
are not auto-converted: `forge doctor` already reports them and the human
re-records the decomposition. Upgrading is still a reviewed diff on a branch,
never an in-place mutation of a client repo's main line.
