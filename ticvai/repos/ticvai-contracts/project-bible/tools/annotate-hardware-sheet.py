# -*- coding: utf-8 -*-
"""Annotate the client's hardware integration sheet with what the MoMs decided.

`TICVAI_Hardware_Integration v1.0.xlsx` lists fifteen integrations and a chosen
vendor for each. Two rows read as undecided - `China` against the gaming reader
and `Decide later` against the kitchen display - and on 19 September neither was
on any open-items list, because nothing in the package had opened the file.

They are not both undecided. The MoMs answer both: the gaming reader has a
settled integration strategy and an open *manufacturer*, and the kitchen display
was never a vendor question at all. This writes those answers back against each
row, with the minute quoted so the reader does not have to take it on trust.

**The source file is not touched.** `sources/` is read-only by its own rule - a
correction to a client document is raised with the client, never edited in place
- so this writes a new workbook to `handoff/`, which is where artefacts that go
back to the client live.

    python tools/annotate-hardware-sheet.py            report
    python tools/annotate-hardware-sheet.py --apply    write the annotated workbook
"""
import io
import os
import sys

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sources', 'specifications', 'reference',
                   'TICVAI_Hardware_Integration v1.0.xlsx')
DST = os.path.join(ROOT, 'handoff', 'TICVAI_Hardware_Integration_annotated_v1_1.xlsx')

SETTLED = 'Settled'
OPEN = 'OPEN'
NOTE = 'Noted'

# integration name -> (status, decision, minute it comes from)
DECISIONS = {
    'Emirates ID Reader Integration': (
        NOTE, 'HID. Capture is configurable per ticket and per region, not fixed system behaviour.',
        'MoM 25 Aug: "Guest/ID-proof attributes (e.g., Emirates ID, passport, handicap/PoD '
        'documentation) are configurable per ticket and per region rather than fixed system '
        'behavior."'),
    'Chainway Handheld Device Integration': (
        NOTE, 'Chainway C66. Handheld validation runs against a secure local database on the device.',
        'MoM 28 Jul: "The client strongly preferred a secure local database on the handheld device."'),
    'RFID Reader Integration': (
        OPEN, 'Kaptur. Bulk stock-count specifications still owed by the client.',
        'MoM 19 Aug: "Action: Allam/Qossai to share RFID reader/device specifications and reference '
        'data." Still pending.'),
    'NFC readers for NFC hardware / Gaming reader': (
        OPEN,
        'Strategy settled: integrate DIRECT to reader hardware via the vendor\'s own SDK/API, not '
        'through an arcade-management layer. Reader displays TICVAI-pushed pricing, branding and '
        'theme; a tap fires a dry-contact signal to start/stop the game, like a turnstile. '
        'MANUFACTURER IS THE OPEN ITEM - not the approach. "China" understates this.',
        'MoM 11 Sep: "established arcade-management vendors (e.g., Simnox, Intercard) generally '
        'refuse to integrate with TICVAI since they view it as a competing platform... TICVAI\'s '
        'intended approach is to integrate directly with reader hardware (via the hardware '
        'vendor\'s own SDK/API)." Open action: "Qossai finalizing with Chinese manufacturers; '
        'Chinmay to check for India-market alternatives."'),
    'Biometric scanners for finger prints': (
        SETTLED, 'HID / Suprema.',
        'MoM 24 Aug: vendor selection narrowed to HID and Suprema (South Korea).'),
    'Receipt Printer': (
        SETTLED, 'Epson TM-T88VII. Assigned per workstation, with device-level status shown.',
        'MoM 14 Aug: "Hardware & Peripheral Management: configures devices per workstation (receipt '
        'printer, cash drawer, payment terminal, barcode/ticket scanner/printer) and shows '
        'device-level status."'),
    'Cash Drawer': (
        SETTLED, 'HP. Assigned per workstation.',
        'MoM 14 Aug, as above. MoM 19 Aug confirms per-outlet assignment.'),
    'Customer Display': (
        SETTLED, 'HP, Toshiba.', 'No MoM reference - hardware sheet only.'),
    'Turnstile Reader Integration': (
        SETTLED,
        'HID and Suprema. Axess, Skidata, CAME, KABA and Boon Edam are STAGED as later integrations '
        '- the RFP asks for "other industry-standard systems", not those five exclusively. '
        'Integration is at two levels, turnstile and reader, over a TCP/IP event push.',
        'MoM 24 Aug (rank 1) supersedes the RFP vendor list (rank 2): "evaluating HID and Suprema '
        '(South Korea)". MoM 2 Sep: "integration happens at two levels - the turnstile itself and '
        'the reader... Devices push events to TICVAI via a TCP/IP API."'),
    'Kitchen Display Integration': (
        SETTLED,
        'NOT a vendor decision. Commodity touchscreen running P15 Kitchen Display, which is ours. '
        'What matters is station mapping, routing rules and offline fallback - all specified. '
        '"Decide later" implies a procurement decision that does not exist.',
        'MoM 31 Jul: "KDS integration only." MoM 18 Aug: "each [station] mapped to specific '
        'printers or KDS devices... fallback station/device if the primary one is offline or '
        'faulty." MoM 9 Sep: KDS drives the guest-facing order-status board.'),
    'Facial Readers Integration': (
        SETTLED, 'HID, Suprema.',
        'MoM 24 Aug: "Qossai is finalizing the access control / facial recognition vendor selection '
        'this week, evaluating HID and Suprema (South Korea)."'),
    'Barcode Scanner': (
        SETTLED, 'HP, Datalogic. Assigned per workstation; a distinct barcode per retail variant.',
        'MoM 7 Aug: each workstation records its connected devices. MoM 19 Aug: "a distinct barcode '
        'per variant".'),
    'Kiosk Integration': (
        SETTLED, 'BlueRhine Kiosk.', 'No MoM reference - hardware sheet only.'),
    'Boca Printer Integration': (
        NOTE,
        'Boca wristband and ticket printer. One unified QR code / wristband per customer across '
        'ticketing, F&B and retail - not one per product line.',
        'MoM 14 Aug: "Ticketing, F&B, and retail share one cart, one receipt, and one unified QR '
        'code/wristband per customer."'),
    'Zebra Bluetooth Printer Integration': (
        SETTLED, 'Zebra. Bluetooth, for mobile/flying POS.',
        'No MoM names Zebra directly; the RFP requires Flying POS on mobile devices.'),
}

