# Deferral Ledger

Deliberately-removed scope with explicit revisit triggers (`forge defer add`).
When a trigger fires, the item goes back on the roadmap and its row is
resolved: `./forge defer resolve <id> --notes "<what happened>"`.

| id | added | item | why deferred | trigger to revisit | status |
|----|-------|------|--------------|--------------------|--------|
| D-0001 | 2026-07-28 | Container-backed containment for untrusted delegation and proof commands | True cross-platform hostile-process containment requires a pinned container image/runtime; process-table sampling cannot provide that boundary on macOS and Linux. | Forge permits untrusted decomposition commands or third-party worker code to execute with write access | open |
| D-0002 | 2026-08-04 | Abort or preserve-under-conflict when a client-added skill name collides with a skill the harness has since started shipping | Autoreview P1 on FORGE-UPG-1.1. Verified pre-existing and symmetric: the non-legacy preserve branch (upgrade.py:160) applies the identical rule, so a colliding client skill is already replaced on every current repo today. Changing it is a harness-wide decision about skill ownership and mixed-ownership semantics, not part of retiring the .agents/ tree, and doing it inside a migration story would change upgrade behavior for every repo under cover of a rename. | A real client repo loses a skill to a name collision, or the harness starts shipping a skill whose name is already common in client repos | open |
| D-0003 | 2026-08-04 | Audit every harness command that writes into a client repo (init, adopt, upgrade) against the path-boundary invariant, with tests per site | The recurring repository-escape class was confined to forge upgrade's new legacy-migration path and every site found is fixed and tested. init and adopt copy into a target the same way but were not touched by this story, so auditing them is a separate self-contained refactor rather than a fourth patch inside a migration story. | A fourth repository-escape finding lands in any client-writing command, or forge init/adopt gains new copy or delete logic | open |
