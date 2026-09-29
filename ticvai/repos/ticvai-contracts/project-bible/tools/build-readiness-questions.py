#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every question between the package and 100% ready on every module, in one workbook.

Asked for on 28 September. The readiness report says *what* stands between each module and 100%;
this is the list somebody takes into the room. Nothing here is authored. It is read from the
contracts, the screens, the design-pack index and the audit decisions, so it shrinks as answers land.

**29 September: the client gets only make-or-break questions.** Chinmay decided that day that the
readiness questions are ours to answer from the minutes, the RFP, the design packs and our build plan
(docs/registers/readiness-closeout.md). 574 of 577 operations were agreed and the 40 design packs were
scoped (handoff/design-pack-coverage.json). So the sessions, flagged, sign-off and scope sheets are gone;
what is left for the client is one sheet, and the rest is our own work, kept here so it is visible.

Sheets:
    Summary        each platform: ready now, and what closes the gap
    Make or break  the only questions for the client: law, a name only they have, their customers' money
    Decided by us  where every other answer is recorded
    Our work       build gaps from the design packs, and screens that still name no operation
    Wireframes     each platform's frames: prototype, drawn, or generated

    python3 tools/build-readiness-questions.py
Writes handoff/TICVAI_Readiness_Questions.xlsx.
"""
import collections
import glob
import importlib.util
import json
import os
import re

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "handoff", "TICVAI_Readiness_Questions.xlsx")
HEAD = PatternFill("solid", fgColor="0B1324")

# The five sessions of the 28 September readiness report, by contract (and pack where a contract splits).
SESSIONS = [
    ("S1", "Access control, ticket media and credentials", "Client operations / security"),
    ("S2", "Pricing and promotions", "Client commercial / product"),
    ("S3", "Resale, orders and the approvals engine", "Client operations / finance"),
    ("S4", "Consent, waivers, privacy and customer service (with CF-127, CF-165)", "Client product / counsel"),
    ("S5", "Partner, reseller and membership terms", "Client commercial"),
]


def session_of(contract, pack):
    p = (pack or "").lower()
    if contract == "access":
        return "S1"
    if contract == "promotions":
        return "S2"
    if contract == "catalogue":
        return "S3" if "resale" in p else "S2"
    if contract in ("orders", "approvals"):
        return "S3"
    if contract == "marketing-crm":
        return "S4"
    if contract == "subscription":
        return "S5"
    return "S3"


def provisional_rows():
    """The review tool's own rows (citation, fields, flag), so both read the same way."""
    spec = importlib.util.spec_from_file_location("bpr", os.path.join(ROOT, "tools", "build-provisional-review.py"))
    bpr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bpr)
    rows = []
    for sub in ("spine", "satellite"):
        for fn in sorted(glob.glob(os.path.join(ROOT, "contracts", sub, "*.yaml"))):
            doc = yaml.safe_load(open(fn, encoding="utf-8")) or {}
            schemas = (doc.get("components") or {}).get("schemas") or {}
            for path, ops in (doc.get("paths") or {}).items():
                for verb, op in (ops or {}).items():
                    if not isinstance(op, dict) or not op.get("x-ticvai-provisional"):
                        continue
                    desc = str(op.get("description") or "")
                    mc = bpr.CITE.search(desc)
                    schema, props = bpr.fields_of(op, schemas)
                    contract = os.path.basename(fn)[:-5]
                    pack = bpr.clean(mc.group(1)) if mc else "(uncited)"
                    rows.append({
                        "session": session_of(contract, pack), "contract": contract, "op": op["operationId"],
                        "call": f"{verb.upper()} {path}", "summary": bpr.clean(op.get("summary")),
                        "pack": pack, "page": int(mc.group(2)) if mc else 0,
                        "fields": ", ".join(props[:30]) + (" ..." if len(props) > 30 else ""),
                        "screens": "; ".join(bpr.clean(s) for s in (op.get("x-ticvai-consumed-by") or [])),
                        "flag": re.sub(r"\*\*", "", bpr.caution(props)),
                        "mob": str(op.get("x-ticvai-make-or-break") or ""),
                    })
    return rows


def screens():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "screens", "P*.yaml"))):
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        for s in doc.get("screens") or []:
            out.append((os.path.basename(f)[:3], s))
    return out


