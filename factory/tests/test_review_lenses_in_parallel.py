"""A default task review calls one helper and publishes one selected generation."""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest

from test_gates import (  # noqa: F401
    DECOMP, HARNESS, git, head, intake, load_factory_lib, record_skeleton_then_frontier,
    record_task_grill, repo, save_plan, sign_off, write_in_scope, write_stages,
)

sys.path.insert(0, str(HARNESS / "factory" / "scripts"))
from forge_cli.review import codex_runs_path, review_task  # noqa: E402
from forge_cli.stages import load_stages  # noqa: E402


FAKE_REVIEW = r'''
import json, os, pathlib, sys
args = sys.argv[1:]
out = pathlib.Path(args[args.index("--json-output") + 1])
prompt = pathlib.Path(args[args.index("--prompt-file") + 1])
dataset = pathlib.Path(args[args.index("--dataset") + 1])
assert "### Approved task inputs" in dataset.read_text(encoding="utf-8")
text = prompt.read_text(encoding="utf-8")
assert all(marker in text for marker in (
    "BEGIN QUALITY", "BEGIN PERFORMANCE", "BEGIN SECURITY",
    "[quality] ", "[performance] ", "[security] ",
))
report = {
    "findings": [],
    "overall_correctness": "patch is correct",
    "overall_explanation": (
        "BEGIN QUALITY\nVERDICT C1: implemented — src/core.py:1\nEND QUALITY\n"
        "BEGIN PERFORMANCE\nNo repeated work.\nEND PERFORMANCE\n"
        "BEGIN SECURITY\nNo unsafe boundary.\nEND SECURITY"
    ),
    "overall_confidence": 0.9,
}
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
if os.environ.get("FAKE_MUTATE_HELPER"):
    pathlib.Path(__file__).write_text(pathlib.Path(__file__).read_text() + "\n# changed\n")
sys.exit(0)
'''


def _fake_skill(tmp_path: Path) -> Path:
    path = tmp_path / "fake-autoreview.py"
    path.write_text(FAKE_REVIEW, encoding="utf-8")
    return path


def _built(repo: Path, tmp_path: Path) -> None:
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    task = {
        **DECOMP["tasks"][0], "id": "T1", "write_scope": ["src/core.py"],
        "plan_contracts": [{"id": "C1",
                            "statement": DECOMP["tasks"][0]["acceptance_criteria"][0],
                            "source": "plan"}],
    }
    record_skeleton_then_frontier(repo, [task])
    write_stages(repo, {"issue": "ENG-1", "stages": [
        {"id": "T1", "title": task["title"], "status": "active", "base_sha": head(repo)},
    ]})
    code, output = record_task_grill(repo, task)
    assert code == 0, output
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "prepare review")
    write_stages(repo, {"issue": "ENG-1", "stages": [
        {"id": "T1", "title": task["title"], "status": "active", "base_sha": head(repo)},
    ]})
    write_in_scope(repo, "src/core.py")
    git(repo, "add", "src/core.py")
    git(repo, "commit", "-qm", "work")
    lib = load_factory_lib(repo)
    commit = head(repo)
    automated = {
        "generated_by": "implementer", "status": "passed",
        "summary": "combined review fixture passed", "blocking_findings": [],
        "commands_run": ["pytest test_review_lenses_in_parallel.py"],
        "reviewed_scope": ["src/core.py"], "remaining_gaps": [],
        "recorded_at": "2026-09-11T00:00:00+00:00", "commit": commit,
    }
    for name, body in (
        ("verify.json", {"ok": True, "commit": commit}),
        ("tests.json", {"automated": automated, "commit": commit}),
    ):
        path = lib.proof_path(repo, "ENG-1", name, task_id="T1", for_write=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        lib.dump_json(path, body)


def _selection(repo: Path) -> tuple[Path, dict, dict]:
    path = repo / ".factory/stories/ENG-1/tasks/T1/reviews/selected.json"
    pointer = json.loads(path.read_text())
    generation_path = path.parent / "generations" / f"{pointer['generation_id']}.json"
    return path, pointer, json.loads(generation_path.read_text())


def test_default_review_uses_one_helper_and_publishes_one_generation(repo, tmp_path):
    _built(repo, tmp_path)
    outcome = review_task(repo, "T1", skill=str(_fake_skill(tmp_path)), engine="claude")

    assert outcome["blocking"] == 0 and outcome["stamped"] is True
    selection_path, pointer, generation = _selection(repo)
    assert selection_path.is_file()
    assert generation["origin"] == "combined"
    assert set(generation["lenses"]) == {"quality", "performance", "security"}
    raw = base64.b64decode(generation["raw_result"]["data"], validate=True)
    assert json.loads(raw)["overall_correctness"] == "patch is correct"
    rows = [json.loads(line) for line in codex_runs_path(repo).read_text().splitlines()]
    assert [row["status"] for row in rows if row.get("kind") == "review"].count(
        "starting") == 1
    stage = next(item for item in load_stages(repo)["stages"] if item["id"] == "T1")
    assert stage["local_review_stamp"]["delta_id"] == pointer["delta_id"]


def test_review_helper_identity_mismatch_refuses_publication(repo, tmp_path, monkeypatch):
    _built(repo, tmp_path)
    helper = _fake_skill(tmp_path)
    review_task(repo, "T1", skill=str(helper), engine="claude")
    selection_path, _pointer, _generation = _selection(repo)
    before = selection_path.read_bytes()

    monkeypatch.setenv("FAKE_MUTATE_HELPER", "1")
    with pytest.raises(SystemExit):
        review_task(repo, "T1", skill=str(helper), engine="claude")
    assert selection_path.read_bytes() == before
