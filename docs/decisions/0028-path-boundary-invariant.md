---
status: accepted
confirmed_by: "vrknetha"
date: 2026-08-06
stories: [FORGE-BOUNDARY-1]
supersedes: ""
---

# Path Boundary Invariant

## Context

`repository-escape` is a RECURRING finding class. It first escalated at
FORGE-UPG-1 and has now been found and patched **five times** across the three
commands that write into a client repository — `forge init`, `forge adopt`,
`forge upgrade`:

- upgrade preservation dereferenced symlinks, copying a link's referent into
  the repo under the link's name while retirement deleted the original;
- adopt's `vendor_file` had to grow a symlink + ancestor check;
- init's `APPEND_OR_TOUCH` preflight had to reject symlinked destinations;
- the new `record-origin.json` write had to be preflighted in both init and
  adopt, and then again for a symlinked `.factory` ancestor (PH-5.4).

Each was fixed where it was found, in that command's own idiom. That is exactly
the pattern decision 0005 says to stop: a class patched a fourth (here, fifth)
time is a design signal, not a fix queue. The commands check the boundary in
three different ways and some write sites check nothing, so the next escape is
already latent in whichever site was missed.

The danger is concrete and severe: these commands run with the user's
privileges against a real project directory. A destination that resolves
outside the target — through a symlink, a symlinked ancestor, or `..` — writes
into, or deletes from, a **different** repository than the one named. The blast
radius is another project's files.

## Decision

Every write a client-writing command makes into a target repository must be
proven to land **inside the target root before the write happens**. This is one
shared, mandatory check, not three idioms:

- The resolved destination, and every ancestor between the target root and it,
  must resolve to a path inside the resolved target root. A symlink, a
  symlinked ancestor, or a `..` component that escapes the root is refused.
- The check runs in the command's **preflight**, before the first mutation, so
  an escape stops the command clean rather than halfway through a partial write.
- Directory-tree copies (`copytree`) validate their **root destination** and
  **every destination entry** before the walk (the preflight walk matches the
  copy's own traversal); a wrapper that validates only the top call is not
  sufficient if the destination can contain links. Source content is
  dereferenced into those validated destinations — the source tree is the
  harness's own, trusted — and a source symlink is not preserved as a link, so
  an outward one cannot be recreated in the target as a fresh escape.

> **Correction, 2026-08-06 (during FORGE-BOUNDARY-1).** An earlier draft of this
> bullet said copies "never follow symlinks into the tree," which read as
> preserving source links (`copytree symlinks=True`). Implementation and review
> established the opposite is safe: preserving a source link would recreate an
> outward one as an escape, so source content is dereferenced (`symlinks=False`)
> and the preflight walks `followlinks=True` to validate every real destination.
- Every write site routes through the shared check. A new write site that does
  not is the bug; a test per command asserts the escape is refused.

`init`, `adopt`, and `upgrade` share one boundary helper. No command re-derives
the rule.

## Consequences

- The recurring class is closed structurally, not by a sixth patch: a future
  write site inherits the check or fails a test, rather than shipping an escape.
- A small, auditable surface: one helper, called at every site, with per-site
  escape tests. The refactor is a consolidation, not new behaviour — a legal
  in-boundary write behaves exactly as before.
- Deferral D-0003 is discharged by FORGE-BOUNDARY-1, which audits every site
  against this invariant and pins each with a test.
- Cost accepted: `resolve()` on every destination is a stat per write. These
  commands run once per project setup, not in a hot path, so the cost is
  irrelevant against the safety it buys.
- This governs commands writing INTO a client repo. It does not change how the
  harness reads its own files, and it is not a sandbox for untrusted worker
  code (that remains D-0001's container question).
