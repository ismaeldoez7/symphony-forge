"""forge stage — per-task execution tracker (.factory/stages.json).

The recorded decomposition is immutable evidence; this file is the mutable
execution state derived from it (one stage per leaf task, list order =
execution order). The loop per stage (WORKFLOW.md "Stage Loop", decision
0007): implement via /codex:rescue → inspect the diff → validate assumption
rows → smallest checks → LOCAL autoreview until clean → commit →
`forge stage done`. `pr_ready` refuses while any stage is not done. Task-
scoped: archived to .factory/history/<issue>/ and cleaned at ship.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from factory_lib import (
    decomposition_state_path, dump_json, head_sha, load_json, now_iso, repo_root, run_cmd,
)

from .common import fail
from .events import append_event

# The workflow writes these itself while a stage runs — the events ledger, the
# stage tracker, an assumption row appended to the active plan. They are not
# the product change under measurement, so write_scope does not have to name
# them. Deliberately NARROWER than pr_ready's EVIDENCE_PATHS: that list exempts
# all of `factory/` and `docs/`, which in the harness's own repo is the product
# — exempting it here would make the scope check vacuous exactly where it is
# being dogfooded.
WORKFLOW_PATHS = (".factory/", "plans/")


def stages_path(base: Path) -> Path:
    return base / ".factory" / "stages.json"


def write_skeleton(base: Path, issue: str, tasks: list[dict]) -> None:
    """Re-recording a decomposition after a mid-story scope change must not
    erase what is already built: surviving task ids keep their status and
    timestamps, new ids arrive pending, removed ids drop out."""
    existing = load_stages(base)
    previous = ({s.get("id"): s for s in existing.get("stages", [])}
                if existing.get("issue") == issue else {})
    stages = []
    for task in tasks:
        stage = {"id": task["id"], "title": task["title"], "status": "pending"}
        old = previous.get(task["id"])
        if old:
            stage.update({k: v for k, v in old.items()
                          if k in ("status", "started_at", "completed_at",
                                   "base_sha", "dirty_at_start", "task_sha256",
                                   "incomplete", "parallel")})
            stage["title"] = task["title"]
        stages.append(stage)
    dump_json(stages_path(base), {"issue": issue, "stages": stages})


def load_stages(base: Path) -> dict:
    return load_json(stages_path(base), default={})


def pending_stages(base: Path) -> list[dict]:
    return [s for s in load_stages(base).get("stages", [])
            if s.get("status") != "done"]


def _git(base: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=base, capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else ""


def dirty_paths(base: Path) -> list[str]:
    paths = []
    for line in _git(base, "status", "--porcelain", "-uall").splitlines():
        rel = line[3:].split(" -> ")[-1].strip().strip('"')
        if rel:
            paths.append(rel)
    return sorted(paths)


def _digest(base: Path, rel: str) -> str:
    path = base / rel
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""                                     # absent or unreadable


def dirty_digests(base: Path) -> dict[str, str]:
    """Content of every already-dirty path when the stage starts.

    Names alone are not enough: subtracting a NAME would hide every later edit
    to that file, so a worker could keep changing an out-of-scope dirty file
    invisibly, and legitimate work confined to an in-scope dirty file would
    read as an empty diff. Digests distinguish "still exactly as I found it"
    from "this stage changed it too"."""
    return {rel: _digest(base, rel) for rel in dirty_paths(base)}


def changed_paths(base: Path, base_sha: str, already_dirty) -> list[str]:
    """Everything this stage moved: commits since base_sha plus the working
    tree, minus paths that are byte-for-byte as the stage found them."""
    paths = set()
    head = head_sha(base)
    if base_sha and head and base_sha != head:
        paths.update(
            line for line in
            _git(base, "diff", "--name-only", f"{base_sha}..{head}").splitlines()
            if line.strip()
        )
    paths.update(dirty_paths(base))
    if isinstance(already_dirty, dict):
        paths = {p for p in paths if _digest(base, p) != already_dirty.get(p, "\0")}
    return sorted(paths)


def task_digest(task: dict) -> str:
    """The task contract a stage was started under.

    The decomposition can be re-recorded while a stage is active — that is the
    sanctioned repair when a scope turns out to be wrong — but it must not be
    a way to widen `write_scope` or drop `required_tests` moments before
    closing over them."""
    payload = json.dumps({k: task.get(k) for k in
                          ("write_scope", "required_tests", "verify_commands",
                           "acceptance_criteria")}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def _covered(path: str, scope: list[str]) -> bool:
    for entry in scope:
        prefix = entry.strip().rstrip("/")
        if prefix and (path == prefix or path.startswith(prefix + "/")):
            return True
    return False


def out_of_scope(paths: list[str], scope: list[str],
                 sibling_scope: list[str] | None = None) -> list[str]:
    """Product paths this stage touched that it never declared.

    `sibling_scope` is the write_scope of stages that ran ALONGSIDE this one.
    Parallel stages share a worktree and a HEAD (WORKFLOW.md Concurrency:
    fan-out happens across leaf tasks, in the task worktree), so a sibling's
    commit lands inside this stage's window. Disjointness is verified at
    `stage start`, so a path in a sibling's scope cannot be in mine — it is
    that sibling's to answer for, and its own `stage done` measures it."""
    return [p for p in paths
            if not p.startswith(WORKFLOW_PATHS)
            and not _covered(p, scope)
            and not _covered(p, sibling_scope or [])]


