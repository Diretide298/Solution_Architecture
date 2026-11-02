#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A decision that names what a screen does is found in that screen's record.

**2 November 2026 (r13, CHG-RCR31-001, CHG-RCR32-001).** The pull of 117 Block A tickets before r12 found
identity decisions made in the contracts and build notes and never carried into the screens that build them
(review roots R31 and R32): IDENTITY-C15 (CHG-R8SPN-024, 20 October) moved CMS-019's Change access from
`updatePrincipal`, which "never grants or removes a role", to `createDelegatedAccess` and `deleteDelegatedAccess`, and
the record still called `updatePrincipal`; IDENTITY-C45 (CHG-R8SPN-032) made a role card name its venue and Select
role send the card's `grantId`, and EMP-002's form still sent `roleId` alone; IDENTITY-C36 decided a badge fills the
username, and SCN-001's PIN note still put the badge in the credential. Each entry said "the surface lane's part" and
closed; nothing checked the surface. This does:

  SD-DECIDED   a screen named in DECIDED below does not declare the operations its decision binds, or still binds
               a control to the operation the decision took away
  SD-GRANT     a form that confirms `selectRole` does not send `grantId` (its body names it), or a card list of a
               person's roles (`LoginResponse.availableRoles`, `Session.availableRoles`, `RoleSummary`) does not
               show the grant's venue (`RoleSummary.scope...`): two grants of one role at two venues would be two
               identical cards, and `roleId` alone is refused 422 grant-required (IDENTITY-C45)
  SD-BADGE     a component's note puts a badge (`card`, `rfid`) in `LoginRequest.credential`: the badge fills the
               username and `method` says how it was entered; the PIN is still the credential (IDENTITY-C36)

What it cannot see: a screen that calls `selectRole` with no list and no form at all (SCN-001 at r13, left for the
lead) passes SD-GRANT, because there is nothing to compare. Read-only; exit 1 on any finding. The self-tests run
first, every time.

    python3 tools/check-screen-decisions.py [--self-test]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

# decision -> the screen, the operations it must declare, and (label, operation) a control may no longer bind
DECIDED = [
    {"decision": "IDENTITY-C15 (CHG-R8SPN-024, 20 October 2026)", "screen": "CMS-019",
     "declares": ["createDelegatedAccess", "deleteDelegatedAccess"],
     "not_bound": [("Change access", "updatePrincipal")]},
]
ROLE_LISTS = ("LoginResponse.availableRoles", "Session.availableRoles", "RoleSummary")
BADGE = re.compile(r"LoginRequest\.credential`?[^.;]*\b(card|rfid)\b", re.I)


def components(s: dict):
    def walk(c):
        yield c
        for v in c.values():
            if isinstance(v, list):
                for x in v:
                    if isinstance(x, dict) and "kind" in x:
                        yield from walk(x)
    for r in (s.get("layout") or {}).get("regions") or []:
        for c in (r or {}).get("components") or []:
            if isinstance(c, dict):
                yield from walk(c)


def confirm_ops(o: dict) -> set:
    c = o.get("confirm") if isinstance(o.get("confirm"), dict) else {}
    return ({c.get("operation")} | set(c.get("alsoCalls") or [])) - {None}


def findings(sid: str, s: dict, decided: list) -> list[str]:
    out = []
    ops = {a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)}
    comps = list(components(s))
    overlays = [o for o in s.get("overlays") or [] if isinstance(o, dict)]
    for d in decided:
        if d["screen"] != sid:
            continue
        for op in d["declares"]:
            if op not in ops:
                out.append(f"SD-DECIDED  {sid}: {d['decision']} binds {op}, which the screen does not declare")
        for label, op in d["not_bound"]:
            bound = [c for c in comps if c.get("label") == label and c.get("operation") == op]
            bound += [o for o in overlays if (o.get("confirm") or {}).get("label") == label
                      and (o.get("confirm") or {}).get("operation") == op]
            if bound:
                out.append(f"SD-DECIDED  {sid}: {label!r} still calls {op} first, which {d['decision']} took away")
    for o in overlays:
        if "selectRole" in confirm_ops(o) and "grantId" not in str(o.get("body") or ""):
            out.append(f"SD-GRANT    {sid}: {o.get('id')} confirms selectRole and does not send grantId")
    for c in comps:
        bt = str(c.get("bindsTo") or "")
        if c.get("kind") == "cardList" and any(bt.startswith(x) for x in ROLE_LISTS):
            if not any(str(x).startswith("RoleSummary.scope") for x in c.get("columns") or []):
                out.append(f"SD-GRANT    {sid}: {c.get('label')!r} lists roles and does not show the grant's venue "
                           f"(RoleSummary.scope)")
        if BADGE.search(str(c.get("notes") or "")):
            out.append(f"SD-BADGE    {sid}: {c.get('label')!r} puts a badge in LoginRequest.credential")
    return out


