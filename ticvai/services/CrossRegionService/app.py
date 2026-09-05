"""CrossRegionService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

16 operations · 5 tables touched · scope levels: region, tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="CrossRegionService", docs_url="/_docs")

# **Pool size is the number the benchmark is for.** A per-venue topology multiplies this by the
# venue count against one primary; a shared topology does not. Set it from the environment so the
# same image runs in all three.
POOL_MIN = int(os.getenv("PG_POOL_MIN", "2"))
POOL_MAX = int(os.getenv("PG_POOL_MAX", "10"))
REDIS = os.getenv("REDIS_URL", "redis://redis:6379/0")

# **One service, many tenant databases** (ADR-0038). The instance is the region and the database
# is the tenant, so a service is not deployed per tenant — it is shared, scaled on traffic, and
# routed per request to a tenant database by tenant id.
#
# **Which makes the pool numbers above per tenant rather than per service**, and that is the whole
# of ADR-0032's amendment: `PG_POOL_MAX` of 20 across 25 concurrent tenants is 500 server
# connections, which is `max_connections` exactly. The benchmark measures this on purpose.
CONTROL_DSN = os.getenv("PG_CONTROL_DSN", "postgres://ticvai:ticvai@pgbouncer:6432/control")
TENANT_DSN = os.getenv("PG_TENANT_DSN_TEMPLATE",
                       "postgres://ticvai:ticvai@pgbouncer:6432/{database}")
TENANT_HEADER = os.getenv("TENANT_HEADER", "x-ticvai-tenant")

# **A request with no tenant is a bug, not a default** — except in the benchmark, which drives
# every operation without an authenticated caller. Named so the fallback is visible in the logs
# rather than looking like a tenant.
DEFAULT_TENANT = os.getenv("DEFAULT_TENANT", "")

class _Rollback(Exception):
    """Raised to undo a benchmark write. **Never escapes `run`.**"""


# **A pool per tenant database, made on first use and kept.** Sixteen services times two
# hundred tenants is not a connection budget anybody has, so the pool is opened when a tenant
# first arrives and the size is what `PG_POOL_MIN/MAX` say. This is the cost ADR-0038 accepted
# and it belongs in the artefact rather than in the ADR alone.
control_pool: asyncpg.Pool | None = None
pools: dict[str, asyncpg.Pool] = {}
databases: dict[str, str] = {}
cache = None


async def database_for(tenant: str) -> str:
    """The tenant's database name in this cell, from `control.cell_tenant`.

    **The control plane is asked, not the name guessed.** ADR-0039 keeps the mapping in a table
    precisely so a tenant can be moved, suspended or renamed without every service agreeing on a
    naming convention first.
    """
    if tenant in databases:
        return databases[tenant]
    async with control_pool.acquire() as con:
        row = await con.fetchrow(
            "SELECT database_name FROM control.cell_tenant "
            " WHERE tenant_id = $1 AND status = 'live' LIMIT 1", tenant)
    # **No row is not the same as no database.** A tenant the control plane does not place here
    # is a tenant in another region, and answering from a fallback would read that region's
    # request against this region's data.
    if not row:
        raise KeyError(tenant)
    databases[tenant] = row["database_name"]
    return databases[tenant]


async def pool_for(tenant: str) -> asyncpg.Pool:
    if tenant not in pools:
        dsn = TENANT_DSN.format(database=await database_for(tenant))
        pools[tenant] = await asyncpg.create_pool(dsn, min_size=POOL_MIN, max_size=POOL_MAX)
    return pools[tenant]


@app.on_event("startup")
async def _start() -> None:
    global control_pool, cache
    # **Cold start is one of the twenty metrics.** Timed here rather than inferred from the
    # orchestrator, because a pool that fills lazily makes the first request the slow one and the
    # container look healthy.
    #
    # **Only the control pool is opened at startup.** A tenant pool is opened on that tenant's
    # first request, so cold start is now a per-tenant number as well as a per-container one —
    # which is a real consequence of ADR-0038 and worth measuring rather than hiding.
    t0 = time.perf_counter()
    control_pool = await asyncpg.create_pool(CONTROL_DSN, min_size=1, max_size=4)
    cache = aioredis.from_url(REDIS, decode_responses=True)
    app.state.cold_start_ms = round((time.perf_counter() - t0) * 1000, 1)


@app.get("/_health")
async def health() -> dict:
    # **Reported per tenant and in total.** One number across every tenant database is the
    # number that made `max_connections` look comfortable while a Saturday evening was not.
    return {"service": "CrossRegionService", "operations": 16,
            "coldStartMs": getattr(app.state, "cold_start_ms", None),
            "tenantPools": len(pools),
            "poolSize": sum(p.get_size() for p in pools.values()),
            "poolIdle": sum(p.get_idle_size() for p in pools.values()),
            "controlPoolSize": control_pool.get_size() if control_pool else 0}


async def run(op: str, scope: str | None, tenant: str | None = None) -> dict:
    """Execute one operation's declared database work, against one tenant's database.

    **Scope is passed as a parameter, not as a deployment.** A venue-scoped operation filters on
    `scope_path`; that is true whether the service is shared or per-venue, and it is the whole
    point of the comparison.

    **Tenant is a connection, not a parameter.** ADR-0038 put a database around each tenant, so
    the query does not filter on `tenant_id` inside a tenant database — a column that says which
    tenant you are while you are inside that tenant's database is a column that will eventually
    disagree with the database it is in.
    """
    t0 = time.perf_counter()
    rows = 0
    pool = await pool_for(tenant or DEFAULT_TENANT)
    async with pool.acquire() as con:
        for sql in READS.get(op, ()):
            rows += len(await con.fetch(sql, *( (scope + "%",) if "$1" in sql else () )))
        # **Wrapped in a transaction that always rolls back.** A benchmark that leaves rows
        # changes the table it is measuring against, so the second run is not the first. The
        # assignment that used to sit here — `raise_rollback = True` — did nothing: asyncpg
        # commits unless the block raises, so every write was being kept.
        if WRITES.get(op):
            try:
                async with con.transaction():
                    for sql in WRITES[op]:
                        await con.fetch(sql, *( (scope + "%",) if "$1" in sql else () ))
                    raise _Rollback()
            except _Rollback:
                pass
    for key in CACHE.get(op, ()):
        await cache.get(key)
    return {"op": op, "rows": rows, "ms": round((time.perf_counter() - t0) * 1000, 2)}



@app.post("/wallet-authorisations")
async def authorise_wallet_spend(request: Request) -> dict:
    """Hold funds against the guest's home-cell balance

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("authoriseWalletSpend", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallet-authorisations/{authorisationId}/capture")
async def capture_wallet_authorisation(request: Request) -> dict:
    """Capture a held amount

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("captureWalletAuthorisation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cross-region-entitlements/{rightId}/consume")
async def consume_cross_region_entitlement(request: Request) -> dict:
    """Consume entries against a right, locally authoritative

    scope: workstation · permission: ACCESS_VALIDATE · offline: True
    """
    return await run("consumeCrossRegionEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/dsar/requests")
async def create_dsar_request(request: Request) -> dict:
    """Raise a data subject request across every linked cell

    scope: tenant · permission: - · offline: False
    """
    return await run("createDsarRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guest-links")
async def create_guest_link(request: Request) -> dict:
    """Link a guest's records across cells

    scope: tenant · permission: - · offline: False
    """
    return await run("createGuestLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cross-region-entitlements/{rightId}")
async def get_cross_region_entitlement(request: Request) -> dict:
    """Read a redemption right

    scope: venue · permission: TICKET_LOOKUP · offline: True
    """
    return await run("getCrossRegionEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dsar/requests/{requestId}")
async def get_dsar_request(request: Request) -> dict:
    """Track fan-out progress per cell

    scope: tenant · permission: - · offline: False
    """
    return await run("getDsarRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest-links/{guestLinkId}")
async def get_guest_link(request: Request) -> dict:
    """Read a guest link

    scope: tenant · permission: - · offline: False
    """
    return await run("getGuestLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/wallet-allocations")
async def get_wallet_allocation(request: Request) -> dict:
    """The consuming cell's bounded offline allocation

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getWalletAllocation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cross-region-entitlements")
async def propagate_cross_region_entitlement(request: Request) -> dict:
    """Propagate a right from the issuing cell to a consuming cell

    scope: tenant · permission: - · offline: False
    """
    return await run("propagateCrossRegionEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cross-region-entitlements/reconcile")
async def reconcile_redemptions(request: Request) -> dict:
    """Report consumption back to the issuing cell

    scope: tenant · permission: - · offline: False
    """
    return await run("reconcileRedemptions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallet-authorisations/{authorisationId}/release")
async def release_wallet_authorisation(request: Request) -> dict:
    """Release a hold without capturing

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("releaseWalletAuthorisation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest-links/resolve")
async def resolve_guest_link(request: Request) -> dict:
    """Find the link for a local subject

    scope: tenant · permission: - · offline: False
    """
    return await run("resolveGuestLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/cross-region-entitlements/{rightId}")
async def revoke_cross_region_entitlement(request: Request) -> dict:
    """Revoke a right

    scope: tenant · permission: - · offline: False
    """
    return await run("revokeCrossRegionEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/guest-links/{guestLinkId}")
async def revoke_guest_link(request: Request) -> dict:
    """Sever a link on consent withdrawal

    scope: tenant · permission: - · offline: False
    """
    return await run("revokeGuestLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/wallet-allocations")
async def set_wallet_allocation_policy(request: Request) -> dict:
    """Set the allocation cap policy

    scope: region · permission: REGION_CONFIGURE · offline: False
    """
    return await run("setWalletAllocationPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

