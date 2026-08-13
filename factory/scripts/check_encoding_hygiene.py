#!/usr/bin/env python3
"""Enforce explicit UTF-8 at every text I/O boundary in factory scripts."""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "factory" / "scripts"

# These byte/lossless paths are intentional and must not be converted to
# replacement-decoded text.  The scanner already ignores binary modes; this
# inventory makes the review-sensitive exceptions explicit and auditable.
BYTE_PATH_ALLOWLIST = (
    "factory/scripts/check_dual_runtime.py:99-108 copy detection",
    "factory/scripts/check_vendor_integrity.py SHA-256 reads",
    "factory/scripts/factory_lib.py sha256_of and fd-based safe writers",
    "factory/scripts/forge_cli/context.py normalized-byte hashing",
    "factory/scripts/forge_cli/gstack.py:125 byte equality",
    "factory/scripts/forge_cli/stages.py:252-265,551-564 measurement digests",
    "factory/scripts/forge_cli/upgrade.py:159,314,324,355 NUL/surrogateescape paths",
    "factory/scripts/forge_cli/delegate.py:150-166,977-1001 ledger and brief digests",
    "factory/scripts/forge_cli/review_brief.py:80-86 review-brief bytes",
    "factory/scripts/forge_cli/board.py:559-577 HTTP payload bytes",
    "factory/scripts/forge_cli/doctor.py:283,983-990 byte-mode/downloaded executables",
    "factory/scripts/forge_cli/plans.py:70-71 plan digests",
    "factory/scripts/forge_cli/signal.py:61-67 identity hashes",
    "factory/scripts/forge_cli/quickfix.py:99-105 identity hashes",
    "factory/scripts/check_agents_hygiene.py:18-22 UTF-8 byte budget",
    "factory/scripts/pr_ready.py:348 byte-mode freshness paths",
)

# Filled with exact file:line call sites after the sweep.  Only diagnostics,
# console reconfiguration, and worker-log read-back belong here.
REPLACE_ALLOWLIST: frozenset[str] = frozenset({
    "factory/scripts/check_agents_hygiene.py:9",
    "factory/scripts/check_dual_runtime.py:19",
    "factory/scripts/check_factory_scaffold.py:9",
    "factory/scripts/check_repo_budget.py:19",
    "factory/scripts/factory_lib.py:25",
    "factory/scripts/factory_lib.py:1054",
    "factory/scripts/forge_cli/common.py:19",
    "factory/scripts/forge_cli/delegate.py:1055",
    "factory/scripts/forge_cli/delegate.py:1058",
    "factory/scripts/forge_cli/doctor.py:63",
    "factory/scripts/forge_cli/doctor.py:412",
    "factory/scripts/forge_cli/doctor.py:472",
    "factory/scripts/forge_cli/doctor.py:593",
    "factory/scripts/forge_cli/doctor.py:655",
    "factory/scripts/forge_cli/doctor.py:664",
    "factory/scripts/forge_cli/doctor.py:813",
    "factory/scripts/forge_cli/stages.py:856",
    "factory/scripts/forge_cli/stages.py:858",
    "factory/scripts/forge_cli/stages.py:950",
    "factory/scripts/forge_cli/stages.py:952",
})


@dataclass(frozen=True)
class Violation:
    path: Path
    line: int
    rule: str
    message: str

    def render(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root)
        except ValueError:
            display = self.path
        return f"{display}:{self.line}: {self.rule}: {self.message}"


def _literal_keyword(call: ast.Call, name: str) -> object:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            return keyword.value.value
    return None


def _has_keyword(call: ast.Call, name: str) -> bool:
    return any(keyword.arg == name for keyword in call.keywords)


def _call_name(call: ast.Call) -> str:
    parts: list[str] = []
    node: ast.expr = call.func
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def _mode(call: ast.Call, *, path_method: bool = False) -> object:
    keyword_mode = _literal_keyword(call, "mode")
    if keyword_mode is not None:
        return keyword_mode
    index = 0 if path_method else 1
    if len(call.args) > index and isinstance(call.args[index], ast.Constant):
        return call.args[index].value
    return None


def _is_text_open(call: ast.Call, name: str) -> bool:
    if name in {"tempfile.TemporaryFile", "tempfile.NamedTemporaryFile"}:
        mode = _mode(call)
        return isinstance(mode, str) and "b" not in mode
    if isinstance(call.func, ast.Name) and call.func.id == "open":
        mode = _mode(call)
    elif name == "io.open":
        mode = _mode(call)
    elif (
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "open"
        and not name.startswith(("os.", "webbrowser."))
    ):
        mode = _mode(call, path_method=True)
    else:
        return False
    return not (isinstance(mode, str) and "b" in mode)


