#!/usr/bin/env python3
"""Release note for the client and the team: what changed in the package between two releases.

    python tools/release-notes.py r1 r2 [--crs crs.json] [--out handoff/release-notes/r2.md]

Reads the two git refs, never the working tree, so the note describes exactly what was tagged. It lists:
  - operations added, changed and removed, per contract
  - screens added and changed, per platform
  - decision records added or changed
  - with --crs (ADAM's release-note export: the CRs confirmed between the two tags), the CRs behind them:
    source, approver, triage class, contract impact
The note says what a client answer changed; the questions still waiting on the client are in the Decisions Register.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "ticvai/"      # the package sits in ticvai/ of the adam repo


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout


def changed(a: str, b: str) -> list[tuple[str, str]]:
    out = git("diff", "--name-status", a, b, "--", ".")
    rows = []
    for line in out.splitlines():
        parts = line.split("\t")
        rows.append((parts[0][0], parts[-1]))
    return rows


def load(ref: str, path: str):
    text = git("show", f"{ref}:{path}")
    try:
        return yaml.safe_load(text) if text else None
    except yaml.YAMLError:
        return None


def ops(doc) -> dict[str, object]:
    out = {}
    for p, item in ((doc or {}).get("paths") or {}).items():
        for verb, op in (item or {}).items():
            if isinstance(op, dict) and op.get("operationId"):
                out[op["operationId"]] = (verb.upper(), p, json.dumps(op, sort_keys=True, default=str))
    return out


def screens(doc) -> dict[str, str]:
    items = doc if isinstance(doc, list) else (doc or {}).get("screens") or []
    return {s["id"]: json.dumps(s, sort_keys=True, default=str) for s in items if isinstance(s, dict) and s.get("id")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--crs")
    ap.add_argument("--out")
    a = ap.parse_args()
    rows = changed(a.old, a.new)
    lines = [f"# TICVAI release {a.new}", "", f"Changes since {a.old}.", ""]

    lines += ["## Operations", ""]
    n = 0
    for st, path in rows:
        rel = path[len(PREFIX):] if path.startswith(PREFIX) else path
        if not (rel.startswith("contracts/") and rel.endswith(".yaml")):
            continue
        before, after = ops(load(a.old, path)), ops(load(a.new, path))
        added = sorted(set(after) - set(before))
        removed = sorted(set(before) - set(after))
        edited = sorted(k for k in set(before) & set(after) if before[k] != after[k])
        if added or removed or edited:
            lines.append(f"- **{Path(rel).stem}**: " + "; ".join(x for x in (
                f"added {', '.join(added)}" if added else "",
                f"changed {', '.join(edited)}" if edited else "",
                f"removed {', '.join(removed)}" if removed else "") if x))
            n += len(added) + len(removed) + len(edited)
    lines += (["- none"] if not n else []) + [""]

    lines += ["## Screens", ""]
    n = 0
    for st, path in rows:
        rel = path[len(PREFIX):] if path.startswith(PREFIX) else path
        if not (rel.startswith("screens/P") and rel.endswith(".yaml")):
            continue
        before, after = screens(load(a.old, path)), screens(load(a.new, path))
        added = sorted(set(after) - set(before))
        edited = sorted(k for k in set(before) & set(after) if before[k] != after[k])
        if added or edited:
            lines.append(f"- **{Path(rel).stem}**: " + "; ".join(x for x in (
                f"new {', '.join(added)}" if added else "",
                f"changed {', '.join(edited[:40])}{' ...' if len(edited) > 40 else ''}" if edited else "") if x))
            n += len(added) + len(edited)
    lines += (["- none"] if not n else []) + [""]

    lines += ["## Decisions", ""]
    adrs = [(st, p) for st, p in rows if p.startswith(PREFIX + "docs/adr/0")]      # not the mirror copies
    lines += [f"- {'new' if st == 'A' else 'updated'}: {Path(p).stem}" for st, p in adrs] or ["- none"]
    lines.append("")

    if a.crs:
        crs = json.loads(Path(a.crs).read_text(encoding="utf-8"))
        lines += ["## Change requests in this release", ""]
        for c in crs:
            lines.append(f"- **{c.get('id')}** {c.get('title', '')}: {c.get('source', '')}"
                         f"{' (' + c['sourceRef'] + ')' if c.get('sourceRef') else ''}; approved by "
                         f"{c.get('approver', '?')}; {c.get('triage', '')}; contract {c.get('contractImpact', 'none')}")
        lines.append("")
    lines += ["Open questions waiting on you are in the Decisions Register (\"For you to answer\")."]
    text = "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"-> {a.out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
