---
status: accepted
confirmed_by: "vrknetha"
date: 2026-07-24
stories: []
supersedes: 0010-client-signoff
---

# Confirmed specs and derived roadmap gate client sign-off

## Context

Sign-off previously required only an accepted client-signoff decision
record; nothing guaranteed the information needed for the factory loop
existed yet. Confirmed in chat (workflow-enforcement design, 2026-07-24):
devs prototype freely, specs are captured per capability as they emerge,
and epics/user stories must be DERIVED from those specs — never
hand-authored — so that after sign-off the loop can plan and ship one
story at a time without re-eliciting requirements.

## Decision

Recording client sign-off additionally requires: at least one spec in
docs/specs/ with none left in draft (confirming a spec requires a fresh,
passing grill), a derived plans/roadmap.json with at least one story, and
every confirmed spec referenced by at least one story. From 0010, retained
unchanged: the harness maintainer is the client for symphony-forge itself,
and their plan approval stands in for client approval on harness
maintenance runs.

## Consequences

- Sign-off cannot be recorded on vibes: the spec set and the derived
  backlog exist first, and each spec survived a grill interrogation.
- Already-recorded sign-offs (including this repo's) remain valid; the
  gate applies when sign-off is recorded or re-recorded.
- Devs review the derived roadmap rather than authoring epics/stories.
- Prototype-phase spec capture stays ceremony-free (docs/ is allowlisted);
  only CONFIRMING a spec carries the grill cost.
