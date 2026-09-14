"""Story closeout tells task-level from story-level by the evidence, not by a
pointer field only task worktrees ever get.

`forge task start` writes `base_main_sha` into the TASK worktree's pointer and
nothing writes it into the story's own. So WF-1, whose five tasks each shipped
as their own PR, was classed story-level at closeout and asked for the
story-wide verify, three-lens review and functional pass that the per-task
flow retired (2026-09-14). A task marker on the trunk, or committed in the
tree, is proof the story ships task by task: a story-level run cannot make one.
"""
from __future__ import annotations

import json

from test_gates import (  # noqa: F401
    configure_origin_main, delegation_ledger, git, prepare_pr_ready_story,
    publish_task_marker, repo, run, task_with_plan_contracts,
)
from factory_lib import (  # noqa: E402
    require_closeout_order, run_is_task_level, task_marker_path,
)

__all__ = ["repo"]


def _two_task_story(repo, tmp_path):
    scoped = prepare_pr_ready_story(repo, tmp_path, scoped_layout=True)
    control = delegation_ledger(repo).parent
    decomposition_path = control / "decomposition.json"
    decomposition = json.loads(decomposition_path.read_text())
    decomposition["tasks"].append({
        **decomposition["tasks"][0], "id": "T2", "title": "second slice",
    })
    decomposition["tasks"] = [
        task_with_plan_contracts(task, prefix=f"{task['id']}-C")
        for task in decomposition["tasks"]
    ]
    decomposition_path.write_text(json.dumps(decomposition))
    (scoped / "decomposition.json").write_text(json.dumps(decomposition))
    configure_origin_main(repo, tmp_path / "closeout-origin.git")
    pointer = json.loads((control / "run.json").read_text())
    assert "base_main_sha" not in pointer  # the story's own pointer never has it
    return scoped


def test_a_task_marker_on_the_trunk_makes_the_story_task_level(repo, tmp_path):
    _two_task_story(repo, tmp_path)
    # No marker anywhere yet: nothing says the story ships task by task.
    assert run_is_task_level(repo) is False
    story_level = require_closeout_order(repo)
    assert any("verify" in problem for problem in story_level)

    publish_task_marker(repo, "ENG-1", "T1")
    assert run_is_task_level(repo) is True
    task_level = require_closeout_order(repo)
    # The story-wide chain is no longer asked for; the per-task proof is.
    assert not any(".factory/verify.json" in problem for problem in task_level)
    assert not any("functional" in problem for problem in task_level)
    assert any("T2" in problem for problem in task_level), task_level
    code, out = run(repo, "pr_ready.py")
    assert code != 0, out
    assert "all task markers on origin/main before story closeout" in out
    assert "T2" in out
    # The story-wide chain is not asked for any more.
    assert "successful .factory/verify.json" not in out
    assert ".factory/tests.json:functional" not in out


def test_a_marker_committed_in_the_tree_counts_before_it_reaches_the_trunk(repo, tmp_path):
    _two_task_story(repo, tmp_path)
    marker = repo / task_marker_path("ENG-1", "T1")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({
        "task_id": "T1", "branch": "feat/ENG-1-T1",
        "base_main_sha": git(repo, "rev-parse", "origin/main"),
        "commit": git(repo, "rev-parse", "HEAD"),
        "sealed_at": "2026-09-14T00:00:00+00:00",
    }) + "\n")
    git(repo, "add", marker.relative_to(repo).as_posix())
    git(repo, "commit", "-q", "-m", "seal T1")
    assert run_is_task_level(repo) is True


def test_the_pointer_field_still_wins_inside_a_task_worktree(repo, tmp_path):
    _two_task_story(repo, tmp_path)
    control = delegation_ledger(repo).parent
    pointer = json.loads((control / "run.json").read_text())
    pointer["base_main_sha"] = git(repo, "rev-parse", "origin/main")
    (control / "run.json").write_text(json.dumps(pointer))
    assert run_is_task_level(repo) is True
