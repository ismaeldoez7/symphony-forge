"""forge grill run — release the read-only cold reader through the ledger.

Grills were the one Codex release the harness could not see. A delegation
records a pid and a review now does too, so a launcher killed uncatchably is
still detectable afterwards; a grill went out through the plugin directly, so
nothing on the forge side knew it had ever started. That is backwards: the
grill is the release the coordinator is told to WATCH every single round.

Releasing it through `launch_companion` — the same launcher a delegation uses —
gives it the same treatment for free: the pid and process create-time are
ledgered before the wait, the process tree is reaped on exit, the argv is
pinned, and `forge codex status` reports it dead if its launcher was killed.

It stays READ-ONLY. `write=False` means no delegation lock is taken and the
row can never satisfy `stage done`, which matches on a write launch bound to a
task contract. The cold read returns findings; recording the gate remains the
coordinator's job through the ledger-matched recorder, exactly as before.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from factory_lib import (
    evidence_path, load_json, protected_decomposition_state_path, repo_root,
    run_state_path,
)

from .common import fail

# Which artifact each gate interrogates. The grill reads it COLD, so the brief
# must carry the text itself — the reader has no memory of the session that
# wrote it.
GATE_ARTIFACTS = {
    "spec": "the capability spec under interrogation",
    "requirements": "the requirements round under interrogation",
    "plan": "the approved plan under interrogation",
    "task": "the per-task implementation plan under interrogation",
    "signoff": "the client sign-off handover under interrogation",
    "epics": "the derived epics under interrogation",
}


def _artifact_text(base: Path, gate: str, task_id: str) -> tuple[str, str]:
    """Return (label, text) for the artifact this gate interrogates."""
    state = load_json(run_state_path(base), default={})
    key = state.get("issue_key", "")

    if gate == "task":
        if not task_id:
            fail("`--gate task` interrogates ONE task's plan: pass --task <id>")
        path = evidence_path(base, key, f"task-plans/{task_id}.md")
        if not path.is_file():
            fail(f"no saved task plan for {task_id} — save it with "
                 f"`./forge task plan save {task_id} --from <path>` first")
        return f"task plan {task_id}", path.read_text(encoding="utf-8")

    if gate == "plan":
        plan_file = load_json(protected_decomposition_state_path(base),
                              default={}).get("plan_file") or state.get("plan_file")
        if not plan_file:
            fail("no approved plan is recorded — `./forge plan save` first")
        path = base / plan_file
        if not path.is_file():
            fail(f"the recorded plan {plan_file!r} does not exist")
        return f"plan {plan_file}", path.read_text(encoding="utf-8")

    fail(f"`--gate {gate}` has no artifact resolver yet; grill it through the "
         "documented path and record it with record_grill_from_json.py")
    raise AssertionError("unreachable")


def _compose_brief(base: Path, gate: str, label: str, artifact: str) -> str:
    contract = base / "factory" / "prompts" / "griller.md"
    contract_text = (contract.read_text(encoding="utf-8")
                     if contract.is_file() else "")
    return "\n".join([
        f"# Cold-read grill — gate: {gate} — {label}",
        "",
        "You did NOT write what follows. Read it cold, as an adversary trying "
        "to break the handover, never as its author defending it. You are "
        "READ-ONLY: return findings, change nothing.",
        "",
        "Load and run the `grill-me` skill to structure the interrogation; the "
        "contract below is the floor, the skill is the technique.",
        "",
        "## Harness grill contract",
        "",
        contract_text,
        "",
        f"## The artifact under interrogation ({label})",
        "",
        artifact,
        "",
        "## What to return",
        "",
        "Findings only: contradictions, gaps, unstated assumptions, and "
        "anything a reader would have to guess. Say what would break and why. "
        "Do not record a gate — the coordinating session records it.",
        "",
    ])


def cmd_grill_run(args: argparse.Namespace) -> None:
    from .delegate import launch_companion, mode_run_config

    base = Path(args.repo).resolve() if args.repo else repo_root()
    gate = args.gate
    task_id = (args.task or "").strip()
    label, artifact = _artifact_text(base, gate, task_id)
    text = _compose_brief(base, gate, label, artifact)

    # Keyed apart from real task ids so a grill row can never be mistaken for
    # a task's delegation, and so concurrent grills of different gates do not
    # collide in the ledger.
    ledger_id = f"grill-{gate}" + (f"-{task_id}" if task_id else "")
    path = base / ".factory" / f"grill-brief-{gate}" \
        f"{'-' + task_id if task_id else ''}.md"
    model, effort, _bound = mode_run_config(base, "grill")

    launch_companion(
        base,
        task_id=ledger_id,
        text=text,
        path=path,
        task_sha256_value="",
        model=model,
        effort=effort,
        write=False,          # a cold read never writes, and never authorises
        story=load_json(run_state_path(base), default={}).get("issue_key", ""),
        print_only=bool(args.print_only),
    )
    if args.print_only:
        return
    print(f"NEXT: carry these findings into your own rounds, then record with "
          f"`python3 factory/scripts/record_grill_from_json.py --gate {gate}"
          f"{' --task ' + task_id if task_id else ''} --input <json>`")
