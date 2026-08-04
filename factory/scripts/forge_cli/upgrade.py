"""forge upgrade — re-vendor harness machinery into an existing client repo.

Run FROM the harness clone, targeting the client repo (mirrors `forge init`).
Replaces machinery the harness owns; never touches project-owned content.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from factory_lib import head_sha, repo_root

from .common import fail
from .scaffold import (
    COPY_CODEX, COPY_WORKFLOWS, DOC_CONTRACTS, PROJECT_STARTERS,
    ensure_jsonl_attributes,
)

# Harness-owned: replaced wholesale on upgrade.
UPGRADE_TREES = ["factory", "constitution", "harness"]
UPGRADE_FILES = ["forge", "CLAUDE.md", "WORKFLOW.md"]
# .claude is MIXED ownership: client repos legitimately carry their own
# skills, agents, launch.json, and settings.local.json (standard Claude Code
# surfaces — see the thin-adapter linter). Upgrade replaces ONLY the paths
# the harness ships and never deletes client additions; retiring a
# harness-shipped path is an explicit upgrade note, not an rmtree side
# effect. Same rule for .codex/agents and .codex/skills below.
CLAUDE_HARNESS_OWNED = ["CLAUDE.md", "settings.json", "skills/forge"]
# Project-owned: never touched — listed here as the explicit contract.
# .github/workflows/ is project-owned EXCEPT the harness's own COPY_WORKFLOWS,
# which are refreshed file-by-file below — the rest of the tree (deployment,
# release, etc.) is left exactly as the project has it.
PROJECT_OWNED = [
    "harness.yaml", "AGENTS.md", ".factory/", "plans/", "prototype/",
    "docs/product/", "docs/decisions/", "docs/architecture/", "docs/context/",
    "docs/specs/", "docs/memory/",
    ".github/ (except the harness factory workflows)",
    ".claude/ and .codex/ additions the harness does not ship (project skills, agents, launch.json)",
]
# Preserved across the factory replacement (project evolution state).
PRESERVE_IN_AGENTS = ["factory/skills/proposed", "factory/skills/rejected"]
# Vendoring never ships build noise.
VENDOR_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def _replace_path(src: Path, dst: Path) -> None:
    if dst.is_dir() and not dst.is_symlink():
        shutil.rmtree(dst)
    elif dst.exists() or dst.is_symlink():
        dst.unlink()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, ignore=VENDOR_IGNORE)
    else:
        shutil.copy2(src, dst)


def _keep_path(src: Path, dst: Path) -> None:
    """Copy project-owned state into the temporary preservation tree.

    Symlinks are preserved AS symlinks. Dereferencing would copy the referent's
    bytes into the repo under the link's name — and since retirement then
    deletes the original, a link pointing outside the repo would be silently
    replaced by its target's content."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir() and not src.is_symlink():
        shutil.copytree(src, dst, dirs_exist_ok=True, symlinks=True)
    else:
        shutil.copy2(src, dst, follow_symlinks=False)


def _check_legacy_retirable(target: Path, harness: Path) -> None:
    """Refuse BEFORE anything is written, or the repair cannot be run.

    Validation used to sit next to the delete, after the trees were replaced —
    so refusing left a clean repo dirty, and the "delete it and re-run" the
    message asks for was then rejected by the dirty-target gate above. The
    counterparts are knowable in advance: they are the harness's own factory/
    tree, plus everything under skills/, which survives either because the
    harness ships it or because it is preserved out of .agents/skills/ (the
    one exception, a client skill whose name the harness has since taken, is
    deferred as D-0002)."""
    legacy = target / ".agents"
    if not legacy.is_dir() or legacy.is_symlink():
        return
    missing = []
    for path in sorted(legacy.rglob("*")):
        if not (path.is_file() or path.is_symlink()):
            continue
        # Vendoring never shipped build noise (VENDOR_IGNORE), so a .pyc has no
        # counterpart by construction — counting it would abort the upgrade on
        # every real pre-rename repo, which all carry __pycache__ from having
        # actually run the machinery. Exempt the bytecode itself and nothing
        # else: exempting the whole directory would let anything parked under
        # a __pycache__ name be deleted without ever being recognized.
        if path.suffix == ".pyc":
            continue
        rel = path.relative_to(legacy)
        if rel.parts and rel.parts[0] == "skills":
            continue
        counterpart = harness / "factory" / rel
        if not (counterpart.is_file() or counterpart.is_symlink()):
            missing.append(f".agents/{rel.as_posix()}")
    if missing:
        listing = "\n  ".join(missing[:10])
        more = f"\n  ... and {len(missing) - 10} more" if len(missing) > 10 else ""
        fail(
            f"legacy .agents/ holds {len(missing)} path(s) with no counterpart in the "
            f"vendored factory/ tree, so they cannot be shown to be the machinery "
            f"being replaced:\n  {listing}{more}\n"
            "Nothing was written and nothing under .agents/ was deleted. If this is "
            "retired machinery, delete it and re-run; if it is yours, move it "
            "somewhere the harness does not own."
        )


