#!/usr/bin/env python3
"""
Validate screen definitions.

Four checks, in order of how often they catch something:

  1. Component vocabulary — every `kind` exists in _components.yaml. A screen calling for a
     component that does not exist is either asking for something new (add it deliberately)
     or using a name the design system already has under a different label.

  2. operationIds resolve — every API referenced exists in the contracts. This is the check
     that catches a wireframe drawn against an imagined endpoint, which is the expensive
     failure: it survives design review, survives estimation, and is found at build.

  3. Four states — loading, empty and error on every screen; offline where the platform is
     offline-capable. The empty state is the one that reaches production unconsidered.

  4. Navigation resolves — every entryFrom and exitTo points at a screen that exists.
  5. Platform naming holds together — audience, form factor, surface and runtime must agree,
     and a POS or handheld must be offline-capable.
  5. Platform naming holds together — audience, form factor, surface and runtime must agree,
     and a POS or handheld must be offline-capable.

Run: python3 tools/check-screens.py
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai-contracts" / "openapi"
if not CONTRACTS.exists():
    CONTRACTS = ROOT / "contracts"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def load_vocabulary() -> tuple[set[str], set[str]]:
    doc = yaml.safe_load((SCREENS / "_components.yaml").read_text())
    return ({c["kind"] for c in doc.get("components", [])},
            {r["id"] for r in doc.get("regions", [])})


def load_operation_ids() -> set[str]:
    ops: set[str] = set()
    if not CONTRACTS.exists():
        return ops
    for f in CONTRACTS.rglob("*.yaml"):
        try:
            doc = yaml.safe_load(f.read_text())
        except Exception:
            continue
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                    if oid := op.get("operationId"):
                        ops.add(oid)
    return ops


# A platform's name should say what the thing is before what it is for: audience and form
# factor lead, purpose follows. "Guest App — Mobile", not "Guest Mobile App". These maps exist
# so the four fields cannot drift apart — surface and runtime are the older vocabulary and
# must keep agreeing with the newer one.
SURFACE_FOR = {"guest": "guestFacing", "staff": "staffFacing",
               "platformAdmin": "platformAdmin", "partner": "partner", "public": "public"}
RUNTIME_FOR = {"web": {"reactWeb"}, "mobileApp": {"reactNative"},
               "kiosk": {"reactWeb", "embedded"},
               "posTerminal": {"reactNativeTablet", "electron"}, "handheld": {"reactNative"}}
OFFLINE_REQUIRED = {"posTerminal", "handheld"}


SHORTNAMES: dict[str, str] = {}

# A guest or public surface may only call operations a guest can call. Enforced because a
# sibling-attachment pass on 17 August put 659 staff operations onto guest screens — including
# `applyManualDiscount` and `exchangeOrderLines` on a guest's own ticket list — and every other
# checker passed, because each operation existed and resolved to a table.
GUEST_PLATFORMS = {"P01", "P02", "P05", "P11"}


def check_guest_operations(name: str, code: str, screen: dict, staff_ops: set[str]) -> None:
    if code not in GUEST_PLATFORMS:
        return
    for a in (screen.get("apis") or []):
        if (oid := a.get("operationId")) in staff_ops:
            ERRORS.append(f"{name}: {screen['id']} is a guest surface and declares '{oid}', "
                          "which carries a staff permission")


def check_platform(name: str, p: dict) -> None:
    """Also enforces that a shortName identifies exactly one platform.

    Three platforms were called "Staff Web" until 17 August — P08 back office, P12 support and
    P13 the CMS. A name that identifies three things identifies none, and it is the kind of
    collision that survives because each file is individually correct.
    """
    if sn := p.get("shortName"):
        if sn in SHORTNAMES and SHORTNAMES[sn] != p.get("code"):
            ERRORS.append(f"{name}: shortName '{sn}' is already used by "
                          f"{SHORTNAMES[sn]} — a name identifying two platforms identifies none")
        SHORTNAMES[sn] = p.get("code")

    for k in ("code", "audience", "formFactor", "shortName", "name"):
        if k not in p:
            ERRORS.append(f"{name}: platform is missing '{k}'")
            return

    if not p["name"].startswith(p["shortName"]):
        ERRORS.append(f"{name}: name '{p['name']}' does not lead with shortName "
                      f"'{p['shortName']}' — audience and form factor come first")

    expected = SURFACE_FOR.get(p["audience"])
    if expected and p.get("surface") != expected:
        ERRORS.append(f"{name}: surface '{p.get('surface')}' disagrees with audience "
                      f"'{p['audience']}' (expected '{expected}')")

    allowed = RUNTIME_FOR.get(p["formFactor"], set())
    if allowed and p.get("runtime") not in allowed:
        ERRORS.append(f"{name}: runtime '{p.get('runtime')}' is not valid for formFactor "
                      f"'{p['formFactor']}'")

    if p["formFactor"] in OFFLINE_REQUIRED and not p.get("offlineCapable"):
        ERRORS.append(f"{name}: a {p['formFactor']} must be offlineCapable — a gate that "
                      "cannot validate without a network is a queue (ADR-0013)")

    if p["formFactor"] == "web" and p.get("offlineCapable"):
        WARNINGS.append(f"{name}: a web surface declaring offlineCapable is unusual — confirm")


def check(path: Path, kinds: set[str], regions: set[str], ops: set[str], all_ids: set[str]) -> None:
    name = path.name
    doc = yaml.safe_load(path.read_text())
    check_platform(name, doc["platform"])
    offline_capable = doc["platform"].get("offlineCapable", False)

    seen: set[str] = set()
    for s in doc["screens"]:
        check_guest_operations(name, doc["platform"]["code"], s, STAFF_OPS)
        sid = s["id"]
        if sid in seen:
            ERRORS.append(f"{name}: duplicate screen id {sid}")
        seen.add(sid)

        for region in (s.get("layout") or {}).get("regions", []):
            if (ref := region.get("ref")) and ref not in regions:
                ERRORS.append(f"{name}: {sid} references unknown region '{ref}'")
            for c in region.get("components", []):
                if (k := c.get("kind")) not in kinds:
                    ERRORS.append(f"{name}: {sid} uses unknown component '{k}'")

        for api in s.get("apis", []):
            oid = api.get("operationId")
            if oid == "TODO":
                WARNINGS.append(f"{name}: {sid} has a TODO operationId")
            elif ops and oid not in ops:
                ERRORS.append(f"{name}: {sid} references unknown operationId '{oid}'")

        states = s.get("states") or {}
        for required in ("loading", "empty", "error"):
            if required not in states:
                ERRORS.append(f"{name}: {sid} is missing the '{required}' state")
        if offline_capable and "offline" not in states:
            ERRORS.append(f"{name}: {sid} is offline-capable but declares no offline state")
        if todo := [k for k, v in states.items() if v == "TODO"]:
            WARNINGS.append(f"{name}: {sid} has TODO states — {', '.join(todo)}")
        if (s.get("purpose") or "").startswith("TODO"):
            WARNINGS.append(f"{name}: {sid} has no purpose written")

    for s in doc["screens"]:
        nav = s.get("navigation") or {}
        for direction in ("entryFrom", "exitTo"):
            for target in nav.get(direction, []):
                if target not in all_ids:
                    ERRORS.append(f"{name}: {s['id']} {direction} points at unknown screen {target}")

    declared = doc["platform"].get("screenCount")
    if declared is not None and declared != len(doc["screens"]):
        ERRORS.append(f"{name}: screenCount says {declared}, file has {len(doc['screens'])}")


def load_staff_operations() -> set[str]:
    """Operations carrying a staff permission. A guest surface may declare none of them."""
    out: set[str] = set()
    for tier in ("spine", "satellite"):
        d = CONTRACTS / tier
        if not d.exists():
            continue
        for f in d.glob("*.yaml"):
            doc = yaml.safe_load(f.read_text())
            for item in (doc.get("paths") or {}).values():
                if not isinstance(item, dict):
                    continue
                for verb, op in item.items():
                    if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                        # `x-ticvai-guest-callable` marks an operation a guest performs on
                        # their own data — createOrder, createPayment, acquireLease. The
                        # permission is for staff doing it on a guest's behalf at a till.
                        if op.get("x-ticvai-permission") and not op.get("x-ticvai-guest-callable"):
                            out.add(op["operationId"])
    return out


STAFF_OPS: set[str] = set()


def main() -> int:
    global STAFF_OPS
    STAFF_OPS = load_staff_operations()
    files = sorted(SCREENS.glob("P*.yaml"))
    if not files:
        print("no platform files found", file=sys.stderr)
        return 1

    kinds, regions = load_vocabulary()
    ops = load_operation_ids()
    all_ids = {s["id"] for f in files for s in yaml.safe_load(f.read_text())["screens"]}

    print(f"checking {len(files)} platform(s)")
    print(f"  {len(kinds)} component kinds, {len(regions)} regions, {len(ops)} operationIds\n")
    if not ops:
        WARNINGS.append("contracts not found alongside — operationId checking skipped")

    total = 0
    for f in files:
        doc = yaml.safe_load(f.read_text())
        total += len(doc["screens"])
        check(f, kinds, regions, ops, all_ids)
        print(f"  {doc['platform']['code']}  {doc['platform']['name']:30} {len(doc['screens']):>3} screens")

    print(f"\n  {'':36} {total:>3} total\n")
    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
