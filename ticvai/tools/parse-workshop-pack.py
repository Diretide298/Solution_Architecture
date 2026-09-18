#!/usr/bin/env python3
"""Parse the workshop reference pack into one record per screen.

**Seventeen module documents, 1,058 pages, 59 boards, 590 screens.** They arrived as
`Workshop Docs.zip` on 3 September and they are the largest single addition the package has ever
been asked to absorb — larger than its entire current screen inventory.

Writes `sources/workshop/pack.json`. Nothing downstream should read the PDFs again.

## Why the table of contents and not the body

**A body scan counts 741 screens where there are 590.** Every document repeats screen titles as
cross-references — "as configured in 11.1.4" — and a title-matching pass cannot tell a reference
from a declaration. The table of contents lists each screen exactly once, which is what makes it
the canonical list rather than merely a convenient one.

## Three numbering conventions, sometimes two in one document

    Screen 7 - Access Control Graphical Map Designer     board 1 of Access Control
    Screen 2.7 - Multi-Park & Crossover Rules            board 2 of the same document
    11.1.7 - Person-Type, Product & Entitlement Rules    area.board.screen, most documents

**`Access Control` and `Product Lifecycle` use the first form for board 1 and the second from
board 2 on.** A parser that assumes one convention silently returns a board's worth of screens and
looks like it worked.

## The reconciliation is the point

Every board in this pack is ten screens, so 59 boards is 590 screens and the two numbers check each
other. **`--check` exits non-zero unless the parse reconciles**, because a partial parse of a
source document is worse than no parse: it is a number somebody will plan against.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pdfplumber
from rapidfuzz import fuzz

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
# **Reads `sources/workshop/`, and that is still where the workshop PDFs live.** A change on
# 18 September pointed this at `sources/packs/` on the assumption that `index-packs.py` had
# centralised every reference PDF there and removed the duplicates. That centralisation was
# reverted — it flattened folders whose *placement carries authority*, which `sources/README.md`
# ranks — so this points back at the folder that still holds the files.
#
# **The twenty PDFs here are byte-identical to twenty in `sources/packs/`** and that duplication is
# real and unresolved. It is recorded in `sources/packs-index.json` and
# `docs/active/source-integrity-18-september.md`. When the centralisation is redone properly this
# line moves with it, and not before.
SRC = ROOT / "sources" / "workshop"
OUT = SRC / "pack.json"

# 17 documents and 590 screens on 3 September; `Approval Workflows & Governance`
# (8 boards) and `Unified BI Reporting & AI Analytics` (10 boards) arrived on
# 9 September in the OneDrive export. `Latest Docs.zip` on 11 September added four more —
# Digital Asset Management (4 boards), Game & Ride (10), Rental Management (10) and
# Subscription Licensing & AI Self-Service (10) — counted from their headings before the parser
# was run, not from its output.
EXPECTED_SCREENS = 1110
EXPECTED_BOARDS = 111

DASH = r"[—–-]"

# `Screen 2.7 - x`, `Screen 7 - x`, or `11.1.7 - x`. The leading `Screen` is optional because the
# area-numbered form never carries it.
SCREEN_LINE = re.compile(r"^(?:Screen\s+)?(\d+(?:\.\d+){0,2})\s*" + DASH + r"\s*(.+)$")
BOARD_LINE = re.compile(r"^Board\s+(\d+)\s*(?:of\s+\d+\s*)?" + DASH + r"?\s*(.*)$")
# **Where a screen's specification stops, other than at the next screen.** The last screen of a
# board is followed by that board's summary table and the next board's objective, and neither
# belongs to it: without this, screen 10 of every board acquired a directory of its own nine
# siblings as its fields, and the eight boards of `Approval Workflows` each did it once.
BOARD_BOUNDARY = re.compile(
    r"^Board\s+\d+\s*(?:" + DASH + r"|:)?\s*(?:Screen Summary|Acceptance Criteria|Core Flow)\b",
    re.I)

AREA_LINE = re.compile(r"^Area\s+(\d+)\s*" + DASH + r"\s*(.+)$")

# Section headings inside a screen's own specification. The pack is consistent about these, which
# is what makes a field-level extract possible at all.
# **Headings that end a section.** `Display`, `Support` and `Each configuration displays` are
# deliberately *not* here: they are sub-labels the pack puts immediately under a real heading —
# "KPI Cards" then "Display:" then the bullets — so treating one as a boundary truncated every
# list to nothing and made a working extract look like a bullet-parsing failure.
SECTIONS = ("Purpose", "KPI Cards", "Configuration Directory", "Transaction Types",
            "Fields", "Actions", "Rules", "Validation", "Filters", "Tabs",
            "Operational Activity", "Governance", "AI Assistance",
            # The `sources/packs/` family's own vocabulary. **`Key requirements` is the one worth
            # having**: it carries matrix ids — `Key requirements: 12.1.8–12.1.15` — so a screen
            # parsed from these packs can be traced to the contracted baseline directly, which no
            # workshop pack offers.
            "Scope of Work", "Key requirements", "Board Objective")

# The pack bullets with a private-use Wingdings glyph, not a bullet character.
BULLET = "•●▪*-–— "


def page_texts(pdf: Path) -> list[str]:
    with pdfplumber.open(pdf) as doc:
        return [(p.extract_text() or "") for p in doc.pages]


def toc_block(pages: list[str]) -> tuple[str, int]:
    """The table of contents, ending where the first screen specification begins.

    **`Privacy, Consent & Preference Management` is why this is not a single `find`.** Cutting at
    the first `Purpose` works for sixteen documents and truncates that one to two screens, because
    the word appears inside its contents list. Cutting at the first page that *starts* a screen
    specification works for all seventeen.
    """
    start = next((i for i, t in enumerate(pages) if "Table of Contents" in t), 0)
    end = len(pages)
    for i in range(start + 1, len(pages)):
        body = pages[i]
        # A specification page carries a screen heading and then a section heading under it.
        if SCREEN_LINE.match(body.strip().split("\n")[0].strip() if body.strip() else ""):
            continue
        # The workshop family puts the heading on its own line; the `sources/packs/` family writes
        # `Purpose:` inline. **Only the first form was recognised**, so for the second the contents
        # block never closed, ran to the last page, and every screen parsed from its own index
        # entry with no body behind it.
        if "Table of Contents" in body:
            continue
        if any(f"\n{s}\n" in body for s in ("Purpose", "KPI Cards")):
            end = i
            break
        if re.search(r"^(Purpose|Scope of Work):\s+\S", body, re.M):
            end = i
            break
    return "\n".join(pages[start:end]), end


def parse_toc(block: str) -> tuple[list[dict], list[str], list[str]]:
    """Screens in declaration order, plus the boards and areas the document claims."""
    screens, boards, areas, seen = [], [], [], set()
    board = None
    for raw in block.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if m := AREA_LINE.match(line):
            if m.group(1) not in areas:
                areas.append(m.group(1))
            continue
        if m := BOARD_LINE.match(line):
            board = m.group(1)
            if board not in boards:
                boards.append(board)
            continue
        if m := SCREEN_LINE.match(line):
            number, title = m.group(1), m.group(2).strip()
            # **The 11 September documents print their page numbers in the contents.**
            # `Digital Asset Management` uses dot leaders — `Command Center ........ 3` — and
            # matched 4 of its 40 screens to a body; `Rental` and `Subscription` set the number
            # after a space, so all 200 of theirs found a body and would have been named
            # `Rental Product Command Center 6` on every board and in every screen file. None of
            # the 770 earlier titles ends in a number, which is what makes the second cut safe.
            title = re.sub(r"\s*\.{2,}.*$", "", title)
            title = re.sub(r"\s+\d{1,3}$", "", title).strip()
            # **A title repeated in the contents is a page-break artefact, not a screen.** The
            # number is unreliable for de-duplication because the three conventions collide:
            # `Screen 7` in board 1 and `7` from `11.1.7` are different screens.
            if title in seen or len(title) < 4:
                continue
            seen.add(title)
            screens.append({"number": number, "title": title, "board": board})

    # **The board comes from the screen number, not from the header above it.** Every contents
    # list repeats "Board N —" in summary lines — `Board 2 — Final Screen Register`,
    # `Board 1 — Commercial Pricing FoundationWhat prices exist?` — so header tracking put two
    # boards' screens under one label twice and left Access Control's first ten with no board at
    # all, because that document opens `ACCESS CONTROL — BOARD 1` in capitals.
    #
    # The numbering already carries it: `11.1.7` is area 11 board 1, `2.7` is board 2, and a bare
    # `7` only ever occurs in a document's first board.
    assign_boards(screens)
    boards = sorted({s_["board"] for s_ in screens}, key=int)
    return screens, boards, areas


def assign_boards(screens: list[dict]) -> None:
    """The board comes from the screen number, whichever list the screens came from."""
    bare = 0
    seq = 0
    for s_ in screens:
        parts = s_["number"].split(".")
        if len(parts) == 3:
            s_["board"] = parts[1]
        elif len(parts) == 2:
            s_["board"] = parts[0]
        else:
            # **A bare number restarts at 1 for every board**, which is how Promotions numbers all
            # ten of its. The restart is the board boundary; nothing else in that document marks
            # one that a contents list does not also repeat three times in prose.
            n = int(parts[0])
            if n <= bare:
                seq += 1
            bare = n
            s_["board"] = str(seq + 1)


# **`Screen` spelled out, for the documents whose contents list boards only.** The bare-number
# form `1 — Title` is fine to match inside a contents block, where every line is a screen entry;
# matched against a whole document it also takes `0–10% → Automatic / Supervisor`,
# `201 — Approval Request Created` and `1–30 Days`. The keyword is what separates a heading
# from a table row, and both board-listing documents carry it on every real screen.
SCREEN_HEADING = re.compile(r"^Screen\s+(\d+(?:\.\d+){0,2})\s*" + DASH + r"\s*(.+)$")


def body_screens(pages: list[str]) -> list[dict]:
    """Screens read from the body, for a document whose contents lists boards and not screens.

    **Two of the nineteen documents index themselves by board.** `Approval Workflows & Governance`
    and `Unified BI Reporting & AI Analytics` list `Board 3 — Screen Summary` in their contents and
    never name a screen there, so `parse_toc` returns nothing and the document parses to zero —
    which is what it did, silently, until the reconciliation refused.

    The docstring's warning about body scans stands and is why this is not the default: a body
    scan that matches titles over-counts, because every document cross-references its own screens.
    It does not apply to a scan for *headings*, which each screen has exactly one of. The board is
    still taken from the numbering rather than from the `Board N` line above, because both
    documents repeat that line in prose between the screens it is supposed to introduce —
    `Board 4: Schedule → Subscribe → Distribute` sits four lines above screen 4.1.
    """
    out, seen = [], set()
    for i, text in enumerate(pages):
        for line in text.split(chr(10)):
            m = SCREEN_HEADING.match(line.strip())
            if not m or len(m.group(2).strip()) < 4:
                continue
            title = m.group(2).strip()
            if title in seen:
                continue
            seen.add(title)
            out.append({"number": m.group(1), "title": title, "board": None})
    return out


def body_headings(pages: list[str], start: int = 0) -> list[dict]:
    """Every screen heading in the body, with where it starts.

    **Matched by heading rather than by searching for the title anywhere on a page.** The first
    cut looked for the title as a substring and missed 65 of 590, because `pdfplumber` breaks a
    long heading across two lines and the substring is then never present. A heading is a line
    that begins a screen, and finding those first turns the problem into matching two lists.
    """
    out = []
    for i, text in enumerate(pages):
        # **The contents entries match this pattern too**, and they come first — so without this
        # every record cited page 2 and carried an empty specification, which looked like a
        # bullet-parsing failure and was not.
        if i < start:
            continue
        pos = 0
        for line in text.split("\n"):
            m = SCREEN_LINE.match(line.strip())
            if m and len(m.group(2).strip()) > 3:
                out.append({"page": i + 1, "index": i, "offset": pos,
                            "number": m.group(1), "title": m.group(2).strip()})
            pos += len(line) + 1
    return out


def spec_for(screen: dict, pages: list[str], headings: list[dict]) -> dict:
    """The body text under the heading that best matches this screen.

    **Fuzzy, because the heading and the contents entry are not always the same string** — a
    trailing degree sign, an ampersand that extracted as `and`, a line break in the middle of a
    noun phrase. The number is used to break ties where the document carries one.
    """
    best, score = None, 0
    for h in headings:
        r = fuzz.ratio(h["title"].lower(), screen["title"].lower())
        if h["number"] == screen["number"]:
            r += 15
        if r > score:
            best, score = h, r
    if not best or score < 70:
        return {"page": None, "body": "", "match": score}

    nxt = next((h for h in headings if (h["index"], h["offset"]) > (best["index"], best["offset"])),
               None)
    # **Cut at the next heading even when it is on the same page.** Two screens share a page
    # wherever one is short, and taking the first page whole ran each of those specifications
    # into the one below it: `Approval Request Detail` carried `Screen 5 - AI Decision Support`
    # and its prose as its own fields, which is a screen's directory attributed to its neighbour.
    first = pages[best["index"]]
    if nxt and nxt["index"] == best["index"]:
        first = first[:nxt["offset"]]
    text = first[best["offset"]:]
    # Continue into following pages until the next screen heading.
    last = nxt["index"] if nxt else min(best["index"] + 5, len(pages) - 1)
    for j in range(best["index"] + 1, last + 1):
        chunk = pages[j]
        if nxt and j == nxt["index"]:
            chunk = chunk[:nxt["offset"]]
        text += "\n" + chunk
    return {"page": best["page"], "body": cut_at_board(text)[:9000], "match": score}


def cut_at_board(text: str) -> str:
    """Everything up to the board's own summary, which belongs to the board and not the screen."""
    lines = text.split(chr(10))
    for i, line in enumerate(lines):
        if BOARD_BOUNDARY.match(line.strip()):
            return chr(10).join(lines[:i])
    return text


