---
slug: gates-stale-only-on-what-they-read
title: Gates stale only on what they read
status: confirmed
saved: 2026-09-11T16:37:36+00:00
---

# Gates stale only on what they read

## Why

Shipping one 17-file client task through this harness took eight re-runs of
gates that had already passed. None was caused by the work changing: each was a
gate invalidated by an edit it never read.

The measured cases, all from GRANTED-1-T1 on 2026-09-11:

- A clean three-lens review stamped the stage. Closing the stage then failed on
  a verify command, and fixing that command in the contract invalidated the
  stamp. An unchanged tree was reviewed again to re-earn it. Decision 0066
  already says a stamp binds `delta_id` alone and that a contract re-record
  never affects it, so this is the implementation not keeping an accepted
  promise.
- Reverting two files so the diff was smaller and cleaner killed the stamp
  again, for the same reason.
- Amending a decision after a spec read re-staled that read; cutting a task
  worktree from trunk re-staled the task grill. In both cases the artifact and
  the records it cited were untouched.

The second cost is the recorder's round floor. Every recorded pass requires a
fresh AskUserQuestion round, so a pass with a genuinely empty frontier cannot be
recorded without inventing a question. Of roughly fifteen questions put to the
owner across that task, several existed only to satisfy the recorder.

The third is the grill budget. A read that died on an upstream tool failure
still consumed an allowance, and recording an escalation printed that grilling
continues while the next read was still refused, including a print-only dry run.
An owner instruction to retry was therefore unexecutable.

Two things this spec does NOT carry, both corrected by the spec cold read.
`forge task close` is a valid command and the intended closeout path; the client
repo was running an older vendored copy, which is a vendoring lag, not a defect
here. And scope widening already has a sanctioned non-cascading path in
`stage amend-scope`, which records measured paths without touching the contract.

## Behaviour

**A gate stales when its inputs change, not when the tree moves.** Each recorded
pass carries an input manifest: for every input it read, a stable identifier and
a content digest. That manifest covers the artifact itself, the handover records
cited, and the active decision set applicable to the gate, so a decision that was
read but never cited cannot change unnoticed. A later edit stales the pass only
if it changes something in that manifest.

**A review stamp binds the diff, as decision 0066 already requires.** A contract
edit that leaves the reviewed delta unchanged never invalidates a stamp. This is
restoring stated behaviour, not changing it.

**A recorded pass needs a real question only when there is one.** The round floor
is per gate, not per recording attempt. Re-recording the same gate after
resolving findings does not demand a new round, and a pass whose frontier is
closed records with the rounds the gate already carries.

**The grill budget counts reads, not failures.** A cold read consumes an
allowance only when it completes and returns a verdict. A launcher or tool
failure consumes nothing. Recording an escalation grants exactly one further read
for that gate and task, and that grant is spent when the next read completes,
clearing both the cap and the repeat-read guard, so the printed promise matches
the behaviour.

## Acceptance criteria

1. Every recorded gate pass carries an input manifest of identifier plus content
   digest, covering the artifact, the cited handover records, and the active
   decisions applicable to that gate. Asserted for all six gates in the gate
   table.
2. Editing a product file absent from a pass's manifest leaves that pass valid,
   asserted for all six gates.
3. Editing anything present in the manifest stales the pass, asserted for all
   six gates, including a decision that was read but not cited.
4. A stage review stamp survives a contract re-record that leaves the delta
   unchanged, asserted end to end through a stamp, a contract edit and a stage
   close, per decision 0066.
5. A gate pass records with no new question round when the gate already carries
   one and the frontier is closed; the floor of one real round per gate still
   holds, asserted both ways.
6. A cold read that ends in a launcher or tool failure leaves the budget
   unchanged, asserted with a simulated failure.
7. Recording an escalation permits exactly one further read for that gate and
   task, clearing both the cap and the repeat-read guard, and that grant is spent
   once the read completes. Asserted from an exhausted budget.
8. A named set of generated `./forge` invocations printed in next-step text
   parses against the real command grammar, arguments included. External programs
   and placeholders are out of scope.
9. Existing suites pass. The 93 failures already red on main are unchanged in
   count and identity, so this change is neither credited nor blamed for them.
