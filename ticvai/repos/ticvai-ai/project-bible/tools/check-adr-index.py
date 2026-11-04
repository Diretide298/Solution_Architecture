#!/usr/bin/env python3
"""The ADR index says what each ADR file says about its own status.

**3 November 2026** (r13 system review A-12; the lead, 3 November 2026: "All four, one release"; CHG-R14J-040). ADR-0065
read "**Status:** Accepted · 1 October 2026" in its own file and "**Proposed** - waiting on Chinmay" in the index
(docs/adr/README.md), so whether browse availability may be cached depended on which file a developer opened. The
index is written by hand, and check-package rule 10 checks only that a status line leads with a word of the
vocabulary, never that the index agrees with the file.

    AI-STATUS    an ADR's index row leads with a different state (Accepted, Accepted in part, Proposed, Superseded)
                 than its file's Status line, or a superseded ADR's row names other successors than its file
    AI-MISSING   an ADR file with no index row, or an index row naming no file

`--self-test` runs the rules on made-up rows.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "AI-STATUS": "an ADR's index row and its file's Status line lead with different states, or a superseded ADR's "
                 "row and file name different successors (CHG-R14J-040, review A-12)",
    "AI-MISSING": "an ADR file with no row in docs/adr/README.md, or a row naming no file (CHG-R14J-040)",
}
ADR_DIR = g.ROOT / "docs" / "adr"
# Longest first, so "Accepted in part" is not read as "Accepted".
STATES = ("Accepted in part", "Accepted", "Proposed", "Superseded")
ROW = re.compile(r"^\|\s*\[(\d{4})\]\(([^)]+)\)\s*\|[^|]*\|([^|]*)\|")


def plain(text: str) -> str:
    """Markdown emphasis and links reduced to their words."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*_`]", "", text).strip()


def state_of(text: str):
    t = plain(text)
    return next((s for s in STATES if t.lower().startswith(s.lower())), None)


def successors(text: str) -> set:
    """The ADR numbers a 'Superseded by ...' status names, up to the first dash or full stop."""
    t = plain(text)
    m = re.match(r"superseded by (.*?)(?:\s[—–-]\s|\.\s|$)", t, re.I)
    return {int(n) for n in re.findall(r"(?:ADR-)?(\d{4})\b", m.group(1))} if m else set()


def file_status(text: str):
    for ln in text.split("\n")[:12]:
        if ln.startswith("**Status:**"):
            return ln[len("**Status:**"):].strip()
    return None


def findings(files: dict, index: str) -> list:
    """files: number -> (file name, file text); index: the README text. [(rule, key, message)]."""
    out, rows = [], {}
    for ln in index.split("\n"):
        m = ROW.match(ln)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3).strip())
    for num, (name, text) in sorted(files.items()):
        st = file_status(text)
        if num not in rows:
            out.append(("AI-MISSING", num, f"docs/adr/{name} has no row in docs/adr/README.md"))
            continue
        link, cell = rows[num]
        if link != name:
            out.append(("AI-MISSING", num, f"the index row for ADR-{num} links {link}, the file is {name}"))
        if st is None:
            continue    # check-package rule 10 fails an ADR with no Status line
        fs, rs = state_of(st), state_of(cell)
        if fs != rs:
            out.append(("AI-STATUS", num, f"ADR-{num}'s file says {fs or plain(st)[:40]!r}, its index row says "
                                          f"{rs or plain(cell)[:40]!r}: make the row say what the file says"))
        elif fs == "Superseded" and successors(st) != successors(cell):
            out.append(("AI-STATUS", num, f"ADR-{num} is superseded by {sorted(successors(st))} in its file and by "
                                          f"{sorted(successors(cell))} in the index"))
    for num, (link, _) in sorted(rows.items()):
        if num not in files:
            out.append(("AI-MISSING", num, f"the index row ADR-{num} links {link}, which is no ADR file"))
    return out


def self_test() -> int:
    idx = ("| [0001](0001-a.md) | A | **Superseded** by 0014 and 0017 | — |\n"
           "| [0002](0002-b.md) | B | Accepted | — |\n"
           "| [0003](0003-c.md) | C | **Proposed** — waiting on Chinmay | — |\n"
           "| [0004](0004-d.md) | D | Accepted in part — the rest waits | — |\n")
    base = {"0001": ("0001-a.md", "# A\n\n**Status:** Superseded by [ADR-0014](0014-x.md) and [ADR-0017](0017-y.md)\n"),
            "0002": ("0002-b.md", "# B\n\n**Status:** Accepted · amended by ADR-0009\n"),
            "0003": ("0003-c.md", "# C\n\n**Status:** Proposed · waiting\n"),
            "0004": ("0004-d.md", "# D\n\n**Status:** Accepted in part · 2 October\n")}

    def rules(files, index=idx):
        return sorted((r, k) for r, k, _ in findings(files, index))

    cases = [
        ("index and files agree", rules(base), []),
        ("the file accepted, the index still proposed (ADR-0065)",
         rules({**base, "0003": ("0003-c.md", "**Status:** Accepted · 1 October 2026 · Chinmay\n")}), [("AI-STATUS", "0003")]),
        ("accepted in part is not accepted",
         rules({**base, "0004": ("0004-d.md", "**Status:** Accepted · 2 October\n")}), [("AI-STATUS", "0004")]),
        ("a different successor",
         rules({**base, "0001": ("0001-a.md", "**Status:** Superseded by [ADR-0038](0038-z.md)\n")}), [("AI-STATUS", "0001")]),
        ("a file with no row", rules({**base, "0005": ("0005-e.md", "**Status:** Accepted\n")}), [("AI-MISSING", "0005")]),
        ("a row with no file", rules({k: v for k, v in base.items() if k != "0002"}), [("AI-MISSING", "0002")]),
    ]
    fails = [f"{name}: got {got}, expected {want}" for name, got, want in cases if got != want]
    for f in fails:
        print("  FAIL", f)
    print(f"check-adr-index self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if self_test():
        return 1
    guard = g.Guard("check-adr-index", RULES)
    files = {f.name[:4]: (f.name, f.read_text(encoding="utf-8")) for f in sorted(ADR_DIR.glob("0*.md"))}
    index = (ADR_DIR / "README.md").read_text(encoding="utf-8")
    for rule, key, message in findings(files, index):
        guard.add(rule, key, message)
    guard.note(f"{len(files)} ADR file(s) against the index in docs/adr/README.md")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