FILL = {
    SETTLED: PatternFill('solid', fgColor='DDF0DD'),
    OPEN:    PatternFill('solid', fgColor='FFE0B2'),
    NOTE:    PatternFill('solid', fgColor='E8EEF7'),
}


def main():
    wb = openpyxl.load_workbook(SRC)
    ws = wb['Hardware']

    header = ws.max_row and 1
    ws.cell(header, 4).value = 'Status'
    ws.cell(header, 5).value = 'Decision / standard'
    ws.cell(header, 6).value = 'Source (quoted from MoM)'
    for c in range(1, 7):
        ws.cell(header, c).font = Font(bold=True)

    unseen = set(DECISIONS)
    missing = []
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 2).value
        if not name:
            continue
        name = str(name).strip()
        if name not in DECISIONS:
            missing.append((r, name))
            continue
        unseen.discard(name)
        status, decision, source = DECISIONS[name]
        ws.cell(r, 4).value = status
        ws.cell(r, 5).value = decision
        ws.cell(r, 6).value = source
        for c in range(1, 7):
            ws.cell(r, c).fill = FILL[status]
            ws.cell(r, c).alignment = Alignment(vertical='top', wrap_text=(c >= 5))

    ws.column_dimensions['B'].width = 42
    ws.column_dimensions['C'].width = 26
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 62
    ws.column_dimensions['F'].width = 78

    counts = {}
    for r in range(2, ws.max_row + 1):
        s = ws.cell(r, 4).value
        if s:
            counts[s] = counts.get(s, 0) + 1

    print('rows annotated: %s' % ', '.join('%s %d' % (k, v) for k, v in sorted(counts.items())))
    if missing:
        print('ROWS IN THE SHEET WITH NO DECISION:')
        for r, n in missing:
            print('   row %d  %s' % (r, n))
    if unseen:
        print('DECISIONS THAT MATCHED NO ROW (check the spelling against the sheet):')
        for n in sorted(unseen):
            print('   %s' % n)

    if '--apply' in sys.argv:
        wb.save(DST)
        print('wrote %s' % DST)
    else:
        print('(dry run - pass --apply to write)')


if __name__ == '__main__':
    main()