def task_for(base: Path, stage_id: str) -> dict:
    tasks = load_json(decomposition_state_path(base), default={}).get("tasks", [])
    return next((t for t in tasks if t.get("id") == stage_id), {})


def unresolved_tests(base: Path, required: list[str]) -> list[str]:
    """A declared test that exists nowhere is a declaration, not a test.

    Entries are test NAMES by convention (see any recorded decomposition), so
    the search is a fixed-string grep across tracked and untracked files —
    language-agnostic, and it catches the real failure: the test was never
    written. `.factory/` and `plans/` are excluded because the declaration
    itself lives there and would match itself."""
    missing = []
    for name in required:
        entry = name.strip()
        if not entry:
            continue
        if "/" in entry or entry.endswith((".py", ".ts", ".js", ".tsx", ".go")):
            if not (base / entry).exists():
                missing.append(entry)
            continue
        found = _git(base, "grep", "-l", "--untracked", "-F", "-e", entry,
                     "--", ":!.factory/", ":!plans/")
        if not found.strip():
            missing.append(entry)
    return missing


def _find(data: dict, stage_id: str) -> dict:
    stage = next((s for s in data.get("stages", []) if s.get("id") == stage_id), None)
    if stage is None:
        known = ", ".join(s.get("id", "?") for s in data.get("stages", []))
        fail(f"stage {stage_id!r} is not in .factory/stages.json ({known or 'empty'})")
    return stage


