#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shlex
from pathlib import Path

from factory_lib import load_json, read_hook_input, repo_root, run_state_path
from forge_cli.quickfix import claim_files, load_active

payload = read_hook_input()
tool_name = payload.get("tool_name", "")
tool_input = payload.get("tool_input") or {}
command = (tool_input.get("command") or "").strip()
permission_mode = payload.get("permission_mode", "")


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    raise SystemExit(0)


# Planning lock: product writes are always refused until a plan is approved
# or a bounded quickfix is open. Planning surfaces stay available.
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
PLANNING_WRITE_OK = (
    "plans/", "docs/", ".factory/", "factory/", ".claude/", ".codex/",
    ".gstack/", ".github/", "constitution/", "harness/", "prototype/",
)
PLANNING_WRITE_OK_FILES = {
    "AGENTS.md", "CLAUDE.md", "WORKFLOW.md", "harness.yaml", "README.md",
    ".gitignore", ".gitattributes", ".envrc",
}
PLAN_MODE_MSG = (
    "Planning lock is armed — product writes require an approved plan. "
    "Either enter plan mode (shift+tab) [PLAN MODE] and save the approved plan per "
    "factory/prompts/planner.md, or run `./forge quickfix start \"<reason>\"` "
    "for a bounded five-file fix."
)
QUICKFIX_LIMIT_MSG = (
    "Quickfix scope exceeded — this is not a quickfix, enter plan mode (shift+tab). "
    "The other planning-lock exit is `./forge quickfix start \"<reason>\"`, but the "
    "current window must be closed first."
)
OPAQUE_WRITE_MSG = (
    "Opaque delegated writes cannot use a quickfix because its five-file budget "
    "cannot be tracked. Either enter plan mode (shift+tab) [PLAN MODE] and save an "
    "approved plan, or use `./forge quickfix start \"<reason>\"` for direct edits "
    "whose product paths the hook can record."
)


def planning_locked(state: dict, quickfix: dict) -> bool:
    return state.get("plan_status") != "approved" and not quickfix


def product_path(raw: str, root: Path) -> str | None:
    """Return a canonical repo-relative product path, otherwise None."""
    value = raw.strip().strip("\"'")
    if not value or value in {"-", "/dev/null"}:
        return None
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        rel = resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    if not rel or rel in PLANNING_WRITE_OK_FILES:
        return None
    if any(rel == prefix.rstrip("/") or rel.startswith(prefix)
           for prefix in PLANNING_WRITE_OK):
        return None
    return rel


def bash_write_paths(value: str) -> list[str]:
    """Extract likely write targets from a shell command.

    # ponytail: heuristic, defends drift not adversaries — tighten patterns
    # if a real bypass shows up.
    """
    found: list[str] = []
    redirect = re.compile(
        r"(?<![<>])>{1,2}(?![>&])\s*(\"[^\"]+\"|'[^']+'|[^\s;&|]+)"
    )
    found.extend(match.group(1) for match in redirect.finditer(value))
    for segment in re.split(r"[;&|]+", value):
        try:
            tokens = shlex.split(segment)
        except ValueError:
            continue
        command_index = next(
            (index for index, token in enumerate(tokens)
             if token.rsplit("/", 1)[-1] in {"tee", "sed", "cp", "mv", "touch"}),
            None,
        )
        if command_index is None:
            continue
        command_name = tokens[command_index].rsplit("/", 1)[-1]
        args = tokens[command_index + 1:]
        operands = [token for token in args
                    if not token.startswith("-") and token not in {">", ">>"}]
        if command_name == "tee":
            found.extend(operands)
        elif command_name == "touch":
            found.extend(operands)
        elif command_name == "cp" and operands:
            found.append(operands[-1])
        elif command_name == "mv":
            found.extend(operands)
        elif command_name == "sed" and any(
            token == "-i" or token.startswith("-i") or token.startswith("--in-place")
            for token in args
        ) and operands:
            found.append(operands[-1])
    return found


