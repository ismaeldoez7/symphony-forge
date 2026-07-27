"""The story timeline (.factory/events.jsonl).

`run.json` holds one mutable `updated_at` that every phase overwrites, so a
story that passed through planning, building, testing and review retains a
single timestamp and no trace of the transitions. This ledger appends one
line per transition instead: what happened, when, and WHO — the scripts that
change state call it themselves, so a timeline cannot be skipped by an agent
that forgets to write it.

Story-scoped lines archive to .factory/history/<issue>/events.jsonl at ship;
discovery lines (spec save, roadmap derive) carry no story and stay.
"""
from __future__ import annotations

import json
from pathlib import Path

from factory_lib import now_iso, validate_payload


def events_path(base: Path) -> Path:
    return base / ".factory" / "events.jsonl"


def load_events(base: Path, story: str | None = None) -> list[dict]:
    path = events_path(base)
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            # A JSONL merge tear across worktrees costs one line, never the
            # whole timeline: the union driver can interleave a partial write.
            continue
    return [e for e in events if story is None or e.get("story") == story]


def append_event(base: Path, event: str, actor: str, story: str = "",
                 detail: str = "") -> None:
    """Append one transition. Never raises on a write failure: the ledger is a
    record, and losing a line must not fail the gate that was doing real work.

    `actor` lands as `generated_by` — the harness's one attribution vocabulary,
    so the schema's pinned allowlist applies to events too."""
    payload = {"event": event, "generated_by": actor, "at": now_iso()}
    if story:
        payload["story"] = story
    if detail:
        payload["detail"] = detail
    try:
        validate_payload(base, "event", payload)
        path = events_path(base)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as fh:
            fh.write(json.dumps(payload) + "\n")
    except Exception:
        return
