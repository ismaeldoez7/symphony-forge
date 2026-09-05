"""`forge next` asks the human how many tasks before the decomposition exists.

Its own module: test_gates.py is one 680-test file, so every branch adding a
test there collides with every other.
"""
from __future__ import annotations

from pathlib import Path

from test_gates import HARNESS, repo  # noqa: F401

import sys

sys.path.insert(0, str(HARNESS / "factory" / "scripts"))
from forge_cli.phase import _task_count_hint  # noqa: E402


def _plan(repo: Path, name: str, body: str) -> str:
    path = repo / "plans" / "active" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return f"plans/active/{name}"


def test_the_recommendation_scales_with_the_plan(repo):
    # A story's task count decides how many plans, grills, approvals, reviews
    # and PRs it will cost, so it is the human's call. But asking with nothing
    # behind the question is a rubber stamp — the answer is always the same
    # number. The plan already knows its size; the question carries it.
    small = _plan(repo, "SMALL-1-tiny.md",
                  "## Acceptance Criteria\n\n1. One thing works.\n")
    assert "about 1" in _task_count_hint(repo, {"plan_file": small})

    big = _plan(repo, "BIG-1-large.md", "## Acceptance Criteria\n\n"
                + "".join(f"{n}. Criterion {n}.\n" for n in range(1, 11))
                + "\n## Surface Impact\n\napps/api/src/x.ts, apps/web/src/y.tsx\n")
    hint = _task_count_hint(repo, {"plan_file": big})
    assert "about 4" in hint
    assert "10 acceptance criteria" in hint
    assert "backend" in hint and "frontend" in hint

    # Never above the preferred ceiling on its own authority.
    huge = _plan(repo, "HUGE-1-vast.md", "## Acceptance Criteria\n\n"
                 + "".join(f"{n}. Criterion {n}.\n" for n in range(1, 41))
                 + "\napps/api apps/web drizzle\n")
    assert "about 4" in _task_count_hint(repo, {"plan_file": huge})


def test_the_recommendation_never_fails_the_command(repo):
    # It is guidance inside `forge next`; a plan it cannot read must not take
    # the command down with it.
    assert _task_count_hint(repo, {})
    assert _task_count_hint(repo, {"plan_file": "plans/active/missing.md"})


def test_forge_next_asks_before_it_decomposes(repo):
    # Ordering is the whole point: asked AFTER the decomposition is authored,
    # the number is a correction to work already shaped by habit.
    source = (HARNESS / "factory" / "scripts" / "forge_cli" / "phase.py"
              ).read_text(encoding="utf-8")
    step = source[source.index("FIRST ask the human how many tasks"):][:600]
    assert "docs-decomposer" in step
    assert step.index("FIRST ask") < step.index("docs-decomposer")
    # And it says WHY, so the number is weighed rather than guessed.
    assert "plan, grill, approval, review and PR" in step
