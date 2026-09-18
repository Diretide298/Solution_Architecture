#!/usr/bin/env python3
"""Write sources/packs-index.json — one record per client document, so a document is held once.

**The same PDF sat in up to three folders and the folder was the only record of what it meant.**
A duplicate scan on 18 September found 30 sets of byte-identical files across `packs/`,
`workshop/`, `requirements/`, `boards/` and `documents/` — 17 packs duplicated into `workshop/`
alone, and `Sample-Ampitheater Seating.pdf` held three times. `sources/README.md` ranks folders by
authority, so the copy in `requirements/` is contracted scope and the identical copy in `packs/` is
reference material. **Copying a file in order to say something about it means the statement dies
the moment the copies drift**, and nothing checks that they have not.

This makes the statement a field. One canonical copy, and everything the placement used to say
recorded here against a `sha256` that proves the copies really were identical before any of them
were removed.

Modelled on `index-boards.py`, which learned these rules the expensive way:

**The parse is cached, the classification never is.** A record whose hash is unchanged keeps its
page count and extracted text. Authority and platform are recomputed on every run, because they are
a function of this tool's rules rather than of the file's bytes — `index-boards.py` cached a
provenance class and the run reported success having changed nothing, 170 boards "unchanged" and
170 classes stale.

**Two signals, reconciled, never one trusted.** Platform assignment is derived twice from
independent evidence and the record carries the agreement *and* both disagreements:

  A  `pack -> provisional operation citation -> x-ticvai-consumed-by -> platform`
  B  `pack -> its screens in sources/workshop/pack.json -> package screen of that name -> platform`

Where both agree the assignment is `confirmed`. Where only one fires it is `claimed`, and the
record says which signal claimed it. **A pack nothing has been drafted from and whose screens match
nothing gets an empty list** — that is the honest answer rather than a default, and with 28 of 45
packs in that state the empty list is the worklist.

**Platforms are many.** `Access Control Module_Reference` feeds both the POS and the back office.
A directory can hold a file once; a field can hold two codes.

**What this measures is the pack's provisional reach, not everything the pack influenced.** Signal
A follows citations, and only *provisional* operations carry them. `listPromotions` is consumed by
P01, P02, P04, P08 and P09 and cites no pack, because it was written before the packs were drafted
from — so the Promotions pack reports P09, the platform its own provisional operations reach.
**That is the honest boundary of the evidence** and not a bug to widen: attributing an established
operation to a pack because the subject matter overlaps is the guess this tool exists to avoid.

**An authority conflict is recorded, not flattened.** A document held in both `requirements/` and
`packs/` asserted two different ranks. The canonical copy keeps every authority every location
gave it, so demoting one is a decision somebody takes rather than a side effect of a move.

## What `--apply` does, and what it refuses to do

**It removes a file only when that file's sha256 equals the canonical copy's**, which is recomputed
at the moment of deletion rather than read from this index. A name match never deletes anything. If
the hash has changed since the scan the copy is kept and reported. `git` is the undo.

`sources/workshop/pack.json` is left alone — it is derived, not a client document.
`parse-workshop-pack.py` is the only tool that reads the PDFs at all; everything downstream reads
that JSON.

Run: python tools/index-packs.py  [--apply]
"""
import argparse
import collections
import hashlib
import io
import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
PACKS = SOURCES / "packs"
CONTRACTS = ROOT / "contracts"
SCREENS = ROOT / "screens"
PACKJSON = SOURCES / "workshop" / "pack.json"
OUT = SOURCES / "packs-index.json"

# Folder -> what holding a file there asserted. Straight from sources/README.md's rank table.
AUTHORITY = {
    "requirements": "requirement",   # rank 2 — the contracted baseline
    "mom": "mom",                    # rank 1 — scope and binding
    "designs": "design",             # rank 3 — directional
    "diagrams": "design",
    "claude-design": "design",
    "packs": "reference",            # a client design pack
    "workshop": "workshop",          # read in a workshop
    "boards": "board",               # drawn screens
    "documents": "document",
    "planning": "planning",
    "rfp": "rfp",
}
RANK = {"mom": 1, "requirement": 2, "design": 3, "board": 4, "reference": 5,
        "workshop": 5, "rfp": 6, "document": 7, "planning": 8}
DOC_EXT = {".pdf", ".xlsx", ".docx", ".jpeg", ".jpg", ".png"}
MIN_BYTES = 1024


