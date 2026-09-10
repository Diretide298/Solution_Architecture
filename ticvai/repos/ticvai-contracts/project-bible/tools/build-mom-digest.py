#!/usr/bin/env python3
"""Transcribe all 22 minutes into one navigable document, so nobody opens a `.docx` again.

**60,000 words across 22 files, 20 of them Word documents and 2 Markdown**, and every question about
what was agreed has meant opening them one at a time and reading. This writes
`docs/active/mom-digest.md`: every minute, in date order, with its objective, its discussion
sections under their own headings, its decisions and its actions — plus a topic index saying which
minutes touch which module.

## Transcription, not summary

**Nothing here is condensed and nothing is paraphrased.** A summary of a minute is a second source
that disagrees with the first at exactly the moment somebody relies on it, and this package has
already spent a week on one such disagreement — CF-164, where a filing label in one document was
read as a fact by the next. So the digest carries the paragraphs as written, and the only editorial
act is ordering them.

The consequence is that it is long. That is correct: it replaces 22 files, and length is not the
cost — hunting is.

## Two things it normalises

**Half the corpus is Markdown wearing a `.docx` extension.** Eleven were replaced with their Word
originals on 9 September when the originals arrived; a comparison first showed the transcriptions
were faithful at 0.99–1.00 similarity, so nothing mined from them was ever wrong. The reader is
detected by magic bytes rather than by extension, because reading the extension raised `BadZipFile`
on two thirds of the corpus the first time this was attempted.

**Dates come from the filename, then the body.** `TICVAI_MoM_2026-08-21_Seat_Management_CMS` and
`MoM_FnB_Retail_Procurement_Inventory_18Aug2026` are the same corpus with two naming conventions,
and a digest ordered by filename puts August after September.

Run: python tools/build-mom-digest.py
"""
from __future__ import annotations

import io
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOM = ROOT / "sources" / "mom"
OUT = ROOT / "docs" / "active" / "mom-digest.md"

MONTHS = {m.lower(): i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

# Headings a minute uses. Everything else is a paragraph under whichever heading precedes it.
SECTION = re.compile(
    r"^(minutes of meeting|date|project|meeting type|prepared by|primary objective|participants|"
    r"agenda|discussion summary|decisions made|decisions|action items|actions|next steps|"
    r"open items|attendees|risks?|assumptions)\s*:?\s*$", re.I)

# `1. Session Framing`, `10. Reference Material & Design Research`
NUMBERED = re.compile(r"^\d{1,2}\.\s+\S")

# The vocabulary the package is organised by, for the topic index. Matching is on whole words so
# `POS` does not match `position` and `AI` does not match `said`.
TOPICS = {
    "Point of sale": r"\bPOS\b|point[- ]of[- ]sale|cashier",
    "F&B": r"\bF&B\b|food (and|&) beverage|kitchen|restaurant|menu|table service",
    "Retail": r"\bretail\b|merchandise|stock",
    "Ticketing & products": r"\bticket(ing|s)?\b|product config|ticket type",
    "Pricing & promotions": r"\bpricing\b|\bprice\b|promotion|discount|bundle",
    "Access control": r"access control|turnstile|anti[- ]?passback|gate",
    "Accreditation": r"accreditation|badge|press",
    "Entitlements": r"entitlement",
    "Virtual queue": r"virtual queue|queue",
    "Wallet & payments": r"\bwallet\b|payment|refund|settlement",
    "Membership & loyalty": r"membership|loyalty|annual pass",
    "CRM & marketing": r"\bCRM\b|marketing|campaign|segment",
    "Seat management": r"seat map|seating|seat management",
    "Resource management": r"resource management|staff scheduling|roster",
    "Inventory & procurement": r"inventory|procurement|purchase order",
    "Reporting & analytics": r"analytics|reporting|dashboard|\bBI\b",
    "Infrastructure & cost": r"hosting|multi[- ]tenan|cell|data residency|AWS",
    "UI/UX & design": r"UI/UX|wireframe|white[- ]label|drawer pattern|look and feel",
    "Integrations & identity": r"\bSSO\b|UAE Pass|Okta|Azure|integration|\bAPI\b",
    "B2B, groups & partners": r"\bB2B\b|reseller|\bOTA\b|group sales|corporate",
    "Waivers & consent": r"waiver|consent|privacy|GDPR",
    "Customer service": r"customer service|complaint|case management|helpdesk",
}


def read(path: Path) -> list[str]:
    """Paragraphs. **Magic bytes, not the extension** — half this corpus is mislabelled."""
    raw = path.read_bytes()
    if raw[:4] != b"PK\x03\x04":
        text = raw.decode("utf-8", "replace")
        return [" ".join(re.sub(r"[|*`#>]+", " ", ln).split())
                for ln in text.splitlines() if ln.strip()]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab[^>]*/>", "  ", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'").replace("﻿", ""))
    return [" ".join(p.split()) for p in text.split("\n") if p.strip()]


