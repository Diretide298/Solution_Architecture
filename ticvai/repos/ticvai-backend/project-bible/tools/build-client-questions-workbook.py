#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The questions to put to the client, derived from what the package says it does not know.

**Asked for on 21 September: "exact questions I can share with client".** Not a summary of open
work -- the list somebody can read out in a meeting, with the client's own page reference beside
each one and a column for the answer.

## Every question here traces to something the package already wrote down

**Nothing is invented.** Three sources, and each row names which:

    x-ticvai-provisional   577 operations drafted out of a client design pack and never agreed
                           with anyone who has to build them. Each carries the pack, the page,
                           the client's own sentence describing the screen, how many bullets
                           became fields and **how many were set aside as prose**
    conflicts.md           the nine open conflicts, each already phrased as a decision
    screens with no        88 screens on P09 that name no operation at all -- an AI product with
    operation              no contract behind it, which is a scope question rather than a draft

## The sharpest question is the one about the bullets we dropped

Across the 577, **12,690 bullets were read into fields and 7,430 were set aside** as prose,
examples or hierarchy illustrations. The fields are checkable by reading them. **The 7,430 are
not** -- they are the part where this package decided something in the client's own document was
not a field, and nobody has confirmed that. The per-screen counts are on the detail sheet so the
question can be asked page by page rather than in aggregate.

Five sheets:

    Ask the client   the meeting agenda -- one row per question, with a blank Answer column
    By pack          the 17 client design packs, what was drafted from each, what it blocks
    Screens          577 rows: pack, page, what the client's screen says, fields, dropped
    No contract      the P09 screens with nothing behind them, grouped by product family
    Open conflicts   the nine, as questions

    python3 tools/build-client-questions-workbook.py
