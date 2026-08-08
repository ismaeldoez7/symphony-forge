"""forge project audit — deterministic project-state gap detection."""
from __future__ import annotations

import argparse
from pathlib import Path

from check_board_complete import board_problems
from check_vendor_integrity import integrity_problems
from factory_lib import repo_root

from .roadmap import pending_story_problems


def project_gaps(base: Path) -> list[dict[str, str]]:
    """Compose the current local validators into one structured gap list."""
    gaps = [
        {"kind": "done-story", "detail": problem}
        for problem in board_problems(base)
    ]
    gaps.extend(
        {"kind": "pending-story", "detail": problem}
        for problem in pending_story_problems(base)
    )
    gaps.extend(
        {"kind": "vendor-drift", "detail": problem}
        for problem in (integrity_problems(base) or [])
    )
    return gaps


def cmd_audit(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    gaps = project_gaps(base)
    if not gaps:
        print("Project audit OK: no project-state gaps.")
        return

    print(f"Project audit FAILED: {len(gaps)} gap(s).")
    for gap in gaps:
        print(f"- [{gap['kind']}] {gap['detail']}")
    raise SystemExit(1)
