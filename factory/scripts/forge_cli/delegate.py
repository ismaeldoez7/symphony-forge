"""forge delegate — compose the brief and the invocation for one task.

Delegation used to be a judgement call made fresh each time: whether the run
could write was decided per request (and three layers disagreed on the
default), and nothing composed context for the executor — `factory/prompts/
implementer.md` was referenced by five docs and read by zero scripts. So the
worker guessed, and a read-only sandbox with `approvalPolicy: never` could
neither write nor ask.

This makes both facts artifacts. The brief is built from what the repo already
knows (the task contract, the implementer prompt, the active decisions, the
lessons matching these paths, the modules already in scope) and recorded with
its digest; write permission is derived from stage state. The pre-tool hook
reads the record, so an unbriefed write run is denied rather than discouraged.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from factory_lib import (
    decomposition_state_path, load_json, now_iso, repo_root, run_state_path,
    sha256_of, validate_payload,
)

from .common import fail
from .decisions import decision_records
from .events import append_event
from .lessons import relevant_lessons
from .stages import load_stages

SAFE_TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
# A brief is read by a model, so an inlined rule set that runs to thousands of
# lines crowds out the task. Enough to carry the rules, not the whole course.
SKILL_INLINE_CHARS = 12000
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_EFFORT = "medium"


def briefs_dir(base: Path) -> Path:
    return base / ".factory" / "briefs"


def delegations_path(base: Path) -> Path:
    return base / ".factory" / "delegations.jsonl"


def brief_path(base: Path, task_id: str) -> Path:
    # The id is matched against the recorded decomposition before it reaches
    # here, and re-validated: a task id must never be able to name a path.
    if not SAFE_TASK_ID.fullmatch(task_id):
        fail(f"task id {task_id!r} is not a plain identifier")
    return briefs_dir(base) / f"{task_id}.md"


def load_delegations(base: Path) -> list[dict]:
    path = delegations_path(base)
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            # Union-merged across worktrees: one torn line costs one record.
            continue
    return entries


def current_delegation(base: Path, task_id: str) -> dict | None:
    """The most recent delegation for this task whose brief still matches the
    file on disk. An edited brief is not the brief that was recorded."""
    path = brief_path(base, task_id)
    if not path.is_file():
        return None
    digest = sha256_of(path)
    for entry in reversed(load_delegations(base)):
        if entry.get("task") == task_id:
            return entry if entry.get("brief_sha256") == digest else None
    return None


def pinned_run_config(base: Path) -> tuple[str, str]:
    """The model and effort harness.yaml pins for implementation.

    Read rather than duplicated — and read here because the repo's own
    .codex/config.toml is shadowed by ~/.codex, so the pin never reaches the
    CLI unless the invocation carries it."""
    text = (base / "harness.yaml").read_text() if (base / "harness.yaml").is_file() else ""
    block = re.search(r"^  implementation:\n((?:    .*\n|\n)*)", text, re.MULTILINE)
    body = block.group(1) if block else ""
    model = re.search(r'^    model:\s*"?([\w.-]+)"?', body, re.MULTILINE)
    effort = re.search(r'^    reasoning:\s*"?(\w+)', body, re.MULTILINE)
    return (model.group(1) if model else DEFAULT_MODEL,
            effort.group(1) if effort else DEFAULT_EFFORT)


def required_skills(base: Path) -> list[str]:
    text = (base / "harness.yaml").read_text() if (base / "harness.yaml").is_file() else ""
    block = re.search(r"^      user_facing:\n((?:        - .*\n)+)", text, re.MULTILINE)
    if not block:
        return []
    return re.findall(r'^        - "?([\w-]+)"?', block.group(1), re.MULTILINE)


def existing_modules(base: Path, scope: list[str]) -> list[str]:
    """What is already in the task's write_scope.

    "Use the components that exist" is an instruction the executor cannot act
    on without knowing what exists — and it is told not to inspect the repo.
    So the listing travels with the brief as data."""
    found: list[str] = []
    for entry in scope:
        target = base / entry.strip().rstrip("/")
        if target.is_file():
            found.append(entry.strip())
        elif target.is_dir():
            found.extend(
                sorted(p.relative_to(base).as_posix()
                       for p in target.rglob("*")
                       if p.is_file() and ".git" not in p.parts)[:60]
            )
    return found


def _skill_text(skill: str) -> str:
    for candidate in (Path.home() / ".claude" / "skills" / skill / "SKILL.md",
                      Path.home() / ".codex" / "skills" / skill / "SKILL.md"):
        if candidate.is_file():
            return candidate.read_text()[:SKILL_INLINE_CHARS]
    return ""


def _section(title: str, body: str) -> str:
    return f"\n## {title}\n\n{body.rstrip()}\n" if body.strip() else ""


def compose_brief(base: Path, task: dict, *, write: bool, user_facing: bool,
                  story: str) -> str:
    scope = task.get("write_scope") or []
    lines = [
        f"# Brief — {task['id']}: {task.get('title', '')}",
        "",
        f"Story: {story or '(none)'} | write access: "
        f"{'YES — you may edit files in the write scope' if write else 'NO — read only'}",
        "",
        "This brief is the whole context you are given. It was composed from the "
        "recorded decomposition, the implementer contract, the active decisions "
        "and the lessons ledger. Do not go looking for the rules elsewhere; if "
        "something needed is missing, raise a signal instead of guessing "
        "(`./forge signal raise`).",
    ]
    body = "\n".join(lines) + "\n"
    body += _section("Objective", task.get("objective", ""))
    body += _section("Acceptance criteria", "\n".join(
        f"- {c}" for c in task.get("acceptance_criteria") or []))
    body += _section("Write scope — nothing outside this", "\n".join(
        f"- {s}" for s in scope) + (
        "\n\n`forge stage done` refuses a change outside this list."))
    modules = existing_modules(base, scope)
    body += _section("What already exists in that scope (use it, do not re-create it)",
                     "\n".join(f"- {m}" for m in modules) or "(nothing yet)")
    body += _section("Tests you must write", "\n".join(
        f"- {t}" for t in task.get("required_tests") or [])
        + ("\n\nThe implementer writes and records the tests; a declared test that "
           "exists nowhere refuses the stage." if task.get("required_tests") else ""))
    body += _section("Verify commands (they will be run when the stage closes)",
                     "\n".join(f"- `{c}`" for c in task.get("verify_commands") or []))
    body += _section("Reviewer focus", task.get("reviewer_focus", ""))
    decisions = [r for r in decision_records(base) if r["status"] == "accepted"]
    body += _section("Active decisions — binding", "\n".join(
        f"- {r['id']}: {r['title']}" for r in decisions))
    lessons = relevant_lessons(base, scope)
    body += _section("Lessons recorded against these paths", "\n".join(
        f"- {le.get('lesson', '')}" for le in lessons))
    prompt = base / "factory" / "prompts" / "implementer.md"
    if prompt.is_file():
        body += _section("Implementer contract", prompt.read_text())
    if user_facing:
        for skill in required_skills(base):
            text = _skill_text(skill)
            body += _section(
                f"Design rules — {skill} (inlined; your runtime cannot load it)",
                text or f"NOT INSTALLED on this machine. `./forge doctor --fix` "
                        f"installs {skill}. Until then this brief cannot carry the "
                        f"rules the harness will require you to attest.")
    return body


def cmd_delegate(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    decomposition = load_json(decomposition_state_path(base), default={})
    tasks = decomposition.get("tasks") or []
    if not tasks:
        fail("no recorded decomposition — a delegation is scoped to a leaf task "
             "(record_decomposition_from_json.py)")
    task = next((t for t in tasks if t.get("id") == args.id), None)
    if task is None:
        fail(f"{args.id!r} is not a task in the recorded decomposition "
             f"({', '.join(str(t.get('id')) for t in tasks)})")
    stage = next((s for s in load_stages(base).get("stages", [])
                  if s.get("id") == args.id), {})
    scope = task.get("write_scope") or []
    # Derived, not typed: an active stage with somewhere to write is a write
    # run. --read-only is the explicit exception, for exploration.
    write = bool(stage.get("status") == "active" and scope) and not args.read_only
    state = load_json(run_state_path(base), default={})
    story = str(state.get("story") or state.get("issue_key") or "")
    text = compose_brief(base, task, write=write,
                         user_facing=bool(decomposition.get("user_facing")),
                         story=story)
    path = brief_path(base, args.id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    model, effort = pinned_run_config(base)
    record = {
        "generated_by": "orchestrator",
        "at": now_iso(),
        "task": args.id,
        "brief_sha256": sha256_of(path),
        "write": write,
        "model": model,
        "effort": effort,
    }
    if story:
        record["story"] = story
    if args.background:
        record["background"] = True
    validate_payload(base, "delegation", record)
    delegations_path(base).parent.mkdir(parents=True, exist_ok=True)
    with delegations_path(base).open("a") as fh:
        fh.write(json.dumps(record) + "\n")
    append_event(base, "delegated", actor="orchestrator", story=story,
                 detail=f"{args.id} ({'write' if write else 'read-only'})")
    rel = path.relative_to(base).as_posix()
    invocation = (
        f"/codex:rescue{' --background' if args.background else ''}"
        f"{' --write' if write else ''} --model {model} --effort {effort} "
        f"--prompt-file {rel} \"{task['id']}: {task.get('title', '')}\""
    )
    print(f"Brief written to {rel} ({len(text.splitlines())} lines)")
    print(f"Write access: {'YES (stage is active with a write scope)' if write else 'NO'}")
    print("\nRun exactly this:\n")
    print(f"  {invocation}\n")
    print("Then WATCH the event channel: Monitor .factory/signals.jsonl alongside "
          "the job (`./forge codex status` shows whether it is still moving).")
    if not write and stage.get("status") != "active":
        print(f"Note: {args.id} is not an active stage, so this is a read-only run. "
              f"`./forge stage start {args.id}` first if it should be building.")
