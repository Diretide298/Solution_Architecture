"""AccessService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

31 operations · 20 tables touched · scope levels: tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="AccessService", docs_url="/_docs")

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
    return {"service": "AccessService", "operations": 31,
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



@app.post("/blacklist")
async def add_blacklist_entry(request: Request) -> dict:
    """Blacklist a media code

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("addBlacklistEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access-points")
async def create_access_point(request: Request) -> dict:
    """Create an access point

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("createAccessPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/admission-rules")
async def create_admission_rules(request: Request) -> dict:
    """Create an admission profile

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("createAdmissionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/parking-entitlements")
async def create_parking_entitlement(request: Request) -> dict:
    """A guest bought parking

    scope: venue · permission: - · offline: False
    """
    return await run("createParkingEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/face-pass/enrolments")
async def enrol_face_pass(request: Request) -> dict:
    """Register a facial profile against an entitlement

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("enrolFacePass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-points/{accessPointId}")
async def get_access_point(request: Request) -> dict:
    """Read an access point

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("getAccessPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlements/{entitlementId}")
async def get_entitlement(request: Request) -> dict:
    """One entitlement, with what remains on it

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlements/{entitlementId}/credential")
async def get_entitlement_credential(request: Request) -> dict:
    """The thing that gets scanned

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getEntitlementCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlements/{entitlementId}/history")
async def get_entitlement_history(request: Request) -> dict:
    """Every scan, freeze, share and reissue against it

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getEntitlementHistory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/face-pass/enrolments/{enrolmentId}")
async def get_face_pass_enrolment(request: Request) -> dict:
    """Whether a pass has a face registered, and when

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getFacePassEnrolment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access/offline-package")
async def get_offline_package(request: Request) -> dict:
    """Entitlement and rule set for offline validation

    scope: workstation · permission: ACCESS_VALIDATE · offline: False
    """
    return await run("getOfflinePackage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-points")
async def list_access_points(request: Request) -> dict:
    """List access points

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listAccessPoints", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/admission-rules")
async def list_admission_rules(request: Request) -> dict:
    """List admission profiles

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listAdmissionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/blacklist")
async def list_blacklist(request: Request) -> dict:
    """List blacklisted media

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listBlacklist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/my/entitlements/all")
async def list_entitlements(request: Request) -> dict:
    """Every entitlement this guest holds, including expired

    scope: tenant · permission: - · offline: False
    """
    return await run("listEntitlements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/me/entitlements")
async def list_my_entitlements(request: Request) -> dict:
    """Every ticket, pass and membership this guest holds

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("listMyEntitlements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/parking-facilities")
async def list_parking_facilities(request: Request) -> dict:
    """Car parks at a venue, and how each integrates

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: True
    """
    return await run("listParkingFacilities", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access/scans")
async def list_scans(request: Request) -> dict:
    """List scan events

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listScans", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access/lookup")
async def lookup_ticket(request: Request) -> dict:
    """Read-only validity check without admitting

    scope: venue · permission: TICKET_LOOKUP · offline: True
    """
    return await run("lookupTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/override")
async def override_access(request: Request) -> dict:
    """Admit against a failed validation

    scope: venue · permission: ACCESS_OVERRIDE · offline: True
    """
    return await run("overrideAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/blacklist/{mediaCode}")
async def remove_blacklist_entry(request: Request) -> dict:
    """Remove a blacklist entry

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("removeBlacklistEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/face-pass/enrolments/{enrolmentId}")
async def revoke_face_pass(request: Request) -> dict:
    """Remove a facial profile

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("revokeFacePass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/access-points/{accessPointId}/geofence")
async def set_access_point_geofence(request: Request) -> dict:
    """Set a geofence for handheld validation

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setAccessPointGeofence", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/parking-facilities")
async def set_parking_facility(request: Request) -> dict:
    """Configure a car park and its integration

    scope: venue · permission: PARKING_CONFIGURE · offline: False
    """
    return await run("setParkingFacility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/access-points/{accessPointId}/mode")
async def set_turnstile_mode(request: Request) -> dict:
    """Set the operating mode of an access point

    scope: venue · permission: TURNSTILE_MODE_SET · offline: True
    """
    return await run("setTurnstileMode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/scans")
async def sync_scans(request: Request) -> dict:
    """Replay scans recorded offline

    scope: workstation · permission: ACCESS_VALIDATE · offline: False
    """
    return await run("syncScans", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/access-points/{accessPointId}")
async def update_access_point(request: Request) -> dict:
    """Update an access point

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("updateAccessPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/admission-rules/{profileId}")
async def update_admission_rules(request: Request) -> dict:
    """Update an admission profile

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("updateAdmissionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/parking-entitlements/{entitlementId}")
async def update_parking_entitlement(request: Request) -> dict:
    """Change the plate, or revoke

    scope: venue · permission: - · offline: False
    """
    return await run("updateParkingEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/validate")
async def validate_access(request: Request) -> dict:
    """Validate media at an access point and admit or deny

    scope: workstation · permission: ACCESS_VALIDATE · offline: True
    """
    return await run("validateAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/group-validate")
async def validate_group_access(request: Request) -> dict:
    """Admit a group on one read

    scope: workstation · permission: ACCESS_VALIDATE · offline: True
    """
    return await run("validateGroupAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