def sections(body: str, doc_title: str) -> dict:
    """Split a screen specification into its labelled blocks.

    **The pack has one universal shape and seventeen local vocabularies.** `Purpose` appears on all
    590 screens and `Acceptance Condition` on 476, but the lists in between sit under verb labels
    that differ per document — `Display:`, `Configure:`, `Support:`, `Show:`, `Capture:`,
    `Allow:`, `Analyze:`. An extractor built around one document's nouns — `KPI Cards`, `Fields`,
    `Actions` — found them on 29 screens of 590 and looked broken when it was merely provincial.

    So the blocks are keyed by whatever label introduces them, and **`terms` is the union**: every
    bullet on the screen, whatever it was called. That union is the vocabulary signature the
    redundancy pass compares, and for that purpose the label matters far less than the nouns.
    """
    label = re.compile(r"^([A-Z][A-Za-z0-9 ,&/'-]{2,40}):?$")
    # **A second pack family writes the label and its content on one line.** The seventeen workshop
    # documents put `Purpose` alone on a line and the prose beneath it; `ACCREDITATION.pdf` and the
    # other packs in `sources/packs/` write `Purpose: Executive and operational landing screen.`
    # Matched only by the label-alone form, every one of those lines fell through to the
    # continuation branch with no `current` label open, and was dropped — which is why the first
    # parse of that pack produced 131 screens and 131 empty bodies.
    inline = re.compile(r"^([A-Z][A-Za-z0-9 ,&/'-]{2,40}):\s+(\S.*)$")
    blocks: dict[str, list[str]] = {}
    current = None
    for raw in body.split(chr(10)):
        line = raw.strip()
        if not line:
            continue
        # **The running header and footer are on every page of every document.** Left in, the
        # module name became the most common "field" in the pack.
        # `N | Pa g e` is the second footer form, and pdfplumber's letter spacing is why it is
        # written that way here rather than as `Page`.
        if (line.startswith("TICVAI") or line == doc_title
                or re.match(r"^TICVAI\s*[.]\s*\d+$", line)
                or re.match(r"^\d+\s*\|\s*Pa\s*g\s*e$", line)
                # The `sources/packs/` family's footer: `Accreditation Functional Design • 3`.
                # Not caught by the `TICVAI` forms above, so it entered `terms` as a field name.
                or re.match(r"^.{4,60}\s[•·]\s*\d+$", line)):
            continue
        if line[0] in BULLET:
            t = line.lstrip(BULLET).strip()
            if t and current and len(t) < 160:
                blocks.setdefault(current, []).append(t)
            continue
        m = label.match(line)
        if m and len(line.split()) <= 5:
            current = m.group(1).strip()
            blocks.setdefault(current, [])
            continue
        m = inline.match(line)
        # **Only a known section name may introduce content inline.** Accepting any short
        # `Word: value` line looked right and was not: across the seventeen workshop packs it
        # invented 925 labels out of table cells and example rows — `Status: Active`,
        # `Venue: Dubai`, `Remaining: 12` — while dissolving 275 real ones. Total content was
        # unchanged, so nothing failed; the vocabulary just quietly became noise.
        #
        # Restricted to `SECTIONS`, the rule does what it was added for — `Purpose:`,
        # `Scope of Work:` and `Key requirements:` in the `sources/packs/` family — and leaves the
        # workshop packs byte-identical.
        if m and m.group(1).strip() in SECTIONS:
            current = m.group(1).strip()
            blocks.setdefault(current, []).append(m.group(2).strip())
            continue
        # An unbulleted continuation line under a label is still content.
        if current and len(line) < 160:
            blocks.setdefault(current, []).append(line)
    return blocks


