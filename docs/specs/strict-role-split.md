---
slug: strict-role-split
title: The role split is a gate: Claude orchestrates, only Codex writes product
status: confirmed
saved: 2026-08-10T19:01:03+00:00
---

# The role split is a gate: Claude orchestrates, only Codex writes product

> Captured 2026-08-11 from operator feedback after a day in which the
> orchestrating session direct-edited product five times (each caught by
> review or gates, none by prevention) and ran discovery through Claude
> subagents. "Use Codex strictly and Claude to just orchestrate."

## Why

The role split (Claude coordinates; Codex executes) is instruction-level:
the planning lock blocks product writes without an approved plan, but WITH
one, the orchestrating session may edit product freely — so judgment creep
is one plausible reason away. Decision 0018 binds stages to a write launch,
yet orchestrator edits can ride worker commits undetected. Discovery
exploration drifted to Claude subagents though the adapter says Codex
read-only. Every other gap named this week became a gate; this one still
runs on discipline.

## Behaviour

All four boundaries below were grilled and human-settled 2026-08-11.

### Write lockout — the hook, always on

- In factory repos the orchestrating session's writes (Edit/Write/Notebook,
  and Bash write-shapes) to **product and canon paths** — code, tests,
  `.github/workflows/`, `constitution/`, `factory/` machinery including
  prompts and skills, `AGENTS.md`, vendored adapters — are DENIED even
  under an approved plan and active stage. The only sanctioned path for
  those files is `forge delegate` (Codex).
- Claude keeps its orchestration surfaces: `docs/specs/`, `docs/decisions/`,
  `docs/product/`, `docs/memory/`, `docs/context/`, `plans/`, `.factory/`
  via recorders, the scratchpad, and git operations on worker-produced
  diffs (stage commits, merges).
- Consequence, deliberate: review findings are re-delegated as follow-up
  briefs on the same stage — mandatory, and mechanically so, since the
  session cannot patch product. No trivial-fix carve-out (grilled: the
  carve-out is the loophole).

### Exploration routing

- Discovery exploration runs as Codex rescue read-only (`gpt-5.6-terra`)
  — no Claude Explore subagents, no orchestrator source-grepping for
  discovery. Claude reads code only inside gate work: reviewing a
  delegated diff, verify, resolving a raised signal (decision 0011's
  direct review stands — a read-ban would break it; instruction-level by
  design, stated honestly).

### Degraded-mode valve — ledgered, never silent

- When the companion path fails (outage, unrecoverable balk-loop), direct
  implementation is allowed ONLY inside an explicitly opened degraded-mode
  window: ledgered like a quickfix with the failure named, closed with the
  work recorded, declared by the PR. The write-lockout hook honors an open
  window; everything else refuses. No window, no exception.

## Acceptance criteria

- With an approved plan and active stage, a session Edit to a product/canon
  path is denied with a message naming `forge delegate` and the
  degraded-mode window; the same edit inside an open degraded window is
  allowed and the window rides the PR (Gate A declares it).
- Orchestration surfaces stay writable exactly as today; recorders and
  stage/git operations are unaffected.
- The adapter and AGENTS.md state the routing (discovery → rescue
  read-only; gate reads only), within the 110-line cap.
- `docs/degraded-mode.md` documents the window as the single exception.
- A decision record captures the boundary set and its grilled rationale.
- Gate tests pin: deny-under-approved-plan, allow-in-window,
  orchestration-surface exemptions, and the window's ledger record.

## Boundaries

- Decision 0011 unchanged: review stays Claude's, direct and adversarial.
- Reads are not machine-fenced (would break review/verify); the fence is
  writes, where enforcement is clean.
- Client repos inherit the same hook behavior (vendored machinery).

## Decomposition (epic → stories)

1. **FORGE-ROLE-1 — write lockout + degraded window + routing docs** — the
   hook change, the window primitive, adapter/AGENTS.md/degraded-mode.md
   updates, the decision record, gate tests. (Single bounded story; its own
   implementation is delegated, dogfooding the rule it lands.)
