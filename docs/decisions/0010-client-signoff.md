---
status: accepted
confirmed_by: "vrknetha"
date: 2026-07-24
stories: []
extended_by: 0014-specs-before-signoff
---

# Client Signoff

## Context
The harness repo itself had no recorded sign-off, so its own gate chain
(intake → sign-off → plan save) blocked harness maintenance work. First
blocked task: FORGE-INIT-1, fixing `forge init`'s blanket non-empty-target
refusal (hit while bootstrapping the agentstats repo, 2026-07-24).

## Decision
The harness maintainer (repo owner) is the client for symphony-forge itself;
their approval of a task's plan constitutes sign-off for harness maintenance
runs.

## Consequences
Harness fixes flow through the same factory gates as client work — intake,
saved plan, verify, autoreview evidence — with the maintainer's plan
approval standing in for client sign-off. No gate is bypassed.

This record is also the ARTIFACT the sign-off gate reads, not only a policy
statement: decision 0009's successor made sign-off derived rather than
recorded, so `harness.yaml` pins this file and every gate resolves the answer
from it. It was briefly marked superseded by 0014, which retired the only
evidence that this project was ever signed off and left the harness repo
failing its own gate. 0014 EXTENDS the preconditions for recording sign-off
(confirmed specs, a derived roadmap); it does not retire this record, and says
so itself: "From 0010, retained unchanged: the harness maintainer is the
client for symphony-forge itself." Restored to accepted on maintainer
confirmation in chat, 2026-08-04.