def prose(blocks: dict, *names: str) -> str:
    for n in names:
        if blocks.get(n):
            return " ".join(blocks[n])[:600]
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero unless the parse reconciles to 59 boards and 590 screens")
    ap.add_argument("--apply", action="store_true", help="write sources/workshop/pack.json")
    # **A pack becomes screens only if it sits in `sources/workshop/`, and 24 packs never did.**
    # 1,955 pages in `sources/packs/` have never been through this parser — not because anyone
    # declined them, but because nothing ever put them where it looks. Copying them in is how the
    # duplication started, so this reads them where they are instead.
    ap.add_argument("--from", dest="src", metavar="DIR",
                    help="parse from this directory instead of sources/workshop")
    ap.add_argument("--only", metavar="SUBSTRING",
                    help="parse just the files whose name contains this — one pack at a time, "
                         "because a pack that does not follow the ten-per-board convention should "
                         "be read before 24 of them are trusted at once")
    a = ap.parse_args()

    src = (ROOT / a.src) if a.src else SRC
    if not src.exists():
        print(f"no {src} — extract Workshop Docs.zip there first")
        return 1

    pdfs = sorted(src.glob("*.pdf"))
    if a.only:
        pdfs = [p for p in pdfs if a.only.lower() in p.name.lower()]
        if not pdfs:
            print("no pdf under %s matching %r" % (src, a.only))
            return 1

    records, per_doc, indexed_by_board = [], [], []
    for pdf in pdfs:
        pages = page_texts(pdf)
        toc, body_starts_at = toc_block(pages)
        screens, boards, areas = parse_toc(toc)
        # **A contents list that indexes boards names no screens**, and the document then parses
        # to zero without failing. Falling back on the body is safe here and only here: the
        # contents block has already been shown not to be a screen list.
        if len(screens) < 5:
            screens = body_screens(pages)
            assign_boards(screens)
            boards = sorted({s_["board"] for s_ in screens}, key=int)
            indexed_by_board.append(pdf.name)
        # **The area number is scanned over the whole document, not the contents block.** Four
        # documents state their area only in a body heading, and four area numbers are claimed by
        # two documents each — 10, 11, 12 and 13. Screen ids cannot be assigned until the client
        # settles that, so under-reporting it here would hide the conflict rather than surface it.
        if not areas:
            found = set()
            for text in pages:
                for line in text.split(chr(10)):
                    if m := AREA_LINE.match(line.strip()):
                        found.add(m.group(1))
            areas = sorted(found, key=int)
        module = re.sub(r"[_ ]*Reference$", "", pdf.stem.replace("_", " ")).strip()
        # The running page header, which is the document's own title.
        doc_title = pages[0].split(chr(10))[0].strip() if pages else module
        headings = body_headings(pages, body_starts_at)
        for s in screens:
            spec = spec_for(s, pages, headings)
            blocks = sections(spec["body"], doc_title)
            records.append({
                "module": module,
                "source": pdf.name,
                "page": spec["page"],
                "area": areas[0] if areas else None,
                "board": s["board"],
                "number": s["number"],
                "title": s["title"],
                "purpose": prose(blocks, "Purpose"),
                "acceptance": prose(blocks, "Acceptance Condition", "Acceptance Criteria"),
                "aiCapability": prose(blocks, "AI Capability"),
                "sections": {k: v for k, v in blocks.items() if v},
                "terms": sorted({t for k, v in blocks.items()
                                 for t in v if k not in ("Purpose", "Example", "Examples",
                                                         "Acceptance Condition")}),
            })
        per_doc.append((pdf.name, areas, len(boards), len(screens)))

    print(f"{'document':46} {'area':>7} {'boards':>7} {'screens':>8}")
    for name, areas, nb, ns in per_doc:
        print(f"{name[:44]:46} {','.join(areas) or '-':>7} {nb:>7} {ns:>8}")
    boards_total = sum(b for _, _, b, _ in per_doc)
    print(f"\n{'TOTAL':46} {'':7} {boards_total:>7} {len(records):>8}")

    if indexed_by_board:
        print(f"{chr(10)}  read from the body, contents indexes boards not screens: "
              f"{', '.join(indexed_by_board)}")

    # **Every board in this pack is ten screens.** A global total can reconcile while one document
    # is short and another long, and only the per-document check catches that.
    ragged = [(n, nb, ns) for n, _, nb, ns in per_doc if ns != nb * 10]
    for name, nb, ns in ragged:
        print(f"{chr(10)}  {name} parsed {ns} screens across {nb} boards - not ten per board")

    unspecified = [r for r in records if not r["page"]]
    if unspecified:
        print(f"\n  {len(unspecified)} screen(s) with no specification body found — "
              f"first: {unspecified[0]['title']}")

    ok = (len(records) == EXPECTED_SCREENS and boards_total == EXPECTED_BOARDS
          and not ragged)
    if not ok:
        print(f"\n  DOES NOT RECONCILE — expected {EXPECTED_BOARDS} boards and "
              f"{EXPECTED_SCREENS} screens. **A partial parse of a source document is a number "
              f"somebody will plan against.**")

    if a.apply:
        # **A partial run must merge, or `--only` silently deletes every other pack.** This writes
        # the whole file, so parsing one document and applying it would replace 1,110 screens with
        # that document's 80 — and the result would look like a successful run. When the parse was
        # scoped, the records for the sources it did *not* read are carried over unchanged and only
        # the ones it did are replaced.
        out = records
        if (a.only or a.src) and OUT.exists():
            existing = json.loads(OUT.read_text(encoding="utf-8"))
            touched = {r.get("source") for r in records}
            kept = [r for r in existing if r.get("source") not in touched]
            out = kept + records
            print("  merged: %d screens kept from %d other source(s), %d replaced or added"
                  % (len(kept), len({r.get('source') for r in kept}), len(records)))
        OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  -> {OUT.relative_to(ROOT)}  ({len(out)} screens)")
    elif not a.check:
        print("  nothing written — pass --apply")

    return 0 if ok or not a.check else 1


if __name__ == "__main__":
    sys.exit(main())
