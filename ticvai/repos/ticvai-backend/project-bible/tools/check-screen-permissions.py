#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A screen is gated on a permission its own operations accept, and the ticket media designers on the product one.

**12 October 2026, CHG-R6-030.** The Vivaticket comparison of 6 October found BO-346 PDF, Printable & POS Ticket
Designer gated on `ACCESS_POINT_CONFIGURE` while the ticket templates it draws for (listTicketTemplates, create,
update, clone and import on BO-344) need `PRODUCT_VIEW` / `PRODUCT_CONFIGURE`: a product manager could create a
template and not design it. Chinmay approved moving the designers to the product permission ("Approve
(Recommended)", BC-034..BC-037 in docs/active/breaking-changes.yaml); BO-349's reader-side RFID/NFC profile stays on
`ACCESS_POINT_CONFIGURE`. Nothing had compared a screen's stated gate with the permissions of the operations it calls.

**What fails** (screens/P*.yaml, contracts/):

  SP-NOACCESS     a screen's `states.emptyNoAccess` names a `Permission` value (in backticks) that no operation in its
                  `apis` requires, so the screen tells a user to ask for a permission that would not let them in
                  (check-screen-patterns P3 asks the same, among findings it carries; this gates at zero)
  SP-DESIGNER     a ticket media designer operation (DESIGNERS below) is gated on another permission than the one
                  decided on 12 October
  SP-DOOR         a screen that declares `login` carries a screen permission (r13, CHG-RCR29-001): a door is
                  reached before anybody is signed in, so no permission can let anyone through it. POS-000 was gated
                  on SESSION_FORCE_LOGOUT, taken from its supervisor panel's reads; the panel carries it on its
                  components. tools/derive-screen-wiring.py no longer derives one for a door.
  SP-COMPONENT    a component's `permission` is not a Permission value (ADM-048's 'Duplicate', PTR-030's 'Approve'
                  were labels), or differs from the permission of the operation the component calls when no
                  operation on the screen requires it and that operation's contract text does not name it: BO-291's
                  Save membership commercial config was gated on PLATFORM_CELL_MANAGE while
                  setMembershipCommercialConfig needs MEMBERSHIP_MANAGE, so the users who see the button and the
                  users the server lets through disagree (r13, CHG-RCR29-001, review finding 2.29883.5). A
                  component may be gated more narrowly than its operation when the screen has an operation that
                  needs that permission (POS-007's over/short panel, OVERSHORT_ACCEPT).

Read-only. Exit 1 on any finding. The self-tests of SP-DOOR and SP-COMPONENT run first, every time.

    python3 tools/check-screen-permissions.py [--self-test]
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

# Chinmay, 12 October 2026 (CHG-R6-030): the artwork of a ticket template takes the product permission; the
# reader-side chip profile stays access configuration.
DESIGNERS = {
    "getPdfPrintablePos": "PRODUCT_VIEW",
    "setPdfPrintablePos": "PRODUCT_CONFIGURE",
    "setAppleWalletPass": "PRODUCT_CONFIGURE",
    "setGoogleWalletPass": "PRODUCT_CONFIGURE",
    "setRfidNfcCard": "ACCESS_POINT_CONFIGURE",
}


def load(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=LOADER)


def components(s: dict):
    """Every component of a screen's layout, nested ones included."""
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


def door_and_components(sid: str, s: dict, perms: dict, texts: dict, vocab: set) -> list[str]:
    """SP-DOOR and SP-COMPONENT for one screen (perms: operationId -> permission; texts: operationId -> its summary
    and description)."""
    out = []
    ops = [a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)]
    if "login" in ops and s.get("permission"):
        out.append(f"SP-DOOR       {sid}: declares login, so it is a door, and is gated on {s.get('permission')}; put the "
                   f"permission on the components that need it")
    required = {perms.get(o) for o in ops} - {None}
    for c in components(s):
        cp = c.get("permission")
        if not cp:
            continue
        label = c.get("label") or c.get("kind")
        op = c.get("operation")
        need = perms.get(op) if op else None
        if cp not in vocab:
            out.append(f"SP-COMPONENT  {sid} {label!r}: permission {cp!r} is not a Permission value"
                       + (f" ({op} needs {need})" if need else ""))
        elif need and cp != need and cp not in required and cp not in texts.get(op, ""):
            out.append(f"SP-COMPONENT  {sid} {label!r}: gated on {cp}, while {op} needs {need} and no operation on the "
                       f"screen needs {cp}")
    return out


