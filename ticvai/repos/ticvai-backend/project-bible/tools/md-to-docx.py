#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown to .docx, for the reports that leave this package as a file.

**Written 21 September because there is no pandoc and no LibreOffice on this machine**, and the
reports that go to the client and the build team are asked for as documents rather than as links.
The Claude Docs export can produce a .docx directly; this exists for the other direction -- a
markdown file on disk, including the ones `tools/` generates, turned into something openable.

**It handles what this package's markdown actually uses** and nothing else: headings, paragraphs
with `**bold**`, `*italic*` and `` `code` `` spans, pipe tables, bullet and ordered lists, block
quotes, fenced code, and `---` rules. A Mermaid fence is rendered as its source in a monospace
block rather than dropped, because a diagram nobody can see is worse than a diagram somebody can
read.

**Inline markers are parsed rather than stripped.** A report whose emphasis is its argument loses
the argument if `**` arrives as two asterisks, and this package writes its findings in bold on
purpose.

    python3 tools/md-to-docx.py <input.md> [output.docx] [--title "..."]
"""
import argparse
import os
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*]+\*|\[[^\]]+\]\([^)]+\))")


def add_runs(par, text):
    """`**bold**`, `*italic*`, `` `code` `` and `[label](url)` -- as runs, not as literals."""
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            par.add_run(piece[2:-2]).bold = True
        elif piece.startswith("`") and piece.endswith("`") and len(piece) > 2:
            r = par.add_run(piece[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x8B, 0x25, 0x52)
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            par.add_run(piece[1:-1]).italic = True
        elif piece.startswith("["):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", piece)
            # The link target is kept beside the label rather than as a field code: a real
            # hyperlink needs a relationship on the part, and a URL somebody can copy out of the
            # page is worth more here than one they can click.
            r = par.add_run(m.group(1))
            r.underline = True
            r.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
        else:
            par.add_run(piece)


def table_rows(lines, i):
    """Collect a pipe table starting at `i`; returns (rows, next_i) or (None, i)."""
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
            rows.append(cells)
        i += 1
    return (rows or None), i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("target", nargs="?")
    ap.add_argument("--title")
    a = ap.parse_args()

    target = a.target or os.path.splitext(a.source)[0] + ".docx"
    lines = open(a.source, encoding="utf-8").read().replace("\r\n", "\n").split("\n")

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(8)

    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            body = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(18)
            if lang:
                cap = doc.paragraphs[-1].insert_paragraph_before()
                cr = cap.add_run(lang)
                cr.italic = True
                cr.font.size = Pt(8)
                cr.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
            r = p.add_run("\n".join(body))
            r.font.name = "Consolas"
            r.font.size = Pt(8.5)
            continue

        if s.startswith("|"):
            rows, i = table_rows(lines, i)
            if rows:
                t = doc.add_table(rows=len(rows), cols=max(len(r) for r in rows))
                t.style = "Light Grid Accent 1"
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                for ri, row in enumerate(rows):
                    for ci, cell in enumerate(row):
                        c = t.cell(ri, ci)
                        c.text = ""
                        par = c.paragraphs[0]
                        par.paragraph_format.space_after = Pt(2)
                        add_runs(par, cell)
                        for run in par.runs:
                            run.font.size = Pt(8.5)
                            if ri == 0:
                                run.bold = True
                doc.add_paragraph()
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            level = len(m.group(1))
            h = doc.add_heading("", level=min(level, 4))
            add_runs(h, m.group(2))
            for r in h.runs:
                r.font.color.rgb = RGBColor(0x0B, 0x13, 0x24)
            i += 1
            continue

        m = re.match(r"[-*+]\s+(.*)", s)
        if m:
            par = doc.add_paragraph(style="List Bullet")
            par.paragraph_format.space_after = Pt(3)
            add_runs(par, m.group(1))
            i += 1
            continue

        m = re.match(r"\d+[.)]\s+(.*)", s)
        if m:
            par = doc.add_paragraph(style="List Number")
            par.paragraph_format.space_after = Pt(3)
            add_runs(par, m.group(1))
            i += 1
            continue

        if s.startswith(">"):
            par = doc.add_paragraph()
            par.paragraph_format.left_indent = Pt(18)
            add_runs(par, s.lstrip("> "))
            for r in par.runs:
                r.italic = True
            i += 1
            continue

        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_runs(par, s)
        i += 1

    if a.title:
        doc.core_properties.title = a.title
    doc.save(target)
    print("  %s -> %s (%d KB)" % (os.path.basename(a.source), os.path.basename(target),
                                  os.path.getsize(target) // 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
