#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the build of 29 September evening: screen bindings and trace verdicts from the group results.

Chinmay's instruction after reading the readiness workbook: the gaps are to be built, not listed. Six
groups wrote contracts (AI, RA, RB, RC1, RC2, RD, then the parked-AI re-trace and the owner-side pass),
each returning a result file in audit/ticvai/steps/B/. Contracts were edited by the groups; this applies
the two things no group was allowed to touch, because several groups needed the same files:

1. **Screens.** Each result lists operations to add to (or remove from) screens. They are written into the
   screen's `apis` block in the authored format, and a `gaps` entry naming an operation that is now bound
   is removed, since the gap it recorded is closed.
2. **Trace verdicts.** Each result lists the requirements it closed. They are written into
   handoff/traceability.json with their evidence; a row left partly covered keeps (or gets) a backlog
   entry, because check-traceability requires one.

Lineage is merged by tools/applied/closeout-lineage-29-september.py over the same result files (they nest
their mappings under "lineage"), after tools/derive-lineage.py --apply has created the new entries.

    python tools/applied/build-29-september.py [--apply]
Without --apply it reports what it would change.
"""
import argparse
import glob
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STEPS = os.path.join(os.path.dirname(ROOT), "audit", "ticvai", "steps", "B")
PROV = "build, 29 September 2026"
PARTIAL_BACKLOG = "BL-182"


def rw(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    return s.replace("\r\n", "\n"), ("\r\n" if "\r\n" in s else "\n")


def q(text):
    text = " ".join(str(text or "").split())
    return text if (": " not in text and not text.startswith(("'", '"', "*", "&", "!", "[", "{", "`"))
                    and " #" not in text) else "'" + text.replace("'", "''") + "'"


def entry(a):
    return (f"  - operationId: {a['operationId']}\n    contract: {a['contract']}\n"
            f"    purpose: {q(a.get('purpose') or a['operationId'])}\n    trigger: {a.get('trigger') or 'onAction'}\n"
            f"    provenance: {PROV}\n")


def screen_span(s, sid):
    m = re.search(rf"^- id: {re.escape(sid)}\n", s, re.M)
    if not m:
        return None
    n = re.search(r"^- id: ", s[m.end():], re.M)
    return m.start(), (m.end() + n.start()) if n else len(s)


def bind(s, sid, add, remove):
    span = screen_span(s, sid)
    if not span:
        return s, f"{sid}: screen not found"
    a, b = span
    blk = s[a:b]
    m = re.search(r"^  apis:.*\n(?:(?:  - |    ).*\n)*", blk, re.M)
    if not m:
        return s, f"{sid}: no apis block"
    items = re.split(r"(?=^  - operationId: )", m.group(0), flags=re.M)
    head, items = items[0], items[1:]
    head = "  apis:\n"
    have = [re.match(r"  - operationId: (\w+)", i).group(1) for i in items]
    keep = [i for i, op in zip(items, have) if op not in set(remove)]
    kept_ops = {op for op in have if op not in set(remove)}
    new = [entry(x) for x in add if x["operationId"] not in kept_ops]
    if not new and len(keep) == len(items):
        return s, None
    blk = blk[:m.start()] + head + "".join(keep + new) + blk[m.end():]
    if not keep and not new:
        blk = blk.replace("  apis:\n", "  apis: []\n", 1)
    for x in add:   # a gap for an operation now bound is closed
        g = re.search(rf"^  - operation: {x['operationId']}\n(?:(?:    .*)?\n)*?(?=^  - |^  [a-z])", blk, re.M)
        if g:
            blk = blk[:g.start()] + blk[g.end():]
    blk = re.sub(r"^  gaps:\n(?=^  [a-z])", "", blk, flags=re.M)
    return s[:a] + blk + s[b:], f"{sid}: +{len(new)} -{len(items) - len(keep)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    # **Order is authority: a later group's verdict on a row replaces an earlier one's.** The build groups
    # first, then the owner-side pass that completed their handoffs, then the re-trace of the parked AI rows,
    # then the gap pass that completed what the re-trace left partial.
    ORDER = ["AI", "RA", "RB", "RC1", "RC2", "RD", "OWN", "T", "G1", "G2"]
    found = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(STEPS, "*.json"))}
    results = {g: json.load(io.open(found[g], encoding="utf-8")) for g in ORDER if g in found}
    for g in sorted(set(found) - set(ORDER)):
        print(f"  (ignored result file {g}.json: not in the apply order)")
    print("results:", ", ".join(results))

    # 1. Screens
    where = {}
    for f in glob.glob(os.path.join(ROOT, "screens", "P*.yaml")):
        for sid in re.findall(r"^- id: (\S+)$", io.open(f, encoding="utf-8").read(), re.M):
            where[sid] = f
    plan = {}
    for g, r in results.items():
        for sc in r.get("screens") or []:
            p = plan.setdefault(sc["screen"], {"add": [], "remove": []})
            p["add"] += [x for x in sc.get("add") or [] if x.get("operationId")]
            p["remove"] += sc.get("remove") or []
    files = {}
    notes = []
    for sid, p in sorted(plan.items()):
        f = where.get(sid)
        if not f:
            notes.append(f"{sid}: no such screen")
            continue
        if f not in files:
            files[f] = rw(f)
        s, nl = files[f]
        s, msg = bind(s, sid, p["add"], p["remove"])
        files[f] = (s, nl)
        if msg:
            notes.append(msg)
    print(f"screens: {len(plan)} planned, {sum(1 for n in notes if '+' in n)} changed")
    for n in notes:
        if "not found" in n or "no such" in n or "no apis" in n:
            print("  !!", n)
    if a.apply:
        for f, (s, nl) in files.items():
            io.open(f, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))

    # 2. Trace verdicts
    tp = os.path.join(ROOT, "handoff", "traceability.json")
    raw = io.open(tp, encoding="utf-8", newline="").read()
    T = json.loads(raw)
    by_ref = {}
    for r in T["rows"]:
        by_ref.setdefault(str(r.get("matrixRef")), r)
        by_ref.setdefault(str(r.get("packageRef")), r)
    changed = 0
    missing = []
    for g, res in results.items():
        for t in res.get("trace") or []:
            r = by_ref.get(str(t.get("matrixRef")))
            if not r:
                missing.append(f"{g}:{t.get('matrixRef')}")
                continue
            v = t.get("verdict")
            if v not in ("CONTRACTED", "CONTRACTED_PARTIAL"):
                continue
            r["verdict"], r["contract"], r["evidence"] = v, t.get("contract"), t.get("evidence")
            r["note"] = t.get("note") or f"re-traced 29 September (build, group {g})"
            # A contracted row keeps its backlog id as history; a partial one must name an open entry.
            if v == "CONTRACTED_PARTIAL" and not r.get("backlog"):
                r["backlog"] = PARTIAL_BACKLOG
            changed += 1
    print(f"trace: {changed} rows set" + (f"; not found: {', '.join(missing)}" if missing else ""))
    if a.apply and changed:
        io.open(tp, "w", encoding="utf-8", newline="").write(
            json.dumps(T, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))

    # 3. What the groups handed off, for the coordinator
    for g, res in results.items():
        for h in res.get("handoffs") or []:
            print(f"  handoff [{g}] {h.get('file')}: {str(h.get('change'))[:160]}")


if __name__ == "__main__":
    main()
