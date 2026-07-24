# Forge Board — structural redesign

## Context

The board (shipped in `5f01a1f`) has the right data and the wrong shape. Every
section renders expanded at once — pulse, callouts, next-steps, frontier chips,
the full epic›story›task tree, specs, decisions — in one scroll, and every one
of them is 13px monospace at near-identical weight. Monospace everywhere reads
as log output, so nothing has hierarchy and the eye has no entry point. The
verdict from the user: *"too much text heavy, throwing everything on the face,
there is no structure — we have a lot of data which we could utilise in a
smarter way."*

The fix is not styling. Progress must be read from **position**, not from
prose; reference material must leave the main surface; and the derived facts we
can compute for free (leverage, bottleneck, age, deltas) must replace text the
reader currently has to assemble in their head.

Six decisions, grilled and locked:

| Decision | Choice |
|---|---|
| Shape | Epic swimlanes × 6 lifecycle columns, card → drawer |
| Main surface | Pulse + banner + next line + lanes. Everything else behind **Library** |
| Motion | FLIP — a card physically travels to its new column when a story advances |
| Derived signals | Leverage ranking, bottleneck column, age in station, since-you-last-looked |
| Drawer | Two-width: narrow status → wide reading pane |
| Visual | Editorial ledger — warm paper/ink, Georgia serif, oxblood accent |

Refused on purpose: velocity, burndown, projected dates, story points. Nothing
in the harness records an estimate, so any forecast would be invented.

---

## 1. Visual system — `factory/board/index.html` (`:root`)

Replace the amber/slate instrument-panel tokens wholesale.

```
LIGHT                          DARK
--paper   #faf8f4              #16140f
--ink     #1a1714              #f0ece4
--accent  #8c2f39  oxblood     #d4707a
--shipped #2f6b4f  forest      #5fa37e
--build   #3b4c8a  indigo      #8296d8
--ready   #a8741a  ochre       #d9a441
--stone   #9a938a  blocked     #6b6459
--rule    hairline, ink @ 12%  cream @ 14%
```

Three typefaces, each with one job — all system-resident on macOS **and**
Windows, no webfonts (the server makes no external requests):

- `--serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif`
  — the project headline, lane names, and **all plan/spec prose**.
- `--sans: system-ui, -apple-system, "Segoe UI", sans-serif` — UI chrome,
  column labels (12px, `.08em` tracking, uppercase), counts.
- `--mono: ui-monospace, "SF Mono", Consolas, monospace` — story keys,
  commands, file paths. Nowhere else.

Surface treatment: hairline rules instead of card borders, generous margin,
ruled lanes. State must never be carried by colour alone — every station and
card also carries a glyph or label (WCAG, and the palette has two mid-tones).

## 2. Layout — one surface

```
┌ header (sticky) ─────────────────── ●live · ☰ library ┐
│  ██████████░░░░░░░  2/7 shipped                       │
│  ⚠ 1 contradiction blocks planning          [resolve] │  ← only when non-empty
│  NEXT › plan RAIL-1                          3 steps ▾│  ← expands to forge next
└───────────────────────────────────────────────────────┘
         SPEC   STORY   PLAN   BUILD   CHECKS   SHIP
  AUTH  ──────────────────────────────── 3 of 4 ───────
  RAILS ──────────────────────────────── 0 of 3 ───────
```

- **Frontier section is deleted.** A ready card is marked in place (★) — the
  chip list was duplicating the board.
- **`next` steps collapse** to the single verb; the numbered list is one click.
- **Specs, decisions, the plans ledger and quickfix history move to Library**, a
  slide-over from the header. Reference material, consulted rarely.
- Signals/quickfix stay in the header banner slot — they are urgent.

Cards carry: key (mono), truncated title, and at most one derived marker.
Nothing else. A lane with no cards in a column renders empty space, not a
placeholder.

## 3. Render architecture — the prerequisite

Today `render()` does `innerHTML = …` on every 4s poll, which destroys
transitions, focus and hover, and makes animation impossible.

Rewrite as **keyed diff-and-patch**: cards are created once, keyed by story
key, and each poll only moves/updates existing nodes. This is required for
motion, and it is also what stops the drawer from fighting the poll.

## 4. Motion budget

