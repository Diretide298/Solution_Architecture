#!/usr/bin/env python3
"""The landing and orientation pages carry no figure the package contradicts.

**3 November 2026** (r13 system review F-13; the lead, 3 November 2026: "All four, one release"; CHG-R14J-041). The
first pages a developer opens gave numbers that were wrong: OVERVIEW.md said "2453 screens cannot be reached" (2
cannot; tools/sync-counts.py had rewritten the generated "2 screens" with a bare "<n> screens" pattern), README.md
"364 definitions" and "10 app manifests", screens/README.md "364 screens across twelve platforms", frontend/README.md
"Ten apps, 364 screens", rtl-and-theming.md "the twelve platforms" (there are sixteen), and COVERAGE.md and
frontend-delivery.md tables frozen on 17 August. Hand-typed counts on a page nobody regenerates.

    LF-FIGURE        on a landing page, "<n> <noun>" (screens, platforms, operations, contracts, tables, flows,
                     journeys, ADRs, state models, events, apps, manifests, frontends, boards) where n, in digits or
                     a number word, is not the package's count of that noun (handoff/status.json)
    LF-COUNT-TABLE   on a landing page, a table with a count column (Screens, Operations, Tables, Flows, Total, W1-W3)
                     holding typed numbers: a count table is derived (OVERVIEW.md) or it is not on the page
    LF-OVERVIEW      OVERVIEW.md is not what tools/derive-overview.py renders from the package now (something edited
                     the generated page after it was written)

**History is allowed and says so.** A page whose first lines carry "**Historical" is a dated record and is not read;
neither is anything under a "## History" heading, nor a fenced code block. `--self-test` runs the rules on made-up
pages.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "LF-FIGURE": "a landing page states '<n> <noun>' for a count the package has otherwise (CHG-R14J-041, review F-13)",
    "LF-COUNT-TABLE": "a landing page carries a hand-typed count table (CHG-R14J-041, review F-13)",
    "LF-OVERVIEW": "OVERVIEW.md differs from what tools/derive-overview.py renders now (CHG-R14J-041, review F-13)",
}
# The pages a developer opens first: the package's landing pages and the folder and architecture pages F-13 named.
PAGES = ("README.md", "COVERAGE.md", "MANIFEST.md", "STRUCTURE.md", "screens/README.md", "frontend/README.md",
         "docs/architecture/README.md", "docs/architecture/frontend-delivery.md",
         "docs/architecture/rtl-and-theming.md")
WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
# noun -> the status.json counts any one of which it may state
NOUNS = {
    "operations": ("operations",), "contracts": ("contracts",), "tables": ("tables", "tablesWritten"),
    "screens": ("screens",), "platforms": ("platforms",), "state models": ("states",), "events": ("events",),
    "flows": ("flows", "flowsAll"), "journeys": ("flows",), "ADRs": ("adrs",), "apps": ("apps", "frontends"),
    "app manifests": ("frontends",), "manifests": ("frontends",), "frontends": ("frontends",), "boards": ("boards",),
}
NUM = r"(\d[\d,]*|" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")"
FIGURE = re.compile(r"(?<![\w.,/-])" + NUM + r" (" + "|".join(sorted(NOUNS, key=len, reverse=True)) + r")\b", re.I)
COUNT_COLUMNS = {"screens", "operations", "tables", "flows", "total", "w1", "w2", "w3"}


def readable(text: str) -> list:
    """[(line number, line)] a reader takes as current: not a historical page, not under '## History', not code."""
    lines = text.replace("\r\n", "\n").split("\n")
    if any("**Historical" in ln for ln in lines[:10]):
        return []
    out, fence = [], False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if re.match(r"^#{1,3} History\b", ln):
            break
        if not fence and not ln.startswith("    "):
            out.append((i, ln))
    return out


def number(tok: str) -> int:
    t = tok.lower()
    return WORDS[t] if t in WORDS else int(t.replace(",", ""))


def page_findings(name: str, text: str, counts: dict) -> list:
    out = []
    rows = readable(text)
    for i, ln in rows:
        for m in FIGURE.finditer(ln):
            noun = next(k for k in NOUNS if k.lower() == m.group(2).lower())
            allowed = {counts[k] for k in NOUNS[noun] if k in counts}
            if allowed and number(m.group(1)) not in allowed:
                out.append(("LF-FIGURE", f"{name}:{i}:{m.group(0)}",
                            f"{name}:{i} says '{m.group(0)}'; the package has {' or '.join(map(str, sorted(allowed)))}: "
                            "take the figure out, or make the page derived"))
    header = None
    for i, ln in rows:
        if not ln.startswith("|"):
            header = None
            continue
        cells = [c.strip().strip("*").strip().lower() for c in ln.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        for col, c in zip(header, cells):
            if col in COUNT_COLUMNS and re.fullmatch(r"\d[\d,]*", c):
                out.append(("LF-COUNT-TABLE", f"{name}:{i}", f"{name}:{i} is a row of a typed count table "
                            f"(column '{col}'): derive it into OVERVIEW.md or a manifest, or drop it"))
                break
    return out


def package_counts() -> dict:
    status = g.load_json(g.ROOT / "handoff" / "status.json", {}) or {}
    c = dict(status.get("counts") or {})
    if "flows" in c:
        c["flowsAll"] = c["flows"] + c.get("flowsDerived", 0)
    return c


def overview_rendered():
    spec = importlib.util.spec_from_file_location("derive_overview", str(g.ROOT / "tools" / "derive-overview.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.render()[0]


def self_test() -> int:
    c = {"screens": 2453, "platforms": 16, "frontends": 13, "apps": 6, "flows": 98, "flowsAll": 291, "operations": 2864}

    def rules(text):
        return sorted(r for r, _, _ in page_findings("p.md", text, c))

    cases = [
        ("a stale screen count", rules("**364 screens across twelve platforms.**\n"), ["LF-FIGURE", "LF-FIGURE"]),
        ("the package's own counts", rules("2453 screens across sixteen platforms; 13 frontends; 291 flows\n"), []),
        ("a number word", rules("Ten apps, one guest.\n"), ["LF-FIGURE"]),
        ("a historical page is not read", rules("# T\n\n> **Historical.** As of 17 August.\n\n364 screens\n"), []),
        ("under a History heading", rules("2453 screens\n\n## History (17 August)\n\n364 screens\n"), []),
        ("a code block", rules("```\n689 operations\n```\n"), []),
        ("a count table", rules("| App | Screens |\n|---|---|\n| guest-web | 29 |\n"), ["LF-COUNT-TABLE"]),
        ("a table with no count column", rules("| App | Owner |\n|---|---|\n| guest-web | 29 |\n"), []),
        ("part of a whole is not a count of the noun", rules("2451 of 2453 screens\n"), []),
    ]
    fails = [f"{name}: got {got}, expected {want}" for name, got, want in cases if got != want]
    for f in fails:
        print("  FAIL", f)
    print(f"check-landing-figures self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if self_test():
        return 1
    guard = g.Guard("check-landing-figures", RULES)
    counts = package_counts()
    if not counts:
        guard.note("no handoff/status.json counts: run tools/build-status.py; figures not compared")
    read = 0
    for name in PAGES:
        p = g.ROOT / name
        if not p.is_file():
            continue
        read += 1
        for rule, key, message in page_findings(name, p.read_text(encoding="utf-8", errors="replace"), counts):
            guard.add(rule, key, message)
    ov = g.ROOT / "OVERVIEW.md"
    if ov.is_file():
        try:
            want = overview_rendered()
        except Exception as exc:  # an input it reads is missing: say so, never pass silently
            guard.add("LF-OVERVIEW", "OVERVIEW.md", f"tools/derive-overview.py could not render ({exc}); run the refresh")
        else:
            if ov.read_text(encoding="utf-8").replace("\r\n", "\n") != want:
                guard.add("LF-OVERVIEW", "OVERVIEW.md", "OVERVIEW.md is not what tools/derive-overview.py renders from "
                          "the package now: something edited it after it was written (sync-counts did, to 3 November "
                          "2026); run tools/derive-overview.py and stop the other writer")
    guard.note(f"{read} landing page(s) read against handoff/status.json; OVERVIEW.md against its generator")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
