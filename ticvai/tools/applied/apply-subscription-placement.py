#!/usr/bin/env python3
"""Place the Subscription book by who works each screen, not by which book it came from.

**Decided 11 September 2026**, after reading all 100 screens. `Latest Docs.zip` put the whole of
*Subscription Licensing & AI Self-Service* on P09, because `subscription.yaml` runs on the control
plane. The book is written for three different people, and P09 is right for only one of them.

| board | who works it | where |
|---|---|---|
| 1, 3, 6.1–6.9, 9, 10 | TICVAI management, administrators, finance | **P09**, unchanged |
| 7 AI Setup, 8 Go-Live, 6.10 Environment Ready | **the new customer's own admin**, inside their tenant | **moved to P08** |
| 2, 4.1–4.7, 5.1–5.4, 5.6, 5.7, 5.9 | **a prospect**, before any tenant exists | **copied to P17 Sign-up**; P09 keeps them |

## Boards 7 and 8 move

Board 7 is the customer configuring their venue — *"AI configuration and manual configuration must
modify the same underlying configuration objects"*, and those objects are P08's. Board 8 is the
customer testing it and signing the go-live declaration; *"a small Essential customer should be
able to complete this entire process without mandatory TICVAI assistance."* 6.10 *Your TICVAI
Environment Is Ready* speaks to that customer and *"hands the customer directly to Board 7"*.

**A move, not a copy**: the P08 screen takes the pack claim, and the `ADM-` id is retired and never
reissued. Everything the generator built is carried; the id, route, component, board anchor and
navigation are P08's. The two derived flows for boards 7 and 8 keep their `F` ids and are rewritten
onto the new screens; board 6's loses the step that has left the platform.

## The prospect gets P17, and P09 keeps its screens

A prospect has no tenant and no cell, so nothing served from a cell can reach them — P08 is out.
ADR-0043 already puts the onboarding application in the regional control database. So the door
is a public face of **TICVAI Control**, the same shape as P11's accreditation intake.

**P09 keeps boards 2, 4 and 5 whole**, because BL-165 decided there are two paths in: operator-led,
where TICVAI sales run the assessment and build the package, and self-service. The book agrees —
*"TICVAI commercial users — or authorized self-service customers where applicable"*, and *"Request
Enterprise Consultation"*. P17 carries `source.sameAs` for the screens a prospect sees and not for
4.8 (it shows **TICVAI's** revenue), 4.9–4.10 (internal review and approval), 5.5 (trial rules),
5.8 (final commercial validation) or 5.10 (lifecycle and escalation). As with Rental on P06,
re-running re-copies the twin's generated fields so the two do not drift.

The journey is the book's own, from 2.1: *tell us about your venue → define your operation → get your
recommended solution → review pricing → start trial / purchase*.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import copy
import glob
import os
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"
FLOWS = ROOT / "flows"
PACK = "Subscription_Licensing_AI_Self_Service.pdf"
MODULE_NAME = "Subscription Licensing AI Self Service"

MOVE = [("6", "10")] + [("7", str(n)) for n in range(1, 11)] + [("8", str(n)) for n in range(1, 11)]
P08_SECTION = "Setup & Go-Live"

SIGNUP = ([("2", str(n)) for n in range(1, 11)] + [("4", str(n)) for n in range(1, 8)]
          + [("5", n) for n in ("1", "2", "3", "4", "6", "7", "9")])
SIGNUP_SECTION = {"2": "Onboarding & Assessment", "4": "Package Builder", "5": "Purchase & Activation"}
COPIED = ("purpose", "pattern", "patternReason", "layout", "states", "gaps", "overlays",
          "apis", "apisNote", "entryState")
CONTROL = ["P09", "P10", "P11", "P14", "P17"]
CONTROL_NOTE = (
    "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, "
    "the developer portal and the sign-up are outward faces of the control plane, not separate "
    "products — but their users are not TICVAI staff, and the permission model has to hold that "
    "line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so "
    "the control plane is the only thing that can serve them.")
DATE = "11 September 2026"
# The twin's `emptyNoAccess` is staff wording — *names the missing permission* — and a prospect is
# signed out and holds none. Not replaced with a guess at what a public page does instead.
P17_NO_ACCESS = (
    "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording "
    "on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, "
    "which is where somebody without access to a saved setup would be sent; no minute has decided it.")


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def pascal(text: str) -> str:
    return "".join(w.capitalize() for w in re.findall(r"[A-Za-z0-9]+", text))[:48] or "Screen"


def key(s: dict) -> tuple:
    src = s.get("source") or {}
    return str(src.get("board")), str(src.get("number"))


def link(a: dict, b: dict, trigger: str, provenance: str, back: bool = False) -> None:
    na, nb = a.setdefault("navigation", {}), b.setdefault("navigation", {})
    for seq, v in ((na.setdefault("exitTo", []), b["id"]), (nb.setdefault("entryFrom", []), a["id"])):
        if v not in seq:
            seq.append(v)
            seq.sort()
    tr = na.setdefault("transitions", [])
    if not any(str(t.get("to", "")).partition("#")[0] == b["id"] for t in tr):
        entry = {"to": b["id"], "trigger": trigger, "provenance": provenance}
        if back:
            entry["back"] = True
        tr.append(entry)


def both(a: dict, b: dict, provenance: str) -> None:
    """Forward labelled with where it goes, back labelled as back — the wiring tools' convention."""
    link(a, b, b["name"], provenance)
    link(b, a, f"Back to {a['name']}", provenance, back=True)


