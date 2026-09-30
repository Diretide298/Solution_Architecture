#!/usr/bin/env python3
"""Record the 19 changed Block A guest-app screens drawn by Claude Code in the Mobile App v4 look.

Mobile App v4 (29 September) replaced the 28 September Mobile v2 build the P02 frames were captured
from. Seventeen P02 screens are views in v4 and are re-captured; these nineteen changed on
29 September and v4 has no view for them, so on 30 September Claude Code drew each one as a frame in
the v4 look (tokens, type, cards, tab bar and icons lifted from the v4 file itself) and imported it
with tools/import-design-frames.py (wireframes/frames/<id>.html). The same frames are assembled in
handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html, and what the operations
could not provide is in FINDINGS.md beside it.

**Not client-verified.** Nobody on the client side has seen these frames; they await the client's
design reviewer. So `wireframe.provenance` is `designed` -- the value the eight Claude Design frames of
29 September carry (tools/applied/client-prototypes-29-september.py), because the vocabulary
check-wireframes and _schema.yaml accept (generated, designed, client-verified) has no value for a
frame an agent drew; `wireframe.source` and `wireframe.note` say who drew it and that it is not
verified, and `wireframe.prototype` points at v4 with `match: none`. The Mobile v2 view each screen
used to cite is kept in the prototype note, since v2 is superseded rather than wrong.

`wireframe.status` is untouched: it describes the design workflow, and the 29 September script left
it alone for the same kind of frame. Idempotent: every block is rebuilt from the constants below, so
a second run writes nothing.

    python tools/applied/guest-v4-drawn-30-september.py [--apply]
"""
import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
YML = ROOT / "screens" / "P02-guest-mobile-app.yaml"
V4 = "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html"
V2 = "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html"
FRAMES = ROOT / "wireframes" / "frames"
WORKING = "handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html"

# The Mobile v2 (28 September) view each screen cited before v4 replaced it: (view, match, differences).
V2_VIEW = {
    'GST-059': ('Account → All screens → Wave 3 → Plan my day – in progress', 'exact', 'Mobile v4 draws no in-progress view of the plan; built from this definition in the v4 style.'),
    'GST-019': ('Account → All screens → Wave 2 → Order history', 'exact', None),
    'GST-039': ('Account → All screens → Wave 1 → Profile (also Account → Profile)', 'exact', 'Emirates ID upload is on Profile in the prototype; the YAML has uploadGuestDocument on GST-066. Account also has a "Saved guests (heights on file)" row that no screen defines.'),
    'GST-042': ('Account → All screens → Wave 1 → Simple registration & OTP (same #ident screen) + "Log in or register" sheet from home', 'partial', 'Prototype has email code, Apple and Google only; the YAML also has password login, UAE Pass and explicit registration.'),
    'GST-066': ('Account → All screens → Wave 2 → Privacy & my data (#privacy; also Account → Data & privacy)', 'exact', 'The prototype labels this screen "GST-070 · Your data" (aria-label "GST-070 Data and privacy"), but GST-070 is Reserve a Table in the YAML, so the label is wrong. Document upload is on Profile instead.'),
    'GST-073': ('Account → All screens → Wave 2 → Security & sign-in', 'partial', 'Prototype offers two-step verification and a trusted-device skip, but the YAML says guests have no second factor (R167). Either remove the toggle from the prototype or reopen the decision.'),
    'GST-048': ('Account → All screens → Wave 2 → Upsell / cross-sell', 'exact', None),
    'GST-050': ('Account → All screens → Wave 3 → Resource booking – cabana; Rev 3 feedback → Cabana map', 'partial', 'Rev 3 books from a map, with a hold countdown and sold-out cabanas; the YAML is a list with addCartLine and no hold. YAML GST-070 also says cabanas are booked by staff (R073c), which contradicts both this screen and the prototype.'),
    'GST-056': ('Account → All screens → Wave 2 → Bundle package', 'exact', None),
    'GST-058': ('Account → All screens → Wave 3 → Resource availability (cabana); Rev 3 feedback → Cabana map', 'exact', 'The Rev 3 cabana map puts availability and booking on one screen.'),
    'GST-074': ('Account → All screens → Rev 3 feedback → Cabana map (r3cabmap)', 'exact', None),
    'GST-075': ('Account → All screens → Rev 3 feedback → Meeting room by the hour (r3room)', 'exact', None),
    'GST-009': ('Account → All screens → Wave 1 → Review & payment; also the "Confirm and pay" sheet in the booking flow', 'exact', 'Prototype offers Tabby and wallet credit as payment methods; the YAML does not name them.'),
    'GST-031': ('Account → All screens → Wave 2 → AI concierge – home', 'exact', None),
    'GST-032': ('Account → All screens → Wave 2 → AI concierge – chat', 'exact', None),
    'GST-052': ('Account → All screens → Wave 3 → Suggested itineraries', 'exact', 'Mobile v4 draws no ready-made plans list: its Plan tab goes straight to the questions. Built from this definition in the v4 style.'),
    'GST-011': ('Account → All screens → Wave 2 → Wallet overview', 'exact', None),
    'GST-015': ('Account → All screens → Wave 2 → Memberships; billing in "Also built, not in the plan" → Membership billing (#billing)', 'exact', 'Prototype splits the screen in two (benefits and delegation vs billing statement and dunning retries).'),
    'GST-036': ('Account → All screens → Wave 2 → Loyalty & rewards', 'exact', None),
}


