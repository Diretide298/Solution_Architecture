#!/usr/bin/env python3
"""Move the approvals and communication console screens, and the partner screens that call staff-only operations, to
Venue Management (P08) (2 October 2026).

**Chinmay, 2 October 2026:** the approvals workflow and matrix screens (ADM-319..ADM-368: workflow library, approval
matrix, governance and compliance, approval integration, approval analytics) and the communication service screens
(ADM-038..ADM-047) configure records a tenant owns, so they are venue screens and move to Venue Management, the same
way the ADM-049 move did (tools/applied/move-adm049-2-october.py, CHG-MOV-001): appended at the end of P08, ids kept as
anchors so their tickets keep their keys, navigation rehomed under Venue Home (BO-100), the platform renamed in the flows
and in the contracts' x-ticvai-consumed-by, duplicates merged with the venue screen, and TICVAI staff reaching them only
under a platform-staff grant into the tenant (R098). On the console they carried the R098 tenant picker and grant
(CHG-SBO-001); inside the tenant's own app that frame has no job, so it comes off. The prospect twins ADM-379..ADM-417
stay on the console (Chinmay accepted; check-console-grant exempts them).

**The lead, 2 October 2026 (logged):** the partner-portal screens that call staff-only writers (PTR-026, PTR-029,
PTR-035, PTR-036, PTR-037, PTR-039, PTR-047, PTR-048) are the venue's own administration of its partners, so they move
to Venue Management as staff screens. Their list reads were partner-audience only; staff is added to each (additive),
and the partner the screen edits comes from the row picked, not the session.

    python3 tools/applied/move-approvals-comms-partner-2-october.py [--apply]

Run once; a second run finds nothing to move. CHG-CLN-003 (approvals and communication), CHG-CLN-004 (partner).
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"
P08 = SCREENS / "P08-venue-back-office.yaml"
P09 = SCREENS / "P09-platform-admin-console.yaml"
P10 = SCREENS / "P10-partner-reseller-portal.yaml"
NOTES = ROOT / "handoff" / "design-notes"
FLOWS = ROOT / "flows"
CONTRACTS = ROOT / "contracts"
DAY = "2 October 2026"
HOME = "BO-100"
CONSOLE_HOME = "ADM-002"
FRAME = {"listTenants", "openPlatformStaffGrant", "listOwnPlatformStaffGrants"}
CHG_ADM, CHG_PTR = "CHG-CLN-003", "CHG-CLN-004"
PTR_MOVE = ["PTR-026", "PTR-029", "PTR-035", "PTR-036", "PTR-037", "PTR-039", "PTR-047", "PTR-048"]
# full merge: the moved screen declares exactly the venue screen's operations (check-screen-wiring S-DUP-SCREEN)
FULL = {"ADM-353": "BO-1074"}
PLATFORM_NAME = {"P09": "P09 TICVAI Web", "P10": "P10 Partner Web"}


def adm_in_range(sid: str) -> bool:
    m = re.fullmatch(r"ADM-(\d+)", sid or "")
    return bool(m) and (319 <= int(m.group(1)) <= 368 or 38 <= int(m.group(1)) <= 47)


def read(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return raw, yaml.load(raw.replace("\r\n", "\n"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def write(path: Path, raw: str, doc) -> None:
    out = yaml.dump(doc, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=100)
    path.write_bytes((out.replace("\n", "\r\n") if "\r\n" in raw else out).encode("utf-8"))


def put_after(d: dict, after: str, key: str, value) -> None:
    if key in d:
        d[key] = value
        return
    out = {}
    for k, v in d.items():
        out[k] = v
        if k == after:
            out[key] = value
    if key not in out:
        out[key] = value
    d.clear()
    d.update(out)


def prepend_notes(s: dict, text: str) -> None:
    old = s.get("notes")
    put_after(s, "navigation", "notes", text + ("\n\n" + old if old else ""))


def comps(s):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            yield r, c


# ------------------------------------------------------------------------------------------------ screens
def strip_grant(s: dict) -> bool:
    """Take the console's R098 frame (CHG-SBO-001) off a screen that now runs inside the tenant's cell."""
    had = any(a.get("operationId") in FRAME for a in s.get("apis") or [])
    s["apis"] = [a for a in s.get("apis") or [] if a.get("operationId") not in FRAME]
    for r in (s.get("layout") or {}).get("regions") or []:
        r["components"] = [c for c in r.get("components") or [] if c.get("operation") not in FRAME]
    if s.get("overlays"):
        s["overlays"] = [o for o in s["overlays"] if (o.get("confirm") or {}).get("operation") not in FRAME]
        if not s["overlays"]:
            del s["overlays"]
    (s.get("states") or {}).pop("grantRequired", None)
    es = s.get("entryState")
    if isinstance(es, dict) and es.get("params"):
        es["params"] = [p for p in es["params"] if p.get("name") != "tenantId"]
        if not es["params"]:
            del es["params"]
    notes = str(s.get("notes") or "")
    paras = [p for p in notes.split("\n\n") if not p.startswith("**Tenant picker and platform-staff grant added")]
    if paras != notes.split("\n\n"):
        if any(p.strip() for p in paras):
            s["notes"] = "\n\n".join(paras)
        else:
            s.pop("notes", None)
    return had


def move(s: dict, routes: set, chg: str, why: str, home_of: dict) -> None:
    sid = s["id"]
    imp = s.setdefault("implementation", {})
    old_app = imp.get("app")
    imp["app"] = "venue-management-web"
    imp["component"] = re.sub(r"^apps/[^/]+/", "apps/venue-management-web/", str(imp.get("component", "")))
    if imp.get("route") in routes:
        imp["route"] = imp["route"].rstrip("/") + "-" + sid.lower()
    routes.add(imp.get("route"))
    wf = s.get("wireframe") or {}
    for key in ("board",):
        v = str(wf.get(key, ""))
        for src in ("wireframes/P09 TICVAI Web.dc.html", "wireframes/P10 Partner Web.dc.html"):
            if v.startswith(src):
                wf[key] = v.replace(src, "wireframes/P08 Venue Management.dc.html")
    for sb in wf.get("stateBoards") or []:
        for src in ("wireframes/P09 TICVAI Web.dc.html", "wireframes/P10 Partner Web.dc.html"):
            if str(sb.get("board", "")).startswith(src):
                sb["board"] = sb["board"].replace(src, "wireframes/P08 Venue Management.dc.html")
    nav = s.setdefault("navigation", {})
    entry, exits = list(nav.get("entryFrom") or []), list(nav.get("exitTo") or [])
    outside = home_of.get(sid)   # a hub that stays on the old platform
    if CONSOLE_HOME in entry or CONSOLE_HOME in exits:
        nav["entryFrom"] = [HOME if x == CONSOLE_HOME else x for x in entry]
        nav["exitTo"] = [HOME if x == CONSOLE_HOME else x for x in exits]
        for t in nav.get("transitions") or []:
            if t.get("to") == CONSOLE_HOME:
                t.clear()
                t.update({"to": HOME, "trigger": "Back to Venue Home",
                          "provenance": f"moved to Venue Management {DAY} ({chg}); it returned to the console's "
                                        "Platform Dashboard (ADM-002)", "back": True})
    elif outside:
        nav["entryFrom"] = [HOME if x == outside else x for x in entry]
        nav["exitTo"] = [HOME if x == outside else x for x in exits]
        trs = [t for t in nav.get("transitions") or [] if t.get("to") != outside]
        trs.append({"to": HOME, "trigger": "Back to Venue Home",
                    "provenance": f"moved to Venue Management {DAY} ({chg}); its board's hub {outside} stays on the "
                                  "partner portal, so Venue Home is its venue-side way in", "back": True})
        nav["transitions"] = trs
    prepend_notes(s, why)


def full_merge(s: dict, target: dict) -> None:
    tid, tname = target["id"], target["name"]
    dropped = [a.get("operationId") for a in s.get("apis") or []]
    s["apis"] = []
    for _, c in comps(s):
        c.pop("operation", None)
    for o in s.get("overlays") or []:
        for k in ("confirm", "dismiss"):
            if isinstance(o.get(k), dict):
                o[k].pop("operation", None)
    nav = s.setdefault("navigation", {})
    for t in nav.get("transitions") or []:
        t.pop("operation", None)
        t.pop("carries", None)
    if tid not in (nav.get("exitTo") or []):
        nav["exitTo"] = (nav.get("exitTo") or []) + [tid]
    nav.setdefault("transitions", []).append({"to": tid, "trigger": f"Open {tname}",
                                              "provenance": f"merged into {tid} {DAY} ({CHG_ADM})"})
    st = s.get("states") or {}
    if "emptyNoAccess" in st:
        st["emptyNoAccess"] = (f"Shown when the caller lacks the permission {tid} {tname} requires; this id has no "
                               "operation of its own since the merge, so it names that screen's.")
    if "Carries the create action" in str(st.get("emptyFirstRun") or ""):
        st["emptyFirstRun"] = f"Nothing set up yet. The create action is {tid}'s; this anchor offers none of its own."
    s["apisNote"] = (f"No operations of its own since {DAY} ({CHG_ADM}): merged into {tid} {tname}, whose operations "
                     f"it routes to ({', '.join(dropped)}).")
    s["purpose"] = str(s.get("purpose") or "").rstrip() + f" (merged into {tid} {tname})."
    prepend_notes(s, f"**Merged into {tid} {tname}** (decided {DAY}, Chinmay: \"duplicate screens: merge as proposed\"; "
                     f"{CHG_ADM}). On P08 it declared the same operations as {tid} (check-screen-wiring S-DUP-SCREEN). "
                     f"One implementation, both ids kept: this id stays for traceability and routes to {tid}.")


def partner_to_staff(s: dict) -> None:
    s["requiresModule"] = "partner"
    s["audience"] = "staff"
    es = s.get("entryState")
    if isinstance(es, dict):
        for p in es.get("params") or []:
            if p.get("name") == "partnerId" and p.get("from") == "session":
                p["from"] = "navigation"
                p["optional"] = True
                p["notes"] = ("The partner whose record is edited: the row picked in the list (every partner's rows "
                              f"load when none is passed). Venue staff carry no partner in their session ({CHG_PTR}).")
    st = s.get("states") or {}
    if "emptyNoAccess" in st:
        st["emptyNoAccess"] = ("Names the missing permission (the write's PARTNER_MANAGE, CREDIT_MANAGE or "
                               "SETTLEMENT_RECONCILE). **Never an empty table** that reads as there is no data.")


def apply_screens(apply: bool) -> dict:
    raw8, d8 = read(P08)
    raw9, d9 = read(P09)
    raw10, d10 = read(P10)
    adm = [s for s in d9["screens"] if adm_in_range(s["id"])]
    ptr = [s for s in d10["screens"] if s["id"] in PTR_MOVE]
    if not adm and not ptr:
        print("nothing to move")
        return {}
    B = {s["id"]: s for s in d8["screens"]}
    routes = {str((s.get("implementation") or {}).get("route")) for s in d8["screens"]}
    log = []
    hubs = [s["id"] for s in adm if CONSOLE_HOME in ((s.get("navigation") or {}).get("entryFrom") or [])]
    for s in adm:
        had = strip_grant(s)
        move(s, routes, CHG_ADM,
             f"**Moved to Venue Management (P08) on {DAY}** (Chinmay, 2 October: the approvals workflow and matrix "
             f"screens and the communication service screens move to Venue Management; {CHG_ADM}). It configures a "
             "record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach "
             "it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's "
             "tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their "
             "keys.", {})
        log.append(f"moved {s['id']}{' (grant frame removed)' if had else ''}")
    hub_of = {}
    for s in ptr:
        for h in (s.get("navigation") or {}).get("entryFrom") or []:
            if h.startswith("PTR-") and h not in PTR_MOVE:
                hub_of[s["id"]] = h
    for s in ptr:
        partner_to_staff(s)
        move(s, routes, CHG_PTR,
             f"**Moved to Venue Management (P08) as a staff screen on {DAY}** (the lead's call, logged: the partner "
             f"screens that call staff-only writers are the venue's own administration of its partners; {CHG_PTR}). "
             "The venue's staff set a partner's rights, terms and settlement here; the partner sees the outcome in "
             "its own portal. TICVAI staff reach it only under a platform-staff grant into the tenant (R098). The id "
             "is kept, so its tickets keep their keys.", hub_of)
        log.append(f"moved {s['id']} (staff; hub {hub_of.get(s['id'])} stays on P10)")
    for sid, tid in FULL.items():
        S = {s["id"]: s for s in adm}
        full_merge(S[sid], B[tid])
        log.append(f"full merge {sid} -> {tid}")
    # Venue Home is the way in for the moved hubs and for the partner screens whose hub stays on P10.
    names = {s["id"]: s["name"] for s in adm + ptr}
    hn = B[HOME]["navigation"]
    for sid in hubs + [s["id"] for s in ptr]:
        if sid not in hn["exitTo"]:
            hn["exitTo"].append(sid)
            hn.setdefault("transitions", []).append(
                {"to": sid, "trigger": names[sid],
                 "provenance": f"moved to Venue Management {DAY} ({CHG_ADM if sid.startswith('ADM') else CHG_PTR}); "
                               + ("its workshop board's hub" if sid.startswith("ADM") else
                                  f"its board's hub {hub_of.get(sid)} stays on the partner portal")})
    # The console's dashboard and the partner hubs lose their edges to what moved.
    moved = {s["id"] for s in adm + ptr}
    for s in d9["screens"] + d10["screens"]:
        if s["id"] in moved:
            continue
        nav = s.get("navigation") or {}
        if not (set(nav.get("exitTo") or []) | set(nav.get("entryFrom") or [])) & moved:
            continue
        nav["exitTo"] = [x for x in nav.get("exitTo") or [] if x not in moved]
        nav["entryFrom"] = [x for x in nav.get("entryFrom") or [] if x not in moved]
        if nav.get("transitions"):
            nav["transitions"] = [t for t in nav["transitions"] if t.get("to") not in moved]
        log.append(f"{s['id']} loses its edges to the moved screens")
    d9["screens"] = [s for s in d9["screens"] if s["id"] not in moved]
    d10["screens"] = [s for s in d10["screens"] if s["id"] not in moved]
    d8["screens"] = d8["screens"] + adm + ptr
    for d in (d8, d9, d10):
        d["platform"]["screenCount"] = len(d["screens"])
    for line in log:
        print("  " + line)
    print(f"moved {len(adm)} console and {len(ptr)} partner screens; P08 {len(d8['screens'])}, P09 {len(d9['screens'])}, "
          f"P10 {len(d10['screens'])}")
    if apply:
        write(P08, raw8, d8)
        write(P09, raw9, d9)
        write(P10, raw10, d10)
    return {"adm": [s["id"] for s in adm], "ptr": [s["id"] for s in ptr],
            "declared": {s["id"]: {a.get("operationId") for a in s.get("apis") or []} for s in adm + ptr}}


# ------------------------------------------------------------------------------------------------ contracts
def op_ranges(lines):
    out = []
    verbs = re.compile(r"^(\s+)(get|post|put|patch|delete):\s*$")
    i = 0
    while i < len(lines):
        m = verbs.match(lines[i])
        if not m:
            i += 1
            continue
        ind = len(m.group(1))
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
            j += 1
        oid = None
        for k in range(i, j):
            mm = re.match(r"^\s+operationId:\s*(\S+)", lines[k])
            if mm:
                oid = mm.group(1).strip("'\"")
                break
        out.append((oid, i, j))
        i = j
    return out


def apply_contracts(apply: bool, moved: dict, declared: dict, staff_reads: set) -> None:
    entry = re.compile(r"^(\s*-\s+)(['\"]?)(P09|P10) ((?:ADM|PTR)-\d+)\b(.*)$")
    for f in sorted(CONTRACTS.glob("*/*.yaml")):
        text = f.read_bytes().decode("utf-8")
        crlf = "\r\n" in text
        lines = text.replace("\r\n", "\n").split("\n")
        owner = {}
        for oid, a, b in op_ranges(lines):
            for k in range(a, b):
                owner[k] = oid
        out, changed = [], 0
        for k, ln in enumerate(lines):
            m = entry.match(ln)
            if m and m.group(4) in moved:
                sid, oid = m.group(4), owner.get(k)
                if oid and oid not in declared.get(sid, set()):
                    changed += 1
                    continue
                out.append(f"{m.group(1)}{m.group(2)}P08 {sid}{m.group(5)}")
                changed += 1
                continue
            out.append(ln)
        # the partner list reads a staff screen now calls: staff joins their audience (additive)
        ranges = op_ranges(out)
        for oid, a, b in reversed(ranges):
            if oid not in staff_reads:
                continue
            for k in range(a, b):
                if re.match(r"^\s+x-ticvai-audience:\s*$", out[k]):
                    j = k + 1
                    items = []
                    while j < b and re.match(r"^\s+-\s+\S", out[j]):
                        items.append(out[j].strip()[2:].strip())
                        j += 1
                    if "staff" not in items:
                        pref = re.match(r"^(\s+-\s+)", out[k + 1]).group(1)
                        out.insert(j, f"{pref}staff")
                        changed += 1
                    break
                mm = re.match(r"^(\s+)x-ticvai-audience:\s*\[(.*)\]\s*$", out[k])
                if mm:
                    items = [x.strip() for x in mm.group(2).split(",") if x.strip()]
                    if "staff" not in items:
                        out[k] = f"{mm.group(1)}x-ticvai-audience: [{', '.join(items + ['staff'])}]"
                        changed += 1
                    break
        if changed:
            print(f"  {f.relative_to(ROOT).as_posix()}: {changed} line(s)")
            if apply:
                body = "\n".join(out)
                f.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))


# ------------------------------------------------------------------------------------------------ flows
def apply_flows(apply: bool, moved: set) -> None:
    for f in sorted(FLOWS.glob("F*.yaml")):
        text = f.read_bytes().decode("utf-8")
        doc = yaml.load(text.replace("\r\n", "\n"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
        steps = {str(st.get("screen")) for st in doc.get("steps") or []}
        if not steps & moved:
            continue
        rest = {x for x in steps - moved if x.startswith(("ADM-", "PTR-"))}
        allmoved = not rest
        crlf = "\r\n" in text
        lines = text.replace("\r\n", "\n").split("\n")
        out, added = [], False
        for ln in lines:
            if re.match(r"^- (P09|P10)\b", ln):
                if allmoved:
                    if not added:
                        out.append("- P08 Venue Management")
                        added = True
                    continue
                out.append(ln)
                if not added:
                    out.append("- P08 Venue Management")
                    added = True
                continue
            if ln.strip() in ("- P08 Venue Management", "- P08") and added:
                continue
            if allmoved and ln in ("actor: platformAdmin", "actor: partner"):
                ln = "actor: venueManager"
            out.append(ln)
        if out != lines:
            print(f"  {f.name}: platform {'renamed' if allmoved else 'P08 added'}")
            if apply:
                body = "\n".join(out)
                f.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))


OLD_PATH = re.compile(r"screens/(P09-platform-admin-console|P10-partner-reseller-portal)\.yaml#((?:ADM|PTR)-\d+)")


def repoint_notes(apply: bool, moved: set) -> None:
    for f in sorted(NOTES.glob("*.yaml")):
        raw = f.read_bytes().decode("utf-8")
        new = OLD_PATH.sub(lambda m: f"screens/P08-venue-back-office.yaml#{m.group(2)}" if m.group(2) in moved
                           else m.group(0), raw)
        if new != raw:
            print(f"  {f.relative_to(ROOT).as_posix()}: sources repointed")
            if apply:
                f.write_bytes(new.encode("utf-8"))
    raw8, d8 = read(P08)
    n = 0
    for s in d8["screens"]:
        if s["id"] not in moved:
            continue
        def walk(x):
            if isinstance(x, str):
                return OLD_PATH.sub(lambda m: f"screens/P08-venue-back-office.yaml#{m.group(2)}"
                                    if m.group(2) in moved else m.group(0), x)
            if isinstance(x, list):
                return [walk(v) for v in x]
            if isinstance(x, dict):
                return {k: walk(v) for k, v in x.items()}
            return x
        new = walk(s)
        if new != s:
            s.clear()
            s.update(new)
            n += 1
    print(f"  P08: {n} moved screen(s) cite their own old path; repointed")
    if apply and n:
        write(P08, raw8, d8)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    r = apply_screens(a.apply)
    if r:
        moved = set(r["adm"]) | set(r["ptr"])
        staff_reads = {o for sid in r["ptr"] for o in r["declared"][sid] if o.startswith("list")}
        apply_contracts(a.apply, moved, r["declared"], staff_reads)
        apply_flows(a.apply, moved)
        repoint_notes(a.apply, moved)
    print("applied" if a.apply else "dry run: --apply writes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
