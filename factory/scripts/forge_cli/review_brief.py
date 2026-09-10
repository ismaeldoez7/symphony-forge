"""Compose plan-contract prompts for per-task and branch-wide review."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from factory_lib import (
    branch_diff_digest, load_json, now_iso,
    plan_digest_without_assumptions, proof_path,
    protected_decomposition_state_path, repo_root, require_task_grill,
    run_state_path, safe_factory_write_bytes, story_dir,
)


VERDICT_INSTRUCTION = (
    "For each contract, emit a verdict — implemented | partial | missing — "
    "with file:line evidence, recorded as contract_verdicts in the quality "
    "artifact. Then review the diff normally; the contract check does not "
    "replace the quality/performance/security lenses."
)

# Every lens hunts for code the diff kept only for compatibility: the owner's
# standing ruling is "we don't need legacy code", and a leftover that survives
# review ships. Rendered beside the lens focus in every brief.
LEFTOVER_INSTRUCTION = (
    "LEFTOVERS (blocking): the diff must carry no code kept only for "
    "compatibility — no wrapper or shim over its replacement, no re-export or "
    "alias kept 'for callers', no renamed-but-retained symbol, no dead branch "
    "behind a removed feature, no 'legacy'/'deprecated'/'backward' naming or "
    "comment. Report each as a BLOCKING finding with file:line and verdict the "
    "contract it belongs to as partial; a clean diff says so in one line."
)


def declared_contracts(decomposition: dict) -> list[dict]:
    """Return the validated decomposition-wide contract union in task order."""
    contracts: list[dict] = []
    for task in decomposition.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        entries = task.get("plan_contracts", [])
        if not isinstance(entries, list):
            continue
        contracts.extend(
            contract for contract in entries
            if isinstance(contract, dict) and isinstance(contract.get("id"), str)
        )
    return contracts


def _lessons_section(base: Path, task: dict) -> list[str]:
    """Lessons whose `applies_to` globs hit the task's write scope — the
    reviewer must not re-raise a finding the ledger already settled (the
    2026-09-04 case: a per-task review re-flagged as P1 the exact behaviour a
    recorded lesson pins as deliberate, because the brief never carried it)."""
    from .lessons import relevant_lessons
    scope = [p for p in task.get("write_scope", []) if isinstance(p, str)]
    if not scope:
        return []
    try:
        hits = relevant_lessons(base, scope)
    except SystemExit:
        return []
    if not hits:
        return []
    lines = ["### Lessons in force", "",
             "Recorded lessons that apply to this task's paths. A finding that "
             "contradicts one is not a defect unless it shows the lesson itself "
             "is wrong; say so explicitly instead of re-raising it.", ""]
    for lesson in hits:
        topic = str(lesson.get("topic", "")).strip()
        body = str(lesson.get("lesson", "")).strip()
        severity = str(lesson.get("severity", "")).strip()
        lines.append(f"- [{severity}] {topic}: {body}")
    lines.append("")
    return lines


def _approved_task_inputs(base: Path, task: dict) -> dict:
    """Load and validate the exact inputs every task review must receive."""
    state = load_json(run_state_path(base), default={})
    story = state.get("issue_key") or state.get("story")
    task_id = task.get("id")
    if not isinstance(story, str) or not story or not isinstance(task_id, str) or not task_id:
        raise SystemExit("Review brief refused: active story and task identity are required.")

    task_root = story_dir(base, story)
    plan = task_root / "task-plans" / f"{task_id}.md"
    if not plan.is_file():
        raise SystemExit(
            f"Review brief refused: approved task plan is missing for {task_id}; "
            "save and approve the target plan before reviewing."
        )
    try:
        plan_text = plan.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(
            f"Review brief refused: task plan for {task_id} is not UTF-8."
        ) from exc
    if not plan_text.strip():
        raise SystemExit(f"Review brief refused: task plan for {task_id} is empty.")

    grill = load_json(task_root / "grills" / "tasks" / f"{task_id}.json", default={})
    if not isinstance(grill, dict):
        raise SystemExit(f"Review brief refused: grill for {task_id} is missing or malformed.")
    digest = plan_digest_without_assumptions(plan)
    if (grill.get("gate") != "task" or grill.get("task_id") != task_id
            or grill.get("verdict") != "pass"):
        raise SystemExit(
            f"Review brief refused: grill for {task_id} is not a passing grill for this task."
        )
    if (grill.get("task_plan_sha256") != digest
            or grill.get("approved_task_plan_sha256") != digest):
        raise SystemExit(
            f"Review brief refused: grill/approval for {task_id} is stale or does not "
            "match the approved task plan."
        )
    if (not isinstance(grill.get("approved_by"), str)
            or not grill["approved_by"].strip()
            or not isinstance(grill.get("approved_at"), str)
            or not grill["approved_at"].strip()):
        raise SystemExit(
            f"Review brief refused: approved_by and approved_at are required for {task_id}."
        )
    try:
        require_task_grill(base, task_id, task)
    except SystemExit as exc:
        raise SystemExit(
            f"Review brief refused: task grill for {task_id} is stale or ungrounded: {exc}"
        ) from exc

    tests_path = proof_path(base, story, "tests.json", task_id=task_id)
    tests = load_json(tests_path, default={})
    automated = tests.get("automated") if isinstance(tests, dict) else None
    required = ("generated_by", "status", "summary", "blocking_findings",
                "commands_run", "reviewed_scope", "remaining_gaps",
                "recorded_at", "commit")
    if (not isinstance(automated, dict)
            or any(field not in automated for field in required)
            or not all(isinstance(automated.get(field), str) and automated[field].strip()
                       for field in ("generated_by", "status", "summary",
                                     "recorded_at", "commit"))
            or not isinstance(automated.get("blocking_findings"), list)
            or not isinstance(automated.get("commands_run"), list)
            or not automated.get("commands_run")
            or not isinstance(automated.get("reviewed_scope"), list)
            or not automated.get("reviewed_scope")
            or not isinstance(automated.get("remaining_gaps"), list)
            or not isinstance(tests.get("commit"), str)
            or tests.get("commit") != automated.get("commit")):
        raise SystemExit(
            f"Review brief refused: tests.json.automated for {task_id} must be the "
            "complete task-owned report (commands, scope, gaps, commit and time)."
        )

    branch = state.get("branch")
    if not isinstance(branch, str) or not branch.strip():
        proc = subprocess.run(
            ["git", "branch", "--show-current"], cwd=base,
            capture_output=True, text=True, encoding="utf-8",
        )
        branch = proc.stdout.strip() if proc.returncode == 0 else ""
    if not branch:
        raise SystemExit(f"Review brief refused: no branch identity for {task_id}.")
    return {
        "story": story,
        "task_id": task_id,
        "branch": branch,
        "plan_text": plan_text,
        "plan_sha256": digest,
        "grill": grill,
        "automated": automated,
    }


def _approved_inputs_section(base: Path, task: dict) -> list[str]:
    inputs = _approved_task_inputs(base, task)
    return [
        "### Approved task inputs", "",
        f"- Story: `{inputs['story']}`",
        f"- Task: `{inputs['task_id']}`",
        f"- Branch: `{inputs['branch']}`",
        f"- Approved plan digest: `{inputs['plan_sha256']}`", "",
        "#### Full approved task plan", "", "```markdown",
        inputs["plan_text"].rstrip(), "```", "",
        "#### Full grill and approval record", "", "```json",
        json.dumps(inputs["grill"], indent=2, sort_keys=True), "```", "",
        "#### Full task-owned automated report", "", "```json",
        json.dumps(inputs["automated"], indent=2, sort_keys=True), "```", "",
    ]

def _task_section(
        task: dict, base: Path | None = None, *, full_inputs: bool = True,
) -> list[str]:
    task_id = task.get("id", "")
    lines = [f"## Task {task_id}", "", "### Plan contracts", ""]
    contracts = task.get("plan_contracts", [])
    if contracts:
        for contract in contracts:
            lines.extend([
                f"- **{contract['id']}**",
                f"  - Source: {contract['source']}",
                f"  - Statement: {contract['statement']}",
            ])
    else:
        lines.append("- None declared.")
    reviewer_focus = task.get("reviewer_focus") \
        or "No task-specific reviewer focus declared."
    if isinstance(reviewer_focus, list):
        # The decomposition records reviewer_focus as a LIST; render bullets.
        reviewer_focus = "\n".join(f"- {item}" for item in reviewer_focus)
    lines.extend([
        "", "### Reviewer focus", "",
        reviewer_focus,
        "",
    ])
    if base is not None:
        lines.extend(_settled_section(base, task))
        lines.extend(_lessons_section(base, task))
        if full_inputs:
            lines.extend(_approved_inputs_section(base, task))
    return lines


def _plan_section_bodies(text: str, wanted: tuple[str, ...]) -> list[tuple[str, str]]:
    """`## <header>` sections of a plan whose header contains one of `wanted`
    (case-insensitive), as (header, body) pairs."""
    out: list[tuple[str, str]] = []
    header, body = "", []
    for line in text.splitlines() + ["## "]:
        if line.startswith("## "):
            if header and any(w in header.lower() for w in wanted):
                out.append((header, "\n".join(body).strip()))
            header, body = line[3:].strip(), []
        else:
            body.append(line)
    return out


def _settled_section(base: Path, task: dict) -> list[str]:
    """What this task's review may not relitigate: the story plan's decisions
    and rulings, and the contracts of tasks already shipped in the story.

    A reviewer that sees only one task's slice can find "defects" that an
    accepted decision requires (a client's three-lens review demanded, three
    rounds running, a guard the approved contract explicitly forbids, and its
    fix broke the story's pinned scenario). Those are proposals to change a
    decision, not findings against the diff; the brief says so."""
    from .stages import load_stages
    state = load_json(run_state_path(base), default={})
    issue = state.get("issue_key") or state.get("story") or ""
    lines: list[str] = []
    plan_files = sorted((base / "plans" / "active").glob(f"{issue}-*.md")) if issue else []
    for plan in plan_files[:1]:
        try:
            text = plan.read_text(encoding="utf-8")
        except OSError:
            continue
        for header, body in _plan_section_bodies(text, ("decision", "ruling")):
            if body:
                lines.extend([f"#### Story plan — {header}", "", body, ""])
    done = {s.get("id") for s in load_stages(base).get("stages", [])
            if isinstance(s, dict) and s.get("status") == "done"}
    decomposition = load_json(protected_decomposition_state_path(base), default={})
    shipped: list[str] = []
    for other in decomposition.get("tasks") or []:
        if not isinstance(other, dict) or other.get("id") == task.get("id"):
            continue
        if other.get("id") not in done:
            continue
        for contract in other.get("plan_contracts") or []:
            if isinstance(contract, dict) and contract.get("statement"):
                shipped.append(f"- **{contract.get('id')}** ({other.get('id')}): "
                               f"{contract['statement']}")
    if shipped:
        lines.extend(["#### Contracts shipped by earlier tasks in this story", ""]
                     + shipped + [""])
    if not lines:
        return []
    return ["### Settled — do not relitigate", "",
            "The following are accepted: the story plan's decisions and rulings, "
            "and the contracts of tasks already sealed in this story. A finding "
            "that contradicts one is a proposal to change a decision, which belongs "
            "in a decision record, not in this review; do not raise it as a defect. "
            "Rejected findings from earlier rounds are ledgered as lessons below.",
            ""] + lines


def cmd_review_brief(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    decomposition = load_json(protected_decomposition_state_path(base), default={})
    if not decomposition:
        raise SystemExit(
            "No recorded decomposition. Record it before composing a review brief."
        )
    if bool(args.id) == bool(args.all):
        raise SystemExit("review-brief requires exactly one task id or --all")

    tasks = decomposition.get("tasks") or []
    if args.all:
        selected = tasks
        filename = "all.md"
        title = "# Branch-wide plan-contract review brief"
    else:
        selected = [task for task in tasks if task.get("id") == args.id]
        if not selected:
            raise SystemExit(f"Unknown decomposition task id: {args.id}")
        filename = f"{args.id}.md"
        title = f"# Plan-contract review brief — {args.id}"

    lines = [title, "", VERDICT_INSTRUCTION, ""]
    from .stages import load_stages
    started = {
        row.get("id") for row in load_stages(base).get("stages", [])
        if isinstance(row, dict) and row.get("status") in {"active", "done"}
    }
    for task in selected:
        # Future tasks are context only in a branch-wide brief. The active task
        # and already-started tasks receive their complete approved inputs.
        full_inputs = not args.all or task.get("id") in started
        lines.extend(_task_section(task, base, full_inputs=full_inputs))
    relative = f"review-briefs/{filename}"
    body = ("\n".join(lines).rstrip() + "\n").encode()
    if not safe_factory_write_bytes(base, relative, body):
        raise SystemExit(f"Could not safely write .factory/{relative}")
    if args.all:
        state = load_json(run_state_path(base), default={})
        story = state.get("issue_key")
        if not isinstance(story, str) or not story:
            raise SystemExit("Cannot mint a branch review run without an active story.")
        brief_sha256 = hashlib.sha256(body).hexdigest()
        diff_digest = branch_diff_digest(base)
        token = {
            "review_run_id": hashlib.sha256(
                (brief_sha256 + diff_digest).encode()
            ).hexdigest(),
            "brief_sha256": brief_sha256,
            "branch_diff_digest": diff_digest,
            "minted_at": now_iso(),
        }
        token_relative = f"stories/{story}/review-run.json"
        token_body = (json.dumps(token, indent=2) + "\n").encode()
        if not safe_factory_write_bytes(base, token_relative, token_body):
            raise SystemExit(f"Could not safely write .factory/{token_relative}")
    print(f".factory/{relative}")
