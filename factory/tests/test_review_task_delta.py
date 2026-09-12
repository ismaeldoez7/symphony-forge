"""Per-task review measures the TASK's delta and carries the lessons in force.

Two 2026-09-04 defects from the first per-task review on a client repo:
- the trunk had been merged into the task branch after the stage began, and
  `forge review` diffed from the stage's recorded base, so the bundle carried
  the whole vendored-harness delta, chunked into three passes, scored 0 on
  findings against code the task never touched, and recorded every contract
  as `partial` because the chunked reviewer never reached the verdict lines;
- the brief carried no lessons, so the reviewer re-raised as P1 the exact
  behaviour a recorded lesson pins as deliberate.
"""
from __future__ import annotations

import json
import copy
import hashlib
import subprocess

import pytest

from test_gates import (  # noqa: I001 — test_gates puts factory/scripts on sys.path
    DECOMP, _write_complete_automated, git, head, intake, record_task_grill, repo,
    run, save_plan, sign_off, skeletal_stage_task, task_skeleton,
)
from forge_cli.review import _project_combined_report, resolve_review_base  # noqa: E402

__all__ = ["repo"]


def _combined_explanation(quality: str, performance: str, security: str) -> str:
    return (
        f"BEGIN FORGE ASSESSMENT quality\n{quality}\nEND FORGE ASSESSMENT quality\n"
        f"BEGIN FORGE ASSESSMENT performance\n{performance}\n"
        f"END FORGE ASSESSMENT performance\n"
        f"BEGIN FORGE ASSESSMENT security\n{security}\nEND FORGE ASSESSMENT security"
    )


def _combined_finding(lens: str, title: str, path: str, line: int) -> dict:
    return {
        "title": f"[{lens}] {title}", "body": "evidence", "priority": "P2",
        "confidence": 0.9, "category": "bug",
        "code_location": {"file_path": path, "line": line},
    }


def test_combined_review_projects_tagged_lenses_and_preserves_ordered_pass_verdicts():
    task = {"id": "T1", "plan_contracts": [
        {"id": "T1-C1", "statement": "works", "source": "plan"},
    ]}
    first = {
        "overall_explanation": _combined_explanation(
            "VERDICT T1-C1: implemented — src/a.py:1", "fast", "safe"),
        "findings": [_combined_finding("performance", "Avoid repeat work", "src/a.py", 4)],
    }
    second = {
        "overall_explanation": _combined_explanation(
            "VERDICT T1-C1: partial — src/a.py:8 race", "bounded", "isolated"),
        "findings": [_combined_finding("security", "Validate token", "src/b.py", 9)],
    }
    report = {
        "overall_explanation": "Review passes returned.",
        "findings": [*first["findings"], *second["findings"]],
        "pass_reports": [
            {"label": "chunk 1/2", "report": first},
            {"label": "chunk 2/2", "report": second},
        ],
    }

    lenses = _project_combined_report(
        task, report, ["src/a.py", "src/b.py"], "a" * 40, "b" * 40, [], [task], {"T1": "active"}, ())

    assert lenses["quality"]["contract_verdicts"] == [{
        "contract_id": "T1-C1", "verdict": "partial", "evidence": "src/a.py:8 race",
    }]
    assert lenses["performance"]["non_blocking_findings"][0]["summary"].startswith(
        "Avoid repeat work (src/a.py:4)")
    assert lenses["security"]["non_blocking_findings"][0]["summary"].startswith(
        "Validate token (src/b.py:9)")


