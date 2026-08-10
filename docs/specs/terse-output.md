---
slug: terse-output
title: Terse by default: output earns its lines
status: confirmed
saved: 2026-08-10T13:09:30+00:00
---

# Terse by default: output earns its lines

> Captured 2026-08-10 from operator feedback: during execution nobody reads
> the commentary — forge commands lecture on every success, and agents narrate
> between actions. Reading load must drop, strictly.

## Why

Every forge command teaches on success (`stage done` recaps the whole loop,
`plan save` lectures the approval flow, `decision new` reminds about trailers)
and agents produce running commentary mid-execution. The guidance is correct
and completely unread — it repeats on every invocation, drowns the one line
that matters (what happened, what changed), and trains operators to skip
output entirely, which is how real warnings get missed.

## Behaviour

### forge CLI: one result line per success (grilled 2026-08-10)

- A successful command prints ONE line: what changed, with identifiers
  (`Stage FORGE-X-1.1 done — 2/3 complete`). No loop recaps, no next-step
  coaching, no reminders on the success path.
- ALL coaching lives in exactly two places: `forge next` (the "lost? run
  this" surface — keeps its numbered guidance) and error/refusal messages,
  which stay FULL fix-it verbosity (the minegate ledger message is the
  model). Terseness never trims a refusal.
- No verbosity flags, no env switches — one deterministic output shape
  (grilled: rejected `FORGE_VERBOSE` and `--quiet` as second surfaces).
- Deterministic budget: a gate test pins the success-path line count of the
  chatty commands so lecture-creep cannot return silently.

### Agent narration: vendored conduct rule

- Constitution (agent conduct) gains a narration budget: during execution,
  one line per state change — what was done, what changed, what's next only
  when it changed. Findings, contradictions, and gate results are ALWAYS
  reported; process narration ("now I will run the tests") is not.
- Full prose belongs at gates and deliverables: plan presentations, review
  summaries, PR bodies, and anything the human explicitly asks to be
  walked through. PR bodies and evidence records keep their current depth
  (grilled: they are the durable record — out of scope for cutting).
- Phase prompts (`factory/prompts/`) reference the rule rather than
  restating it.

## Acceptance criteria

- Success paths of the chatty commands (`stage start/done`, `plan save`,
  `plan approve`, `decision new/accept`, `quickfix start/done`, recorders)
  print one result line each; a budget gate test pins it.
- Error and refusal messages are unchanged, byte-for-byte where feasible.
- `forge next` retains full coaching and remains the single learning surface.
- The constitution carries the narration-budget rule; phase prompts point to
  it; the rule is vendored to clients like the rest of the canon.
- No new flags, env vars, or config for verbosity.

## Boundaries

- PR bodies, review records, plans, grills, and outcome prose are untouched.
- `forge next`, errors, and refusals keep full verbosity by design.
- Board UI text is out of scope.

## Decomposition (epic → stories)

1. **Terse CLI success paths + budget test** — trim the chatty commands,
   keep errors byte-identical, pin with the budget gate test.
2. **Narration budget in the constitution + prompt pointers** — the conduct
   rule, phase-prompt references, vendoring intact. (Independent of story 1.)
