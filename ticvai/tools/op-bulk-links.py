#!/usr/bin/env python3
"""Prepare the "follows" links for a one-shot, server-side insert into OpenProject.

The API adds one link per call and re-walks the whole dependency graph each time (about 40 s a link once the
graph is large), so the links are inserted on the server instead, by `op-bulk-links.rb`. This script does the
checking the server would otherwise repeat per link, once, here:

  - every task and dependency has an OpenProject id (from handoff/service-docs/pms-map.json)
  - the graph has no cycle
  - no link repeats, and none a longer chain already implies (--all-links keeps those)

and writes `handoff/service-docs/op-links.json`: [[from_id, to_id], ...] where from follows to.

  python3 tools/op-bulk-links.py

Hand `op-links.json` and `tools/op-bulk-links.rb` to whoever has shell access to the OpenProject server.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
reduce_links = __import__("push-openproject").reduce_links    # links a longer chain implies are left out

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"


def main() -> int:
    rows = [r for r in csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8")) if r["type"] == "Task"]
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    edges = sorted({(r["key"], d) for r in rows for d in r["dependsOn"].split()})
    missing = sorted({k for e in edges for k in e if k not in mp})
    if missing:
        print("no OpenProject id for:", ", ".join(missing[:20]))
        return 1

    # a cycle would make OpenProject's scheduling loop; the per-link check is skipped on the server, so check here
    after = {}
    for k, d in edges:
        after.setdefault(k, []).append(d)
    state = {}

    def visit(k, path):
        state[k] = 1
        for d in after.get(k, []):
            if state.get(d) == 1:
                raise SystemExit("cycle: " + " > ".join(path + [k, d]))
            if not state.get(d):
                visit(d, path + [k])
        state[k] = 2

    sys.setrecursionlimit(10000)
    for k in after:
        if not state.get(k):
            visit(k, [])

    if "--all-links" not in sys.argv:
        edges = reduce_links(edges)
    out = [[mp[k], mp[d]] for k, d in edges]
    (DOCS / "op-links.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"{len(out)} links, no cycles, written to {DOCS / 'op-links.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
