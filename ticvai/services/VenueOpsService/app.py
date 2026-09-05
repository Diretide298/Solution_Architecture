"""VenueOpsService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

102 operations · 43 tables touched · scope levels: tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="VenueOpsService", docs_url="/_docs")

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
    return {"service": "VenueOpsService", "operations": 102,
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



@app.post("/venue-maps/{mapId}/proposals")
async def accept_venue_label_proposals(request: Request) -> dict:
    """Accept, edit or reject what the assistant suggested

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("acceptVenueLabelProposals", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps/{mapId}/walkway-proposals")
async def accept_walkway_proposals(request: Request) -> dict:
    """Accept or reject proposed walkways

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("acceptWalkwayProposals", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/accept")
async def accept_work_order(request: Request) -> dict:
    """The assignee takes the job

    scope: venue · permission: MAINTENANCE_EXECUTE · offline: True
    """
    return await run("acceptWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/game-cards/{cardCode}/adjust")
async def adjust_game_card(request: Request) -> dict:
    """Manually adjust credits or points

    scope: venue · permission: LEDGER_POST · offline: False
    """
    return await run("adjustGameCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/attachments")
async def attach_work_order_evidence(request: Request) -> dict:
    """Photo, video, document, note or signature

    scope: venue · permission: MAINTENANCE_EXECUTE · offline: True
    """
    return await run("attachWorkOrderEvidence", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/resource-bookings")
async def book_resource(request: Request) -> dict:
    """Reserve a specific resource for a window

    scope: venue · permission: RESOURCE_BOOK · offline: False
    """
    return await run("bookResource", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/queues/{queueId}/call-next")
async def call_next_parties(request: Request) -> dict:
    """Call the next parties forward

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("callNextParties", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/cancel")
async def cancel_work_order(request: Request) -> dict:
    """Cancel a work order

    scope: venue · permission: WORK_ORDER_MANAGE · offline: False
    """
    return await run("cancelWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/resource-bookings/{bookingId}/check-in")
async def check_in_resource(request: Request) -> dict:
    """Take it back, and settle the deposit

    scope: venue · permission: RESOURCE_BOOK · offline: True
    """
    return await run("checkInResource", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/resource-bookings/{bookingId}/check-out")
async def check_out_resource(request: Request) -> dict:
    """Hand it over, with a deposit against it

    scope: venue · permission: RESOURCE_BOOK · offline: True
    """
    return await run("checkOutResource", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/close")
async def close_work_order(request: Request) -> dict:
    """Administratively closed

    scope: venue · permission: MAINTENANCE_APPROVE · offline: False
    """
    return await run("closeWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/media/uploads/{uploadId}/complete")
async def complete_upload(request: Request) -> dict:
    """Confirm an upload and create the asset

    scope: venue · permission: ASSET_LIBRARY_MANAGE · offline: False
    """
    return await run("completeUpload", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/complete")
async def complete_work_order(request: Request) -> dict:
    """Complete a work order

    scope: venue · permission: WORK_ORDER_MANAGE · offline: True
    """
    return await run("completeWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/queue-feeds")
async def configure_queue_feed(request: Request) -> dict:
    """Configure a sensor feed

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("configureQueueFeed", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/assets")
async def create_asset(request: Request) -> dict:
    """Register an asset

    scope: venue · permission: ASSET_MANAGE · offline: False
    """
    return await run("createAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/media/collections")
async def create_collection(request: Request) -> dict:
    """Create a collection

    scope: venue · permission: ASSET_LIBRARY_MANAGE · offline: False
    """
    return await run("createCollection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/games")
async def create_game(request: Request) -> dict:
    """Register a game

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createGame", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inspection-templates")
async def create_inspection_template(request: Request) -> dict:
    """Create an inspection template

    scope: tenant · permission: INSPECTION_MANAGE · offline: False
    """
    return await run("createInspectionTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/maintenance-plans")
async def create_maintenance_plan(request: Request) -> dict:
    """Create a planned maintenance schedule

    scope: venue · permission: ASSET_MANAGE · offline: False
    """
    return await run("createMaintenancePlan", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/prizes")
async def create_prize(request: Request) -> dict:
    """Add a prize

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createPrize", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/queues")
async def create_queue(request: Request) -> dict:
    """Create a queue

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("createQueue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/resources")
async def create_resource(request: Request) -> dict:
    """Define a bookable resource

    scope: venue · permission: RESOURCE_MANAGE · offline: False
    """
    return await run("createResource", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/media/uploads")
async def create_upload(request: Request) -> dict:
    """Request a signed upload URL

    scope: venue · permission: ASSET_LIBRARY_MANAGE · offline: False
    """
    return await run("createUpload", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps")
async def create_venue_map(request: Request) -> dict:
    """Start a map

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("createVenueMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders")
async def create_work_order(request: Request) -> dict:
    """Raise a work order

    scope: venue · permission: WORK_ORDER_MANAGE · offline: True
    """
    return await run("createWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/media/{mediaId}")
async def delete_media_asset(request: Request) -> dict:
    """Delete an asset

    scope: venue · permission: ASSET_LIBRARY_MANAGE · offline: False
    """
    return await run("deleteMediaAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/assets/{assetId}")
async def get_asset(request: Request) -> dict:
    """Read an asset with history and documents

    scope: venue · permission: ASSET_VIEW · offline: True
    """
    return await run("getAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/assets/{assetId}/history")
async def get_asset_history(request: Request) -> dict:
    """Service history

    scope: venue · permission: ASSET_VIEW · offline: False
    """
    return await run("getAssetHistory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/maintenance-plans/due")
async def get_due_maintenance(request: Request) -> dict:
    """Planned tasks due or overdue

    scope: venue · permission: ASSET_VIEW · offline: False
    """
    return await run("getDueMaintenance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media/rights-expiring")
async def get_expiring_rights(request: Request) -> dict:
    """Assets whose licence is expiring or expired

    scope: venue · permission: ASSET_LIBRARY_VIEW · offline: False
    """
    return await run("getExpiringRights", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/game-cards/{cardCode}")
async def get_game_card(request: Request) -> dict:
    """Read a card's balances

    scope: venue · permission: - · offline: True
    """
    return await run("getGameCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/incidents/{incidentId}")
async def get_incident(request: Request) -> dict:
    """Read an incident

    scope: venue · permission: INCIDENT_VIEW · offline: False
    """
    return await run("getIncident", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media/{mediaId}")
async def get_media_asset(request: Request) -> dict:
    """Read an asset with derivatives and usage

    scope: venue · permission: ASSET_LIBRARY_VIEW · offline: True
    """
    return await run("getMediaAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queues/{queueId}")
async def get_queue(request: Request) -> dict:
    """Read a queue with live position

    scope: venue · permission: QUEUE_VIEW · offline: True
    """
    return await run("getQueue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queue-feeds/{feedId}/health")
async def get_queue_feed_health(request: Request) -> dict:
    """Feed health

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("getQueueFeedHealth", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resources/{resourceId}/availability")
async def get_resource_availability(request: Request) -> dict:
    """When it is free, with conflicts already resolved

    scope: venue · permission: RESOURCE_VIEW · offline: False
    """
    return await run("getResourceAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/sessions/{sessionId}/manifest")
async def get_session_manifest(request: Request) -> dict:
    """Who is in a session, in what order

    scope: venue · permission: RESOURCE_VIEW · offline: True
    """
    return await run("getSessionManifest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/signage/queue-board")
async def get_signage_queue_board(request: Request) -> dict:
    """Wait-time board for a display

    scope: venue · permission: - · offline: True
    """
    return await run("getSignageQueueBoard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/signage/queue-calls")
async def get_signage_queue_calls(request: Request) -> dict:
    """Currently called party numbers

    scope: venue · permission: - · offline: True
    """
    return await run("getSignageQueueCalls", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venue-maps/{mapId}")
async def get_venue_map(request: Request) -> dict:
    """A map with its points and paths

    scope: venue · permission: VENUE_MAP_VIEW · offline: True
    """
    return await run("getVenueMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venue-maps/{mapId}/graph")
async def get_venue_map_graph(request: Request) -> dict:
    """The navigation graph, ready to route over

    scope: venue · permission: VENUE_MAP_VIEW · offline: True
    """
    return await run("getVenueMapGraph", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venue-maps/{mapId}/live")
async def get_venue_map_live(request: Request) -> dict:
    """The map with live operational state on it

    scope: venue · permission: VENUE_MAP_VIEW · offline: False
    """
    return await run("getVenueMapLive", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queues/wait-times")
async def get_wait_times(request: Request) -> dict:
    """Wait times across a venue

    scope: venue · permission: - · offline: True
    """
    return await run("getWaitTimes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiting-guests/{entryId}")
async def get_waiting_guest(request: Request) -> dict:
    """Read a queue entry

    scope: venue · permission: - · offline: False
    """
    return await run("getWaitingGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/work-orders/{workOrderId}")
async def get_work_order(request: Request) -> dict:
    """Read a work order

    scope: venue · permission: WORK_ORDER_VIEW · offline: True
    """
    return await run("getWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps/{mapId}/import")
async def import_venue_geometry(request: Request) -> dict:
    """Read a drawing into shapes

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("importVenueGeometry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/game-cards")
async def issue_game_card(request: Request) -> dict:
    """Issue or activate a game card

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("issueGameCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waiting-guests")
async def join_queue(request: Request) -> dict:
    """Join a virtual queue

    scope: venue · permission: - · offline: False
    """
    return await run("joinQueue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/waiting-guests/{entryId}")
async def leave_queue(request: Request) -> dict:
    """Leave a queue

    scope: venue · permission: - · offline: False
    """
    return await run("leaveQueue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/assets")
async def list_assets(request: Request) -> dict:
    """List assets

    scope: venue · permission: ASSET_VIEW · offline: True
    """
    return await run("listAssets", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media/collections")
async def list_collections(request: Request) -> dict:
    """List collections

    scope: venue · permission: ASSET_LIBRARY_VIEW · offline: False
    """
    return await run("listCollections", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/games")
async def list_games(request: Request) -> dict:
    """List games

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listGames", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/incidents")
async def list_incidents(request: Request) -> dict:
    """List incidents

    scope: venue · permission: INCIDENT_VIEW · offline: False
    """
    return await run("listIncidents", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inspection-templates")
async def list_inspection_templates(request: Request) -> dict:
    """List inspection templates

    scope: venue · permission: INSPECTION_VIEW · offline: True
    """
    return await run("listInspectionTemplates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inspections")
async def list_inspections(request: Request) -> dict:
    """List completed inspections

    scope: venue · permission: INSPECTION_VIEW · offline: False
    """
    return await run("listInspections", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/maintenance-plans")
async def list_maintenance_plans(request: Request) -> dict:
    """List planned maintenance schedules

    scope: venue · permission: ASSET_VIEW · offline: False
    """
    return await run("listMaintenancePlans", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/prizes")
async def list_prizes(request: Request) -> dict:
    """The prize catalogue

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listPrizes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queues/{queueId}/entries")
async def list_queue_entries(request: Request) -> dict:
    """List entries in a queue

    scope: venue · permission: QUEUE_VIEW · offline: False
    """
    return await run("listQueueEntries", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queue-feeds")
async def list_queue_feeds(request: Request) -> dict:
    """List configured sensor feeds

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("listQueueFeeds", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queues")
async def list_queues(request: Request) -> dict:
    """List queues

    scope: venue · permission: QUEUE_VIEW · offline: True
    """
    return await run("listQueues", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resources")
async def list_resources(request: Request) -> dict:
    """Resources at this venue

    scope: venue · permission: RESOURCE_VIEW · offline: False
    """
    return await run("listResources", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venue-maps")
async def list_venue_maps(request: Request) -> dict:
    """Maps for this venue

    scope: venue · permission: VENUE_MAP_VIEW · offline: False
    """
    return await run("listVenueMaps", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/work-orders")
async def list_work_orders(request: Request) -> dict:
    """List work orders

    scope: venue · permission: WORK_ORDER_VIEW · offline: True
    """
    return await run("listWorkOrders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/game-cards/{cardCode}/load")
async def load_game_credits(request: Request) -> dict:
    """Load credits onto a card

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("loadGameCredits", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/assets/lookup")
async def lookup_asset(request: Request) -> dict:
    """Find an asset by tag or QR

    scope: venue · permission: ASSET_VIEW · offline: True
    """
    return await run("lookupAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waiting-guests/{entryId}/override")
async def override_waiting_guest(request: Request) -> dict:
    """Admit against a failed redemption

    scope: venue · permission: QUEUE_OVERRIDE · offline: True
    """
    return await run("overrideWaitingGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/pause")
async def pause_work_order(request: Request) -> dict:
    """Stopped, and why

    scope: venue · permission: MAINTENANCE_EXECUTE · offline: True
    """
    return await run("pauseWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps/{mapId}/publish")
async def publish_venue_map(request: Request) -> dict:
    """Make the draft the one guests see

    scope: venue · permission: VENUE_MAP_PUBLISH · offline: False
    """
    return await run("publishVenueMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/incidents/{incidentId}/notify-authority")
async def record_authority_notification(request: Request) -> dict:
    """Record notification to an external authority

    scope: venue · permission: INCIDENT_MANAGE · offline: False
    """
    return await run("recordAuthorityNotification", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/game-plays")
async def record_game_play(request: Request) -> dict:
    """Record a play

    scope: venue · permission: - · offline: True
    """
    return await run("recordGamePlay", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/parts")
async def record_work_order_parts(request: Request) -> dict:
    """Record parts consumed

    scope: venue · permission: WORK_ORDER_MANAGE · offline: False
    """
    return await run("recordWorkOrderParts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/time")
async def record_work_order_time(request: Request) -> dict:
    """Start, pause or stop work

    scope: venue · permission: WORK_ORDER_MANAGE · offline: True
    """
    return await run("recordWorkOrderTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/prize-redemptions")
async def redeem_prize(request: Request) -> dict:
    """Redeem points for a prize

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("redeemPrize", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waiting-guests/{entryId}/redeem")
async def redeem_waiting_guest(request: Request) -> dict:
    """Admit a party at the ride

    scope: workstation · permission: QUEUE_REDEEM · offline: True
    """
    return await run("redeemWaitingGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/reject")
async def reject_work_order(request: Request) -> dict:
    """The assignee declines, with a reason

    scope: venue · permission: MAINTENANCE_EXECUTE · offline: True
    """
    return await run("rejectWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/sessions/{sessionId}/manifest")
async def reorder_session_manifest(request: Request) -> dict:
    """Change the running order

    scope: venue · permission: RESOURCE_BOOK · offline: True
    """
    return await run("reorderSessionManifest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/media/{mediaId}/replace")
async def replace_media_asset(request: Request) -> dict:
    """Replace the file behind an asset

    scope: venue · permission: ASSET_LIBRARY_MANAGE · offline: False
    """
    return await run("replaceMediaAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/incidents")
async def report_incident(request: Request) -> dict:
    """Report an incident

    scope: venue · permission: INCIDENT_REPORT · offline: True
    """
    return await run("reportIncident", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/resume")
async def resume_work_order(request: Request) -> dict:
    """Back to work

    scope: venue · permission: MAINTENANCE_EXECUTE · offline: True
    """
    return await run("resumeWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media")
async def search_media(request: Request) -> dict:
    """Search the asset library

    scope: venue · permission: ASSET_LIBRARY_VIEW · offline: False
    """
    return await run("searchMedia", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/assets/{assetId}/status")
async def set_asset_status(request: Request) -> dict:
    """Take an asset out of service or return it

    scope: venue · permission: ASSET_MANAGE · offline: True
    """
    return await run("setAssetStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps/{mapId}/paths/{pathId}/closure")
async def set_path_closure(request: Request) -> dict:
    """Close a route during works or an incident

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("setPathClosure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/queues/{queueId}/status")
async def set_queue_status(request: Request) -> dict:
    """Open, pause or close a queue

    scope: venue · permission: QUEUE_MANAGE · offline: True
    """
    return await run("setQueueStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/reader-profiles")
async def set_reader_profile(request: Request) -> dict:
    """How a reader behaves and what it shows

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setReaderProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/resources/{resourceId}/qualifications")
async def set_resource_qualifications(request: Request) -> dict:
    """What a person resource is certified to do, and until when

    scope: venue · permission: RESOURCE_MANAGE · offline: False
    """
    return await run("setResourceQualifications", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps/{mapId}/points")
async def set_venue_point(request: Request) -> dict:
    """Place or amend a point of interest

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("setVenuePoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/queues/{queueId}/wait-time")
async def set_wait_time(request: Request) -> dict:
    """Manually set a wait time

    scope: venue · permission: QUEUE_MANAGE · offline: True
    """
    return await run("setWaitTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/start")
async def start_work_order(request: Request) -> dict:
    """Work has begun

    scope: venue · permission: MAINTENANCE_EXECUTE · offline: True
    """
    return await run("startWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inspections")
async def submit_inspection(request: Request) -> dict:
    """Submit a completed inspection

    scope: venue · permission: INSPECTION_SUBMIT · offline: True
    """
    return await run("submitInspection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/queue-feeds/readings")
async def submit_queue_reading(request: Request) -> dict:
    """Inbound sensor reading

    scope: venue · permission: - · offline: False
    """
    return await run("submitQueueReading", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/game-plays/sync")
async def sync_game_plays(request: Request) -> dict:
    """Replay plays recorded offline

    scope: venue · permission: - · offline: False
    """
    return await run("syncGamePlays", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/queue-feeds/{feedId}/test")
async def test_queue_feed(request: Request) -> dict:
    """Test a feed before trusting it

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("testQueueFeed", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/game-cards/{cardCode}/transfer")
async def transfer_game_card(request: Request) -> dict:
    """Move balances to another card

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("transferGameCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/assets/{assetId}")
async def update_asset(request: Request) -> dict:
    """Amend an asset

    scope: venue · permission: ASSET_MANAGE · offline: False
    """
    return await run("updateAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/games/{gameId}")
async def update_game(request: Request) -> dict:
    """Amend a game

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateGame", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/incidents/{incidentId}")
async def update_incident(request: Request) -> dict:
    """Investigate, escalate or close an incident

    scope: venue · permission: INCIDENT_MANAGE · offline: False
    """
    return await run("updateIncident", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/maintenance-plans/{planId}")
async def update_maintenance_plan(request: Request) -> dict:
    """Amend or suspend a plan

    scope: venue · permission: ASSET_MANAGE · offline: False
    """
    return await run("updateMaintenancePlan", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/media/{mediaId}")
async def update_media_asset(request: Request) -> dict:
    """Amend metadata, tags or rights

    scope: venue · permission: ASSET_LIBRARY_MANAGE · offline: False
    """
    return await run("updateMediaAsset", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/queues/{queueId}")
async def update_queue(request: Request) -> dict:
    """Amend queue configuration

    scope: venue · permission: QUEUE_MANAGE · offline: False
    """
    return await run("updateQueue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/work-orders/{workOrderId}")
async def update_work_order(request: Request) -> dict:
    """Assign, reprioritise or amend

    scope: venue · permission: WORK_ORDER_MANAGE · offline: True
    """
    return await run("updateWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/venue-maps/{mapId}/validate-graph")
async def validate_venue_map_graph(request: Request) -> dict:
    """What is unreachable, before anyone publishes it

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("validateVenueMapGraph", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/work-orders/{workOrderId}/verify")
async def verify_work_order(request: Request) -> dict:
    """Supervisor verification

    scope: venue · permission: WORK_ORDER_VERIFY · offline: False
    """
    return await run("verifyWorkOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

