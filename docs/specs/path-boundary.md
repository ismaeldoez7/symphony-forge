---
slug: path-boundary
title: The factory never writes outside the repo it was told to
status: draft
saved: 2026-08-06T07:33:47+00:00
---

# The factory never writes outside the repo it was told to

## Why

`forge init`, `forge adopt` and `forge upgrade` write files into a client
repository, running with the user's own privileges. A destination that resolves
outside the named target — through a symlink, a symlinked ancestor folder, or a
`..` component — writes into, or deletes from, a *different* repository than the
one the command names.

This is not hypothetical. `repository-escape` is a RECURRING finding class: it
has been found and patched **five times** across these three commands, each time
in that command's own idiom, because there is no single check they all share.
Some write sites validate the boundary; others validate nothing. The next
escape is already latent in whichever site was missed. Decision 0005 says a
class patched this many times is a design signal to consolidate, not to patch a
sixth time; decision 0028 states the invariant.

## Behaviour

Every write a client-writing command makes into a target repository is proven to
land inside the target root before the write happens, through one shared check
that all three commands call — never three idioms and never an unchecked site.

- The resolved destination, and every ancestor between the target root and it,
  must resolve inside the resolved target root. A symlink, a symlinked ancestor,
  or a `..` that escapes the root is refused.
- The check runs in preflight, before the first mutation, so an escape stops the
  command clean rather than halfway through a partial write.
- A directory-tree copy validates its root destination before it walks, and does
  not follow symlinks into the tree — validating only the top call is not enough
  when the tree can contain links.
- A legal, in-boundary write behaves exactly as it does today. This changes
  safety, not outcomes.

## Acceptance criteria

- `forge init`, `forge adopt` and `forge upgrade` route every write into the
  target through one shared boundary check that refuses a destination resolving
  outside the target root, including through a symlinked ancestor or `..`.
- The check runs in each command's preflight, before the first mutation.
- Every `copytree` validates its root destination before the walk and does not
  follow symlinks into the tree.
- Each of the three commands has a per-site test asserting that a symlinked
  destination and a symlinked ancestor are refused, and the recurring
  repository-escape class has a regression test it cannot silently reopen.
- A legal in-boundary run of each command produces the same result as before the
  refactor.