def self_test() -> list[str]:
    vocab = {"SESSION_FORCE_LOGOUT", "MEMBERSHIP_MANAGE", "PLATFORM_CELL_MANAGE", "OVERSHORT_ACCEPT", "SHIFT_OPEN"}
    perms = {"login": None, "listActiveSessions": "SESSION_FORCE_LOGOUT", "setCfg": "MEMBERSHIP_MANAGE",
             "listShifts": "SHIFT_OPEN", "acceptOverShort": "OVERSHORT_ACCEPT"}

    def scr(perm, ops, comps):
        return {"permission": perm, "apis": [{"operationId": o} for o in ops],
                "layout": {"regions": [{"components": comps}]}}
    cases = [
        ("a gated door", scr("SESSION_FORCE_LOGOUT", ["login", "listActiveSessions"], []), ["SP-DOOR"]),
        ("an open door, its panel gated", scr(None, ["login", "listActiveSessions"],
                                              [{"kind": "detailPanel", "operation": "listActiveSessions",
                                                "permission": "SESSION_FORCE_LOGOUT"}]), []),
        ("a platform permission on a venue write", scr("MEMBERSHIP_MANAGE", ["setCfg"],
                                                       [{"kind": "primaryButton", "operation": "setCfg",
                                                         "permission": "PLATFORM_CELL_MANAGE"}]), ["SP-COMPONENT"]),
        ("a label for a permission", scr(None, [], [{"kind": "secondaryButton", "permission": "Approve"}]),
         ["SP-COMPONENT"]),
        ("narrower, and the screen needs it", scr("SHIFT_OPEN", ["listShifts", "acceptOverShort"],
                                                   [{"kind": "dataTable", "operation": "listShifts",
                                                     "permission": "OVERSHORT_ACCEPT"}]), []),
        ("nested", scr(None, ["setCfg"], [{"kind": "card", "items": [{"kind": "primaryButton", "operation": "setCfg",
                                                                       "permission": "PLATFORM_CELL_MANAGE"}]}]),
         ["SP-COMPONENT"]),
    ]
    bad = []
    for name, s, want in cases:
        got = [x.split()[0] for x in door_and_components("T-1", s, perms, {}, vocab)]
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
        print("PASS - the SP-DOOR and SP-COMPONENT self-tests")
        return 0
    perms: dict[str, str | None] = {}
    texts: dict[str, str] = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        doc = load(f) or {}
        for item in (doc.get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId"):
                    perms[op["operationId"]] = op.get("x-ticvai-permission")
                    texts[op["operationId"]] = f"{op.get('summary') or ''} {op.get('description') or ''}"
    modules = (load(ROOT / "contracts" / "shared" / "permissions.yaml") or {}).get("x-ticvai-permission-modules") or {}
    vocab = {p for values in (modules.get("modules") or {}).values() for p in values or []}

    bad: list[str] = []
    for op, want in DESIGNERS.items():
        if op not in perms:
            bad.append(f"SP-DESIGNER   {op} is in no contract")
        elif perms[op] != want:
            bad.append(f"SP-DESIGNER   {op} requires {perms[op]}; decided {want} (CHG-R6-030)")

    screens = 0
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = load(f) or []
        items = doc if isinstance(doc, list) else doc.get("screens") or []
        for s in items:
            if not isinstance(s, dict):
                continue
            screens += 1
            bad += door_and_components(f"{f.name} {s.get('id')}", s, perms, texts, vocab)
            text = str((s.get("states") or {}).get("emptyNoAccess") or "")
            named = [p for p in re.findall(r"`([A-Z][A-Z0-9_]+)`", text) if p in vocab]
            if not named:
                continue
            required = {perms.get(a.get("operationId")) for a in s.get("apis") or [] if isinstance(a, dict)}
            if not set(named) & required:
                bad.append(f"SP-NOACCESS   {f.name} {s.get('id')}: emptyNoAccess names {', '.join(named)}, which none "
                           f"of its operations requires ({', '.join(sorted(p for p in required if p)) or 'none'})")

    print(f"check-screen-permissions: {screens} screen(s), {len(DESIGNERS)} designer operation(s)")
    for b in bad:
        print(f"  FAIL {b}")
    if bad:
        print(f"FAIL - {len(bad)} finding(s)")
        return 1
    print("PASS - every screen's stated gate is a permission its operations require; no door is gated; every component's "
          "gate is its operation's; the designers as decided")
    return 0


if __name__ == "__main__":
    sys.exit(main())
