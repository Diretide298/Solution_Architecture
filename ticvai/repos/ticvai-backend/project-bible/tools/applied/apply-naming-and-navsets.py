#!/usr/bin/env python3
"""Three corrections the duplicate-name check surfaced, and the navigation sets nothing defined.

**Same name, three different defects.** The checker reports name collisions and cannot tell them
apart; comparing operations, modules and purposes can.

1. **`ADM-321` is a duplicate of `ADM-241` and is collapsed.** Both are *Visual Workflow Designer*,
   both in Platform, both wave 3. `ADM-241` has an operation and two layout regions; `ADM-321` has
   **none of either**, and its purpose reads *"This should be the main configuration screen of
   Board 2"* — pack instruction text rather than a screen. Same case as `ANL-011`, resolved the
   same way: purpose and gaps carried across, the one inbound edge repointed, the screen removed.

2. **`BO-020` and `BO-047` are not duplicates — one is misnamed.** Different modules, different
   waves, and **not one operation in common** between 11 and 14. `BO-047` is called *F&B Order
   Management* while its own purpose says *"Fix an order that has gone wrong"* and all fourteen of
   its operations are order lifecycle — void, refund, exchange, reschedule, reprint, hold, manual
   discount. It is renamed to match what it does. `BO-020`, which really is F&B order management,
   keeps the name.

3. **`BO-031` / `BO-069` is left alone.** `BO-031`'s seven operations are a strict subset of
   `BO-069`'s eleven, which looks like a duplicate — but their purposes differ ("define what a gate
   is" against "know what equipment exists"). A subset with a different stated intent is a product
   question, and this tool does not answer those.

**And the two navigation sets.** 16 P04 screens named `posPrimaryRail` or `posSaleToPayment` in
`navigation.uses` and **nothing anywhere defined either**. Both were checked against what their
members actually do:

- **`posSaleToPayment` is real.** All seven members exit to `POS-005 Payment`; most also return to
  `POS-002`. It is defined from that evidence.
- **`posPrimaryRail` is not.** Its twelve members share **no common destination at all** — zero.
  Whatever rail was intended, the screens do not implement it. It is declared as unrealised and
  carries the count, rather than being quietly given a plausible membership.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations
import glob
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
COLLAPSE = ("ADM-321", "ADM-241")
RENAME = ("BO-047", "Order Corrections & Exceptions")


def main() -> int:
    apply = "--apply" in sys.argv
    docs = {f: yaml.safe_load(open(f, encoding="utf-8"))
            for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))}
    screens = {s["id"]: s for d in docs.values() for s in d["screens"]}
    todo = []

    # --- 1. collapse ------------------------------------------------------------------
    drop, keep = COLLAPSE
    if drop in screens:
        todo.append(f"collapse {drop} into {keep}")
        if apply:
            d, k = screens[drop], screens[keep]
            if d.get("purpose") and d["purpose"] != k.get("purpose"):
                k.setdefault("purposeNote", d["purpose"])
            for g in (d.get("gaps") or []):
                if g not in (k.get("gaps") or []):
                    k.setdefault("gaps", []).append(g)
            for s in screens.values():
                nav = s.get("navigation") or {}
                for key in ("exitTo", "entryFrom"):
                    if drop in (nav.get(key) or []):
                        nav[key] = sorted({keep if x == drop else x for x in nav[key]})
                for t in (nav.get("transitions") or []):
                    if str(t.get("to", "")).partition("#")[0] == drop:
                        t["to"] = keep
                        t["trigger"] = f"Back to {screens[keep]['name']}" \
                            if t.get("back") else t.get("trigger")
            for doc in docs.values():
                before = len(doc["screens"])
                doc["screens"] = [s for s in doc["screens"] if s["id"] != drop]
                if len(doc["screens"]) != before and "screenCount" in doc["platform"]:
                    doc["platform"]["screenCount"] = len(doc["screens"])

    # --- 2. rename --------------------------------------------------------------------
    sid, newname = RENAME
    if sid in screens and screens[sid]["name"] != newname:
        todo.append(f"rename {sid} {screens[sid]['name']!r} -> {newname!r}")
        if apply:
            screens[sid]["nameNote"] = (
                "**Renamed 9 September 2026.** It was called *F&B Order Management*, which is "
                "BO-020's job and shares not one of this screen's fourteen operations. Its own "
                "purpose — fix an order that has gone wrong — is what it is called now.")
            screens[sid]["name"] = newname

    # --- 3. navigation sets -----------------------------------------------------------
    for f, doc in docs.items():
        if doc["platform"]["code"] != "P04":
            continue
        members = {}
        for s in doc["screens"]:
            for u in ((s.get("navigation") or {}).get("uses") or []):
                members.setdefault(u, []).append(s["id"])
        if not members:
            continue
        exits = {i: set(((screens[i].get("navigation") or {}).get("exitTo") or []))
                 for ids in members.values() for i in ids}
        sets = {}
        for name, ids in sorted(members.items()):
            common = set.intersection(*[exits[i] for i in ids]) if ids else set()
            block = {"members": sorted(ids)}
            if common:
                block["destinations"] = sorted(common)
                block["provenance"] = (f"derived — every one of the {len(ids)} screens naming this "
                                       f"set exits to all of them")
            else:
                block["destinations"] = []
                block["unrealised"] = (
                    f"**Named by {len(ids)} screens and implemented by none of them.** They share "
                    f"no destination at all, so there is nothing here to call a rail. Either the "
                    f"shared exits are missing from those screens or the key is wrong — but a "
                    f"plausible membership invented here would read as fact.")
            sets[name] = block
        if doc["platform"].get("navigationSets") != sets:
            todo.append(f"P04: define navigationSets — "
                        + ", ".join(f"{k} ({len(v['destinations'])} destination(s))"
                                    for k, v in sets.items()))
            if apply:
                doc["platform"]["navigationSets"] = sets

    if not todo:
        print("nothing to do")
        return 0
    for t in todo:
        print(f"  {t}")
    if apply:
        for f, d in docs.items():
            pathlib.Path(f).write_text(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8")
        print(f"\nwritten to {len(docs)} platform file(s)")
    else:
        print("\nrun with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
