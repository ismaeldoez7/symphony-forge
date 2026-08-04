"""forge upgrade — re-vendor harness machinery into an existing client repo.

Run FROM the harness clone, targeting the client repo (mirrors `forge init`).
Replaces machinery the harness owns; never touches project-owned content.
"""
from __future__ import annotations

import argparse
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
    # Refuse a symlinked ROOT, do not just decline to retire it: every later
    # step reaches through it. `.agents/skills` resolves past the link, so
    # iterdir() would walk an external directory and copy its contents into
    # factory/skills — importing files from outside the repository entirely.
    if legacy.is_symlink():
        fail(
            ".agents is a symlink. The upgrade would migrate skills by reading "
            "through it, pulling content from outside the repository into "
            "factory/skills, and retiring it would drop the link rather than the "
            "machinery. Replace it with a real directory (or remove it) and "
            "re-run. Nothing was written."
        )
    if not legacy.is_dir():
        return
    # A symlinked skills root cannot be traversed (iterdir() would walk the
    # referent) and cannot be merged into the real factory/skills without a
    # policy for it — and retirement would then delete the link, silently
    # dropping every client skill it stood for. Refuse the topology instead.
    if (legacy / "skills").is_symlink():
        fail(
            ".agents/skills is a symlink. The upgrade cannot migrate client skills "
            "through it without dereferencing content that lives outside the "
            "machinery tree, and retiring .agents/ would drop the link. Replace it "
            "with a real directory (or move it out of .agents/) and re-run."
        )
    # A legacy skills entry whose name the harness also ships is treated as the
    # machinery being replaced. That cannot be decided from the paths: an older
    # harness's copy of a skill differs from the current one exactly the way a
    # client's would, and the harness ships factory/skills/forge.md, so
    # refusing every collision would refuse every upgrade. It is not silent
    # either — upgrade refuses a dirty tree, so the replacement lands as a
    # reviewed deletion in the upgrade diff. Conflict policy is D-0002.
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


def _indexed_symlinks_naming_legacy(target: Path) -> list[str]:
    """Symlinks whose target names the retired tree.

    `git grep` skips symlink entries, but a symlink's blob IS its target text —
    and a link into .agents/ breaks exactly like a mention of it does. Read the
    blob from the index rather than the working tree, so no link is ever
    followed and no ancestor can redirect the read out of the repository.
    """
    listing = subprocess.run(
        ["git", "ls-files", "-s", "-z"], cwd=target, capture_output=True)
    if listing.returncode != 0:
        return []
    found = []
    for raw in listing.stdout.split(b"\0"):
        metadata, _, rel = raw.partition(b"\t")
        fields = metadata.split()
        if not rel or len(fields) < 2 or fields[0] != b"120000":
            continue
        blob = subprocess.run(
            ["git", "cat-file", "blob", fields[1].decode()],
            cwd=target, capture_output=True)
        if blob.returncode != 0:
            continue
        link = blob.stdout.decode("utf-8", errors="replace")
        # Whole path component: `legacy-tools -> .agents` has no trailing slash.
        if ".agents" in link.split("/"):
            found.append(rel.decode("utf-8", errors="surrogateescape"))
    return found


def _stale_agents_references(
    target: Path, harness: Path, migrated: list[str] | None = None,
    from_legacy: set[str] | None = None,
) -> list[str]:
    """Project-owned files that still name the retired tree.

    Searched in the INDEX, never through the working tree. Git streams blob
    content and resolves paths itself, so this cannot follow a symlink (at the
    leaf or at any ancestor) out of the repository, cannot wander into an
    ignored node_modules/ or dist/, and cannot allocate a whole large file to
    look for a short marker. A symlink's blob is its target text, so a link
    that merely NAMES .agents is matched like any other content.
    """
    search = subprocess.run(
        ["git", "grep", "-l", "--cached", "-I", "-z", "-F", "-e", ".agents", "--"],
        cwd=target, capture_output=True,
    )
    # 0 = matches, 1 = none. Anything else is a real failure, but this report
    # is advisory and runs after the migration; it must never abort the upgrade.
    if search.returncode not in (0, 1):
        return []
    hits = [
        raw.decode("utf-8", errors="surrogateescape")
        for raw in search.stdout.split(b"\0") if raw
    ]
    hits.extend(_indexed_symlinks_naming_legacy(target))
    # Client skills carried out of .agents/skills/ land at factory/skills/<name>,
    # untracked until the human stages the upgrade. Their INDEXED source is the
    # .agents/skills/ path, so translate the hit to where the file now lives
    # rather than walking the freshly copied tree.
    # ONLY names actually carried out of the legacy tree. A name preserved from
    # the CURRENT location had its legacy twin deliberately skipped (the
    # current location wins), so translating that discarded copy's hits would
    # name a current file that has no stale reference — or none at all.
    carried = from_legacy or set()
    # A client skill ALREADY at factory/skills/<name> is preserved, not
    # replaced — so it is project-owned even though _is_harness_owned sees it
    # inside an UPGRADE_TREES entry and would otherwise discard it. Match the
    # path itself as well as its descendants: a skill can be a single file
    # (factory/skills/client.md) or a symlink, preserved at that exact path.
    owned = set(migrated or [])
    preserved = tuple(f"{rel}/" for rel in owned)
    stale = set()
    for rel in hits:
        if rel.startswith(".factory/history/"):
            continue
        parts = rel.split("/")
        if parts[0] == ".agents":
            if len(parts) > 2 and parts[1] == "skills" and parts[2] in carried:
                stale.add("factory/skills/" + "/".join(parts[2:]))
            continue
        if rel not in owned and not rel.startswith(preserved) \
                and _is_harness_owned(rel, harness):
            continue
        stale.add(rel)
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
    carried_from_legacy: set[str] = set()
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
        # exists() is False for a DANGLING symlink, and a client skill can
        # legitimately be one. Without the is_symlink() arm it is never
        # preserved, so replacing factory/ deletes project-owned content.
        if src.exists() or src.is_symlink():
            dest = keep_root / rel
            _keep_path(src, dest)
            preserved[rel] = dest
    # `is_dir()` follows symlinks: a symlinked skills root would have iterdir()
    # walk an external directory and copy its contents into factory/skills.
    if legacy_skills.is_dir() and not legacy_skills.is_symlink():
        for child in legacy_skills.iterdir():
            rel = f"factory/skills/{child.name}"
            # The current location wins when a name exists in BOTH. Copying the
            # legacy one on top would merge into whatever the first copy left
            # at that destination — and if that was a symlink, through it.
            if rel in preserved:
                continue
            if child.name not in harness_skill_names or rel in PRESERVE_IN_AGENTS:
                dest = keep_root / rel
                _keep_path(child, dest)
                preserved[rel] = dest
                carried_from_legacy.add(child.name)

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
    stale_references = _stale_agents_references(
        target, harness, sorted(preserved), carried_from_legacy)
    # The scan reads the index, which equals the working tree only because the
    # dirty-target gate held. --force bypasses that gate, so uncommitted edits
    # and untracked files are outside what was searched — say so rather than
    # printing a definitive answer the scan cannot support.
    caveat = " (index only — --force skipped the clean-tree check, so uncommitted " \
             "and untracked files were not searched)" if args.force else ""
    if stale_references:
        print(f"Project-owned files still referencing .agents/{caveat}:")
        for rel in stale_references:
            print(f"  {rel}")
    else:
        print(f"Project-owned files still referencing .agents/: none{caveat}")
    print("Next: review with `git diff`, run `python3 factory/scripts/check_dual_runtime.py` "
          "and the gate tests, then commit.")
