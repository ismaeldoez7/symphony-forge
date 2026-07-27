"""forge codex status — is the delegated run still moving?

A stalled Codex job used to be invisible until somebody thought to ask. The
companion already records everything needed to see it — status, phase, the
write flag, timestamps, the log path — in its own job registry; nothing read
it.

DELIBERATELY ADVISORY. This reads a third-party path this repo does not own,
so it always exits 0 and never blocks a ship: a diagnostic over data outside
the contract must not be able to fail a gate (decision 0018).
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

from factory_lib import repo_root

from .stages import load_stages

STATE_ROOT = Path.home() / ".claude" / "plugins" / "data" / "codex-openai-codex" / "state"
STALL_MINUTES = 20


def _parse_time(value: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def load_jobs(base: Path, state_root: Path | None = None) -> list[dict]:
    """Jobs whose workspace IS this repo.

    Matched on `workspaceRoot` rather than the state directory's name, which
    is a hash this repo has no business reproducing. Parsed defensively: the
    registry belongs to the plugin and may change shape without notice."""
    root = state_root or STATE_ROOT
    if not root.is_dir():
        return []
    jobs = []
    for path in sorted(root.glob("*/jobs/*.json")):
        try:
            job = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(job, dict):
            continue
        if Path(str(job.get("workspaceRoot", ""))) != base:
            continue
        job["_path"] = path
        jobs.append(job)
    return sorted(jobs, key=lambda j: str(j.get("createdAt", "")))


def age_minutes(job: dict, now: datetime.datetime | None = None) -> float | None:
    started = _parse_time(job.get("startedAt") or job.get("createdAt") or "")
    if started is None:
        return None
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if started.tzinfo is None:
        started = started.replace(tzinfo=datetime.timezone.utc)
    return (now - started).total_seconds() / 60.0


def warnings_for(job: dict, *, stage_active: bool, stale_minutes: int,
                 now: datetime.datetime | None = None) -> list[str]:
    notes = []
    running = str(job.get("status", "")) in {"running", "starting", "queued"}
    age = age_minutes(job, now)
    if running and age is not None and age >= stale_minutes:
        notes.append(f"STALLED? running {int(age)}m with phase "
                     f"{str(job.get('phase') or 'unknown')!r}")
    if running and stage_active and job.get("write") is not True:
        # A read-only sandbox with approvalPolicy "never" can neither write nor
        # ask, so it narrates a plan and exits 0. That is the silent stall.
        notes.append("READ-ONLY while a stage is active — it cannot write and "
                     "cannot ask; re-run via `./forge delegate <task-id>`")
    return notes


def cmd_status(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    state_root = Path(args.state_root).expanduser() if args.state_root else STATE_ROOT
    if not state_root.is_dir():
        print(f"codex status: unknown — no plugin job registry at {state_root}. "
              "Nothing to report (this is a diagnostic, not a gate).")
        return
    jobs = load_jobs(base, state_root)
    if not jobs:
        print(f"codex status: no jobs recorded for {base}")
        return
    stage_active = any(s.get("status") == "active"
                       for s in load_stages(base).get("stages", []))
    flagged = 0
    for job in jobs:
        age = age_minutes(job)
        age_text = f"{int(age)}m" if age is not None else "?"
        print(f"[{str(job.get('status', '?')):<9}] {str(job.get('id', '?')):<22} "
              f"phase={str(job.get('phase') or '-'):<12} "
              f"write={'yes' if job.get('write') else 'no ':<3} age={age_text}")
        summary = str(job.get("summary") or job.get("title") or "").strip()
        if summary:
            print(f"            {summary[:100]}")
        if job.get("logFile"):
            print(f"            log: {job['logFile']}")
        for note in warnings_for(job, stage_active=stage_active,
                                 stale_minutes=args.stale_minutes):
            flagged += 1
            print(f"            !! {note}")
    if flagged:
        print(f"\n{flagged} warning(s). Advisory only — this reads the plugin's own "
              "registry and never fails a gate.")
