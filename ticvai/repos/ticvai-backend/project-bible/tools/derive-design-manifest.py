#!/usr/bin/env python3
"""Write `wireframes/design-manifest.json` — the work list a design session reads instead of asking.

**1,229 screens will not fit in one Claude Design session, and the failure mode is not a crash.**
Past a certain point a session keeps producing plausible frames that no longer match the spec, and
nobody can tell by looking. That is how 155 board files ended up orphaned and archived on
9 and 10 September.

**So the work is cut into batches, and the package remembers which are done.** A session asks this
file what is left; it does not ask a person, and it does not carry the answer in its head from the
last conversation.

The batch unit is the one the work already has:

- **The 73 workshop boards** (`WS01`…) — the client's own unit, nine or ten screens each, and the
  grouping `source.pack` + `source.board` already carries. Codes match `derive-wireframes.py`.
- **Platform + module**, ten at a time, for everything that did not come from a pack.

**Status is read off the disk, never stored.** A batch is `drawn` when every screen in it has a
frame in `wireframes/frames/`, `partial` when some do, `pending` when none do. Nothing has to be
marked complete by hand, so nothing can claim to be complete and not be.

**`drawable` is the number that decides the order.** A screen with four or more components can be
drawn from what it declares; one with fewer cannot, and a session drawing it is inventing
requirements that will come back looking finished. 470 of the 1,229 are in that state and 130
declare no components at all — so the drawable batches go first and the thin ones wait for
specification work rather than design time.

Idempotent, derived, no arguments. Run it from `refresh.sh`.
"""

from __future__ import annotations

import json
import math
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
FRAMES = ROOT / "wireframes" / "frames"
OUT = ROOT / "wireframes" / "design-manifest.json"

BATCH_SIZE = 10
DRAWABLE_AT = 4          # components below which the board would be inventing, not rendering

# **Platforms a batch would not improve.** Locking one here means no batch is ever cut for it,
# rather than relying on whoever runs the export to remember why.
LOCKED = {
    "P04": ("Already built, and better than a batch would build it. "
            "`sources/designs/TICVAI_POS_Terminal_client_approved.html` is a working Claude Design "
            "terminal for these 29 screens and is the fidelity reference every other batch is "
            "measured against. Cutting a batch for P04 would commission a second, worse version "
            "of an artefact the client has already responded to. Its screens were enriched from "
            "the prototype on 10 September rather than redesigned. "
            "**Brought inside the package on 10 September.** It had been sitting at the repository "
            "root as `TICVAI POS Terminal (1) 1.html`, where the root ignore rule (`/*`, with "
            "`!/*/` letting the folders back in) kept it out of git entirely -- so the one "
            "artefact all 169 batches are measured against existed on a single machine and in no "
            "clone."),
}


def _utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def module_of(pack: str) -> str:
    """`Access Control Module_Reference.pdf` is the module the workshop called it."""
    stem = re.sub(r"\.pdf$", "", pack, flags=re.I)
    stem = re.sub(r"[_ ]*Reference$", "", stem, flags=re.I)
    stem = re.sub(r"[_ ]*Module$", "", stem, flags=re.I)
    return stem.replace("_", " ").strip() or pack


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "screens"


def components(screen: dict) -> int:
    return sum(len(r.get("components") or [])
               for r in ((screen.get("layout") or {}).get("regions") or []))


def collect() -> tuple[list, dict]:
    """Every batch, and the screen records they point at."""
    screens: dict = {}
    workshop: dict = {}
    modules: dict = {}

    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            screens[s["id"]] = (code, s)
            src = s.get("source") or {}
            if src.get("pack") and src.get("board") is not None:
                workshop.setdefault((module_of(src["pack"]), int(src["board"])), []).append(s["id"])
            else:
                modules.setdefault((code, s.get("module") or "Screens"), []).append(s["id"])

    batches = []
    for i, key in enumerate(sorted(workshop), 1):
        ids = sorted(workshop[key])
        batches.append({
            "id": "WS%02d" % i,
            "kind": "workshop",
            "label": "%s board %d" % key,
            "platform": screens[ids[0]][0],
            "screens": ids,
        })

    # **Ten at a time, and the split is by count rather than by anything clever.** `P06 Operations`
    # is 46 screens; one session cannot hold it and a reviewer cannot read it in a pass either.
    for code, mod in sorted(modules):
        ids = sorted(modules[(code, mod)])
        parts = max(1, math.ceil(len(ids) / BATCH_SIZE))
        for n in range(parts):
            chunk = ids[n * BATCH_SIZE:(n + 1) * BATCH_SIZE]
            if not chunk:
                continue
            batches.append({
                "id": "%s-%s-%02d" % (code, slug(mod)[:24], n + 1),
                "kind": "module",
                "label": "%s · %s%s" % (code, mod, "" if parts == 1 else " (%d of %d)" % (n + 1, parts)),
                "platform": code,
                "screens": chunk,
            })

    return batches, screens


