#!/usr/bin/env python3
"""Link the workshop screens to the operations that exist, and name the ones that do not.

**Wires what can be evidenced and specifies the rest.** Writes the matches into `screens/P*.yaml`
and the gap into `docs/active/workshop-contract-gap.md` as named operations.

## What signal works, and the two that do not

A screen's operations are decided by **what entity it acts on and what it does to it** — and both
are recoverable from the title, because this pack titles every screen after its entity and its
archetype. `Access Point Directory` is a list of access points; `Offline Validation Policy Builder`
sets an offline policy. Matched against operation NAMES, that is precise:

    Access Point Directory                 -> listAccessPoints
    Face Pass Enrollment Configuration     -> enrolFacePass
    Offline Validation Policy Builder      -> setOfflinePolicy
    Queue Configuration & Management       -> listQueues
    Sender Identity, Domain & Brand Config -> setBrandIdentity

**Two weaker signals were tried first and both fail the same way** — the terms they agree on are
the generic ones:

*Bag-of-words over operation summaries, paths and tables.* Eight unrelated screens matched
`listScans` at 0.75, `Group & B2B Admission Profile Builder` among them. An operation with a small
vocabulary wins any containment measure.

*The field lists, joined through the schema.* Only 9% of the pack's 4,756 field terms resolve to a
real column, and the ones that do are `status`, `owner`, `channel` and `venue_id` — so
`Pricing Rule Command Center` came back pointing at `pii.subject`.

## The gap is the more valuable half

552 of 590 screens name an entity no operation serves. **That is not a matching failure, it is the
contract scope, and the same derivation names it**: an archetype implies a verb, so a screen with
no match yields the operationId that should exist. `listPricingRules` is a specification somebody
can write; "196 distinct terms" is not.

Run: `python3 tools/derive-pack-linkage.py [--apply]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "sources" / "workshop" / "pack.json"
SCREENS = ROOT / "screens"
GAP = ROOT / "docs" / "active" / "workshop-contract-gap.md"

# Verbs an operationId may lead with. Anything else is treated as part of the entity.
VERBS = ("list", "get", "create", "update", "set", "delete", "remove", "add", "approve",
         "reject", "publish", "activate", "deactivate", "cancel", "void", "assign", "validate",
         "simulate", "export", "import", "record", "submit", "configure", "search", "resolve",
         "revoke", "issue", "enrol", "enroll", "override", "register", "release", "reconcile")

# **The archetype word says what the screen does, and it is also not part of the entity.** A
# "Command Center" is a list; a "Builder" writes. Stripping them is what leaves the entity behind.
ARCHETYPE_VERB = {
    "command": "list", "center": "list", "centre": "list", "dashboard": "list",
    "monitor": "list", "directory": "list", "register": "list", "registry": "list",
    "library": "list", "explorer": "list", "inbox": "list", "management": "list",
    "audit": "list", "history": "list", "log": "list", "analytics": "list",
    "intelligence": "list", "optimization": "list", "forecasting": "list", "overview": "list",
    "builder": "set", "designer": "set", "workspace": "set", "studio": "set",
    "configuration": "set", "config": "set", "setup": "set", "assignment": "set",
    "simulation": "simulate", "approval": "approve", "publication": "publish",
    "creation": "create", "execution": "create",
}
NOISE = set(ARCHETYPE_VERB) | {"and", "the", "of", "for", "with", "ai", "amp", "screen",
                               "operations", "operation", "control", "controls", "engine"}

WIRE_AT = 0.60          # wire the match into the screen
CANDIDATE_AT = 0.45     # report it, do not wire it


def singular(word: str) -> str:
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word


def op_tokens(oid: str) -> tuple:
    parts = [p.lower() for p in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", oid)]
    verb = parts[0] if parts and parts[0] in VERBS else None
    rest = parts[1:] if verb else parts
    return verb, {singular(p) for p in rest if len(p) > 2}


def screen_tokens(title: str) -> tuple:
    """Archetype verbs, the entity as a set, and the entity in the order the title says it.

    **Order matters for the proposed name and not for the match.** Sorting the tokens
    alphabetically turned `Venue & Park Access Structure` into `listAccessParkStructure`, which
    reads like something nobody would call an endpoint. The set is what scores; the sequence is
    what gets written down.
    """
    words = [w.lower() for w in re.findall(r"[A-Za-z]+", title)]
    verbs = {ARCHETYPE_VERB[w] for w in words if w in ARCHETYPE_VERB} or {"list"}
    seq, seen = [], set()
    for w in words:
        t = singular(w)
        if w not in NOISE and len(w) > 2 and t not in seen:
            seen.add(t)
            seq.append(t)
    return verbs, set(seq), seq


def pascal(words) -> str:
    return "".join(w.capitalize() for w in words)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    ops = {o: op_tokens(o) for o in lin}

    wired, candidates, gaps = {}, {}, defaultdict(list)
    stats = Counter()
    for rec in pack:
        verbs, entity, seq = screen_tokens(rec["title"])
        scored = []
        for oid, (ov, oent) in ops.items():
            if not entity or not oent:
                continue
            share = len(entity & oent) / len(entity | oent)
            # **The operation's own verb has to be one the archetype implies.** Allowing an
            # unrecognised leading word to match any archetype put `transitionProductLifecycle`
            # on `Product Lifecycle Command Center` at 0.67 — a write wired onto a screen whose
            # whole shape is a list. A verb this tool does not know is a verb it cannot place.
            if share >= CANDIDATE_AT and ov in verbs:
                scored.append((round(share, 2), oid))
        scored.sort(reverse=True)
        key = (rec["source"], rec["number"], rec["title"])
        if scored and scored[0][0] >= WIRE_AT:
            wired[key] = [o for s, o in scored if s >= WIRE_AT][:4]
            stats["wired"] += 1
        elif scored:
            candidates[key] = scored[:3]
            stats["candidate"] += 1
        else:
            stats["gap"] += 1
        if not scored or scored[0][0] < WIRE_AT:
            # **The verb comes from the archetype and the entity from the title**, so an unmatched
            # screen still yields the operation that ought to exist.
            ent = seq[:3]
            for v in sorted(verbs):
                gaps[(rec["module"], rec["board"])].append(
                    (rec["title"], v + pascal(ent), sorted(entity)))

    print(f"{len(pack)} pack screens\n")
    print(f"  wired to an existing operation   {stats['wired']:>4}")
    print(f"  candidate below the threshold    {stats['candidate']:>4}")
    print(f"  no operation exists              {stats['gap']:>4}")
    proposed = sorted({g[1] for v in gaps.values() for g in v})
    print(f"\n  distinct operations to author    {len(proposed):>4}")

    if not a.apply:
        print("\n  nothing written — pass --apply")
        return 0

    # ---- wire the confident matches ---------------------------------------------------------
    n = 0
    for f in sorted(SCREENS.glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        touched = False
        for s in d["screens"]:
            src = s.get("source") or {}
            if not src.get("pack"):
                continue
            key = (src["pack"], src["number"], s["name"])
            if key in wired:
                s["apis"] = [{"operationId": o, "contract": lin[o]["contract"],
                              "purpose": (lin[o].get("summary") or o)[:90],
                              "trigger": "onLoad" if o.startswith(("list", "get")) else "onAction"}
                             for o in wired[key]]
                # **A wired operation may take a path parameter, and the screen has to say where
                # it comes from.** `check-screens` refuses a screen that calls an operation
                # needing `productId` and declares no entry state — it cannot know what it is
                # showing, which is a real defect and not a formality.
                needed = sorted({q for o in wired[key]
                                 for q in re.findall(r"\{([a-zA-Z]+)\}", lin[o].get("path", ""))})
                if needed:
                    s["entryState"] = {
                        "params": [{"name": q, "from": "navigation"} for q in needed],
                        "coldEntry": "**Reached from the list that owns it**, so the identifier "
                                     "arrives with the navigation. Opened cold without one, the "
                                     "screen says what is missing and offers that list — never an "
                                     "empty form that looks configurable.",
                    }
                touched = True
                n += 1
        if touched:
            f.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                         encoding="utf-8")
            print(f"  -> {f.relative_to(ROOT)}")
    print(f"  {n} screen(s) wired")

    # ---- the register ------------------------------------------------------------------------
    lines = [
        "# Workshop pack — the contract gap, as named operations",
        "",
        "**Derived by `tools/derive-pack-linkage.py`. Regenerate rather than editing.**",
        "",
        f"| | |", "|---|---:|",
        f"| Pack screens | {len(pack)} |",
        f"| Wired to an operation that exists | **{stats['wired']}** |",
        f"| Candidate match below the threshold | {stats['candidate']} |",
        f"| No operation exists | **{stats['gap']}** |",
        f"| Distinct operations to author | **{len(proposed)}** |",
        "",
        "## How these were derived",
        "",
        "A screen's operations follow from **what entity it acts on and what it does to it**, and "
        "this pack titles every screen after both — `Access Point Directory` is a list of access "
        "points, `Offline Validation Policy Builder` sets an offline policy. Matched against "
        "operation names that is precise: `listAccessPoints`, `setOfflinePolicy`, `enrolFacePass`, "
        "`listQueues`, `setBrandIdentity` all came out of it.",
        "",
        "**Two weaker signals were tried first and both failed the same way** — the terms they "
        "agree on are the generic ones. Bag-of-words over summaries and tables put eight "
        "unrelated screens on `listScans` at 0.75. Joining the field lists through the schema "
        "resolved only 9% of 4,756 field terms, and the ones that resolved were `status`, `owner` "
        "and `channel`, so `Pricing Rule Command Center` came back pointing at `pii.subject`.",
        "",
        "**A proposed name is a specification, not a decision.** The verb comes from the "
        "archetype and the entity from the title; the shape of the request and response does not "
        "follow from either, and neither does the permission, the scope level or the audience. "
        "Those are the parts a person writes.",
        "",
    ]
    for (module, board), rows in sorted(gaps.items()):
        names = sorted({p for _, p, _ in rows})
        lines += [f"## {module} — board {board}", "",
                  f"{len(rows)} screens · {len(names)} operations to author", "",
                  "| Screen | Operation to author |", "|---|---|"]
        lines += [f"| {t} | `{p}` |" for t, p, _ in rows]
        lines += [""]
    GAP.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> {GAP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
