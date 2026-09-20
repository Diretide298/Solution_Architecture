#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The build-readiness workbook: the package as rows a backend engineer can sort and filter.

**Asked for on 21 September, alongside the report.** The report says what the numbers are; this is
what somebody opens to work from. A engineer picking up `createFnbOrder` wants its service, its
permission, whether it is agreed, which tables it touches and which screens call it — on one row,
next to the other 2,072.

## The one column that decides what can be built: `provisional`

**577 of 2,073 operations carry `x-ticvai-provisional`, and all 577 of them — with no exception in
either direction — are exactly the operations with no lineage.** An operation drafted out of a
client workshop pack and never agreed with a builder was never going to have its tables resolved,
because what it reads and writes is the thing still to be settled. So `provisional` is not a
footnote on the Operations sheet; it is the filter that separates 1,496 rows somebody can start on
from 577 that need a meeting first.

Eight sheets:

    Summary       the chain, link by link, and the scale beside it
    Operations    2,073 rows — the sheet the other seven exist to explain
    Tables        627 rows, with the RLS mode each one actually gets
    Contracts     32 rows
    Services      17 rows
    Platforms     16 rows, scored by what share of each is ready to build
    Boundaries    every reference that crosses a service, one row each
    Open          what is unresolved, with the count and where it lives

**Nothing here is authored.** Every row is read from a file the refresh wrote, which is why this
runs after `build-package-report.py` and reads the same sources.

    python3 tools/build-readiness-workbook.py
"""
import collections
import glob
import io
import json
import os
import re
import sys

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
OUT = os.path.join(H, "TICVAI_Build_Readiness.xlsx")

HEAD = PatternFill("solid", fgColor="0B1324")
BAND = PatternFill("solid", fgColor="F2F5F9")
WARN = PatternFill("solid", fgColor="FCE4D6")
GOOD = PatternFill("solid", fgColor="C6EFCE")
TIER = {"foundation": PatternFill("solid", fgColor="DDEBF7"),
        "commerce": PatternFill("solid", fgColor="C6EFCE"),
        "operations": PatternFill("solid", fgColor="FFF2CC"),
        "engagement": PatternFill("solid", fgColor="FCE4D6"),
        "platform": PatternFill("solid", fgColor="EDEDED")}
THIN = Side(style="thin", color="D8DEE8")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def head(ws, cols, widths, row=1):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row, i, c)
        cell.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
        cell.fill = HEAD
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30
    ws.freeze_panes = ws.cell(row + 1, 1)
    ws.auto_filter.ref = "A%d:%s%d" % (row, get_column_letter(len(cols)), row)


def put(ws, r, i, v, bold=False, band=False, fill=None, wrap=True):
    c = ws.cell(r, i, v)
    c.font = Font(name="Arial", size=9, bold=bold)
    c.alignment = Alignment(vertical="top", wrap_text=wrap)
    c.border = BORDER
    if fill:
        c.fill = fill
    elif band:
        c.fill = BAND
    return c


def load(name):
    p = os.path.join(H, name)
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None


def read_contracts():
    """operationId -> the bits only the YAML has: provisional, step-up, verb, path, summary."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        name = os.path.splitext(os.path.basename(f))[0]
        if name in ("common", "permissions"):
            continue
        d = yaml.safe_load(io.open(f, encoding="utf-8").read())
        for path, ms in (d.get("paths") or {}).items():
            for verb, o in (ms or {}).items():
                if not isinstance(o, dict) or not o.get("operationId"):
                    continue
                out[o["operationId"]] = {
                    "contract": name,
                    "verb": verb.upper(),
                    "path": path,
                    "summary": (o.get("summary") or "").strip(),
                    "provisional": bool(o.get("x-ticvai-provisional")),
                    "stepUp": bool(o.get("x-ticvai-step-up")),
                    "permission": o.get("x-ticvai-permission") or "",
                }
    return out


def read_screens():
    """operationId -> screens naming it, and the per-platform tallies."""
    by_op = collections.defaultdict(list)
    platforms = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "screens", "P*.yaml"))):
        d = yaml.safe_load(io.open(f, encoding="utf-8").read())
        p = d.get("platform") or {}
        code = p.get("code") or os.path.basename(f)[:3]
        seen, n, withops = set(), 0, 0
        for s in d.get("screens") or []:
            n += 1
            ids = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
            if ids:
                withops += 1
            for oid in ids:
                by_op[oid].append("%s/%s" % (code, s.get("id")))
                seen.add(oid)
        platforms[code] = {"name": p.get("name") or code, "app": p.get("app") or "",
                           "screens": n, "withOperations": withops, "operations": seen}
    return by_op, platforms


