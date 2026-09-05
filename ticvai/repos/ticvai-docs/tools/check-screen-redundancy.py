#!/usr/bin/env python3
"""Cluster every screen by what it does, and say which ones do the same thing.

**`audit/SCREEN-REDUNDANCY.md` was written by hand on 1 September** and found 105 exact functional
duplicates among 492 screens. It opens with that 492 against today's 500 — **it went stale eight
screens later and there was no way to refresh it short of redoing the whole thing.** This is that
audit as a tool.

## Two signatures, because the new screens do not have operations yet

**Operation signature** — the set of `operationId`s a screen declares. Two screens with the same
set read the same data and offer the same actions, so they are the same screen whatever they are
called. **This is the authority** and it is what the hand audit used.

**Vocabulary signature** — the nouns a screen names: its title, purpose, module, the components it
binds and the fields it lists. Weaker, and it is the only thing the 590 screens in
`sources/workshop/pack.json` have, because a screen parsed from a PDF has no operations until
somebody assigns them. **Assigning them is the expensive half of the work**, which is precisely why
the comparison has to happen first.

Where both exist the operation signature decides. The vocabulary signature is what lets a screen
that has not been built be held against one that has.

## What it answers

    exact duplicates          identical operation signature
    near duplicates           >= 80% Jaccard, three or more operations
    cross-platform capability a capability on P04 and not on P07, which is a finding
    pack triage               each of the 590 new screens against the 500 existing

Run: `python3 tools/check-screen-redundancy.py [--pack] [--json]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
PACK = ROOT / "sources" / "workshop" / "pack.json"
OUT = ROOT / "handoff" / "screen-redundancy.json"

NEAR = 0.80
MIN_OPS = 3

# **Words that carry no signal about what a screen does.** Left in, every screen matches every
# other on `management`, `configuration` and `screen` — the pack's own title vocabulary. 57 of its
# 59 boards open with a "Command Center".
STOP = {
    "the", "and", "for", "with", "from", "that", "this", "its", "all", "any", "per", "via",
    "screen", "screens", "page", "view", "views", "tab", "tabs", "management", "manage",
    "configuration", "configure", "configured", "settings", "setting", "system", "module",
    "display", "displays", "show", "shows", "list", "lists", "detail", "details", "data",
    "information", "support", "supports", "each", "every", "new", "add", "edit", "delete",
    "create", "update", "user", "users", "admin", "team", "teams", "one", "two", "can",
    "must", "should", "when", "where", "which", "what", "who", "how", "not", "are", "was",
    "has", "have", "will", "may", "into", "out", "over", "under", "between", "across",
}


def terms_of(*texts) -> set:
    """Content words, lowercased and stemmed of the commonest plural."""
    out = set()
    for t in texts:
        for w in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", str(t or "")):
            w = w.lower().strip("'-")
            if len(w) < 3 or w in STOP:
                continue
            if w.endswith("ies") and len(w) > 5:
                w = w[:-3] + "y"
            elif w.endswith("s") and not w.endswith("ss") and len(w) > 3:
                w = w[:-1]
            if w not in STOP:
                out.add(w)
    return out


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def tfidf_match(pack: list, pkg: list):
    """Best existing screen for each pack screen, by TF-IDF cosine over the joint corpus.

    **Two simpler measures were tried and both failed, in opposite directions.**

    *Jaccard* drowned in the size difference — a built screen names a median of 28 terms and a pack
    screen 56, so the union dominated and every one of the 590 scored under 0.1 and came back
    "new". *Overlap coefficient* then over-corrected: dividing by the smaller set rewards a built
    screen with a tiny generic vocabulary, and it matched `Rule Priority, Conflict Resolution &
    Dynamic Sequencing` to `Select Date & Time` at 0.64.

    **The failure both share is treating every word as equally informative.** This pack opens 57 of
    its 59 boards with a Command Center; `management`, `configuration` and `rule` appear
    everywhere and carry almost no signal, while `passback`, `chargeback` and `guardian` carry a
    great deal. Inverse document frequency is the measure that knows the difference, and cosine
    normalises the lengths that sank Jaccard.

    **This is still a shortlist for a person.** A screen that has not been built has no operations,
    and operations are what actually decide whether two screens are the same.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    docs = [" ".join(sorted(r["terms"])) for r in pkg + pack]
    X = TfidfVectorizer(min_df=1, sublinear_tf=True).fit_transform(docs)
    n = len(pkg)
    sim = cosine_similarity(X[n:], X[:n])
    out = []
    for i, row in enumerate(sim):
        j = int(row.argmax())
        out.append((pack[i], pkg[j], float(row[j])))
    return out


