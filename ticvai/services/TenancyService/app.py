"""TenancyService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

52 operations · 36 tables touched · scope levels: brand, region, tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="TenancyService", docs_url="/_docs")

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
    return {"service": "TenancyService", "operations": 52,
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



@app.post("/announcements/{announcementId}/acknowledge")
async def acknowledge_announcement(request: Request) -> dict:
    """Confirm you have read it

    scope: venue · permission: WORKFORCE_VIEW · offline: True
    """
    return await run("acknowledgeAnnouncement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/attendance/{recordId}/amend")
async def amend_attendance(request: Request) -> dict:
    """A supervisor corrects a record

    scope: venue · permission: WORKFORCE_MANAGE · offline: False
    """
    return await run("amendAttendance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guest-broadcast")
async def broadcast_to_guests(request: Request) -> dict:
    """broadcastToGuests

    scope: venue · permission: ANNOUNCEMENT_PUBLISH · offline: False
    """
    return await run("broadcastToGuests", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/workstations/{workstationId}")
async def configure_workstation(request: Request) -> dict:
    """Configure a workstation

    scope: venue · permission: WORKSTATION_CONFIGURE · offline: False
    """
    return await run("configureWorkstation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/delegations")
async def create_approval_delegation(request: Request) -> dict:
    """Delegate approval authority

    scope: venue · permission: APPROVAL_DECIDE · offline: False
    """
    return await run("createApprovalDelegation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/approval-requests")
async def create_approval_request(request: Request) -> dict:
    """Raise a request

    scope: venue · permission: APPROVAL_REQUEST · offline: False
    """
    return await run("createApprovalRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/org-units")
async def create_org_unit(request: Request) -> dict:
    """Create a scope node

    scope: brand · permission: SCOPE_MANAGE · offline: False
    """
    return await run("createOrgUnit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/outlets")
async def create_outlet(request: Request) -> dict:
    """Create an outlet

    scope: venue · permission: REGION_CONFIGURE · offline: False
    """
    return await run("createOutlet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/rota-assignments")
async def create_rota_assignment(request: Request) -> dict:
    """Put someone on the rota

    scope: venue · permission: WORKFORCE_MANAGE · offline: False
    """
    return await run("createRotaAssignment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/sale-boards")
async def create_sale_board(request: Request) -> dict:
    """Create a sale board

    scope: venue · permission: WORKSTATION_CONFIGURE · offline: False
    """
    return await run("createSaleBoard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/approval-requests/{requestId}/decide")
async def decide_approval_request(request: Request) -> dict:
    """Approve or reject

    scope: venue · permission: APPROVAL_DECIDE · offline: False
    """
    return await run("decideApprovalRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/configuration-profiles/{profileId}/deploy")
async def deploy_configuration_profile(request: Request) -> dict:
    """deployConfigurationProfile

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("deployConfigurationProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/approval-requests/{requestId}/escalate")
async def escalate_approval_request(request: Request) -> dict:
    """Move it up a level

    scope: venue · permission: APPROVAL_REQUEST · offline: False
    """
    return await run("escalateApprovalRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/approval-requests/evaluate")
async def evaluate_approval_requirement(request: Request) -> dict:
    """Does this need approval, and from whom

    scope: venue · permission: APPROVAL_VIEW · offline: False
    """
    return await run("evaluateApprovalRequirement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/announcements/{announcementId}/reach")