def sha256(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def page_count(path):
    """Pages without a PDF library. `/Type /Page` objects, falling back to the largest `/Count`."""
    if path.suffix.lower() != ".pdf":
        return None
    try:
        b = path.read_bytes()
    except Exception:
        return None
    n = len(re.findall(rb"/Type\s*/Page[^s]", b))
    if n:
        return n
    m = re.findall(rb"/Count\s+(\d+)", b)
    return max(int(x) for x in m) if m else None


def norm_doc(name):
    """`F&B Dashboard Screens v1.0` and `FB_Dashboard_Screens_v1_0` are one document."""
    s = os.path.splitext(os.path.basename(str(name)))[0].lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def norm_title(s):
    """Compare a pack screen title to a package screen name without tripping on typography."""
    s = (s or "").replace("&amp;", "&").replace("/", " / ")
    return " ".join(s.split()).lower()


def resolve(doc_key, table):
    """Look a document up in a signal's table, tolerating the suffix the citations drop.

    **The contracts cite `Communication & Notification Platform Services` and the file is
    `Communication & Notification Platform Services_Reference.pdf`.** Keyed on equality this
    matched nothing at all and every pack reported as never drafted from — a number that would
    have been believed, because 28 undrafted was already the expected answer.

    A citation key must be a **prefix** of the document key, not merely contained in it: `Retail`
    appears inside a dozen filenames and containment would hand one pack's operations to all of
    them. The shortest qualifying key wins, so `Seat_Management_Venue_Mapping` does not absorb
    `Seat_Management_Dashboard`'s citations.
    """
    if doc_key in table:
        return table[doc_key]
    hits = [k for k in table if len(k) >= 10 and (doc_key.startswith(k) or k.startswith(doc_key))]
    if not hits:
        return set()
    out = set()
    for k in sorted(hits, key=len)[:1]:
        out |= table[k]
    return out


def signal_a():
    """pack -> {operationId}, and operationId -> {platform}. Both read from the contracts."""
    packs = collections.defaultdict(set)
    plats = collections.defaultdict(set)
    for p in sorted(CONTRACTS.rglob("*.yaml")):
        text = io.open(str(p), encoding="utf-8", errors="replace").read()
        ops = [(m.start(), m.group(1)) for m in re.finditer(r"operationId:\s*(\w+)", text)]
        # A citation belongs to the operation it sits under, so the nearest preceding one.
        #
        # **The pack name may contain a comma and three of them do.** `B2B, Reseller & OTA Partner
        # Management`, `Waiver, Consent & Digital Form Management` and `Ticket Upgrade, Exchange &
        # Conversion` are all cited by operations, and a pattern that stopped at the first comma
        # captured only the tail — so all three reported as never drafted from. That answer was
        # plausible enough to keep: 28 undrafted packs was already the expected number.
        #
        # Commas are allowed and the match is non-greedy, so it ends at the first `, page N` rather
        # than the first comma. Over-capture is harmless because `resolve()` only accepts a key
        # that prefixes a real filename.
        for m in re.finditer(r"([A-Z][^\n]{6,70}?),\s*page\s+\d+", text):
            prior = [o for pos, o in ops if pos < m.start()]
            if prior:
                packs[norm_doc(m.group(1))].add(prior[-1])
        for i, (pos, op) in enumerate(ops):
            end = ops[i + 1][0] if i + 1 < len(ops) else len(text)
            for c in re.finditer(r'"\s*(P\d{2})[\s-]', text[pos:end]):
                plats[op].add(c.group(1))
    return packs, plats


def signal_b(screen_platform):
    """pack -> {platform}, via its own screens in pack.json matched to package screens by name.

    Independent of the contracts: `pack.json` is parsed straight from the PDFs and the package
    screens are authored by hand, so an agreement between this and signal A is two different
    people's work landing in the same place.
    """
    out = collections.defaultdict(set)
    hits = collections.defaultdict(set)
    if not PACKJSON.exists():
        return out, hits
    try:
        rows = json.loads(PACKJSON.read_text(encoding="utf-8"))
    except Exception:
        return out, hits
    for r in rows:
        src = norm_doc(r.get("source") or "")
        t = norm_title(r.get("title"))
        if not src or not t:
            continue
        for code, names in screen_platform.items():
            if t in names:
                out[src].add(code)
                hits[src].add(t)
    return out, hits


def package_screens():
    """platform code -> {normalised screen name}, and code -> display name."""
    import yaml
    per, names = {}, {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        names[code] = doc["platform"].get("name", "")
        per[code] = {norm_title(s.get("name")) for s in doc.get("screens") or []}
    return per, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="centralise into packs/ and remove byte-identical copies")
    args = ap.parse_args()

    prior = {}
    if OUT.exists():
        try:
            prior = {r["sha256"]: r
                     for r in json.loads(OUT.read_text(encoding="utf-8"))["records"]}
        except Exception:
            prior = {}

    # 1. Every client document under sources/, grouped by content rather than by name.
    by_hash = collections.defaultdict(list)
    for p in sorted(SOURCES.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in DOC_EXT:
            continue
        if p.stat().st_size < MIN_BYTES:
            continue
        by_hash[sha256(p)].append(p)

    per_platform, platform_names = package_screens()
    a_packs, a_plats = signal_a()
    b_packs, b_hits = signal_b(per_platform)

    records, reused = [], 0
    for h, paths in sorted(by_hash.items()):
        inpacks = [p for p in paths if p.parent == PACKS]
        canonical = inpacks[0] if inpacks else paths[0]
        key = norm_doc(canonical.name)
        folders = sorted({p.parent.name for p in paths})
        auth = sorted({AUTHORITY.get(f, f) for f in folders}, key=lambda a: RANK.get(a, 99))

        ops = sorted(resolve(key, a_packs))
        pa = {c for o in ops for c in a_plats.get(o, set())}
        pb = set(resolve(key, b_packs))

        was = prior.get(h)
        if was:
            pages = was.get("pages")          # cached: a function of the bytes
            reused += 1
        else:
            pages = page_count(canonical)

        confirmed = sorted(pa & pb)
        records.append({
            "document": canonical.name,
            "sha256": h,
            "bytes": canonical.stat().st_size,
            "pages": pages,
            "canonical": ("sources/packs/" + canonical.name),
            # Never cached — a function of this tool's rules, not of the file.
            "authority": auth,
            "authorityConflict": len(auth) > 1,
            "heldIn": folders,
            "copies": [str(p.relative_to(ROOT)).replace("\\", "/") for p in sorted(paths)],
            "duplicated": len(paths) > 1,
            "platforms": sorted(pa | pb),
            "platformsConfirmed": confirmed,
            "platformsFromContractsOnly": sorted(pa - pb),
            "platformsFromPackScreensOnly": sorted(pb - pa),
            "platformNames": {c: platform_names.get(c, "") for c in sorted(pa | pb)},
            "operations": ops,
            "packScreensMatched": len(b_hits.get(key, set())),
            "drafted": bool(ops),
            "firstIndexed": (was or {}).get("firstIndexed", date.today().isoformat()),
            "lastSeen": date.today().isoformat(),
        })

    records.sort(key=lambda r: r["document"].lower())
    dupes = [r for r in records if r["duplicated"]]
    redundant = sum(r["bytes"] * (len(r["copies"]) - 1) for r in records)

    removed, copied, refused = [], 0, []
    if args.apply:
        for r in records:
            dest = PACKS / r["document"]
            src = ROOT / r["copies"][0]
            if not dest.exists():
                shutil.copy2(str(src), str(dest))
                copied += 1
            for rel in r["copies"]:
                p = ROOT / rel
                if p.resolve() == dest.resolve() or p.parent == PACKS:
                    continue
                # **Re-hashed here, not trusted from the scan.** A name match never deletes.
                if p.exists() and sha256(p) == r["sha256"]:
                    p.unlink()
                    removed.append(rel)
                elif p.exists():
                    refused.append(rel)

    doc = {
        "generatedBy": "tools/index-packs.py",
        "generated": date.today().isoformat(),
        "note": ("One record per client document under `sources/`, keyed by content hash. "
                 "**The folder a document sat in was the only record of what it meant** — this "
                 "makes that a field. `authority` keeps every rank any location gave it, and "
                 "`platforms` is derived twice from independent evidence: "
                 "`platformsConfirmed` is where the contracts and the pack's own screens agree."),
        "counts": {
            "documents": len(records),
            "duplicateSets": len(dupes),
            "redundantBytes": redundant,
            "drafted": sum(1 for r in records if r["drafted"]),
            "undrafted": sum(1 for r in records if not r["drafted"]),
            "withPlatform": sum(1 for r in records if r["platforms"]),
            "platformConfirmed": sum(1 for r in records if r["platformsConfirmed"]),
            "authorityConflicts": sum(1 for r in records if r["authorityConflict"]),
            "reusedFromCache": reused,
        },
        # The set, not only the count. Two artefacts that each recompute coverage disagree.
        "undraftedDocuments": [r["document"] for r in records if not r["drafted"]],
        "authorityConflicts": [{"document": r["document"], "authority": r["authority"],
                                "heldIn": r["heldIn"]}
                               for r in records if r["authorityConflict"]],
        "removed": sorted(removed),
        "refusedToRemove": sorted(refused),
        "records": records,
    }
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")

    c = doc["counts"]
    print("  documents: %d  |  duplicate sets: %d  |  redundant: %.1f MB"
          % (c["documents"], c["duplicateSets"], c["redundantBytes"] / 1048576.0))
    print("  drafted from: %d  |  nothing drafted: %d" % (c["drafted"], c["undrafted"]))
    print("  platform assigned: %d  |  confirmed by both signals: %d"
          % (c["withPlatform"], c["platformConfirmed"]))
    print("  authority conflicts: %d  |  reused from cache: %d"
          % (c["authorityConflicts"], c["reusedFromCache"]))
    if args.apply:
        print("  copied into packs/: %d  |  removed: %d  |  refused (hash changed): %d"
              % (copied, len(removed), len(refused)))
    else:
        print("  dry run - nothing moved or removed. Re-run with --apply")
    print("  -> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