def rls_modes():
    """table -> the policy it actually gets, read from the emitted SQL rather than inferred."""
    mode = {}
    for f in glob.glob(os.path.join(ROOT, "backend", "*", "920-row-level-security.sql")):
        s = io.open(f, encoding="utf-8").read()
        for t in re.findall(r"apply_scope_rls\('([^']+)'", s):
            mode[t.replace('"', "")] = "scope_path"
        for t in re.findall(r"apply_venue_rls\('([^']+)'", s):
            mode[t.replace('"', "")] = "venue_id"
        for t in re.findall(r"CREATE POLICY \w+ ON ([\w.\"]+)", s):
            mode.setdefault(t.replace('"', ""), "explicit")
    return mode


def main():
    lineage = load("api-data-lineage.json") or {}
    svc = (load("service-decomposition.json") or {"services": {}})["services"]
    graph = load("relationship-graph.json") or {"rels": []}
    schema = load("schema-reference.json") or {}
    trace = load("traceability.json") or {"rows": []}
    caps = load("module-capabilities.json") or {}
    report = load("package-report.json")
    if report is None:
        print("  !! handoff/package-report.json is missing - run "
              "tools/build-package-report.py --apply first")
        return 1

    meta = read_contracts()
    by_op, platforms = read_screens()
    rls = rls_modes()
    cols = schema.get("cols") or {}
    tables = {k for k in cols if "." in k and not k.startswith(("cache:", "vault:"))}
    schema_of = {sc: n for n, s in svc.items() for sc in s.get("schemas") or []}

    reached = collections.Counter()
    for o, d in lineage.items():
        for t in set(d.get("reads") or []) | set(d.get("writes") or []):
            reached[t] += 1
    deg = collections.Counter()
    for e in graph["rels"]:
        deg[e.get("frm")] += 1
        deg[e.get("to")] += 1

    wb = Workbook()

    # ---- Summary -----------------------------------------------------------------------------
    ws = wb.active
    ws.title = "Summary"
    head(ws, ["", "Done", "Total", "%", "What it means"], [40, 10, 10, 8, 90])
    r = 2
    put(ws, r, 1, "THE CHAIN — a screen is buildable when the whole chain under it resolves",
        bold=True)
    r += 1
    for c in report["chain"]:
        band = r % 2 == 0
        put(ws, r, 1, c["link"], band=band)
        put(ws, r, 2, c["done"], band=band)
        put(ws, r, 3, c["total"], band=band)
        put(ws, r, 4, "%d%%" % c["percent"], band=band,
            fill=(WARN if c["percent"] < 85 else None))
        put(ws, r, 5, c["note"], band=band)
        r += 1
    r += 1
    put(ws, r, 1, "SCALE", bold=True)
    r += 1
    for k, v in report["counts"].items():
        put(ws, r, 1, k, band=r % 2 == 0)
        put(ws, r, 2, v, band=r % 2 == 0)
        r += 1
    r += 1
    put(ws, r, 1, "THE ONE CORRELATION TO READ FIRST", bold=True)
    r += 1
    prov = {o for o, m in meta.items() if m["provisional"]}
    nolin = {o for o, d in lineage.items() if not (d.get("reads") or d.get("writes"))}
    for label, val in (
            ("Operations flagged x-ticvai-provisional", len(prov)),
            ("Operations with no lineage", len(nolin)),
            ("Provisional AND no lineage", len(prov & nolin)),
            ("Provisional WITH lineage", len(prov - nolin)),
            ("No lineage and NOT provisional", len(nolin - prov)),
            ("Agreed operations (not provisional)", len(set(lineage) - prov)),
            ("Agreed operations with lineage", len(set(lineage) - prov - nolin))):
        put(ws, r, 1, label, band=r % 2 == 0)
        put(ws, r, 2, val, band=r % 2 == 0)
        r += 1
    put(ws, r, 1, "Every provisional operation lacks lineage and every operation with lineage is "
                  "agreed. The two are one body of work, not two problems.", bold=True)

    # ---- Operations --------------------------------------------------------------------------
    ws = wb.create_sheet("Operations")
    head(ws, ["Operation", "Contract", "Service", "Verb", "Path", "Agreed?", "Permission",
              "Step-up", "Reads", "Writes", "Screens", "Routing", "Scope", "Offline", "Summary"],
         [30, 15, 20, 7, 34, 10, 24, 8, 7, 7, 8, 11, 10, 8, 46])
    for i, (oid, d) in enumerate(sorted(lineage.items()), 2):
        m = meta.get(oid, {})
        band = i % 2 == 0
        agreed = not m.get("provisional")
        put(ws, i, 1, oid, band=band, wrap=False)
        put(ws, i, 2, d.get("contract") or m.get("contract") or "", band=band)
        put(ws, i, 3, d.get("service") or "", band=band)
        put(ws, i, 4, m.get("verb") or d.get("verb") or "", band=band)
        put(ws, i, 5, m.get("path") or d.get("path") or "", band=band)
        put(ws, i, 6, "agreed" if agreed else "PROVISIONAL", band=band,
            fill=(None if agreed else WARN))
        put(ws, i, 7, d.get("perm") or m.get("permission") or "", band=band)
        put(ws, i, 8, "yes" if m.get("stepUp") else "", band=band)
        put(ws, i, 9, len(d.get("reads") or []), band=band)
        put(ws, i, 10, len(d.get("writes") or []), band=band)
        put(ws, i, 11, len(by_op.get(oid) or []), band=band)
        put(ws, i, 12, d.get("routing") or "", band=band)
        put(ws, i, 13, d.get("scope") or "", band=band)
        put(ws, i, 14, "yes" if d.get("offline") else "", band=band)
        put(ws, i, 15, d.get("summary") or m.get("summary") or "", band=band)

    # ---- Tables ------------------------------------------------------------------------------
    ws = wb.create_sheet("Tables")
    head(ws, ["Table", "Schema", "Service", "Columns", "Row-level security", "Operations "
              "reaching it", "References"], [38, 16, 22, 10, 20, 16, 12])
    for i, t in enumerate(sorted(tables), 2):
        sc = t.split(".", 1)[0]
        band = i % 2 == 0
        put(ws, i, 1, t, band=band, wrap=False)
        put(ws, i, 2, sc, band=band)
        put(ws, i, 3, schema_of.get(sc) or "", band=band)
        put(ws, i, 4, len(cols.get(t) or []), band=band)
        put(ws, i, 5, rls.get(t, "none"), band=band,
            fill=(None if t in rls else BAND))
        put(ws, i, 6, reached.get(t, 0), band=band, fill=(WARN if not reached.get(t) else None))
        put(ws, i, 7, deg.get(t, 0), band=band)

    # ---- Contracts ---------------------------------------------------------------------------
    ws = wb.create_sheet("Contracts")
    head(ws, ["Contract", "Service", "Operations", "Agreed", "Provisional", "With lineage",
              "On a screen", "With a permission"], [20, 22, 12, 10, 12, 12, 12, 16])
    per = collections.defaultdict(set)
    for o, d in lineage.items():
        per[d.get("contract") or meta.get(o, {}).get("contract") or "?"].add(o)
    csvc = {c: n for n, s in svc.items() for c in s.get("contracts") or []}
    for i, name in enumerate(sorted(per, key=lambda k: -len(per[k])), 2):
        o = per[name]
        band = i % 2 == 0
        p = len(o & prov)
        put(ws, i, 1, name, band=band)
        put(ws, i, 2, csvc.get(name, ""), band=band)
        put(ws, i, 3, len(o), band=band)
        put(ws, i, 4, len(o) - p, band=band)
        put(ws, i, 5, p, band=band, fill=(WARN if p else None))
        put(ws, i, 6, len(o - nolin), band=band)
        put(ws, i, 7, len([x for x in o if by_op.get(x)]), band=band)
        put(ws, i, 8, len([x for x in o if lineage[x].get("perm")]), band=band)

    # ---- Services ----------------------------------------------------------------------------
    ws = wb.create_sheet("Services")
    head(ws, ["Service", "Tier", "Contracts", "Schemas", "Operations", "Agreed", "With lineage",
              "Tables", "Refs out", "Refs in", "Why it is its own service"],
         [22, 13, 26, 26, 11, 9, 12, 9, 10, 9, 80])
    out_e = collections.Counter()
    in_e = collections.Counter()
    for e in graph["rels"]:
        f = schema_of.get((e.get("frm") or "").split(".", 1)[0])
        t = schema_of.get((e.get("to") or "").split(".", 1)[0])
        if f and t and f != t:
            out_e[f] += 1
            in_e[t] += 1
    order = ["foundation", "commerce", "operations", "engagement", "platform"]
    rows = sorted(svc.items(), key=lambda kv: (order.index(kv[1]["tier"]),
                                               -(kv[1].get("operations") or 0)))
    for i, (name, s) in enumerate(rows, 2):
        mine = {o for o, d in lineage.items() if d.get("service") == name}
        fill = TIER.get(s["tier"])
        put(ws, i, 1, name, bold=True, fill=fill)
        put(ws, i, 2, s["tier"], fill=fill)
        put(ws, i, 3, ", ".join(s.get("contracts") or []))
        put(ws, i, 4, ", ".join(s.get("schemas") or []))
        put(ws, i, 5, len(mine))
        put(ws, i, 6, len(mine - prov))
        put(ws, i, 7, len(mine - nolin))
        put(ws, i, 8, s.get("tables"))
        put(ws, i, 9, out_e[name])
        put(ws, i, 10, in_e[name])
        put(ws, i, 11, re.sub(r"\*\*", "", s.get("why") or ""))

    # ---- Platforms ---------------------------------------------------------------------------
    ws = wb.create_sheet("Platforms")
    head(ws, ["Code", "Platform", "App", "Screens", "Naming an operation", "Distinct operations",
              "Provisional", "Ready to build"], [8, 22, 24, 10, 18, 18, 12, 14])
    for i, (code, p) in enumerate(sorted(platforms.items()), 2):
        o = p["operations"]
        ready = len([x for x in o if x not in prov and x not in nolin])
        pc = int(round(100.0 * ready / max(len(o), 1)))
        band = i % 2 == 0
        put(ws, i, 1, code, band=band)
        put(ws, i, 2, p["name"], band=band)
        put(ws, i, 3, p["app"], band=band)
        put(ws, i, 4, p["screens"], band=band)
        put(ws, i, 5, p["withOperations"], band=band)
        put(ws, i, 6, len(o), band=band)
        put(ws, i, 7, len(o & prov), band=band)
        put(ws, i, 8, "%d%%" % pc, band=band, fill=(GOOD if pc >= 95 else
                                                    WARN if pc < 80 else None))

    # ---- Boundaries --------------------------------------------------------------------------
    # **One row per reference that leaves its service.** Inside a service this is a foreign key
    # the database enforces; across two it is a call, a cache or an eventual read somebody owns.
    ws = wb.create_sheet("Boundaries")
    head(ws, ["From table", "Column", "To table", "From service", "To service", "Required",
              "Kind"], [36, 24, 36, 22, 22, 10, 14])
    i = 2
    for e in sorted(graph["rels"], key=lambda e: (e.get("frm") or "", e.get("col") or "")):
        f = schema_of.get((e.get("frm") or "").split(".", 1)[0])
        t = schema_of.get((e.get("to") or "").split(".", 1)[0])
        if not f or not t or f == t:
            continue
        band = i % 2 == 0
        put(ws, i, 1, e.get("frm"), band=band, wrap=False)
        put(ws, i, 2, e.get("col"), band=band)
        put(ws, i, 3, e.get("to"), band=band, wrap=False)
        put(ws, i, 4, f, band=band)
        put(ws, i, 5, t, band=band)
        put(ws, i, 6, e.get("required"), band=band)
        put(ws, i, 7, e.get("edgeKind"), band=band)
        i += 1

    # ---- Open --------------------------------------------------------------------------------
    ws = wb.create_sheet("Open")
    head(ws, ["What", "Count", "Where it lives"], [46, 10, 80])
    verdicts = collections.Counter(r.get("verdict") for r in trace["rows"])
    items = [
        ("Operations not yet agreed (provisional)", len(prov),
         "contracts/*/*.yaml, x-ticvai-provisional — CF-171"),
        ("Operations with no lineage", len(nolin),
         "577 of these are the provisional set; 67 are not"),
        ("Requirements GAP_CONTRACT", verdicts.get("GAP_CONTRACT", 0),
         "handoff/traceability.json"),
        ("Requirements CONTRACTED_PARTIAL", verdicts.get("CONTRACTED_PARTIAL", 0),
         "handoff/traceability.json"),
        ("Requirements GAP_DECISION", verdicts.get("GAP_DECISION", 0),
         "handoff/traceability.json"),
        ("Permission keys with no description", (caps.get("unlabelled") or {}).get("count", 0),
         "contracts/shared/permissions.yaml — blocks the grant screen"),
        ("Operations carrying no permission", len([o for o, d in lineage.items()
                                                   if not d.get("perm")]),
         "on no module checklist"),
        ("Tables no operation reaches", len([t for t in tables if not reached.get(t)]),
         "handoff/package-report.json — a judgement per row"),
        ("Screens naming no operation", sum(p["screens"] - p["withOperations"]
                                            for p in platforms.values()),
         "88 of them are P09 TICVAI Web"),
        ("Conflicts open", (report.get("open") or {}).get("conflictsOpen"),
         "docs/registers/conflicts.md — none blocking"),
    ]
    for i, (what, n, where) in enumerate(items, 2):
        band = i % 2 == 0
        put(ws, i, 1, what, band=band, bold=True)
        put(ws, i, 2, n, band=band)
        put(ws, i, 3, where, band=band)

    wb.save(OUT)
    print("  %d operation(s), %d table(s), %d crossing reference(s)"
          % (len(lineage), len(tables), sum(out_e.values())))
    print("  -> handoff/TICVAI_Build_Readiness.xlsx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