async def get_announcement_reach(request: Request) -> dict:
    """Who has acknowledged, and who has not

    scope: venue · permission: WORKFORCE_VIEW · offline: False
    """
    return await run("getAnnouncementReach", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/approval-analytics")
async def get_approval_analytics(request: Request) -> dict:
    """Volumes, times, rejections and bottlenecks

    scope: venue · permission: APPROVAL_VIEW · offline: False
    """
    return await run("getApprovalAnalytics", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/org-units/{orgUnitId}")
async def get_org_unit(request: Request) -> dict:
    """Read a scope node

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("getOrgUnit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/regions/{regionId}/settings")
async def get_region_settings(request: Request) -> dict:
    """Read region settings

    scope: region · permission: SCOPE_VIEW · offline: True
    """
    return await run("getRegionSettings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venues/{venueId}/settings")
async def get_venue_settings(request: Request) -> dict:
    """Operational settings for this venue

    scope: venue · permission: TENANT_VIEW · offline: True
    """
    return await run("getVenueSettings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/workstations/{workstationId}")
async def get_workstation(request: Request) -> dict:
    """Read a workstation

    scope: workstation · permission: SCOPE_VIEW · offline: True
    """
    return await run("getWorkstation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/workstations/{workstationId}/health")
async def get_workstation_health(request: Request) -> dict:
    """getWorkstationHealth

    scope: tenant · permission: DEVICE_VIEW · offline: False
    """
    return await run("getWorkstationHealth", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/announcements")
async def list_announcements(request: Request) -> dict:
    """What staff have been told

    scope: venue · permission: WORKFORCE_VIEW · offline: True
    """
    return await run("listAnnouncements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/delegations")
async def list_approval_delegations(request: Request) -> dict:
    """Who is standing in for whom

    scope: venue · permission: APPROVAL_VIEW · offline: False
    """
    return await run("listApprovalDelegations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/approval-matrices")
async def list_approval_matrices(request: Request) -> dict:
    """What requires approval here

    scope: venue · permission: APPROVAL_CONFIGURE · offline: False
    """
    return await run("listApprovalMatrices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/approval-requests")
async def list_approval_requests(request: Request) -> dict:
    """Requests awaiting a decision, or already decided

    scope: venue · permission: APPROVAL_VIEW · offline: False
    """
    return await run("listApprovalRequests", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/attendance")
async def list_attendance(request: Request) -> dict:
    """Who was here

    scope: venue · permission: WORKFORCE_VIEW · offline: False
    """
    return await run("listAttendance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/audit-records")
async def list_audit_records(request: Request) -> dict:
    """Who did what, where, and when

    scope: venue · permission: AI_AUDIT_VIEW · offline: False
    """
    return await run("listAuditRecords", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/devices")
async def list_devices(request: Request) -> dict:
    """List registered devices

    scope: venue · permission: DEVICE_VIEW · offline: True
    """
    return await run("listDevices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/org-units")
async def list_org_units(request: Request) -> dict:
    """List scope nodes visible to the session

    scope: tenant · permission: SCOPE_VIEW · offline: False
    """
    return await run("listOrgUnits", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/outlets")
async def list_outlets(request: Request) -> dict:
    """List outlets

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listOutlets", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/rota-assignments")
async def list_rota_assignments(request: Request) -> dict:
    """The rota

    scope: venue · permission: WORKFORCE_VIEW · offline: True
    """
    return await run("listRotaAssignments", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/sale-boards")
async def list_sale_boards(request: Request) -> dict:
    """List sale boards

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listSaleBoards", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/workstations")
async def list_workstations(request: Request) -> dict:
    """List workstations

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listWorkstations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/announcements")
async def publish_announcement(request: Request) -> dict:
    """Tell staff something

    scope: venue · permission: ANNOUNCEMENT_PUBLISH · offline: False
    """
    return await run("publishAnnouncement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/attendance/clock")
async def record_attendance(request: Request) -> dict:
    """Clock in, clock out, or take a break

    scope: venue · permission: ATTENDANCE_RECORD · offline: True
    """
    return await run("recordAttendance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/devices/{deviceId}/heartbeat")
async def record_device_heartbeat(request: Request) -> dict:
    """Device heartbeat and status

    scope: workstation · permission: - · offline: False
    """
    return await run("recordDeviceHeartbeat", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/devices")
async def register_device(request: Request) -> dict:
    """Register a device

    scope: venue · permission: DEVICE_CONFIGURE · offline: False
    """
    return await run("registerDevice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/rota-assignments/{assignmentId}/swap")
async def request_shift_swap(request: Request) -> dict:
    """Ask someone to take your shift

    scope: venue · permission: WORKFORCE_VIEW · offline: False
    """
    return await run("requestShiftSwap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/approval-requests/{requestId}/resubmit")
async def resubmit_approval_request(request: Request) -> dict:
    """Amend a rejected request and try again

    scope: venue · permission: APPROVAL_REQUEST · offline: False
    """
    return await run("resubmitApprovalRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/delegations/{delegationId}")
async def revoke_approval_delegation(request: Request) -> dict:
    """End a delegation early

    scope: venue · permission: APPROVAL_DECIDE · offline: False
    """
    return await run("revokeApprovalDelegation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/approval-matrices")
async def set_approval_matrix(request: Request) -> dict:
    """Configure what requires approval

    scope: venue · permission: APPROVAL_CONFIGURE · offline: False
    """
    return await run("setApprovalMatrix", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/configuration-profiles")
async def set_configuration_profile(request: Request) -> dict:
    """setConfigurationProfile

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setConfigurationProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/connectivity-policy")
async def set_connectivity_thresholds(request: Request) -> dict:
    """setConnectivityThresholds

    scope: venue · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setConnectivityThresholds", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/offline-policy")
async def set_offline_policy(request: Request) -> dict:
    """setOfflinePolicy

    scope: venue · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setOfflinePolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/roles/{roleId}/permissions")
async def set_role_permissions(request: Request) -> dict:
    """What this role may do

    scope: tenant · permission: ROLE_MANAGE · offline: False
    """
    return await run("setRolePermissions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/venues/{venueId}/settings")
async def set_venue_settings(request: Request) -> dict:
    """Set support hours, quiet hours, segregated access and alerting

    scope: venue · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setVenueSettings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/org-units/{orgUnitId}")
async def update_org_unit(request: Request) -> dict:
    """Rename or deactivate a scope node

    scope: brand · permission: SCOPE_MANAGE · offline: False
    """
    return await run("updateOrgUnit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/outlets/{outletId}")
async def update_outlet(request: Request) -> dict:
    """Amend an outlet

    scope: venue · permission: REGION_CONFIGURE · offline: False
    """
    return await run("updateOutlet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/regions/{regionId}/settings")
async def update_region_settings(request: Request) -> dict:
    """Update region settings

    scope: region · permission: REGION_CONFIGURE · offline: False
    """
    return await run("updateRegionSettings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/rota-assignments/{assignmentId}")
async def update_rota_assignment(request: Request) -> dict:
    """Move or cancel an assignment

    scope: venue · permission: WORKFORCE_MANAGE · offline: False
    """
    return await run("updateRotaAssignment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/sale-boards/{saleBoardId}")
async def update_sale_board(request: Request) -> dict:
    """Update a sale board

    scope: venue · permission: WORKSTATION_CONFIGURE · offline: False
    """
    return await run("updateSaleBoard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/approval-requests/{requestId}/withdraw")
async def withdraw_approval_request(request: Request) -> dict:
    """The requester takes it back

    scope: venue · permission: APPROVAL_REQUEST · offline: False
    """
    return await run("withdrawApprovalRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

