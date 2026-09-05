#!/usr/bin/env python3
"""Size the platform — how many instances of what, under normal load and under a sale.

**Two loads, two mixes, and they are not the same shape.** Under a sale, Catalogue is 64% of the
calls and F&B is absent. Under normal operation Catalogue is 11%, F&B is 13%, and **Order is the
largest single service at 15%** because a venue day is mostly transactions rather than browsing.

**Sizing one from the other is the mistake this tool exists to prevent.** A shared cell provisioned
from the burst mix would run eight Catalogue replicas and one F&B, which is backwards for 363 days
of the year.

## The algorithm

    replicas = max(survivable_floor, ceil(load_rps x service_share / rps_per_replica))

**Three inputs, and only one of them is measured.** `rps_per_replica` comes from ADR-0032's
autoscale triggers and is a hypothesis until `tools/bench.py` runs. `service_share` is derived from
the flows. `load_rps` comes from the venue tier.

**No ceiling in either mode.** A maximum caps absorbing a peak nobody predicted, and under normal
operation the peak is a Saturday nobody scheduled.

**The floor differs by mode and that is the interesting part.**

**Normal**: the floor is survivability — two replicas, because one is a restart that is an outage.
The autoscaler handles the rest, and it has all day to react.

**Sale**: the floor is the expected peak. A burst environment goes `provisioning -> warming ->
live`, warming happens before traffic arrives, and **the first seconds of a flash sale are the
peak** — thirty thousand people do not arrive gradually.

Writes `handoff/sizing.json`.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# **From ADR-0032.** Requests per second one replica sustains at p95 under 200ms. **Hypotheses**:
# `tools/bench.py` replaces them, and the Order figure is the one most likely to be wrong because
# it is bounded by lease contention rather than by CPU.
RPS_PER_REPLICA = {
    "CatalogueService": 400, "OrderService": 250, "IdentityService": 600, "AccessService": 800,
    "TenancyService": 500, "LedgerService": 300, "PlatformService": 400, "WhiteLabelService": 500,
    "FnbService": 300, "InventoryService": 300, "RetailService": 300, "VenueOpsService": 300,
    "MarketingService": 400, "AiService": 100, "ReportingService": 200, "CrossRegionService": 300,
}

# **One replica is a restart that is an outage.** The floor under normal operation, where the
# autoscaler has all day to react to a busy afternoon.
SURVIVABLE_FLOOR = 2

# **Every service scales on its own utilisation, and the target is 60% rather than full.**
#
# **`rpsPerReplica` is a cliff, not a target.** It is what one replica sustains at p95 under 200ms
# — run a service at it and the next request queues. Sizing to 100% means the autoscaler is asked
# to react at the moment latency is already degrading, and it reacts in seconds while a burst
# arrives in milliseconds.
#
# **60% leaves the headroom the reaction needs.** A service at 60% absorbs a 66% spike before it
# degrades at all, which is roughly how long a scale-out takes to serve traffic.
#
# **Previously nothing scaled.** At 375 RPS every service sat at the survivable floor because the
# arithmetic divided by the full figure and rounded to one — **the platform was reporting that
# 3,000 concurrent users drove no capacity anywhere**, which was arithmetically true and
# operationally meaningless.
TARGET_UTILISATION = 0.60

# **Scale out in 5% steps of utilisation, not by doubling.**
#
# **A doubling policy overshoots and then sits there**: 2 to 4 to 8 replicas for a load that needed
# 5, paid for until the cooldown expires. **Stepping adds what the excess requires** — each step
# takes 5 percentage points off utilisation, so a service at 75% steps three times to reach 60%
# rather than doubling past it.
#
# **The deadband matters more than the step.** Anything within 5% of target does not move, which is
# what stops a service oscillating between 4 and 5 replicas all afternoon.
UTILISATION_STEP = 0.05

# **Venue tiers, from the 31 July minute.** Qossai contrasted a Real Madrid-scale stadium selling
# out in hours against a water park at 2,000 visitors a day — *roughly five people a minute*.
VENUES = {
    "small":  {"guests": 2_000,  "buyRate": 0.30, "example": "museum, water park"},
    "medium": {"guests": 18_500, "buyRate": 0.55, "example": "theme park, concert night"},
    "large":  {"guests": 60_000, "buyRate": 0.95, "example": "stadium, arena"},
}

# **A buying guest costs about 22 requests, a visiting guest about 14.** From the flow steps: F58 a
# ticket sold at a till is 21 operations, F61 a gate admitting a group is 12.
REQ_PER_BUYER = 22
REQ_PER_VISITOR = 14
OPEN_HOURS = 12

# **Peak against mean.** A venue day is not flat: a gate opening and a lunch service are both
# multiples of the average, and provisioning for the mean is provisioning for a moment that never
# happens.
NORMAL_PEAK_FACTOR = 6


def flow_mix(lin: dict, only: set | None = None) -> dict:
    """Service share, weighted by how often each operation appears across the flows.

    **94 journeys, each naming its operations.** An operation on the sale path appears in many; one
    on a month-end close appears in one. **That ratio is the workload and it is already recorded** —
    nobody has to estimate it.
    """
    freq: Counter = Counter()
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for step in (doc.get("steps") or []):
            for op in (step.get("operations") or []):
                if op in lin and (only is None or op in only):
                    freq[op] += 1
    svc: Counter = Counter()
    for op, n in freq.items():
        svc[lin[op].get("service")] += n
    total = sum(svc.values()) or 1
    return {s: 100 * n / total for s, n in svc.items() if s}


def size(load_rps: float, mix: dict, floor_is_peak: bool) -> dict:
    """The algorithm. Three inputs, one of them measured.

    **`floor_is_peak` is the whole difference between the two modes.** Under normal operation the
    autoscaler has time and the floor is survivability; during a sale it does not and the floor is
    the peak.
    """
    out = {}
    for svc, share in sorted(mix.items(), key=lambda x: -x[1]):
        per = RPS_PER_REPLICA.get(svc, 400)
        svc_rps = load_rps * (share / 100)
        # **Sized against the target, not the cliff.** One replica is treated as carrying 60% of
        # what it can, so the platform holds the headroom a scale-out needs to happen inside.
        effective = per * TARGET_UTILISATION
        need = math.ceil(svc_rps / effective) if svc_rps > 0 else 0
        floor = max(SURVIVABLE_FLOOR, need) if floor_is_peak else SURVIVABLE_FLOOR
        out[svc] = {
            "share": round(share, 1),
            "rpsAtLoad": round(load_rps * share / 100, 1),
            "rpsPerReplica": per,
            # **What the load implies, and what the autoscaler will actually settle at.** The
            # first `floor` figure was reporting the same 32 replicas for a 382 RPS cell and a
            # 7,036 RPS one, because under normal operation the floor is survivability and the
            # arithmetic sits above it — **the number that varies was being hidden by the number
            # that does not.**
            "impliedByLoad": need,
            "floor": floor,
            "steadyState": max(floor, need),
            "max": None,
            "targetUtilisation": TARGET_UTILISATION,
            # **What the service is actually running at once settled.** A figure well under target
            # means the floor is carrying it and load is not the reason for those replicas.
            "utilisationAtSteady": (
                round(svc_rps / (max(floor, need) * per), 3) if max(floor, need) else 0),
            "scaleOutAt": round(per * TARGET_UTILISATION),
            "stepAddsAt": round(per * (TARGET_UTILISATION + UTILISATION_STEP)),
            "drivenBy": "load" if need > floor else "survivability floor",
        }
    return out


def venue_load(tier: str) -> dict:
    """Requests per second a venue tier generates, mean and peak."""
    v = VENUES[tier]
    buyers = v["guests"] * v["buyRate"]
    daily = buyers * REQ_PER_BUYER + v["guests"] * REQ_PER_VISITOR
    mean = daily / (OPEN_HOURS * 3600)
    return {"guests": v["guests"], "example": v["example"],
            "dailyRequests": round(daily), "meanRps": round(mean, 1),
            "peakRps": round(mean * NORMAL_PEAK_FACTOR, 1)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--sale-rps", type=int, default=5000)
    a = ap.parse_args()

    H = ROOT / "handoff"
    lin = json.loads((H / "api-data-lineage.json").read_text(encoding="utf-8"))
    burst = json.loads((H / "burst-scope.json").read_text(encoding="utf-8"))
    burst_ops = {o["operationId"] for o in burst["operations"]}

    normal_mix = flow_mix(lin)
    sale_mix = {s["name"]: s["weightedShare"] for s in burst["services"] if s["deployed"]}

    # **A shared cell serves many venues at once**, so its load is the sum. Three tiers here is
    # illustrative; the arithmetic takes any mix.
    cells = {}
    for label, counts in (("small cell", {"small": 20, "medium": 4, "large": 0}),
                          ("medium cell", {"small": 60, "medium": 20, "large": 2}),
                          ("large cell", {"small": 120, "medium": 60, "large": 8})):
        mean = sum(venue_load(t)["meanRps"] * n for t, n in counts.items())
        peak = sum(venue_load(t)["peakRps"] * n for t, n in counts.items())
        cells[label] = {
            "venues": counts, "meanRps": round(mean, 1), "peakRps": round(peak, 1),
            "services": size(peak, normal_mix, floor_is_peak=False),
            "replicasAtFloor": sum(v["floor"] for v in size(peak, normal_mix, False).values()),
            "replicasAtPeak": sum(v["steadyState"] for v in size(peak, normal_mix, False).values()),
            "note": ("**Floor is survivability, not peak.** The autoscaler has all day to react to "
                     "a busy afternoon, so paying for the peak all night buys nothing."),
        }

    out = {
        "generatedBy": "tools/derive-sizing.py",
        "algorithm": "replicas = max(floor, ceil(load_rps x share / rps_per_replica))",
        "note": (
            "**Two loads, two mixes, and they are not the same shape.** Under a sale Catalogue is "
            "64% of the calls and F&B is absent; under normal operation Catalogue is 11%, F&B is "
            "13%, and Order is the largest at 15% because a venue day is mostly transactions "
            "rather than browsing.\n\n"
            "**A shared cell sized from the burst mix would run eight Catalogue replicas and one "
            "F&B** — backwards for 363 days of the year."),
        "unmeasured": (
            "`rpsPerReplica` comes from ADR-0032's autoscale triggers and is a hypothesis until "
            "`tools/bench.py` runs. Everything else here is arithmetic on top of it."),
        "venueTiers": {t: venue_load(t) for t in VENUES},
        "normal": {
            "mix": {s: round(v, 1) for s, v in sorted(normal_mix.items(), key=lambda x: -x[1])},
            "cells": cells,
        },
        "sale": {
            "mix": sale_mix,
            "loadRps": a.sale_rps,
            "services": size(a.sale_rps, sale_mix, floor_is_peak=True),
            "note": ("**Floor is the expected peak.** A burst environment warms before traffic "
                     "arrives and the first seconds of a sale are the peak — thirty thousand "
                     "people do not arrive gradually."),
        },
    }

    if a.apply:
        (H / "sizing.json").write_text(json.dumps(out, indent=1, ensure_ascii=False),
                                       encoding="utf-8")

    print(f"  normal: {len(normal_mix)} services · {len(cells)} cell sizes")
    print(f"  sale:   {len(sale_mix)} services at {a.sale_rps} RPS")
    if not a.apply:
        print("  nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
