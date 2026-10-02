#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every TICVAI Console screen that acts in a tenant carries the tenant picker and the platform-staff grant.

**Audit R098, decided again by Chinmay on 2 October 2026 (pre-apply round: "console R098, about 66 screens: add
a tenant picker and grant", CHG-SBO-001).** The Console (P09) runs in the Control Plane, outside every cell. A
platform operator's token carries PLATFORM_* permissions and no tenant permission, so an operation gated by a
tenant permission (TENANT_CONFIGURE, AI_CONFIGURE, APPROVAL_CONFIGURE, ...) is refused 403 until the operator
picks a tenant and opens a time-boxed, audited grant into it. ADM-412 is the reference implementation.

Rules (P09 only):

  C-GRANT    a screen declaring an operation whose x-ticvai-permission is a tenant permission (not PLATFORM_*)
             also declares listTenants (the picker) and openPlatformStaffGrant (the grant), reaches
             openPlatformStaffGrant from a button or an overlay, and has a `grantRequired` state.
  C-CORE     a Console screen's requiresModule is `core`: a platform operator's console does not depend on what
             any tenant licensed (design-note corrections, platform-foundation, 1-2 October 2026).

The 408 workshop-pack screens moved to Venue Management on 2 October (Chinmay: "they are venue screens", DEC-100,
CHG-MOV-001) are P08 screens and this check no longer reads them; ADM-068 and ADM-619 stayed on the Console and
carry the grant. So did the approvals and communication screens (ADM-319..ADM-368, ADM-038..ADM-047) the same day
(CHG-CLN-003): inside the tenant's own app they need no tenant picker. **Prospect twins (decided):** the Console's
sign-up journey ADM-379..ADM-417 is TICVAI's assisted-sale view of a prospect who has no tenant yet, so there is no
tenant to open a grant into. Chinmay accepted, 2 October 2026, keeping them on the Console and exempt from C-GRANT
(CHG-CLN-003); any screen another platform copies (`source.sameAs`, the P17 sign-up journey) is exempt the same way.
C-CORE still applies to them.

Read-only. Exit 1 on any finding.

    python3 tools/check-console-grant.py
"""
import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
CONSOLE = ROOT / "screens" / "P09-platform-admin-console.yaml"
CONTRACTS = ROOT / "contracts"
FRAME = {"listTenants", "openPlatformStaffGrant", "listOwnPlatformStaffGrants"}
# The prospect twins: the Console's sign-up journey, exempt from C-GRANT (Chinmay, 2 October 2026; CHG-CLN-003).
PROSPECT_TWINS = range(379, 418)


def prospect_twin(sid: str) -> bool:
    m = re.fullmatch(r"ADM-(\d+)", sid or "")
    return bool(m) and int(m.group(1)) in PROSPECT_TWINS


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    try:
        return yaml.load(text, Loader=yaml.CSafeLoader)
    except Exception:
        return yaml.load(text, Loader=yaml.SafeLoader)


def permissions() -> dict:
    out = {}
    for f in CONTRACTS.rglob("*.yaml"):
        doc = load(f) or {}
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = op.get("x-ticvai-permission")
    return out


def twins() -> set:
    out = set()
    for f in (ROOT / "screens").glob("P*.yaml"):
        if f == CONSOLE:
            continue
        for s in (load(f) or {}).get("screens") or []:
            t = (s.get("source") or {}).get("sameAs")
            if t:
                out.add(t)
    return out


def main() -> int:
    perms = permissions()
    copied = twins()
    doc = load(CONSOLE) or {}
    findings = []
    checked = 0
    for s in doc.get("screens") or []:
        sid = s.get("id", "?")
        checked += 1
        if (s.get("requiresModule") or "core") != "core":
            findings.append(("C-CORE", f"{sid}: requiresModule is {s.get('requiresModule')!r}, not core"))
        apis = {a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)}
        tenant = sorted(o for o in apis - FRAME
                        if perms.get(o) and not str(perms.get(o)).startswith("PLATFORM_"))
        if not tenant or sid in copied or prospect_twin(sid):
            continue
        missing = sorted({"listTenants", "openPlatformStaffGrant"} - apis)
        if missing:
            findings.append(("C-GRANT", f"{sid}: calls {tenant[0]} ({perms[tenant[0]]}) and declares no "
                                        f"{', '.join(missing)}"))
            continue
        comps = [c for r in (s.get("layout") or {}).get("regions") or [] for c in r.get("components") or []
                 if isinstance(c, dict)]
        reached = any("Button" in str(c.get("kind")) and c.get("operation") == "openPlatformStaffGrant" for c in comps) \
            or any((o.get("confirm") or {}).get("operation") == "openPlatformStaffGrant"
                   for o in s.get("overlays") or [] if isinstance(o, dict))
        if not reached:
            findings.append(("C-GRANT", f"{sid}: declares openPlatformStaffGrant and nothing opens it"))
        if "grantRequired" not in (s.get("states") or {}):
            findings.append(("C-GRANT", f"{sid}: acts in a tenant and has no grantRequired state"))
    for rule, msg in findings:
        print(f"  {rule:8s} {msg}")
    if findings:
        print(f"FAIL - {len(findings)} finding(s) on {checked} console screen(s)")
        return 1
    print(f"PASS - {checked} console screen(s): every one acting in a tenant has the picker and the grant; all core")
    return 0


if __name__ == "__main__":
    sys.exit(main())