def self_test() -> list[str]:
    dec = [{"decision": "D-1", "screen": "T-1", "declares": ["a"], "not_bound": [("Go", "b")]}]

    def scr(ops, comps, overlays=()):
        return {"apis": [{"operationId": o} for o in ops], "layout": {"regions": [{"components": list(comps)}]},
                "overlays": list(overlays)}
    cases = [
        ("decided and done", "T-1", scr(["a", "b"], [{"kind": "button", "label": "Go", "operation": "a"}]), []),
        ("not declared", "T-1", scr(["b"], []), ["SD-DECIDED"]),
        ("still bound", "T-1", scr(["a", "b"], [{"kind": "button", "label": "Go", "operation": "b"}]), ["SD-DECIDED"]),
        ("another screen", "T-2", scr([], []), []),
        ("role form without the grant", "T-2", scr(["selectRole"], [], [
            {"id": "f", "body": "Sends roleId.", "confirm": {"operation": "selectRole"}}]), ["SD-GRANT"]),
        ("role form with the grant", "T-2", scr(["selectRole"], [], [
            {"id": "f", "body": "Sends roleId and grantId.", "confirm": {"operation": "selectRole"}}]), []),
        ("cards without the venue", "T-2", scr([], [{"kind": "cardList", "bindsTo": "LoginResponse.availableRoles",
                                                   "columns": ["RoleSummary.name"]}]), ["SD-GRANT"]),
        ("cards with the venue", "T-2", scr([], [{"kind": "cardList", "bindsTo": "LoginResponse.availableRoles",
                                                "columns": ["RoleSummary.name", "RoleSummary.scope.name"]}]), []),
        ("badge in the credential", "T-2", scr([], [{"kind": "textField", "notes":
            "Goes into `LoginRequest.credential` with `method: pin`, or the badge with `method: card`."}]), ["SD-BADGE"]),
        ("badge in the username", "T-2", scr([], [{"kind": "textField", "notes":
            "Goes into `LoginRequest.credential`; the PIN is typed. A badge fills the username, method `card`."}]), []),
    ]
    bad = []
    for name, sid, s, want in cases:
        got = [x.split()[0] for x in findings(sid, s, dec)]
        if got != want:
            bad.append(f"self-test {name}: expected {want}, got {got}")
    return bad


def main() -> int:
    tests = self_test()
    for t in tests:
        print(f"  SELF-TEST  {t}")
    if tests:
        print(f"FAIL {len(tests)} self-test(s)")
        return 1
    if "--self-test" in sys.argv:
        print("PASS - the SD-DECIDED, SD-GRANT and SD-BADGE self-tests")
        return 0
    bad, n, seen = [], 0, set()
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.load(f.read_text(encoding="utf-8"), Loader=LOADER) or []
        for s in doc if isinstance(doc, list) else doc.get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                n += 1
                seen.add(s["id"])
                bad += findings(s["id"], s, DECIDED)
    for d in DECIDED:
        if d["screen"] not in seen:
            bad.append(f"SD-DECIDED  {d['screen']}: named by {d['decision']} and not in screens/")
    print(f"check-screen-decisions: {n} screen(s), {len(DECIDED)} decided binding(s)")
    for b in bad:
        print(f"  FAIL {b}")
    if bad:
        print(f"FAIL - {len(bad)} finding(s)")
        return 1
    print("PASS - the decided bindings are in their screens; role forms send the grant and role cards name the venue; "
          "no badge goes in the credential")
    return 0


if __name__ == "__main__":
    sys.exit(main())
