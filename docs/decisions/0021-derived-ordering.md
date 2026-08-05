---
status: accepted
confirmed_by: "vrknetha"
date: 2026-08-04
stories: [PH-2]
---

# Derived Ordering

## Context

Work in this harness has an order, and that order is currently written down in
more than one place. Stories carry `depends_on`. Decompositions carry
`build_waves`. Plans describe a sequence in prose. Each is authored by hand, and
none is derived from the others.

Two hand-written orderings of the same work cannot be kept true. When a story
moves, `depends_on` gets corrected because `ready_pending()` and `check_dag()`
read it — and the wave list silently keeps its old shape, because nothing reads
it except a renderer nobody runs. The harness then shows a confident sequence
that no longer matches the dependencies it claims to summarise.

The derivations already exist and are already correct: `ready_pending()` for the
frontier, `leverage()` for transitive unblocks, `epic_gating()` for epic-to-epic
order, `board._summary()` for progress. None of them needs an authored ordering.

## Decision

`depends_on` on a story is the only ordering anyone writes. Every other
statement of sequence — epic order, the ready frontier, leverage, waves — is
derived from it at read time. No artifact may carry a second hand-written
ordering of the same work.

## Consequences

- `build_waves` stops being authored: removed from
  `factory/prompts/decomposer.md` and the griller's checklist. The schema field
  stays optional so the shipped `.factory/history/` artifacts that carry it keep
  parsing, and `render_linear_task_graph.py` — its only reader — is deleted in
  the same task that stops writing it, or it becomes an orphan by construction.
  PH-3 does that work and consumes this decision.
- A UI may show any ordering it likes, provided it derives it. PH-4's epic map
  and delivery order are views over `depends_on`, never a stored sequence.
- Adding an ordering field to any schema is a change to this decision, not a
  schema tweak.
- Tasks inside a story stay sequential by array index. That is one ordering,
  authored once, in the place the stage engine already reads — not a second copy.
