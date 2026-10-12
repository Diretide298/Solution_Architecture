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

Read-only. Exit 1 on any finding.

    python3 tools/check-screen-permissions.py
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


def main() -> int:
    perms: dict[str, str | None] = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        doc = load(f) or {}
        for item in (doc.get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId"):
                    perms[op["operationId"]] = op.get("x-ticvai-permission")
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
    print("PASS - every screen's stated gate is a permission its operations require; the designers as decided")
    return 0


if __name__ == "__main__":
    sys.exit(main())