def main() -> int:
    _utf8_stdout()
    batches, screens = collect()
    drawn_ids = {p.stem.upper() for p in FRAMES.glob("*.html")} if FRAMES.exists() else set()

    for b in batches:
        specs = [screens[i][1] for i in b["screens"]]
        b["drawable"] = sum(1 for s in specs if components(s) >= DRAWABLE_AT)
        b["thin"] = len(specs) - b["drawable"]
        b["frames"] = sum(1 for i in b["screens"] if i in drawn_ids)
        if b["platform"] in LOCKED:
            b["status"] = "locked"
            b["lockedReason"] = LOCKED[b["platform"]]
        elif b["frames"] == len(b["screens"]):
            b["status"] = "drawn"
        elif b["frames"]:
            b["status"] = "partial"
        else:
            b["status"] = "pending"

    # **Fully drawable batches first.** Drawing a thin screen produces a requirement nobody wrote,
    # so those wait for specification rather than for design time. Within a tier, `id` order —
    # a stable order means two people picking "the next batch" pick the same one.
    order = {"pending": 0, "partial": 0, "drawn": 1, "locked": 2}
    batches.sort(key=lambda b: (order[b["status"]], b["thin"] > 0, b["thin"], b["id"]))

    doc = {
        "generatedBy": "tools/derive-design-manifest.py",
        "generated": date.today().isoformat(),
        "note": ("The Claude Design work list. Status is read off wireframes/frames/ every run and "
                 "never stored, so a batch cannot claim to be finished and not be. Batches with "
                 "thin screens sort last: a screen with fewer than %d components cannot be drawn "
                 "from what it declares, and drawing it invents requirements." % DRAWABLE_AT),
        "batchSize": BATCH_SIZE,
        "drawableAt": DRAWABLE_AT,
        "locked": LOCKED,
        "counts": {
            "batches": len(batches),
            "screens": sum(len(b["screens"]) for b in batches),
            "framesOnDisk": len(drawn_ids),
            "byStatus": {k: sum(1 for b in batches if b["status"] == k)
                         for k in ("pending", "partial", "drawn", "locked")},
            "screensByStatus": {k: sum(len(b["screens"]) for b in batches if b["status"] == k)
                                for k in ("pending", "partial", "drawn", "locked")},
            "fullyDrawableBatches": sum(1 for b in batches
                                        if b["thin"] == 0 and b["status"] != "locked"),
        },
        "batches": batches,
    }
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")

    c = doc["counts"]
    print("  %d batch(es) · %d screens · %d frame(s) on disk"
          % (c["batches"], c["screens"], c["framesOnDisk"]))
    print("    %-9s %d batch(es), %d screen(s)"
          % ("pending", c["byStatus"]["pending"], c["screensByStatus"]["pending"]))
    for k in ("partial", "drawn", "locked"):
        if c["byStatus"][k]:
            print("    %-9s %d batch(es), %d screen(s)"
                  % (k, c["byStatus"][k], c["screensByStatus"][k]))
    print("    %d batch(es) are fully drawable as specified" % c["fullyDrawableBatches"])
    nxt = next((b for b in batches if b["status"] in ("pending", "partial")), None)
    if nxt:
        print("  next: %s — %s (%d screens, %d thin)"
              % (nxt["id"], nxt["label"], len(nxt["screens"]), nxt["thin"]))
    print("  -> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
