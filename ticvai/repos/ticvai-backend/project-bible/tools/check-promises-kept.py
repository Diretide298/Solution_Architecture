#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What a screen, a flow or a decision promises has an operation, a field or a reader behind it.

**12 October 2026, CHG-R6-031..038.** The Vivaticket comparison of 6 October found the package's own broken
promises: seated events sold with no way to build a seat map by hand, a scanner "Venue full" that nothing could
make fire, a guest and POS waitlist nobody could join, and a cancellation that "notifies every holder" with
nothing that sends the notice. The same day's decisions (a configurable business-day cut-off, a per-channel
ticket credential, the client's Apple Wallet pass certificate) are settings that only work if every reader reads
them. Each was a promise with nothing behind it, and no check compared the two. This one holds each promise to
the operation, field, binding or reader that keeps it, and keeps the business day one definition.

**What fails** (contracts/, screens/P*.yaml, flows/, events/):

  PK-FIELD      a decided field is missing from its schema, or its default is not the decided one
  PK-OPERATION  a promised operation is in no contract
  PK-BOUND      a screen that makes the promise does not bind the operation (`apis`) or the field (`bindsTo`)
  PK-READER     an operation or schema that must read a setting does not name it in its description
  PK-EVENT      an event's consumer that keeps a promise names no operation, or one that does not consume it
  PK-FLOW       a flow step that keeps a promise lists no operation
  PK-BUSINESS-DAY  a contract description speaks of a business day, business date or trading day and does not say
                it closes at `businessDayCutoff` (tenancy `VenueSettings`), unless the description is in
                OTHER_DAYS with its reason

Read-only. Exit 1 on any finding.

    python3 tools/check-promises-kept.py
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

# (change, contract, schema, field, decided default or None)
FIELDS = [
    ("CHG-R6-031", "catalogue", "SalesChannelProfile", "ticketCredentialFormat", None),
    ("CHG-R6-031", "catalogue", "ChannelFeesPaymentFulfillmentConfigurationInput", "ticketCredentialFormat", None),
    ("CHG-R6-031", "access", "AccessVerificationMethodPolicy", "credentialFormatOverride", None),
    ("CHG-R6-031", "access", "Entitlement", "credentialFormat", None),
    ("CHG-R6-032", "tenancy", "VenueSettings", "businessDayCutoff", "00:00"),
    ("CHG-R6-032", "shift", "Shift", "businessDate", None),
    ("CHG-R6-033", "white-label", "StoreAccount", "passTypeIdentifier", None),
    ("CHG-R6-033", "white-label", "StoreAccount", "passCertificateSecretRef", None),
    ("CHG-R6-033", "white-label", "StoreAccount", "passCertificateExpiresAt", None),
]

# (change, operation, screens that must bind it)
OPERATIONS = [
    ("CHG-R6-035", "editSeatMapStructure", ["BO-954", "BO-956"]),
    ("CHG-R6-036", "setAccessAreaCapacity", ["BO-145"]),
    ("CHG-R6-037", "joinWaitlist", ["WEB-006", "GST-007"]),
    ("CHG-R6-037", "offerWaitlistCapacity", ["BO-017"]),
    ("CHG-R6-038", "notifyPerformanceHolders", []),
    ("CHG-R6-038", "listMessageDispatches", ["BO-023"]),
]

# (change, screen, field it binds)
BINDINGS = [
    ("CHG-R6-031", "ADM-266", "ChannelFeesPaymentFulfillmentConfigurationInput.ticketCredentialFormat"),
    ("CHG-R6-032", "BO-1062", "VenueSettings.businessDayCutoff"),
]

# (change, "operation:<id>" or "schema:<contract>.<Schema>", text its description must contain)
READERS = [
    ("CHG-R6-031", "operation:issueOrderEntitlements", "ticketCredentialFormat"),
    ("CHG-R6-031", "operation:issueOrderEntitlements", "credentialFormatOverride"),
    ("CHG-R6-031", "operation:getEntitlementCredential", "credentialFormat"),
    ("CHG-R6-032", "operation:postOrderRevenue", "businessDayCutoff"),
    ("CHG-R6-032", "operation:getUnifiedReconciliation", "businessDayCutoff"),
    ("CHG-R6-032", "operation:ingestSettlementFile", "businessDayCutoff"),
    ("CHG-R6-032", "operation:closeShift", "businessDayCutoff"),
    ("CHG-R6-032", "operation:runReport", "businessDayCutoff"),
    ("CHG-R6-032", "operation:getKpiValues", "businessDayCutoff"),
    ("CHG-R6-033", "operation:issueWalletPass", "passCertificateSecretRef"),
    ("CHG-R6-036", "schema:access.DenyReason", "setAccessAreaCapacity"),
    ("CHG-R6-038", "operation:cancelPerformance", "notifyPerformanceHolders"),
]

# (change, event file, consumer context, operation it must name)
EVENTS = [
    ("CHG-R6-033", "whitelabel-passCertificateExpiring.yaml", "marketing", None),
    ("CHG-R6-033", "whitelabel-passCertificateExpiring.yaml", "platform-ops", None),
    ("CHG-R6-038", "performance-cancelled.yaml", "marketing", "marketing-crm.notifyPerformanceHolders"),
]

