"""CatalogueService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

136 operations · 48 tables touched · scope levels: region, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="CatalogueService", docs_url="/_docs")

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
    return {"service": "CatalogueService", "operations": 136,
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



@app.post("/inventory-holds")
async def acquire_inventory_hold(request: Request) -> dict:
    """Acquire an inventory lease

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("acquireInventoryHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-blocks/{blockId}/allocate")
async def allocate_blocked_seats(request: Request) -> dict:
    """Issue seats from a block to a group

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("allocateBlockedSeats", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotions/{promotionId}/conflicts")
async def analyse_promotion_conflicts(request: Request) -> dict:
    """Analyse stacking against live promotions

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("analysePromotionConflicts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/{productId}/change-impact")
async def assess_product_change(request: Request) -> dict:
    """What a change would touch, before making it

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("assessProductChange", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/coupon-codes/{code}/assign")
async def assign_coupon(request: Request) -> dict:
    """Assign a coupon to a named guest

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("assignCoupon", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/performances/{performanceId}/assign-seats")
async def assign_seats(request: Request) -> dict:
    """Pick and hold the best available seats

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("assignSeats", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/bulk-price")
async def bulk_change_prices(request: Request) -> dict:
    """Reprice a category or a whole catalogue

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("bulkChangePrices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/performances/{performanceId}/cancel")
async def cancel_performance(request: Request) -> dict:
    """Cancel a performance

    scope: venue · permission: PERFORMANCE_CONFIGURE · offline: False
    """
    return await run("cancelPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/{productId}/clone")
async def clone_product(request: Request) -> dict:
    """Copy a product as a new draft

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("cloneProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/clone")
async def clone_seat_map(request: Request) -> dict:
    """Clone a map, optionally into another venue

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("cloneSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/import/{jobId}/commit")
async def commit_catalogue_import(request: Request) -> dict:
    """Apply a parsed catalogue import

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("commitCatalogueImport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/import/{jobId}")
async def commit_import_job(request: Request) -> dict:
    """Apply a parsed import

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("commitImportJob", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/price-lists/{priceListId}/copy")
async def copy_price_list(request: Request) -> dict:
    """Copy a price list, optionally with an adjustment

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("copyPriceList", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/sections/copy")
async def copy_seat_map_section(request: Request) -> dict:
    """Copy one section into another map

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("copySeatMapSection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/bundles")
async def create_bundle(request: Request) -> dict:
    """Create a bundle

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/channel-capacities")
async def create_channel_capacity(request: Request) -> dict:
    """Create a capacity envelope

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("createChannelCapacity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/coupon-campaigns")
async def create_coupon_campaign(request: Request) -> dict:
    """Create a coupon campaign

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("createCouponCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/donation-campaigns")
async def create_donation_campaign(request: Request) -> dict:
    """Create a campaign

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createDonationCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/entitlement-templates")
async def create_entitlement_template(request: Request) -> dict:
    """Create an entitlement template

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createEntitlementTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/events")
async def create_event(request: Request) -> dict:
    """Create an event

    scope: venue · permission: EVENT_CONFIGURE · offline: False
    """
    return await run("createEvent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/events/{eventId}/performances")
async def create_performances(request: Request) -> dict:
    """Create performances, singly or by schedule

    scope: venue · permission: PERFORMANCE_CONFIGURE · offline: False
    """
    return await run("createPerformances", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/price-lists")
async def create_price_list(request: Request) -> dict:
    """Create a price list

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("createPriceList", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products")
async def create_product(request: Request) -> dict:
    """Create a product

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions")
async def create_promotion(request: Request) -> dict:
    """Create a promotion

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("createPromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-blocks")
async def create_seat_block(request: Request) -> dict:
    """Block seats from sale

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("createSeatBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-categories")
async def create_seat_category(request: Request) -> dict:
    """Create a seat category

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("createSeatCategory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-holds")
async def create_seat_hold(request: Request) -> dict:
    """Hold specific seats

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createSeatHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps")
async def create_seat_map(request: Request) -> dict:
    """Create a seat map

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("createSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-map-templates")
async def create_seat_map_template(request: Request) -> dict:
    """Save a map as a reusable template

    scope: region · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("createSeatMapTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/upsell-rules")
async def create_upsell_rule(request: Request) -> dict:
    """Create an upsell rule

    scope: region · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createUpsellRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/voucher-batches")
async def create_voucher_batch(request: Request) -> dict:
    """Issue a voucher batch

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("createVoucherBatch", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/upsell-rules/{ruleId}")
async def delete_upsell_rule(request: Request) -> dict:
    """Remove an upsell rule

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("deleteUpsellRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-maps/{seatMapId}/diff")
async def diff_seat_map_versions(request: Request) -> dict:
    """Compare two versions of a layout

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("diffSeatMapVersions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions/{promotionId}/end")
async def end_promotion(request: Request) -> dict:
    """End a promotion early

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("endPromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions/evaluate")
async def evaluate_promotions(request: Request) -> dict:
    """Evaluate promotions against a cart

    scope: venue · permission: PRICE_VIEW · offline: True
    """
    return await run("evaluatePromotions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-holds/{holdId}/extend")
async def extend_seat_hold(request: Request) -> dict:
    """Extend a hold

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("extendSeatHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inventory-holds/{inventoryHoldId}/force-release")
async def force_release_inventory_hold(request: Request) -> dict:
    """Reclaim a stranded lease

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("forceReleaseInventoryHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/entitlements/{entitlementId}/freeze")
async def freeze_entitlement(request: Request) -> dict:
    """Pause a membership at the guest's request

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("freezeEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/coupon-campaigns/{campaignId}/codes")
async def generate_coupon_codes(request: Request) -> dict:
    """Generate codes in bulk

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("generateCouponCodes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/availability")
async def get_availability(request: Request) -> dict:
    """Live remaining capacity

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundles/{bundleId}")
async def get_bundle(request: Request) -> dict:
    """Read a bundle with components and allocation

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-capacities/{channelCapacityId}/channel-allocations")
async def get_channel_allocations(request: Request) -> dict:
    """Capacity allocated to each channel

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getChannelAllocations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/coupon-codes/{code}")
async def get_coupon_code(request: Request) -> dict:
    """Look up a code

    scope: venue · permission: PRICE_VIEW · offline: True
    """
    return await run("getCouponCode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/events/{eventId}")
async def get_event(request: Request) -> dict:
    """Read an event

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getEvent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-maps/{seatMapId}/import/{jobId}")
async def get_import_job(request: Request) -> dict:
    """Import progress and findings

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getImportJob", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/catalogue/bundles/latest")
async def get_latest_bundle(request: Request) -> dict:
    """Pull the current bundle for this workstation's venue

    scope: workstation · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getLatestBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/me/memberships")
async def get_my_memberships(request: Request) -> dict:
    """A guest's own memberships, benefits and history

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getMyMemberships", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/performances/{performanceId}")
async def get_performance(request: Request) -> dict:
    """Read a performance

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-lists/{priceListId}")
async def get_price_list(request: Request) -> dict:
    """Read a price list

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("getPriceList", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/products/{productId}")
async def get_product(request: Request) -> dict:
    """Read a product

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotions/{promotionId}")
async def get_promotion(request: Request) -> dict:
    """Read a promotion

    scope: venue · permission: PRICE_VIEW · offline: True
    """
    return await run("getPromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotions/{promotionId}/usage")
async def get_promotion_usage(request: Request) -> dict:
    """Redemption count and discount given

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("getPromotionUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/recommendations")
async def get_recommendations(request: Request) -> dict:
    """What else this guest might want

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getRecommendations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/performances/{performanceId}/seat-availability")
async def get_seat_availability(request: Request) -> dict:
    """Seat status for a performance

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getSeatAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-holds/{holdId}")
async def get_seat_hold(request: Request) -> dict:
    """Read a hold

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getSeatHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-maps/{seatMapId}")
async def get_seat_map(request: Request) -> dict:
    """Read a seat map with its structure

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-map-imports/{importId}")
async def get_seat_map_import(request: Request) -> dict:
    """How the import went

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getSeatMapImport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-maps/{seatMapId}/rules")
async def get_seating_rules(request: Request) -> dict:
    """Read seating rules

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getSeatingRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/upsell-suggestions")
async def get_upsell_suggestions(request: Request) -> dict:
    """Suggestions for a cart

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getUpsellSuggestions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/import")
async def import_product_catalogue(request: Request) -> dict:
    """Parse a catalogue file into a preview

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("importProductCatalogue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/import/geometry")
async def import_seat_geometry(request: Request) -> dict:
    """Import seat geometry from a plan

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("importSeatGeometry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/import/manifest")
async def import_seat_manifest(request: Request) -> dict:
    """Import the logical seat structure

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("importSeatManifest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-map-imports")
async def import_seat_map(request: Request) -> dict:
    """Import a seat map from a plan or a manifest

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("importSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waitlist-entries")
async def join_waitlist(request: Request) -> dict:
    """Ask to be told if capacity frees up

    scope: venue · permission: - · offline: False
    """
    return await run("joinWaitlist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/waitlist-entries/{entryId}")
async def leave_waitlist(request: Request) -> dict:
    """Stop waiting

    scope: venue · permission: - · offline: False
    """
    return await run("leaveWaitlist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/allocation-splits")
async def list_allocation_splits(request: Request) -> dict:
    """List allocation split definitions

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("listAllocationSplits", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/products/{productId}/alternative-codes")
async def list_alternative_codes(request: Request) -> dict:
    """External identifiers for a product

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listAlternativeCodes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundles")
async def list_bundles(request: Request) -> dict:
    """List bundles

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listBundles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/catalogue/bundles")
async def list_catalogue_bundles(request: Request) -> dict:
    """List published bundles

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listCatalogueBundles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-capacities")
async def list_channel_capacities(request: Request) -> dict:
    """List capacity envelopes

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelCapacities", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/coupon-campaigns")
async def list_coupon_campaigns(request: Request) -> dict:
    """List coupon campaigns

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCouponCampaigns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/coupon-campaigns/{campaignId}/codes")
async def list_coupon_codes(request: Request) -> dict:
    """List generated codes

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCouponCodes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/donation-campaigns")
async def list_donation_campaigns(request: Request) -> dict:
    """Campaigns a guest can give to

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listDonationCampaigns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlement-templates")
async def list_entitlement_templates(request: Request) -> dict:
    """List entitlement templates

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listEntitlementTemplates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/events")
async def list_events(request: Request) -> dict:
    """List events

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listEvents", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest/memberships")
async def list_guest_memberships(request: Request) -> dict:
    """A guest's memberships, benefits and history

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listGuestMemberships", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inventory-holds")
async def list_inventory_holds(request: Request) -> dict:
    """List leases

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listInventoryHolds", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/events/{eventId}/performances")
async def list_performances(request: Request) -> dict:
    """List performances of an event

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listPerformances", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-lists")
async def list_price_lists(request: Request) -> dict:
    """List price lists

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPriceLists", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-lists/{priceListId}/prices")
async def list_prices(request: Request) -> dict:
    """List prices in a list

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPrices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-categories")
async def list_product_categories(request: Request) -> dict:
    """listProductCategories

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listProductCategories", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/products/{productId}/variants")
async def list_product_variants(request: Request) -> dict:
    """List generated variants

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listProductVariants", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/products/{productId}/versions")
async def list_product_versions(request: Request) -> dict:
    """What this product used to be

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductVersions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/products")
async def list_products(request: Request) -> dict:
    """List products

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listProducts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotions")
async def list_promotions(request: Request) -> dict:
    """List promotions

    scope: venue · permission: PRICE_VIEW · offline: True
    """
    return await run("listPromotions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-blocks")
async def list_seat_blocks(request: Request) -> dict:
    """List seat blocks

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSeatBlocks", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-categories")
async def list_seat_categories(request: Request) -> dict:
    """List seat categories

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listSeatCategories", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-map-templates")
async def list_seat_map_templates(request: Request) -> dict:
    """List reusable layout templates

    scope: region · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSeatMapTemplates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-maps")
