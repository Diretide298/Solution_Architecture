#!/usr/bin/env python3
"""Import the POS v2 build (1 October) as candidate frames for P04: designed, in review, not client-verified.

Chinmay dropped `TICVAI POS Terminal (3).html` on 1 October, kept as
sources/designs/TICVAI_POS_Terminal_v2.html (9.7 MB, excluded from git in .git/info/exclude). It is
OUR improved version of the client-approved terminal (sources/designs/TICVAI_POS_Terminal_client_approved.html),
and the client has not approved it. So nothing here is client-verified:

- the screen's frame becomes the v2 capture, `wireframe.provenance: designed`, `wireframe.status: review`;
- the v2 view goes into a new `wireframe.candidate` block (schema: screens/_schema.yaml, added 1 October):
  file, rev, captured, capture, match, view, differences;
- `wireframe.prototype`, the client-approved view, is not touched. When the client approves v2, the
  candidate becomes the prototype block and the provenance client-verified again.

Captured on 1 October with tools/capture-prototype.mjs and tools/capture-plans/pos-v2.json into
wireframes/incoming/P04-pos-v2/. Only the screens whose view changed in v2 are in the plan; the
screens whose view did not change beyond the shared chrome keep their client-verified frame
(POS-007, 008, 011, 013, 014, 016, 020, 026, 027). The V2-* captures are views with no P04 screen
(sales journal, cart history, reservations and encoding, the shift management panel): they are for
review only and this script skips them. P15 (kitchen display) has no view in either build.

For each captured POS screen this:

1. copies the capture to wireframes/frames/img/ (removing the image of the other extension);
2. imports the fragment through tools/import-design-frames.py under the screen's own batch;
3. writes the screen's `wireframe.candidate` block and sets `provenance: designed`, `status: review`.

Nothing checks that the v2 file is on disk (it is not in git): the capture and the frame are the record.
Idempotent: a second run copies, imports and writes nothing.

    python tools/applied/pos-v2-1-october.py [--apply]
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / "wireframes" / "frames"
YML = ROOT / "screens" / "P04-point-of-sale.yaml"
CAPTURE = ROOT / "wireframes" / "incoming" / "P04-pos-v2"
BUILD = "sources/designs/TICVAI_POS_Terminal_v2.html"
REV = "v2, 1 October 2026 (TICVAI POS Terminal (3).html): ours, not client-approved"
CAPTURED = "2026-10-01"

# How close the v2 view is to the screen's definition. A drawer step, a view that lacks operations
# the definition declares, or one that only partly shows the screen is partial.
MATCH = {
    "POS-000": "exact", "POS-001": "exact", "POS-002": "exact", "POS-003": "partial",
    "POS-004": "partial", "POS-005": "exact", "POS-006": "partial", "POS-012": "partial",
    "POS-021": "exact", "POS-022": "partial", "POS-023": "exact", "POS-025": "exact",
    "POS-028": "partial", "POS-029": "exact",
}

# What the v2 view does that the definition does not, or the reverse. Read against the definition and
# the approved view's `prototype.differences`; a contradiction with a decided audit item is named.
DIFF = {
    "POS-000": (
        "v2 co-brands the sign-in with the venue (name and logo, a demo setting of the build), shows "
        "recent cashiers four at a time with their last shift, adds a cashier-ID entry for anyone not on "
        "the tiles, and switches between a 4-digit PIN and a password (LoginRequest.method takes pin or "
        "password). Badge / RFID, Corporate SSO, the 90 s idle lock and the 'Shift not started · Float "
        "pending' pill stay. As in the approved build: no MFA challenge, no active-session / force-logout, "
        "no role selection, and no denied, offline or emptyNoAccess state."),
    "POS-001": (
        "v2 counts the float on note and coin images (tap the row to count up, or type the quantity) and "
        "runs the hardware check beside the count (six devices, Re-run). A failed device shows Retry device "
        "test, Report to facilities and a reroute hint (open the shift and print to the spare gate B "
        "printer); Report to facilities has no operation on this screen. The expected float and a live "
        "variance ('Matches expected float — no variance') are still shown while counting. No suspend, "
        "resume or reopen, cash movement, no-sale, deposit-box float or role selection, as before."),
    "POS-002": (
        "v2: REFINE chips (available now, today, low capacity, best seller, on sale), availability on each "
        "card ('Next slot 17:30 · 26 left'), On now, an experience Builder and Scan. The cart shows the "
        "inventory hold with its countdown and Extend +2 min, History (cart history: no P04 screen), Hold "
        "sale, and Reserve (a sale reserved without payment: no P04 screen); Charge becomes Proceed to "
        "payment. The F1-F7 function bar replaces the home hot keys on every screen, and the operational "
        "inventory ledger is gone. As before: no game-card issue, transfer or load, no exchange or "
        "reschedule, and promotion codes only inside the Discount dialog."),
    "POS-003": (
        "Still a step of the POS-002 drawer, not a page (the 3 August decision). v2: the visit date is a "
        "business-date card with Change, the entry slot a card with what is left ('59 LEFT') and Change, "
        "then guests by ticket type (adult, child, senior, infant) and group & family bundles at one price. "
        "The cart's inventory hold (countdown, Extend +2 min) is the only hold the cashier sees: there is no "
        "acquire, renew or relinquish of an inventory hold as such."),
    "POS-004": (
        "Still inside the POS-002 drawer, not a full-screen map. v2 adds the section-then-seat flow for a "
        "reserved big-top event (Pluma Circus: date and time, a section map, then the section's seats with "
        "held and sold seats and three price tiers; Back and All sections step back). No seat-hold extend or "
        "recommend, and no booking-fee line."),
    "POS-005": (
        "v2 takes a split on the tender itself (Add to split, Exact, Half, quick amounts) and lists the part "
        "payments taken ('Already taken in part payments'); there is no Split payment tender, where the "
        "definition still has a 'Split payment' button. Tenders: cash, card, contactless, Apple Pay, Google "
        "Pay, guest wallet, gift voucher, complimentary, corporate voucher, prepaid / online. A printer-"
        "offline banner offers the receipt by email. As before: no tip step, no foreign-currency tender, and "
        "no buyer name, address or TRN above the AED 10,000 invoice threshold."),
    "POS-006": (
        "v2 makes Held sales a screen (it was a modal): held sales, parked value, units held and oldest "
        "hold, then each hold with every line, Recall into sale, Print hold slip and Discard hold, and an "
        "empty state ('No held sales on this terminal'). Reached from the cart's Hold sale and F2 Recall "
        "held. Still this terminal only, no search (emptyNoResults is not drawn), and no modify, refund, "
        "exchange or reschedule of a held order, although the definition attaches those overlays."),
    "POS-012": (
        "v2: four order types in the cart (Dine-in, Quick service, Takeaway, Delivery); Delivery asks the "
        "fulfilment source (Own delivery or Delivery partner), and the queue (POS-029) works the orders. "
        "Quick service is a counter order with no guest details, whose number prints on the receipt and "
        "shows on the guest status board. No click-and-collect of merchandise (reserveMerchandise) and no "
        "handover record beyond the queue's stage action."),
    "POS-021": (
        "v2: category tabs with counts (Popular, Mains, Sides, Drinks, Desserts), REFINE chips and Scan; the "
        "cart takes the order type. The header still reads 'kitchen fires on payment', which the 28 "
        "September decision replaced (audit R261: send to kitchen, then charge, for every POS F&B order). "
        "No item-availability (86) toggle, although the definition attaches setItemAvailability."),
    "POS-022": (
        "There is still no send-to-kitchen step at the counter: partner and kiosk orders arrive as Received "
        "and are sent from the queue (POS-029) with Send to kitchen, and a counter order fires on payment, "
        "which the 28 September decision replaced (audit R261: send to kitchen, then charge, for every POS "
        "F&B order). v2 adds the guest status board: takeaway and quick-service numbers under Preparing and "
        "Ready for pickup, mirroring the kitchen display, never a name. Kitchen ticket status and "
        "collection are worked from the queue, not from a screen of their own."),
    "POS-023": (
        "v2: category tabs including Lockers, REFINE chips and Scan; the operational inventory ledger that "
        "the approved build had under Sync is gone. Still no size or variant picker for apparel, and "
        "stockConflict shows only through sync conflicts."),
    "POS-025": (
        "v2: the F1-F7 function bar (Scan ticket, Recall held, Open drawer, Reprint receipt, Reservations, "
        "Encode tickets · inactive, Sales journal) replaces the home hot keys and stays on every screen; the "
        "KPI tiles (shift sales, average basket, open checks, queue now) drill into the Sales journal; the "
        "launcher, the recent transactions with 'Open sales journal', and the venue highlight stay. The 'On "
        "shift' pill opens a Shift management panel (clock out, start break, shift statistics, the cash "
        "drawer, End shift & declare cash). Reservations, Encode tickets, the Sales journal and the shift "
        "panel have no P04 screen. Alerts and device health stay in the top bar."),
    "POS-028": (
        "v2: three halls (Main Hall, Terrace, Majlis rooms), the floor plan drawn to scale with status "
        "filters (vacant, occupied, bill requested, reserved), and the hall's table list with Seat & order, "
        "Recall check, Settle bill and Seat booking. Reservations takes a sitting with party size, the table "
        "held for, the tables that fit and an optional holding deposit. Still no move, merge or close / "
        "clear of a table visit."),
    "POS-029": (
        "v2 adds the guest status board above the lanes (order numbers only, Preparing and Ready for "
        "pickup, mirroring the kitchen display) and quick-service orders beside takeaway, partner, dine-in "
        "and delivery. Each card carries its stage action (Send to kitchen, Mark ready, Served to table, "
        "Mark delivered, Hand over to guest) and Cancel, which has no operation on this screen. No queue "
        "feed-health display."),
}


def q(s):
    """A single-quoted YAML scalar on one line."""
    return "'" + re.sub(r"\s+", " ", str(s)).strip().replace("'", "''") + "'"


def same(a: Path, b: Path) -> bool:
    return b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    apply = ap.parse_args().apply

    man = json.loads((CAPTURE / "manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((ROOT / man["plan"]).read_text(encoding="utf-8"))
    assert man["prototype"] == plan["prototype"] == BUILD, man["prototype"]
    cap = {c["id"]: c for c in man["captured"] if c["id"].startswith("POS-")}
    for c in man["captured"]:
        if c["id"] not in cap:
            print(f"  review only, no P04 screen: {c['id']}: {c['name']}")
    for m in man.get("missing", []):
        print(f"  not captured: {m['id']}")
    assert set(cap) == set(MATCH) == set(DIFF), sorted(set(cap) ^ set(MATCH) | set(cap) ^ set(DIFF))

    batches = json.loads((ROOT / "wireframes" / "design-manifest.json").read_text(encoding="utf-8"))["batches"]
    batch_of = {s.upper(): b["id"] for b in batches for s in b["screens"]}

    n_img = 0
    for sid, c in sorted(cap.items()):
        src = CAPTURE / c["file"]
        dest = FRAMES / "img" / src.name
        stale = [FRAMES / "img" / (sid.lower() + e) for e in (".png", ".jpg") if e != src.suffix]
        stale = [p for p in stale if p.exists()]
        if same(src, dest) and not stale:
            continue
        n_img += 1
        print(f"  image  {sid}: {src.name}" + (f" (removes {', '.join(p.name for p in stale)})" if stale else ""))
        if apply:
            shutil.copyfile(src, dest)
            for p in stale:
                p.unlink()

    n_frame = 0
    for sid in sorted(cap):
        src = CAPTURE / f"{sid.lower()}.html"
        dest = FRAMES / src.name
        if dest.exists() and dest.read_text(encoding="utf-8") == src.read_text(encoding="utf-8"):
            continue
        n_frame += 1
        cmd = [sys.executable, str(ROOT / "tools" / "import-design-frames.py"), batch_of[sid], str(src)]
        if apply:
            r = subprocess.run(cmd + ["--apply"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            ok = r.returncode == 0 and "accepted  " + sid in r.stdout
            print(f"  frame  {sid} ({batch_of[sid]}): {'imported' if ok else 'REFUSED'}")
            if not ok:
                print(r.stdout + r.stderr)
                raise SystemExit(1)
        else:
            print(f"  frame  {sid} ({batch_of[sid]}): to import")

    text = YML.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    screens = {s["id"]: s for s in yaml.safe_load(text)["screens"]}
    no_proto = [sid for sid in cap if not (screens[sid].get("wireframe") or {}).get("prototype")]
    assert not no_proto, f"no wireframe.prototype block to keep: {no_proto}"

    def candidate(sid):
        c = cap[sid]
        return ["    candidate:", f"      file: {BUILD}", f"      rev: {q(REV)}", f"      captured: '{CAPTURED}'",
                f"      capture: wireframes/incoming/P04-pos-v2/{c['file']}", f"      match: {MATCH[sid]}",
                f"      view: {q(c['view'])}", f"      differences: {q(DIFF[sid])}"]

    lines = text.split(nl)
    out, cur, i, in_wf = [], None, 0, False
    placed = set()
    while i < len(lines):
        ln = lines[i]
        mm = re.match(r"^- id: (\S+)", ln)
        if mm:
            cur, in_wf = mm.group(1), False
        if re.match(r"^  \S", ln):
            # Only the screen's own `wireframe:` block: an operation under `apis:` carries a
            # `provenance:` at the same indent, and it is not this one.
            in_wf = ln.startswith("  wireframe:")
        mine = cur in cap and in_wf
        if mine and ln == "    candidate:":
            # An earlier run's block: drop it; it is written again after the prototype block.
            i += 1
            while i < len(lines) and lines[i].startswith("      "):
                i += 1
            continue
        if mine and ln == "    prototype:":
            out.append(ln)
            i += 1
            while i < len(lines) and lines[i].startswith("      "):
                out.append(lines[i])
                i += 1
            out += candidate(cur)
            placed.add(cur)
            continue
        if mine and ln.startswith("    provenance: "):
            ln = "    provenance: designed"
        if mine and ln.startswith("    status: "):
            ln = "    status: review"
        out.append(ln)
        i += 1
    assert placed == set(cap), sorted(set(cap) - placed)
    new = nl.join(out)

    after = {s["id"]: s for s in yaml.safe_load(new)["screens"]}
    assert after.keys() == screens.keys()
    rest = lambda d: {k: v for k, v in d.items() if k != "wireframe"}
    n_yaml = 0
    for sid in screens:
        if sid not in cap:
            assert after[sid] == screens[sid], sid
            continue
        assert rest(after[sid]) == rest(screens[sid]), sid
        w, w0 = after[sid]["wireframe"], screens[sid]["wireframe"]
        assert w["prototype"] == w0["prototype"], f"{sid}: the approved prototype block changed"
        assert {k: v for k, v in w.items() if k not in ("candidate", "provenance", "status")} == \
               {k: v for k, v in w0.items() if k not in ("candidate", "provenance", "status")}, sid
        cd = w["candidate"]
        assert cd["file"] == BUILD and cd["view"] == cap[sid]["view"] and cd["match"] == MATCH[sid], sid
        assert str(cd["captured"]) == CAPTURED and cd["differences"] == re.sub(r"\s+", " ", DIFF[sid]).strip(), sid
        assert w["provenance"] == "designed" and w["status"] == "review", sid
        if w != w0:
            n_yaml += 1
    print(f"P04: {len(cap)} captured screens: {n_img} images, {n_frame} frames, {n_yaml} wireframe blocks to change")
    if apply and new != text:
        with open(YML, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"written {YML.relative_to(ROOT)}")
    if not apply:
        print("\ndry run; pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