The page repaints ~900×/hour, so almost nothing may animate. Exactly one
automatic animation exists:

- **Story advances a station** (a few times a day — rare enough for delight):
  FLIP the card from its old column rect to its new one, ~400ms `ease-out`,
  then settle a 1.5s accent ring. The lane counter rolls up; the header bar
  segment transitions its width.
- Human-initiated only: drawer slide 220ms `ease-out`, drawer width change
  260ms, lane expand 180ms, `:active { transform: scale(.98) }` on cards.
- Everything else changes silently. `prefers-reduced-motion: reduce` disables
  FLIP and every transition — cards reposition instantly.

## 5. Derived signals — all client-side

`depends_on`, `completed_at` and the plan's `saved` already travel in
`/api/state`, so **`board.py` needs no new computation for these**:

- **Leverage** — transitive count of stories each ready story unblocks; ranks
  the ready column ("unblocks 3"). Answers *which* to plan next.
- **Bottleneck** — the station holding the most non-shipped cards gets a tint
  and a marker. Answers *why it feels stuck*.
- **Age in station** — from `plan.saved` / `completed_at`, shown only past a
  threshold so a healthy board stays quiet. Story granularity only; there are
  no per-stage timestamps, so it reads "building 3d", never "stage 2 stalled".
- **Since you last looked** — snapshot `/api/state` into `localStorage`, diff on
  next visit, mark changed cards with a dot until clicked.

## 6. Drawer — two widths

Narrow (420px): key + title, gate rail, state and age, **the blockers standing
between it and the next gate** (reuse `approval_readiness()` in
`board.py:237` — each with the command that clears it), then the task list.
No document text.

Wide (760px): "read plan" widens the same panel; `plan` · `spec` · `proof`
tabs, markdown typeset in serif at a comfortable measure, raw-JSON toggle and
the `vscode://` link retained. `‹ back` returns to narrow. Esc closes; the
board dims behind and stays live; focus returns to the originating card.

**Still read-only.** No accept button, no edit box — approval happens in chat
because the grill is bound by digest to the exact plan text.

## 7. Server — small addition only

`factory/scripts/forge_cli/board.py`: add `plans/quickfixes.jsonl` to the
payload for the Library (~10 lines). Everything else the redesign needs
already ships.

## Files touched

- `factory/board/index.html` — the redesign (rewrite)
- `factory/scripts/forge_cli/board.py` — quickfix ledger in the payload
- `factory/tests/test_gates.py:2448-2454` — retarget the anchors; `id="frontier"`,
  `id="tree"`, `id="next-section"`, `id="decisions"` and `"Ready to plan"` all
  disappear. Assert the new regions (`id="lanes"`, `id="drawer"`, `id="library"`)
  and that the page still polls `/api/state`.
- `factory/skills/forge.md` — the Library and drawer replace "scroll to the
  section"; deep-link form stays `#STORY-KEY`.

## Build

Delegate to Codex per the role split (`/codex:rescue --background`,
`gpt-5.6-sol` @ medium) with this file as the brief. `factory/` is on the
planning-lock allowlist, so no quickfix window is needed. I review the result
through the `emil-design-eng` lens and iterate on the craft directly — FLIP
timing and type scale need eyes on a screenshot, not a spec.

## Verification

1. `python3 -m pytest factory/tests/test_gates.py` — 120 pass after the anchor
   retarget.
2. `python3 factory/scripts/check_dual_runtime.py` — green.
3. Serve the seeded demo clone (`./forge board`), screenshot light **and** dark.
   Confirm: no horizontal scroll at 1280px and at 768px.
4. **FLIP check** — with the board open, flip a stage to `done` in the demo
   repo's `stages.json`; within one poll the card travels to its new column and
   the header bar segment grows. Then re-run with reduced-motion emulated: the
   card repositions instantly, nothing else moves.
5. **Keyboard/a11y** — Tab reaches every card, Enter opens the drawer, Esc
   closes it and focus returns to the card. Cards are `<button>`s.
6. **Offline/Windows** — grep `index.html` for `http://`/`https://` (only
   `vscode://` may appear) and for any `@font-face`; confirm every font is a
   system stack present on both platforms.
7. Confirm the board is still read-only: no `POST` handler, no form controls
   that mutate `.factory/`.
