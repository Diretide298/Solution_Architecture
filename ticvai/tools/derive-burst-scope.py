#!/usr/bin/env python3
"""Derive what a flash-sale environment runs, for the viewer.

**Not a list somebody chose.** The burst path comes from the flows already walked — F43 the
concurrency case, F58 a ticket sold at a till, F59 a seat picked and held — plus the discovery
operations a guest hits before buying.

**Presence on the path is not the same as carrying the load.** Seven services appear; two of them
account for 86% of the calls a single buyer makes. **Weighting by calls-per-buyer is what separates
a service that must replicate from one that is merely reachable**, and it is the difference between
deploying three services and deploying seven.

**Six services see no part of a ticket sale**: Marketing, Reporting, Inventory, F&B, Maintenance,
WhiteLabel. They are in the output marked `deployed: false` rather than omitted, **because a viewer
showing what is absent is more useful than one showing only what is present.**

Writes `handoff/burst-scope.json` — services, tables and operations, each with the reason.
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

# **The flows that constitute a sale.** F43 is the concurrency case and the reason this environment
# exists at all — two people wanting the last seat.
BURST_FLOWS = ("F43", "F58", "F59")

# **Discovery is not in a flow because nobody wrote a flow for browsing.** It is most of the
# traffic: a buyer looks at four things and buys one, so the read path outnumbers the write path
# by an order of magnitude and sizes the environment.
DISCOVERY = {
    "listProducts", "getProduct", "listPerformances", "getAvailability", "searchCatalogue",
    "listEvents", "getEvent", "evaluatePromotions", "getCart", "addCartLine", "createOrder",
    "createPayment", "acquireInventoryHold", "createSeatHold", "getSeatMap", "listSeats",
    "authenticate", "refreshToken",
}

# **Calls a single buyer makes.** Estimated from the flow steps and the shape of a purchase — a
# buyer checks availability repeatedly and pays once. **These are the numbers a benchmark replaces**,
# and until it runs they are the honest basis for the weighting rather than an equal split.
CALLS_PER_BUYER = {
    "getAvailability": 6, "getCart": 4, "getProduct": 4, "listProducts": 3,
    "acquireInventoryHold": 3, "listPerformances": 2, "getSeatMap": 2, "listSeats": 2,
    "createSeatHold": 2, "addCartLine": 2, "evaluatePromotions": 2,
    "createOrder": 1, "createPayment": 1, "authenticate": 1, "refreshToken": 1,
}

# **The autoscale triggers from ADR-0032**, in requests per second per replica. **These are the
# declared decisions**; the replica count is arithmetic on top of them and used to be declared
# separately, which is how `deploy/c-flash-sale.yml`, ADR-0035 and this file came to state three
# different sets of numbers with no workings behind any of them.
RPS_PER_REPLICA = {
    "CatalogueService": 400,
    "OrderService": 250,
    "IdentityService": 600,
    "AccessService": 800,
}

# **The floor a service can never drop below, whatever the arithmetic says.**
#
# **A burst environment has no resting state**, which is why this is not the usual cost-against-
# cold-start trade. It goes `provisioning -> warming -> live`, and **warming happens before any
# traffic arrives** — so by the time the sale opens the environment is already scaled and there is
# no idle period for a low floor to save money during.
#
# **The first seconds of a flash sale are the peak.** Thirty thousand people do not arrive
# gradually. A floor below the expected peak means the opening moment is served by whatever was
# provisioned while the autoscaler catches up — **and that is precisely the moment that must not
# queue.**
#
# **So the floor is the expected peak** (see `replicas_for`), and these are only the absolute
# minimum below which a service is not survivable regardless: **one replica is a restart that is
# an outage.**
ABSOLUTE_MIN = {
    "CatalogueService": 2,
    "OrderService": 2,
    "IdentityService": 2,
}

# **A reference load, not a limit.** Used to say what the trigger implies so a database and a
# pool can be sized; the autoscaler is not bounded by it.
# **The target the environment is sized for.** 5,000 RPS is roughly one stadium selling out fast:
# 60,000 seats over a two-hour window is 1,045 RPS at a six-times burst, and compressed into twenty
# minutes it is 6,270.
TARGET_RPS = 5000

# **Which mode each contended table runs in.** Derived from how the row is selected, not from the
# table name - see the note on `contentionModel` below.
#
# **`seating.seat_hold` is unresolved deliberately.** It is `per_entity` where a guest picks a
# seat and `allocator_serialised` where the system picks, and **nobody has established which the
# platform does** - `seatingRules` in the contract offers best-available, so both are reachable.
# Marking it one or the other on a guess would tell the client a story that may be wrong in the
# direction that matters.
CONTENTION_MODEL = {
    "catalogue.inventory_hold": {
        "modes": ["single_row"],
        "ceilingSource": "pinned",
        "note": "One counter per (performance, ticket type). Every buyer hits the same row.",
    },
    # **Both modes are reachable and the event configuration decides which.** `seatingRules`
    # offers best-available, so a venue can run guest-picks and auto-allocate on one performance.
    #
    # **`unresolved` was the wrong answer and it was the old boolean wearing a new name** - it
    # rendered as "not contended" in every derived artefact, which is the defect it replaced.
    #
    # **Worst case unless the event pins it**, because `allocator_serialised` is the normal
    # configuration for a high-demand on-sale - which is precisely the case this environment
    # exists for. **Showing one red bar was under-stating**, not correcting: in best-available
    # mode `seat_hold` is worse than `inventory_hold`, because losers retry and burn lock
    # acquisitions without producing sales, so effective throughput lands *below* the single-row
    # ceiling rather than at it.
    "seating.seat_hold": {
        "modes": ["per_entity", "allocator_serialised"],
        "ceilingSource": "worst_case_unless_pinned",
        "pinnedBy": "catalogue.performance.seatingRules",
        "note": ("Guest picks a seat: per_entity, 43,693 rows, structurally not contended. "
                 "System picks best available: allocator_serialised, effectively one row and "
                 "worse than single_row because losers retry."),
    },
}

# **Connections a replica holds**, from `deploy/c-flash-sale.yml`.
POOL_MAX_PER_REPLICA = 40

# **One database means one pool** (ADR-0038, which supersedes ADR-0036). This read 3 while a burst
# cell held a database per service; a burst cell is one tenant and one event, so under
# one-database-per-tenant it is one database and one pool.
#
# **Kept as a named constant rather than folded back into the arithmetic.** It was a single figure
# describing one pool before ADR-0036 split it, and it went stale silently on that split — a
# constant that has been wrong twice for the same reason should be visible enough to be checked
# the third time.
#
# **`max_connections` is per instance, not per database**, which still matters: a permanent cell
# holds many tenant databases on one instance, and there the sum across pools is the constraint
# ADR-0032's amended arithmetic is about.
PGBOUNCER_POOLS = 1
PGBOUNCER_MAX_CLIENT_CONN = 5000
PGBOUNCER_SERVER_POOL_SIZE = 80          # per pool
POSTGRES_MAX_CONNECTIONS = 800           # per instance, shared across all three databases

# **8% of weighted calls is the line.** Below it a service is reachable from the burst path and
# served by the shared cell; above it the environment carries its own.
REPLICATE_THRESHOLD = 8.0

# **Which modes count as a wall.** `per_entity` alone does not; anything else does.
CONTENDED_MODES = {"single_row", "allocator_serialised"}


def replicas_for(name: str, share: float) -> dict:
    """The floor. There is no ceiling.

    **A maximum is a cap on surviving the thing you cannot predict**, and the peak is precisely
    what nobody knows — a stadium selling out over two hours is 1,045 RPS, and the same sale
    compressed into twenty minutes is 6,270. **A ceiling set from the first number fails the
    second**, and failing at a ceiling is the Bahrain outage with a config value in front of it.

    **`min` is the only replica number that is a decision.** Traded against cold start: under five
    seconds to ready means autoscaling can respond inside a burst, and above it the floor absorbs
    what the autoscaler cannot reach in time.

    **`expectedAt` is arithmetic, not a limit.** It says what the target load implies at the
    declared trigger, so somebody sizing a database or a connection pool has a number — and it
    carries no authority to stop the autoscaler above it.

    **The real constraint is not a replica count at all.** `acquireInventoryHold` serialises; above
    some number more replicas are more waiters on one lock. **That is a property of the contention
    model, and a static ceiling cannot express it** — only `tools/bench.py` can find it, and the
    answer will be a throughput number rather than a replica number.
    """
    per = RPS_PER_REPLICA.get(name, 400)
    peak = math.ceil(TARGET_RPS * (share / 100) / per)
    floor = max(ABSOLUTE_MIN[name], peak)
    return {
        # **The floor is the expected peak, not a resting minimum.** Provisioned during `warming`,
        # before the sale opens, because the opening seconds are the peak rather than a ramp.
        "min": floor,
        "max": None,
        "maxNote": (
            "**No ceiling, deliberately.** A cap is a cap on absorbing a peak nobody predicted, "
            "and the peak is the whole reason this environment exists. 60,000 seats over two "
            "hours is 1,045 RPS; the same sale in twenty minutes is 6,270."),
        "floorIsPeak": True,
        "derivedFrom": f"{share}% of {TARGET_RPS} RPS at {per} RPS per replica",
        "absoluteMin": ABSOLUTE_MIN[name],
        "connectionsAtFloor": floor * POOL_MAX_PER_REPLICA,
        "poolerCapacity": PGBOUNCER_MAX_CLIENT_CONN,
        "realConstraint": (
            "Lease contention on acquireInventoryHold, not replica count. Measure it with "
            "tools/bench.py --pattern hot-venue."),
    }


def burst_operations(lin: dict) -> set[str]:
    ops: set[str] = set()
    for fid in BURST_FLOWS:
        for f in glob.glob(str(ROOT / "flows" / f"{fid}-*.yaml")):
            doc = yaml.safe_load(Path(f).read_text(encoding="utf-8")) or {}
            for step in (doc.get("steps") or []):
                ops |= set(step.get("operations") or [])
    return {o for o in (ops | DISCOVERY) if o in lin}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    H = ROOT / "handoff"
    lin = json.loads((H / "api-data-lineage.json").read_text(encoding="utf-8"))
    sch = json.loads((H / "schema-reference.json").read_text(encoding="utf-8"))
    dec = json.loads((H / "service-decomposition.json").read_text(encoding="utf-8"))["services"]

    ops = burst_operations(lin)
    weight: Counter = Counter()
    for o in ops:
        weight[lin[o].get("service")] += CALLS_PER_BUYER.get(o, 1)
    total = sum(weight.values()) or 1

    services = []
    for name, meta in dec.items():
        w = weight.get(name, 0)
        share = round(100 * w / total, 1)
        deployed = name in ABSOLUTE_MIN
        services.append({
            "name": name, "tier": meta["tier"],
            "onBurstPath": bool(w), "weightedShare": share, "deployed": deployed,
            "replicas": replicas_for(name, share) if deployed else None,
            "reason": (
                "carries the burst — replicates on RPS"
                if deployed and share >= REPLICATE_THRESHOLD else
                "required for every purchase, small but not optional"
                if deployed else
                "on the path but not the load — served from the shared cell"
                if w else
                "no part of a ticket sale — not deployed"),
        })

    tables = []
    for t in sorted({x for o in ops for x in lin[o]["reads"] + lin[o]["writes"]
                     if "." in x and ":" not in x}):
        touching = [o for o in ops if t in lin[o]["reads"] + lin[o]["writes"]]
        written = [o for o in ops if t in lin[o]["writes"]]
        note = str((sch.get("storage") or {}).get(t) or "").split(". **Hangs off**")[0].strip()
        tables.append({
            "table": t, "schema": t.split(".")[0],
            "columns": len(sch["cols"].get(t, [])),
            "burstOperations": len(touching), "written": bool(written),
            # **`contended: true` was the wrong shape of field and it produced a board showing two
            # red bars where there is one wall.**
            #
            # **Contention is not a property of a table.** It is a property of row cardinality
            # times access distribution, and `seating.seat_hold` has three modes:
            #
            # **single_row** - one counter per (performance, ticket type). Every buyer hits the
            # same row. `catalogue.inventory_hold` is this, and it is the wall.
            #
            # **per_entity** - 43,693 seat rows, a guest picking a specific one. Hot-spotted on
            # premium seats and **structurally not contended**.
            #
            # **allocator_serialised** - "best available", where the row count looks fine and
            # everyone races the same top-of-order seat. **This is the mode nobody models**, and
            # it is worse than single_row: a `SELECT ... WHERE status='free' ORDER BY rank LIMIT 1
            # FOR UPDATE` burns lock acquisitions on losers that retry, so effective throughput
            # lands *below* the single-row ceiling rather than at it.
            #
            # **`seating.seat_hold` may legitimately be both, per event configuration** - a venue
            # offering seat selection and best-available on the same performance is running two
            # modes against one table. That is worth knowing before the next infra session.
            "contention": CONTENTION_MODEL.get(t),
            # **Worst case when the model is unpinned.** A table that could be
            # `allocator_serialised` is treated as contended until the event configuration says
            # otherwise — **failing open here is how a board comes to show one bar where there
            # are two**, and the second one is the worse of them.
            "contended": bool(
                CONTENDED_MODES & set((CONTENTION_MODEL.get(t) or {}).get("modes", []))),
            "contentionIndeterminate": (
                (CONTENTION_MODEL.get(t) or {}).get("ceilingSource") == "worst_case_unless_pinned"),
            "note": note[:220],
        })

    operations = []
    for o in sorted(ops):
        v = lin[o]
        operations.append({
            "operationId": o, "verb": v["verb"], "path": v["path"],
            "service": v.get("service"), "contract": v["contract"],
            "callsPerBuyer": CALLS_PER_BUYER.get(o, 1),
            "reads": [t for t in v["reads"] if "." in t and ":" not in t],
            "writes": [t for t in v["writes"] if "." in t and ":" not in t],
            "lock": ("FOR UPDATE SKIP LOCKED" if o == "acquireInventoryHold"
                     else "FOR UPDATE" if o == "createSeatHold" else None),
        })

    real_tables = len([t for t in sch["cols"] if "." in t and ":" not in t])

    # **Two paths run at the same time and share nothing but the reconciliation.** A stadium on a
    # routine Saturday is 48.5 RPS across all sixteen services in the shared cell — food, access,
    # retail, staff back-office. **The venue's ordinary traffic never enters the burst
    # environment**, and presenting the burst set alone reads as though it were the platform.
    all_ops = len(lin)
    burst_ids = {o["operationId"] for o in operations}
    routing = {
        "note": (
            "**Normal traffic and sale traffic are separate systems running concurrently.** The "
            "burst environment carries the on-sale and nothing else; everything a venue does that "
            "day continues in the shared cell. **They meet once, afterwards, at reconciliation.**"),
        "paths": [
            {
                "name": "normal",
                "target": "shared cell",
                "services": len(dec),
                "operations": all_ops - len(burst_ids),
                "tables": real_tables,
                "exampleLoad": "stadium, routine Saturday: 60,000 guests x 14 requests = 48.5 RPS",
                "description": (
                    "**Everything except the sale.** Admission, food, retail, stock, staff "
                    "back-office, reporting. Runs whether or not a sale is happening."),
            },
            {
                "name": "sale",
                "target": "burst environment",
                "services": sum(1 for x in services if x["deployed"]),
                "operations": len(burst_ids),
                "tables": len(tables),
                "exampleLoad": "same stadium on-sale: 1.25M requests in 2h = 1,045 RPS at a 6x "
                               "burst; compressed to 20 minutes, 6,270",
                "description": (
                    "**The on-sale only.** Provisioned before it opens, torn down after, and "
                    "**its orders reconcile back into the shared cell** (ADR-0035) — which is the "
                    "single point the two paths touch."),
            },
        ],
        "meetingPoint": {
            "operation": "reconcileBurstEnvironment",
            "mechanism": "environment id, monotonic sequence, idempotent replay, sync.rejection",
            "note": (
                "**The same three properties as `syncOrders` one layer up.** A till's offline "
                "journal and a burst environment's order log are the same problem at different "
                "scale."),
        },
    }
    out = {
        "generatedBy": "tools/derive-burst-scope.py",
        "basis": f"flows {', '.join(BURST_FLOWS)} plus the discovery path",
        "note": (
            "**What a flash-sale environment runs, derived rather than chosen.** Weighted by how "
            "many times a single buyer calls each operation — two services carry most of the load "
            "and everything else is on the path without being the load.\n\n"
            "**Services with `deployed: false` are shown deliberately.** A viewer that shows what "
            "is absent is more useful than one showing only what is present, and the absence is "
            "the point: six services see no part of a ticket sale."),
        "totals": {
            "services": len(services),
            "deployed": sum(1 for s in services if s["deployed"]),
            "operations": len(operations), "ofTotalOperations": len(lin),
            "tables": len(tables), "ofTotalTables": real_tables,
        },
        "routing": routing,
        "services": sorted(services, key=lambda x: -x["weightedShare"]),
        "tables": sorted(tables, key=lambda x: -x["burstOperations"]),
        "operations": sorted(operations, key=lambda x: -x["callsPerBuyer"]),
    }

    if a.apply:
        (H / "burst-scope.json").write_text(
            json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    t = out["totals"]
    print(f"  {t['deployed']} of {t['services']} services deployed · "
          f"{t['operations']} of {t['ofTotalOperations']} operations · "
          f"{t['tables']} of {t['ofTotalTables']} tables")
    if not a.apply:
        print("  nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
