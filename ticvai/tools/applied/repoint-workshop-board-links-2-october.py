#!/usr/bin/env python3
"""Re-point the static workshop boards' links at the board that now holds each screen (2 October 2026).

**One-off, already applied (CHG-GTB-009).** The `WS## ...` boards are static since `derive-pack-boards.py`
was retired on 10 September; each carries links like `P09%20TICVAI%20Web.dc.html#adm-320` to the platform
board that renders the screen. The ADM-049 move (CHG-MOV-001..010) re-pointed its own links, but the
approvals, communication and partner move of the same day (`move-approvals-comms-partner-2-october.py`)
moved screens from P09 and P10 to P08 and left 181 links on nine boards pointing at boards that no longer
render them. check-wireframes (rule 4, hrefs across every board) failed the r2 full refresh on them.

For every href `<P## board>.dc.html#<id>` on a WS board, the screen id is looked up in `screens/P*.yaml`;
when another platform now holds it, the href names that platform's `wireframeBoard`. A link to a screen no
platform defines is reported and left alone. Idempotent: a second run changes nothing.

    python3 tools/applied/repoint-workshop-board-links-2-october.py [--apply]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

import yaml

ROOT = Path(__file__).resolve().parents[2]
HREF = re.compile(r'href="(P\d\d[^"#]*\.dc\.html)#([a-z]{2,5}-\d{3,4})"')


def main() -> int:
    apply = "--apply" in sys.argv[1:]
    board_of: dict[str, str] = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        board = ((doc.get("platform") or {}).get("wireframeBoard") or "").split("/")[-1]
        for s in doc.get("screens") or []:
            board_of[s["id"]] = board
    changed, unknown = 0, set()
    for f in sorted((ROOT / "wireframes").glob("WS*.dc.html")):
        text = f.read_bytes().decode("utf-8")
        n = 0

        def fix(m: re.Match) -> str:
            nonlocal n
            sid = m.group(2).upper()
            want = board_of.get(sid)
            if not want:
                unknown.add(sid)
                return m.group(0)
            if unquote(m.group(1)) == want:
                return m.group(0)
            n += 1
            return f'href="{quote(want)}#{m.group(2)}"'

        new = HREF.sub(fix, text)
        if n:
            changed += n
            print(f"  {f.name}: {n} link(s) re-pointed")
            if apply:
                f.write_bytes(new.encode("utf-8"))
    if unknown:
        print(f"  {len(unknown)} linked screen(s) no platform defines, left alone: {sorted(unknown)[:10]}")
    print(f"{changed} link(s) {'re-pointed' if apply else 'to re-point (dry run; --apply writes)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
