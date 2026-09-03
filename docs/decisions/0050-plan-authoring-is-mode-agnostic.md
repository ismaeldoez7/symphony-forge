---
status: accepted
confirmed_by: "Nandu"
date: 2026-09-03
stories: [upgrade-preserves-doc-contracts]
supersedes: 0048-plan-mode-and-grill-provenance
---

# Plan authoring is mode-agnostic

## Context

Decision 0048 made plan-mode provenance enforced rather than advisory: `plan
save`, `plan approve`, `task plan save` and `task approve` all refused without a
plan-mode marker recorded by the PostToolUse hook. The intent was provenance —
evidence that a human-facing plan was authored deliberately rather than
synthesised in passing.

In practice it forces a MODE SWITCH. A coordinator working in auto mode is
pushed into plan mode for every plan and every per-task contract, then back out,
repeatedly through a story. Reported by the maintainer in-session
(2026-09-03): "while task planning i have my claude in auto but it is always
shifting to plan mode, claude shouldnt change modes".

The cost buys nothing for planning quality. Plan mode in Claude Code is a
PERMISSION mode, not a reasoning mode: it restricts tools to read-only and asks
for a plan. It does not change the model and does not change the thinking or
effort level — that is a separate dial, and `AGENTS.md` already sets planning to
`high` independently. The one real property plan mode contributes, a read-only
tool surface, is ALREADY provided by the harness's own session write lock, which
is armed at all times and denies product and canon writes regardless of mode.

So the marker enforces a mode whose only unique benefit the harness already has,
and pays for it in mode churn.

## Decision

Plans and per-task contracts may be authored in ANY mode. `plan save`, `plan
approve`, `task plan save` and `task approve` no longer require a plan-mode
marker. The PostToolUse hook may still record markers — they remain useful
provenance — but no gate consults them.

The gates that actually protect a plan are unchanged and are the ones that
matter: the plan must carry its required sections, its grill must be clean and
digest-bound to the exact body, the plan is visible on the BOARD before anyone
approves it, and the human approves it there exactly once. Provenance now comes
from the grill and the recorded human approval rather than from which editor
mode produced the text.

This supersedes 0048's plan-mode clause only. 0048's GRILL provenance — a
digest-bound grill recorded against the exact plan body — stands unchanged.

## Consequences

- The coordinator stops switching modes mid-session; auto mode carries a story
  from planning through implementation.
- Plan-mode markers become advisory records, not gates. `require_plan_mode_marker`
  loses its callers.
- Nothing weakens the approval path: an ungrilled plan still cannot be saved as
  awaiting-approval, and an unapproved plan still cannot start implementation.
- Tests that asserted a refusal-without-marker now assert the opposite, and the
  suite documents the reasoning so the requirement is not reintroduced by
  reflex.