def test_combined_review_refuses_incomplete_noncontiguous_missing_copied_or_mixed_output():
    mutators = (
        lambda report: report.update(
            overall_explanation="preface\n" + report["overall_explanation"]),
        lambda report: report.update(overall_explanation=report["overall_explanation"].replace(
            "END FORGE ASSESSMENT quality\nBEGIN FORGE ASSESSMENT performance",
            "END FORGE ASSESSMENT quality\nstray\nBEGIN FORGE ASSESSMENT performance")),
        lambda report: report.update(overall_explanation=report["overall_explanation"].replace(
            "BEGIN FORGE ASSESSMENT performance",
            "BEGIN FORGE ASSESSMENT security", 1)),
        lambda report: report["findings"].append(
            _combined_finding("quality", "Same issue", "src/./a.py", 3)),
        lambda report: report["findings"].append(
            _combined_finding("security", "  same   ISSUE ", "src/a.py", 3)),
        lambda report: report["findings"][0].update(title="Missing lens tag"),
    )
    for mutate in mutators:
        report = {
            "overall_explanation": _combined_explanation(
                "VERDICT C1: implemented — src/a.py:1", "measured", "bounded"),
            "findings": [_combined_finding("quality", "Same issue", "src/a.py", 3)],
        }
        mutate(report)
        with pytest.raises(SystemExit):
            _project_combined_report(
                {"id": "T1", "plan_contracts": [{"id": "C1"}]}, report,
                ["src/a.py"], "a" * 40, "b" * 40, [], [], {}, ())
    first = {"overall_explanation": _combined_explanation(
        "VERDICT C1: implemented — src/a.py:1", "measured", "bounded"),
        "findings": [_combined_finding("quality", "first", "src/a.py", 1)]}
    second = {**first, "findings": [
        _combined_finding("security", "second", "src/a.py", 2)]}
    report = {"overall_explanation": "passes", "findings": [
        *second["findings"], *first["findings"]], "pass_reports": [
        {"label": "chunk 1/2", "report": first},
        {"label": "chunk 2/2", "report": second}]}
    with pytest.raises(SystemExit):
        _project_combined_report(
            {"id": "T1", "plan_contracts": [{"id": "C1"}]}, report,
            ["src/a.py"], "a" * 40, "b" * 40, [], [], {}, ())

    # Matching fingerprints cannot hide changed finding evidence in the
    # synthesized top-level report.
    report = {"overall_explanation": "passes", "findings": [
        copy.deepcopy(first["findings"][0])], "pass_reports": [
        {"label": "chunk 1/1", "report": first}]}
    report["findings"][0]["body"] = "different evidence"
    with pytest.raises(SystemExit):
        _project_combined_report(
            {"id": "T1", "plan_contracts": [{"id": "C1"}]}, report,
            ["src/a.py"], "a" * 40, "b" * 40, [], [], {}, ())


def test_review_set_recorder_validates_origin_specific_shape_and_raw_bytes(repo, tmp_path):
    from test_review_settled_contracts import _publish, _story
    _story(repo, tmp_path)
    generation, _pointer = _publish(repo)
    candidate = {key: value for key, value in generation.items() if key != "generation_id"}
    malformed = copy.deepcopy(candidate)
    malformed["raw_result"]["bytes"] += 1
    code, out = run(repo, "record_review_from_json.py", "--set", "--task", "T2",
                    stdin=json.dumps(malformed))
    assert code != 0 and "decoded byte count" in out
    malformed = copy.deepcopy(candidate)
    malformed["origin"] = "rejection"
    malformed["rejection"] = {
        "source_generation_id": generation["generation_id"],
        "source_generation_sha256": _pointer["generation_sha256"],
        "root_generation_id": generation["generation_id"],
        "history": [{"finding_fingerprint": "f" * 64, "reason": "reason",
                     "citation": "T1-AC1", "actor": "autoreview"}],
    }
    code, out = run(repo, "record_review_from_json.py", "--set", "--task", "T2",
                    stdin=json.dumps(malformed))
    assert code != 0 and "only accepts origin=combined" in out
    fabricated = copy.deepcopy(candidate)
    fabricated["lenses"]["security"]["summary"] = "fabricated clean proof"
    code, out = run(repo, "record_review_from_json.py", "--set", "--task", "T2",
                    stdin=json.dumps(fabricated))
    assert code != 0 and "do not match the raw helper result" in out

    stale = copy.deepcopy(candidate)
    token_path = repo / ".factory/stories/ENG-1/review-run.json"
    token = json.loads(token_path.read_text())
    token["branch_diff_digest"] = "0" * 64
    token["review_run_id"] = hashlib.sha256(
        (token["brief_sha256"] + token["branch_diff_digest"]).encode()
    ).hexdigest()
    token_path.write_text(json.dumps(token))
    stale["review_run_id"] = token["review_run_id"]
    for lens in stale["lenses"].values():
        lens["review_run_id"] = token["review_run_id"]
    code, out = run(repo, "record_review_from_json.py", "--set", "--task", "T2",
                    stdin=json.dumps(stale))
    assert code != 0 and "current task delta" in out


