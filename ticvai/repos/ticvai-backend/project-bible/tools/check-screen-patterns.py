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
         or a guest account overlay asks for a password again (passwordless,
         CHG-FXS-003)                                                         (CHG-R11-002)
    READ a screen shows data and binds no read, or edits saved data (PUT or
         PATCH) and binds no read that returns it: the r1 gate's G3           (CHG-R1S-004)
         Block A fails on any; outside Block A the count may only fall
         (READ_OUTSIDE_A_CEILING), each one fixed before its block is cut
    NP   a screen a Sprint 1 or 2 task builds says a person must define it, or
         binds no operation: the Sprint 1-2 judging of 4 October           (CHG-FXS-007)
         Sprints 1-2 fail on any; a later sprint's count may only fall
         (NP_LATER_CEILING), each one defined before its sprint is judged

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

# NP: Sprint 1-2 screens the package cannot define, handed to the plan to move out of Sprints 1-2
# (runs/fix-s12/LEDGER.md, 4 October 2026). Each goes when the plan moves it; then the exemption is unused.
NP_OUT = {
    "BO-822": "no operation stores service-recovery automation rules (contract gap CHG-WIR-007)",
    "BO-1069": "no tenant-facing operation reports platform service status (contract gap CHG-WIR-024)",
    "BO-1072": "no staff read of the published API definitions (contract gap CHG-WIR-027)",
    "ADM-408": "no operation approves a prospect's commercial package (contract gap CHG-WIR-024)",
}
for _sid, _why in NP_OUT.items():
    EXEMPT[("NP", _sid, "")] = "moved out of Sprints 1-2 by the plan (ledger, 4 October): " + _why

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
    ("ADM-541", "decisionRecordId"), ("ADM-542", "decisionRecordId"), ("ADM-543", "decisionRecordId"),
    ("ADM-544", "decisionRecordId"), ("ADM-545", "decisionRecordId"), ("ADM-546", "decisionRecordId"),
    ("ADM-548", "decisionRecordId"),
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
    # Guest accounts are passwordless (CHG-FXS-003): the overlay that links a guest checkout to an account is
    # "Create an account" (email, code, verify), never "Set a password" (4 October 2026, CHG-R11-002).
    ("CHG-R11-002", "WEB-013", "passwordless", "linkGuestCheckout"),
    ("CHG-R11-002", "GST-010", "passwordless", "linkGuestCheckout"),
]
# READ outside Block A: 545 on 3 October (430 screens with no read, 115 edits with no read back), found
# by the rule that fixed the 47 in Block A (CHG-R1S-004); 574 once the same day's lineage fix (CHG-R1S-005)
# gave write operations that wrote nothing their tables, so a screen no longer counted such a POST as its
# read. Each is fixed before its block is broken into tasks; until then the count may only fall. Lower this
# number when it does.
READ_OUTSIDE_A_CEILING = 574
# NP after Sprint 2: the screens later sprints build that still say a person must define them or bind
# nothing, 4 October 2026 (CHG-FXS-007). Each is defined before its sprint is judged; lower this number
# when the count falls.
NP_LATER_CEILING = 191

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
        elif rule == "passwordless":
            for o in s.get("overlays") or []:
                if (o.get("confirm") or {}).get("operation") != op:
                    continue
                words = " ".join(str(x or "") for x in (o.get("trigger"), (o.get("confirm") or {}).get("label"),
                                                         o.get("body"))).lower().replace("no password", "").replace("passwordless", "")
                if "password" in words:
                    out.append(("DEC", sid, f"{chg}: overlay {o.get('id')} asks for a password; guest accounts "
                                            f"are passwordless (Create an account: email, code, verify)"))
    return out


def run(only=None):
    pk = sp.Package()
    S = pk.screens
    inb = sp.inbound(S)
    owners = sp.component_owners(S)
    block_a = sp.block_a_screens()
    sprints = sp.planned_sprints() if only in (None, "NP") else {}
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
        if only in (None, "READ") and block_a is not None:
            found += sp.p_read(pk, sid, s)
        if only in (None, "NP") and sprints and sid in sprints:
            found += [(r, i, f"{d} (Sprint {sprints[sid]})") for r, i, d in sp.p_np(pk, sid, s)]
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
    outside = [f for f in found if f[0] == "READ" and block_a is not None and f[1] not in block_a]
    found = [f for f in found if not (f[0] == "READ" and block_a is not None and f[1] not in block_a)]
    if outside:
        print(f"  ratchet READ {len(outside)} outside Block A (ceiling {READ_OUTSIDE_A_CEILING}): each is "
              f"fixed before its block is cut (CHG-R1S-004); --list-read shows them")
        if "--list-read" in args:
            for _, sid, detail in outside:
                print(f"    READ {sid:<9} {detail}")
        if len(outside) > READ_OUTSIDE_A_CEILING:
            found += [("READ", "-", f"{len(outside)} READ findings outside Block A, above the ceiling of "
                                    f"{READ_OUTSIDE_A_CEILING}: a new screen shows or edits data with no read")]
    later = [f for f in found if f[0] == "NP" and not f[2].endswith(("(Sprint 1)", "(Sprint 2)"))]
    found = [f for f in found if f not in later]
    if later:
        print(f"  ratchet NP {len(later)} in Sprints 3 and later (ceiling {NP_LATER_CEILING}): each is "
              f"defined before its sprint is judged (CHG-FXS-007); --list-np shows them")
        if "--list-np" in args:
            for _, sid, detail in later:
                print(f"    NP {sid:<9} {detail}")
        if len(later) > NP_LATER_CEILING:
            found += [("NP", "-", f"{len(later)} NP findings in Sprints 3 and later, above the ceiling of "
                                  f"{NP_LATER_CEILING}: a screen planned later needs a person or binds nothing")]
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
