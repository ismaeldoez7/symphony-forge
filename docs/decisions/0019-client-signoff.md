---
status: superseded
confirmed_by: "vrknetha"
date: 2026-08-04
stories: []
superseded_by: 0010-client-signoff
---

# Client Signoff

## Context

> **Superseded by 0010-client-signoff.** This record was minted on a branch that could not see 0010 — the same divergence that had `harness.yaml` pinned two different ways. Both were accepted and both said the same thing; `harness.yaml` pins 0010, so this one is retired rather than left as a second live answer to one question.

This project was signed off once already, on 2026-07-24, against
`0010-client-signoff` — maintainer plan approval standing in for client
sign-off on a harness maintenance repo. The evidence is still live in
`.factory/run.json` on `chore/codify-process-rules`: `client_signoff: true`,
`client_signoff_record: docs/decisions/0010-client-signoff.md`, confirmed by
vrknetha.

Two things have happened since, and together they left the mainline unsigned.

`0010` was superseded by `0014-specs-before-signoff`, which restated the gate
more strictly — confirmed specs plus a derived roadmap. Superseding replaced
the *rule*; it did not withdraw the *sign-off*. But `record_signoff.py` looks
for a decision record whose status is `accepted`, and `0010` no longer is.

Separately, PR #26 moved sign-off from a per-worktree flag in
`.factory/run.json` to a pinned, derived project fact: a `signoff_record:` line
in committed `harness.yaml` that every clone and every worktree reads
identically. `chore/codify-process-rules` predates that merge and still carries
the flag; `main` carries the mechanism with the pin empty. Neither line is
wrong, and neither can read the other's answer.

The practical cost is that no worktree branched from `main` can pass
`plan save`, and `roadmap add` refuses, so no new story can start on the
mainline at all — including the fix for the delegation reaping defect that
currently blocks every story from passing `verify.py`.

## Decision

Re-record this project's sign-off against this record so the pinned,
derived mechanism has a value on the mainline. This does not re-open the
sign-off question; it restates a confirmation that was already given, under the
record format the current gate reads.

The scope is unchanged from `0010`: this is the harness's own repository, and
maintainer plan approval is the sign-off. `0014` remains the governing rule for
what sign-off requires — confirmed specs and a roadmap derived from them.

## Consequences

`harness.yaml` gains `signoff_record: docs/decisions/0019-client-signoff.md`,
committed. From then on every worktree cut from the mainline derives sign-off
without re-establishing per-worktree state, which is the property PR #26 was
built for.

Sign-off stays a one-time project gate. It is never re-recorded per task; the
per-task human gate remains plan approval, which is grilled and enforced
against its own issue.

`0010` stays superseded and is not edited. This record supersedes nothing —
it is the same confirmation, re-recorded in the form the current gate can read.

The branch divergence itself is not resolved by this record. It is resolved
when `chore/codify-process-rules` merges; until then that branch keeps reading
its own flag, and reads the same answer.