def _commit(repo, name: str, content: str) -> str:
    (repo / name).parent.mkdir(parents=True, exist_ok=True)
    (repo / name).write_text(content)
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", f"add {name}")
    return head(repo)


def test_review_base_advances_past_a_trunk_merged_after_the_stage_began(repo):
    recorded = head(repo)                       # the stage's recorded base
    git(repo, "checkout", "-q", "-b", "feat/ENG-1-T1")
    task_commit = _commit(repo, "src/task.py", "task work\n")

    # No trunk merge: the recorded base stands.
    assert resolve_review_base(repo, {"base_sha": recorded}, {}, head(repo)) == recorded

    # The trunk moves and is merged INTO the task branch.
    git(repo, "checkout", "-q", "-b", "trunk-work", recorded)
    trunk_commit = _commit(repo, "factory/vendored.py", "harness delta\n")
    git(repo, "update-ref", "refs/remotes/origin/main", trunk_commit)
    git(repo, "checkout", "-q", "feat/ENG-1-T1")
    git(repo, "merge", "-q", "--no-edit", "origin/main")
    tip = head(repo)

    advanced = resolve_review_base(repo, {"base_sha": recorded}, {}, tip)
    assert advanced == trunk_commit
    # The reviewed delta is the task's own work only.
    delta = git(repo, "diff", "--name-only", f"{advanced}...{tip}").splitlines()
    assert delta == ["src/task.py"]
    assert task_commit != tip
    from factory_lib import product_delta_digest
    expected = subprocess.run(
        ["git", "diff", "--binary", "--no-ext-diff", advanced, tip,
         "--", "src/task.py"], cwd=repo, capture_output=True, check=True,
    ).stdout
    historical_delta = product_delta_digest(repo, advanced, tip)
    assert historical_delta == hashlib.sha256(expected).hexdigest()
    (repo / "src/task.py").write_text("later unreviewed edit\n")
    git(repo, "add", "src/task.py")
    assert product_delta_digest(repo, advanced, tip) == historical_delta
    git(repo, "restore", "--source", tip, "--staged", "--worktree", "src/task.py")

    # A trunk that moved WITHOUT being merged does not move the base.
    git(repo, "checkout", "-q", "trunk-work")
    unmerged = _commit(repo, "factory/later.py", "later\n")
    git(repo, "update-ref", "refs/remotes/origin/main", unmerged)
    git(repo, "checkout", "-q", "feat/ENG-1-T1")
    assert resolve_review_base(repo, {"base_sha": recorded}, {}, tip) == trunk_commit

    # A recorded base that is not an ancestor of HEAD is refused, not guessed.
    with pytest.raises(SystemExit):
        resolve_review_base(repo, {"base_sha": unmerged}, {}, tip)


def test_review_base_advances_when_the_recorded_base_is_a_branch_commit(repo):
    """A story branch carried planning commits BEFORE the stage started, so the
    recorded base is a branch commit — neither ancestor nor descendant of the
    trunk point once the trunk is merged in. The trunk point is still the base:
    the branch's own delta since divergence is reviewed, never the trunk's."""
    fork = head(repo)
    git(repo, "checkout", "-q", "-b", "feat/ENG-1-story")
    _commit(repo, "plans/story-plan.md", "planning\n")
    recorded = head(repo)                       # stage started here, on the branch
    _commit(repo, "src/task.py", "task work\n")

    git(repo, "checkout", "-q", "-b", "trunk-work", fork)
    trunk_commit = _commit(repo, "factory/vendored.py", "harness delta\n")
    git(repo, "update-ref", "refs/remotes/origin/main", trunk_commit)
    git(repo, "checkout", "-q", "feat/ENG-1-story")
    git(repo, "merge", "-q", "--no-edit", "origin/main")
    tip = head(repo)

    advanced = resolve_review_base(repo, {"base_sha": recorded}, {}, tip)
    assert advanced == trunk_commit
    delta = sorted(git(repo, "diff", "--name-only", f"{advanced}...{tip}").splitlines())
    assert delta == ["plans/story-plan.md", "src/task.py"]
    assert "factory/vendored.py" not in delta