def guard_product_writes(targets: list[str], state: dict, root: Path) -> None:
    product = list(dict.fromkeys(
        rel for raw in targets if (rel := product_path(raw, root)) is not None
    ))
    if not product or state.get("plan_status") == "approved":
        return
    quickfix = load_active(root)
    if not quickfix:
        deny(PLAN_MODE_MSG)
    claimed, _ = claim_files(root, product)
    if not claimed:
        deny(QUICKFIX_LIMIT_MSG)


blocked = [
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+push\s+--force\b",
    r"\bterraform\s+destroy\b",
    r"\bkubectl\s+delete\b",
]
for pattern in blocked:
    if re.search(pattern, command):
        deny(f"Blocked by factory policy: {command}")

# Raw `codex exec` bypasses the sanctioned runtime (/codex:rescue -> the
# plugin companion): no session threading, no background management, no
# repo-pinned invocation shape. There is NO escape hatch — doctor installs
# codex-plugin-cc as a required tool; if it breaks, repair it or work in a
# Codex session directly (docs/degraded-mode.md).
# Match INVOCATIONS (command position, env prefixes, pipeline segments,
# command substitution) — not prose in heredocs/echo that mentions the phrase.
# `codex [global flags] exec` counts too — flags between must not bypass.
CODEX_EXEC_INVOCATION = re.compile(
    r"(?:^|[;&|]\s*|\$\(\s*)(?:\w+=\S+\s+)*codex(?:\s+-{1,2}[\w-]+(?:[= ]\S+)?)*\s+exec\b",
    re.MULTILINE,
)
if CODEX_EXEC_INVOCATION.search(command):
    deny(
        "Direct `codex exec` is off-contract — invoke Codex through the plugin: "
        "/codex:rescue [--background] [--write] [--model <m>] [--effort <e>] \"<task>\" "
        "(read-only unless --write). Plugin missing or broken? `./forge doctor --fix` "
        "reinstalls it; meanwhile work in a Codex session directly "
        "(docs/degraded-mode.md) — same prompts, same artifacts, same gates."
    )

check_bypass = ["pnpm test", "pnpm lint", "pnpm typecheck", "pnpm check:all"]
if any(token in command for token in check_bypass) and "factory/scripts/verify.py" not in command:
    deny(
        "Use `python3 factory/scripts/verify.py` so verification artifacts stay deterministic."
    )

# Sign-off gate: heavy factory phases cannot start before client sign-off.
# Discovery/prototype phases and record_signoff.py itself stay allowed.
PHASE_ADVANCING = (
    "record_decomposition_from_json.py",
    "pr_ready.py",
)
GATED_PHASES = (
    "planning",
    "decomposing",
    "awaiting-approval",
    "implementing",
    "testing",
    "reviewing",
    "functional-check",
    "pr-ready",
)
root = repo_root()
run_state = load_json(run_state_path(root), default={})

if permission_mode != "plan":
    if tool_name in EDIT_TOOLS:
        target = (tool_input.get("file_path") or tool_input.get("notebook_path") or "")
        if target:
            guard_product_writes([target], run_state, root)
    if tool_name == "Bash":
        guard_product_writes(bash_write_paths(command), run_state, root)
    if tool_name == "Bash" and run_state.get("plan_status") != "approved" \
            and "codex-companion.mjs" in command \
            and " task" in command and "--write" in command:
        # Opaque delegation cannot prove that a quickfix stayed inside its budget.
        deny(OPAQUE_WRITE_MSG)

if run_state and not run_state.get("client_signoff"):
    advancing = any(script in command for script in PHASE_ADVANCING)
    if "update_run.py" in command and "--phase" in command:
        advancing = advancing or any(phase in command for phase in GATED_PHASES)
    if advancing:
        deny(
            "Client sign-off not recorded. Get docs/decisions/NNNN-client-signoff.md "
            "accepted (non-empty confirmed_by), then run "
            "`python3 factory/scripts/record_signoff.py` before advancing the phase."
        )

print(json.dumps({}))