def _retire_legacy_agents(target: Path) -> bool:
    """Delete only. _check_legacy_retirable already refused anything unknown,
    before the first write."""
    legacy = target / ".agents"
    if not legacy.is_dir() or legacy.is_symlink():
        return False
    shutil.rmtree(legacy)
    return True


def _is_harness_owned(rel: str, harness: Path) -> bool:
    def within(root: str) -> bool:
        return rel == root or rel.startswith(root + "/")

    if any(within(root) for root in UPGRADE_TREES + [".agents"]):
        return True
    if rel in UPGRADE_FILES or rel in COPY_WORKFLOWS:
        return True
    if rel in {dst for _, dst in DOC_CONTRACTS}:
        return True
    if any(within(f".claude/{path}") for path in CLAUDE_HARNESS_OWNED):
        return True
    if rel in {f".codex/{name}" for name in COPY_CODEX}:
        return True
    for sub in ("agents", "skills"):
        shipped = harness / ".codex" / sub
        if shipped.is_dir() and any(
            within(f".codex/{sub}/{child.name}") for child in shipped.iterdir()
        ):
            return True
    return False


def _stale_agents_references(target: Path, harness: Path) -> list[str]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=target, capture_output=True, check=True
    ).stdout.split(b"\0")
    stale = []
    for raw in tracked:
        if not raw:
            continue
        rel = raw.decode("utf-8", errors="surrogateescape")
        if rel.startswith(".factory/history/") or _is_harness_owned(rel, harness):
            continue
        path = target / rel
        try:
            # A symlink's tracked content IS its target text — following it
            # would both miss a link that names .agents/ (broken once the tree
            # is retired) and read whatever it points at, which is exactly the
            # untracked/external content this report must never touch.
            if path.is_symlink():
                if ".agents/" in os.readlink(path):
                    stale.append(rel)
            elif path.is_file() and b".agents/" in path.read_bytes():
                stale.append(rel)
        except OSError:
            continue
    return sorted(stale)


