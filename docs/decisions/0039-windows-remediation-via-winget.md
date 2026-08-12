---
status: proposed
confirmed_by: ""
date: 2026-08-12
stories: [FORGE-WIN-2]
---

# Windows Remediation Via Winget

## Context

The zero-setup spec obliges `forge doctor --fix` to install Git for Windows
and Python ≥ 3.10 on a bare Windows machine with no user-typed commands and
at most ONE consolidated UAC confirm (spec grill, 2026-08-11). Doctor's
existing installers are all user-scope and never elevate; the only
privilege-escalation precedent in the codebase is `_install_direnv_linux`'s
per-command sudo — exactly the per-package prompting the settlement forbids.
The direnv Windows installer downloads a single static binary via urllib;
Git and Python are full installers with dependencies, signatures, and update
cadence that pattern cannot carry safely.

## Decision

winget is the sole installer for Windows prerequisites. `--fix` attempts
user-scope installs first (`winget install --scope user --silent
--accept-package-agreements --accept-source-agreements`, no prompt at all);
only when the OS or policy refuses user scope does it fall back to ONE
elevated PowerShell invocation (`Start-Process -Verb RunAs`) whose argument
list carries every pending install — a single UAC confirm per doctor run,
never per package. winget absent (LTSC/Server/old images) is a named
required red row carrying the manual installer URLs. Installs run via
direct `subprocess.run` with an installer-scale timeout, not `run_quiet`
(hardcoded 15s, ~15 shared call sites).

## Consequences

- Rejected: bundled urllib installer downloads (attack and maintenance
  surface — the direnv single-binary precedent does not scale to full
  installers); per-package elevation (the linux sudo shape); elevating
  when user scope suffices; any winget policy-evasion on managed machines.
- The one-confirm invariant is machine-proven by argv-recording fakes
  (exactly one elevation-shaped invocation, both package ids); the real
  UAC path is proven once on the affected client's machine as functional
  evidence — CI runners are already admin and cannot exercise it.
- Convergence is same-run: after installs, doctor refreshes the process
  PATH with known install locations and re-probes, so the run that fixed
  the machine is the run that reports green.
