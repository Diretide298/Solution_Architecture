#!/usr/bin/env python3
"""Record every screen id that has been issued, so two workstreams cannot issue the same one.

**On 4 September two workstreams both allocated ADM-038.** Each computed max+1 over the screens it
could see, neither could see the other, and nothing in the package held a number — so one
'Dead Letters' and one 'Communication Service Command Center' were both correct and both wrong.
Neither side did anything unreasonable; the estate simply had no issue log.

**A number in this register is spent.** An allocator starts above the highest number RECORDED
rather than above the highest number it happens to have loaded, which is the difference between
two workstreams agreeing and merely not overlapping yet.

**A retired id is never reissued.** `nextFree` is the high-water mark plus one, gaps and all —
`EMP` has issued 66 ids across the range 1-70, and those four gaps stay gaps. Reusing a deleted
screen's number is how a link in a six-month-old document opens the wrong screen.

`tools/check-screens.py` fails on a screen issued above the recorded high-water mark, so the
register has to be regenerated and committed in the same change that adds screens.

Run: `python3 tools/derive-id-register.py [--apply]`
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
OUT = SCREENS / "_id-register.yaml"

NOTE = (
    "**The issue log for screen ids, and the reason it exists.** On 4 September two workstreams "
    "both allocated ADM-038 — each took max+1 of the same prefix, neither could see the other, and "
    "nothing in the package held a number. One was 'Dead Letters', the other 'Communication "
    "Service Command Center'. The collision was silent on both sides.\n\n"
    "**An id appears here when it is issued, not when it is built.** That is the whole mechanism: "
    "a number in this file is spent, and the next allocator starts above the highest number "
    "recorded rather than above the highest number it can see.\n\n"
    "**A retired id is never reissued.** `nextFree` is the high-water mark plus one, gaps "
    "included — reusing a deleted screen's number is how an old link opens the wrong screen.\n\n"
    "`tools/check-screens.py` fails on a screen issued above the recorded high-water mark. "
    "Regenerate with `tools/derive-id-register.py --apply` and commit it in the same change.")


def collect() -> dict:
    reg: dict = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for s in doc["screens"]:
            pre, num = s["id"].rsplit("-", 1)
            origin = "pack" if (s.get("source") or {}).get("pack") else "authored"
            reg.setdefault(pre, {})[int(num)] = origin
    return reg


def build(reg: dict) -> dict:
    out = {"_note": NOTE, "generatedBy": "tools/derive-id-register.py",
           "updated": str(datetime.date.today()), "prefixes": {}}
    for pre in sorted(reg):
        nums = reg[pre]
        packn = sorted(n for n, o in nums.items() if o == "pack")
        auth = sorted(n for n, o in nums.items() if o == "authored")
        out["prefixes"][pre] = {
            "issued": len(nums),
            "highWaterMark": max(nums),
            "nextFree": max(nums) + 1,
            "authored": ("%d-%d" % (min(auth), max(auth))) if auth else None,
            "generatedPack": ("%d-%d" % (min(packn), max(packn))) if packn else None,
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    reg = collect()
    out = build(reg)
    total = sum(len(v) for v in reg.values())
    print("%d ids across %d prefixes" % (total, len(reg)))
    for pre, v in out["prefixes"].items():
        print("  %-4s issued %-4d next free %-4d  authored %-9s pack %s"
              % (pre, v["issued"], v["nextFree"], v["authored"], v["generatedPack"]))

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    OUT.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=100),
                   encoding="utf-8")
    print("  -> screens/%s" % OUT.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