def test_review_brief_carries_the_lessons_in_force_for_the_task_paths(repo, tmp_path):
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    first = {**DECOMP["tasks"][0], "id": "T1", "reviewer_focus": "focus one",
             "acceptance_criteria": ["first statement"],
             "write_scope": ["src/permission/gate.py", "test/gate_test.py"],
             "plan_contracts": [{"id": "C1", "statement": "first statement",
                                  "source": "plan.md#first"}]}
    second = {**skeletal_stage_task("T2", "second slice"), "dependencies": ["T1"]}
    skeletons = [task_skeleton(first), task_skeleton(second)]
    code, out = run(repo, "record_decomposition_from_json.py", stdin=json.dumps(
        {**DECOMP, "tasks": skeletons}))
    assert code == 0, out
    code, out = run(repo, "record_decomposition_from_json.py", stdin=json.dumps(
        {**DECOMP, "tasks": [first, skeletons[1]]}))
    assert code == 0, out
    code, out = record_task_grill(repo, first)
    assert code == 0, out
    _write_complete_automated(repo)

    for topic, applies_to in (
        ("soft rail asks keep classifier eligibility", "src/permission/**"),
        ("unrelated discord lesson", "src/channels/discord/**"),
    ):
        code, out = run(repo, "forge.py", "lesson", "add", "--topic", topic,
                        "--lesson", f"{topic} — pinned by test", "--source", "review r1",
                        "--applies-to", applies_to, "--severity", "high",
                        "--by", "orchestrator", "--repo", str(repo))
        assert code == 0, out

    code, out = run(repo, "forge.py", "review-brief", "T1", "--repo", str(repo))
    assert code == 0, out
    brief = (repo / out.strip()).read_text()
    assert "### Lessons in force" in brief
    assert "soft rail asks keep classifier eligibility" in brief
    assert "pinned by test" in brief
    assert "unrelated discord lesson" not in brief


def test_review_tip_puts_harness_bookkeeping_back_at_the_task_base(repo, tmp_path):
    from forge_cli.review import product_only_tip

    base_sha = head(repo)
    git(repo, "checkout", "-q", "-b", "feat/ENG-1-T1")
    (repo / "plans" / "exploration").mkdir(parents=True, exist_ok=True)
    (repo / "plans" / "exploration" / "grill-r1.md").write_text("x" * 5000)
    (repo / ".factory" / "stories" / "ENG-1").mkdir(parents=True, exist_ok=True)
    (repo / ".factory" / "stories" / "ENG-1" / "verify.json").write_text("{}")
    _commit(repo, "src/task.py", "task work\n")
    git(repo, "add", "-A", "plans", ".factory")
    git(repo, "commit", "-q", "-m", "planning artifacts")
    tip = head(repo)

    worktree = tmp_path / "review-wt"
    git(repo, "worktree", "add", "--detach", str(worktree), tip)
    review_tip = product_only_tip(worktree, base_sha)
    assert review_tip != tip
    delta = sorted(git(worktree, "diff", "--name-only", f"{base_sha}..{review_tip}").splitlines())
    assert delta == ["src/task.py"]
    # The task branch itself is untouched.
    assert head(repo) == tip
    git(repo, "worktree", "remove", "--force", str(worktree))


def test_review_brief_carries_the_recorded_verification_evidence(repo, tmp_path):
    sign_off(repo)
    intake(repo)
    save_plan(repo, tmp_path)
    first = {**DECOMP["tasks"][0], "id": "T1", "reviewer_focus": "focus one",
             "acceptance_criteria": ["unit suites pass; tsc green"],
             "write_scope": ["src/gate.py"],
             "plan_contracts": [{"id": "C1", "statement": "unit suites pass; tsc green",
                                  "source": "plan.md#first"}]}
    code, out = run(repo, "record_decomposition_from_json.py", stdin=json.dumps(
        {**DECOMP, "tasks": [task_skeleton(first)]}))
    assert code == 0, out
    code, out = run(repo, "record_decomposition_from_json.py", stdin=json.dumps(
        {**DECOMP, "tasks": [first]}))
    assert code == 0, out
    code, out = record_task_grill(repo, first)
    assert code == 0, out
    _write_complete_automated(repo)

    code, out = run(repo, "forge.py", "review-brief", "T1", "--repo", str(repo))
    assert code == 0, out
    brief = (repo / out.strip()).read_text()
    assert "### Approved task inputs" in brief
    assert "#### Full task-owned automated report" in brief
    assert '"status": "passed"' in brief
    assert '"commands_run"' in brief


