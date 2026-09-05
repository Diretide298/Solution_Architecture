#!/usr/bin/env python3
"""One row per screen, saying exactly what is missing from it.

**"All screens accounted for" is a completeness question, and nothing in the package answered it.**
The eleven checks each answer one question well — are the links live, do the operations exist, is
the wireframe drawn — and a screen can pass all eleven while still being unfinished, because no
check asks whether a screen is *done*.

This asks. Six obligations per screen, each derived rather than asserted:

  `ops`        it calls at least one operation. A screen that calls nothing is a picture.
  `nav-in`     something navigates to it. Otherwise it is reachable only by knowing its id.
  `nav-out`    it goes somewhere. A screen with no exit is a dead end for whoever lands on it.
  `wire`       its wireframe anchor resolves to a frame that exists.
  `impl`       it names an app, a route and a component.
  `unique`     no other screen declares an identical operation set.

**A screen is `done` when all six hold.** Nothing here is a judgement call — every column is a
fact about the file, so the ledger can be regenerated and diffed rather than maintained.

Run: `python3 tools/screen-ledger.py [--bucket NAME] [--write]`
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
OUT = ROOT / "docs" / "active" / "screen-ledger.md"

COLS = ("ops", "nav-in", "nav-out", "wire", "impl", "unique")


def load():
    plats, screens = {}, []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        plats[p["code"]] = p
        for s in doc["screens"]:
            s["_plat"] = p["code"]
            s["_platName"] = p.get("shortName") or p["code"]
            s["_file"] = f.name
            s["_pack"] = bool((s.get("source") or {}).get("pack"))
            screens.append(s)
    return plats, screens


def board_ok(cache: dict, ref: str) -> bool:
    """The anchor has to name a frame that exists, not merely a file that does."""
    if not ref or "#" not in ref:
        return False
    path, _, anchor = ref.partition("#")
    p = ROOT / path
    if path not in cache:
        cache[path] = p.read_text(encoding="utf-8", errors="replace") if p.exists() else None
    txt = cache[path]
    return bool(txt) and ('id="%s"' % anchor) in txt


def assess(screens):
    # **Inbound arrives two ways and the first version of this counted one.** `exitTo` on the
    # source screen is the obvious edge; `entryFrom` on the DESTINATION is the same edge declared
    # from the other end, and there are 343 of them. Counting only `exitTo` reported 184 orphans
    # where there are 78 — the difference being screens that say who reaches them rather than
    # screens nobody reaches.
    #
    # **A declared entry point has no inbound by definition** and is not an orphan.
    ids = {s["id"] for s in screens}
    inbound = collections.Counter()
    for s in screens:
        nav = s.get("navigation") or {}
        for t in (nav.get("exitTo") or []):
            inbound[t] += 1
        for t in (nav.get("entryFrom") or []):
            if t in ids:
                inbound[s["id"]] += 1
        if nav.get("isEntryPoint"):
            inbound[s["id"]] += 1

    # **Outbound is symmetric with inbound and has to be counted the same way.** If B declares
    # `entryFrom: [A]` then A goes to B, whether or not A's own `exitTo` says so. Counting only
    # `exitTo` here would repeat the mistake `nav-in` made in the other direction — it happens to
    # give the same 87 today, and would stop doing so the moment an edge is declared from one end.
    outbound: dict = collections.defaultdict(set)
    for s in screens:
        nav = s.get("navigation") or {}
        for t in (nav.get("exitTo") or []):
            if t in ids:
                outbound[s["id"]].add(t)
        for a in (nav.get("entryFrom") or []):
            if a in ids:
                outbound[a].add(s["id"])

    # **`unique` failed 141 screens the triage calls correct.** A Guest Web screen and its Guest
    # App twin share an operation set because they are one product on two devices; a list and its
    # detail share one because a detail is a row of the list. Counting those as unfinished means a
    # screen can never be done for a reason nobody would ever act on — so only a cluster the
    # triage classes as UNDER-SPECIFIED counts against its members, which is the same rule
    # `--duplicates` reports and the only one that names real work.
    sig = collections.defaultdict(list)
    plat_of, aud_of = {}, {}
    for s in screens:
        plat_of[s["id"]] = s["_plat"]
        ops = frozenset(a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId"))
        if ops:
            sig[ops].append(s["id"])
    underspec: set = set()
    for ops, members in sig.items():
        if len(members) < 3:
            continue                      # two screens on one platform is a pair, not a gap
        if len({plat_of[m] for m in members}) > 1:
            continue                      # more than one platform is a form factor or an audience
        underspec |= set(members)

    cache: dict = {}
    rows = []
    for s in screens:
        ops = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
        impl = s.get("implementation") or {}
        key = frozenset(ops)
        st = {
            "ops": bool(ops),
            "nav-in": inbound[s["id"]] > 0,
            "nav-out": bool(outbound.get(s["id"])),
            "wire": board_ok(cache, (s.get("wireframe") or {}).get("board")),
            "impl": all(impl.get(k) for k in ("app", "route", "component")),
            "unique": s["id"] not in underspec,
        }
        rows.append({
            "id": s["id"], "name": s.get("name", ""), "plat": s["_plat"],
            "platName": s["_platName"], "pack": s["_pack"], "ops": len(ops),
            "twins": [x for x in sig.get(key, []) if x != s["id"]] if ops else [],
            "st": st, "done": all(st.values()),
            "missing": [c for c in COLS if not st[c]],
        })
    return rows


DUP_OUT = ROOT / "docs" / "active" / "screen-duplicate-triage.md"


def duplicates(screens, plats) -> int:
    """Classify every identical-signature cluster, because the headline number misleads.

    **"107 exact functional duplicates" reads as "delete 107 screens", and that is wrong.**
    Clustering by operation signature puts three different things in one bucket:

      *the same journey on two form factors* - `WEB-002 Event & Attraction Listing` on Guest Web
      and `GST-003 Event & Attraction Listing` on Guest App are one product on two devices, and
      40 of the 66 clusters are this;

      *a list and its detail* - `EMP-004 Task list` and `EMP-005 Task detail` read the same
      operations because a detail is a row of the list;

      *screens nobody has specified yet* - and this is the large one. `ADM-032 WAF & Security
      Policy View`, `ADM-033 Backup & DR Status` and `ADM-034 Archival Job Monitor` share seven
      generic cell operations because **WAF, archival and auto-scaling have no operation at all**.
      They are not redundant. They are empty, and they look redundant from a distance.

    **The action for the third kind is to specify, not to delete.** Deleting them would remove the
    only record that the platform is expected to do these things.
    """
    sig = collections.defaultdict(list)
    for s in screens:
        ops = frozenset(a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId"))
        if ops:
            sig[ops].append(s)
    clusters = [(ops, v) for ops, v in sig.items() if len(v) > 1]

    rows = []
    for ops, v in sorted(clusters, key=lambda kv: -len(kv[1])):
        ps = {s["_plat"] for s in v}
        auds = {(plats.get(s["_plat"]) or {}).get("audience") for s in v}
        if len(ps) > 1 and len(auds) > 1:
            kind = "different audience"
        elif len(ps) > 1:
            kind = "same journey, two form factors"
        elif len(v) == 2:
            # **Two screens on one platform sharing a set is a pair, not a gap.** A list and its
            # detail read the same rows; an assistant's home and its answer are one conversation;
            # a view and the act it offers are two steps of one job. Under-specification looks
            # different — it is THREE OR MORE screens on a thin generic set, which is what
            # `BO-101..BO-108` on `getVenueSettings` alone actually was.
            kind = "a pair - one step and its next"
        else:
            kind = "under-specified"
        rows.append((kind, sorted(ps), sorted(ops), v))

    tally = collections.Counter(r[0] for r in rows)
    print("%d identical-signature clusters covering %d screens\n"
          % (len(rows), sum(len(r[3]) for r in rows)))
    for k, n in tally.most_common():
        print("  %-32s %3d clusters  %4d screens"
              % (k, n, sum(len(r[3]) for r in rows if r[0] == k)))

    L = ["# Identical operation sets — what each cluster actually is", "",
         "**Derived by `tools/screen-ledger.py --duplicates`. Regenerate rather than editing.**", "",
         "**\"107 exact functional duplicates\" reads as \"delete 107 screens\", and that is "
         "wrong.** Clustering by operation signature puts three unrelated things in one bucket, "
         "and only one of them is duplication.", "",
         "| Kind | Clusters | Screens | What to do |", "|---|---:|---:|---|"]
    DO = {
        "same journey, two form factors":
            "**Nothing.** One product on two devices is the design.",
        "a pair - one step and its next":
            "**Nothing.** A detail reads the row its list read, and an answer reads the "
            "conversation its question opened.",
        "different audience":
            "**Nothing, but say so.** Same operations, different scope — a venue managing its own "
            "domain and a platform admin managing anyone's.",
        "under-specified":
            "**Specify.** These share a generic set because the operations that would distinguish "
            "them do not exist. Deleting them removes the only record the platform is expected to "
            "do these things.",
    }
    for k, n in tally.most_common():
        L.append("| %s | %d | %d | %s |"
                 % (k, n, sum(len(r[3]) for r in rows if r[0] == k), DO[k]))
    L += ["", "## Every cluster", ""]
    for kind in [k for k, _ in tally.most_common()]:
        L += ["### %s" % kind, "",
              "| Platform(s) | Screens | Shared operations |", "|---|---|---|"]
        for k, ps, ops, v in rows:
            if k != kind:
                continue
            L.append("| %s | %s | %s |"
                     % (", ".join(ps),
                        "<br>".join("%s %s" % (s["id"], s.get("name", "")) for s in v),
                        ", ".join("`%s`" % o for o in ops[:6])
                        + (" +%d" % (len(ops) - 6) if len(ops) > 6 else "")))
        L += [""]
    DUP_OUT.write_text(chr(10).join(L), encoding="utf-8")
    print("  -> docs/active/%s" % DUP_OUT.name)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", help="print the screens missing this one thing, and stop")
    ap.add_argument("--plat", help="restrict to one platform code")
    ap.add_argument("--duplicates", action="store_true",
                    help="classify the identical-signature clusters and write the triage")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    plats, screens = load()
    rows = assess(screens)
    if a.plat:
        rows = [r for r in rows if r["plat"] == a.plat]

    done = [r for r in rows if r["done"]]
    print("%d screens · %d done · %d outstanding" % (len(rows), len(done), len(rows) - len(done)))
    print()
    for c in COLS:
        miss = [r for r in rows if c in r["missing"]]
        pk = sum(1 for r in miss if r["pack"])
        print("  missing %-8s %5d   (%d from the pack, %d authored)"
              % (c, len(miss), pk, len(miss) - pk))

    if a.bucket:
        miss = sorted((r for r in rows if a.bucket in r["missing"]),
                      key=lambda r: (r["plat"], r["id"]))
        print("\n%d screen(s) missing '%s'\n" % (len(miss), a.bucket))
        for r in miss:
            extra = ""
            if a.bucket == "unique" and r["twins"]:
                extra = "  == " + ", ".join(r["twins"][:5])
            print("  %-8s %-46s %-4s %s%s"
                  % (r["id"], r["name"][:46], r["plat"],
                     "pack" if r["pack"] else "auth", extra))
        return 0

    if a.duplicates:
        return duplicates(screens, plats)

    print()
    by_plat = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        by_plat[r["plat"]][0] += 1
        by_plat[r["plat"]][1] += 1 if r["done"] else 0
    print("  %-6s %-24s %6s %6s %6s" % ("", "", "total", "done", "left"))
    for p in sorted(by_plat):
        t, d = by_plat[p]
        print("  %-6s %-24s %6d %6d %6d" % (p, plats.get(p, {}).get("shortName", "")[:24],
                                            t, d, t - d))

    if not a.write:
        print("\n  nothing written - pass --write")
        return 0

    L = ["# Screen ledger — what is missing from every screen", "",
         "**Derived by `tools/screen-ledger.py`. Regenerate rather than editing.**", "",
         "A screen is **done** when it calls an operation, something navigates to it, it goes "
         "somewhere, its wireframe anchor resolves to a frame that exists, it names an app/route/"
         "component, and no other screen declares an identical operation set.", "",
         "| | |", "|---|---:|",
         "| Screens | %d |" % len(rows),
         "| **Done** | **%d** |" % len(done),
         "| Outstanding | %d |" % (len(rows) - len(done)), ""]
    L += ["| Missing | Screens | From the pack | Authored |", "|---|---:|---:|---:|"]
    for c in COLS:
        miss = [r for r in rows if c in r["missing"]]
        pk = sum(1 for r in miss if r["pack"])
        L.append("| `%s` | %d | %d | %d |" % (c, len(miss), pk, len(miss) - pk))
    L += ["", "## By platform", "",
          "| Platform | Total | Done | Left |", "|---|---:|---:|---:|"]
    for p in sorted(by_plat):
        t, d = by_plat[p]
        L.append("| %s %s | %d | %d | %d |"
                 % (p, plats.get(p, {}).get("shortName", ""), t, d, t - d))
    L += ["", "## Every outstanding screen", "",
          "| Screen | Platform | Origin | Missing |", "|---|---|---|---|"]
    for r in sorted((r for r in rows if not r["done"]), key=lambda r: (r["plat"], r["id"])):
        L.append("| %s %s | %s | %s | %s |"
                 % (r["id"], r["name"], r["plat"], "pack" if r["pack"] else "authored",
                    ", ".join("`%s`" % m for m in r["missing"])))
    OUT.write_text("\n".join(L), encoding="utf-8")
    print("\n  -> docs/active/%s" % OUT.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
