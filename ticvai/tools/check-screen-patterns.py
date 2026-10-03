#!/usr/bin/env python3
"""Fail when a screen asks for, shows, names, needs or says what the Block A audit of 3 October found.

**The audit judged 75 r2 tickets from their developer pulls and found patterns, not slips**
(`changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`). Every one of them came from a
generator or a move that nothing checked afterwards, so each came back across hundreds of screens.
The rules live in `tools/screen_patterns.py`, shared with the generators and the 3 October fix
(`tools/applied/spec-screen-patterns-3-october.py`, CHG-SPF-001..006):

    P1   a form asks for a field the request schema marks readOnly           (CHG-SPF-001)
    P2   a list or panel shows a schema unfiltered                           (CHG-SPF-002)
    P3   the no-access state names the wrong permission, or not the read's
         and the actions' own                                                 (CHG-SPF-003)
    P5   a required entry parameter that no inbound edge carries              (CHG-SPF-004)
    P7b  a route or component that belongs to another screen                  (CHG-SPF-005)
    P8   a Block A screen that says it is not in the first release, or is
         not wave 1                                                           (CHG-SPF-006)
    DEC  a screen Chinmay's 3 October answers changed drifts back             (CHG-SPF-007..013)

**An exception is written here with its reason**, never skipped silently, and every exemption used
is printed. P8 reads Block A from `handoff/service-docs/op-release.json` (what the tickets were cut
from); when that file is absent it says so and the rule does not run.

    python tools/check-screen-patterns.py            # fail on any finding
    python tools/check-screen-patterns.py --list     # every finding, not the first 40
    python tools/check-screen-patterns.py --only P5  # one rule
"""
from __future__ import annotations

import sys
from collections import Counter

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import screen_patterns as sp  # noqa: E402

