---
status: accepted
confirmed_by: "Ravi"
date: 2026-09-11
stories: [GATES-1]
supersedes: 0051-every-grill-gate-is-ledger-matched
---

# A question round belongs to its gate and story, and may be reused there

## Context

Decision 0051 made every grill gate ledger-matched: a recorded pass must cite a
real AskUserQuestion round, and no round is reused across grills. That stopped
passes being recorded against questions nobody asked, which was the right
problem to solve.

The rule is enforced by consuming rounds found in previous grill records, so a
round is spent the first time any pass claims it. In a per-task flow that turns
out to punish the ordinary case. A gate is re-recorded whenever its findings are
resolved, its contract is corrected, or an earlier gate moves, and each
re-recording demands a brand new question. When the frontier is genuinely closed
there is nothing left to ask, so the question gets invented purely to satisfy the
recorder.

On one client task that produced roughly fifteen owner questions, several of
which existed only because a pass could not otherwise be recorded. Asking a
person to choose between options that do not matter is worse than not asking:
it spends their attention and teaches them that the questions are noise.

The implementation also cannot express what 0051 intends. Ledger rows carry the
question, its options, the answer and a session id. They carry no gate and no
story, and a globally recorded gate receives no issue at all, so "reused across
grills" can only be approximated by consuming rows globally.

## Decision

A question round belongs to the gate and story it was asked for, and may be
reused when re-recording THAT gate for THAT story. It is never reused across a
different gate, a different story, or a different task.

Rounds therefore carry their provenance: the ledger records the gate and story
active when the question was asked, and the recorder matches on that provenance
before consuming a round. A round with no recorded provenance, which is every
round written before this decision, keeps 0051's behaviour and is consumed
globally.

The floor 0051 set is unchanged: every gate still requires at least one real
round, and a pass still cannot be recorded against a question nobody asked.

## Consequences

- Re-recording a gate after resolving its findings no longer manufactures a
  question, which is the only case this relaxes.
- The ledger gains gate and story fields, and the recorder gains a provenance
  match. Rounds written before this keep working unchanged.
- A global-gate recording can no longer consume a round asked during another
  story, which 0051 permitted by accident.
- 0051 is retired. Its intent, that no gate is satisfied by a question nobody
  asked, is carried forward intact.
