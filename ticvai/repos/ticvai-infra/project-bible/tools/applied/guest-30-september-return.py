#!/usr/bin/env python3
"""Import the 30 September design return (WebApp_30thSep.zip) as client-verified frames, P01 and P02.

The return is the client-approved guest build with the 30 September website feedback in it
(CLIENT-RESPONSE-30SEP.md: group booking with a headcount, multi-park counters, surf session tickets,
the swim-ability answer, transport stations and departures, popular route cards). Its text layer is in
sources/designs/guest-rev3-30-september/ (the images are byte-identical to the 28 and 29 September
folders, which the capture plans use as asset roots; the two 24 MB single-file builds stay out).

Captured on 1 October with tools/capture-prototype.mjs:

- P02: tools/capture-plans/guest-mobile-v4.json -> wireframes/incoming/P02-mobile-v4/. The 17 views
  first captured on 30 September, re-taken from the 30 September build; GST-021 moved onto the walking
  navigation view (the 3D map following the route, MoM 4.8); and GST-076 to GST-079, the intercity
  transport screens, which cited the superseded Mobile v2 build and are views in v4 now.
- P01: tools/capture-plans/guest-web-v2.json -> wireframes/incoming/P01-web-v2/ (viewport mode,
  1440 x 900). The screens this return or the 29 September audit changed on the website: WEB-005,
  WEB-006, WEB-049 (the booking flows of the 30 September feedback), the At the venue tabs (WEB-036,
  039, 040, 041, 042, 043, 046), and WEB-050 from the Visit Planner, which had no frame.

A screen whose proof text was missing is not in the manifest, so it is not touched. For each captured
screen this:

1. copies the capture to wireframes/frames/img/ (removing the image of the other extension);
2. imports the fragment through tools/import-design-frames.py under the screen's own batch;
3. rewrites the screen's `wireframe.prototype` block (file, rev, `verified`, the view it was captured
   from, match, differences) and sets `wireframe.provenance: client-verified`.

`differences` keeps what the screen already said, with what this return changes appended (DIFF_ADD),
or is replaced where the old text described a superseded build (DIFF_SET). `wireframe.status` is
untouched. Idempotent: a second run copies, imports and writes nothing.

    python tools/applied/guest-30-september-return.py [--apply]
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
VERIFIED = "2026-10-01"
DESIGNS = "sources/designs/guest-rev3-30-september/"

PLATFORMS = {
    "P02": {
        "yml": ROOT / "screens" / "P02-guest-mobile-app.yaml",
        "capture": ROOT / "wireframes" / "incoming" / "P02-mobile-v4",
        "rev": {DESIGNS + "TICVAI Mobile App v4.dc.html": "mobile v4 (30 September build)"},
    },
    "P01": {
        "yml": ROOT / "screens" / "P01-guest-web-storefront.yaml",
        "capture": ROOT / "wireframes" / "incoming" / "P01-web-v2",
        "rev": {DESIGNS + "TICVAI Guest Booking v2.dc.html": "rev 3 (30 September build)",
                DESIGNS + "TICVAI Visit Planner.dc.html": "Visit Planner (30 September build)"},
    },
}

NOT_YET = ("pending in design: specified, and built from the definition until the design shows it "
           "(handoff/design-batches/apps/1-guest-app/README.md)")

# Match where the new view is not the old one's equal.
MATCH = {"GST-077": "partial"}

# Differences replaced: the old text described the Mobile v2 build or a view that is gone.
DIFF_SET = {
    "GST-021": ("The walking navigation follows the route in 3D, with turn-by-turn above the map and a live "
                "position (ADR-0069). The 2D/3D choice is a demo setting of the prototype (Config, Maps: 3D or "
                "2D), not a switch the guest has, and neither the 3D-unavailable state (map3dUnavailable) nor "
                "the weak-GPS state (weakGps, \"Position approximate\") is drawn: both " + NOT_YET + "."),
    "GST-038": ("The live Map view renders the park in 3D with the route and the position dot (2D when the "
                "prototype's Maps setting is 2D). No guest-facing 2D/3D switch, and no map3dUnavailable or "
                "weakGps state: both " + NOT_YET + "."),
    "GST-076": ("Mobile puts stations, date, departures and passengers on one screen (Plan your trip). The "
                "route opens with its stations filled in and the departures listed without a search "
                "(30 September); Popular routes, the route cards, is the first transport product. The route "
                "map needs a street-map tile provider (the capture shows the provider's API-key watermark; "
                "audit R038)."),
    "GST-077": ("The chosen departure's stops are the route map above the departures, not a stop list; the "
                "passengers sit under the departures on the same screen (Plan your trip)."),
    "WEB-049": ("30 September: the route opens with its stations filled in and the departures listed without "
                "a search; the time-period buttons filter them. The engine's other transport flow, Popular "
                "routes (card view), is route cards with a from-fare and Book, then the date, the departures "
                "and the passengers. The route map needs a street-map tile provider (audit R038)."),
    "WEB-050": ("Single-park planner: no \"Which park each day?\" step, no shops or kiosks as plan stops and no "
                "preferenceNotAtVenue (MoM 4.7, 30 September); these are " + NOT_YET + "."),
}

# Differences extended: what this return adds over the view the screen already cited.
DIFF_ADD = {
    "WEB-005": ("30 September: the guest counters take their price from the ticket chosen (2 park ticket, three "
                "adults: one line, AED 1,425), and Group / school booking starts from four group tickets with "
                "a typed headcount. The same flow's Read more panel still prices guests at single-park rates "
                "(Adult AED 325, Infant AED 475): a prototype defect; the counters on the page are the "
                "reference."),
    "WEB-006": ("30 September: a session's tickets (Surfer, Junior surfer, Spectator) appear once the session "
                "is chosen, and choosing it adds nothing to the cart."),
    "WEB-039": ("The map has a 3D view / 2D plan switch (\"Same plan, drawn two ways\"); no map3dUnavailable or "
                "weakGps state is drawn."),
    "WEB-042": ("29 September: collect at the gate, at the car park kiosk, or delivered home, with a "
                "collection code after paying."),
}


def q(s):
    """A single-quoted YAML scalar on one line."""
    return "'" + re.sub(r"\s+", " ", str(s)).strip().replace("'", "''") + "'"


def same(a: Path, b: Path) -> bool:
    return b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()


def differences(sid, old):
    if sid in DIFF_SET:
        return DIFF_SET[sid]
    prev = old.get("differences")
    add = DIFF_ADD.get(sid)
    if not add:
        return prev
    if prev and add in prev:
        return prev
    return f"{prev} {add}" if prev else add


def platform(code, cfg, batch_of, apply):
    man = json.loads((cfg["capture"] / "manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((ROOT / man["plan"]).read_text(encoding="utf-8"))
    cap = {c["id"]: dict(c, prototype=c.get("prototype") or man["prototype"]) for c in man["captured"]}
    for m in man.get("missing", []):
        print(f"  {code} not captured: {m['id']}: {m['reason']}")
    for c in cap.values():
        assert c["prototype"] in cfg["rev"], c
        assert (ROOT / c["prototype"]).exists(), c["prototype"]
    assert plan["prototype"] == man["prototype"]

    n_img = 0
    for sid, c in sorted(cap.items()):
        src = cfg["capture"] / c["file"]
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
        src = cfg["capture"] / f"{sid.lower()}.html"
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

    yml = cfg["yml"]
    text = yml.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    screens = {s["id"]: s for s in yaml.safe_load(text)["screens"]}
    missing_block = [sid for sid in cap if not (screens[sid].get("wireframe") or {}).get("prototype")]
    assert not missing_block, f"no wireframe.prototype block to rewrite: {missing_block}"
    lines = text.split(nl)
    out, cur, i, in_wf = [], None, 0, False
    while i < len(lines):
        ln = lines[i]
        mm = re.match(r"^- id: (\S+)", ln)
        if mm:
            cur, in_wf = mm.group(1), False
        if re.match(r"^  \S", ln):
            # Only the screen's own `wireframe:` block: an operation under `apis:` has a
            # `provenance:` at the same indent, and it is not this one.
            in_wf = ln.startswith("  wireframe:")
        c = cap.get(cur) if in_wf else None
        if c and ln == "    prototype:":
            i += 1
            while i < len(lines) and lines[i].startswith("      "):
                i += 1
            old = (screens[cur].get("wireframe") or {}).get("prototype") or {}
            match = MATCH.get(cur) or (old.get("match") if old.get("match") in ("exact", "partial") else "exact")
            block = ["    prototype:", f"      file: {c['prototype']}",
                     f"      rev: {cfg['rev'][c['prototype']]}", f"      verified: '{VERIFIED}'",
                     f"      match: {match}", f"      view: {q(c['view'])}"]
            diff = differences(cur, old)
            if diff:
                block.append(f"      differences: {q(diff)}")
            out += block
            continue
        if c and ln.startswith("    provenance: "):
            ln = "    provenance: client-verified"
        out.append(ln)
        i += 1
    new = nl.join(out)
    after = {s["id"]: s for s in yaml.safe_load(new)["screens"]}
    assert after.keys() == screens.keys()
    n_yaml = 0
    rest = lambda d: {k: v for k, v in d.items() if k != "wireframe"}
    for sid in screens:
        if sid not in cap:
            assert after[sid] == screens[sid], sid
            continue
        assert rest(after[sid]) == rest(screens[sid]), sid
        p = after[sid]["wireframe"]["prototype"]
        assert p["file"] == cap[sid]["prototype"] and p["view"] == cap[sid]["view"] and str(p["verified"]) == VERIFIED, sid
        assert after[sid]["wireframe"]["provenance"] == "client-verified", sid
        if after[sid]["wireframe"] != screens[sid].get("wireframe"):
            n_yaml += 1
    print(f"{code}: {len(cap)} captured screens: {n_img} images, {n_frame} frames, {n_yaml} wireframe blocks to change")
    if apply and new != text:
        with open(yml, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"written {yml.relative_to(ROOT)}")
    return len(cap)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    batches = json.loads((ROOT / "wireframes" / "design-manifest.json").read_text(encoding="utf-8"))["batches"]
    batch_of = {s.upper(): b["id"] for b in batches for s in b["screens"]}
    for code, cfg in PLATFORMS.items():
        platform(code, cfg, batch_of, a.apply)
    if not a.apply:
        print("\ndry run; pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
