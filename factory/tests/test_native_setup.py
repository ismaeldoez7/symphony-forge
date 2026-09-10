"""Codex-only readiness and dual-adapter scaffold regression coverage."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

import pytest

from test_gates import HARNESS, adopt, existing_repo, git, repo, run  # noqa: F401


def _hook(event: str, source, *, enabled=True, trust="trusted") -> dict:
    from forge_cli.doctor import CODEX_HOOK_CONTRACT

    hook = {
        "eventName": event,
        "sourcePath": str(source),
        "enabled": enabled,
        "trustStatus": trust,
        "command": f"sh -c 'forge{CODEX_HOOK_CONTRACT[event]}'",
        "currentHash": "sha256:trusted-by-codex",
    }
    if event == "preToolUse":
        hook["matcher"] = (
            "Bash|apply_patch|Edit|Write|request_user_input|request_user_input_async"
        )
    elif event == "postToolUse":
        hook["matcher"] = "^request_user_input$"
    elif event == "sessionStart":
        hook["matcher"] = "startup|resume|clear|compact"
    return hook


def test_codex_hook_readiness_requires_exact_enabled_trusted_source(
        tmp_path, monkeypatch):
    from forge_cli import doctor

    config = tmp_path / ".codex" / "hooks.json"
    config.parent.mkdir()
    config.write_text('{"hooks": {}}\n')
    valid = [_hook(event, config) for event in doctor.CODEX_HOOK_EVENTS]
    monkeypatch.setattr(doctor.shutil, "which", lambda name: f"/tools/{name}")
    monkeypatch.setattr(doctor, "_git_worktree_roots", lambda _base: ({tmp_path}, ""))
    monkeypatch.setattr(
        doctor, "_codex_hooks_inventory", lambda _binary, _base: (valid, ""))

    ok, detail = doctor.codex_hook_readiness(tmp_path)
    assert ok and "PATH-based CLI probe does not certify Codex Desktop" in detail

    for matcher in ("*", "", None):
        match_all = [dict(hook) for hook in valid]
        for hook in match_all:
            if hook["eventName"] not in {"preToolUse", "postToolUse", "sessionStart"}:
                continue
            if matcher is None:
                hook.pop("matcher", None)
            else:
                hook["matcher"] = matcher
        monkeypatch.setattr(
            doctor, "_codex_hooks_inventory",
            lambda _binary, _base, hooks=match_all: (hooks, ""),
        )
        assert doctor.codex_hook_readiness(tmp_path)[0]

    for hooks, expected in (
        ([], "did not load hooks from"),
        ([*valid[:-1], _hook("stop", config, trust="untrusted")], "not trusted"),
        ([*valid[:-1], _hook("stop", config, enabled=False)], "disabled"),
        (valid[:-1], "required hooks"),
        ([_hook(event, tmp_path / "other.json") for event in doctor.CODEX_HOOK_EVENTS],
         "did not load hooks from"),
    ):
        monkeypatch.setattr(
            doctor, "_codex_hooks_inventory",
            lambda _binary, _base, hooks=hooks: (hooks, ""),
        )
        assert expected in doctor.codex_hook_readiness(tmp_path)[1]

    wrong = [dict(hook) for hook in valid]
    wrong[0]["command"] = "sh -c 'forge hook unrelated'"
    monkeypatch.setattr(
        doctor, "_codex_hooks_inventory", lambda _binary, _base: (wrong, ""))
    assert "wrong hook command" in doctor.codex_hook_readiness(tmp_path)[1]

    wrong = [dict(hook) for hook in valid]
    next(hook for hook in wrong if hook["eventName"] == "preToolUse")["matcher"] = "Bash"
    monkeypatch.setattr(
        doctor, "_codex_hooks_inventory", lambda _binary, _base: (wrong, ""))
    assert "PreToolUse matcher" in doctor.codex_hook_readiness(tmp_path)[1]

    malformed = [dict(hook) for hook in valid]
    next(hook for hook in malformed if hook["eventName"] == "preToolUse")["matcher"] = "["
    monkeypatch.setattr(
        doctor, "_codex_hooks_inventory", lambda _binary, _base: (malformed, ""))
    assert "matcher is invalid" in doctor.codex_hook_readiness(tmp_path)[1]

    sources = doctor.CODEX_SESSION_START_SOURCES
    for missing in sources:
        incomplete = [dict(hook) for hook in valid]
        next(hook for hook in incomplete
             if hook["eventName"] == "sessionStart")["matcher"] = "|".join(
                 source for source in sources if source != missing)
        monkeypatch.setattr(
            doctor, "_codex_hooks_inventory",
            lambda _binary, _base, hooks=incomplete: (hooks, ""),
        )
        detail = doctor.codex_hook_readiness(tmp_path)[1]
        assert "SessionStart matcher" in detail and missing in detail


def test_codex_hook_readiness_accepts_only_identical_inherited_worktree_hooks(
        tmp_path, monkeypatch):
    from forge_cli import doctor

    main = tmp_path / "main"
    linked = tmp_path / "linked"
    subprocess.run(["git", "init", "-q", str(main)], check=True)
    subprocess.run(["git", "config", "user.email", "forge@example.invalid"], cwd=main, check=True)
    subprocess.run(["git", "config", "user.name", "Forge Tests"], cwd=main, check=True)
    config = main / ".codex" / "hooks.json"
    config.parent.mkdir()
    config.write_text('{"hooks": {"fixture": true}}\n')
    subprocess.run(["git", "add", "."], cwd=main, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "hooks"], cwd=main, check=True)
    subprocess.run(["git", "worktree", "add", "-q", "-b", "linked", str(linked)],
                   cwd=main, check=True)
    inherited = [_hook(event, config) for event in doctor.CODEX_HOOK_EVENTS]
    monkeypatch.setattr(doctor.shutil, "which", lambda name: f"/tools/{name}")
    monkeypatch.setattr(
        doctor, "_codex_hooks_inventory", lambda _binary, _base: (inherited, ""))

    assert doctor.codex_hook_readiness(linked)[0]

    config.write_text('{"hooks": {"fixture": "diverged"}}\n')
    ok, detail = doctor.codex_hook_readiness(linked)
    assert not ok and "inherited divergent hooks" in detail


SESSION_START_ADAPTERS = (".codex/hooks.json", ".claude/settings.json")
SESSION_START_SOURCES = ("startup", "resume", "clear", "compact")


def _remove_session_start_source(config, missing):
    document = json.loads(config.read_text(encoding="utf-8"))
    document["hooks"]["SessionStart"][0]["matcher"] = "|".join(
        source for source in SESSION_START_SOURCES if source != missing)
    config.write_text(json.dumps(document), encoding="utf-8")


@pytest.mark.parametrize("adapter", SESSION_START_ADAPTERS)
def test_dual_runtime_checker_accepts_session_start_match_all(repo, adapter):
    config = repo / adapter
    document = json.loads(config.read_text(encoding="utf-8"))
    document["hooks"]["SessionStart"][0]["matcher"] = "*"
    config.write_text(json.dumps(document), encoding="utf-8")

    code, out = run(repo, "check_dual_runtime.py", str(repo))

    assert code == 0, out


@pytest.mark.parametrize("adapter", SESSION_START_ADAPTERS)
@pytest.mark.parametrize("missing", SESSION_START_SOURCES)
def test_dual_runtime_checker_requires_each_session_start_source(
        repo, adapter, missing):
    _remove_session_start_source(repo / adapter, missing)

    code, out = run(repo, "check_dual_runtime.py", str(repo))

    assert code != 0 and f"missing: {missing}" in out


@pytest.mark.parametrize("missing", SESSION_START_SOURCES)
def test_dual_runtime_checker_rejects_session_start_omission_in_both_adapters(
        repo, missing):
    for adapter in SESSION_START_ADAPTERS:
        _remove_session_start_source(repo / adapter, missing)

    code, out = run(repo, "check_dual_runtime.py", str(repo))

    assert code != 0
    assert out.count(f"missing: {missing}") == 2

