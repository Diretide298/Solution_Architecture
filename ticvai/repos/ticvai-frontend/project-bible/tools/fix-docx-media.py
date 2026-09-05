#!/usr/bin/env python3
"""Restore image content types that pandoc drops from a .docx.

**Word refuses to open a document whose `[Content_Types].xml` does not declare an extension it
contains.** Pandoc writes `word/media/rId22.png` and then declares only `xml` and `rels` — even
when the reference document declares `png`, `jpeg`, `svg` and five more correctly.

**The result opens nowhere and reports "unreadable content"**, which is the least diagnostic error
message Word produces. Both deployment documents shipped that way on 31 August; the zip was intact,
`document.xml` parsed, every relationship resolved, and the file was still broken.

**Run after pandoc, before the cover injection.** It rewrites nothing else.

    python3 tools/fix-docx-media.py FILE.docx [FILE.docx ...]
"""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

# **Extension to MIME, for everything pandoc might embed.** `emf` and `wmf` appear when a diagram
# comes through a Windows toolchain; harmless to declare and expensive to discover missing.
TYPES = {
    "png": "image/png",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
    "svg": "image/svg+xml",
    "emf": "image/x-emf",
    "wmf": "image/x-wmf",
    "pdf": "application/pdf",
}


def fix(path: Path) -> int:
    """Add any missing Default declaration. Returns how many were added."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        ct = z.read("[Content_Types].xml").decode("utf-8")
        blobs = {n: z.read(n) for n in names}

    present = {n.rsplit(".", 1)[-1].lower() for n in names if "." in n}
    missing = [e for e in sorted(present & set(TYPES))
               if f'Extension="{e}"' not in ct]
    if not missing:
        return 0

    # **Inserted immediately after the opening tag**, because `Default` elements must precede
    # `Override` ones in the schema and pandoc writes its overrides first.
    ins = "".join(f'<Default Extension="{e}" ContentType="{TYPES[e]}"/>' for e in missing)
    i = ct.index(">", ct.index("<Types")) + 1
    ct = ct[:i] + ins + ct[i:]
    blobs["[Content_Types].xml"] = ct.encode("utf-8")

    tmp = path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        # **Order preserved.** Word tolerates reordering, but a diff against the original should
        # show one changed part rather than a reshuffled archive.
        for n in names:
            out.writestr(n, blobs[n])
    shutil.move(str(tmp), str(path))
    return len(missing)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fix-docx-media.py FILE.docx [FILE.docx ...]")
        return 2
    bad = 0
    for a in sys.argv[1:]:
        p = Path(a)
        if not p.exists():
            print(f"  {p.name}: not found")
            bad += 1
            continue
        n = fix(p)
        print(f"  {p.name}: {n} content type(s) restored" if n
              else f"  {p.name}: already complete")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
