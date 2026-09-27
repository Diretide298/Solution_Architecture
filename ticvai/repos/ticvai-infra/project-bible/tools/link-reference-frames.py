#!/usr/bin/env python3
"""Bring the drawn boards back where the package can see them, and point screens at their frames.

Audit R258 (88 findings; it explains R252's "no wireframe"). On 9 September the Claude Design and
client boards were archived to _dump/wireframes-3-september/ and screens were repointed to generated
frames. _dump/ is gitignored and nothing reads it, so the drawn work never reached ADAM or a
developer, and 133 screens say only, in a note, that they were "designed once".

Two things, both idempotent:

1. **Reference boards.** Copies the archived boards into wireframes/reference/ (tracked), with the
   support.js and logo they load. Each screen whose note names the board that drew it gets
   `derivedFrom: wireframes/reference/<board>` - the schema's field for "the frame this screen's
   layout was taken from". Status and provenance stay as they are: the screen still renders its
   generated frame, and the reference is the drawing to build that frame towards.
2. **Imported frames.** A screen whose frame is in wireframes/frames/<id>.html (drawn by a design
   batch and imported by import-design-frames.py) renders that drawn frame, so its wireframe says
   `provenance: designed` and `status: review` - drawn, waiting for review. When the client verifies
   it, a person sets `approved`.

    python tools/link-reference-frames.py [--apply]
Run tools/refresh.sh afterwards (derive-wireframes, check-wireframes).
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = "--apply" in sys.argv
ARCHIVE = ROOT / "_dump" / "wireframes-3-september"
REF = ROOT / "wireframes" / "reference"
NOTE_BOARD = re.compile(r"Drawn by Claude Design on `([^`]+)`")

copied = 0
if ARCHIVE.is_dir():
    for f in sorted(ARCHIVE.glob("*.dc.html")):
        target = REF / f.name
        if not target.exists() or target.read_bytes() != f.read_bytes():
            copied += 1
            if APPLY:
                REF.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
    for dep in ("support.js", "assets/ticvai-light-logo.png"):
        src = ROOT / "wireframes" / dep
        if src.exists() and APPLY:
            (REF / dep).parent.mkdir(parents=True, exist_ok=True)
            if not (REF / dep).exists() or (REF / dep).read_bytes() != src.read_bytes():
                shutil.copy2(src, REF / dep)
available = {f.name for f in ARCHIVE.glob("*.dc.html")} if ARCHIVE.is_dir() else {f.name for f in REF.glob("*.dc.html")}
frames = {f.stem.upper() for f in (ROOT / "wireframes" / "frames").glob("*.html")}

linked = drawn = missing = 0
for path in sorted((ROOT / "screens").glob("P*.yaml")):
    raw = path.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(eol)
    out, i, sid, changed = [], 0, None, False
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^- id: (\S+)\s*$", line)
        if m:
            sid = m.group(1)
        if re.match(r"^  wireframe:\s*$", line) and sid:
            j = i + 1
            while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()):
                j += 1
            block = lines[i + 1:j]
            text = eol.join(block)
            new = list(block)
            board = NOTE_BOARD.search(text)
            if board and not any(b.lstrip().startswith("derivedFrom:") for b in block):
                if board.group(1) in available:
                    at = next((k + 1 for k, b in enumerate(new) if b.lstrip().startswith("board:")), len(new))
                    new.insert(at, f"    derivedFrom: wireframes/reference/{board.group(1)}")
                    linked += 1
                else:
                    missing += 1
            if sid in frames:
                before = list(new)
                new = [re.sub(r"^    provenance: generated\s*$", "    provenance: designed", b) for b in new]
                new = [re.sub(r"^    status: notStarted\s*$", "    status: review", b) for b in new]
                if new != before:
                    drawn += 1
            if new != block:
                changed = True
            out += [line] + new
            i = j
            continue
        out.append(line)
        i += 1
    if changed and APPLY:
        path.write_bytes(eol.join(out).encode("utf-8"))

print(f"reference boards to copy: {copied} (into wireframes/reference/)")
print(f"screens linked to their drawn reference board: {linked}; note names a board not in the archive: {missing}")
print(f"screens whose imported frame is now provenance designed, status review: {drawn}")
print("applied - now run tools/refresh.sh" if APPLY else "dry run - pass --apply")
