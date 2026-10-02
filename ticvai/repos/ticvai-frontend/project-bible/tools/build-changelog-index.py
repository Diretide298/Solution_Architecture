#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write changes/CHANGELOG.md, the index of the change log, from changes/entries/*.yaml.

**Generated, not authored** (council of 2 October 2026; `changes/README.md`). The entries are one file per
change so parallel branches never conflict; an index edited by hand on two branches would be the
conflict the directory avoids. So the index is derived at the refresh, never committed from a branch,
and `tools/check-changelog.py` notes when it is stale.

    python3 tools/build-changelog-index.py
"""
from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "changes" / "entries"
INDEX = ROOT / "changes" / "CHANGELOG.md"


def _cell(x, limit=220) -> str:
    s = " ".join(str(x or "").split()).replace("|", "\\|")
    return s if len(s) <= limit else s[:limit - 1] + "…"


def _prev(p) -> str:
    if not isinstance(p, dict):
        return ""
    if p.get("type") == "none":
        return f"none ({_cell(p.get('reason'), 80)}; approved {p.get('approved_by')})"
    return f"{p.get('type')}: `{p.get('ref')}`"


def render(entries: list[dict]) -> str:
    def key(e):
        return (str(e.get("date") or ""), str(e.get("id") or ""))

    rows = sorted((e for e in entries if isinstance(e, dict)), key=key, reverse=True)
    n_open = sum(1 for e in rows if e.get("status") == "open")
    L = ["# Change log", "",
         "> **Generated** by `tools/build-changelog-index.py` from `changes/entries/*.yaml`; do not edit, and do not "
         "commit it from a branch. The rules: `changes/README.md`; the checker: `tools/check-changelog.py`.", "",
         f"{len(rows)} change(s): {n_open} open, {len(rows) - n_open} closed. Newest first.", ""]
    for title, want in (("Open", "open"), ("Closed", "closed")):
        part = [e for e in rows if e.get("status") == want]
        L += [f"## {title} ({len(part)})", ""]
        if not part:
            L += ["None.", ""]
            continue
        L += ["| Id | Date | Source · kind | Summary | Decision (by, date) | Why | Prevention | Release |",
              "|---|---|---|---|---|---|---|---|"]
        for e in part:
            d = e.get("decision") or {}
            L.append(f"| {e.get('id')} | {e.get('date')} | {e.get('source')} · {e.get('kind')} | "
                     f"{_cell(e.get('summary'))} | {_cell(d.get('what'), 160)} ({d.get('by')}, {d.get('date')}) | "
                     f"{_cell(e.get('why'), 200)} | {_prev(e.get('prevention'))} | {e.get('release_tag')} |")
        L.append("")
    return "\n".join(L)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    entries = []
    for p in sorted(ENTRIES.glob("*.yaml")):
        try:
            entries.append(yaml.safe_load(p.read_text(encoding="utf-8")))
        except Exception as ex:
            print(f"  skipped {p.name}: {ex}")
    text = render(entries)
    INDEX.write_text(text, encoding="utf-8")
    print(f"  {INDEX.relative_to(ROOT).as_posix()}: {len(entries)} change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