def load_existing() -> list[dict]:
    rows = []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        for s in doc["screens"]:
            ops = {a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")}
            # Everything the definition says about what is on the screen. `bindsTo` names the
            # schema a region renders and `notes` says what the person is looking at.
            bits = [s.get("name"), s.get("purpose"), s.get("module")]
            for region in ((s.get("layout") or {}).get("regions") or []):
                for c in (region.get("components") or []):
                    bits += [c.get("bindsTo"), c.get("notes"), c.get("kind")]
            bits += [a.get("purpose") for a in (s.get("apis") or [])]
            rows.append({
                "id": s["id"], "name": s.get("name", ""), "platform": p["code"],
                "platformName": p.get("shortName", ""), "module": s.get("module", ""),
                "ops": ops, "terms": terms_of(*bits), "source": "package",
            })
    return rows


def load_pack() -> list[dict]:
    if not PACK.exists():
        return []
    rows = []
    for r in json.loads(PACK.read_text(encoding="utf-8")):
        rows.append({
            "id": f"{r['module'][:3].upper()}-{r['number']}", "name": r["title"],
            "platform": "PACK", "platformName": r["module"], "module": r["module"],
            "board": r.get("board"), "ops": set(),
            "terms": terms_of(r["title"], r.get("purpose"), *(r.get("terms") or [])),
            "source": "pack",
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", action="store_true",
                    help="also triage sources/workshop/pack.json against the built screens")
    ap.add_argument("--json", action="store_true", help="write handoff/screen-redundancy.json")
    a = ap.parse_args()

    pkg = load_existing()
    by_id = {r["id"]: r for r in pkg}
    WARN: list[str] = []

    # ---- exact operation signatures --------------------------------------------------------
    sig = defaultdict(list)
    for r in pkg:
        if r["ops"]:
            sig[frozenset(r["ops"])].append(r["id"])
    clusters = {k: v for k, v in sig.items() if len(v) > 1}
    in_cluster = {i for v in clusters.values() for i in v}
    duplicates = sum(len(v) - 1 for v in clusters.values())
    no_ops = [r["id"] for r in pkg if not r["ops"]]

    print(f"{len(pkg)} screens · {len(pkg) - len(no_ops)} declaring operations · "
          f"{len(sig)} distinct operation signatures\n")
    print(f"  exact functional duplicates      {duplicates}")
    print(f"  screens inside a cluster         {len(in_cluster)} "
          f"({100 * len(in_cluster) // max(len(pkg), 1)}%)")
    print(f"  identical-signature clusters     {len(clusters)}")
    print(f"  screens declaring no operations  {len(no_ops)}")

    # ---- near duplicates --------------------------------------------------------------------
    cand = [r for r in pkg if len(r["ops"]) >= MIN_OPS]
    near = []
    for x, y in combinations(cand, 2):
        if frozenset(x["ops"]) == frozenset(y["ops"]):
            continue
        j = jaccard(x["ops"], y["ops"])
        if j >= NEAR:
            near.append((x["id"], y["id"], round(j, 3)))
    print(f"  near-identical pairs (>={int(NEAR * 100)}%)     {len(near)} "
          f"({len({i for p in near for i in p[:2]})} screens)")

    # ---- per platform -----------------------------------------------------------------------
    per = defaultdict(lambda: [0, 0])
    for r in pkg:
        per[r["platform"]][0] += 1
        if r["id"] in in_cluster:
            per[r["platform"]][1] += 1
    print("\n  platform            screens  in a cluster   share")
    for code in sorted(per, key=lambda c: -per[c][1] / max(per[c][0], 1)):
        n, c = per[code]
        name = next(r["platformName"] for r in pkg if r["platform"] == code)
        print(f"  {code} {name[:18]:20}{n:>5}{c:>13}{100 * c // max(n, 1):>7}%")

    # ---- cross-platform capability ----------------------------------------------------------
    # **An operation reachable on one platform and not another is a finding, not a gap in this
    # report.** A guest can do it on the web and not in the app is a product decision somebody
    # should have made on purpose.
    op_plat = defaultdict(set)
    for r in pkg:
        for o in r["ops"]:
            op_plat[o].add(r["platform"])
    single = {o: p for o, p in op_plat.items() if len(p) == 1}
    print(f"\n  operations reachable from exactly one platform   {len(single)} of {len(op_plat)}")

    report = {
        "screens": len(pkg), "signatures": len(sig), "duplicates": duplicates,
        "clusters": {",".join(sorted(v)): sorted(v) for v in clusters.values()},
        "nearPairs": near, "noOperations": no_ops,
        "singlePlatformOperations": {o: sorted(p) for o, p in sorted(single.items())},
    }

    # ---- pack triage ------------------------------------------------------------------------
    if a.pack:
        pack = load_pack()
        if not pack:
            print("\n  no sources/workshop/pack.json — run tools/parse-workshop-pack.py --apply")
        else:
            print(f"\n{'=' * 62}\n  workshop pack: {len(pack)} screens against {len(pkg)} built\n")
            triage = []
            for r, best, score in tfidf_match(pack, pkg):
                # **Calibrated, not absolute.** TF-IDF cosine over bags of 30-60 terms in a
                # 1,090-document corpus runs low by construction: the median here is 0.11 and the
                # maximum 0.24. The bands are cut from that distribution, so **the count they
                # produce is the size of a review queue and not a count of duplicates.**
                verdict = ("check first — close match" if score >= 0.18 else
                           "check against the named screen" if score >= 0.15 else "no near match")
                triage.append({"packId": r["id"], "title": r["name"], "module": r["module"],
                               "board": r.get("board"), "match": best["id"] if best else None,
                               "matchName": best["name"] if best else None,
                               "score": round(score, 3), "verdict": verdict})
            counts = Counter(t["verdict"] for t in triage)
            for v in ("check first — close match", "check against the named screen",
                      "no near match"):
                print(f"  {v:32} {counts.get(v, 0):>4}")

            # Archetype collapse inside the pack itself.
            arch = defaultdict(list)
            for r in pack:
                key = re.sub(r"[^a-z ]", "", r["name"].lower()).split()
                arch[key[-2] + " " + key[-1] if len(key) > 1 else r["name"].lower()].append(r["id"])
            repeated = {k: v for k, v in arch.items() if len(v) > 2}
            print(f"\n  repeated archetypes inside the pack   {len(repeated)} "
                  f"covering {sum(len(v) for v in repeated.values())} screens")
            for k, v in sorted(repeated.items(), key=lambda x: -len(x[1]))[:8]:
                print(f"     {len(v):>3}  {k}")
            report["packTriage"] = triage

    if a.json:
        OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"\n  -> {OUT.relative_to(ROOT)}")

    for c in sorted(clusters.values(), key=len, reverse=True)[:20]:
        names = ", ".join(f"{i} {by_id[i]['name'][:28]}" for i in sorted(c)[:4])
        WARN.append(f"{len(c)} screens share one operation set: {names}"
                    + (" …" if len(c) > 4 else ""))
    print()
    for w in WARN:
        print(f"  WARN  {w}")
    print(f"\nPASS — {len(WARN)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
