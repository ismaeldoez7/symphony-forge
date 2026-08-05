---
status: proposed
confirmed_by: ""
date: 2026-08-04
stories: [PH-1]
---

# Markdown Structure Subset

## Context

The capture gates ask one question of a brief or a spec: does this document
have this section, with content. Answering it means deciding which lines are
headings, and that is Markdown parsing.

`factory/scripts` is stdlib-only by design, enforced by `check_dual_runtime.py`'s
allowlist, so a CommonMark library is not available to the gate. Six rounds of
review on PH-1 each named a real construct where heading-shaped text is not a
heading — fenced examples, HTML comments, top-level fences indented up to three
spaces, fences opened inside a list item, verbatim raw blocks (`<pre>`,
`<script>`, `<style>`, `<textarea>`), and type-6 container blocks. Each round
was correct. The tail continues past them: setext headings, link reference
definitions, block quotes.

Two review rounds also reached opposite conclusions about the same construct.
One filed unterminated-construct-masks-through-EOF as a defect that refuses
complete specs; a later one filed the opposite as a defect that accepts
incomplete ones. Both readings are defensible, which is the signal that this is
a contract question rather than a bug.

## Decision

The capture gates determine document structure over a documented subset of
CommonMark, implemented as a single line-state scanner in
`factory_lib.example_ranges`. Ambiguity resolves toward masking LESS: an
unterminated fence, comment or raw block masks nothing, deviating from
CommonMark deliberately.

The asymmetry is the whole rule. Masking too little sends an author to the
digest-bound grill that `spec confirm` and sign-off require anyway. Masking too
much refuses a document whose sections are plainly written, which is the
failure the gate exists to remove.

## Consequences

- The gate is a structural check, not an authorization boundary. Decision 0014
  already puts authorization at the grill; this states where the line falls.
- Constructs outside the subset are accepted, not refused. That is the safe
  direction by the rule above, and the grill remains the depth.
- Adding a Markdown dependency to `factory/scripts` would supersede this and is
  a harness change — `harness.yaml` plus the stdlib-only constraint — never a
  local fix inside a story.
- Review findings against constructs outside the subset are contract questions
  for this record, not defects in the scanner. Without this, each one restarts
  the same patch cycle that decision 0005 exists to stop.
