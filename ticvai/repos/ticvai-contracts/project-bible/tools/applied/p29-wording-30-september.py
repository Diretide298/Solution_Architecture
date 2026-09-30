# -*- coding: utf-8 -*-
"""Take the internal step name "P29" out of screen and event notes (30 September 2026).

"P29" was the audit step that applied the 29 September decisions. It reads as a platform code (P01-P17),
check-package rule 11 rejects a document naming a platform code no screen file defines, and the notes
are copied into every design batch Claude Design reads. The date says the same thing, so the code goes.
The same pass spells out one "P95/P99" latency label for the same reason.

The two hand-made design folders (B2B-OPTIONS, CMS-FLOW-BUILDER) are not rebuilt by the batch export,
so their BUNDLE.md files get the same edit.

    python tools/applied/p29-wording-30-september.py           # report
    python tools/applied/p29-wording-30-september.py --apply
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = (sorted((ROOT / "screens").glob("P*.yaml")) + sorted((ROOT / "events").glob("*.yaml"))
         + [ROOT / "handoff" / "design-batches" / d / "BUNDLE.md" for d in ("B2B-OPTIONS", "CMS-FLOW-BUILDER")])
RULES = [
    (r"29 September 2026 \(P29\)", "29 September 2026"),
    (r"29 September \(P29\)", "29 September"),
    (r", P29\)", ")"),
    (r"\(P29 pass, ", "("),
    (r" \(P29 pass\)", ""),
    (r"\(P29 group ([A-Z0-9]+)\)", r"(group \1)"),
    (r"P29 pass", "29 September pass"),
    (r"\bP29\b", "the 29 September pass"),
    (r"P95/P99 latency", "95th and 99th percentile latency"),
]


def main():
    apply = "--apply" in sys.argv
    total = 0
    for f in FILES:
        if not f.exists():
            continue
        text = io.open(f, encoding="utf-8").read()
        new, n = text, 0
        for pat, rep in RULES:
            new, k = re.subn(pat, rep, new)
            n += k
        if n:
            total += n
            print(f"  {f.relative_to(ROOT)}: {n}")
            if apply:
                io.open(f, "w", encoding="utf-8", newline="\n").write(new)
    print(f"{total} edit(s)" + ("" if apply else " (report only; --apply to write)") if total else "nothing to do")


if __name__ == "__main__":
    main()