# (rule, screen, a phrase the finding's detail contains) -> why it is right as it stands.
EXEMPT = {
    ("P8", "KIT-001", "not in the first release"): "the station-load tile alone is out of the first "
        "release (audit R277, 28 September); the screen is in it. Accurate, about one tile",
    ("P8", "KIT-002", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-003", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-004", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-005", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-006", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-007", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-008", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-009", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "KIT-010", "not in the first release"): "the station-load tile only (audit R277)",
    ("P8", "WEB-012", "not in the first release"): "Tabby split-in-4, pay on arrival and invoice/PO "
        "are the payment methods left out of the first release (CHG-SGU-020); checkout itself is in",
    # P3: the screen states the design and the contract has not caught up; the contract moves.
    ("P3", "POS-008", "REPORT_VIEW"): "the till's day view is the cashier's own or the terminal's "
        "figures (REPORT_VIEW_OWN / REPORT_VIEW_WORKSTATION); runReport and listReports still declare "
        "REPORT_VIEW_VENUE. Asked of the contract owner in the CHG-SPF-003 report",
}

# P5: Block A screens whose load needs an id that no screen holding it links to yet, each a question
# for the lead (CHG-SPF-004); the screen is right that it cannot load without it.
P5_BLOCK_A = {
    ("WEB-014", "token"): "the pay-by-link page opens from the link the guest is sent; no in-app "
        "screen holds the link's token",
    ("WEB-038", "sessionId"): "order tracking reads the table's session, which the table QR carries",
    ("WEB-039", "mapId"): "the guest map needs the venue's published map; no guest read returns its "
        "id yet (a 'published map for this venue' read is the contract question)",
    ("GST-005", "eventId"): "What's On lists one event's performances; from Home the event is the "
        "venue's current one, which no read returns yet",
    ("POS-010", "mediaId"): "getMediaAsset is the asset library's read; the till's 'existing ticket' "
        "is the guest's ticket media (mediaCode). A binding question for the POS owner",
    ("KIT-010", "dashboardId"): "the kitchen's dashboard is the station's; no read returns its id yet",
}
# The rest are workshop-pack spokes outside Block A: the hub that opens each does not hold the record
# the spoke works on. Which list hands it over is a Block B design decision (CHG-SPF-004).
P5_PACK_SPOKES = {
    ("KSK-011", "orderId"), ("EMP-036", "mediaCode"), ("EMP-036", "mediaId"), ("EMP-030", "mapId"),
    ("EMP-057", "subjectId"), ("EMP-061", "dashboardId"), ("EMP-099", "depositId"),
    ("BO-027", "mediaCode"), ("BO-140", "menuId"), ("BO-273", "groupBookingId"),
    ("BO-355", "entitlementId"), ("BO-488", "subjectId"), ("BO-572", "depositId"),
    ("BO-601", "priceListId"), ("BO-737", "guestId"), ("BO-738", "guestId"), ("BO-740", "guestId"),
    ("BO-742", "guestId"), ("BO-743", "guestId"), ("BO-833", "dashboardId"),
    ("BO-875", "resourceId"), ("BO-957", "seatMapId"), ("BO-958", "seatMapId"),
    ("BO-959", "seatMapId"), ("BO-960", "seatMapId"), ("BO-961", "seatMapId"),
    ("BO-976", "seatMapId"), ("BO-982", "seatMapId"), ("BO-995", "performanceId"),
    ("BO-1001", "performanceId"), ("BO-1002", "performanceId"), ("BO-1065", "regionId"),
    ("BO-1070", "seatMapId"), ("ADM-180", "bundleId"), ("ADM-181", "bundleId"),
    ("ADM-185", "bundleId"), ("ADM-187", "bundleId"), ("ADM-189", "itemId"),
    ("ADM-191", "bundleId"), ("ADM-195", "bundleId"), ("ADM-593", "token"),
    ("ADM-680", "subjectId"), ("ADM-366", "approvalRequestId"), ("ADM-027", "runId"),
    ("ADM-533", "decisionRecordId"), ("PTR-013", "accountId"), ("ANL-006", "countId"),
}
for (_sid, _p), _why in P5_BLOCK_A.items():
    EXEMPT[("P5", _sid, f"requires {_p} ")] = "Block A, open: " + _why
for _sid, _p in P5_PACK_SPOKES:
    EXEMPT[("P5", _sid, f"requires {_p} ")] = ("a pack spoke outside Block A: its hub does not hold "
                                               "the record; the edge is a Block B design decision")


# DEC: Chinmay's 3 October answers that changed a screen, held so a later edit cannot quietly undo
# them: (change id, screen, rule, operation). `without` — the screen calls the operation nowhere
# (apis, components, overlays); `with` — the screen declares it; `not-on-load` — never on load;
# `no-buttons` — no button of any kind (the operation field is unused).
DECIDED = [
    ("CHG-SPF-007", "GST-001", "without", "listAnalyticsProviders"),
    ("CHG-SPF-007", "WEB-001", "without", "listAnalyticsProviders"),
    ("CHG-SPF-008", "KIT-007", "without", "recordOrderHandover"),
    ("CHG-SPF-008", "KIT-007", "no-buttons", ""),
    ("CHG-SPF-009", "BO-056", "without", "recordAttendance"),
    ("CHG-SPF-010", "BO-078", "without", "rejectRequisition"),
    ("CHG-SPF-010", "BO-078", "without", "returnRequisition"),
    ("CHG-SPF-011", "ANL-023", "with", "createDashboard"),
    ("CHG-SPF-012", "POS-000", "not-on-load", "listActiveSessions"),
    ("CHG-SPF-013", "GST-031", "without", "sendConversationMessage"),
    ("CHG-SPF-013", "GST-032", "without", "sendConversationMessage"),
    ("CHG-SPF-013", "WEB-044", "without", "sendConversationMessage"),
    ("CHG-SPF-013", "GST-031", "with", "sendGuestConversationMessage"),
    ("CHG-SPF-013", "GST-032", "with", "sendGuestConversationMessage"),
    ("CHG-SPF-013", "WEB-044", "with", "sendGuestConversationMessage"),
    ("CHG-SPF-013", "GST-070", "with", "listMyTableReservations"),
    ("CHG-SPF-013", "GST-070", "with", "listBookableOutlets"),
    ("CHG-SPF-013", "EMP-026", "with", "uploadIncidentMedia"),
    ("CHG-SPF-013", "EMP-026", "with", "addIncidentPerson"),
]
BUTTONS = {"primaryButton", "secondaryButton", "destructiveButton", "iconButton"}


def decided(S) -> list:
    out = []
    for chg, sid, rule, op in DECIDED:
        s = S.get(sid)
        if s is None:
            out.append(("DEC", sid, f"{chg}: the screen is gone"))
            continue
        a = {x["operationId"]: x for x in sp.apis(s)}
        used = set(a) | {c.get("operation") for _, c in sp.components(s)} | \
            {(o.get("confirm") or {}).get("operation") for o in s.get("overlays") or []}
        if rule == "without" and op in used:
            out.append(("DEC", sid, f"{chg}: calls {op} again"))
        elif rule == "with" and op not in a:
            out.append(("DEC", sid, f"{chg}: no longer declares {op}"))
        elif rule == "not-on-load" and op in a and a[op].get("trigger") in sp.LOAD_TRIGGERS:
            out.append(("DEC", sid, f"{chg}: {op} is read on load again"))
        elif rule == "no-buttons" and any(c.get("kind") in BUTTONS for _, c in sp.components(s)):
            out.append(("DEC", sid, f"{chg}: a read-only display has a button again"))
    return out


def run(only=None):
    pk = sp.Package()
    S = pk.screens
    inb = sp.inbound(S)
    owners = sp.component_owners(S)
    block_a = sp.block_a_screens()
    found = decided(S) if only in (None, "DEC") else []
    for sid, s in S.items():
        if only in (None, "P1"):
            found += sp.p1(pk, sid, s)
        if only in (None, "P2"):
            found += sp.p2(pk, sid, s)
        if only in (None, "P3"):
            found += sp.p3(pk, sid, s)
        if only in (None, "P5"):
            found += sp.p5(pk, sid, s, inb)
        if only in (None, "P7b"):
            found += sp.p7b(pk, sid, s, owners)
        if only in (None, "P8") and block_a is not None:
            found += sp.p8(pk, sid, s, block_a, {})
    return found, block_a


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    args = sys.argv[1:]
    only = args[args.index("--only") + 1] if "--only" in args else None
    found, block_a = run(only)
    if block_a is None:
        print("  P8 not run: handoff/service-docs/op-release.json is absent (derive it first)")
    used, bad = [], []
    for rule, sid, detail in found:
        why = next((w for (r, s, phrase), w in EXEMPT.items()
                    if r == rule and s == sid and phrase in detail), None)
        (used if why else bad).append((rule, sid, detail, why))
    for rule, sid, detail, why in used:
        print(f"  exempt {rule:<4} {sid:<9} {why}")
    by = Counter(r for r, _, _, _ in bad)
    show = bad if "--list" in args else bad[:40]
    for rule, sid, detail, _ in show:
        print(f"  {rule:<4} {sid:<9} {detail}")
    if len(show) < len(bad):
        print(f"  … and {len(bad) - len(show)} more (--list shows all)")
    if bad:
        print(f"FAIL {len(bad)} finding(s): " + ", ".join(f"{k} {v}" for k, v in sorted(by.items())))
        return 1
    print(f"ok: no screen asks for a readOnly field, dumps a schema, names the wrong permission, "
          f"needs a parameter nothing carries, wears another screen's route, says a Block A screen "
          f"is out or undoes a 3 October decision ({len(used)} exemption(s), each with its reason)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
