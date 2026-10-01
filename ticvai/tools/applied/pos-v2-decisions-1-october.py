#!/usr/bin/env python3
"""Apply the eight POS v2 decisions of 1 October to the P04 frames: two new candidate frames, and the
design corrections on the candidates pos-v2-1-october.py wrote.

Chinmay approved all eight recommended decisions on the POS v2 build on 1 October ("all recommended");
the register is docs/registers/pos-v2-decisions.md (handoff/pos-v2-decisions.json, POSV2-1 to POSV2-8).
The specification changes (the new screens POS-030 and POS-031, listOrders' new filters, POS-005's split,
recordAttendance on POS-009, KIT-007 and POS-029) are root edits made by hand. This script does the
part that follows the import route of tools/applied/pos-v2-1-october.py:

1. **POS-030 Sales Journal** and **POS-031 Reservations & Group Arrivals** take the v2 views that had no
   P04 screen as their candidate frames. POS-030 is the v2 sales journal (V2-JOURNAL) with the cart
   history (V2-CARTHIST) as its variant: one screen, opened from F7 or from the cart's History.
   POS-031 is the v2 group reservations (V2-GROUPS) with the encode dialog (V2-GROUPS-ENCODE) as its
   variant, and the frame says what is corrected: nothing is encoded before payment (POSV2-2).
   For each: the captures are copied to wireframes/frames/img/ (pos-030.png and pos-030-cart-history.png,
   pos-031.jpg and pos-031-encode.png), a fragment is written to wireframes/incoming/P04-pos-v2/ and
   imported through tools/import-design-frames.py under the screen's batch, and the screen's
   `wireframe.candidate` block is written after its `prototype` block (`provenance: designed`,
   `status: review`, never client-verified: v2 is ours and the client has not approved it).
2. **The candidates of 1 October carry the decisions.** Each `candidate.differences` written by
   pos-v2-1-october.py is rewritten as that script's text, with any clause a decision answered taken
   out, and the decision appended (POS-001, 002, 005, 006, 021, 022, 025, 028, 029). The text is
   always rebuilt from pos-v2-1-october.py's DIFF, so a second run writes nothing; **run this after
   pos-v2-1-october.py** if that one is ever run again, because it writes its own text back.

The v2 file is not in git (sources/designs/TICVAI_POS_Terminal_v2.html, 9.7 MB): the captures in
wireframes/incoming/P04-pos-v2/ and the frames are the record. Idempotent.

    python tools/applied/pos-v2-decisions-1-october.py [--apply]
"""
import argparse
import hashlib
import html
import importlib.util
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
CAPTION = "POS v2 build, ours, not client-approved (1 Oct 2026)"

_spec = importlib.util.spec_from_file_location("pos_v2_1_october", Path(__file__).with_name("pos-v2-1-october.py"))
V2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V2)
BUILD, REV, CAPTURED = V2.BUILD, V2.REV, V2.CAPTURED

