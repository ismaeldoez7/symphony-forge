#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from factory_lib import (
    decomposition_state_path, dump_json, gate, head_sha, now_iso, repo_root,
    run_state_path, validate_payload,
)

parser = argparse.ArgumentParser(description="Record decomposition from structured JSON")
parser.add_argument("--input", help="Path to decomposition JSON. If omitted, read from stdin.")
args = parser.parse_args()

if args.input:
    payload = json.loads(Path(args.input).read_text())
else:
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("Expected JSON on stdin or via --input")
    payload = json.loads(raw)

root = repo_root()
state = gate(root, signoff=True, approved_plan=True)
validate_payload(root, "decomposition", payload)
tasks = payload.get("tasks") or []
if not tasks:
    raise SystemExit(
        "decomposition needs at least one leaf task — an empty task graph opens the "
        "implementation gates with nothing bounded to implement."
    )
OBJECTIVE_MAX = 500
for pos, task in enumerate(tasks, 1):
    if not isinstance(task, dict) or not isinstance(task.get("id"), str) \
            or not isinstance(task.get("title"), str) or not task["id"].strip():
        raise SystemExit(
            f"decomposition task {pos} must be an object with string 'id' and 'title' "
            "(plus write_scope/acceptance_criteria per the decomposer contract)."
        )
    # The narrative fields were prompt-convention and silently droppable, so a
    # task could reach the board as an id and a title. They are the contract now.
    objective = task.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        raise SystemExit(
            f"decomposition task {task['id']}: 'objective' is required — one or two "
            "sentences of what this task changes and why, in a reader's language."
        )
    if len(objective) > OBJECTIVE_MAX:
        raise SystemExit(
            f"decomposition task {task['id']}: 'objective' is {len(objective)} chars "
            f"(max {OBJECTIVE_MAX}) — it is the summary a human reads, not the "
            "implementation transcript; put the detail in the plan."
        )
    criteria = task.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria or not all(
        isinstance(c, str) and c.strip() for c in criteria
    ):
        raise SystemExit(
            f"decomposition task {task['id']}: 'acceptance_criteria' must be a "
            "non-empty list of non-empty strings — a task nobody can check is done "
            "cannot be reviewed."
        )
payload["commit"] = head_sha(root)
dump_json(decomposition_state_path(root), payload)
# The decomposition is immutable evidence; the stage tracker is its mutable
# execution twin (decision 0007) — pr_ready refuses while stages are open.
from forge_cli.stages import write_skeleton  # noqa: E402
write_skeleton(root, state.get("issue_key", ""), tasks)
state["decomposition_status"] = "recorded"
state["updated_at"] = now_iso()
dump_json(run_state_path(root), state)
from forge_cli.events import append_event  # noqa: E402
append_event(root, "decomposed", actor="docs-decomposer",
             story=state.get("issue_key", ""), detail=f"{len(tasks)} task(s)")
print(f"Recorded decomposition ({len(tasks)} stage(s) -> .factory/stages.json; "
      "work them with `forge stage start/done`)")
