#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every decision we closed for the client, how we closed it, and the few questions only they can answer.

Asked for on 29 September, to go to the client with an email: "all the decisions we closed and how we
closed them". The decisions were taken in four passes, each already recorded in the package, and the
client had no single place to read them. This puts them in one workbook, generated from those records so
it cannot drift from them:

  handoff/audit-decisions.json      the 77 audit questions, answered with our recommendation (28 September)
  handoff/rev3-decisions.json       the 55 points of the client's rev 3 prototype feedback (29 September)
  handoff/readiness-closeout.json   the 574 operations agreed from the minutes, packs and build plan (29 September)
  handoff/ai-decisions.json         the AI system design decisions (29 September)
  handoff/traceability.json         the requirements re-traced and built on 29 September

The questions for the client are the make-or-break ones: law, a name or account only they hold, or money
their customers pay or get back. For each, the default we built is stated, so nothing waits on the answer.

    python3 tools/build-decisions-workbook.py
Writes handoff/TICVAI - Decisions Register.xlsx.
"""
import collections
import datetime
import io
import json
import os
import re

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
OUT = os.path.join(H, "TICVAI - Decisions Register.xlsx")
MATRIX = os.path.join(ROOT, "sources", "requirements", "Ticvai_matrix_20260621_2.xlsx")
HEAD = PatternFill("solid", fgColor="1F3864")
ASK = PatternFill("solid", fgColor="FFEB9C")
DONE = PatternFill("solid", fgColor="C6EFCE")
LINK = Font(color="0563C1", underline="single")
WHY = {"a": "Law, a regulator or a third-party contract", "b": "A name, account or vendor only you hold",
       "c": "Money your customers pay or get back", "d": "A cost you approve"}

# The questions raised by the build of 29 September. Each has a default built into the platform today.
NEW_QUESTIONS = [
    ("Tax documents", "Tax invoices and credit notes",
     "Which fields must a tax invoice and a simplified tax invoice show, and in which language (Arabic, English "
     "or both)? May a guest ask for a simplified invoice to be replaced by a full one? What must a credit note "
     "show, and within what period must it be issued?", "a",
     "Full and simplified tax invoices, numbered in sequence with no gaps per legal entity; full or partial "
     "credit notes linked to the invoice and the refund.", "Your tax adviser"),
    ("Tax documents", "E-invoicing",
     "Which accredited e-invoicing provider will you use (account and Peppol ID), from what mandate date, and "
     "do you confirm the PINT AE field mapping once the provider is chosen?", "b",
     "Invoices can be transmitted through an accredited provider; the provider is a setting.", "Your finance team"),
    ("Tax documents", "VAT return",
     "Do you confirm the VAT 201 box layout, and how sales are attributed to each emirate?", "a",
     "VAT 201 figures prepared by the platform; sales attributed by the venue's location.", "Your tax adviser"),
    ("Guest data", "Face capture on a notice",
     "May a guest be enrolled for Face Tag on a displayed notice alone, with no action from them, under the "
     "UAE PDPL?", "a",
     "The guest must actively agree on screen before capture. The notice-only option is not offered.",
     "Your data protection counsel"),
    ("Guest data", "Identity verification provider",
     "Do you use an external identity-verification provider for guest ID documents, and if so which one?", "b",
     "Guest ID documents are reviewed by your staff.", "Your operations team"),
    ("Guest data", "Biometric retention by law",
     "What minimum or maximum retention does the law require for Face Pass, Face Tag and failed or abandoned "
     "captures, in each region you operate? (Asked before; restated with what we built.)", "a",
     "Face Tag deleted once the ticket is fully used; Face Pass retention set by each venue. The legal limit "
     "you confirm becomes a floor no venue setting can go below.", "Your data protection counsel"),
    ("Forecasting", "Weather data",
     "Do you approve a commercial weather data service as an input to attendance forecasting, and its monthly "
     "cost?", "d",
     "Forecasts run on sales history, bookings on hand and the calendar (holidays, Ramadan) without weather "
     "until you approve.", "Your commercial team"),
]

# The questions sent before (readiness report of 29 September), written out in full. The default is read from
# the audit decision where there is one; otherwise the specification keeps the point open.
PRIOR_QUESTIONS = [
    ("Guest data", "Guardian consent for a minor's Face Pass",
     "At what age must a guardian consent to a minor's Face Pass enrolment, in each jurisdiction?", "a", "R205"),
    ("Guest data", "The age of a minor",
     "Below what age is a guest a minor?", "a",
     "A guest with no date of birth is treated as a minor; the age is the one your counsel gives."),
    ("Guest data", "Guest document retention",
     "How long is each kind of guest document kept?", "a",
     "Kept until the purpose ends, then for the period your counsel sets."),
    ("Refunds", "Cancelled event after a resale",
     "When an event is cancelled after a ticket was resold, who is refunded and how much: the resale buyer at the "
     "resale price, the original buyer, or both? Is the seller's payout taken back?", "c", None),
    ("Suppliers", "Facial-reader vendor",
     "Which facial-reader vendor have you contracted? It sets the SDK and the template format.", "b",
     "The platform uses the SDK of the vendor you name; nothing vendor-specific is built before that."),
    ("Accounts and people", "Approved libraries",
     "Who on your side approves the list of third-party libraries each part of the platform may use, and any "
     "addition to it?", "b", "R038"),
    ("Accounts and people", "Payment sandbox access",
     "Who delivers access to the payment providers' test environments, and by when?", "b", "R065"),
    ("Accounts and people", "Design reviewer",
     "Who is the one design reviewer who signs off each wireframe batch within 3 working days?", "b", "R252"),
    ("Consumer law", "Price tests on live customers",
     "Are A/B price tests on live customers allowed, and with what notice? Not blocking: built as a venue "
     "setting that a person approves.", "a", None),
    ("Consumer law", "Cooling-off after auto-renewal",
     "What cooling-off rights apply after an auto-renewal charge? Not blocking: built as a venue setting that a "
     "person approves.", "a", None),
]


def sheet(wb, title, cols, widths, rows):
    ws = wb.create_sheet(title)
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
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{max(ws.max_row, 2)}"
    return ws


def clean(s):
    return re.sub(r"\*\*|`", "", " ".join(str(s or "").split()))


def source_kind(ev):
    e = ev.lower()
    if re.search(r"\bmom\b|minutes", e) and "mom silent" not in e:
        return "Minutes and design pack"
    if "build plan" in e:
        return "Design pack and our build plan"
    return "Design pack"


def main():
    load = lambda n: json.load(io.open(os.path.join(H, n), encoding="utf-8"))
    audit, rev3, close = load("audit-decisions.json"), load("rev3-decisions.json"), load("readiness-closeout.json")
    ai = load("ai-decisions.json")
    trace = load("traceability.json")["rows"]
    text = {}
    if os.path.exists(MATRIX):
        for r in load_workbook(MATRIX, read_only=True).worksheets[0].iter_rows(min_row=2, values_only=True):
            if r and r[4]:
                text[str(r[4]).strip()] = " ".join(str(r[5] or "").split())

    by_id = {d.get("id"): d for d in audit}
    prior = [(a, t, q, w, clean(by_id[d].get("default")) if d in by_id else (d or "Kept open in the specification; the rest is built."))
             for a, t, q, w, d in PRIOR_QUESTIONS]

    built = [r for r in trace if str(r.get("note") or "").startswith("re-traced 29 September")]
    today = datetime.date.today().strftime("%d %B %Y").lstrip("0")

    wb = Workbook()
    ov = wb.active
    ov.title = "Summary"
    ov.column_dimensions["A"].width = 46
    ov.column_dimensions["B"].width = 16
    ov.column_dimensions["C"].width = 70
    ov["A1"] = "TICVAI — Decisions Register"
    ov["A1"].font = Font(bold=True, size=18)
    ov["A2"] = f"Prepared by Softlabs · {today} · generated from the specification package"
    ov["A4"] = "How we decided"
    ov["A4"].font = Font(bold=True)
    ov["A5"] = clean(close.get("rule"))
    ov.merge_cells("A5:C5")
    ov["A5"].alignment = Alignment(wrap_text=True, vertical="top")
    ov.row_dimensions[5].height = 62
    rows = [
        ("For you to answer", len(NEW_QUESTIONS) + len(prior),
         "The only questions left for you: law, a name or account only you hold, or your customers' money. "
         "Each shows the default we built, so nothing waits on the answer."),
        ("Audit decisions", len(audit), "Questions from the audit of the specification, answered with our recommendation (28 September)."),
        ("Rev 3 prototype feedback", len(rev3), "Each point of your rev 3 prototype review, and what we decided (29 September)."),
        ("Agreed operations", len(close["closed"]),
         "Every back-office operation that was waiting for sign-off, agreed from your minutes, design packs and "
         "our build plan, with the evidence and what changed (29 September)."),
        ("Operations added", len(close["addedOperations"]) + len((close.get("dataModel") or {}).get("writersAdded") or []),
         "Operations the review found missing and added (29 September)."),
        ("AI decisions", len(ai["decisions"]), "The AI system design questions and trade-offs, answered (29 September)."),
        ("Requirements closed", len(built),
         "Requirements re-traced against the current specification or built on 29 September, with what now serves each."),
    ]
    ov["A7"], ov["B7"], ov["C7"] = "Sheet", "Items", "What it holds"
    for c in (ov["A7"], ov["B7"], ov["C7"]):
        c.font, c.fill = Font(bold=True, color="FFFFFF"), HEAD
    for i, (t, n, what) in enumerate(rows, 8):
        c = ov.cell(row=i, column=1, value=t)
        c.hyperlink, c.font = f"#'{t}'!A1", LINK
        ov.cell(row=i, column=2, value=n)
        ov.cell(row=i, column=3, value=what).alignment = Alignment(wrap_text=True, vertical="top")
    ov.cell(row=8, column=1).fill = ASK

    ask = sheet(wb, "For you to answer",
                ["#", "Area", "Topic", "Question", "Why only you", "What the platform does today", "Who answers", "Your answer"],
                [5, 16, 26, 60, 26, 52, 22, 40],
                [(i, a, t, q, WHY.get(w, w), d, who, "") for i, (a, t, q, w, d, who) in enumerate(NEW_QUESTIONS, 1)]
                + [(len(NEW_QUESTIONS) + i, a, f"{t} (sent before)", q, WHY.get(w, w), d, "", "")
                   for i, (a, t, q, w, d) in enumerate(prior, 1)])
    for row in ask.iter_rows(min_row=2):
        row[7].fill = ASK

    sheet(wb, "Audit decisions", ["Id", "Theme", "Question", "What we decided", "Status", "Who it concerned", "Applied"],
          [8, 24, 60, 70, 30, 22, 10],
          [(d.get("id"), clean(d.get("theme")), clean(d.get("question")), clean(d.get("default")),
            clean(d.get("decision")), clean(d.get("who")), "yes" if d.get("applied") else "") for d in audit])
    sheet(wb, "Rev 3 prototype feedback",
          ["Ref", "Your feedback", "What we decided", "Specification change", "Kind", "Decided"],
          [10, 50, 60, 60, 12, 12],
          [(d.get("ref"), clean(re.sub(r"^\S+\.md#\d+\s*", "", str(d.get("source") or ""))),
            clean(d.get("what")), clean(d.get("decision") or d.get("proposal")),
            d.get("kind"), clean(d.get("decided"))) for d in rev3])
    sheet(wb, "Agreed operations", ["Area", "Operation", "How it was agreed", "Evidence", "What changed"],
          [18, 34, 26, 70, 60],
          [(c["contract"], c["op"], source_kind(c.get("evidence") or ""), clean(c.get("evidence")),
            clean(c.get("changed")) or "Agreed as drafted")
           for c in sorted(close["closed"], key=lambda c: (c["contract"], c["op"]))])
    added = [(a["contract"], a["op"], ", ".join(a.get("screens") or []), "Found missing in the review")
             for a in close["addedOperations"]]
    added += [("", str(a.get("op")), ", ".join(a.get("screens") or []), "A table had nothing writing it")
              for a in (close.get("dataModel") or {}).get("writersAdded") or []]
    sheet(wb, "Operations added", ["Area", "Operation", "Screens", "Why"], [18, 36, 50, 34], added)
    sheet(wb, "AI decisions", ["Id", "Question", "Decision"], [10, 46, 90],
          [(d["id"], d["q"], d["a"]) for d in ai["decisions"]])
    status = {"CONTRACTED": "covered", "CONTRACTED_PARTIAL": "partly covered", "GAP_CONTRACT": "not covered",
              "PARKED": "out of scope"}
    rc = sheet(wb, "Requirements closed", ["Requirement", "Module", "Requirement text", "Status", "Served by", "How"],
               [11, 26, 60, 14, 32, 70],
               [(str(r.get("matrixRef")), r.get("domain"), text.get(str(r.get("matrixRef")), ""),
                 status.get(r.get("verdict"), r.get("verdict")), f"{r.get('contract')}: {r.get('evidence')}",
                 clean(r.get("note")))
                for r in sorted(built, key=lambda r: [int(p) if p.isdigit() else 0
                                                      for p in str(r.get("matrixRef")).split(".")])])
    for row in rc.iter_rows(min_row=2):
        row[3].fill = DONE if row[3].value == "covered" else ASK

    wb.save(OUT)
    print(f"{len(NEW_QUESTIONS) + len(prior)} questions for the client, {len(audit)} audit, {len(rev3)} rev 3, "
          f"{len(close['closed'])} agreed operations, {len(added)} added, {len(ai['decisions'])} AI decisions, "
          f"{len(built)} requirements -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
