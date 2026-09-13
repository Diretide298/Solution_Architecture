#!/usr/bin/env python3
"""Guest web and guest app say the same thing when the connection drops.

**Decided 12 September 2026: guest web and guest app should be identical, offline included, and
both tell the guest to go online with the same banner.**

Until today they disagreed completely. **All 71 app screens declared an offline state and none of
the 46 web screens did**, so a guest whose signal dropped on the website saw *"Could not load"* —
which reads as the venue being down. And the app's generated boards stamped every guest screen
*"works from the local journal"*, a line written for the till.

**The web is still not offline-capable and this does not pretend it is.** The difference is kept
where it is true — `platform.offlineCapable`, and the app's store surviving a restart — and taken
out of what the guest reads. Every offline state is written to be true on both: *"already loaded"*
is this visit's page on the web and the device's store on the app.

What it writes, from `screens/_guest-pairs.yaml`:

  - `platform.offlineBanner` on P01 and P02, the same object on both
  - `states.offline` on every P01 and P02 screen — one text per capability group, word for word

**Meant to be re-run**, like `apply-rental-staff-app.py`: after a guest screen is added or its
offline state edited by hand, run it again or `check-screens` fails the group for disagreeing.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"
FILES = {"P01": SCREENS / "P01-guest-web-storefront.yaml",
         "P02": SCREENS / "P02-guest-mobile-app.yaml"}
PAIRS = SCREENS / "_guest-pairs.yaml"

# **The same pattern `check-screens` reads as a promise of continued function.** A text matching
# it would be true on the app and false on the web, so it is refused here rather than warned later.
CLAIMS = re.compile(r"keeps working|continues|works from|from the (cached|local)|"
                    r"still (works|takes|sells)|local journal|sells from|selling continues", re.I)


def dump(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    apply = "--apply" in sys.argv
    pairs = yaml.safe_load(PAIRS.read_text(encoding="utf-8"))
    banner = pairs["banner"]
    default = " ".join(pairs["defaultOffline"].split())

    raw = {c: p.read_text(encoding="utf-8") for c, p in FILES.items()}
    docs = {c: yaml.safe_load(t) for c, t in raw.items()}
    for c, t in raw.items():
        if dump(docs[c]) != t:
            print(f"  ! {FILES[c].name} does not round-trip through safe_dump — the write would "
                  "reformat lines this tool did not change. Stopping.")
            return 1

    by_id = {s["id"]: s for d in docs.values() for s in d["screens"]}
    seen: dict[str, str] = {}
    problems, changes = [], []

    for g in pairs["groups"]:
        text = " ".join(str(g.get("offline") or default).split())
        if CLAIMS.search(text):
            problems.append(f"{g['key']}: offline text promises continued function — "
                            f"'{CLAIMS.search(text).group(0)}'")
        for sid in (g.get("web") or []) + (g.get("app") or []):
            if sid in seen:
                problems.append(f"{sid} is in two groups, {seen[sid]} and {g['key']}")
            seen[sid] = g["key"]
            s = by_id.get(sid)
            if s is None:
                problems.append(f"{g['key']} names {sid}, which does not exist")
                continue
            states = s.setdefault("states", {})
            if states.get("offline") != text:
                changes.append(f"{sid} offline state ({g['key']})")
                states["offline"] = text

    for sid in by_id:
        if sid not in seen:
            problems.append(f"{sid} is in no group of _guest-pairs.yaml")

    for c, d in docs.items():
        p = d["platform"]
        if p.get("offlineBanner") != banner:
            changes.append(f"{c} offlineBanner")
            rebuilt = {}
            for k, v in p.items():
                if k == "offlineBanner":
                    continue
                rebuilt[k] = v
                if k == "offlineCapable":
                    rebuilt["offlineBanner"] = banner
            rebuilt.setdefault("offlineBanner", banner)
            d["platform"] = rebuilt
            d_ordered = {"platform": rebuilt, **{k: v for k, v in d.items() if k != "platform"}}
            docs[c] = d_ordered

    for p in problems:
        print(f"  ! {p}")
    if problems:
        print(f"\n{len(problems)} problem(s) — nothing written")
        return 1
    if not changes:
        print("nothing to do — guest web and app carry one banner and agree offline, group by group")
        return 0
    print(f"{len(changes)} change(s): {sum('offline state' in x for x in changes)} offline states, "
          f"{sum('offlineBanner' in x for x in changes)} banners")
    for x in changes[:12]:
        print(f"  {x}")
    if len(changes) > 12:
        print(f"  … and {len(changes) - 12} more")
    if not apply:
        print("\nrun with --apply to write")
        return 0
    for c, d in docs.items():
        tmp = FILES[c].with_suffix(".yaml.tmp")
        tmp.write_text(dump(d), encoding="utf-8")
        os.replace(tmp, FILES[c])
    print("\nwritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
