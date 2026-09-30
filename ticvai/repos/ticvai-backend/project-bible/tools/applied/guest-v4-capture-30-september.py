#!/usr/bin/env python3
"""Replace the Mobile v2 frames of the 17 P02 screens that are views in the client's Mobile App v4.

All 77 P02 frames were captures of the 28 September build (Mobile v2). Mobile App v4 replaced it on
29 September, and 17 screens are views in v4 (handoff/design-batches/apps/1-guest-app/README.md). On
30 September they were captured from v4 with tools/capture-prototype.mjs and the plan
tools/capture-plans/guest-mobile-v4.json, into wireframes/incoming/P02-mobile-v4/ (a fragment per
screen, img/ and manifest.json). A screen whose proof text was missing is not in the manifest, so it
is not touched here.

For each captured screen this:

1. copies the capture to wireframes/frames/img/ (removing the v2 image of the other extension);
2. imports the fragment through tools/import-design-frames.py under the screen's own batch, so the
   importer's rules (id anchor, no document, no script, over 200 bytes) apply as to any frame;
3. rewrites the screen's `wireframe.prototype` block: the v4 file, rev, `verified: '2026-09-30'`,
   the view it was captured from, and the match and differences it already had; and sets
   `wireframe.provenance: client-verified`.

`wireframe.status` is untouched (it describes the board file, check-wireframes). Idempotent: a second
run copies, imports and writes nothing.

    python tools/applied/guest-v4-capture-30-september.py [--apply]
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
CAPTURE = ROOT / "wireframes" / "incoming" / "P02-mobile-v4"
FRAMES = ROOT / "wireframes" / "frames"
YML = ROOT / "screens" / "P02-guest-mobile-app.yaml"
PROTO = "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html"
REV = "mobile v4 (29 September build)"
VERIFIED = "2026-09-30"
SCREENS = ("GST-063 GST-012 GST-007 GST-008 GST-049 GST-041 GST-001 GST-002 GST-003 GST-004 GST-006 "
           "GST-051 GST-053 GST-054 GST-021 GST-022 GST-038").split()


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
    a = ap.parse_args()
    assert (ROOT / PROTO).exists(), PROTO
    man = json.loads((CAPTURE / "manifest.json").read_text(encoding="utf-8"))
    cap = {c["id"]: c for c in man["captured"] if c["id"] in SCREENS}
    for m in man.get("missing", []):
        print(f"  not captured: {m['id']}: {m['reason']}")
    batches = json.loads((ROOT / "wireframes" / "design-manifest.json").read_text(encoding="utf-8"))["batches"]
    batch_of = {s.upper(): b["id"] for b in batches for s in b["screens"]}

    # 1. images
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
        if a.apply:
            shutil.copyfile(src, dest)
            for p in stale:
                p.unlink()

    # 2. frames, through the importer
    n_frame = 0
    for sid in sorted(cap):
        src = CAPTURE / f"{sid.lower()}.html"
        dest = FRAMES / src.name
        if dest.exists() and dest.read_text(encoding="utf-8") == src.read_text(encoding="utf-8"):
            continue
        n_frame += 1
        cmd = [sys.executable, str(ROOT / "tools" / "import-design-frames.py"), batch_of[sid], str(src)]
        if a.apply:
            r = subprocess.run(cmd + ["--apply"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            ok = r.returncode == 0 and "accepted  " + sid in r.stdout
            print(f"  frame  {sid} ({batch_of[sid]}): {'imported' if ok else 'REFUSED'}")
            if not ok:
                print(r.stdout + r.stderr)
                return 1
        else:
            print(f"  frame  {sid} ({batch_of[sid]}): to import")

    # 3. the screen definitions
    text = YML.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    screens = {s["id"]: s for s in yaml.safe_load(text)["screens"]}
    lines = text.split(nl)
    out, cur, i, n_yaml, in_wf = [], None, 0, 0, False
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
            match = old.get("match") if old.get("match") in ("exact", "partial") else "exact"
            block = ["    prototype:", f"      file: {PROTO}",
                     f"      rev: {REV}", f"      verified: '{VERIFIED}'", f"      match: {match}",
                     f"      view: {q(c['view'])}"]
            if old.get("differences"):
                block.append(f"      differences: {q(old['differences'])}")
            out += block
            continue
        if c and ln.startswith("    provenance: "):
            ln = "    provenance: client-verified"
        out.append(ln)
        i += 1
    new = nl.join(out)
    # The rewrite must still parse, and must leave every other screen as it was.
    after = {s["id"]: s for s in yaml.safe_load(new)["screens"]}
    assert after.keys() == screens.keys()
    for sid in screens:
        if sid not in cap:
            assert after[sid] == screens[sid], sid
        else:
            rest = lambda d: {k: v for k, v in d.items() if k != "wireframe"}
            assert rest(after[sid]) == rest(screens[sid]), sid
            p = after[sid]["wireframe"]["prototype"]
            assert p["file"] == PROTO and p["view"] == cap[sid]["view"] and str(p["verified"]) == VERIFIED, sid
            if p != (screens[sid].get("wireframe") or {}).get("prototype"):
                n_yaml += 1
    print(f"\n{len(cap)} captured screens: {n_img} images, {n_frame} frames, {n_yaml} prototype blocks to change")
    if a.apply and new != text:
        with open(YML, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"written {YML.relative_to(ROOT)}")
    if not a.apply:
        print("dry run; pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
