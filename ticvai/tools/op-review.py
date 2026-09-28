#!/usr/bin/env python3
"""Every change a ticket update would make in OpenProject, in one workbook, before anyone says go.

Added 28 September for the audit decisions. Four tools each change a different part of OpenProject:
op-descriptions.rb rewrites text and titles, op-create.rb makes tickets, op-retire.py moves them out of the
plan. Nothing showed the lot together, so a yes to one was a yes to things nobody had looked at.

What OpenProject holds now is read from the commit whose text was last applied (--applied), not from the
server: 2,800 API reads through Cloudflare take an hour, and the server copy only differs where somebody edited
a ticket by hand, which MODE=status already protects (a started ticket gets a comment, never a rewrite).

Writes handoff/service-docs/op-subjects.json (the retitles, read by op-descriptions.rb as SUBJECTS) and the
workbook. Run op-descriptions.py and push-openproject.py --export first; this reads their output.

    python tools/op-review.py --applied 82522ce --export <export.json> --out <review.xlsx>
"""
import argparse
import csv
import importlib.util
import io
import json
import subprocess
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
HEAD = PatternFill("solid", fgColor="0B1324")


def at(ref, rel):
    return subprocess.run(["git", "show", f"{ref}:ticvai/{rel}"], cwd=ROOT, capture_output=True,
                          check=True).stdout.decode("utf-8")


def first_change(old, new):
    """The first line that differs, each side, ignoring the timeframe line."""
    o = [x for x in old.splitlines() if not x.startswith("- Timeframe:")]
    n = [x for x in new.splitlines() if not x.startswith("- Timeframe:")]
    for i in range(max(len(o), len(n))):
        a, b = (o[i] if i < len(o) else ""), (n[i] if i < len(n) else "")
        if a != b:
            return a, b
    return "", ""


def sheet(wb, title, cols, widths, rows, first=False):
    ws = wb.active if first else wb.create_sheet(title)
    ws.title = title
    ws.append(cols)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
        c = ws.cell(row=1, column=i)
        c.font, c.fill = Font(bold=True, color="FFFFFF"), HEAD
    for r in rows:
        ws.append([str(x)[:32000] if isinstance(x, str) else x for x in r])
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--applied", required=True, help="the commit whose ticket text is in OpenProject now")
    ap.add_argument("--export", required=True, help="push-openproject.py --export output: tickets to make")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    key_of = {str(v): k for k, v in mp.items() if not k.startswith(("_", "VERSION"))}
    rows = {r["key"]: r for r in csv.DictReader(open(DOCS / "tasks.csv", encoding="utf-8"))}
    old_rows = {r["key"]: r for r in csv.DictReader(io.StringIO(at(a.applied, "handoff/service-docs/tasks.csv")))}
    old_subj = json.loads(at(a.applied, "handoff/service-docs/op-subjects.json"))
    new_txt = json.loads((DOCS / "op-descriptions.json").read_text(encoding="utf-8"))
    old_txt = json.loads(at(a.applied, "handoff/service-docs/op-descriptions.json"))

    # Retitles: top-level tickets whose title moved since the applied commit (sub-task titles are an operation
    # name or build / connect / tests, and do not move).
    retitle = {}
    for k, r in rows.items():
        if k in mp and k in old_rows:
            was = old_subj.get(str(mp[k]), old_rows[k]["subject"])
            if r["subject"][:255] != was:
                retitle[str(mp[k])] = (k, was, r["subject"][:255])
    (DOCS / "op-subjects.json").write_text(json.dumps({i: s for i, (_, _, s) in retitle.items()}, indent=1,
                                                      ensure_ascii=False), encoding="utf-8")

    rewrite = []
    kinds = Counter()
    for i, t in new_txt.items():
        was = old_txt.get(i, "")
        if was.strip() == t.strip():
            continue
        o, n = first_change(was, t)
        kind = "timeframe only" if not (o or n) else ("new text" if not was else "content")
        kinds[kind] += 1
        k = key_of.get(i, "")
        r = rows.get(k.partition("#")[0], {})
        rewrite.append((int(i), k, r.get("track", ""), r.get("type", "") + (" (sub-task)" if "#" in k else ""),
                        kind, o, n, len(was), len(t)))

    made = json.loads(Path(a.export).read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("retire", ROOT / "tools" / "op-retire.py")
    retire = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(retire)
    _, plan, unexplained = retire.build_plan()

    wb = Workbook()
    summary = [
        ("Descriptions rewritten (New tickets) or commented (started)", len(rewrite),
         ", ".join(f"{k} {v}" for k, v in kinds.most_common()),
         "op-descriptions.rb MODE=status on the server: New tickets are rewritten, started ones get one comment"),
        ("Titles changed", len(retitle), "", "the same run, SUBJECTS=op-subjects.json"),
        ("New tickets", len(made), ", ".join(f"{k} {v}" for k, v in Counter(
            ("sub-task" if "#" in m["key"] else "ticket") for m in made).most_common()),
         "op-create.rb on the server, then op-created-merge.py; links after with push-openproject.py"),
        ("Tickets out of the plan: on hold", sum(1 for _, k, _ in plan if k == "defer"), "",
         "op-retire.py --apply; only New tickets move, started ones are listed and left"),
        ("Tickets out of the plan: closed as merged", sum(1 for _, k, _ in plan if k == "merge"), "", "the same"),
        ("Out of the plan with no reason (left alone)", len(unexplained), ", ".join(unexplained), "must be 0"),
    ]
    sheet(wb, "Summary", ["Change", "Tickets", "Split", "How it is applied"], [52, 10, 50, 80], summary, first=True)
    sheet(wb, "Rewrites", ["Id", "Key", "Track", "Type", "Change", "First line that differs: now",
                           "First line that differs: new", "Characters now", "Characters new"],
          [8, 34, 10, 16, 14, 60, 60, 10, 10], sorted(rewrite, key=lambda x: (x[4] == "timeframe only", x[1])))
    sheet(wb, "Retitles", ["Id", "Key", "Title now", "New title"], [8, 30, 70, 70],
          [(int(i), k, o, n) for i, (k, o, n) in sorted(retitle.items(), key=lambda x: x[1][0])])
    sheet(wb, "New tickets", ["Key", "Parent", "Title", "Assignee", "Description (start)"], [34, 26, 70, 22, 80],
          [(m["key"], m.get("parent_key") or m.get("parent") or "", m["subject"], m.get("assignee") or "",
            (m.get("description") or "")[:600]) for m in made])
    sheet(wb, "Out of the plan", ["Id", "Key", "Action", "Comment it gets"], [8, 40, 22, 100],
          [(mp[k], k, "On hold, off the board" if kind == "defer" else "Rejected (merged)", note)
           for k, kind, note in plan])
    wb.save(a.out)
    print(f"{len(rewrite)} rewrites ({dict(kinds)}), {len(retitle)} retitles, {len(made)} new, "
          f"{len(plan)} out of the plan, {len(unexplained)} unexplained -> {a.out}")


if __name__ == "__main__":
    main()
