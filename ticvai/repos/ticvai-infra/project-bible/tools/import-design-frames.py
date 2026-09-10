#!/usr/bin/env python3
"""Take frames back from a Claude Design session, and refuse the ones that are not what was asked.

**A frame is one screen, keyed by its id** — `wireframes/frames/pos-005.html`. `derive-wireframes`
uses it in place of the frame it would have drawn, so the drawn work slots into the board that
already carries the navigation, the workshop badge, the machine and the overlays. Nothing built
here can lose those, because they are rendered around the frame rather than inside it.

**Why per screen and not per board.** Every board Claude Design produced before 10 September was a
whole file, which is why 155 of them ended up archived: a file is all-or-nothing, it goes stale as
a unit, and it competes with the generator for ownership of the navigation. A frame cannot. Half a
batch imported is half a batch drawn, and the manifest counts it truthfully.

**What is refused, and why each rule exists.**

- **A frame for a screen not in the batch.** A session that drifts onto neighbouring screens is a
  session that has lost the plot; taking the work would hide that.
- **A frame whose id does not appear in its own markup.** The anchor is how a board links to it —
  `check-wireframes` calls a broken one *a click that silently does nothing*.
- **A whole document.** `<html>`, `<head>` or `<body>` means a page was returned, not a frame; it
  would nest a document inside a board and break every style around it.
- **A `<script>`.** Boards are read, not run. A frame that needs JavaScript to make sense is a
  prototype, and belongs in the app build rather than on a review board.
- **Anything under 200 bytes.** A placeholder that says *TODO* is worse than no frame: the manifest
  would count the screen as drawn.

    python3 tools/import-design-frames.py P01-cart-checkout-01 <dir-or-file> [--apply]

Idempotent: importing the same frame twice replaces it and reports it as unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "wireframes" / "design-manifest.json"
FRAMES = ROOT / "wireframes" / "frames"

MIN_BYTES = 200


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def fault(sid: str, text: str) -> str | None:
    """What is wrong with this frame, or None."""
    low = text.lower()
    # **Structure first, size second.** A 62-byte `<html>` page failed the size gate before the
    # document gate, and the message told the reader to pad it out rather than to stop returning
    # pages. Order the checks by what is most wrong, not by what is cheapest to test.
    # **The tag has to end where the name ends.** A plain substring test for `<head` matches
    # `<header>`, which is an ordinary element in a frame -- the first frame ever put through this
    # tool was refused for being a document because it opened with a header. The tag name must be
    # followed by whitespace, `>` or `/`, or it is a different tag that merely starts the same.
    for tag in ("html", "head", "body"):
        if re.search(r"<%s[\s/>]" % tag, low):
            return "contains <%s> — this is a document, not a frame" % tag
    if re.search(r"<script[\s/>]", low):
        return "contains <script> — a board is read, not run"
    if len(text.encode("utf-8")) < MIN_BYTES:
        return f"under {MIN_BYTES} bytes — a placeholder counted as drawn is worse than no frame"
    if not re.search(r'id="%s"' % re.escape(sid.lower()), text, re.I):
        return f'no element carries id="{sid.lower()}" — the board could not link to it'
    return None


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("source", help="a directory of <screen-id>.html, or one such file")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if not MANIFEST.exists():
        print("no design-manifest.json — run tools/derive-design-manifest.py first")
        return 1
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    batch = next((b for b in man["batches"] if b["id"] == a.batch), None)
    if not batch:
        print(f"no batch {a.batch!r} in the manifest")
        return 1
    expected = {s.upper() for s in batch["screens"]}

    src = pathlib.Path(a.source)
    files = sorted(src.glob("*.html")) if src.is_dir() else [src]
    if not files:
        print(f"nothing to import — no .html under {src}")
        return 1

    take, reject, unchanged = [], [], []
    for f in files:
        sid = f.stem.upper()
        text = f.read_text(encoding="utf-8", errors="replace")
        if sid not in expected:
            reject.append((f.name, f"{sid} is not in {a.batch} — that batch is "
                                   f"{', '.join(sorted(expected))}"))
            continue
        why = fault(sid, text)
        if why:
            reject.append((f.name, why))
            continue
        dest = FRAMES / f"{sid.lower()}.html"
        if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == \
                hashlib.sha256(text.encode("utf-8")).hexdigest():
            unchanged.append(sid)
            continue
        take.append((sid, dest, text))

    for name, why in reject:
        print(f"  REFUSED  {name}: {why}")
    for sid in unchanged:
        print(f"  unchanged {sid}")
    for sid, _d, _t in take:
        print(f"  accepted  {sid}")

    # **What is still undrawn, counting what this run is about to accept.** The parenthesis
    # mattered: without it the conditional bound to the whole expression, the subtraction never
    # happened, and the tool named a screen as undrawn in the same breath as accepting it.
    on_disk = {f.stem.upper() for f in FRAMES.glob("*.html")} if FRAMES.exists() else set()
    missing = sorted(expected - {sid for sid, _d, _t in take} - set(unchanged) - on_disk)
    if missing:
        print(f"\n  still undrawn in {a.batch}: {', '.join(missing)}")

    print(f"\n{len(take)} accepted · {len(unchanged)} unchanged · {len(reject)} refused")
    if reject:
        print("**A refused frame is not a failed batch.** Fix what is named above and import "
              "again — the accepted ones are already in.")
    if not a.apply:
        print("\nrun with --apply to write")
        return 0

    # **Do not announce a write that did not happen.** With every frame refused the tool still
    # printed "written to wireframes/frames/", which reads as success.
    if not take:
        print("\nnothing accepted — nothing written")
        return 1 if reject else 0

    FRAMES.mkdir(parents=True, exist_ok=True)
    for _sid, dest, text in take:
        dest.write_text(text, encoding="utf-8")
    print(f"\nwritten to {FRAMES.relative_to(ROOT)}/")
    print("run tools/derive-wireframes.py to see them on the boards, then "
          "tools/derive-design-manifest.py to update what is left")
    return 0


if __name__ == "__main__":
    sys.exit(main())
