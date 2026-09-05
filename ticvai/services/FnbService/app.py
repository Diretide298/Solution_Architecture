"""FnbService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

99 operations · 44 tables touched · scope levels: venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="FnbService", docs_url="/_docs")

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
    return {"service": "FnbService", "operations": 99,
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



@app.post("/fnb-orders/{orderId}/accept")
async def accept_fnb_order(request: Request) -> dict:
    """The outlet takes the order

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("acceptFnbOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/fnb-orders/{orderId}")
async def amend_fnb_order(request: Request) -> dict:
    """Amend an order before it is prepared

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("amendFnbOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/menus/{menuId}/actions")
async def apply_menu_actions(request: Request) -> dict:
    """Do the same thing to many items at once

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("applyMenuActions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/menu-items/{menuItemId}/modifier-groups")
async def attach_modifier_group(request: Request) -> dict:
    """Give an item its choices

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("attachModifierGroup", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/production-plans")
async def build_production_plan(request: Request) -> dict:
    """Turn a forecast into a prep list

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("buildProductionPlan", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fnb-orders/{orderId}/cancel")
async def cancel_fnb_order(request: Request) -> dict:
    """Cancel an order

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("cancelFnbOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-stations/{stationId}/chase")
async def chase_station(request: Request) -> dict:
    """The pass asks a station where an item is

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("chaseStation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/location-sessions")
async def claim_location_session(request: Request) -> dict:
    """Tell the platform where the guest is

    scope: venue · permission: - · offline: False
    """
    return await run("claimLocationSession", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-sessions")
async def claim_table_session(request: Request) -> dict:
    """Identify which table a guest is sitting at

    scope: venue · permission: - · offline: False
    """
    return await run("claimTableSession", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tables/{tableId}/clear")
async def clear_table(request: Request) -> dict:
    """Mark a table cleared and free

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("clearTable", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/food-safety/corrective-actions/{actionId}/close")
async def close_corrective_action(request: Request) -> dict:
    """Close a signed finding

    scope: venue · permission: INCIDENT_MANAGE · offline: False
    """
    return await run("closeCorrectiveAction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/close")
async def close_table_visit(request: Request) -> dict:
    """Settle and close a visit

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("closeTableVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/comp")
async def comp_item(request: Request) -> dict:
    """Take a line off the bill, with a reason and a name

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("compItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/production-runs/{runId}/complete")
async def complete_production_run(request: Request) -> dict:
    """Record what was actually made

    scope: venue · permission: FNB_MANAGE · offline: True
    """
    return await run("completeProductionRun", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/combos")
async def create_combo(request: Request) -> dict:
    """A meal deal, priced as one thing

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createCombo", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fnb-orders")
async def create_fnb_order(request: Request) -> dict:
    """Place an F&B order

    scope: workstation · permission: ORDER_CREATE · offline: True
    """
    return await run("createFnbOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guest-orders")
async def create_guest_fnb_order(request: Request) -> dict:
    """A guest orders food

    scope: venue · permission: - · offline: False
    """
    return await run("createGuestFnbOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/menus")
async def create_menu(request: Request) -> dict:
    """Create a menu

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createMenu", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/modifier-groups")
async def create_modifier_group(request: Request) -> dict:
    """Create a modifier group

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createModifierGroup", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tables")
async def create_table(request: Request) -> dict:
    """A table as a thing, not an inference

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createTable", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-reservations")
async def create_table_reservation(request: Request) -> dict:
    """Book a table in advance

    scope: venue · permission: - · offline: False
    """
    return await run("createTableReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts/{countId}/lines")
async def enter_count_line(request: Request) -> dict:
    """What was actually on the shelf

    scope: venue · permission: PRODUCT_CONFIGURE · offline: True
    """
    return await run("enterCountLine", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/food-safety/corrective-actions/{actionId}/escalate")
async def escalate_corrective_action(request: Request) -> dict:
    """Escalate a finding

    scope: venue · permission: INCIDENT_MANAGE · offline: False
    """
    return await run("escalateCorrectiveAction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-tickets/{ticketId}/fire")
async def fire_course(request: Request) -> dict:
    """Send a held course to the pass

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("fireCourse", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/table-visits/{visitId}/bill")
async def get_bill(request: Request) -> dict:
    """Bill for a visit

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getBill", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fnb-orders/{orderId}")
async def get_fnb_order(request: Request) -> dict:
    """Read an F&B order

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getFnbOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/table-sessions/{sessionId}/bill")
async def get_guest_bill(request: Request) -> dict:
    """The bill for the guest's table

    scope: venue · permission: - · offline: False
    """
    return await run("getGuestBill", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/outlets/{outletId}/guest-menu")
async def get_guest_menu(request: Request) -> dict:
    """The menu a guest sees

    scope: venue · permission: - · offline: True
    """
    return await run("getGuestMenu", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest-orders/{orderId}")
async def get_guest_order_status(request: Request) -> dict:
    """Track an order

    scope: venue · permission: - · offline: False
    """
    return await run("getGuestOrderStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/food-safety/status")
async def get_haccp_status(request: Request) -> dict:
    """getHaccpStatus

    scope: venue · permission: INCIDENT_VIEW · offline: True
    """
    return await run("getHaccpStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/menus/{menuId}")
async def get_menu(request: Request) -> dict:
    """Read a menu with sections and items

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getMenu", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/production-runs/{runId}")
async def get_production_run(request: Request) -> dict:
    """One run — its plan, its output, and the gap

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getProductionRun", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/outlets/{outletId}/tables")
async def get_table_map(request: Request) -> dict:
    """Table map with live state

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getTableMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/table-visits/{visitId}")
async def get_table_visit(request: Request) -> dict:
    """Read a visit with all its orders

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getTableVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-tickets/{ticketId}/hold")
async def hold_course(request: Request) -> dict:
    """Stop a course going out

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("holdCourse", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waitlist")
async def join_restaurant_waitlist(request: Request) -> dict:
    """Add a party to an outlet's waitlist

    scope: venue · permission: FNB_SERVE · offline: True
    """
    return await run("joinRestaurantWaitlist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/outlets/{outletId}/86-events")
async def list86_events(request: Request) -> dict:
    """What came off the menu today, when, and for how long

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("list86Events", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venues/{venueId}/delivery-locations")
async def list_delivery_locations(request: Request) -> dict:
    """Where an order can be delivered

    scope: venue · permission: - · offline: True
    """
    return await run("listDeliveryLocations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venues/{venueId}/dining")
async def list_dining_outlets(request: Request) -> dict:
    """Where a guest can eat, right now

    scope: venue · permission: - · offline: False
    """
    return await run("listDiningOutlets", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fnb-orders")
async def list_fnb_orders(request: Request) -> dict:
    """List F&B orders

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listFnbOrders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/kitchen/stations")
async def list_kitchen_stations(request: Request) -> dict:
    """List preparation stations and their routing

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listKitchenStations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/kitchen/tickets")
async def list_kitchen_tickets(request: Request) -> dict:
    """Kitchen ticket queue

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("listKitchenTickets", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/menus")
async def list_menus(request: Request) -> dict:
    """List menus

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listMenus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/modifier-groups")
async def list_modifier_groups(request: Request) -> dict:
    """List modifier groups

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listModifierGroups", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/production-runs")
async def list_production_runs(request: Request) -> dict:
    """What is being made, and what was

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listProductionRuns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/recipes")
async def list_recipes(request: Request) -> dict:
    """List recipes

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRecipes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/table-reservations")
async def list_table_reservations(request: Request) -> dict:
    """Bookings for a service period

    scope: venue · permission: FNB_OPERATE · offline: True
    """
    return await run("listTableReservations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/food-safety/cold-chain")
async def log_cold_chain(request: Request) -> dict:
    """logColdChain

    scope: venue · permission: INCIDENT_REPORT · offline: True
    """
    return await run("logColdChain", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-exceptions")
async def log_kitchen_exception(request: Request) -> dict:
    """Something went wrong that is not a refire

    scope: venue · permission: INCIDENT_REPORT · offline: True
    """
    return await run("logKitchenException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/food-safety/temperature-logs")
async def log_temperature(request: Request) -> dict:
    """logTemperature

    scope: venue · permission: INCIDENT_REPORT · offline: True
    """
    return await run("logTemperature", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/collected")
async def mark_order_collected(request: Request) -> dict:
    """The guest took it

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("markOrderCollected", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/merge")
async def merge_table_visits(request: Request) -> dict:
    """Merge another visit into this one

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("mergeTableVisits", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/move")
async def move_table_visit(request: Request) -> dict:
    """Move a party to a different table, mid-service

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("moveTableVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/notify-server")
async def notify_server(request: Request) -> dict:
    """The kitchen calls the server to the pass

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("notifyServer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waitlist/{entryId}/notify")
async def notify_waitlist_party(request: Request) -> dict:
    """Their table is ready

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("notifyWaitlistParty", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits")
async def open_table_visit(request: Request) -> dict:
    """Seat a party and open a visit

    scope: workstation · permission: ORDER_CREATE · offline: True
    """
    return await run("openTableVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/production-runs")
async def plan_production_run(request: Request) -> dict:
    """Plan a batch, for one outlet or several

    scope: venue · permission: FNB_MANAGE · offline: False
    """
    return await run("planProductionRun", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-tickets/{ticketId}/label")
async def print_order_label(request: Request) -> dict:
    """A label for the bag

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("printOrderLabel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen/tickets/{ticketId}/prioritise")
async def prioritise_kitchen_ticket(request: Request) -> dict:
    """Move a ticket up the queue

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("prioritiseKitchenTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/menus/{menuId}/publish")
async def publish_menu(request: Request) -> dict:
    """Make the draft live, now or on a date

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishMenu", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waitlist/{entryId}/quote")
async def quote_wait_time(request: Request) -> dict:
    """Tell a party how long, and mean it

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("quoteWaitTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/table-visits/{visitId}/server")
async def reassign_server(request: Request) -> dict:
    """Hand a table to another server

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("reassignServer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-stations/rebalance")
async def rebalance_station_load(request: Request) -> dict:
    """Move work between stations mid-service

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("rebalanceStationLoad", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-tickets/{ticketId}/recall")
async def recall_kitchen_ticket(request: Request) -> dict:
    """Bring back a ticket that was bumped by mistake

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("recallKitchenTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/food-safety/corrective-actions/{actionId}/action")
async def record_corrective_action(request: Request) -> dict:
    """Record what was done about a finding

    scope: venue · permission: INCIDENT_MANAGE · offline: False
    """
    return await run("recordCorrectiveAction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guest-orders/{orderId}/delivery")
async def record_order_handover(request: Request) -> dict:
    """Record that an order reached the guest

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("recordOrderHandover", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/outlets/{outletId}/waste")
async def record_waste(request: Request) -> dict:
    """Record waste

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("recordWaste", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kitchen-tickets/{ticketId}/refire")
async def refire_item(request: Request) -> dict:
    """Make it again

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("refireItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/production-plans/{planId}/release")
async def release_production_plan(request: Request) -> dict:
    """Make the plan real

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("releaseProductionPlan", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/request-bill")
async def request_bill(request: Request) -> dict:
    """The party asked to pay

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("requestBill", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts/{countId}/recount")
async def request_recount(request: Request) -> dict:
    """Send a line back to be counted again

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("requestRecount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/table-reservations/conflicts")
async def resolve_booking_conflict(request: Request) -> dict:
    """Two bookings, one table — and what to do about it

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("resolveBookingConflict", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/menus/{menuId}/rollback")
async def rollback_menu(request: Request) -> dict:
    """Put the previous version back

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("rollbackMenu", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/menus/{menuId}/schedule")
async def schedule_menu_publish(request: Request) -> dict:
    """Publish it on a date, not now

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("scheduleMenuPublish", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-reservations/{reservationId}/seat")
async def seat_table_reservation(request: Request) -> dict:
    """The party arrived and has been sat down

    scope: venue · permission: FNB_OPERATE · offline: True
    """
    return await run("seatTableReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-reservations/{reservationId}/confirm")
async def send_booking_confirmation(request: Request) -> dict:
    """Confirm a booking, and ask them to confirm back

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("sendBookingConfirmation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fnb-orders/{orderId}/notify")
async def send_order_notification(request: Request) -> dict:
    """Tell the guest where their order is

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("sendOrderNotification", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/combos/{comboId}/slots")
async def set_combo_slots(request: Request) -> dict:
    """What the guest chooses, and what it costs extra

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setComboSlots", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/outlets/{outletId}/course-rules")
async def set_course_rules(request: Request) -> dict:
    """How this outlet courses by default

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setCourseRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/menu-items/{itemId}/availability")
async def set_item_availability(request: Request) -> dict:
    """Mark an item available or eighty-sixed

    scope: venue · permission: PRODUCT_CONFIGURE · offline: True
    """
    return await run("setItemAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/outlets/{outletId}/kitchen-sla")
async def set_kitchen_sla(request: Request) -> dict:
    """How long a ticket may sit before it is late

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setKitchenSla", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/kitchen/stations")
async def set_kitchen_stations(request: Request) -> dict:
    """Configure stations and item routing

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setKitchenStations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/kitchen/tickets/{ticketId}/status")
async def set_kitchen_ticket_status(request: Request) -> dict:
    """Advance a kitchen ticket

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("setKitchenTicketStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/menus/{menuId}/sections")
async def set_menu_sections(request: Request) -> dict:
    """Set menu sections and their item ordering

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setMenuSections", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/recipes")
async def set_recipe(request: Request) -> dict:
    """Define a recipe for a menu item

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setRecipe", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/outlets/{outletId}/sections")
async def set_section_layout(request: Request) -> dict:
    """Divide the floor into sections and give each a server

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setSectionLayout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/table-visits/{visitId}/stage")
async def set_service_stage(request: Request) -> dict:
    """Where this table is in its meal

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("setServiceStage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/substitution-rules")
async def set_substitution_rules(request: Request) -> dict:
    """What may replace what

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setSubstitutionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/outlets/{outletId}/table-combinations")
async def set_table_combinations(request: Request) -> dict:
    """Which tables can be pushed together, and to what capacity

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setTableCombinations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/outlets/{outletId}/tables")
async def set_table_layout(request: Request) -> dict:
    """Configure the table layout

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setTableLayout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/food-safety/corrective-actions/{actionId}/sign")
async def sign_corrective_action(request: Request) -> dict:
    """signCorrectiveAction

    scope: venue · permission: INCIDENT_MANAGE · offline: False
    """
    return await run("signCorrectiveAction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/bill/split")
async def split_bill(request: Request) -> dict:
    """Split a bill

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("splitBill", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/transfer-items")
async def transfer_order_items(request: Request) -> dict:
    """Move items to another table's bill

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("transferOrderItems", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/table-visits/{visitId}/transfer")
async def transfer_table_visit(request: Request) -> dict:
    """Move a check to another server

    scope: venue · permission: FNB_SERVE · offline: True
    """
    return await run("transferTableVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/menus/{menuId}")
async def update_menu(request: Request) -> dict:
    """Amend a menu

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateMenu", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tables/{tableId}")
async def update_table(request: Request) -> dict:
    """Change what a table is

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateTable", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/table-reservations/{reservationId}")
async def update_table_reservation(request: Request) -> dict:
    """Change or cancel a booking

    scope: venue · permission: - · offline: False
    """
    return await run("updateTableReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/table-visits/{visitId}")
async def update_table_visit(request: Request) -> dict:
    """Amend covers, move table, or reassign server

    scope: venue · permission: ORDER_MODIFY · offline: True
    """
    return await run("updateTableVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/menu-items/{menuItemId}/verify-allergens")
async def verify_allergens(request: Request) -> dict:
    """Does this dish still match its claim?

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("verifyAllergens", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