"""
import collections
import glob
import io
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
OUT = os.path.join(ROOT, "handoff", "TICVAI_Client_Questions.xlsx")

HEAD = PatternFill("solid", fgColor="0B1324")
BAND = PatternFill("solid", fgColor="F2F5F9")
ASK = PatternFill("solid", fgColor="FFF2CC")
BLANK = PatternFill("solid", fgColor="FFFBEA")
THIN = Side(style="thin", color="D8DEE8")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

SRC = re.compile(r"not invented\.\*\*\s*(.+?),\s*page\s*(\d+)\.", re.S)
SAYS = re.compile(r"The screen says:\s*(.+?)(?:\n\n|$)", re.S)
CNT = re.compile(r"(\d+)\s+were read from the screen's own bulleted directory and\s+"
                 r"(\d+)\s+bullets were dropped")


def head(ws, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(1, i, c)
        cell.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
        cell.fill = HEAD
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = ws.cell(2, 1)
    ws.auto_filter.ref = "A1:%s1" % get_column_letter(len(cols))


def put(ws, r, i, v, bold=False, band=False, fill=None, size=9):
    c = ws.cell(r, i, v)
    c.font = Font(name="Arial", size=size, bold=bold)
    c.alignment = Alignment(vertical="top", wrap_text=True)
    c.border = BORDER
    if fill:
        c.fill = fill
    elif band:
        c.fill = BAND
    return c


def read_provisional():
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        contract = os.path.splitext(os.path.basename(f))[0]
        if contract in ("common", "permissions"):
            continue
        d = yaml.safe_load(io.open(f, encoding="utf-8").read())
        for path, ms in (d.get("paths") or {}).items():
            for verb, o in (ms or {}).items():
                if not (isinstance(o, dict) and o.get("x-ticvai-provisional")):
                    continue
                desc = o.get("description") or ""
                src, says, cnt = SRC.search(desc), SAYS.search(desc), CNT.search(desc)
                # **Whitespace in a pack name is not cosmetic here.** The names are read out of
                # PDF headings and several carry a doubled space where a separator was; collapsing
                # it is what makes seventeen packs seventeen rather than twenty-one.
                pack = re.sub(r"\s+", " ", src.group(1)).strip() if src else "(no citation)"
                rows.append({
                    "operationId": o["operationId"],
                    "contract": contract,
                    "verb": verb.upper(),
                    "path": path,
                    "title": (o.get("summary") or "").strip(),
                    "pack": pack,
                    "page": int(src.group(2)) if src else None,
                    "says": re.sub(r"\s+", " ", says.group(1)).strip() if says else "",
                    "fields": int(cnt.group(1)) if cnt else 0,
                    "dropped": int(cnt.group(2)) if cnt else 0,
                    "permission": o.get("x-ticvai-permission") or "",
                    "screens": list(o.get("x-ticvai-consumed-by") or []),
                })
    return rows


def read_shell_screens():
    """P09 screens naming no operation, grouped into the product family they belong to."""
    fam = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(ROOT, "screens", "P*.yaml"))):
        d = yaml.safe_load(io.open(f, encoding="utf-8").read())
        code = (d.get("platform") or {}).get("code") or os.path.basename(f)[:3]
        for s in d.get("screens") or []:
            if [a for a in (s.get("apis") or []) if a.get("operationId")]:
                continue
            name = s.get("name") or ""
            blob = name + " " + (s.get("purpose") or "")
            if re.search(r"AI Config|Discovery|Blueprint|Guided|Configuration", blob, re.I):
                group = "AI configuration assistant"
            elif re.search(r"Forecast", blob, re.I):
                group = "Forecasting"
            elif re.search(r"\bAI\b|Governance|Oversight|Policy", blob, re.I):
                group = "AI governance and human oversight"
            else:
                group = "Other"
            fam[group].append((code, s.get("id"), name))
    return fam


# **The nine open conflicts, phrased as the client hears them.** The register states each as a
# finding with its evidence; a client needs the decision it is waiting on. The wording is taken
# from `docs/registers/conflicts.md` and shortened, never widened.
CONFLICTS = [
    ("CF-35", "Biometrics and PDPL",
     "Does a consent notice acknowledged at a counter satisfy PDPL's 'explicit consent' for a "
     "same-visit Face Tag, or is a signature required?",
     "Requirement 3.2.44 says Face Tag does not require a signed consent form. PDPL Article 4's "
     "exceptions are an exhaustive list with no legitimate-interests basis, so we built it "
     "requiring explicit consent anyway and recorded the deviation.",
     "A signature is not operable at a gate. The answer changes the gate flow, not the schema.",
     "Face Pass, facial readers, fingerprint enrolment", "Client counsel"),
    ("CF-127", "Cookie consent",
     "Do we build cookie consent, buy it, or drop it?",
     "2.6.51-2.6.65 ask for banner, categorisation, automatic site scanning for new third-party "
     "cookies, script blocking before consent, preference centre, consent records and an admin "
     "portal. 2.6.60 names GDPR, ePrivacy, CCPA, CPRA, LGPD and PDPL.",
     "Scanning means maintaining a cookie database as third-party tags change. Buying puts a "
     "vendor on every tenant storefront, which is a data-residency question. Dropping is only "
     "available if no storefront sets a non-essential cookie.",
     "Every tenant storefront", "Client"),
    ("CF-133", "UAE tax invoice",
     "What must a compliant UAE tax invoice and credit memo contain, and is e-invoicing in the "
     "delivery window?",
     "5.10.3 requires 'all required fields in accordance with VAT regulations' and nothing states "
     "what those fields are. We hold the TRN, compound tax and inclusive treatment; the document "
     "itself does not exist.",
     "Issuing a non-compliant invoice is an audit finding. Gapless sequential numbering also has "
     "to be decided per legal entity, per venue or per till.",
     "Finance, POS receipts, refunds", "Client finance"),
    ("CF-140", "Delivery plan priorities",
     "Can priorities be re-derived from the dependency matrix rather than from requirement counts?",
     "Resource Management is P3 (Could) and is the most-depended-on gap in the walk - rentals, "
     "lockers, cabanas, instructor assignment and maintenance planning all sit behind it. Access "
     "Control is also P3 at 114 requirements.",
     "A P3 prerequisite blocks every P1 that needs it. Notifications, Loyalty and Portfolio each "
     "appear at P1, P2 and P3, which is not a schedulable statement.",
     "The whole schedule", "Client + us"),
    ("CF-162", "Flash-sale environment",
     "How does a burst environment's data come back into the permanent platform?",
     "A dedicated environment for a large sale takes tens of thousands of concurrent users for "
     "hours and then goes away. Its shape is settled; the reconciliation path is not.",
     "Orders taken there have to land in the permanent platform afterwards, and that path has no "
     "design.", "Flash sales, mega events", "Client + us"),
    ("CF-165", "Retention and archival",
     "Confirm the retention periods per data class so the archival rules can be built.",
     "The policy is decided (ADR-0047) and not yet built. The archive is a separate instance, and "
     "derived stores purge at archive rather than at erasure.",
     "Five contract changes are named and ordered. No erase operation exists yet.",
     "Guest profiles, PII, the knowledge base", "Client"),
    ("CF-169", "Dashboard authoring",
     "Confirm who builds and edits dashboards, and whether a shared dashboard can be deleted.",
     "57 command centres become rows in a dashboard table, which needs three or four authoring "
     "screens that do not exist. There is also no delete operation.",
     "The editor must surface the cost of a tile: 24 tiles on a short refresh is a performance "
     "incident nobody was warned about.", "Reporting across every module", "Client + us"),
    ("CF-170", "Approve-but-cannot-publish",
     "On five screens, what happens after an approval - who publishes, and when does it go live?",
     "BO-293, BO-353, ADM-247, CMS-030 and CMS-050 each declare only an approve step against a "
     "title ending in Publication. An approval with nothing to release is a dead end.",
     "The approve operations are themselves provisional, so the approval step is not agreed "
     "either. This folds into the 577.", "Membership, media, versioning, privacy, waivers",
     "Client"),
    ("CF-171", "577 unagreed operations",
     "Will you review the 577 operations we drafted from your design packs, pack by pack?",
     "Each cites the pack and page it came from and every citation resolves to a real page. They "
     "are drafts read out of a PDF, not agreed API.",
     "They are 28% of the API surface and they are exactly the operations with no data lineage. "
     "Nothing behind them can be built until they are agreed.",
     "Back office: P08, P09, P10, P12, P13", "Client + us"),
]


def main():
    prov = read_provisional()
    shells = read_shell_screens()
    by_pack = collections.defaultdict(list)
    for r in prov:
        by_pack[r["pack"]].append(r)

    # Which platforms each pack lands on, through the screens that consume its operations.
    pack_platforms = collections.defaultdict(collections.Counter)
    for r in prov:
        for s in r["screens"]:
            m = re.match(r"(P\d\d)", str(s))
            if m:
                pack_platforms[r["pack"]][m.group(1)] += 1

    wb = Workbook()

    # ---- Ask the client ----------------------------------------------------------------------
    ws = wb.active
    ws.title = "Ask the client"
    head(ws, ["#", "Theme", "The question", "Why we are asking", "What it blocks",
              "Affects", "Who answers", "Answer", "Answered on"],
         [5, 24, 56, 62, 56, 30, 16, 40, 13])
    r = 2
    for cid, theme, q, why, blocks, affects, who in CONFLICTS:
        band = r % 2 == 0
        put(ws, r, 1, cid, bold=True, band=band)
        put(ws, r, 2, theme, band=band)
        put(ws, r, 3, q, bold=True, band=band)
        put(ws, r, 4, why, band=band)
        put(ws, r, 5, blocks, band=band)
        put(ws, r, 6, affects, band=band)
        put(ws, r, 7, who, band=band)
        put(ws, r, 8, "", fill=BLANK)
        put(ws, r, 9, "", fill=BLANK)
        r += 1

    packs = sorted(by_pack.items(), key=lambda kv: -len(kv[1]))
    for pack, items in packs:
        pages = sorted({i["page"] for i in items if i["page"]})
        fields = sum(i["fields"] for i in items)
        dropped = sum(i["dropped"] for i in items)
        pf = ", ".join("%s (%d)" % (p, n)
                       for p, n in pack_platforms[pack].most_common(3))
        band = r % 2 == 0
        put(ws, r, 1, "PK", bold=True, band=band)
        put(ws, r, 2, pack, band=band)
        put(ws, r, 3, "%s: confirm the %d screens we drafted from pages %s. We read %d of your "
                      "bullets as fields and set aside %d as prose - were any of those %d "
                      "actually fields?" % (pack, len(items), _range(pages), fields, dropped,
                                            dropped),
            bold=True, band=band, fill=ASK)
        put(ws, r, 4, "Every operation from this pack cites its page and carries your own "
                      "sentence describing the screen. Names and types are our reading of those "
                      "sentences; the sentences are yours.", band=band)
        put(ws, r, 5, "%d operations stay unagreed, and none of them can have its tables "
                      "resolved until the shape is settled." % len(items), band=band)
        put(ws, r, 6, pf or "-", band=band)
        put(ws, r, 7, "Client", band=band)
        put(ws, r, 8, "", fill=BLANK)
        put(ws, r, 9, "", fill=BLANK)
        r += 1

    n_ai = sum(len(v) for k, v in shells.items() if k != "Other")
    scope = [
        ("SC-1", "AI configuration assistant",
         "Is the AI Configuration Assistant in this delivery? %d screens - setup discovery, "
         "guided Q&A, blueprint, execution, rollback and audit." % len(
             shells.get("AI configuration assistant", [])),
         "These screens name no operation at all. This is not an unagreed draft - there is no "
         "contract behind them.",
         "If it is in, it needs contracts written from scratch. It is the largest single piece of "
         "undone design in the package.", "P09 TICVAI Web", "Client"),
        ("SC-2", "Forecasting",
         "Is Forecasting in this delivery? %d screens with no operation behind them." % len(
             shells.get("Forecasting", [])),
         "Same shape as the AI assistant: screens exist, contracts do not.",
         "Demand and revenue forecasting touches pricing, capacity and staffing.",
         "P09 TICVAI Web", "Client"),
        ("SC-3", "AI governance and oversight",
         "Is AI governance in this delivery? %d screens - capability registry, risk "
         "classification, policy builder, approval review." % len(
             shells.get("AI governance and human oversight", [])),
         "The ai contract has 31 operations in total, against %d screens of AI product with "
         "nothing behind them." % n_ai,
         "Governance of an AI feature has to exist before the feature ships, not after.",
         "P09 TICVAI Web", "Client"),
        # **Payroll is deliberately NOT a question here, and this note is why.** It was drafted
        # as one, and it is answered: Decision 6 closed it on 20 September on the client's own
        # Resource Management pack, Board 3 p45, which says TICVAI connects to *external* HR,
        # payroll and workforce systems, against zero payroll rows in the requirement matrix.
        # **Asking a client something their own document already answers is how a question list
        # loses its authority**, so it is stated as settled on the By-pack sheet instead.
        ("SC-4", "Payroll — settled, listed for confirmation only",
         "Payroll is out of scope and HR is taken as an externally mastered projection. Confirm "
         "only if you disagree.",
         "Not a question we are asking. Your Resource Management pack, Board 3 page 45, names "
         "HRMS, Payroll and Time & Attendance as integration sources, and the requirement matrix "
         "has no row mentioning payroll, payslip, salary, wage or HRMS on any of five sheets.",
         "Nothing. Seven payroll tables are declined and seven HR tables are taken as a "
         "projection, with the field-ownership and sync layer Board 3 requires.",
         "Workforce, finance", "Client (confirm only)"),
        ("SC-5", "Column prefixes",
         "Do you want every column prefixed with its table name, and if so what is the reason?",
         "You prefix code as access_point_code and id as <table>_id on 193 tables. We do not, "
         "because access.access_point.code is unambiguous inside its own row.",
         "One decision disposes of 645 of your 743 change rows, and 21 table renames with it.",
         "The whole schema", "Client backend"),
        ("SC-6", "platform.scope",
         "Confirm you are happy for the scope hierarchy to stay one table rather than five.",
         "We are taking your name. Nine scope levels are enumerated and ADR-0011 makes the "
         "hierarchy binding.",
         "Five typed tables make adding a level a new table rather than a new row.",
         "Tenancy, everything below it", "Client backend"),
    ]
    for sid, theme, q, why, blocks, affects, who in scope:
        band = r % 2 == 0
        put(ws, r, 1, sid, bold=True, band=band)
        put(ws, r, 2, theme, band=band)
        put(ws, r, 3, q, bold=True, band=band, fill=ASK)
        put(ws, r, 4, why, band=band)
        put(ws, r, 5, blocks, band=band)
        put(ws, r, 6, affects, band=band)
        put(ws, r, 7, who, band=band)
        put(ws, r, 8, "", fill=BLANK)
        put(ws, r, 9, "", fill=BLANK)
        r += 1
    n_questions = r - 2

    # ---- By pack -----------------------------------------------------------------------------
    ws = wb.create_sheet("By pack")
    head(ws, ["Client design pack", "Screens drafted", "Pages cited", "Bullets read as fields",
              "Bullets set aside", "Contracts", "Platforms"],
         [46, 14, 26, 18, 16, 30, 26])
    for i, (pack, items) in enumerate(packs, 2):
        band = i % 2 == 0
        pages = sorted({x["page"] for x in items if x["page"]})
        put(ws, i, 1, pack, bold=True, band=band)
        put(ws, i, 2, len(items), band=band)
        put(ws, i, 3, _range(pages), band=band)
        put(ws, i, 4, sum(x["fields"] for x in items), band=band)
        put(ws, i, 5, sum(x["dropped"] for x in items), band=band,
            fill=ASK if sum(x["dropped"] for x in items) > 200 else None)
        put(ws, i, 6, ", ".join(sorted({x["contract"] for x in items})), band=band)
        put(ws, i, 7, ", ".join("%s (%d)" % (p, n)
                                for p, n in pack_platforms[pack].most_common(4)), band=band)

    # ---- Screens -----------------------------------------------------------------------------
    ws = wb.create_sheet("Screens")
    head(ws, ["Pack", "Page", "Screen / operation", "What your screen says", "Contract",
              "Fields read", "Bullets set aside", "Operation id", "Answer"],
         [34, 7, 40, 74, 15, 11, 13, 30, 34])
    order = sorted(prov, key=lambda x: (x["pack"], x["page"] or 0))
    for i, x in enumerate(order, 2):
        band = i % 2 == 0
        put(ws, i, 1, x["pack"], band=band)
        put(ws, i, 2, x["page"], band=band)
        put(ws, i, 3, x["title"], bold=True, band=band)
        put(ws, i, 4, x["says"], band=band)
        put(ws, i, 5, x["contract"], band=band)
        put(ws, i, 6, x["fields"], band=band)
        put(ws, i, 7, x["dropped"], band=band, fill=ASK if x["dropped"] > x["fields"] else None)
        put(ws, i, 8, x["operationId"], band=band)
        put(ws, i, 9, "", fill=BLANK)

    # ---- No contract -------------------------------------------------------------------------
    ws = wb.create_sheet("No contract")
    head(ws, ["Product family", "Platform", "Screen", "Screen name", "Answer"],
         [34, 10, 12, 62, 34])
    i = 2
    for group in ("AI configuration assistant", "Forecasting",
                  "AI governance and human oversight", "Other"):
        for code, sid, name in sorted(shells.get(group, [])):
            band = i % 2 == 0
            put(ws, i, 1, group, bold=True, band=band)
            put(ws, i, 2, code, band=band)
            put(ws, i, 3, sid, band=band)
            put(ws, i, 4, name, band=band)
            put(ws, i, 5, "", fill=BLANK)
            i += 1

    wb.save(OUT)
    tot_f = sum(x["fields"] for x in prov)
    tot_d = sum(x["dropped"] for x in prov)
    print("  %d question(s) · %d pack(s) · %d screen(s) to confirm · %d screen(s) with no contract"
          % (n_questions, len(packs), len(prov), sum(len(v) for v in shells.values())))
    print("  %d bullet(s) read as fields, %d set aside as prose" % (tot_f, tot_d))
    print("  -> handoff/TICVAI_Client_Questions.xlsx")
    return 0


def _range(pages):
    """'4-9, 14, 20-22' -- a page list a client can find in their own PDF."""
    if not pages:
        return "-"
    out, start, prev = [], pages[0], pages[0]
    for p in pages[1:] + [None]:
        if p == prev + 1:
            prev = p
            continue
        out.append(str(start) if start == prev else "%d-%d" % (start, prev))
        start = prev = p
    return ", ".join(out)


if __name__ == "__main__":
    raise SystemExit(main())
