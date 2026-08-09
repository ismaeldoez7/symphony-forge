"""Read-only repo hygiene reporters used by ``forge sanitise``."""
from __future__ import annotations

import subprocess
from pathlib import Path

from factory_lib import clean_git_env

from . import context
from .common import fail


def _git_paths(base: Path, command: list[str]) -> list[str]:
    proc = subprocess.run(
        command, cwd=base, capture_output=True, text=True, env=clean_git_env(),
    )
    if proc.returncode != 0:
        fail(f"could not inspect repo hygiene: {proc.stderr.strip()}")
    return [entry for entry in proc.stdout.split("\0") if entry]


def source_secret_findings(base: Path) -> list[str]:
    """Report secret-shaped content in tracked, regular text files."""
    findings: list[str] = []
    for relative in _git_paths(base, ["git", "ls-files", "-z"]):
        path = base / relative
        if path.is_symlink() or not path.is_file():
            continue
        findings.extend(
            f"{relative}: {finding}" for finding in context.secret_findings(path)
        )
    return findings


def _is_dropping(relative: str) -> bool:
    path = Path(relative.rstrip("/"))
    if path.name == ".DS_Store" or "__pycache__" in path.parts:
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    return (
        path.parts[:1] == (".factory",)
        and path.name.endswith((".tmp", ".tmp.json", ".log"))
    )


def untracked_droppings(base: Path) -> list[str]:
    """List ignored or untracked machine droppings without removing them."""
    records = _git_paths(
        base,
        ["git", "status", "--porcelain=v1", "--ignored", "-z", "--untracked-files=all"],
    )
    return sorted({
        record[3:]
        for record in records
        if record[:2] in {"??", "!!"} and _is_dropping(record[3:])
    })


def secret_cruft_findings(base: Path) -> dict[str, list[str]]:
    """Return repo-wide secret and untracked-cruft findings without mutation."""
    return {
        "secrets": source_secret_findings(base),
        "untracked_droppings": untracked_droppings(base),
    }
