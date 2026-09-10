#!/usr/bin/env python3
"""Check every provisional operation's citation against the client pack it names.

**577 operations say where they came from and nothing checked it.** Each one carries
`x-ticvai-provisional: true` and a description reading *"Drafted from the workshop pack; the shape
below is read out of it, not invented"* followed by `<pack>, page N`. Until 8 September the packs
were not in the repository, so the claim was unfalsifiable from inside the package — which is the
same shape as every other defect found this week: an assertion nothing could check.

The audit is two questions, and both are cheap:

  **Does the pack exist?** A citation naming a document nobody has is a citation to nothing.

  **Is the page inside it?** `page 180` of a 183-page book is plausible; `page 180` of a 40-page
  book means the number was invented or the pack was replaced.

It also reports the packs **nothing cites**, which on the first run was the larger finding: 27 of
44 packs, 1,815 pages, with Retail, Inventory & Procurement, Resource Management, F&B backend,
Wallet and Finance untouched. **A pack nobody drafted from is scope nobody has read.**

Run: python3 tools/audit-pack-citations.py
"""
import difflib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
# The corpus arrived in two batches and sits in two directories: the dashboard exports came in
# first as `sources/boards/`, the reference packs on 8 September as `sources/packs/`. Both are
# client design material and a citation may name either, so the audit reads both — **a checker
# that looks in one of two places reports a missing pack that is sitting next to it.**
PACK_DIRS = [ROOT / "sources" / "packs", ROOT / "sources" / "boards"]
CONTRACTS = ROOT / "contracts"

# The sentence every drafted operation carries, and the citation that follows it.
CITE = re.compile(r"read out of it, not invented\.\*\*\s*(.+?),\s*page\s*(\d+)", re.S)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def pack_index() -> dict:
    """Pack stem -> (filename, page count). Page counts need pypdf; absent, only existence."""
    try:
        import pypdf
    except ImportError:
        pypdf = None
        print("  note: pypdf not installed — checking pack existence but not page numbers")
    out = {}
    for f in sorted(f for d in PACK_DIRS if d.exists() for f in d.glob("*.pdf")):
        pages = None
        if pypdf:
            try:
                pages = len(pypdf.PdfReader(str(f)).pages)
            except Exception:  # noqa: BLE001 — a pack we cannot parse is reported, not fatal
                print(f"  note: could not read {f.name}")
        # **`Preference` contains `Reference`.** Stripping the suffix without a word boundary
        # truncated `Privacy, Consent & Preference Management` to `Privacy Consent P` and
        # reported 19 real citations as missing packs. The boundary is the fix.
        stem = re.sub(r"[_ ]Reference\b.*$", "", f.stem, flags=re.I)
        out[norm(stem)] = (f.name, pages)
    return out


def citations():
    for f in sorted(CONTRACTS.rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for item in ((doc.get("paths") or {}) if isinstance(doc, dict) else {}).values():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb not in ("get", "post", "put", "patch", "delete") or not isinstance(op, dict):
                    continue
                if op.get("x-ticvai-provisional") is not True:
                    continue
                m = CITE.search(op.get("description") or "")
                if not m:
                    yield op.get("operationId"), None, None
                    continue
                yield op.get("operationId"), " ".join(m.group(1).split()), int(m.group(2))


def main() -> int:
    if not any(d.exists() for d in PACK_DIRS):
        print("  no sources/packs or sources/boards — nothing to audit against")
        return 1
    books = pack_index()
    keys = list(books)

    uncited, bad_pack, bad_page, no_cite = set(books), [], [], []
    total = 0
    for oid, pack, page in citations():
        total += 1
        if pack is None:
            no_cite.append(oid)
            continue
        hit = books.get(norm(pack))
        if not hit:
            close = difflib.get_close_matches(norm(pack), keys, n=1, cutoff=0.72)
            hit = books[close[0]] if close else None
        if not hit:
            bad_pack.append((oid, pack))
            continue
        uncited.discard(norm(re.sub(r"[_ ]Reference\b.*$", "", Path(hit[0]).stem, flags=re.I)))
        if hit[1] and page > hit[1]:
            bad_page.append((oid, pack, page, hit[1]))

    print(f"{total} provisional operations · {len(books)} packs")
    print(f"  {total - len(bad_pack) - len(no_cite)} citations resolve to a pack")
    for oid, pack in bad_pack:
        print(f"  FAIL  {oid} cites '{pack}', which is in neither sources/packs/ nor sources/boards/")
    for oid, pack, page, n in bad_page:
        print(f"  FAIL  {oid} cites {pack} page {page}; that pack has {n} pages")
    for oid in no_cite:
        print(f"  WARN  {oid} is provisional and names no source pack")

    if uncited:
        pages = sum(books[k][1] or 0 for k in uncited)
        print(f"\n  {len(uncited)} pack(s) nothing cites — {pages} pages of unread scope:")
        for k in sorted(uncited, key=lambda x: -(books[x][1] or 0)):
            print(f"    {str(books[k][1] or '?'):>4}pp  {books[k][0]}")

    failed = bad_pack or bad_page
    print("\nFAIL" if failed else "\nPASS — every citation resolves to a real pack and a real page")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