def block(sid):
    view, match, diff = V2_VIEW[sid]
    was = f"Mobile v2 (28 September, superseded by v4) showed it at: {view} ({match})."
    if diff:
        was += f" What v2 did differently: {diff}"
    return {
        "provenance": "designed",
        "board": f"wireframes/P02 Guest App.dc.html#{sid.lower()}",
        "prototype": {
            "file": V4,
            "rev": "Mobile App v4, 29 September 2026",
            "match": "none",
            "note": ("Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the "
                     "v4 look (the frame on this screen's board, wireframes/frames/" + sid.lower() + ".html, and "
                     "#" + sid + " in " + WORKING + "). NOT client-verified: awaiting the client's design "
                     "reviewer. Build the layout from that frame and this definition. " + was),
        },
        "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
        "note": ("**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, "
                 "awaiting the client's design reviewer.** `provenance: designed` because the accepted "
                 "vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design "
                 "frames of 29 September carry. Gaps the operations leave are in "
                 "handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."),
    }


def render(sid, status, indent="  "):
    d = {"status": status}
    d.update(block(sid))
    text = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=110, default_flow_style=False)
    return [indent + "wireframe:"] + [indent + "  " + ln if ln else ln for ln in text.rstrip("\n").split("\n")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    assert (ROOT / V4).exists(), V4
    missing = [s for s in V2_VIEW if not (FRAMES / (s.lower() + ".html")).exists()]
    if missing:
        raise SystemExit(f"no drawn frame on disk for {missing}: import them first (tools/import-design-frames.py)")
    text = YML.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    out, cur, i, done = [], None, 0, []
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^- id: (\S+)\s*$", ln)
        if m:
            cur = m.group(1)
        if cur in V2_VIEW and ln == "  wireframe:":
            j = i + 1
            status = "notStarted"
            while j < len(lines) and (lines[j].startswith("    ") or lines[j] == ""):
                sm = re.match(r"^    status: (\S+)", lines[j])
                if sm:
                    status = sm.group(1)
                j += 1
            out += render(cur, status)
            done.append(cur)
            i = j
            continue
        out.append(ln)
        i += 1
    absent = sorted(set(V2_VIEW) - set(done))
    if absent:
        raise SystemExit(f"no wireframe block found for {absent}")
    new = nl.join(out)
    # The file must still parse, and every rewritten block must read back as written.
    doc = yaml.safe_load(new)
    by = {s["id"]: s for s in doc["screens"]}
    for sid in V2_VIEW:
        w = by[sid]["wireframe"]
        assert w["provenance"] == "designed" and w["prototype"]["match"] == "none", sid
        assert w["prototype"]["file"] == V4 and "NOT client-verified" in w["prototype"]["note"], sid
    changed = new != text
    print(f"P02: {len(done)} wireframe blocks rebuilt ({'changed' if changed else 'unchanged'})")
    if a.apply and changed:
        with open(YML, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print("written screens/P02-guest-mobile-app.yaml")
    elif not a.apply:
        print("dry run; pass --apply")


if __name__ == "__main__":
    main()
