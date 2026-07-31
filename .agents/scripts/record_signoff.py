#!/usr/bin/env python3
"""Establish the project's client sign-off by pinning its decision record in
harness.yaml.

Sign-off happens ONCE for the project — the gate sits between prototype and
planning (WORKFLOW.md), not on every task. So this does not write a per-run
flag; it names the record in committed state and every gate derives the answer
from that. Re-running it on a signed-off project is refused rather than
silently re-pointing the attestation at whatever record happens to be newest.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from factory_lib import parse_frontmatter, repo_root, require_grill, signoff_pin


CLIENT_SIGNOFF_NAME = re.compile(r"^[0-9]{4}-.*client-signoff\.md$")


def pin_into_harness(manifest: Path, relative: str) -> None:
    text = manifest.read_text()
    updated, count = re.subn(
        r"^signoff_record:.*$",
        f'signoff_record: "{relative}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        # A project vendored before this key existed keeps its own harness.yaml
        # through `forge upgrade` (it is project-owned), so the key is simply
        # absent. Add it rather than refusing — otherwise the gate is
        # unreachable in exactly the repos that predate it.
        updated = f'signoff_record: "{relative}"\n' + text
    manifest.write_text(updated)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--record",
        help="Path to the accepted client-signoff decision record. Optional when "
        "exactly one exists; required when there are several.",
    )
    args = parser.parse_args()

    root = repo_root()
    already = signoff_pin(root)
    if already:
        print(
            f"VIOLATION: this project is already signed off ({already}).\n"
            "  Sign-off is a ONE-TIME project gate, so it is never re-recorded per task —\n"
            "  the per-task human gate is plan approval (`forge.py plan save`).\n"
            "  If the pin is genuinely wrong, change harness.yaml in a reviewed PR."
        )
        return 1

    # The handover must be grilled for gaps/contradictions BEFORE it becomes
    # the contract downstream work builds on. Fresh = product docs unchanged
    # since the grill (the sign-off record itself is expected exhaust).
    require_grill(
        root, "signoff",
        ("docs/product/", "docs/decisions/", "prototype/"),
        ignore_names=("client-signoff", "epics-approved"),
    )

    decisions = root / "docs" / "decisions"
    if args.record:
        # An explicit path is still held to the contract: inside this repo's
        # docs/decisions/ and named NNNN-...client-signoff.md. Without this,
        # ANY file carrying `status: accepted` and a `confirmed_by` could be
        # pinned as the project's sign-off, and `../` would persist a traversal
        # into harness.yaml.
        record = (root / args.record).resolve()
        try:
            inside = record.relative_to(decisions.resolve()).parts
        except ValueError:
            inside = ()
        if not record.is_file():
            print(f"VIOLATION: --record {args.record} does not exist.")
            return 1
        if len(inside) != 1 or not CLIENT_SIGNOFF_NAME.match(record.name):
            print(
                f"VIOLATION: --record {args.record} is not a client sign-off record.\n"
                "  Expected docs/decisions/NNNN-<slug>client-signoff.md directly under "
                "this repo's docs/decisions/."
            )
            return 1
    else:
        candidates = sorted(decisions.glob("[0-9][0-9][0-9][0-9]-*client-signoff.md"))
        if not candidates:
            print(
                "VIOLATION: no client sign-off decision record found.\n"
                f"  Expected: {decisions.relative_to(root)}/NNNN-client-signoff.md\n"
                "  Create one with `python3 .agents/scripts/forge.py decision new client-signoff`,\n"
                "  get the client's confirmation, set status: accepted and confirmed_by, then re-run."
            )
            return 1
        if len(candidates) > 1:
            # NEVER guess which one is THE project sign-off. Guessing is the bug
            # this script had: it took the highest-numbered record, whatever task
            # it belonged to, and attested an unrelated human's confirmation.
            listing = "\n".join(f"    {c.relative_to(root)}" for c in candidates)
            print(
                "VIOLATION: several client-signoff records exist; name the project's "
                "one explicitly with --record.\n"
                f"{listing}"
            )
            return 1
        record = candidates[0]

    fields = parse_frontmatter(record.read_text())
    relative = record.relative_to(root).as_posix()
    if fields.get("status") != "accepted":
        print(
            f"VIOLATION: {relative} has status "
            f"'{fields.get('status', 'missing')}', expected 'accepted'.\n"
            "  Set status: accepted once the client has confirmed."
        )
        return 1
    if not fields.get("confirmed_by"):
        print(
            f"VIOLATION: {relative} has empty confirmed_by.\n"
            "  Record WHO confirmed (a human name); agents must not self-confirm —"
            "  an explicit human confirmation in chat authorizes recording it."
        )
        return 1

    pin_into_harness(root / "harness.yaml", relative)
    print(
        f"client sign-off pinned to {relative} in harness.yaml "
        f"(confirmed by {fields['confirmed_by']}).\n"
        "Commit harness.yaml — every gate reads the pin from committed state."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
