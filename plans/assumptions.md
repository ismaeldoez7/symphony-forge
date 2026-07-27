# Implementation Assumptions Ledger

One row per assumption made during implementation (`forge plan assume`).
The orchestrator reviews open rows and guides:
`./forge assumptions resolve <id> --status confirmed|fix-needed|promoted --notes "..."`.
`pr_ready.py` refuses while the task has rows at `open` or `fix-needed`.

| id | date | issue | assumption | status | guidance |
|----|------|-------|------------|--------|----------|
| A-0001 | 2026-07-27 | FORGE-DELEG-1 | stage done exempts only .factory/ and plans/, NOT pr_ready's EVIDENCE_PATHS as the plan said — that list exempts all of factory/ and docs/, which in this repo is the product, so reusing it would make the write_scope check vacuous exactly where it is dogfooded | open |  |
| A-0002 | 2026-07-27 | FORGE-DELEG-1 | required_tests entries are test NAMES by existing convention (see any recorded decomposition), not file paths as the plan assumed — resolution is a fixed-string search across tracked and untracked files, excluding .factory/ and plans/ so the declaration cannot match itself | open |  |
| A-0003 | 2026-07-27 | FORGE-DELEG-1 | stage start also records dirty_at_start and stage done subtracts it: a file already dirty when the stage began is not that stage's work, and blaming it for one would refuse honest runs over unrelated edits | open |  |