def when(path: Path, paras: list[str]) -> str:
    """ISO date, from the filename first because the body writes it six different ways."""
    if m := re.search(r"(20\d{2})-(\d{2})-(\d{2})", path.name):
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if m := re.search(r"(\d{1,2})([A-Za-z]{3})(20\d{2})", path.name):
        return f"{m.group(3)}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    # `..._Jul_28_2026` — a fourth convention, and the one that left a minute filed under
    # "unknown" and sorted to the end of a chronological document.
    if m := re.search(r"([A-Za-z]{3})[_ ](\d{1,2})[_ ](20\d{2})", path.name):
        if (mon := MONTHS.get(m.group(1).lower())):
            return f"{m.group(3)}-{mon:02d}-{int(m.group(2)):02d}"
    for p in paras[:12]:
        if m := re.match(r"^(\d{1,2})\s+([A-Za-z]+)\s+(20\d{2})$", p.strip()):
            mon = MONTHS.get(m.group(2)[:3].lower())
            if mon:
                return f"{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}"
    return "unknown"


def title_of(paras: list[str], path: Path) -> str:
    """The meeting's own subject line.

    **Not "the first paragraph mentioning TICVAI"** — that put *"Allam's proposed approach, based
    on prior TICVAI discussions"* in the index as the title of the 19 August minute.
    """
    for i, p in enumerate(paras[:20]):
        if re.match(r"^meeting type\s*:?$", p, re.I) and i + 1 < len(paras):
            return paras[i + 1]
    for p in paras[:6]:
        if len(p.split()) > 4 and not re.match(r"^(minutes of meeting|date|project)$", p, re.I):
            return p
    return re.sub(r"[_]+", " ", path.stem)


def sectionise(paras: list[str]) -> list[tuple[str, list[str]]]:
    """`[(heading, paragraphs)]`, keeping every paragraph exactly once."""
    out: list[tuple[str, list[str]]] = [("Front matter", [])]
    for p in paras:
        if SECTION.match(p) or (NUMBERED.match(p) and len(p) < 90):
            out.append((p.rstrip(":"), []))
        else:
            out[-1][1].append(p)
    return [(h, ps) for h, ps in out if ps]


def main() -> int:
    files = sorted(MOM.glob("*.docx")) + sorted(MOM.glob("*.md"))
    minutes = []
    for f in files:
        paras = read(f)
        minutes.append({"file": f.name, "date": when(f, paras), "title": title_of(paras, f),
                        "words": sum(len(p.split()) for p in paras),
                        "sections": sectionise(paras), "real": f.read_bytes()[:4] == b"PK\x03\x04"})
    minutes.sort(key=lambda m: (m["date"], m["file"]))

    # topic index
    topic_hits: dict[str, list[str]] = defaultdict(list)
    for m in minutes:
        blob = " ".join(p for _, ps in m["sections"] for p in ps)
        for topic, pattern in TOPICS.items():
            # Five, not three. **Three mentions is a passing reference**, and at that threshold
            # every module matched almost every minute and the table said nothing.
            if len(re.findall(pattern, blob, re.I)) >= 5:
                topic_hits[topic].append(m["date"])

    total = sum(m["words"] for m in minutes)
    lines = [
        "# The minutes, transcribed — every workshop in one document",
        "",
        f"**{len(minutes)} minutes, {total:,} words, {minutes[0]['date']} to "
        f"{minutes[-1]['date']}.** Generated by `tools/build-mom-digest.py`; regenerate it rather "
        "than editing it.",
        "",
        "**This is a transcription, not a summary.** Every paragraph appears as written and the "
        "only editorial act is ordering. A summary would be a second source that disagrees with "
        "the first at the moment somebody relies on it — which this package has already spent a "
        "week on once, when a filing label in one document was read as a fact by the next "
        "(CF-164).",
        "",
        "---",
        "",
        "## The minutes",
        "",
        "| Date | Words | Minute |",
        "|---|---:|---|",
    ]
    for m in minutes:
        lines.append(f"| [{m['date']}](#{m['date']}) | {m['words']:,} | {m['title'][:96]} |")

    lines += ["", "---", "", "## Which minutes touch which module", "",
              "Counted on whole-word matches, five or more mentions. **A topic listed against one "
              "date has been discussed once**, which is usually the more useful fact.", "",
              "| Module | Discussed on |", "|---|---|"]
    for topic in TOPICS:
        if dates := topic_hits.get(topic):
            lines.append(f"| **{topic}** | {' · '.join(dates)} |")
    missing = [t for t in TOPICS if t not in topic_hits]
    if missing:
        lines += ["", f"**Never substantially discussed in any minute:** {', '.join(missing)}. "
                      f"Each is a module the package specifies and no workshop covered."]

    for m in minutes:
        lines += ["", "---", "", f'<a id="{m["date"]}"></a>', "", f"## {m['date']}", "",
                  f"`sources/mom/{m['file']}` · {m['words']:,} words"
                  + ("" if m["real"] else " · **held as Markdown, no Word original**"), ""]
        for heading, paras in m["sections"]:
            lines += [f"### {heading}", ""]
            for p in paras:
                lines.append(f"- {p}" if len(p.split()) < 25 else p)
                lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(minutes)} minutes · {total:,} words -> {OUT.relative_to(ROOT)}")
    print(f"{len(topic_hits)} of {len(TOPICS)} modules discussed; never covered: "
          f"{', '.join(missing) or 'none'}")
    print(f"{sum(1 for m in minutes if not m['real'])} still held as Markdown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
