#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The client's build readiness workbook, generated from the package instead of typed.

`TICVAI - Build Readiness.xlsx` was hand-made on 23 September for the client: an overview, every
application, every service in plain words, and how complete the specification is. By 29 September
every number in it was out of date (2,113 operations became 2,405, 639 tables became 983, and 576
operations "pending confirmation" became 4), and nothing would have noticed. So this writes it
from the package on demand. The only authored text is the service descriptions below, kept from the
23 September file, because a client reads "Products and pricing", not "CatalogueService".

**"Ready to build"** means an operation is agreed (not `x-ticvai-provisional`) and its lineage names a
real table, so a developer can build it without asking anyone. **"Pending confirmation"** is the
operations still waiting on the client, which after the readiness close-out of 29 September are only
the make-or-break ones.

    python3 tools/build-client-readiness.py
Writes handoff/TICVAI - Build Readiness.xlsx, and copies it to the repository root where the client
file has always lived.
"""
import collections
import datetime
import glob
import json
import os
import re
import shutil

import yaml
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "handoff", "TICVAI - Build Readiness.xlsx")
CLIENT_COPY = os.path.join(os.path.dirname(ROOT), "TICVAI - Build Readiness.xlsx")
MATRIX = os.path.join(ROOT, "sources", "requirements", "Ticvai_matrix_20260621_2.xlsx")
STATUS = {"CONTRACTED": "covered", "CONTRACTED_PARTIAL": "partly covered", "GAP_CONTRACT": "not covered",
          "GAP_DECISION": "waiting on a decision", "PARKED": "parked (out of scope)"}
# Worst first, so an application's sheet opens on what is left.
STATUS_ORDER = ["not covered", "waiting on a decision", "partly covered", "covered", "parked (out of scope)"]
NO_SCREEN = "Back end only (no screen)"
LINK = Font(color="0563C1", underline="single")
HEAD = PatternFill("solid", fgColor="1F3864")

# Application names and groups as the client knows them (23 September file), by platform code.
APPS = [
    ("P01", "Guest-facing", "Guest Web — Storefront"), ("P02", "Guest-facing", "Guest App — Mobile"),
    ("P05", "Guest-facing", "Guest Kiosk — Self-Service"),
    ("P04", "Venue floor", "Venue POS — Terminal and Tablet"), ("P06", "Venue floor", "Venue Staff App — Operations"),
    ("P07", "Venue floor", "Venue Scanner — Access Control"), ("P15", "Venue floor", "Kitchen Display — Pass and Stations"),
    ("P08", "Venue management", "Venue Management — Back Office"), ("P13", "Venue management", "Venue CMS — White Label"),
    ("P16", "Venue management", "Venue Analytics — Cross-Domain Reporting"),
    ("P12", "Venue management", "Venue Support — Agent Console"),
    ("P09", "Platform, partners and onboarding", "TICVAI Web — Platform Console"),
    ("P10", "Platform, partners and onboarding", "Partner Web — Reseller Portal"),
    ("P11", "Platform, partners and onboarding", "Accreditation Web — Applications"),
    ("P14", "Platform, partners and onboarding", "Developer Portal"),
    ("P17", "Platform, partners and onboarding", "TICVAI Sign-up — Onboarding & Purchase"),
]
# The seventeen services in plain words (authored on 23 September; the only prose this tool carries).
SERVICES = [
    ("LedgerService", "Finance", "The financial record of every sale, refund and payment, and currency rates.",
     "Finance postings wait until it returns; trading is not affected."),
    ("FnbService", "Food and beverage", "Menus, table service, kitchen screens and food orders.",
     "Kitchens fall back to printed tickets."),
    ("InventoryService", "Stock", "Stock levels, counting and purchasing.",
     "Receiving and counting pause; selling continues."),
    ("RetailService", "Retail", "Merchandise, shop sales, returns and shop-and-drop.",
     "The shop stops; gates and restaurants do not."),
    ("AiService", "AI assistance", "Suggestions and the guest concierge.",
     "Suggestions stop; nothing that takes money depends on it."),
    ("CrossRegionService", "Cross-region", "Entitlements that work across regions.", "Each region continues on its own."),
    ("WhiteLabelService", "Branding",
     "Your brand, theme, pages, navigation and content in the guest web and mobile app.",
     "Guests keep seeing the last published version."),
    ("IdentityService", "Sign-in and people",
     "Staff and guest accounts, sign-in, roles and permissions, and personal-data requests.",
     "Nobody can sign in, so everything stops."),
    ("WalletService", "Wallets and credit", "Guest wallets, stored credit, gift cards and membership credit.",
     "Wallet balances cannot be spent until it returns."),
    ("VenueOpsService", "Venue operations",
     "Queues and wait times, maintenance, bookable resources, the venue map, media and transport.",
     "Venue operations degrade; selling and entry continue."),
    ("ReportingService", "Reporting", "Dashboards, reports and alerts.",
     "Dashboards pause; nothing operational depends on them."),
    ("TenancyService", "Organisation and settings",
     "Your organisation, regions, venues, outlets and tills, and the settings each one uses.",
     "Nothing can find its venue or settings, so everything stops."),
    ("PlatformService", "Subscription and platform", "Your subscription, licensed modules and platform administration.",
     "Provisioning and administration pause; trading continues."),
    ("MarketingService", "Guests and marketing", "Guest profiles, consent, loyalty, campaigns, forms and support.",
     "Campaigns and guest look-up pause; trading continues."),
    ("OrderService", "Sales and payments",
     "Baskets, orders, payments, refunds, and opening and closing cashier shifts.",
     "No new sales can be taken. This service has the highest availability target."),
    ("CatalogueService", "Products and pricing",
     "What is sold, at what price and when: products, events and sessions, price lists, promotions, bundles and seating.",
     "Tills keep selling from their last published catalogue; changes wait."),
    ("AccessService", "Entry and admission", "Tickets and passes at the gate, admission rules and entry validation.",
     "Gates fall back to their local copy of what is valid."),
]


def pct(a, b):
    """A fraction Excel formats as a percentage (a string made the green 'number stored as text' marks)."""
    return float(round(a / b, 4)) if b else None


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
    return ws


def main():
    report = json.load(open(os.path.join(ROOT, "handoff", "package-report.json"), encoding="utf-8"))
    lin = json.load(open(os.path.join(ROOT, "handoff", "api-data-lineage.json"), encoding="utf-8"))
    slice_ = json.load(open(os.path.join(ROOT, "handoff", "delivery-slice.json"), encoding="utf-8"))

    ops = {}
    for f in glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml")):
        for item in ((yaml.safe_load(open(f, encoding="utf-8")) or {}).get("paths") or {}).values():
            for o in (item or {}).values():
                if isinstance(o, dict) and o.get("operationId"):
                    ops[o["operationId"]] = o

    def ready(oid):
        o, e = ops.get(oid) or {}, lin.get(oid) or {}
        real = [t for t in (e.get("reads") or []) + (e.get("writes") or []) if not t.startswith("cache:")]
        return not o.get("x-ticvai-provisional") and bool(real)

    pending = {o for o, v in ops.items() if v.get("x-ticvai-provisional")}

    # Per application: the distinct operations its screens call.
    plat_ops = collections.defaultdict(set)
    op_plats = collections.defaultdict(set)   # operation -> the applications whose screens call it
    plat_screens = collections.Counter()
    plat_noop = collections.Counter()
    plat_design = collections.Counter()
    for f in glob.glob(os.path.join(ROOT, "screens", "P*.yaml")):
        code = os.path.basename(f)[:3]
        for s in yaml.safe_load(open(f, encoding="utf-8"))["screens"]:
            plat_screens[code] += 1
            mine = {a.get("operationId") for a in s.get("apis") or []
                    if isinstance(a, dict) and a.get("operationId") in ops}
            plat_ops[code] |= mine
            for o_ in mine:
                op_plats[o_].add(code)
            plat_noop[code] += not mine
            plat_design[code] += (s.get("wireframe") or {}).get("provenance") in ("designed", "client-verified")
    first_release = set((slice_.get("platforms") or {}).keys())
    first_codes = {"P01", "P02", "P04"} | {c for c in first_release if c.startswith("P")}
    apps = []
    for code, group, name in APPS:
        o = plat_ops[code]
        apps.append([group, name, plat_screens[code], len(o), len(o & pending), pct(sum(map(ready, o)), len(o)),
                     plat_noop[code], pct(plat_design[code], plat_screens[code]),
                     "yes" if code in first_codes else "", code])

    # Per service: the operations its lineage entries assign to it.
    by_svc = collections.defaultdict(list)
    for oid, e in lin.items():
        if oid in ops:
            by_svc[e.get("service")].append(oid)
    services = [(label, what, down, len(by_svc[svc]), pct(sum(map(ready, by_svc[svc])), len(by_svc[svc])))
                for svc, label, what, down in SERVICES]
    services.sort(key=lambda r: -(r[4] or 0))

    counts = report["counts"]
    total = len(ops)
    n_ready = sum(map(ready, ops))
    floor = set().union(*(plat_ops[c] for c in ("P01", "P02", "P05", "P04", "P06", "P07", "P15")))
    slice_ops = slice_.get("operations") or {}
    slice_ops = set(slice_ops if isinstance(slice_ops, (list, dict)) else [])
    slice_tables = {t for o in slice_ops for t in ((lin.get(o) or {}).get("reads") or []) +
                    ((lin.get(o) or {}).get("writes") or []) if not t.startswith("cache:")}
    slice_services = {(lin.get(o) or {}).get("service") for o in slice_ops} - {None}
    migrations = 0
    tasks = os.path.join(ROOT, "handoff", "service-docs", "tasks.csv")
    if os.path.exists(tasks):
        import csv
        migrations = sum(1 for r in csv.DictReader(open(tasks, encoding="utf-8"))
                         if r["key"].startswith("MIG-") and r["type"] == "Task")
    today = datetime.date.today().strftime("%d %B %Y").lstrip("0")

    trace = json.load(open(os.path.join(ROOT, "handoff", "traceability.json"), encoding="utf-8"))["rows"]
    inscope = [r for r in trace if r.get("verdict") != "PARKED"]

    def evidence_ready(r):
        names = [n for n in __import__("re").findall(r"[a-z][A-Za-z0-9]+", str(r.get("evidence") or "")) if n in ops]
        return all(ready(n) for n in names) if names else True   # a schema-field requirement is ready with its schema
    buildable = [r for r in inscope if r.get("verdict") == "CONTRACTED" and evidence_ready(r)]
    missing = [r for r in inscope if r.get("verdict") != "CONTRACTED"]
    mods = collections.defaultdict(lambda: collections.Counter())
    for r in trace:
        m = mods[r.get("domain") or "Other"]
        m["all"] += 1
        m[r.get("verdict")] += 1
        if r in buildable:
            m["ready"] += 1
    modules = []
    for d, m in sorted(mods.items(), key=lambda x: -x[1]["all"]):
        scope = m["all"] - m["PARKED"]
        modules.append((d, scope, m["CONTRACTED"], m["CONTRACTED_PARTIAL"], m["GAP_CONTRACT"] + m["GAP_DECISION"],
                        m["PARKED"], pct(m["ready"], scope)))

    # **Every requirement, and the applications it lands in.** A requirement reaches an application
    # through the operations its trace names (the evidence, else the note) and the screens that call
    # them. One met by a schema field or a job reaches no screen and says so.
    text = {}
    if os.path.exists(MATRIX):
        for r in load_workbook(MATRIX, read_only=True).worksheets[0].iter_rows(min_row=2, values_only=True):
            if r and r[4]:
                text[str(r[4]).strip()] = (r[3] or "", " ".join(str(r[5] or "").split()))
    short = {code: name.split(" — ")[0] for code, _, name in APPS}
    req_rows = []
    for r in trace:
        ref = str(r.get("matrixRef") or r.get("packageRef"))
        names = [n for n in re.findall(r"[a-z][A-Za-z0-9]+", str(r.get("evidence") or "")) if n in ops]
        names = names or [n for n in re.findall(r"[a-z][A-Za-z0-9]+", str(r.get("note") or "")) if n in ops]
        sub, req = text.get(ref, ("", ""))
        req_rows.append(dict(ref=ref, module=r.get("domain") or "Other", sub=sub, text=req,
                             codes=sorted(set().union(*(op_plats[n] for n in names))) if names else [],
                             status=STATUS.get(r.get("verdict"), r.get("verdict")),
                             ready="yes" if r in buildable else "",
                             ops=", ".join(dict.fromkeys(names)), note=r.get("note") or ""))

    def reqkey(x):
        return [int(p) if p.isdigit() else 0 for p in x["ref"].split(".")]
    req_rows.sort(key=reqkey)

    def req_counts(rows):
        live = [x for x in rows if x["status"] != "parked (out of scope)"]
        left = sum(x["status"] != "covered" for x in live)
        return len(live), len(live) - left, left, pct(len(live) - left, len(live))
    by_app = {code: [x for x in req_rows if code in x["codes"]] for code, _, _ in APPS}
    by_app[NO_SCREEN] = [x for x in req_rows if not x["codes"]]

    wb = Workbook()
    ws = wb.active
    ws.title = "Overview"
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 26
    ws["A1"] = "TICVAI — Build Readiness"
    ws["A1"].font = Font(bold=True, size=18)
    ws["A2"] = "The whole platform: every application and every service"
    ws["A3"] = f"Prepared by Softlabs · {today} · generated from the package"
    rows = [
        ("Applications", len(APPS)), ("Screens", counts["screens"]), ("Back-end services", len(SERVICES)),
        ("Operations", total),
        ("Database tables", next((c["total"] for c in report.get("chain") or []
                                  if c["link"] == "Tables reached by an operation"), "")),
        ("Requirements in scope", len(inscope)),
        ("Requirements specified and ready to build", f"{len(buildable):,} of {len(inscope):,} ({round(100 * len(buildable) / len(inscope))}%)"),
        ("Requirements not yet covered or only partly (sheet Missing)", len(missing)),
        ("Specified operations ready to build", f"{n_ready:,} of {total:,} ({round(100 * n_ready / total)}%)"),
        ("Guest and venue-floor operations pending confirmation", f"{len(floor & pending)} of {len(floor)}"),
        ("Operations waiting on the client (make-or-break questions only)", len(pending)),
        ("Screens not yet specified (no operation)", sum(plat_noop.values())),
        ("Screens with an agreed design (your prototype, or drawn and accepted)", sum(plat_design.values())),
        ("Build gaps from the design packs, not yet specified", "6 (about 100 to 170 operations)"),
        ("First release: back-end services", len(slice_services)),
        ("First release: operations", len(slice_ops)),
        ("First release: database tables", len(slice_tables)),
        ("First release: database changes (migrations)", migrations),
    ]
    for i, (k, v) in enumerate(rows, 5):
        ws.cell(row=i, column=1, value=k)
        ws.cell(row=i, column=2, value=v)
    ws.cell(row=len(rows) + 6, column=1, value=(
        "On 29 September the readiness questions were answered from the client's own minutes, design packs and "
        "boards; only questions a wrong guess would make costly (law, names only you hold, your customers' money) "
        "stay open. They are listed in TICVAI_Readiness_Questions.xlsx. \"Operations ready to build\" counts "
        "operations only: screens still to specify (mostly the AI console, waiting on its design review), screens "
        "still to design, and the six design-pack gaps are counted separately above."))
    ws.cell(row=len(rows) + 6, column=1).alignment = Alignment(wrap_text=True)

    sheet(wb, "Modules", ["Module (requirement domain)", "Requirements in scope", "Covered", "Partly covered",
                          "Not covered", "Parked (out of scope)", "Specified and ready to build"],
          [40, 12, 10, 10, 10, 12, 14], modules)
    sheet(wb, "Missing", ["Requirement", "Section", "Module", "Status", "What exists", "Note"], [12, 10, 34, 18, 40, 70],
          [(r.get("matrixRef"), r.get("section"), r.get("domain"),
            {"GAP_CONTRACT": "not covered", "CONTRACTED_PARTIAL": "partly covered",
             "GAP_DECISION": "waiting on a decision"}.get(r.get("verdict"), r.get("verdict")),
            r.get("evidence") or "", r.get("note") or "") for r in sorted(missing, key=lambda r: (r.get("domain") or "", str(r.get("matrixRef"))))])
    app_rows = [a[:9] + list(req_counts(by_app[a[9]])) for a in apps]
    app_rows.append(["", NO_SCREEN, "", "", "", "", "", "", ""] + list(req_counts(by_app[NO_SCREEN])))
    wsa = sheet(wb, "Applications", ["Group", "Application (click to see its requirements)", "Screens", "Operations",
                                     "Pending confirmation", "Specified operations ready to build",
                                     "Screens not yet specified", "Screens with an agreed design", "First release",
                                     "Requirements", "Covered", "Left", "Requirements covered"],
                [30, 44, 10, 12, 14, 14, 14, 14, 12, 14, 10, 10, 14], app_rows)
    sheet(wb, "Services", ["Service", "What it looks after", "If it is unavailable", "Operations", "Ready to build"],
          [26, 60, 50, 12, 14], services)
    chain = {c["link"]: c for c in report.get("chain") or []}
    spec = []
    for label, key in (("Requirements in scope", "Requirements in scope"),
                       ("Requirements covered by the specification", "Requirements contracted"),
                       ("Screens connected to operations", "Screens naming an operation"),
                       ("Operations owned by a service", "Operations declaring a service"),
                       ("Operations with a permission", "Operations declaring a permission"),
                       ("Operations that name the data they read and write", "Operations with resolved lineage"),
                       ("Tables used by an operation", "Tables reached by an operation")):
        c = chain.get(key)
        if c:
            spec.append((label, c["done"], c["total"], float(round(c["done"] / c["total"], 4)) if c["total"] else None))
    sheet(wb, "Specification", ["Measure", "Done", "Of", "%"], [52, 10, 10, 8], spec)

    # **One sheet per application, opening on what is left**, plus every requirement on one sheet with
    # filters. The Applications sheet and the Overview link to them.
    req_cols = ["Requirement", "Sub-domain", "Module", "Requirement text", "Applications", "Status",
                "Ready to build", "Operations", "Note"]
    req_w = [11, 22, 24, 60, 30, 16, 10, 34, 60]

    def req_line(x):
        return (x["ref"], x["sub"], x["module"], x["text"], ", ".join(short[c] for c in x["codes"]) or NO_SCREEN,
                x["status"], x["ready"], x["ops"], x["note"])
    sheet(wb, "Requirements", req_cols, req_w, [req_line(x) for x in req_rows])
    app_sheets = {}
    for code, _, name in APPS + [(NO_SCREEN, "", NO_SCREEN)]:
        rows_ = sorted(by_app[code], key=lambda x: (STATUS_ORDER.index(x["status"])
                                                    if x["status"] in STATUS_ORDER else 9, reqkey(x)))
        title = (f"{code} {short[code]}" if code in short else "Back end only")[:31]
        ws_ = sheet(wb, title, req_cols, req_w, [req_line(x) for x in rows_])
        ws_.insert_rows(1)
        n, done, left, _ = req_counts(by_app[code])
        c = ws_.cell(row=1, column=1, value="← Applications")
        c.hyperlink, c.font = f"#'Applications'!A1", LINK
        ws_.cell(row=1, column=4, value=f"{name}: {n} requirements in scope, {done} covered, "
                                        f"{left} left (listed first)").font = Font(bold=True)
        ws_.freeze_panes = "A3"
        ws_.auto_filter.ref = f"A2:{get_column_letter(len(req_cols))}{ws_.max_row}"
        app_sheets[code] = title
    for row in wsa.iter_rows(min_row=2):
        code = next((c for c, _, nm in APPS if nm == row[1].value), NO_SCREEN if row[1].value == NO_SCREEN else None)
        if code in app_sheets:
            row[1].hyperlink, row[1].font = f"#'{app_sheets[code]}'!A1", LINK
    for ws_ in wb.worksheets:
        if ws_.title != "Overview" and ws_.title not in app_sheets.values():
            ws_.auto_filter.ref = f"A1:{get_column_letter(ws_.max_column)}{ws_.max_row}"

    # **Colour says where to look.** Green is ready (95% and up), amber needs work (80-95%), red is where
    # the gaps are (under 80%). The Missing sheet colours each requirement by its status.
    GREEN, AMBER, RED, GREY = (PatternFill("solid", fgColor=c) for c in ("C6EFCE", "FFEB9C", "FFC7CE", "E7E6E6"))
    for ws_ in wb.worksheets:
        for row in ws_.iter_rows(min_row=2):
            for c in row:
                if isinstance(c.value, float) and 0 <= c.value <= 1:
                    c.number_format = "0%"
                    v_ = round(c.value, 2)   # coloured as shown: 94.9% reads "95%", so it is green
                    c.fill = GREEN if v_ >= 0.95 else AMBER if v_ >= 0.80 else RED
    status_fill = {"not covered": RED, "partly covered": AMBER, "waiting on a decision": GREY, "covered": GREEN}
    for ws_ in wb.worksheets:
        hdr = 2 if ws_.title in app_sheets.values() else 1
        col = next((c.column - 1 for c in ws_[hdr] if c.value == "Status"), None)
        for row in (ws_.iter_rows(min_row=hdr + 1) if col is not None else []):
            f = status_fill.get(row[col].value)
            if f:
                row[col].fill = f
                if f is not GREEN:
                    row[0].fill = f
    # The Overview's headline fractions ("2,650 of 2,788 (95%)") are text; colour them by their percentage.
    for row in wb["Overview"].iter_rows(min_row=5):
        v = row[1].value
        m = __import__("re").search(r"\((\d+)%\)$", str(v or ""))
        if m:
            p_ = int(m.group(1)) / 100
            row[1].fill = GREEN if p_ >= 0.95 else AMBER if p_ >= 0.80 else RED
    ov = wb["Overview"]
    top = ov.max_row + 2
    ov.cell(row=top, column=1, value="Where to look").font = Font(bold=True)
    for i, (title, what) in enumerate((
            ("Applications", "each application; click one to see its requirements, what is left first"),
            ("Requirements", "every requirement, its applications and status; use the filters in the header"),
            ("Missing", "only the requirements not yet covered or partly covered"),
            ("Modules", "requirements by module"),
            ("Services", "the back-end services in plain words"),
            ("Specification", "how complete the specification is")), top + 1):
        c = ov.cell(row=i, column=1, value=title)
        c.hyperlink, c.font = f"#'{title}'!A1", LINK
        ov.cell(row=i, column=2, value=what)
    ov.column_dimensions["B"].width = 70
    legend = wb["Overview"].max_row + 2
    for i, (fill, text) in enumerate(((GREEN, "95% and up: ready"), (AMBER, "80% to 95%: needs work"),
                                      (RED, "under 80%: where the gaps are")), legend):
        wb["Overview"].cell(row=i, column=1, value=text).fill = fill
    wb.save(OUT)
    if os.path.isdir(os.path.dirname(CLIENT_COPY)):
        try:
            shutil.copyfile(OUT, CLIENT_COPY)
        except PermissionError:
            print(f"NOT copied to {CLIENT_COPY}: it is open (close it in Excel and run again)")
    print(f"{len(buildable)} of {len(inscope)} requirements ready, {len(missing)} missing; {n_ready} of {total} operations ready -> "
          f"{os.path.relpath(OUT, ROOT)} (and the client copy at the repository root)")


if __name__ == "__main__":
    main()