async def list_seat_maps(request: Request) -> dict:
    """List seat maps

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSeatMaps", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seat-maps/{seatMapId}/seats")
async def list_seats(request: Request) -> dict:
    """List seats in a map

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSeats", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upsell-rules")
async def list_upsell_rules(request: Request) -> dict:
    """List upsell and cross-sell rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listUpsellRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/voucher-batches")
async def list_voucher_batches(request: Request) -> dict:
    """List voucher batches

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listVoucherBatches", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waitlist-entries")
async def list_waitlist_entries(request: Request) -> dict:
    """Who is waiting for capacity

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listWaitlistEntries", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/waitlist-entries/{entryId}/offer")
async def offer_waitlist_capacity(request: Request) -> dict:
    """Tell a waiting guest that capacity appeared

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("offerWaitlistCapacity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions/{promotionId}/pause")
async def pause_promotion(request: Request) -> dict:
    """Pause a live promotion

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("pausePromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/allocation-splits/preview")
async def preview_allocation_split(request: Request) -> dict:
    """Preview how an amount divides

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("previewAllocationSplit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/catalogue/bundles")
async def publish_bundle(request: Request) -> dict:
    """Compute, sign and publish a catalogue bundle

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions/{promotionId}/publish")
async def publish_promotion(request: Request) -> dict:
    """Publish a promotion

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("publishPromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/publish")
async def publish_seat_map(request: Request) -> dict:
    """Validate and publish a seat map

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("publishSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/performances/{performanceId}/seat-recommendations")
async def recommend_seats(request: Request) -> dict:
    """Recommend seats for a party

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("recommendSeats", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/vouchers/{voucherCode}/redeem")
async def redeem_voucher(request: Request) -> dict:
    """Redeem voucher value against an order

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("redeemVoucher", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/entitlements/{entitlementId}/reinstate")
async def reinstate_entitlement(request: Request) -> dict:
    """Lift a suspension

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("reinstateEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/channel-capacities/{channelCapacityId}/channel-allocations/release")
async def release_channel_allocation(request: Request) -> dict:
    """Return unsold channel allocation to the general pool

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("releaseChannelAllocation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/inventory-holds/{inventoryHoldId}")
async def release_inventory_hold(request: Request) -> dict:
    """Return unsold units

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("releaseInventoryHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/seat-blocks/{blockId}")
async def release_seat_block(request: Request) -> dict:
    """Release a block back to sale

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("releaseSeatBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/seat-holds/{holdId}")
async def release_seat_hold(request: Request) -> dict:
    """Release a hold

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("releaseSeatHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inventory-holds/{inventoryHoldId}/renew")
async def renew_inventory_hold(request: Request) -> dict:
    """Extend a lease TTL

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("renewInventoryHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/catalogue/bundles/{version}/applied")
async def report_bundle_applied(request: Request) -> dict:
    """Report that a workstation applied a bundle

    scope: workstation · permission: PRODUCT_VIEW · offline: False
    """
    return await run("reportBundleApplied", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/products/resolve")
async def resolve_product_by_code(request: Request) -> dict:
    """Resolve a partner code to a product

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("resolveProductByCode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/{productId}/versions/{version}/restore")
async def restore_product_version(request: Request) -> dict:
    """Put a previous version back

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("restoreProductVersion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/search")
async def search_catalogue(request: Request) -> dict:
    """Find something by name

    scope: venue · permission: - · offline: True
    """
    return await run("searchCatalogue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/products/{productId}/alternative-codes")
async def set_alternative_codes(request: Request) -> dict:
    """Set external identifiers

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setAlternativeCodes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-capacities/{channelCapacityId}/channel-allocations")
async def set_channel_allocations(request: Request) -> dict:
    """Allocate envelope capacity across channels

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("setChannelAllocations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/seat-maps/{seatMapId}/zones")
async def set_map_zones(request: Request) -> dict:
    """Standing areas, suites, stages and obstructions

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("setMapZones", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/price-lists/{priceListId}/prices")
async def set_prices(request: Request) -> dict:
    """Set prices in bulk

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setPrices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/products/{productId}/attributes")
async def set_product_attributes(request: Request) -> dict:
    """Set the attribute axes for a product

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductAttributes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/product-categories")
async def set_product_categories(request: Request) -> dict:
    """setProductCategories

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductCategories", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/promotions/{promotionId}/variants")
async def set_promotion_variants(request: Request) -> dict:
    """A/B test two versions against each other

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setPromotionVariants", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/seat-maps/{seatMapId}/rules")
async def set_seating_rules(request: Request) -> dict:
    """Set seating rules

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("setSeatingRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions/{promotionId}/simulate")
async def simulate_promotion(request: Request) -> dict:
    """What this promotion would have cost on real history

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("simulatePromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/entitlements/{entitlementId}/suspend")
async def suspend_entitlement(request: Request) -> dict:
    """Suspend or reinstate an entitlement

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("suspendEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/{productId}/lifecycle")
async def transition_product_lifecycle(request: Request) -> dict:
    """Move a product through its lifecycle

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("transitionProductLifecycle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/promotions/{promotionId}/unschedule")
async def unschedule_promotion(request: Request) -> dict:
    """Pull a scheduled promotion before it starts

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("unschedulePromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/bundles/{bundleId}")
async def update_bundle(request: Request) -> dict:
    """Amend a bundle

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/channel-capacities/{channelCapacityId}")
async def update_channel_capacity(request: Request) -> dict:
    """Amend an envelope

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("updateChannelCapacity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/donation-campaigns/{campaignId}")
async def update_donation_campaign(request: Request) -> dict:
    """Amend or close a campaign

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateDonationCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/events/{eventId}")
async def update_event(request: Request) -> dict:
    """Amend an event

    scope: venue · permission: EVENT_CONFIGURE · offline: False
    """
    return await run("updateEvent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/performances/{performanceId}")
async def update_performance(request: Request) -> dict:
    """Amend a performance

    scope: venue · permission: PERFORMANCE_CONFIGURE · offline: False
    """
    return await run("updatePerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/price-lists/{priceListId}")
async def update_price_list(request: Request) -> dict:
    """Amend a price list

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("updatePriceList", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/products/{productId}")
async def update_product(request: Request) -> dict:
    """Update a product

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/promotions/{promotionId}")
async def update_promotion(request: Request) -> dict:
    """Amend a promotion

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("updatePromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/seat-maps/{seatMapId}")
async def update_seat_map(request: Request) -> dict:
    """Rename or amend a seat map

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("updateSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/seat-maps/{seatMapId}/seats")
async def update_seats(request: Request) -> dict:
    """Bulk-amend seats

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("updateSeats", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seat-maps/{seatMapId}/validate")
async def validate_seat_map(request: Request) -> dict:
    """Run validation without publishing

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("validateSeatMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/coupon-codes/{code}/void")
async def void_coupon_code(request: Request) -> dict:
    """Void a code

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("voidCouponCode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/vouchers/{voucherId}/void")
async def void_voucher(request: Request) -> dict:
    """Cancel a voucher

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("voidVoucher", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