def cmd_upgrade(args: argparse.Namespace) -> None:
    harness = repo_root()
    target = Path(args.target).resolve()
    if not (target / ".git").exists() or not (target / "AGENTS.md").exists():
        fail(f"{target} does not look like a scaffolded repo (.git + AGENTS.md required)")
    if target == harness:
        fail("run upgrade FROM the harness clone TARGETING a client repo, not itself")
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=target, capture_output=True, text=True
    ).stdout.strip()
    if dirty and not args.force:
        fail(
            f"{target} has uncommitted changes. Commit or stash first so the upgrade "
            "is a reviewable diff (--force to override)."
        )
    _check_legacy_retirable(target, harness)

    preserved: dict[str, Path] = {}
    keep_root = Path(tempfile.mkdtemp(prefix="forge-upgrade-keep-"))
    # factory/skills is mixed ownership too: the `skills` CLI installs
    # project skills there (skills-lock.json repos like knacklabs-ats carry
    # a dozen). Preserve every child the harness does not ship, plus the
    # evolution dirs (proposed/rejected — client's version always wins).
    client_skill_dirs: list[str] = []
    target_skills = target / "factory" / "skills"
    legacy_skills = target / ".agents" / "skills"
    harness_skill_names = {p.name for p in (harness / "factory" / "skills").iterdir()} \
        if (harness / "factory" / "skills").is_dir() else set()
    if target_skills.is_dir():
        for child in target_skills.iterdir():
            rel = f"factory/skills/{child.name}"
            if child.name not in harness_skill_names and rel not in PRESERVE_IN_AGENTS:
                client_skill_dirs.append(rel)
    for rel in PRESERVE_IN_AGENTS + client_skill_dirs:
        src = target / rel
        if src.exists():
            dest = keep_root / rel
            _keep_path(src, dest)
            preserved[rel] = dest
    # `is_dir()` follows symlinks: a symlinked skills root would have iterdir()
    # walk an external directory and copy its contents into factory/skills.
    if legacy_skills.is_dir() and not legacy_skills.is_symlink():
        for child in legacy_skills.iterdir():
            rel = f"factory/skills/{child.name}"
            if child.name not in harness_skill_names or rel in PRESERVE_IN_AGENTS:
                dest = keep_root / rel
                _keep_path(child, dest)
                preserved[rel] = dest

    for tree in UPGRADE_TREES:
        src = harness / tree
        if not src.exists():
            continue
        dst = target / tree
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=VENDOR_IGNORE)
    # .claude is mixed ownership: replace only harness-shipped paths; the
    # client's own skills/agents/launch.json survive untouched.
    for rel in CLAUDE_HARNESS_OWNED:
        src = harness / ".claude" / rel
        if src.exists():
            _replace_path(src, target / ".claude" / rel)
    # .github/workflows/ is mixed ownership: refresh only the harness's own
    # factory workflows, file-by-file, so the project's other workflows survive.
    for rel in COPY_WORKFLOWS:
        src = harness / rel
        if src.exists():
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    (target / ".codex").mkdir(exist_ok=True)
    for name in COPY_CODEX:
        shutil.copy2(harness / ".codex" / name, target / ".codex" / name)
    # Same mixed-ownership rule: refresh each harness-shipped agent/skill
    # entry; leave client-added ones alone.
    for sub in ("agents", "skills"):
        src = harness / ".codex" / sub
        if src.is_dir():
            for child in src.iterdir():
                _replace_path(child, target / ".codex" / sub / child.name)
    for name in UPGRADE_FILES:
        src = harness / name
        if src.exists():
            shutil.copy2(src, target / name)
    for src_rel, dst_rel in DOC_CONTRACTS:
        src = harness / src_rel
        if src.exists():
            dst = target / dst_rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    for rel, kept in preserved.items():
        dst = target / rel
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        elif dst.exists() or dst.is_symlink():
            dst.unlink()
        dst.parent.mkdir(parents=True, exist_ok=True)
        # Same symlink rule as _keep_path: a link kept as a link must come back
        # as a link, or the round trip quietly materializes its referent.
        if kept.is_dir() and not kept.is_symlink():
            shutil.copytree(kept, dst, symlinks=True)
        else:
            shutil.copy2(kept, dst, follow_symlinks=False)
    shutil.rmtree(keep_root, ignore_errors=True)

    retired_legacy = _retire_legacy_agents(target)

    # Newer harness additions that older scaffolds predate: create-if-missing /
    # append-if-missing (never overwrite — projects may extend these files).
    ensured: list[str] = []
    if not (target / ".envrc").exists():
        shutil.copy2(harness / ".envrc", target / ".envrc")
        ensured.append(".envrc (run `direnv allow` in the repo)")
    if ensure_jsonl_attributes(target, harness):
        ensured.append(".gitattributes (missing JSONL merge rules added)")
    from .scaffold import ensure_onboarding
    if ensure_onboarding(target, target.name):
        ensured.append("README.md ('Working in this repo' onboarding section appended)")
    gitignore = target / ".gitignore"
    if gitignore.exists() and ".gstack/sessions/" not in gitignore.read_text():
        with gitignore.open("a") as fh:
            fh.write("\n# Project-local gstack store: projects/ committed, machine noise not\n"
                     ".gstack/sessions/\n.gstack/analytics/\n.gstack/cdp-profile/\n"
                     ".gstack/tmp/\n.gstack/.*\n.gstack/**/brain-cache/\n"
                     ".gstack/**/timeline.jsonl\n.gstack/slug-cache/\n")
        ensured.append(".gitignore (gstack entries appended)")
    for rel in PROJECT_STARTERS:
        destination = target / rel
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(harness / rel, destination)
            ensured.append(rel)

    commit = head_sha(harness) or "unknown"
    (target / "constitution" / "VENDORED_FROM").write_text(
        f"symphony-forge @ {commit}\nUpdate by re-vendoring from the harness repo; do not edit in place.\n"
    )
    # Re-freeze the gate surface at the new vendoring (frozen-gate-integrity).
    from check_vendor_integrity import write_manifest
    write_manifest(target, commit)

    drift = ""
    if (harness / "harness.yaml").read_text() != (target / "harness.yaml").read_text():
        drift = ("\nNOTE: harness.yaml differs from the harness default (project-owned, "
                 "left untouched) — diff manually if the phase contract changed upstream.")
    print(f"Upgraded {target} to symphony-forge @ {commit[:8]}")
    print("Replaced (harness-owned): "
          + ", ".join(UPGRADE_TREES + UPGRADE_FILES + COPY_WORKFLOWS) + ", doc contracts")
    if ensured:
        print("Added (missing on this older scaffold): " + ", ".join(ensured))
    print("Untouched (project-owned): " + ", ".join(PROJECT_OWNED) + drift)
    if retired_legacy:
        print("Retired legacy machinery: .agents/")
    stale_references = _stale_agents_references(target, harness)
    if stale_references:
        print("Project-owned files still referencing .agents/:")
        for rel in stale_references:
            print(f"  {rel}")
    else:
        print("Project-owned files still referencing .agents/: none")
    print("Next: review with `git diff`, run `python3 factory/scripts/check_dual_runtime.py` "
          "and the gate tests, then commit.")
