"""forge board — read-only localhost lifecycle dashboard."""
from __future__ import annotations

import argparse
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from factory_lib import load_json, now_iso, repo_root

from .plans import parse_frontmatter
from .quickfix import load_active
from .roadmap import load_roadmap, ready_pending
from .signal import open_signals
from .specs import spec_records


def _plan_records(base: Path, location: str) -> list[dict]:
    records = []
    for path in sorted((base / "plans" / location).glob("*.md")):
        fields, _ = parse_frontmatter(path.read_text())
        records.append({
            **fields,
            "path": path.relative_to(base).as_posix(),
            "location": location,
        })
    return records


def _stage_summary(base: Path) -> dict:
    data = load_json(base / ".factory" / "stages.json", default={})
    items = data.get("stages", [])
    return {
        "issue": data.get("issue"),
        "done": sum(1 for stage in items if stage.get("status") == "done"),
        "total": len(items),
        "items": items,
    }


def _plan_evidence(base: Path, plan: dict | None) -> tuple[dict | None, dict]:
    empty_reviews = {aspect: False for aspect in ("quality", "performance", "security")}
    if not plan:
        return None, {"verify": False, "tests": False, "reviews": empty_reviews}
    if plan.get("location") == "completed":
        root = base / ".factory" / "history" / str(plan.get("issue", ""))
    else:
        root = base / ".factory"
    stages_data = load_json(root / "stages.json", default={})
    stages = stages_data.get("stages", [])
    progress = None
    if stages:
        progress = {
            "done": sum(1 for stage in stages if stage.get("status") == "done"),
            "total": len(stages),
        }
    evidence = {
        "verify": load_json(root / "verify.json", default={}).get("ok") is True,
        "tests": (root / "tests.json").is_file(),
        "reviews": {
            aspect: (root / "reviews" / f"{aspect}.json").is_file()
            for aspect in ("quality", "performance", "security")
        },
    }
    return progress, evidence


def aggregate_state(base: Path) -> dict:
    roadmap = load_roadmap(base)
    items = roadmap.get("items", [])
    ready, _ = ready_pending(items)
    frontier = [item["key"] for item in ready]
    plans = {
        "active": _plan_records(base, "active"),
        "completed": _plan_records(base, "completed"),
    }
    plan_by_story = {
        plan.get("story"): plan
        for location in ("completed", "active")
        for plan in plans[location]
        if plan.get("story")
    }
    specs = [
        {key: value for key, value in record.items() if key != "_path"}
        for record in spec_records(base)
    ]
    spec_status = {record["path"]: record.get("status", "draft") for record in specs}
    run = load_json(base / ".factory" / "run.json", default={})
    stages = _stage_summary(base)
    stories = []
    for item in items:
        story = dict(item)
        plan = plan_by_story.get(item.get("key"))
        progress, evidence = _plan_evidence(base, plan)
        story["ready_to_plan"] = item.get("key") in frontier
        story["plan"] = plan
        story["lifecycle"] = {
            "spec": spec_status.get(item.get("spec"), "missing"),
            "roadmap": True,
            "planned": plan is not None,
            "stages": progress,
            "verify": evidence["verify"],
            "tests": evidence["tests"],
            "reviews": evidence["reviews"],
            "shipped": item.get("status") == "done",
        }
        stories.append(story)
    return {
        "generated_at": now_iso(),
        "specs": specs,
        "epics": roadmap.get("epics", []),
        "stories": stories,
        "frontier": frontier,
        "plans": plans,
        "run": {
            key: run.get(key)
            for key in ("issue_key", "phase", "plan_status", "decomposition_status",
                        "plan_file", "story")
        },
        "stages": stages,
        "signals": open_signals(base),
        "quickfix": load_active(base) or None,
    }


def make_server(base: Path, port: int) -> ThreadingHTTPServer:
    root = base.resolve()

    class BoardHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
            route = urlsplit(self.path).path
            if route == "/api/state":
                body = json.dumps(aggregate_state(root)).encode()
                content_type = "application/json; charset=utf-8"
                status = 200
            elif route == "/":
                body = (root / "factory" / "board" / "index.html").read_bytes()
                content_type = "text/html; charset=utf-8"
                status = 200
            else:
                body = b"Not found\n"
                content_type = "text/plain; charset=utf-8"
                status = 404
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    # ponytail: stdlib server + polling, no websockets/framework — upgrade
    # only if multiple simultaneous viewers ever matter.
    return ThreadingHTTPServer(("127.0.0.1", port), BoardHandler)


def cmd_board(args: argparse.Namespace) -> None:
    base = Path(args.repo).resolve() if args.repo else repo_root()
    server = make_server(base, args.port)
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"Lifecycle board: {url} (Ctrl+C to stop)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBoard stopped.")
    finally:
        server.server_close()