# The two new screens. `images` is (capture under CAPTURE/img, frame image name, caption); the first
# is the screen's main view, the second its variant.
NEW = {
    "POS-030": {
        "name": "Sales Journal",
        "images": [
            ("v2-journal.png", "pos-030.png",
             "F7 'Sales journal' (or a Till Home KPI tile) -> first row expanded: line items, transaction "
             "status, Reprint receipt / Email tax invoice / Refund or void"),
            ("v2-carthist.png", "pos-030-cart-history.png",
             "Variant: the same journal opened from the cart's 'History' (Cart history): this terminal by "
             "day; a row opens Reload this cart / Reprint receipt / Email tax invoice"),
        ],
        "match": "partial",
        "view": "F7 'Sales journal' or a Till Home KPI tile -> the journal, first row expanded; the cart's "
                "'History' opens it as Cart history (this terminal, by day), drawn as the variant",
        "differences": (
            "v2 draws two views and the definition makes them one screen (decided 1 October, POSV2-1): the "
            "Sales journal (gross value and settlement tiles, every sale with its pay status, a row "
            "expanding to its lines and transaction status, Reprint receipt, Email tax invoice, Refund or "
            "void) and the Cart history (the cart's History: this terminal's sales by day, Reload this cart). "
            "The definition opens on this terminal and today, filters by terminal, day, customer, payment "
            "method and status (listOrders), hands Refund or void to POS-011 and refunds nothing here, and "
            "reloads a cart with getOrder then addCartLine at today's prices. v2's CSV and Excel export is "
            "not in r2 (a later change: no operation exports orders)."),
    },
    "POS-031": {
        "name": "Reservations & Group Arrivals",
        "images": [
            ("v2-groups.jpg", "pos-031.jpg",
             "Left rail 'Bookings' (F5 'Reservations') -> a group reservation: deposit paid, balance due, "
             "Take payment. Design correction: the tickets shown as encoded inactive are not built; tickets "
             "are issued when the order is paid"),
            ("v2-groups-encode.png", "pos-031-encode.png",
             "Variant: a confirmed, unpaid group (v2 offers 'Encode tickets as Inactive · Pay on arrival'). "
             "Design correction: not built; nothing is encoded before payment (convert, pay, issue)"),
        ],
        "match": "partial",
        "view": "Left rail 'Bookings' (F5 'Reservations') -> a group reservation (deposit paid, balance due, "
                "Take payment); a confirmed unpaid group opens the encode dialog, drawn as the variant",
        "differences": (
            "Design correction (decided 1 October, POSV2-2): v2 encodes a group's tickets as Inactive before "
            "payment ('Encode tickets as Inactive · Pay on arrival', 'VALID AT GATES', 'Set active', "
            "'Activate all on payment', and F6 'Encode tickets · inactive' on the function bar). That is "
            "not built: a reservation creates no entitlement, so nothing is encoded before payment; on "
            "arrival the reservation is converted (convertReservation), paid at POS-005, and the tickets "
            "are issued then. A group's deposit and balance come from the group's order; the balance is "
            "taken at POS-005, and the arrival is recorded with recordGroupCheckIn. v2's New reservation "
            "(Tentative 48 h hold or Confirmed) maps to createReservation with its expiry, and Extend and "
            "Cancel to extendReservation and cancelReservation."),
    },
}

# The candidates written by pos-v2-1-october.py: clauses a decision answered (old, new), then the
# decision. Rebuilt from V2.DIFF every run.
DECIDED = {
    "POS-001": ([], "Design corrections (decided 1 October): the expected float and the live variance "
                    "are not shown while counting; the blind count stands (POSV2-3, audit R080). Report to "
                    "facilities is dropped from the design: no operation is behind it (POSV2-8)."),
    "POS-002": ([("History (cart history: no P04 screen)", "History (the cart history: POS-030 Sales "
                  "Journal)"),
                 ("Reserve (a sale reserved without payment: no P04 screen)", "Reserve (a reservation "
                  "without payment: POS-031)")],
                "Decided 1 October: the cart's History opens POS-030 (POSV2-1) and Reserve opens POS-031, "
                "where a reservation holds capacity and issues no ticket (POSV2-2)."),
    "POS-005": ([("; there is no Split payment tender, where the definition still has a 'Split payment' "
                  "button.", "; there is no Split payment tender.")],
                "Decided 1 October (POSV2-5): the definition follows v2: a split is taken on any tender, "
                "with no separate Split payment button."),
    "POS-006": ([], "Design gap (decided 1 October, POSV2-6): the modify, refund, exchange and reschedule "
                    "overlays stay in the definition; the design must add them to a held sale."),
    "POS-021": ([], "Design correction (decided 1 October, POSV2-4): 'kitchen fires on payment' is wrong; "
                    "audit R261 stands: send to kitchen, then charge."),
    "POS-022": ([], "Design correction (decided 1 October, POSV2-4): a counter order is not fired on "
                    "payment; audit R261 stands: send to kitchen, then charge. The guest status board is "
                    "owned by KIT-007 (POSV2-7)."),
    "POS-025": ([("Reservations, Encode tickets, the Sales journal and the shift panel have no P04 screen.",
                  "")],
                "Decided 1 October: the Sales journal (F7 and the KPI tiles) is POS-030 (POSV2-1) and "
                "Reservations (F5) is POS-031 (POSV2-2). Design corrections: Encode tickets (F6) is not "
                "built, since nothing is encoded before payment (POSV2-2); the Shift management panel drops "
                "'Expected in drawer', the blind count standing (POSV2-3, audit R080), and its Clock out and "
                "breaks call recordAttendance, on POS-009 Staff Roster (POSV2-3)."),
    "POS-028": ([("Still no move, merge or close / clear of a table visit.", "Still no close / clear of a table visit.")],
                "Decided 1 October (POSV2-8): moving and merging tables is deferred until after r2 and taken off "
                "this screen; moveTableVisit and mergeTableVisits stay in the contract and on EMP-058."),
    "POS-029": ([], "Decided 1 October: Cancel is dropped from the design, no operation is behind it "
                    "(POSV2-8); the guest status board is owned by KIT-007 (P15) and this queue mirrors it "
                    "(POSV2-7)."),
}