def _is_subprocess_text(call: ast.Call, name: str) -> bool:
    if name not in {
        "subprocess.run",
        "subprocess.Popen",
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
    }:
        return False
    text_mode = (
        _literal_keyword(call, "text") is True
        or _literal_keyword(call, "universal_newlines") is True
        or _has_keyword(call, "encoding")
        or _has_keyword(call, "errors")
    )
    if not text_mode:
        return False
    if name == "subprocess.check_output":
        return True
    if _literal_keyword(call, "capture_output") is True:
        return True
    return any(
        keyword.arg in {"stdout", "stderr"}
        and isinstance(keyword.value, ast.Attribute)
        and isinstance(keyword.value.value, ast.Name)
        and keyword.value.value.id == "subprocess"
        and keyword.value.attr == "PIPE"
        for keyword in call.keywords
    )


def _is_sys_stdin(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "sys"
        and node.attr == "stdin"
    )


def _strict_stdin_wrapper(call: ast.Call, name: str) -> bool:
    if name not in {"io.TextIOWrapper", "TextIOWrapper"} or not call.args:
        return False
    source = call.args[0]
    return (
        isinstance(source, ast.Attribute)
        and source.attr == "buffer"
        and _is_sys_stdin(source.value)
        and _literal_keyword(call, "encoding") == "utf-8"
        and _literal_keyword(call, "errors") in {None, "strict"}
    )


def check_file(
    path: Path,
    *,
    root: Path = ROOT,
    replace_allowlist: frozenset[str] = REPLACE_ALLOWLIST,
) -> list[Violation]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        return [Violation(path, getattr(exc, "lineno", 1) or 1, "parse", str(exc))]

    subprocess_aliases = {"subprocess": "subprocess"}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess":
                    subprocess_aliases[alias.asname or alias.name] = "subprocess"
        elif isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            for alias in node.names:
                subprocess_aliases[alias.asname or alias.name] = (
                    f"subprocess.{alias.name}"
                )

    violations: list[Violation] = []
    wrapped_stdin_nodes: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        head, separator, tail = name.partition(".")
        if head in subprocess_aliases:
            name = subprocess_aliases[head] + (separator + tail if separator else "")
        if _strict_stdin_wrapper(node, name):
            wrapped_stdin_nodes.add(id(node.args[0].value))

        if _is_subprocess_text(node, name):
            encoding = _literal_keyword(node, "encoding")
            if encoding != "utf-8":
                violations.append(Violation(
                    path, node.lineno, "subprocess-text",
                    "text capture requires literal encoding='utf-8'",
                ))

        is_path_text = (
            isinstance(node.func, ast.Attribute)
            and node.func.attr in {"read_text", "write_text"}
        )
        if is_path_text or _is_text_open(node, name):
            encoding = _literal_keyword(node, "encoding")
            if encoding != "utf-8":
                violations.append(Violation(
                    path, node.lineno, "text-file",
                    "text file I/O requires literal encoding='utf-8'",
                ))

        if _literal_keyword(node, "errors") == "replace":
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError:
                relative = path.as_posix()
            site = f"{relative}:{node.lineno}"
            if site not in replace_allowlist:
                violations.append(Violation(
                    path, node.lineno, "replace-policy",
                    "errors='replace' is not allowlisted at this file:line",
                ))

    for node in ast.walk(tree):
        if _is_sys_stdin(node) and id(node) not in wrapped_stdin_nodes:
            violations.append(Violation(
                path, node.lineno, "stdin",
                "sys.stdin must be read through a strict UTF-8 TextIOWrapper",
            ))
    return violations


def check_paths(
    paths: Iterable[Path],
    *,
    root: Path = ROOT,
    replace_allowlist: frozenset[str] = REPLACE_ALLOWLIST,
) -> list[Violation]:
    violations: list[Violation] = []
    for path in sorted(paths):
        violations.extend(check_file(
            path, root=root, replace_allowlist=replace_allowlist
        ))
    return violations


def main() -> int:
    paths = (
        path for path in SCRIPTS.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    violations = check_paths(paths)
    if violations:
        for violation in violations:
            print(violation.render(ROOT))
        print(f"encoding hygiene: FAIL ({len(violations)} violation(s))")
        return 1
    print("encoding hygiene: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
