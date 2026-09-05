#!/usr/bin/env python3
"""Audit the screen estate: duplicates, connectivity, and functionality that stops at one audience.

**Three questions, and the third is the one nothing answered.**

*Which screens are the same screen?* `check-screen-redundancy.py` already clusters by operation
signature and this tool does not repeat it — it reports the count and defers.

*Is every screen connected?* A screen nothing navigates to and that navigates nowhere is a screen
a reviewer reaches only by knowing its id.

*Is a capability stranded on one audience?* **This is the question the package could not answer.**
`x-ticvai-audience` declares who MAY call an operation; the screens show who actually DOES. The
gap between them is not a rounding error — it is a capability that exists, is permitted to a
guest, and has no guest surface. `check-screens.py` covers the guest case; this covers all three
audiences and adds the harder half: **an operation used by exactly one platform whose entity is
used by several**, which is how a venue-side function that a guest also needs stays invisible.

**A finding here is a question, not a defect.** An operation declared `staff` and used only by
staff is correct. An operation declared `staff, guest`, used only by staff, is either a missing
surface or a wrong declaration — and the tool cannot tell you which, because that is a product
decision. It tells you where to look.

Run: `python3 tools/audit-screen-estate.py [--write]`
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
OUT = ROOT / "docs" / "active" / "screen-estate-audit.md"

# Words that carry no entity — stripping them is what leaves the thing the screen acts on.
NOISE = {
    "command", "center", "centre", "dashboard", "monitor", "directory", "registry", "library",
    "explorer", "inbox", "management", "manager", "audit", "history", "log", "analytics",
    "overview", "builder", "designer", "workspace", "studio", "configuration", "config", "setup",
    "assignment", "simulation", "approval", "publication", "creation", "execution", "and", "the",
    "of", "for", "with", "amp", "screen", "operations", "operation", "control", "controls",
    "engine", "settings", "detail", "details", "list", "view", "page", "my", "new", "edit",
}


def singular(w: str) -> str:
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        return w[:-1]
    return w


def entity(text: str) -> set:
    return {singular(w) for w in re.findall(r"[A-Za-z]+", (text or "").lower())
            if w not in NOISE and len(w) > 3}


# **The screens and the contracts do not use one audience vocabulary, and conflating them was the
# first version of this tool reporting 158 gaps that were mostly nothing.** A platform declares
# `platformAdmin`; a contract declares `staff`. A platform admin IS staff. Mapped explicitly:
PLAT_SERVES = {
    "staff": {"staff"},
    "platformAdmin": {"staff"},
    "guest": {"guest", "anonymous", "public"},
    "public": {"public", "anonymous", "guest"},
    "partner": {"partner"},
}
# **No screen serves these and none should.** `device` is a scanner or a turnstile, `service` is
# machine-to-machine. Counting them as uncovered audiences is counting the absence of a UI for a
# turnstile as a design gap.
NON_HUMAN = {"device", "service"}

# Entities so common that sharing one says nothing. `order` is worked by every audience in the
# package; that two audiences both touch "order" is not evidence about any one operation.
GENERIC = {"order", "entry", "venue", "item", "detail", "record", "request", "status", "report",
           "note", "list", "code", "type", "group", "event", "session", "account", "profile",
           "setting", "policy", "rule", "user", "member", "product", "price", "payment"}


def load():
    plats, screens = {}, []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        plats[p["code"]] = p
        for s in doc["screens"]:
            s["_plat"] = p["code"]
            s["_aud"] = p.get("audience")
            s["_file"] = f.name
            screens.append(s)
    return plats, screens


def contract_audiences() -> dict:
    """Who each operation DECLARES it may serve. `x-ticvai-audience` on the operation."""
    aud: dict = {}
    for c in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        for _path, item in (doc.get("paths") or {}).items():
            for _verb, op in (item or {}).items():
                if isinstance(op, dict) and op.get("operationId"):
                    a = op.get("x-ticvai-audience")
                    if a:
                        aud[op["operationId"]] = set(a if isinstance(a, list) else [a])
    return aud


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    plats, screens = load()
    declared = contract_audiences()

    # ── who actually calls what ──────────────────────────────────────────────────────────────
    op_plats: dict = collections.defaultdict(set)
    op_auds: dict = collections.defaultdict(set)   # in the CONTRACT's vocabulary
    op_pauds: dict = collections.defaultdict(set)  # in the PLATFORM's vocabulary
    for s in screens:
        for x in (s.get("apis") or []):
            o = x.get("operationId")
            if o:
                op_plats[o].add(s["_plat"])
                op_pauds[o].add(s["_aud"])
                op_auds[o] |= PLAT_SERVES.get(s["_aud"], {s["_aud"]})

    # ── 1. audience declared but never served ────────────────────────────────────────────────
    stranded = []
    for o, decl in sorted(declared.items()):
        if o not in op_plats:
            continue
        missing = (decl - op_auds[o]) - NON_HUMAN
        if missing:
            stranded.append((o, sorted(decl), sorted(op_auds[o]), sorted(missing),
                             sorted(op_plats[o])))

    # ── 2. an entity several audiences touch, reachable from one ─────────────────────────────
    #
    # **The harder half, and the one the user asked for.** A capability is not stranded because
    # its declaration says so — most declarations are right. It is stranded when the SAME entity
    # is worked by more than one audience and one particular operation on it is reachable from
    # only one. That is a venue-side function a guest plausibly needs, and no annotation says so.
    # Entities are taken from OPERATION names, not screen titles — an operation is the unit of
    # capability, and a screen title is a label somebody chose.
    ent_auds: dict = collections.defaultdict(set)
    for o, au in op_pauds.items():
        for e in entity(re.sub(r"(?<!^)(?=[A-Z])", " ", o)) - GENERIC:
            ent_auds[e] |= au
    shared_ents = {e for e, au in ent_auds.items() if len(au) > 1}

    single = []
    for o, ps in sorted(op_plats.items()):
        if len(op_pauds[o]) != 1:
            continue
        # **Reads only.** A guest plausibly needs to SEE what staff can see; they rarely need to
        # perform the staff act. Reporting every write triples the list and none of it is
        # actionable — `acceptFnbOrder` being staff-only is not a finding, it is the design.
        if not re.match(r"^(list|get|search|view|export)", o):
            continue
        e = entity(re.sub(r"(?<!^)(?=[A-Z])", " ", o)) - GENERIC
        hit = sorted(e & shared_ents)
        if hit:
            others = sorted(set().union(*[ent_auds[x] for x in hit]) - op_pauds[o])
            if others:
                single.append((o, sorted(op_pauds[o])[0], hit, others, sorted(ps)))

    # ── 3. connectivity ──────────────────────────────────────────────────────────────────────
    inbound: dict = collections.Counter()
    for s in screens:
        for t in ((s.get("navigation") or {}).get("exitTo") or []):
            inbound[t] += 1
    orphans = [s for s in screens
               if inbound[s["id"]] == 0 and not ((s.get("navigation") or {}).get("exitTo"))]
    no_in = [s for s in screens if inbound[s["id"]] == 0]
    # **Split, because the two are different problems.** A pack screen has no navigation because
    # nobody has written it yet; an authored screen with none is a screen that fell out of the
    # graph. Reporting one number hides the second inside the first.
    no_in_pack = [s for s in no_in if (s.get("source") or {}).get("pack")]
    no_in_auth = [s for s in no_in if not (s.get("source") or {}).get("pack")]

    # ── report ───────────────────────────────────────────────────────────────────────────────
    print("%d screens · %d platforms · %d operations called by a screen"
          % (len(screens), len(plats), len(op_plats)))
    print()
    print("  audience declared and never served      %4d operations" % len(stranded))
    print("  single-audience op on a shared entity   %4d operations" % len(single))
    print("  screens nothing navigates to            %4d" % len(no_in))
    print("    authored (fell out of the graph)      %4d" % len(no_in_auth))
    print("    from the pack (never wired yet)       %4d" % len(no_in_pack))
    print("    of all those, also exiting nowhere    %4d" % len(orphans))
    print()
    top = collections.Counter(m for _o, _d, _h, ms, _p in stranded for m in ms)
    for k, v in top.most_common():
        print("  never served, by audience: %-8s %4d" % (k, v))
    print()
    for row in stranded[:8]:
        print("  %-34s declared %-24s served %-12s" % (row[0], ",".join(row[1]), ",".join(row[2])))
    print()
    for row in single[:8]:
        print("  %-34s only %-8s entity %-26s also worked by %s"
              % (row[0], row[1], ",".join(row[2])[:26], ",".join(row[3])))

    if not a.write:
        print("\n  nothing written - pass --write")
        return 0

    L = ["# Screen estate audit — duplication, connectivity, and stranded capability", "",
         "**Derived by `tools/audit-screen-estate.py`. Regenerate rather than editing.**", "",
         "| | |", "|---|---:|",
         "| Screens | %d |" % len(screens),
         "| Platforms | %d |" % len(plats),
         "| Operations called by at least one screen | %d |" % len(op_plats),
         "| **Audience declared and never served** | **%d** |" % len(stranded),
         "| **Single-audience operation on a shared entity** | **%d** |" % len(single),
         "| Screens nothing navigates to — authored | **%d** |" % len(no_in_auth),
         "| Screens nothing navigates to — from the pack | %d |" % len(no_in_pack),
         "| …of all those, also exiting nowhere | %d |" % len(orphans), "",
         "## What a finding here is",
         "",
         "**A question, not a defect.** An operation declared `staff` and used only by staff is "
         "correct. An operation declared `staff, guest` and used only by staff is either a missing "
         "surface or a wrong declaration, and this tool cannot tell you which — that is a product "
         "decision. It tells you where to look.",
         "",
         "Duplication is not recomputed here. `tools/check-screen-redundancy.py` clusters by "
         "operation signature and remains the authority on it.",
         "",
         "## 1. Declared for an audience no screen serves",
         "",
         "`x-ticvai-audience` says who **may** call an operation. The screens say who **does**.",
         "",
         "| Operation | Declared | Actually served | Never served | Platforms |",
         "|---|---|---|---|---|"]
    for o, d, srv, ms, ps in stranded:
        L.append("| `%s` | %s | %s | **%s** | %s |"
                 % (o, ", ".join(d), ", ".join(srv) or "—", ", ".join(ms), ", ".join(ps)))
    L += ["",
          "## 2. One audience, on an entity several audiences work",
          "",
          "**The harder half.** These operations are not mis-declared — they are reachable from "
          "one audience while the *same entity* is worked by others. A venue-side function a "
          "guest plausibly needs looks exactly like this, and no annotation marks it.",
          "",
          "| Operation | Reachable from | Entity | Also worked by | Platforms |",
          "|---|---|---|---|---|"]
    for o, au, hit, others, ps in single:
        L.append("| `%s` | %s | %s | **%s** | %s |"
                 % (o, au, ", ".join(hit), ", ".join(others), ", ".join(ps)))
    L += ["",
          "## 3. Connectivity",
          "",
          "A screen nothing navigates to is reachable only by knowing its id. One that also exits "
          "nowhere is not in the graph at all.",
          "",
          "| Screen | Platform | Nothing navigates to it | Exits nowhere |",
          "|---|---|---|---|"]
    for s in sorted(no_in, key=lambda x: (x["_plat"], x["id"]))[:400]:
        L.append("| %s %s | %s | yes | %s |"
                 % (s["id"], s.get("name", ""), s["_plat"],
                    "yes" if s in orphans else "no"))
    OUT.write_text("\n".join(L), encoding="utf-8")
    print("\n  -> docs/active/%s" % OUT.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