# (change, flow file prefix, step)
FLOW_STEPS = [
    ("CHG-R6-038", "F09-", 5),
]

DAY = re.compile(r"\bbusiness[- ]day\b|\bbusiness[- ]date\b|\btrading[- ]day\b", re.I)
# Descriptions that speak of another day on purpose: (contract, path fragment) -> reason.
OTHER_DAYS = {
    ("finance", "/fx-rates/ingest"): "a bank business day for FX rates, not the venue's trading day",
    ("finance", "FxProviderAssignment"): "the FX feed's business day, not the venue's trading day",
    ("finance", "FxRate/properties/fetchedAt"): "the FX feed's business day, not the venue's trading day",
    ("tenancy", "VenueSettings/properties/calendarDayStartHour"): "says it moves no business date (DEC-039)",
}


def load(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=LOADER) or {}


def descriptions(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "description" and isinstance(v, str):
                yield path, v
            else:
                yield from descriptions(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from descriptions(v, f"{path}[{i}]")


def main() -> int:
    contracts, ops = {}, {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        doc = load(f)
        contracts[f.stem] = doc
        for item in (doc.get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId"):
                    ops[op["operationId"]] = (f.stem, op)
    screens = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = load(f)
        for s in doc if isinstance(doc, list) else doc.get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                screens[s["id"]] = s

    bad: list[str] = []
    for chg, c, schema, field, default in FIELDS:
        prop = ((((contracts.get(c) or {}).get("components") or {}).get("schemas") or {}).get(schema) or {}) \
            .get("properties", {}).get(field)
        if prop is None:
            bad.append(f"PK-FIELD      {c}.{schema}.{field} is missing ({chg})")
        elif default is not None and str(prop.get("default")) != default:
            bad.append(f"PK-FIELD      {c}.{schema}.{field} defaults to {prop.get('default')!r}, decided {default!r} ({chg})")

    for chg, op, on in OPERATIONS:
        if op not in ops:
            bad.append(f"PK-OPERATION  {op} is in no contract ({chg})")
            continue
        for sid in on:
            s = screens.get(sid)
            bound = {a.get("operationId") for a in (s or {}).get("apis") or [] if isinstance(a, dict)}
            if op not in bound:
                bad.append(f"PK-BOUND      {sid} does not bind {op} ({chg})")

    for chg, sid, field in BINDINGS:
        if f"bindsTo: {field}" not in yaml.safe_dump(screens.get(sid) or {}, width=10_000, sort_keys=False):
            bad.append(f"PK-BOUND      {sid} binds no component to {field} ({chg})")

    for chg, where, text in READERS:
        kind, _, name = where.partition(":")
        if kind == "operation":
            desc = str((ops.get(name) or (None, {}))[1].get("description") or "")
        else:
            c, _, schema = name.partition(".")
            desc = str((((contracts.get(c) or {}).get("components") or {}).get("schemas") or {}).get(schema, {})
                       .get("description") or "")
        if text not in desc:
            bad.append(f"PK-READER     {name}'s description does not name {text} ({chg})")

    for chg, fname, context, op in EVENTS:
        p = ROOT / "events" / fname
        if not p.exists():
            bad.append(f"PK-EVENT      events/{fname} is missing ({chg})")
            continue
        ev = load(p)
        cons = [c for c in ev.get("consumers") or [] if c.get("context") == context]
        if not cons:
            bad.append(f"PK-EVENT      {ev.get('name')} has no {context} consumer ({chg})")
        elif op:
            if cons[0].get("operation") != op:
                bad.append(f"PK-EVENT      {ev.get('name')}'s {context} consumer names {cons[0].get('operation')!r}, "
                           f"not {op} ({chg})")
            target = ops.get(op.split(".", 1)[-1])
            if not target or ev.get("name") not in (target[1].get("x-ticvai-consumes") or []):
                bad.append(f"PK-EVENT      {op} does not consume {ev.get('name')} ({chg})")

    for chg, prefix, step in FLOW_STEPS:
        files = sorted((ROOT / "flows").glob(f"{prefix}*.yaml"))
        st = [s for f in files for s in load(f).get("steps") or [] if s.get("step") == step]
        if not st or not st[0].get("operations"):
            bad.append(f"PK-FLOW       {prefix}* step {step} lists no operation ({chg})")

    for c, doc in contracts.items():
        for path, text in descriptions(doc):
            if DAY.search(text) and "businessDayCutoff" not in text and not path.endswith("/businessDayCutoff") \
                    and not any(c == oc and frag in path for oc, frag in OTHER_DAYS):
                # a label-sized description (an enum label, a column title) carries no definition
                if len(text) > 40:
                    bad.append(f"PK-BUSINESS-DAY {c}{path}: speaks of a business or trading day and does not say "
                               f"it closes at businessDayCutoff (CHG-R6-032)")

    print(f"check-promises-kept: {len(FIELDS)} field(s), {len(OPERATIONS)} operation(s), {len(READERS)} reader(s), "
          f"{len(EVENTS)} event consumer(s), {len(FLOW_STEPS)} flow step(s)")
    for b in bad:
        print(f"  FAIL {b}")
    if bad:
        print(f"FAIL - {len(bad)} finding(s)")
        return 1
    print("PASS - every promise checked has its operation, field, binding or reader; one business day")
    return 0


if __name__ == "__main__":
    sys.exit(main())
