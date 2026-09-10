"""Native Codex coordinator selection and exact exec contracts."""
from __future__ import annotations

import json
import os
from pathlib import Path


RUNTIMES = ("claude", "codex")


def selected_coordinator(requested: str | None = None) -> str:
    """Select the coordinator without changing the legacy outside-runtime default."""
    explicit = requested if requested is not None else os.environ.get("FORGE_COORDINATOR")
    if explicit is not None:
        value = explicit.strip().lower()
        if value not in RUNTIMES:
            raise SystemExit(
                "FORGE_COORDINATOR must be 'claude' or 'codex', "
                f"got {explicit!r}"
            )
        return value
    if os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SHELL"):
        return "codex"
    if os.environ.get("CLAUDECODE"):
        return "claude"
    return "claude"


def coordinator_runtime() -> str:
    return selected_coordinator()


def native_argv(
        executable: str, base: Path, model: str, effort: str, write: bool,
        *, resume_session: str = "") -> list[str]:
    """Build the complete shell-free native invocation used as launch evidence."""
    argv = [
        executable,
        "exec",
        "--json",
        "--enable",
        "hooks",
        "-C",
        str(base),
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{effort}"',
        "--config",
        'approval_policy="never"',
        "--sandbox",
        "workspace-write" if write else "read-only",
    ]
    if resume_session:
        argv.extend(("resume", resume_session))
    argv.append("-")
    return argv


def native_argv_valid(entry: dict, base: Path) -> bool:
    executable = entry.get("executable_path")
    argv = entry.get("argv")
    if not isinstance(executable, str) or not executable:
        return False
    if not isinstance(argv, list) or not all(isinstance(v, str) for v in argv):
        return False
    return argv == native_argv(
        executable,
        base,
        str(entry.get("model") or ""),
        str(entry.get("effort") or ""),
        entry.get("write") is True,
        resume_session=str(entry.get("resume_session") or ""),
    )


def _native_events(path: Path, *, allow_truncated_tail: bool = False) -> list[dict]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"native Codex output is unavailable: {exc}") from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        boundary = max(raw.rfind(b"\n"), raw.rfind(b"\r"))
        if (not allow_truncated_tail or raw.endswith((b"\n", b"\r"))
                or exc.start <= boundary):
            raise ValueError("native Codex output is not UTF-8") from exc
        text = raw[:boundary + 1].decode("utf-8")
    lines = text.splitlines()
    events = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            if (allow_truncated_tail and number == len(lines)
                    and not text.endswith(("\n", "\r"))):
                break
            raise ValueError(f"native Codex output line {number} is not JSON") from exc
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            raise ValueError(f"native Codex output line {number} is not an event")
        events.append(event)
    return events


def parse_native_result(path: Path) -> str:
    """Return the persisted Codex session id only for a terminal success stream."""
    events = _native_events(path)
    session_id = native_session_identity(path)
    if not session_id:
        raise ValueError("native Codex output has no unique thread.started identity")
    if any(event.get("type") in {"error", "turn.failed"} for event in events):
        raise ValueError("native Codex output reports a failed run")
    if not events or events[-1].get("type") != "turn.completed":
        raise ValueError("native Codex output has no terminal turn.completed event")
    return session_id


def native_session_identity(path: Path) -> str:
    """Return only an unambiguous runtime identity, regardless of outcome."""
    try:
        starts = [event for event in _native_events(path, allow_truncated_tail=True)
                  if event.get("type") == "thread.started"]
    except ValueError:
        return ""
    if len(starts) != 1 or not isinstance(starts[0].get("thread_id"), str):
        return ""
    return starts[0]["thread_id"].strip()


def native_completed_message(path: Path) -> str:
    messages = [
        event.get("item", {}).get("text")
        for event in _native_events(path)
        if event.get("type") == "item.completed"
        and isinstance(event.get("item"), dict)
        and event["item"].get("type") == "agent_message"
        and isinstance(event["item"].get("text"), str)
    ]
    return messages[-1].strip() if messages else ""
