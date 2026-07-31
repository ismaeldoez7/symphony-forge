# Deferral Ledger

Deliberately-removed scope with explicit revisit triggers (`forge defer add`).
When a trigger fires, the item goes back on the roadmap and its row is
resolved: `./forge defer resolve <id> --notes "<what happened>"`.

| id | added | item | why deferred | trigger to revisit | status |
|----|-------|------|--------------|--------------------|--------|
| D-0001 | 2026-07-28 | Container-backed containment for untrusted delegation and proof commands | True cross-platform hostile-process containment requires a pinned container image/runtime; process-table sampling cannot provide that boundary on macOS and Linux. | Forge permits untrusted decomposition commands or third-party worker code to execute with write access | open |