def test_contract_verdicts_read_every_preserved_pass_report_and_keep_the_worst():
    """A chunked autoreview replaces the top-level explanation with a summary
    line and keeps each pass's conclusions (with its VERDICT lines) under
    pass_reports; the recorder must read those, and when two passes disagree
    the worse verdict wins (a pass that saw a defect is never outvoted by a
    pass that only saw the files exist)."""
    from forge_cli.review import _contract_verdicts

    task = {"id": "T1", "plan_contracts": [
        {"id": "T1-AC1", "statement": "a", "source": "p"},
        {"id": "T1-AC2", "statement": "b", "source": "p"},
        {"id": "T1-AC3", "statement": "c", "source": "p"},
    ]}
    reviewed = {
        "overall_explanation": "Review passes returned. chunk 1/2: 1 finding(s), "
                               "chunk 2/2: 0 finding(s). See preserved pass reports.",
        "findings": [],
        "pass_reports": [
            {"report": {"overall_explanation":
                        "VERDICT T1-AC1: implemented — src/a.py:1 present\n"
                        "VERDICT T1-AC2: partial — src/b.py:9 races the index\n",
                        "findings": []}},
            {"report": {"overall_explanation":
                        "VERDICT T1-AC1: implemented — src/a.py:1\n"
                        "VERDICT T1-AC2: implemented — src/b.py:1 exists\n"
                        "VERDICT T1-AC3: missing — nothing in this chunk\n",
                        "findings": []}},
        ],
    }
    out = {v["contract_id"]: v for v in _contract_verdicts(task, reviewed, [task], {})}
    assert out["T1-AC1"]["verdict"] == "implemented"
    assert out["T1-AC2"]["verdict"] == "partial"
    assert "races the index" in out["T1-AC2"]["evidence"]
    assert out["T1-AC3"]["verdict"] == "missing"
    assert "no VERDICT line" not in out["T1-AC1"]["evidence"]


def test_every_lens_brief_hunts_for_compatibility_leftovers():
    """Owner ruling: no legacy code. Every lens prompt carries the leftover
    instruction (wrappers, shims, aliases, retained symbols, dead branches,
    'legacy' naming are blocking and verdict the contract partial)."""
    from forge_cli.review import _lens_prompt
    from forge_cli.review_brief import LEFTOVER_INSTRUCTION

    task = {"id": "T1", "plan_contracts": [], "reviewer_focus": "focus"}
    for lens in ("quality", "performance", "security"):
        text = _lens_prompt(task, lens).decode()
        assert LEFTOVER_INSTRUCTION in text, lens
        assert "BLOCKING" in LEFTOVER_INSTRUCTION


def test_vendored_client_review_excludes_the_harness_machinery(repo):
    """A re-vendor commit on a task branch put 36 harness files into a client's
    review bundle and the quality lens raised P1s against harness code the task
    never touched. In a vendored client the review drops the same machinery
    prefixes the stage measure already exempts."""
    from forge_cli.review import HARNESS_PREFIXES, review_excluded_prefixes
    from forge_cli.stages import HARNESS_MACHINERY_PATHS, WORKFLOW_PATHS
    marker = repo / "constitution" / "VENDORED_FROM"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text("symphony-forge @ deadbeef\n")
    vendored = review_excluded_prefixes(repo)
    assert "factory/" in vendored and ".claude/" in vendored and "constitution/" in vendored
    assert set(vendored) == set(HARNESS_PREFIXES) | set(WORKFLOW_PATHS) | set(HARNESS_MACHINERY_PATHS)
    marker.unlink()
    harness_only = review_excluded_prefixes(repo)
    assert set(harness_only) == set(HARNESS_PREFIXES) | set(WORKFLOW_PATHS)
    assert "factory/" not in harness_only