def q(s):
    return V2.q(s)


def clean(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def decided_text(sid):
    text = clean(V2.DIFF[sid])
    subs, suffix = DECIDED[sid]
    for old, new in subs:
        assert clean(old) in text, f"{sid}: {old!r} is no longer in pos-v2-1-october.py's text"
        text = text.replace(clean(old), clean(new))
    return clean(text + " " + suffix)


def fragment(sid):
    n = NEW[sid]
    parts = [f'<section id="{sid.lower()}" class="proto-frame">']
    for i, (_cap, img, caption) in enumerate(n["images"]):
        style = "display:block;width:100%;height:auto" + (";margin-top:24px" if i else "")
        parts.append(f'<img src="frames/img/{img}" alt="{sid} {html.escape(n["name"])}'
                     f'{" (variant)" if i else ""}, {CAPTION}" style="{style}">')
        parts.append(f'<p style="font:12px sans-serif;color:#667">{CAPTION} · {html.escape(caption)}</p>')
    parts.append("</section>")
    return "".join(parts) + "\n"


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
    assert man["prototype"] == BUILD, man["prototype"]
    captured = {c["file"]: c for c in man["captured"]}
    for sid, n in NEW.items():
        for cap, _img, _c in n["images"]:
            assert f"img/{cap}" in captured, f"{sid}: no capture img/{cap} in the manifest"

    text = YML.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    screens = {s["id"]: s for s in yaml.safe_load(text)["screens"]}
    missing = [sid for sid in NEW if sid not in screens]
    assert not missing, f"add the screens first (root edit): {missing}"
    for sid in DECIDED:
        cd = (screens[sid].get("wireframe") or {}).get("candidate") or {}
        assert cd.get("file") == BUILD, f"{sid}: no v2 candidate block; run pos-v2-1-october.py first"

    # 1. images and frames for the two new screens
    n_img = n_frame = 0
    for sid, n in NEW.items():
        for cap, img, _c in n["images"]:
            src, dest = CAPTURE / "img" / cap, FRAMES / "img" / img
            if same(src, dest):
                continue
            n_img += 1
            print(f"  image  {sid}: {cap} -> {img}")
            if apply:
                shutil.copyfile(src, dest)
        frag = CAPTURE / f"{sid.lower()}.html"
        body = fragment(sid)
        if not frag.exists() or frag.read_text(encoding="utf-8") != body:
            print(f"  fragment {sid}: {frag.relative_to(ROOT)}")
            if apply:
                with open(frag, "w", encoding="utf-8", newline="\n") as f:
                    f.write(body)
    batches = json.loads((ROOT / "wireframes" / "design-manifest.json").read_text(encoding="utf-8"))["batches"]
    batch_of = {s.upper(): b["id"] for b in batches for s in b["screens"]}
    for sid in NEW:
        assert sid in batch_of, f"{sid} is in no batch: run tools/derive-design-manifest.py first"
        src, dest = CAPTURE / f"{sid.lower()}.html", FRAMES / f"{sid.lower()}.html"
        if dest.exists() and src.exists() and dest.read_text(encoding="utf-8") == src.read_text(encoding="utf-8"):
            continue
        n_frame += 1
        if apply:
            cmd = [sys.executable, str(ROOT / "tools" / "import-design-frames.py"), batch_of[sid], str(src), "--apply"]
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            ok = r.returncode == 0 and "accepted  " + sid in r.stdout
            print(f"  frame  {sid} ({batch_of[sid]}): {'imported' if ok else 'REFUSED'}")
            if not ok:
                print(r.stdout + r.stderr)
                raise SystemExit(1)
        else:
            print(f"  frame  {sid} ({batch_of[sid]}): to import")

    # 2. the candidate blocks: new for POS-030/031, decided text for the others
    def new_block(sid):
        n = NEW[sid]
        return ["    candidate:", f"      file: {BUILD}", f"      rev: {q(REV)}", f"      captured: '{CAPTURED}'",
                f"      capture: wireframes/incoming/P04-pos-v2/img/{n['images'][0][0]}",
                f"      match: {n['match']}", f"      view: {q(n['view'])}", f"      differences: {q(n['differences'])}"]

    lines = text.split(nl)
    out, cur, i, in_wf, in_cand = [], None, 0, False, False
    placed = set()
    while i < len(lines):
        ln = lines[i]
        mm = re.match(r"^- id: (\S+)", ln)
        if mm:
            cur, in_wf, in_cand = mm.group(1), False, False
        if re.match(r"^  \S", ln):
            in_wf, in_cand = ln.startswith("  wireframe:"), False
        if in_wf and re.match(r"^    \S", ln):
            in_cand = ln == "    candidate:"
        if cur in NEW and in_wf and ln == "    candidate:":
            i += 1
            while i < len(lines) and lines[i].startswith("      "):
                i += 1
            continue
        if cur in NEW and in_wf and ln == "    prototype:":
            out.append(ln)
            i += 1
            while i < len(lines) and lines[i].startswith("      "):
                out.append(lines[i])
                i += 1
            out += new_block(cur)
            placed.add(cur)
            continue
        if cur in NEW and in_wf and ln.startswith("    provenance: "):
            ln = "    provenance: designed"
        if cur in NEW and in_wf and ln.startswith("    status: "):
            ln = "    status: review"
        if cur in DECIDED and in_cand and ln.startswith("      differences: "):
            # One line, as pos-v2-1-october.py writes it; a deriver may have wrapped it since, so its
            # continuation lines go too.
            while i + 1 < len(lines) and lines[i + 1].startswith("        "):
                i += 1
            ln = f"      differences: {q(decided_text(cur))}"
            placed.add(cur)
        out.append(ln)
        i += 1
    assert placed == set(NEW) | set(DECIDED), sorted(set(NEW) | set(DECIDED) - placed)
    new = nl.join(out)

    after = {s["id"]: s for s in yaml.safe_load(new)["screens"]}
    assert after.keys() == screens.keys()
    rest = lambda d: {k: v for k, v in d.items() if k != "wireframe"}
    n_yaml = 0
    for sid in screens:
        if sid not in NEW and sid not in DECIDED:
            assert after[sid] == screens[sid], sid
            continue
        assert rest(after[sid]) == rest(screens[sid]), sid
        w, w0 = after[sid]["wireframe"], screens[sid]["wireframe"]
        assert w.get("prototype") == w0.get("prototype"), f"{sid}: the approved prototype block changed"
        cd = w["candidate"]
        assert cd["file"] == BUILD and str(cd["captured"]) == CAPTURED, sid
        if sid in NEW:
            assert cd["differences"] == clean(NEW[sid]["differences"]) and cd["match"] == NEW[sid]["match"], sid
            assert w["provenance"] == "designed" and w["status"] == "review", sid
        else:
            assert cd["differences"] == decided_text(sid), sid
            assert {k: v for k, v in cd.items() if k != "differences"} == \
                   {k: v for k, v in w0["candidate"].items() if k != "differences"}, sid
        if w != w0:
            n_yaml += 1
    print(f"P04: {len(NEW)} new candidate frames ({n_img} images, {n_frame} frames), "
          f"{n_yaml} wireframe blocks to change")
    if apply and new != text:
        with open(YML, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"written {YML.relative_to(ROOT)}")
    if not apply:
        print("\ndry run; pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
