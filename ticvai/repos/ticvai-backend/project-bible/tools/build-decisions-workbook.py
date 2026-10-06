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
    # 1 October: from the 30 September revision feedback on the guest builds (CLIENT-RESPONSE-30SEP).
    ("Group booking", "Supervisors",
     "Your build lists supervisors separately and free. How many supervisors come free per group (per N guests), "
     "and is that per group ticket?", "a",
     "Supervisors are a separate, free guest type, up to 1 per 10 guests, counted on the group request.", "Your commercial team"),
    ("Group booking", "Group types",
     "Your build shows School, Corporate, Tour operator and Community groups; the platform has general, school, "
     "corporate and party. Do tour operator and community become their own types, or map to general?", "b",
     "Tour operator and community are added as their own group types.", "Your commercial team"),
    ("Group booking", "Minimum group size",
     "Each group ticket card shows a minimum group size. Is the minimum set per group ticket (product), and what "
     "are the values?", "b",
     "Each group ticket carries its own minimum, default 10.", "Your commercial team"),
    ("Group booking", "Water-park groups by session",
     "Your build has a water-park group pick a session first; group requests today take a date only. Are water-park "
     "groups booked into a session?", "b",
     "Group requests take a date and, for session-based products, a session.", "Your operations team"),
    ("Guest safety", "Swim ability",
     "The swim answer now changes what is offered: all swimmers see everything, some get a 'swim vests needed' counter, "
     "and none see a cheaper splash-and-river pass without slides. Is the vest an add-on product, and is the "
     "splash-and-river pass a separate product only non-swimmers are offered?", "a",
     "The answer filters products ('Help me choose'); the vest is an add-on; the splash-and-river pass is its own product.",
     "Your operations and safety team"),
    ("Transport", "Popular routes card",
     "The popular routes cards need a starting fare, a featured order and an image or badge per route. Should "
     "these be set per route in the back office?", "c",
     "Routes carry a featured order and an image; the starting fare is computed from the lowest fare.", "Your transport team"),
    # 1 October: from the ADRs decided that day (0060 availability, 0062 e-invoicing, 0063 encryption and keys).
    ("Tax documents", "B2C e-invoices",
     "Are e-invoices to consumers (B2C) outside the first phase of the UAE mandate for you, so only B2B invoices "
     "go through the provider at launch? (ADR-0062)", "b",
     "B2B invoices go through the provider; B2C receipts are issued by the platform and can be switched to the "
     "provider per venue when your mandate covers them.", "Your finance team"),
    ("Availability", "What 99.99% covers",
     "Which services does the 99.99% availability commitment cover: the whole platform, or the guest purchase "
     "and admission path only? And do you accept a separate target per tier: 99.99% at the venue (gates, POS, kitchen "
     "display, which keep working offline), 99.95% for online sales, 99.9% for the back office and reporting, 99.5% "
     "for AI? (ADR-0060)", "a",
     "Built to those four tiers: the venue at 99.99% because it runs offline, online sales at 99.95%, back office "
     "99.9%, AI 99.5%.", "Your IT owner"),
    ("Availability", "Zone-redundant hosting cost",
     "The availability targets need high-availability hosting in UAE North: about USD 8,050 a month for a production "
     "cell, against about USD 5,550 without it (re-priced 1 October). Do you accept that cost for production? "
     "(ADR-0060, the Azure cost sheet)", "a",
     "Production is costed zone-redundant; pre-production is not.", "Your budget owner"),
    ("Guest data", "Where face templates are stored",
     "Where may face templates be stored: only inside the facial-reader vendor's system at the venue, or also in "
     "the platform in UAE North (encrypted, with a key per tenant)? (ADR-0063)", "a",
     "Templates stay with the reader vendor; the platform keeps only a reference and the guest's consent.",
     "Your data protection officer"),
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
    ("Guest data", "Biometrics for children",
     "Adults may have face data stored with their consent. For guests under 18, should face capture (Face Pass, "
     "Face Tag) be excluded entirely, or allowed with a consent form signed by a parent or guardian? (Raised in "
     "the 30 September meeting.)", "a",
     "Face capture is not offered to guests under 18 until you decide; with guardian consent, the guardian's "
     "signed consent is recorded against the child's ticket before capture.", "Your data protection counsel"),
    ("Forecasting", "Weather data",
     "Do you approve a commercial weather data service as an input to attendance forecasting, and its monthly "
     "cost?", "d",
     "Forecasts run on sales history, bookings on hand and the calendar (holidays, Ramadan) without weather "
     "until you approve.", "Your commercial team"),
    # 30 September: the two client-side prerequisites that were tickets on our board, and the event broker.
    # (The Qdrant approval question was withdrawn the same day: approved by Chinmay on condition it is hosted
    # on UAE servers - ADR-0049.)
    # "Why only you" may be a WHY code or the sentence itself.
    ("Accounts and people", "Design sign-off",
     "Name one design reviewer who signs off each wireframe batch within 3 working days.",
     "A name only you can give",
     "Front-end screens are accepted only after that sign-off (decided 28 September).", "Your product owner"),
    ("Accounts and people", "Payment sandboxes",
     "Send Stripe and Network International sandbox credentials, and name the finance or payments owner, by a "
     "date we agree together.",
     "Accounts only you hold",
     "Checkout's declined, unknown and reconcile paths cannot be tested without a sandbox.",
     "Your finance / payments owner"),
    ("Infrastructure", "Cloud event broker",
     "Which broker should carry the platform's events in the cloud: RabbitMQ or Kafka? We need your answer before "
     "12 October (the second week of the first sprint), so that the first purchase can be proven end to end by "
     "23 October. Why it matters: every sale reaches ticketing, the ledger and stock through this broker, so it must "
     "keep each order's events in sequence, set aside messages that fail, and run in the UAE. Our recommendation "
     "is RabbitMQ, ideally as a managed service in the Azure UAE North region if one is available there: it fits "
     "this workload, it is simpler to run, and venues that run on their own premises use RabbitMQ anyway. Kafka "
     "is the better choice only if you want to replay the history of events from the broker itself.",
     "A platform and running cost you choose",
     "Everything is built behind one interface and tested on RabbitMQ, so either answer works; only the cloud "
     "setup waits for your choice.",
     "Your IT / infrastructure owner"),
    # 30 September: hardware and vendors the requirements need and the hardware list or the answers so far do not
    # name. Found by checking TICVAI_Hardware_Integration v1.0.xlsx against the dependency register and R117.
    ("Hardware", "POS terminal",
     "Which POS terminal will the cashiers use: make, model and operating system (Windows, Android or iPad)? Your "
     "hardware list names the receipt printer, cash drawer, customer display and scanner, but not the terminal.",
     "A device only you buy",
     "The POS is built as an app that works offline and drives the printer, drawer and display through standard "
     "drivers. We assume a Windows touch terminal (the HP cash drawer, display and scanner on your list suggest an HP "
     "POS system); the operating system decides how those devices are driven, so we need it before the first sprint ends.",
     "Your operations / IT team"),
    ("Hardware", "Kitchen display",
     "Which kitchen display screens and kitchen printers will the kitchens use? Your hardware list says \"decide later\", "
     "and the kitchen display is in the first release.",
     "A device only you buy",
     "The kitchen display is built as a browser screen that runs on any wall-mounted touch screen or tablet, with "
     "kitchen tickets also printable on an Epson-compatible printer.",
     "Your F&B / operations team"),
    ("Hardware", "Card payment terminals",
     "Which card payment terminals will the POS and the kiosks use, and from which provider (Stripe Terminal, "
     "Network International, or another)? They are not on your hardware list.",
     "A device and a merchant contract only you hold",
     "Card payments at the POS go through the payment provider's terminal, paired to one POS; the POS never sees a "
     "card number. Until you name the terminal, testing uses the provider's simulator.",
     "Your finance / payments owner"),
    ("Hardware", "NFC and RFID media",
     "Which NFC readers (your list says \"China\", still open) and RFID readers (Kaptur, still open), and which wristband and card chip type (for example MIFARE "
     "DESFire) will be used at gates and for cashless payments, and which device encodes the wristbands?",
     "A device only you buy",
     "Wristbands and cards are read by their unique id and a secured application on the chip; nothing of value is "
     "stored on the chip itself. The exact chip type sets how the encoder is driven.",
     "Your operations / IT team"),
    ("Hardware", "Staff and flying POS devices",
     "Will the staff app and the flying (handheld) POS run on the Chainway C66 handhelds on your list, or on other "
     "phones or tablets?",
     "A device only you buy",
     "Both are built as one Android app for the Chainway C66, which also scans and prints over Bluetooth to the "
     "Zebra printer.",
     "Your operations team"),
    # 5 October 2026 (CHG-R4-002): Muhamed Allam sent the BOCA printer documents (sources/client/2026-10-05-allam-boca-printer.md).
    # Pending: not sent to the client yet; the lead sends them with the next weekly batch.
    ("Hardware", 'BOCA printer: model and count (pending, not sent)',
     'Which BOCA model or models will you use (Lemur, Lemur-C or another), and how many at each kiosk, POS and box office?',
     'A device only you buy',
     "Tickets and wristbands print in BOCA's FGL command language, which the BOCA models share; we build and test against an emulated printer until the unit arrives.",
     'Your operations / IT team'),
    ("Hardware", 'BOCA printer: connection and host (pending, not sent)',
     'How will each BOCA printer connect (USB, Ethernet or serial), and which operating system runs the kiosks and POS it is attached to? That decides whether we print through the Windows driver or send FGL directly over the network from our device app.',
     'A device only you buy',
     'We send FGL directly to the printer (over the network or USB) from the device app, so no operating-system driver is needed; the Windows driver is the fallback.',
     'Your operations / IT team'),
    ("Hardware", 'BOCA printer: ticket and wristband stock (pending, not sent)',
     'Which ticket and wristband stock will you use: sizes, thermal or other, pre-printed backgrounds, and the black-mark and cut settings?',
     'A device only you buy',
     'Ticket and wristband layouts come from the ticket designer at a standard ticket and wristband size; the stock settings are per printer.',
     'Your operations team'),
    ("Hardware", 'BOCA printer: RFID encoding (pending, not sent)',
     "Are RFID-encoded wristbands or tickets in scope? If so, which chip, what data is written (the credential id only?), and do the gates' readers read it?",
     'A device only you buy',
     'RFID encoding on the BOCA Lemur is built behind a switch, off, until you confirm; tickets and wristbands carry the printed QR code.',
     'Your operations / IT team'),
    ("Hardware", 'BOCA printer: arrival and contact (pending, not sent)',
     'When will the printer reach our India office, and who is the BOCA technical contact for questions?',
     'A name, account or vendor only you hold',
     'The driver is built and tested on an emulated printer now; the test on the real printer is scheduled when it arrives.',
     'Muhamed Allam'),
    ("Hardware", 'BOCA printer: mandated settings (pending, not sent)',
     'Does the venue mandate any printer firmware version or printer settings we must keep?',
     'A device only you buy',
     "We keep BOCA's factory settings and change only what printing needs (the stock, the cut).",
     'Your operations / IT team'),
    ("Hardware", "Devices in the requirements but not on your hardware list",
     "Your requirements include parking cameras and barriers, queue and occupancy sensors and beacons, game readers "
     "and redemption terminals, electronic lockers and digital signage, but your hardware list names none of them. "
     "Which are in scope, and which make and model for each?",
     "A device only you buy",
     "Each is built behind a standard device interface and connected when you name the device; until then they are "
     "out of the first release.",
     "Your operations / IT team"),
    ("Suppliers", "Messaging providers",
     "Which SMS gateway and which email sending service will deliver tickets, codes and receipts, and will you use "
     "WhatsApp Business (whose account)?",
     "An account only you hold",
     "Tickets and one-time codes are sent through a provider adapter; development uses a test mailbox and a test SMS "
     "sender. The first release needs the real SMS and email senders for guests to receive their tickets.",
     "Your IT / marketing team"),
    ("Suppliers", "Accounting system",
     "Which accounting or ERP system receives the platform's financial postings (for example SAP or Oracle), and in "
     "what format?",
     "A system and a format only you hold",
     "The ledger exports its journal as a file per day in a documented format; an adapter for your system is built "
     "once you name it.",
     "Your finance team"),
    ("Suppliers", "UAE Pass",
     "Is your organisation registered as a UAE Pass service provider, and who holds the credentials? Guests sign in "
     "with UAE Pass as well as a one-time code and social sign-in.",
     "An account only you hold",
     "UAE Pass sign-in is built against its staging environment and switched on when your credentials arrive; the other "
     "sign-in methods work without it.",
     "Your IT team"),
    ("Suppliers", "App stores and digital wallets",
     "Which Apple and Google developer accounts will publish each venue's app, and who holds the Apple Wallet and "
     "Google Wallet pass certificates?",
     "An account only you hold",
     "Apps are built and signed in our test accounts; publishing and wallet passes wait for yours.",
     "Your IT / marketing team"),
    ("Government", "Tourism authority reporting",
     "Must the platform report visitor or sales figures to the Department of Economy and Tourism (Dubai) or the "
     "Department of Culture and Tourism (Abu Dhabi), and if so which reports and with which credentials?",
     "Law, a regulator or a third-party contract",
     "No reporting to a tourism authority is built; the figures such a report needs are all in the reporting layer, "
     "so a report can be added once the rules are known.",
     "Your compliance / finance team"),
    ("Suppliers", "Named third-party services",
     "Your requirements name dynamic pricing (Digonex), city passes (Go City), locker systems (Gantner, Metra) and "
     "third-party queue systems. Which of these do you use or plan to use?",
     "A name, account or vendor only you hold",
     "Pricing rules, passes, lockers and queues are built into the platform; an outside service is connected through an "
     "adapter once you confirm it.",
     "Your commercial / operations team"),
    # 30 September meeting (MoM 4.8): in-park 3D navigation built natively - ADR-0069.
    ("Venue data", "3D venue model for in-park navigation",
     "In-park 3D navigation is built into the guest app, as agreed on 30 September, and needs two files for each "
     "venue: a 3D model of the venue (a GLB file) and a pathway and location file (the walkable paths, and where "
     "each ride, outlet, shop and facility is, linked to its catalogue item), with two or more surveyed GPS points "
     "so the model lines up with the guest's position. Will you supply these for each venue, or commission a 3D "
     "vendor to produce them, and by when? We will send the file specification.",
     "Your venue's own asset, or a cost you approve",
     "In-park navigation runs on the 2D park map, with the same routes and live GPS, until a venue's model is "
     "supplied; the 3D view switches on per venue when its files pass the platform's checks.",
     "Your operations / venue team"),
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