def sheet(wb, title, cols, widths, rows, first=False):
    ws = wb.active if first else wb.create_sheet(title)
    ws.title = title
    ws.append(cols)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
        c = ws.cell(row=1, column=i)
        c.font, c.fill = Font(bold=True, color="FFFFFF"), HEAD
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def main():
    prov = provisional_rows()
    scr = screens()
    report = json.load(open(os.path.join(ROOT, "handoff", "package-report.json"), encoding="utf-8"))
    decisions = json.load(open(os.path.join(ROOT, "handoff", "audit-decisions.json"), encoding="utf-8"))
    packs_cov = json.load(open(os.path.join(ROOT, "handoff", "design-pack-coverage.json"), encoding="utf-8"))["packs"]

    by_session = collections.defaultdict(list)
    for r in prov:
        by_session[r["session"]].append(r)
    prov_ops = {r["op"]: r for r in prov}

    # Per platform: operations it calls, unagreed ones by session, screens with no operation, frames.
    plat = collections.defaultdict(lambda: {"ops": set(), "noop": [], "wf": collections.Counter(), "name": ""})
    for code, s in scr:
        p = plat[code]
        ops = {a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)} - {None}
        p["ops"] |= ops
        if not ops and not (s.get("deferred") or str(s.get("wave")) == "4"):
            p["noop"].append(s)
        p["wf"][(s.get("wireframe") or {}).get("status", "none")] += 1
    names = {p["code"]: p["name"] for p in report.get("platforms", [])}
    wb = Workbook()

    summary = []
    for code in sorted(plat):
        p = plat[code]
        unagreed = collections.Counter(prov_ops[o]["session"] for o in p["ops"] if o in prov_ops)
        pr = next((x for x in report.get("platforms", []) if x["code"] == code), {})
        closes = []
        if unagreed:
            closes.append(f"{sum(unagreed.values())} make-or-break question(s) for the client")
        if p["noop"]:
            closes.append(f"{len(p['noop'])} screens to specify")
        closes.append("wireframes verified" if p["wf"].get("approved") == sum(p["wf"].values())
                      else f"wireframes: {sum(p['wf'].values()) - p['wf'].get('approved', 0)} to verify")
        summary.append((code, names.get(code, ""), pr.get("screens", ""), len(p["ops"]),
                        sum(unagreed.values()), len(p["noop"]), "; ".join(closes)))
    sheet(wb, "Summary", ["Platform", "Name", "Screens", "Operations called", "Unagreed", "Screens with no operation",
                          "What gets it to 100%"], [9, 30, 9, 12, 11, 12, 70], summary, first=True)

    kept_ops = [r for r in prov]
    mob = []
    for r in kept_ops:
        mob.append((r["op"], r["contract"], r["summary"], "(" + ", ".join(sorted(set(re.findall(r"\(([abc])\)", r.get("mob", "")))) or ["?"]) + ")",
                    r.get("mob", "") or "Kept provisional", r["screens"], ""))
    # An agreed operation can still carry one make-or-break value (K1's Face Tag retention threshold).
    for sub in ("spine", "satellite"):
        for fn in sorted(glob.glob(os.path.join(ROOT, "contracts", sub, "*.yaml"))):
            for path_, ops_ in ((yaml.safe_load(open(fn, encoding="utf-8")) or {}).get("paths") or {}).items():
                for verb_, op_ in (ops_ or {}).items():
                    if (isinstance(op_, dict) and op_.get("x-ticvai-make-or-break")
                            and op_["operationId"] not in {r["op"] for r in kept_ops}):
                        q = str(op_["x-ticvai-make-or-break"])
                        mob.append((op_["operationId"], os.path.basename(fn)[:-5], op_.get("summary", ""),
                                    "(" + ", ".join(sorted(set(re.findall(r"\(([abc])\)", q))) or ["a"]) + ")", q, "", ""))
    for d in decisions:
        for m in re.finditer(r"\[client to (?:name|set)[^\]]*\]", json.dumps(d, ensure_ascii=False)):
            mob.append((d["id"], d["theme"], m.group(0), "(b)", "A value only the client can name", "", ""))
    for rid, what, why in (("R126 / R205", "The age below which a guest is a minor", "(a) law"),
                           ("R149 (3)", "How long each kind of guest document is kept", "(a) law"),
                           ("R077 (b)", "The facial-reader vendor, which sets the SDK and template format", "(b) vendor"),
                           ("R252", "One design reviewer who signs off each wireframe batch within 3 working days", "(b) a person only the client can name"),
                           ("Consumer law", "A/B price tests on live customers: allowed, and with what notice?", "(a) law, not blocking"),
                           ("Consumer law", "Cooling-off rights after an auto-renewal charge", "(a) law, not blocking")):
        mob.append((rid, what, "", why, "", "", ""))
    sheet(wb, "Make or break", ["Id", "Topic", "Detail", "Why only the client", "Question", "Screens", "Answer"],
          [16, 34, 34, 18, 70, 30, 30], mob)

    sheet(wb, "Decided by us", ["What", "Where it is recorded", "Count"], [44, 60, 10], [
        ("Audit questions, our recommendation (28 September)", "docs/registers/audit-decisions.md", len(decisions)),
        ("Rev 3 prototype feedback (29 September)", "docs/registers/rev3-decisions.md", ""),
        ("Operations agreed from minutes, packs and build plan (29 September)", "docs/registers/readiness-closeout.md", ""),
        ("Design pack scope (29 September)", "docs/active/design-pack-coverage.md", len(packs_cov)),
    ])
    work = [(p["pack"], p.get("verdict", ""), p.get("gap", ""), p.get("estimatedNewOperations", ""), p.get("action", ""))
            for p in packs_cov if "gap" in str(p.get("verdict", "")) or "residual" in str(p.get("verdict", ""))]
    spec = [(c, s["id"], s.get("name", ""), s.get("module", ""),
             "What does this screen show, and what does it read and change? Name its records and actions; "
             "we write the operations.", "")
            for c, s in scr if not ({a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)} - {None})
            and not (s.get("deferred") or str(s.get("wave")) == "4")]
    sheet(wb, "Our work", ["Design pack or platform", "Verdict", "Gap", "New operations (estimate)", "Action"],
          [40, 22, 60, 14, 60],
          work + [(c, "screen names no operation", f"{s['id']} {s.get('name', '')}",
                   "", "Waits on the AI design review" if c == "P09" else "Specify from its pack")
                  for c, s in scr if not ({a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)} - {None})
                  and not (s.get("deferred") or str(s.get("wave")) == "4")])

    wf = [(code, names.get(code, ""), sum(plat[code]["wf"].values()),
           ", ".join(f"{k} {v}" for k, v in plat[code]["wf"].most_common()),
           "Who verifies this platform's frames, and by when? Frames arrive by batch; each is signed off "
           "within 3 working days (audit R252).", "") for code in sorted(plat)]
    sheet(wb, "Wireframes", ["Platform", "Name", "Screens", "Frame status now", "Question", "Answer"],
          [9, 30, 9, 40, 60, 30], wf)

    wb.save(OUT)
    print(f"{len(mob)} make-or-break questions for the client, {len(work)} build gaps, "
          f"{len(spec)} screens naming no operation -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
