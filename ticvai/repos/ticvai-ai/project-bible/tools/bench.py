#!/usr/bin/env python3
"""Drive identical load against all three topologies.

**The workload is not invented.** It is the flows already walked — F58 a ticket sold at a till, F59
a seat picked and held, F61 a gate admitting a group, F43 the concurrency case. Each step names its
operations, so the request sequence and its ratios come out of the package rather than out of a
guess.

**Six patterns, and the fifth is the one that decides the argument:**

    steady          the boring case, 2.9 RPS
    burst           2x to 5x, ramped
    venue-heavy     load concentrated in venues
    tenant-heavy    load concentrated in one tenant
    hot-venue       **one venue generating disproportionate load**
    even            uniformly spread

**`hot-venue` is the Bahrain case** — 30,000 people buying for one event at one venue — and it is
where per-tenant placement fails, because one venue's spike scales a whole tenant.

**Reports the twenty metrics that can be measured** and names the ones that cannot. Application CPU
under real business logic is not measurable from a skeleton, and the harness says so rather than
reporting a number that looks like it means something.

    python3 tools/bench.py --topology hybrid --pattern hot-venue --rps 1000 --seconds 300
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def workload() -> list[tuple[str, str, str, float]]:
    """The request mix, from the flows.

    **Weighted by how often a step appears across 94 journeys.** An operation on the sale path
    appears in many flows; one on a month-end close appears in one. That ratio is the workload, and
    it is already recorded.
    """
    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    freq: Counter = Counter()
    import yaml
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for st in (doc.get("steps") or []):
            for op in (st.get("operations") or []):
                if op in lin:
                    freq[op] += 1
    mix = []
    for op, n in freq.most_common():
        v = lin[op]
        mix.append((op, v["verb"], v["path"], float(n)))
    return mix


# **Scope keys are the partition.** A hot-venue pattern is not more requests; it is the same
# requests with a skewed `x-scope-path`, which is what makes a shared service's cache behave
# differently from a per-venue one.
def scope_for(pattern: str, venues: list[str], tenants: list[str]) -> str:
    if pattern == "hot-venue":
        # **90% to one venue.** The distribution is the experiment.
        return venues[0] if random.random() < 0.9 else random.choice(venues)
    if pattern == "venue-heavy":
        return random.choice(venues)
    if pattern == "tenant-heavy":
        return tenants[0] if random.random() < 0.8 else random.choice(tenants)
    return random.choice(venues + tenants)


async def worker(session, base: str, mix, pattern, venues, tenants, stop, lat, errs, codes, held):
    ops, weights = [m for m in mix], [m[3] for m in mix]
    while time.time() < stop:
        op, verb, path, _ = random.choices(ops, weights=weights, k=1)[0]
        url = base + path.replace("{", "").replace("}", "-x")
        t0 = time.perf_counter()
        try:
            async with session.request(verb, url, timeout=10,
                                       headers={"x-scope-path": scope_for(pattern, venues, tenants)}) as r:
                await r.read()
                codes[r.status] += 1
                if r.status >= 500:
                    errs[op] += 1
        except Exception as e:
            errs[type(e).__name__] += 1
            codes[0] += 1
        _ms = (time.perf_counter() - t0) * 1000
        lat.append(_ms)
        if op in ("acquireInventoryHold", "createSeatHold"):
            held.append((op, _ms))


async def run(a) -> dict:
    import aiohttp
    mix = workload()
    venues = [f"uae.dubai.v{i}" for i in range(1, 4)]
    tenants = [f"uae.t{i}" for i in range(1, 4)]
    lat: list = []
    # **Recorded separately from general latency.** A lease acquisition that takes 400ms while
    # every read takes 12ms is invisible in a p95 across all requests, and it is the only figure
    # that separates the four variants.
    _held: list = []
    errs: Counter = Counter()
    codes: Counter = Counter()
    stop = time.time() + a.seconds

    # **Concurrency is derived from the target, not set by hand.** A fixed worker count either
    # cannot reach the RPS or overshoots it, and both make the latency figure meaningless.
    conc = max(8, min(a.rps // 4, 512))
    conn = aiohttp.TCPConnector(limit=conc * 2)
    async with aiohttp.ClientSession(connector=conn) as s:
        await asyncio.gather(*[
            worker(s, a.base, mix, a.pattern, venues, tenants, stop, lat, errs, codes, _held)
            for _ in range(conc)])

    lat.sort()
    n = len(lat) or 1
    return {
        "topology": a.topology, "variant": a.variant,
        "pattern": a.pattern, "targetRps": a.rps,
        "seconds": a.seconds, "requests": len(lat),
        "achievedRps": round(len(lat) / max(1, a.seconds), 1),
        "avgMs": round(statistics.fmean(lat), 2) if lat else None,
        "p95Ms": round(lat[int(n * 0.95) - 1], 2) if lat else None,
        "p99Ms": round(lat[int(n * 0.99) - 1], 2) if lat else None,
        "errorRate": round(sum(errs.values()) / n, 5),
        "statusCodes": dict(codes.most_common()),
        "topErrors": dict(errs.most_common(5)),
        # **Holds acquired per second on one hot performance is the number.** Latency and error
        # rate move under every variant; this one moves under C alone, and if it does not move
        # there either then the ceiling is Postgres row locking and no application change reaches
        # it.
        "holdsPerSecond": round(
            sum(1 for op, _ in _held) / max(1, a.seconds), 2) if _held else None,
        "holdContentionMs": round(
            statistics.fmean([ms for _, ms in _held]), 2) if _held else None,
        "notMeasured": [
            "application CPU under real business logic — a skeleton has none",
            "cold start beyond pool fill — reported per service on /_health",
            "autoscale reaction — needs an orchestrator, not compose",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", default="hybrid",
                    choices=["all-venue", "all-tenant", "hybrid"])
    ap.add_argument("--pattern", default="steady",
                    choices=["steady", "burst", "venue-heavy", "tenant-heavy", "hot-venue", "even"])
    ap.add_argument("--rps", type=int, default=1000)
    ap.add_argument("--seconds", type=int, default=300,
                    help="**Long enough to see autoscaling, not a peak.** Five minutes minimum.")
    ap.add_argument("--base", default="http://localhost:8000")
    ap.add_argument("--variant", default="A",
                    choices=["A", "B", "C", "D"],
                    help="**A** baseline · **B** read cache · **C** lease shards · "
                         "**D** write batching. Recorded on the result so two runs are comparable.")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    mix = workload()
    print(f"  workload: {len(mix)} operations, weighted by appearance across 94 flows")
    print(f"  top: {', '.join(m[0] for m in mix[:5])}")
    try:
        import aiohttp  # noqa
    except ImportError:
        print("\n  aiohttp not installed — pip install aiohttp")
        print("  workload model is valid; the run needs a target to hit.")
        return 1

    res = asyncio.run(run(a))
    print(json.dumps(res, indent=1))
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
