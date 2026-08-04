# Deferral Ledger

Deliberately-removed scope with explicit revisit triggers (`forge defer add`).
When a trigger fires, the item goes back on the roadmap and its row is
resolved: `./forge defer resolve <id> --notes "<what happened>"`.

| id | added | item | why deferred | trigger to revisit | status |
|----|-------|------|--------------|--------------------|--------|
| D-0001 | 2026-07-28 | Container-backed containment for untrusted delegation and proof commands | True cross-platform hostile-process containment requires a pinned container image/runtime; process-table sampling cannot provide that boundary on macOS and Linux. | Forge permits untrusted decomposition commands or third-party worker code to execute with write access | open |
| D-0002 | 2026-08-04 | Heading-shaped text inside a raw HTML block (<pre>, <div>) still counts as document structure in spec confirm and sign-off | Closing it means parsing Markdown properly, and factory/scripts is stdlib-only by design (factory_lib.py states it). Adding a Markdown dependency is a project-constraint change, not a task fix. The threat model is also weak: the gate serves the spec's own author, so bypassing it means deliberately faking structure to defeat a check that only helps you. Two autoreview cycles reached on this task; the governor says reclassify rather than patch a third time. | A spec or brief is found in a real project whose required sections exist only inside raw HTML, or the stdlib-only constraint is lifted for factory/scripts | open |