def cmd_start(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    data = load_stages(base)
    if not data:
        fail("no .factory/stages.json — record the decomposition first "
             "(record_decomposition_from_json.py creates the stage tracker)")
    stage = _find(data, args.id)
    if stage.get("status") == "done":
        fail(f"{args.id} is already done — stages don't reopen; a follow-up is a "
             "new stage in a re-recorded decomposition")
    # Order is the execution contract: earlier stages must be done first.
    # --parallel opts out ONLY for provably disjoint write scopes
    # (WORKFLOW.md Concurrency) — the caller asserts that, on the record.
    if not args.parallel:
        earlier = [s for s in data["stages"] if s is not stage]
        earlier = earlier[:data["stages"].index(stage)]
        not_done = [s["id"] for s in earlier if s.get("status") != "done"]
        if not_done:
            fail(f"{args.id} follows unfinished stage(s): {', '.join(not_done)} — "
                 "finish them, or pass --parallel if write scopes are disjoint "
                 "(WORKFLOW.md Concurrency).")
    else:
        # --parallel used to be an unchecked assertion. The decomposition
        # already states each task's write_scope, so the claim is verifiable.
        mine = task_for(base, args.id).get("write_scope") or []
        for other in data["stages"]:
            if other is stage or other.get("status") != "active":
                continue
            theirs = task_for(base, other["id"]).get("write_scope") or []
            overlap = sorted(
                {p for p in mine if _covered(p, theirs)}
                | {p for p in theirs if _covered(p, mine)}
            )
            if overlap:
                fail(f"{args.id} cannot run parallel to active stage {other['id']}: "
                     f"their write scopes overlap on {', '.join(overlap)}. Finish "
                     "one first, or re-decompose so the scopes are disjoint "
                     "(WORKFLOW.md Concurrency).")
    stage["status"] = "active"
    stage["started_at"] = now_iso()
    # `stage done` measures the diff, and a measurement needs a fixed point —
    # plus the dirt that was already there, which is not this stage's work.
    stage["base_sha"] = head_sha(base) or ""
    stage["dirty_at_start"] = dirty_digests(base)
    stage["task_sha256"] = task_digest(task_for(base, args.id))
    append_event(base, "stage-start", actor="implementer", story=data.get("issue", ""),
                 detail=f"{args.id} {stage.get('title', '')}")
    if args.parallel:
        stage["parallel"] = True
    dump_json(stages_path(base), data)
    print(f"Stage {args.id} active — {stage.get('title')}")
    print("Loop: implement via /codex:rescue → inspect diff → validate assumptions → "
          "smallest checks → LOCAL autoreview until clean → commit → forge stage done "
          f"{args.id}")


def _measure(base: Path, stage_id: str, stage: dict, task: dict,
             siblings: list[dict]) -> None:
    """Closing a stage is a measurement, not an assertion.

    Every other diff-based check in this repo fires when TOO MUCH changed.
    None fired when too little did — which is exactly what a stalled or
    half-finished delegation looks like, and it signed itself off."""
    base_sha = stage.get("base_sha")
    if not base_sha:
        fail(f"{stage_id} was started before its base commit was recorded, so "
             "there is nothing to measure against. Re-run "
             f"`forge stage start {stage_id}` (it is still active) and close it again.")
    if not task:
        fail(f"{stage_id} has no task in the recorded decomposition, so there is "
             "no contract to measure it against — a stage with no boundary is "
             "not something that can be attested. Re-record the decomposition "
             "with this task, then re-start the stage.")
    if not (task.get("write_scope") or []):
        fail(f"{stage_id} declares no write_scope, so nothing bounds what it may "
             "change. Re-record the decomposition with the paths this task owns, "
             f"then `forge stage start {stage_id}` again.")
    recorded = stage.get("task_sha256")
    if recorded and recorded != task_digest(task):
        # Re-recording mid-stage is the sanctioned repair for a wrong scope —
        # but it must not be a way to widen the contract moments before closing
        # over it. Re-starting re-baselines deliberately and on the record.
        fail(f"{stage_id}'s task contract changed after the stage started "
             "(write_scope, required_tests, verify_commands or acceptance "
             "criteria). Closing over a contract you just rewrote proves "
             f"nothing — run `forge stage start {stage_id}` to re-baseline "
             "against the current decomposition, then close it.")
    # Emptiness is judged on PRODUCT paths only. A stalled run still churns
    # .factory/ — the stage tracker and the events ledger move on every
    # command — so counting workflow paths would make this check pass for
    # exactly the runs it exists to catch.
    product = [p for p in changed_paths(base, base_sha, stage.get("dirty_at_start", []))
               if not p.startswith(WORKFLOW_PATHS)]
    if not product:
        fail(f"{stage_id} closes on an EMPTY diff — no product path changed since "
             f"{base_sha[:8]}, in commits or in the working tree. That is what a "
             "stalled or read-only run looks like. If the work is genuinely "
             f"partial, say so: forge stage done {stage_id} --incomplete \"<what "
             "is missing>\".")
    scope = task.get("write_scope") or []
    if scope:
        sibling_scope = [p for s in siblings
                         for p in (task_for(base, s["id"]).get("write_scope") or [])]
        strays = out_of_scope(product, scope, sibling_scope)
        if strays:
            fail(f"{stage_id} changed {len(strays)} path(s) outside its declared "
                 f"write_scope: {', '.join(strays[:10])}"
                 f"{'…' if len(strays) > 10 else ''}. Either the work exceeded the "
                 "task or the scope was wrong — re-record the decomposition with "
                 "the real scope rather than closing over it.")
    missing = unresolved_tests(base, task.get("required_tests") or [])
    if missing:
        fail(f"{stage_id} declares test(s) that exist nowhere in the repo: "
             f"{', '.join(missing)}. The implementer writes and records the "
             "tests (AGENTS.md); a declared test is not a test.")
    for command in task.get("verify_commands") or []:
        if not str(command).strip():
            continue
        result = run_cmd(str(command), base)
        if result["exit_code"] != 0:
            tail = (result["stderr"] or result["stdout"] or "").strip().splitlines()
            fail(f"{stage_id} verify command failed (exit {result['exit_code']}): "
                 f"{command}\n" + "\n".join(tail[-15:]))


def cmd_done(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    data = load_stages(base)
    if not data:
        fail("no .factory/stages.json — record the decomposition first")
    stage = _find(data, args.id)
    if stage.get("status") != "active":
        fail(f"{args.id} is {stage.get('status', 'pending')!r}, not active — "
             "`forge stage start` it first; done attests a stage that actually ran.")
    task = task_for(base, args.id)
    incomplete = (getattr(args, "incomplete", None) or "").strip()
    if incomplete:
        # A worker that genuinely finished part of the job had no vocabulary for
        # it: every signal kind presumes it wants to continue. This says so and
        # leaves the stage open, so nothing downstream reads it as delivered.
        stage["incomplete"] = incomplete
        stage["updated_at"] = now_iso()
        append_event(base, "stage-incomplete", actor="implementer",
                     story=data.get("issue", ""),
                     detail=f"{args.id}: {incomplete}")
        dump_json(stages_path(base), data)
        print(f"Stage {args.id} recorded INCOMPLETE and left active: {incomplete}")
        print("Nothing downstream treats it as delivered. Finish the gap, then "
              f"forge stage done {args.id}.")
        return
    # Stages that ran alongside this one: their commits land inside this
    # stage's window because parallel fan-out shares the task worktree.
    siblings = [s for s in data.get("stages", [])
                if s is not stage
                and (s.get("status") == "active"
                     or (s.get("completed_at") or "") >= (stage.get("started_at") or "~"))]
    _measure(base, args.id, stage, task, siblings)
    stage.pop("incomplete", None)
    stage["status"] = "done"
    stage["completed_at"] = now_iso()
    append_event(base, "stage-done", actor="implementer", story=data.get("issue", ""),
                 detail=f"{args.id} {stage.get('title', '')}")
    dump_json(stages_path(base), data)
    remaining = [s for s in data["stages"] if s.get("status") != "done"]
    if remaining:
        print(f"Stage {args.id} done. Next: forge stage start {remaining[0]['id']} "
              f"— {remaining[0].get('title')} ({len(remaining)} to go)")
    else:
        print(f"Stage {args.id} done — all {len(data['stages'])} stage(s) complete. "
              "Continue the task loop: verify, then the ONE branch autoreview.")


def cmd_list(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    data = load_stages(base)
    if not data:
        print("No stage tracker (.factory/stages.json) — it is created when the "
              "decomposition is recorded.")
        return
    marks = {"pending": " ", "active": ">", "done": "x"}
    for stage in data.get("stages", []):
        status = stage.get("status", "pending")
        par = " [parallel]" if stage.get("parallel") else ""
        print(f"[{marks.get(status, '?')}] {stage['id']} — {stage.get('title')}{par}")