def strip(s: dict, gone: set) -> int:
    nav, n = s.get("navigation") or {}, 0
    for k in ("entryFrom", "exitTo"):
        if k in nav:
            kept = [v for v in nav[k] if v not in gone]
            n += len(nav[k]) - len(kept)
            nav[k] = kept
    if "transitions" in nav:
        kept = [t for t in nav["transitions"] if str(t.get("to", "")).partition("#")[0] not in gone]
        n += len(nav["transitions"]) - len(kept)
        nav["transitions"] = kept
    return n


def dump(path: pathlib.Path, doc: dict) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    os.replace(tmp, path)


def main() -> int:
    apply = "--apply" in sys.argv
    files = {pathlib.Path(f).name[:3]: pathlib.Path(f) for f in glob.glob(str(SCREENS / "P*.yaml"))}
    docs = {code: yaml.safe_load(p.read_text(encoding="utf-8")) for code, p in files.items()}
    # Only a file whose content changed is written: re-serialising a file this did not touch
    # produces a diff of thousands of lines that means nothing and hides the lines that do.
    before_docs = {code: yaml.safe_dump(d, sort_keys=True) for code, d in docs.items()}
    p08, p09 = docs["P08"], docs["P09"]
    register = yaml.safe_load((SCREENS / "_id-register.yaml").read_text(encoding="utf-8"))

    def next_id(prefix: str, doc: dict | None) -> str:
        reg = int(((register["prefixes"].get(prefix) or {}).get("nextFree")) or 1)
        seen = [int(s["id"].split("-")[1]) for s in (doc or {}).get("screens", []) if s["id"].startswith(prefix + "-")]
        n = max([reg] + [x + 1 for x in seen])
        register["prefixes"].setdefault(prefix, {})["nextFree"] = n + 1
        return "%s-%03d" % (prefix, n)

    def ours(doc: dict) -> dict:
        return {key(s): s for s in doc["screens"] if (s.get("source") or {}).get("pack") == PACK}

    # ---- 1. boards 7 and 8, and 6.10, move to P08 ------------------------------------------------
    on09, on08 = ours(p09), ours(p08)
    moved: dict[str, str] = {}
    for k in MOVE:
        if k in on08:
            continue
        old = on09[k]
        sid = next_id("BO", p08)
        new = copy.deepcopy(old)
        new["id"] = sid
        new["module"] = P08_SECTION
        new["implementation"] = {
            "app": p08["platform"]["app"],
            "route": f"/{slug(P08_SECTION)}/{slug(old['name'])[:56]}-{sid.lower()}",
            "component": f"apps/{p08['platform']['app']}/src/routes/{slug(P08_SECTION)}/{pascal(old['name'])}.tsx",
            "status": (old.get("implementation") or {}).get("status", "notStarted")}
        new["wireframe"] = {"status": (old.get("wireframe") or {}).get("status", "notStarted"),
                            "board": f"{p08['platform']['wireframeBoard']}#{sid.lower()}"}
        new["navigation"] = {}
        new["notes"] = ((old.get("notes") + "\n\n") if old.get("notes") else "") + (
            f"**Moved from P09 `{old['id']}` on {DATE}.** Board {k[0]} is worked by the new customer's "
            "own administrator inside their tenant, not by TICVAI; "
            "`tools/applied/apply-subscription-placement.py` records why. "
            f"`{old['id']}` is retired and never reissued.")
        p08["screens"].append(new)
        p09["screens"].remove(old)
        on08[k] = new
        moved[old["id"]] = sid

    gone = set(moved)
    stripped = sum(strip(s, gone) for d in docs.values() for s in d["screens"])

    home08 = next(s for s in p08["screens"] if (s.get("navigation") or {}).get("isEntryPoint"))
    for board in ("7", "8"):
        rows = sorted((s for k, s in on08.items() if k[0] == board), key=lambda s: int(key(s)[1]))
        prov = f"structural — Subscription board {board} on P08, {DATE}"
        both(home08, rows[0], prov)
        for child in rows[1:]:
            both(rows[0], child, prov)
    ready, setup_hub, setup_end, live_hub = on08[("6", "10")], on08[("7", "1")], on08[("7", "10")], on08[("8", "1")]
    both(home08, ready, f"structural — Subscription board 6 on P08, {DATE}")
    link(ready, setup_hub, setup_hub["name"],
         f"structural — the book's handoff, 6.10: \"This hands the customer directly to Board 7\", {DATE}")
    link(setup_end, live_hub, live_hub["name"],
         f"structural — the book's handoff, 7.10: \"This hands the customer to Board 8\", {DATE}")

    # ---- 2. P17 Sign-up ---------------------------------------------------------------------------
    created = "P17" not in docs
    if created:
        p11 = docs["P11"]["platform"]
        docs["P17"] = {"platform": {
            "code": "P17", "audience": "public", "formFactor": "web", "shortName": "TICVAI Sign-up",
            "name": "TICVAI Sign-up — Onboarding & Purchase", "surface": "public",
            "runtime": p11.get("runtime", "reactWeb"), "offlineCapable": False,
            "themes": ["light"], "directions": ["ltr", "rtl"], "screenCount": 0,
            "app": "signup-web", "appStatus": "not scaffolded", "packages": ["design-tokens", "ui"],
            "deployment": {
                "target": "browser", "distribution": "public, served from the Control Plane",
                "bundleUpdate": "immediate on deploy",
                "hosting": ("Control Plane, outside every cell — a prospect has no cell yet. The "
                            "application itself is written to the prospect's regional control "
                            "database (ADR-0043)"),
                "storeReview": False, "deviceOwnership": "prospect device, unmanaged",
                "networkAssumption": "public internet", "releaseCadence": "monthly"},
            "reachesOtherPlatforms": [],
            "operator": "public",
            "wireframeBoard": "wireframes/P17 TICVAI Sign-up.dc.html",
            "wireframeBoardNote": (
                "**The generated board for the whole platform**, declared when the platform was "
                f"created on {DATE} so `check-wireframes` never meets an orphan."),
            "note": (
                "**Somebody who is not a customer yet, buying TICVAI.** Created on "
                f"{DATE} from the Subscription book's boards 2, 4 and 5, which were on P09 — a console "
                "a prospect cannot sign into. **Every operation the journey needs is authenticated "
                "today**: `submitOnboardingApplication` requires `TENANT_CONFIGURE` at tenant scope, "
                "so only a tenant can apply to become one, and `listPlans` requires a TICVAI staff "
                "permission. That is a contract gap, recorded in `workshop-contract-gap.md`, not "
                "something this platform can resolve by being drawn."),
        }, "screens": []}
    p17 = docs["P17"]
    for code in CONTROL:
        ta = docs[code]["platform"].setdefault("targetApp", copy.deepcopy(docs["P09"]["platform"]["targetApp"]))
        ta["siblings"] = [c for c in CONTROL if c != code]
        ta["note"] = CONTROL_NOTE

    by_twin = {(s.get("source") or {}).get("sameAs"): s for s in p17["screens"]}
    new17, synced = [], 0
    for k in SIGNUP:
        twin = on09[k]
        mine = by_twin.get(twin["id"])
        if mine is None:
            sid = next_id("SGN", p17)
            section = SIGNUP_SECTION[k[0]]
            mine = {
                "id": sid, "name": twin["name"], "module": section,
                "requiresModule": "core", "wave": twin.get("wave"),
                "source": {"sameAs": twin["id"], "book": PACK, "board": twin["source"]["board"],
                           "number": twin["source"]["number"], "page": twin["source"]["page"]},
                "implementation": {
                    "app": p17["platform"]["app"],
                    "route": f"/{slug(section)}/{slug(twin['name'])[:56]}-{sid.lower()}",
                    "component": f"apps/{p17['platform']['app']}/src/routes/{slug(section)}/{pascal(twin['name'])}.tsx",
                    "status": "notStarted"},
                "density": "compact",
                "notes": (f"The self-service form of `{twin['id']}`, for a prospect with no account. "
                          f"Decided {DATE}; P09 keeps its screen for the operator-led path (BL-165). "
                          "`tools/applied/apply-subscription-placement.py` keeps the two in step."),
                "wireframe": {"status": "notStarted", "board": f"{p17['platform']['wireframeBoard']}#{sid.lower()}"},
            }
            p17["screens"].append(mine)
            by_twin[twin["id"]] = mine
            new17.append(sid)
        before = yaml.safe_dump({f: mine.get(f) for f in COPIED}, sort_keys=True)
        for f in COPIED:
            if f in twin:
                mine[f] = copy.deepcopy(twin[f])
            else:
                mine.pop(f, None)
        # `check-screens` holds every web platform to `compact`; P17 was first written `comfortable`.
        mine["density"] = "compact"
        if "emptyNoAccess" in (mine.get("states") or {}):
            mine["states"]["emptyNoAccess"] = P17_NO_ACCESS
        synced += before != yaml.safe_dump({f: mine.get(f) for f in COPIED}, sort_keys=True)

    mine = {key(by_twin[on09[k]["id"]]): by_twin[on09[k]["id"]] for k in SIGNUP}
    journey = f"structural — the book's own journey, 2.1 \"Journey Preview\", {DATE}"
    mine[("2", "1")].setdefault("navigation", {})["isEntryPoint"] = True
    chain = [mine[("2", str(n))] for n in range(1, 11)] + [mine[("4", "1")]]
    for a, b in zip(chain, chain[1:]):
        both(a, b, journey)
    for n in range(2, 8):
        both(mine[("4", "1")], mine[("4", str(n))], journey)
    chain = [mine[("4", "1")]] + [mine[("5", n)] for n in ("1", "2", "3", "4", "6", "7")]
    for a, b in zip(chain, chain[1:]):
        both(a, b, journey)
    link(mine[("5", "7")], mine[("5", "9")], mine[("5", "9")]["name"], journey)
    # **The confirmation is not a dead end; it is the last screen on this device.** The package
    # writes a hand-off to another app as a transition with `crossesDevice`, and no `exitTo`.
    done = mine[("5", "9")].setdefault("navigation", {}).setdefault("transitions", [])
    if not any(str(t.get("to", "")).partition("#")[0] == ready["id"] for t in done):
        done.append({"to": ready["id"], "trigger": ready["name"],
                     "provenance": f"structural — the book's board flow, \"Board 5 — Subscription "
                                   f"Activated → Board 6 → Board 7\", {DATE}",
                     "crossesDevice": True, "back": False})
    p17["platform"]["reachesOtherPlatforms"] = [{
        "screen": ready["id"], "platform": "P08",
        "board": f"{p08['platform']['wireframeBoard']}#{ready['id'].lower()}",
        "note": ("After activation the customer's next screen is *Your TICVAI Environment Is Ready*, "
                 "inside their own tenant — provisioning between the two is automatic (board 6)")}]

    for code in ("P08", "P09", "P17"):
        docs[code]["platform"]["screenCount"] = len(docs[code]["screens"])

    # ---- 3. flows and the gap register follow the ids -------------------------------------------
    flow_edits = []
    for f in sorted(FLOWS.glob("F*.yaml")):
        text = f.read_text(encoding="utf-8")
        hits = [i for i in moved if re.search(rf"\b{i}\b", text)]
        if not hits:
            continue
        doc = yaml.safe_load(text)
        entry = (doc.get("trigger") or {}).get("entryScreen")
        if entry in moved:
            for old, new in moved.items():
                text = re.sub(rf"\b{old}\b", new, text)
            doc = yaml.safe_load(text)
            doc["platforms"] = [f"P08 {p08['platform']['shortName']}"]
            doc["actor"] = "venueManager"
            flow_edits.append((f, doc, f"rewritten onto P08 ({len(hits)} ids)"))
        else:
            steps, out, skip = doc["steps"], [], False
            for st in steps:
                if skip and st.get("screen") == entry:
                    skip = False
                    continue
                skip = False
                if st.get("screen") in moved:
                    skip = True
                    continue
                out.append(st)
            renumber = {}
            for n, st in enumerate(out, 1):
                renumber[st["step"]] = n
                st["step"] = n
            doc["steps"] = out
            # A branch hangs off a step number; one on a dropped step goes, the rest follow.
            doc["branches"] = [{**b, "at": renumber[b["at"]]} for b in doc.get("branches") or []
                               if b.get("at") in renumber]
            flow_edits.append((f, doc, f"{len(steps) - len(out)} step(s) that left the platform dropped"))

    # **6.10 left board 6's flow and must arrive in board 7's**, or it is a board screen no flow
    # names — found by review on 11 September. It opens F213 because on P08 it is the way into the
    # AI Setup hub; `entryScreen` stays the hub, which is what `derive-board-flows` keys a board on.
    pending = {f: (i, doc) for i, (f, doc, _) in enumerate(flow_edits)}
    for f in sorted(FLOWS.glob("F*.yaml")):
        doc = pending[f][1] if f in pending else (yaml.safe_load(f.read_text(encoding="utf-8")) or {})
        if (doc.get("trigger") or {}).get("entryScreen") != setup_hub["id"]:
            continue
        if any(st.get("screen") == ready["id"] for st in doc.get("steps") or []):
            break
        for st in doc["steps"]:
            st["step"] += 1
        doc["branches"] = [{**b, "at": b["at"] + 1} for b in doc.get("branches") or []]
        doc["steps"].insert(0, {"step": 1, "screen": ready["id"],
                                "action": f"Arrives at {ready['name']}", "operations": [],
                                "outcome": ready.get("purpose") or ready["name"]})
        points = doc["trigger"].setdefault("entryPoints", [])
        if f"Arrives at {ready['name']}" not in points:
            points.insert(0, f"Arrives at {ready['name']}")
        if f in pending:
            flow_edits[pending[f][0]] = (f, doc, flow_edits[pending[f][0]][2] + f"; opens on {ready['id']}")
        else:
            flow_edits.append((f, doc, f"opens on {ready['id']}, the hand-off from provisioning"))
        break

    gap = ROOT / "docs" / "active" / "workshop-contract-gap.md"
    gap_text = gap.read_text(encoding="utf-8")
    gap_new = gap_text
    for old, new in moved.items():
        gap_new = re.sub(rf"\b{old}\b", new, gap_new)

    print(f"moved to P08: {len(moved)}" + (f" ({min(moved)}…{max(moved)} → {min(moved.values())}…{max(moved.values())})" if moved else ""))
    print(f"  navigation references to retired ids removed: {stripped}")
    print(f"P17 {'created' if created else 'exists'}: {len(new17)} new screen(s), {synced} re-synced, {len(p17['screens'])} total")
    for f, _, what in flow_edits:
        print(f"  {f.name}: {what}")
    print(f"  workshop-contract-gap.md: {'ids updated' if gap_new != gap_text else 'unchanged'}")
    print(f"P08 {len(p08['screens'])} · P09 {len(p09['screens'])} · P17 {len(p17['screens'])}")
    if not apply:
        print("\npreview only — run with --apply")
        return 0

    for code, doc in docs.items():
        if before_docs.get(code) == yaml.safe_dump(doc, sort_keys=True):
            continue
        path = files.get(code) or SCREENS / "P17-ticvai-signup.yaml"
        dump(path, doc)
        print(f"  -> {path.name}")
    for f, doc, _ in flow_edits:
        dump(f, doc)
    if gap_new != gap_text:
        gap.write_text(gap_new, encoding="utf-8")
    print("written — run tools/derive-id-register.py --apply (refresh.sh does)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
