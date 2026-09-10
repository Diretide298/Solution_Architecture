#!/usr/bin/env python3
"""Write sources/board-reads.json — every panel the client F&B boards name, with its frames.

**This step used to happen once, by hand, into `/tmp/reads.json`.** `derive-board-panel-map.py`
read that scratch file, and from 3 September 16:06 it did not exist: every run since printed
*"keeping the existing map"* and returned, `check-package` passed, and the artefact sat frozen
for five days while looking current. **A deriver whose input lives outside the package is a
deriver that stops without failing.**

The extract is reproducible, which is why it is a tool and not a note. Each frame in the six
`wireframes/FnB Board *.dc.html` files carries an `OPERATIONS` line; this reads the frame's
anchor as its code and the names on that line as its panels, and inverts them into
`panel -> [frame codes]` — the same shape the scratch file held.

It recovers **210 panels**, which is the figure `derive-board-panel-map.py` has cited in its own
docstring since 24 August. The scratch file carried 103 of them; the other 107 were never in the
package at all, and now show up as `unmapped` rather than as nothing.

Run: python3 tools/extract-board-reads.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARDS = sorted((ROOT / "wireframes").glob("FnB Board *.dc.html"))
OUT = ROOT / "sources" / "board-reads.json"

# A frame opens with its own anchor; the panels are the names on its OPERATIONS line. Both are
# read off the rendered board rather than a sidecar, because **the board is the thing the client
# actually sent** and any index beside it is one more artefact to go stale.
FRAME = re.compile(r'(?=<div id="(?:fnb|FNB)-[^"]+")')
ANCHOR = re.compile(r'<div id="([^"]+)"')
OPS_LINE = re.compile(r">OPERATIONS</b>(.*?)</div>", re.S)
TAGS = re.compile(r"<[^>]+>")
NAME = re.compile(r"\b([a-z][A-Za-z0-9]{3,})\b")


def main() -> int:
    if not BOARDS:
        print("  board-reads: no wireframes/FnB Board *.dc.html found")
        return 1

    panels: dict[str, list[str]] = defaultdict(list)
    frames = 0
    for f in BOARDS:
        text = f.read_text(encoding="utf-8", errors="replace")
        for block in FRAME.split(text):
            anchor = ANCHOR.match(block)
            if not anchor:
                continue
            line = OPS_LINE.search(block)
            if not line:
                continue
            frames += 1
            code = anchor.group(1).upper()
            for name in NAME.findall(TAGS.sub("", line.group(1))):
                if code not in panels[name]:
                    panels[name].append(code)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({k: panels[k] for k in sorted(panels)}, indent=1),
                   encoding="utf-8")
    print(f"  board-reads: {len(panels)} panels across {frames} frames "
          f"in {len(BOARDS)} board(s) -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
