#!/usr/bin/env python3
"""Give a pandoc-generated docx the proposal's cover page.

**Pandoc's title block is a heading and a line of metadata.** Beside a client proposal that opens
on a full cover — 40pt navy title, teal subtitle, submitted-to and submitted-by blocks, a
confidentiality mark — it reads as a draft somebody forgot to finish.

**The cover is lifted from the proposal itself rather than recreated**, which is why the type sizes
and the exact navy `#1B2A4A` and teal `#0F6E56` match instead of approximately matching. Recreating
it would drift the moment somebody adjusted the proposal.

Usage:
    inject-cover.py <docx> --title "TICVAI PLATFORM" --subtitle "Architecture Note" \\
                    --strapline "Hierarchy, Data Segregation and Services" --date "24 August 2026"
"""
from __future__ import annotations

import argparse
import re
import shutil
import zipfile
from pathlib import Path

COVER = Path(__file__).resolve().parents[1] / "docs" / "cover.xml"


def swap(xml: str, old: str, new: str) -> str:
    """Replace the text of a run without touching its formatting."""
    return xml.replace(f">{old}<", f">{new}<")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--title", default="TICVAI PLATFORM")
    ap.add_argument("--subtitle", default="Architecture Note")
    ap.add_argument("--strapline", default="")
    ap.add_argument("--date", default="24 August 2026")
    ap.add_argument("--version", default="Design Package  —  Version 1.0")
    ap.add_argument("--cover", default=str(COVER))
    a = ap.parse_args()

    cover = Path(a.cover).read_text(encoding="utf-8")
    for old, new in (
        ("TICVAI PLATFORM", a.title),
        ("Architecture Note", a.subtitle),
        ("Hierarchy, Data Segregation and Services", a.strapline or a.subtitle),
        ("24 August 2026  —  ", f"{a.date}  —  "),
        ("Design Package  —  Version 1.0", a.version),
    ):
        cover = swap(cover, old, new)

    src = Path(a.docx)
    tmp = src.with_suffix(".tmp.docx")
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                doc = data.decode("utf-8")
                # **Drop pandoc's own title block.** It is a Title paragraph followed by the
                # metadata line, and leaving it means the reader meets the title twice — once
                # badly on the cover and once again on page two.
                # **Drop pandoc's own title block and its empty TOC heading.** The reader would
                # otherwise meet the title twice — once on the cover and once again on page two —
                # and `Table of Contents` renders as a bare label because pandoc's field is empty
                # and `prep.py` builds the contents statically instead.
                #
                # Matched on the paragraph's own style so the regex cannot run past the paragraph
                # it means: an earlier version used `.*?</w:p>` after the style tag and swallowed
                # whatever followed.
                #
                # **`\s*` before the slash is not cosmetic.** Pandoc writes
                # `<w:pStyle w:val="Title" />` with a space; the first version of this required
                # `"Title"/>` and silently matched nothing, which looked exactly like the cover
                # having failed to inject.
                for style in ("Title", "TOCHeading", "Subtitle", "Author", "Date"):
                    doc = re.sub(
                        r'<w:p\b[^>]*>(?:(?!</w:p>).)*?<w:pStyle w:val="'
                        + style + r'"\s*/>(?:(?!</w:p>).)*?</w:p>',
                        "", doc, flags=re.S)
                m = re.search(r"<w:body>", doc)
                doc = doc[:m.end()] + cover + doc[m.end():]
                data = doc.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, src)
    print(f"  cover injected -> {src.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
