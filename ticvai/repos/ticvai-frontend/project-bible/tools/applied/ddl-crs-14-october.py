#!/usr/bin/env python3
"""One-off, batch DDL (r6, 14 October 2026): the contract declarations and lineage entries for ADAM CR-069,
CR-070 and CR-073. Already applied; kept as the record of what was changed and why. Idempotent.

* CR-069 (CHG-DDL-004): the keys the Sprint 1 modules built after CR-013 (payments, queue, venuemap, retail)
  carried by naming convention only become declared references (`x-ticvai-references`), so 900 has a foreign
  key and 920 can scope a child through its owner, as CR-013 was settled (CHG-R6-015). `RetailProductRecommendation`
  had its product keys guessed as the recommendation table itself: the source is a catalogue product, the target
  names no single table (`targetService` says which), so `x-ticvai-references: none`.
* CR-070 (CHG-DDL-005): `Refund.taxReversalEntryId` is the journal entry `reverseJournalEntry` posts, not a
  guest in a ride queue (`queue.entry`, the name rule's guess).
* CR-073 (CHG-DDL-007): the outlet operations' lineage names `platform.outlet_opening_hour`, the rows of
  `Outlet.openingHours` (derive-lineage adds entries and never updates one, so an existing entry is edited here).

    python3 tools/applied/ddl-crs-14-october.py [--apply]
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (contract file, schema, property, target table or none)
REFERENCES = [
    # CR-069: payments (OrderService)
    ("contracts/satellite/payments.yaml", "PayInstalmentPlan", "orderId", "orders.sales_order"),
    ("contracts/satellite/payments.yaml", "ChargebackEvidence", "chargebackId", "orders.chargeback"),
    ("contracts/satellite/payments.yaml", "PaymentsEligibilityRule", "paymentMethodId", "payments.method"),
    ("contracts/satellite/payments.yaml", "PaymentsMethodConfig", "paymentMethodId", "payments.method"),
    ("contracts/satellite/payments.yaml", "PaymentTerminal", "deviceId", "platform.device"),
    ("contracts/spine/orders.yaml", "PaymentRouting", "providerId", "payments.provider"),
    ("contracts/spine/orders.yaml", "PaymentRouting", "fallbackProviderId", "payments.provider"),
    ("contracts/spine/orders.yaml", "PaymentToken", "providerId", "payments.provider"),
    # CR-069: venuemap
    ("contracts/satellite/venue-map.yaml", "VenueMapVersion", "mapId", "venuemap.map"),
    ("contracts/satellite/venue-map.yaml", "VenueMapVersion", "publishedByPrincipalId", "identity.principal"),
    ("contracts/satellite/venue-map.yaml", "PlacedResource", "mapId", "venuemap.map"),
    ("contracts/satellite/venue-map.yaml", "VenuePath", "fromPointId", "venuemap.point"),
    ("contracts/satellite/venue-map.yaml", "VenuePath", "toPointId", "venuemap.point"),
    ("contracts/satellite/venue-map.yaml", "VenuePath", "restrictedByPointId", "venuemap.point"),
    # CR-069: queue
    ("contracts/satellite/queue.yaml", "CreateQueueRequest", "parentQueueId", "queue.queue"),
    ("contracts/satellite/queue.yaml", "WaitingGuest", "priorityTierId", "marketing.programme_tier"),
    ("contracts/satellite/queue.yaml", "WaitingGuest", "priorityPromotionId", "promotions.promotion"),
    ("contracts/satellite/queue.yaml", "WaitingGuest", "overriddenByPrincipalId", "identity.principal"),
    ("contracts/satellite/queue.yaml", "QueueReading", "feedId", "queue.feed"),
    # CR-069: retail (the product keys the name rule pointed at the recommendation table itself)
    ("contracts/satellite/retail.yaml", "RetailProductRecommendation", "sourceProductId", "catalogue.product"),
    ("contracts/satellite/retail.yaml", "RetailProductRecommendation", "targetProductId", "none"),
    # CR-070
    ("contracts/spine/orders.yaml", "Refund", "taxReversalEntryId", "ledger.journal_entry"),
]

# operationId -> (reads to add, writes to add)
LINEAGE = {
    "createOutlet": (["platform.outlet_opening_hour"], ["platform.outlet_opening_hour"]),
    "updateOutlet": (["platform.outlet_opening_hour"], ["platform.outlet_opening_hour"]),
    "getOutlet": (["platform.outlet_opening_hour"], []),
    "listOutlets": (["platform.outlet_opening_hour"], []),
}


def declare(path: Path, schema: str, prop: str, target: str, apply: bool) -> str:
    raw = io.open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    start = next((i for i, l in enumerate(lines) if re.match(r"^    " + schema + r":\s*$", l)), None)
    if start is None:
        return f"  ! {schema} not found in {path.name}"
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^    [A-Za-z]", lines[i])), len(lines))
    hit = next((i for i in range(start, end) if re.match(r"^(\s+)" + prop + r":", lines[i])), None)
    if hit is None:
        return f"  ! {schema}.{prop} not found in {path.name}"
    line = lines[hit]
    ind = len(line) - len(line.lstrip())
    m = re.match(r"^(\s+" + prop + r":\s*)\{(.*)\}\s*$", line)
    if m:
        if "x-ticvai-references" in m.group(2):
            return f"  = {schema}.{prop} already declared"
        lines[hit] = f"{m.group(1)}{{{m.group(2).rstrip()}, x-ticvai-references: {target} }}"
    else:
        j = hit + 1
        while j < end and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
            if re.match(r"^\s+x-ticvai-references:", lines[j]) and len(lines[j]) - len(lines[j].lstrip()) == ind + 2:
                return f"  = {schema}.{prop} already declared"
            j += 1
        lines.insert(hit + 1, " " * (ind + 2) + f"x-ticvai-references: {target}")
    if apply:
        io.open(path, "w", encoding="utf-8", newline="").write(nl.join(lines))
    return f"  + {path.name} {schema}.{prop} -> {target}"


def main() -> int:
    apply = "--apply" in sys.argv
    tic = ROOT / "ticvai" if (ROOT / "ticvai").is_dir() else ROOT
    for f, s, p, t in REFERENCES:
        print(declare(tic / f, s, p, t, apply))
    lin_path = tic / "handoff" / "api-data-lineage.json"
    lin = json.loads(lin_path.read_text(encoding="utf-8"))
    n = 0
    for oid, (reads, writes) in LINEAGE.items():
        e = lin.get(oid)
        if e is None:
            print(f"  ! lineage has no {oid}")
            continue
        for key, add in (("reads", reads), ("writes", writes)):
            for t in add:
                if t not in e.setdefault(key, []):
                    e[key] = sorted(set(e[key]) | {t})
                    n += 1
    print(f"  lineage: {n} table name(s) added")
    if apply and n:
        raw = lin_path.read_text(encoding="utf-8")
        indent = 1 if raw.startswith("{\n ") else None
        lin_path.write_text(json.dumps(lin, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""),
                            encoding="utf-8")
    if not apply:
        print("dry run; pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
