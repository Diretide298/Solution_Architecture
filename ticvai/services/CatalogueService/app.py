"""CatalogueService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

344 operations · 48 tables touched · scope levels: region, venue, workstation
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
    return {"service": "CatalogueService", "operations": 344,
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


@app.put("/campaign-workflow")
async def approve_campaign_workflow(request: Request) -> dict:
    """Campaign Approval Workflow Designer

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("approveCampaignWorkflow", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/decision")
async def approve_decision(request: Request) -> dict:
    """Approval Inbox & Decision Workspace

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("approveDecision", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pricing-workflow-authority")
async def approve_pricing_workflow_authority(request: Request) -> dict:
    """Pricing Approval Workflow & Authority Matrix

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("approvePricingWorkflowAuthority", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/review-decision")
async def approve_review_decision(request: Request) -> dict:
    """Approval Review & Decision Workspace

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("approveReviewDecision", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/workflow")
async def approve_workflow(request: Request) -> dict:
    """Approval Workflow Designer

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("approveWorkflow", request.headers.get("x-scope-path", "uae"),
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


@app.post("/bulk-product-catalogue")
async def create_bulk_product_catalogue(request: Request) -> dict:
    """Bulk Product Creation & Catalogue Import

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createBulkProductCatalogue", request.headers.get("x-scope-path", "uae"),
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


@app.post("/channel-profile")
async def create_channel_profile(request: Request) -> dict:
    """Channel Creation & Profile Configuration

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createChannelProfile", request.headers.get("x-scope-path", "uae"),
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


@app.post("/live-dynamic-price")
async def create_live_dynamic_price(request: Request) -> dict:
    """Live Dynamic Price Execution & Deployment Monitor

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createLiveDynamicPrice", request.headers.get("x-scope-path", "uae"),
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


@app.get("/advanced-offer")
async def list_advanced_offer(request: Request) -> dict:
    """Advanced Offer Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listAdvancedOffer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/advanced-offer-guardrail")
async def list_advanced_offer_guardrail(request: Request) -> dict:
    """Advanced Offer Guardrails & Conflict Controls

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listAdvancedOfferGuardrail", request.headers.get("x-scope-path", "uae"),
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


@app.get("/audience-discovery-targeting")
async def list_audience_discovery_targeting(request: Request) -> dict:
    """AI Audience Discovery & Targeting Optimization

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listAudienceDiscoveryTargeting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/audience-preview-reach")
async def list_audience_preview_reach(request: Request) -> dict:
    """Audience Preview, Reach & Eligibility Simulator

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listAudiencePreviewReach", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/automation-policy-autonomou")
async def list_automation_policy_autonomous(request: Request) -> dict:
    """Automation Policy & Autonomous Pricing Orchestrator

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listAutomationPolicyAutonomous", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/behavioral-transaction-targeting")
async def list_behavioral_transaction_targeting(request: Request) -> dict:
    """Behavioral & Transaction Targeting

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBehavioralTransactionTargeting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/best-offer-customer")
async def list_best_offer_customer(request: Request) -> dict:
    """Best Offer & Customer Benefit Resolver

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBestOfferCustomer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/budget-consumption-forecast")
async def list_budget_consumption_forecast(request: Request) -> dict:
    """Budget Consumption & Forecast Monitor

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBudgetConsumptionForecast", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bulk-pricing-update")
async def list_bulk_pricing_update(request: Request) -> dict:
    """Bulk Pricing Update, Import & Mass Maintenance

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listBulkPricingUpdate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-availability-capacity")
async def list_bundle_availability_capacity(request: Request) -> dict:
    """Bundle Availability, Capacity & Validation

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleAvailabilityCapacity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-availability-channel")
async def list_bundle_availability_channel(request: Request) -> dict:
    """Bundle Availability by Channel, Venue & Partner

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleAvailabilityChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-availability-forecast")
async def list_bundle_availability_forecast(request: Request) -> dict:
    """Bundle Availability Forecast, Alerts & Recovery

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleAvailabilityForecast", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-bogo-advanced")
async def list_bundle_bogo_advanced(request: Request) -> dict:
    """Bundle, BOGO & Advanced Offer Analytics

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleBogoAdvanced", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-combo")
async def list_bundle_combo(request: Request) -> dict:
    """Bundle & Combo Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleCombo", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-pricing-commercial")
async def list_bundle_pricing_commercial(request: Request) -> dict:
    """Bundle Pricing & Commercial Model

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundlePricingCommercial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-sellability-dependency")
async def list_bundle_sellability_dependency(request: Request) -> dict:
    """Bundle Sellability & Dependency Rule Engine

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleSellabilityDependency", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundle-validity-scheduling")
async def list_bundle_validity_scheduling(request: Request) -> dict:
    """Bundle Validity, Scheduling & Redemption Rules

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listBundleValidityScheduling", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bundles")
async def list_bundles(request: Request) -> dict:
    """List bundles

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listBundles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/calculation-validation-reconciliation")
async def list_calculation_validation_reconciliation(request: Request) -> dict:
    """Calculation Validation, Reconciliation & Service Interface

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCalculationValidationReconciliation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaign-calendar-timeline")
async def list_campaign_calendar_timeline(request: Request) -> dict:
    """Campaign Calendar & Timeline

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCampaignCalendarTimeline", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaign-experiment-test")
async def list_campaign_experiment_test(request: Request) -> dict:
    """Campaign Experiment & A/B Test Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCampaignExperimentTest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaign-financial-commercial")
async def list_campaign_financial_commercial(request: Request) -> dict:
    """Campaign Financial & Commercial Simulator

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCampaignFinancialCommercial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaign-governance-budget")
async def list_campaign_governance_budget(request: Request) -> dict:
    """Campaign Governance & Budget Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCampaignGovernanceBudget", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaign-promotion-performance")
async def list_campaign_promotion_performance(request: Request) -> dict:
    """Campaign & Promotion Performance Explorer

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCampaignPromotionPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/capacity-pool-reservation")
async def list_capacity_pool_reservation(request: Request) -> dict:
    """Capacity Pool & Reservation Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCapacityPoolReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cart-transaction-threshold")
async def list_cart_transaction_threshold(request: Request) -> dict:
    """Cart & Transaction Threshold Rules

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCartTransactionThreshold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/catalogue/bundles")
async def list_catalogue_bundles(request: Request) -> dict:
    """List published bundles

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listCatalogueBundles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/change-impact-analysi")
async def list_change_impact_analysis(request: Request) -> dict:
    """Change Impact Analysis

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChangeImpactAnalysis", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/change-propagation-dependency")
async def list_change_propagation_dependency(request: Request) -> dict:
    """Change Propagation & Dependency Control

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChangePropagationDependency", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel")
async def list_channel(request: Request) -> dict:
    """Channel Operations Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel")
async def list_channel2(request: Request) -> dict:
    """AI Channel Optimization & Intelligence Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannel2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-allocation-rebalancing")
async def list_channel_allocation_rebalancing(request: Request) -> dict:
    """Channel Allocation & Rebalancing Operations

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelAllocationRebalancing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-based-pricing")
async def list_channel_based_pricing(request: Request) -> dict:
    """Channel-Based Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelBasedPricing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-capacities")
async def list_channel_capacities(request: Request) -> dict:
    """List capacity envelopes

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelCapacities", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-connection-integration")
async def list_channel_connection_integration(request: Request) -> dict:
    """Channel Connection & Integration Manager

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelConnectionIntegration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-customer-segment")
async def list_channel_customer_segment(request: Request) -> dict:
    """Channel, Customer Segment & Location Dynamic Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelCustomerSegment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-exception-incident")
async def list_channel_exception_incident(request: Request) -> dict:
    """Channel Exceptions, Incidents & Recovery

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelExceptionIncident", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-governance-sla")
async def list_channel_governance_sla(request: Request) -> dict:
    """Channel Governance, SLA & Partner Control

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelGovernanceSla", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-log-transaction")
async def list_channel_log_transaction(request: Request) -> dict:
    """Channel Audit, Logs & Transaction Traceability

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelLogTransaction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-performance-commercial")
async def list_channel_performance_commercial(request: Request) -> dict:
    """Channel Performance & Commercial Analytics

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelPerformanceCommercial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-sale-rule")
async def list_channel_sale_rule(request: Request) -> dict:
    """Channel Sales Rules, Limits & Restrictions

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelSaleRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-sale-schedule")
async def list_channel_sale_schedule(request: Request) -> dict:
    """Channel Sales Schedule & Availability Windows

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listChannelSaleSchedule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cheapest-lowest-value")
async def list_cheapest_lowest_value(request: Request) -> dict:
    """Cheapest / Lowest-Value Item Promotion

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCheapestLowestValue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/code-eligibility-restriction")
async def list_code_eligibility_restriction(request: Request) -> dict:
    """Code Eligibility & Restriction Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCodeEligibilityRestriction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/code-security-fraud")
async def list_code_security_fraud(request: Request) -> dict:
    """Code Security, Fraud & Exception Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCodeSecurityFraud", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commercial-pricing")
async def list_commercial_pricing(request: Request) -> dict:
    """Commercial Pricing Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCommercialPricing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commercial-pricing-structure")
async def list_commercial_pricing_structure(request: Request) -> dict:
    """Commercial Pricing Structure Validation

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCommercialPricingStructure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/competitor-pricing-market")
async def list_competitor_pricing_market(request: Request) -> dict:
    """Competitor Pricing & Market Position Intelligence

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCompetitorPricingMarket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/component-inventory-availability")
async def list_component_inventory_availability(request: Request) -> dict:
    """Component Inventory & Availability Matrix

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listComponentInventoryAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/conflict")
async def list_conflict(request: Request) -> dict:
    """Conflict Simulation & AI Optimization

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listConflict", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/conflict-detection-resolution")
async def list_conflict_detection_resolution(request: Request) -> dict:
    """Conflict Detection & Resolution Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listConflictDetectionResolution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/context-location-channel")
async def list_context_location_channel(request: Request) -> dict:
    """Context, Location, Channel & Time Targeting

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listContextLocationChannel", request.headers.get("x-scope-path", "uae"),
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


@app.get("/crm-customer-segment")
async def list_crm_customer_segment(request: Request) -> dict:
    """CRM & Customer Segment Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCrmCustomerSegment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/currency-precision-rounding")
async def list_currency_precision_rounding(request: Request) -> dict:
    """Currency Precision, Rounding & Monetary Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCurrencyPrecisionRounding", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-eligibility-rule")
async def list_customer_eligibility_rule(request: Request) -> dict:
    """Customer & Eligibility Rules by Channel

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCustomerEligibilityRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-membership-segment")
async def list_customer_membership_segment(request: Request) -> dict:
    """Customer, Membership & Segment Discount Rules

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCustomerMembershipSegment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-segment-channel")
async def list_customer_segment_channel(request: Request) -> dict:
    """Customer, Segment, Channel & Partner Analytics

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listCustomerSegmentChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-segment-profile")
async def list_customer_segment_profile(request: Request) -> dict:
    """Customer Segment & Profile Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listCustomerSegmentProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/demand-booking-curve")
async def list_demand_booking_curve(request: Request) -> dict:
    """AI Demand Forecasting & Booking Curve Studio

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listDemandBookingCurve", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/discount-calculation-application")
async def list_discount_calculation_application(request: Request) -> dict:
    """Discount Calculation & Application Sequence

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDiscountCalculationApplication", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/discount-cap-maximum")
async def list_discount_cap_maximum(request: Request) -> dict:
    """Discount Cap & Maximum Benefit Controller

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDiscountCapMaximum", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/discount-limit-guardrail")
async def list_discount_limit_guardrail(request: Request) -> dict:
    """Discount Limits, Guardrails & Commercial Controls

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDiscountLimitGuardrail", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/discount-margin-profitability")
async def list_discount_margin_profitability(request: Request) -> dict:
    """Discount, Margin & Profitability Analytics

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDiscountMarginProfitability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/donation-campaigns")
async def list_donation_campaigns(request: Request) -> dict:
    """Campaigns a guest can give to

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listDonationCampaigns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-bundle")
async def list_dynamic_bundle(request: Request) -> dict:
    """Dynamic Bundle Operations Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDynamicBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-bundle")
async def list_dynamic_bundle2(request: Request) -> dict:
    """Dynamic Bundle Simulation & AI Optimization

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDynamicBundle2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-bundle-rule")
async def list_dynamic_bundle_rule(request: Request) -> dict:
    """Dynamic Bundle Rule & Composition Engine

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDynamicBundleRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-component-substitution")
async def list_dynamic_component_substitution(request: Request) -> dict:
    """Dynamic Component Substitution Engine

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listDynamicComponentSubstitution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-price-band")
async def list_dynamic_price_band(request: Request) -> dict:
    """Dynamic Price Bands, Ladders & Adjustment Matrix

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listDynamicPriceBand", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-pricing-automation")
async def list_dynamic_pricing_automation(request: Request) -> dict:
    """Dynamic Pricing Automation Policy & Control

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listDynamicPricingAutomation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-pricing-guardrail")
async def list_dynamic_pricing_guardrail(request: Request) -> dict:
    """Dynamic Pricing Guardrails & Commercial Protection

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listDynamicPricingGuardrail", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-pricing-performance")
async def list_dynamic_pricing_performance(request: Request) -> dict:
    """Dynamic Pricing Performance & Optimization Analytics

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listDynamicPricingPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-pricing-strategy")
async def list_dynamic_pricing_strategy(request: Request) -> dict:
    """Dynamic Pricing Strategy Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listDynamicPricingStrategy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/effective-date-season")
async def list_effective_date_season(request: Request) -> dict:
    """Effective Date, Season & Day-Based Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listEffectiveDateSeason", request.headers.get("x-scope-path", "uae"),
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


@app.get("/executive-promotion-reporting")
async def list_executive_promotion_reporting(request: Request) -> dict:
    """Executive Promotion Intelligence & Reporting Studio

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listExecutivePromotionReporting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fee-surcharge")
async def list_fee_surcharge(request: Request) -> dict:
    """Fee & Surcharge Library

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listFeeSurcharge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fee-waiver-tax")
async def list_fee_waiver_tax(request: Request) -> dict:
    """Fee Waiver, Tax Exemption & Exception Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listFeeWaiverTax", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/governance-risk-launch")
async def list_governance_risk_launch(request: Request) -> dict:
    """Governance Audit, AI Risk & Launch Readiness

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listGovernanceRiskLaunch", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/governance-risk-monitoring")
async def list_governance_risk_monitoring(request: Request) -> dict:
    """Governance Risk, AI Monitoring & Control Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listGovernanceRiskMonitoring", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest/memberships")
async def list_guest_memberships(request: Request) -> dict:
    """A guest's memberships, benefits and history

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listGuestMemberships", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/incrementality-attribution-cannibalization")
async def list_incrementality_attribution_cannibalization(request: Request) -> dict:
    """Incrementality, Attribution & Cannibalization Analysis

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listIncrementalityAttributionCannibalization", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/internal-demand-booking")
async def list_internal_demand_booking(request: Request) -> dict:
    """Internal Demand & Booking Signal Hub

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listInternalDemandBooking", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inventory-capacity-channel")
async def list_inventory_capacity_channel(request: Request) -> dict:
    """Inventory, Capacity & Channel Allocation

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listInventoryCapacityChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inventory-holds")
async def list_inventory_holds(request: Request) -> dict:
    """List leases

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listInventoryHolds", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/learning-model-performance")
async def list_learning_model_performance(request: Request) -> dict:
    """AI Learning, Model Performance & Optimization Feedback

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listLearningModelPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/location-venue-event")
async def list_location_venue_event(request: Request) -> dict:
    """Location, Venue & Event Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listLocationVenueEvent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/market-tourism-holiday")
async def list_market_tourism_holiday(request: Request) -> dict:
    """Market, Tourism, Holiday & Contextual Signal Hub

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listMarketTourismHoliday", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/market-venue-currency")
async def list_market_venue_currency(request: Request) -> dict:
    """Market, Venue & Currency Pricing Structure

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listMarketVenueCurrency", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-loyalty-guest")
async def list_membership_loyalty_guest(request: Request) -> dict:
    """Membership, Loyalty & Guest Eligibility

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listMembershipLoyaltyGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-loyalty-pricing")
async def list_membership_loyalty_pricing(request: Request) -> dict:
    """Membership & Loyalty Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listMembershipLoyaltyPricing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/multi-buy-quantity")
async def list_multi_buy_quantity(request: Request) -> dict:
    """Multi-Buy & Quantity Offer Configurator

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listMultiBuyQuantity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/nearby-event-exhibition")
async def list_nearby_event_exhibition(request: Request) -> dict:
    """Nearby Event, Exhibition & Local Demand Intelligence

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listNearbyEventExhibition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/next-best-action")
async def list_next_best_action(request: Request) -> dict:
    """AI Optimization & Next-Best-Action Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listNextBestAction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/offer-basket-trace")
async def list_offer_basket_trace(request: Request) -> dict:
    """Offer Simulation, Basket Trace & AI Optimization

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listOfferBasketTrace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/package-bundle-add")
async def list_package_bundle_add(request: Request) -> dict:
    """Package, Bundle & Add-On Pricing

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPackageBundleAdd", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-external-product")
async def list_partner_external_product(request: Request) -> dict:
    """Partner & External Product Bundle Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPartnerExternalProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-payment-eligibility")
async def list_partner_payment_eligibility(request: Request) -> dict:
    """Partner, B2B & Payment Eligibility

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPartnerPaymentEligibility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/payment-method-bank")
async def list_payment_method_bank(request: Request) -> dict:
    """Payment Method, Bank & Partner Discount Rules

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPaymentMethodBank", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/percentage-fixed-discount")
async def list_percentage_fixed_discount(request: Request) -> dict:
    """Percentage & Fixed Discount Configurator

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPercentageFixedDiscount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/events/{eventId}/performances")
async def list_performances(request: Request) -> dict:
    """List performances of an event

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listPerformances", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-calculation-sequence")
async def list_price_calculation_sequence(request: Request) -> dict:
    """Price Calculation Sequence & Formula Engine

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPriceCalculationSequence", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-category-rate")
async def list_price_category_rate(request: Request) -> dict:
    """Price Category & Rate Type Library

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPriceCategoryRate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-elasticity-revenue")
async def list_price_elasticity_revenue(request: Request) -> dict:
    """Price Elasticity & Revenue Response Intelligence

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPriceElasticityRevenue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-list-template")
async def list_price_list_template(request: Request) -> dict:
    """Price List Templates, Clone & Reuse

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPriceListTemplate", request.headers.get("x-scope-path", "uae"),
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


@app.get("/pricing")
async def list_pricing(request: Request) -> dict:
    """AI Pricing Intelligence Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-change-impact")
async def list_pricing_change_impact(request: Request) -> dict:
    """Pricing Change Impact Analysis

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingChangeImpact", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-compliance")
async def list_pricing_compliance(request: Request) -> dict:
    """Pricing History, Audit & Compliance Explorer

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingCompliance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-distribution-synchronization")
async def list_pricing_distribution_synchronization(request: Request) -> dict:
    """Pricing Distribution, Synchronization & Publication Monitor

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingDistributionSynchronization", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-governance")
async def list_pricing_governance(request: Request) -> dict:
    """Pricing Governance Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingGovernance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-recommendation-explainability")
async def list_pricing_recommendation_explainability(request: Request) -> dict:
    """AI Pricing Recommendation & Explainability Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingRecommendationExplainability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-rollback-emergency")
async def list_pricing_rollback_emergency(request: Request) -> dict:
    """Pricing Rollback & Emergency Control Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingRollbackEmergency", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-rule")
async def list_pricing_rule(request: Request) -> dict:
    """Pricing Rule Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-rule-priority")
async def list_pricing_rule_priority(request: Request) -> dict:
    """Pricing Rule Priority, Conflict Resolution & Testing

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingRulePriority", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/pricing-version-baseline")
async def list_pricing_version_baseline(request: Request) -> dict:
    """Pricing Version & Baseline Management

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPricingVersionBaseline", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-categories")
async def list_product_categories(request: Request) -> dict:
    """listProductCategories

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listProductCategories", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-duplication-template")
async def list_product_duplication_template(request: Request) -> dict:
    """Product Duplication & Template Library

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductDuplicationTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-governance")
async def list_product_governance(request: Request) -> dict:
    """Product Governance Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductGovernance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-import-export")
async def list_product_import_export(request: Request) -> dict:
    """Product Import / Export & Environment Transfer

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductImportExport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-lifecycle")
async def list_product_lifecycle(request: Request) -> dict:
    """Product Lifecycle Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductLifecycle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-price-availability")
async def list_product_price_availability(request: Request) -> dict:
    """Product, Price & Availability Synchronization

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductPriceAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-retirement-suspension")
async def list_product_retirement_suspension(request: Request) -> dict:
    """Product Retirement, Suspension & Archive

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductRetirementSuspension", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-trail-change")
async def list_product_trail_change(request: Request) -> dict:
    """Product Audit Trail & Change History

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listProductTrailChange", request.headers.get("x-scope-path", "uae"),
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


@app.get("/promotion-activity-version")
async def list_promotion_activity_version(request: Request) -> dict:
    """Promotion Audit, Activity & Version History

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionActivityVersion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-alert-exception")
async def list_promotion_alert_exception(request: Request) -> dict:
    """Promotion Alerts & Exception Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionAlertException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-campaign")
async def list_promotion_campaign(request: Request) -> dict:
    """Promotion & Campaign Directory

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-channel")
async def list_promotion_channel(request: Request) -> dict:
    """Promotion Channel & Publication Monitor

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-decision-trace")
async def list_promotion_decision_trace(request: Request) -> dict:
    """Promotion Decision Trace & Transaction Explainer

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionDecisionTrace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-exclusion-compatibility")
async def list_promotion_exclusion_compatibility(request: Request) -> dict:
    """Promotion Exclusion & Compatibility Matrix

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionExclusionCompatibility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-health-performance")
async def list_promotion_health_performance(request: Request) -> dict:
    """Promotion Health & Performance Monitor

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionHealthPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-lifecycle-statu")
async def list_promotion_lifecycle_status(request: Request) -> dict:
    """Promotion Lifecycle & Status Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionLifecycleStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-performance")
async def list_promotion_performance(request: Request) -> dict:
    """Promotion Performance Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotion-priority-hierarchy")
async def list_promotion_priority_hierarchy(request: Request) -> dict:
    """Promotion Priority & Hierarchy Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listPromotionPriorityHierarchy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/promotions")
async def list_promotions(request: Request) -> dict:
    """List promotions

    scope: venue · permission: PRICE_VIEW · offline: True
    """
    return await run("listPromotions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/quantity-group-volume")
async def list_quantity_group_volume(request: Request) -> dict:
    """Quantity, Group & Volume Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listQuantityGroupVolume", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/real-time-availability")
async def list_real_time_availability(request: Request) -> dict:
    """Real-Time Availability & Checkout Validation

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRealTimeAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/real-time-channel")
async def list_real_time_channel(request: Request) -> dict:
    """Real-Time Channel Availability & Inventory Monitor

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRealTimeChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/recommendation-review-decision")
async def list_recommendation_review_decision(request: Request) -> dict:
    """AI Recommendation Review & Decision Queue

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRecommendationReviewDecision", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/redemption")
async def list_redemption(request: Request) -> dict:
    """Redemption Analytics, Audit & AI Optimization

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRedemption", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/redemption-code-lookup")
async def list_redemption_code_lookup(request: Request) -> dict:
    """Redemption Monitor & Code Lookup

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRedemptionCodeLookup", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/redemption-conversion-funnel")
async def list_redemption_conversion_funnel(request: Request) -> dict:
    """Redemption, Conversion & Funnel Analytics

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRedemptionConversionFunnel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/redemption-discount-exposure")
async def list_redemption_discount_exposure(request: Request) -> dict:
    """Redemption, Discount & Exposure Limit Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRedemptionDiscountExposure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/residency-nationality-market")
async def list_residency_nationality_market(request: Request) -> dict:
    """Residency, Nationality & Market Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listResidencyNationalityMarket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/revenue")
async def list_revenue(request: Request) -> dict:
    """Revenue Optimization Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRevenue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/revenue-allocation-cost")
async def list_revenue_allocation_cost(request: Request) -> dict:
    """Revenue Allocation, Cost & Settlement Rules

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRevenueAllocationCost", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/revenue-demand-impact")
async def list_revenue_demand_impact(request: Request) -> dict:
    """Revenue & Demand Impact Forecasting

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRevenueDemandImpact", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reward-selection-substitution")
async def list_reward_selection_substitution(request: Request) -> dict:
    """Reward Selection, Substitution & Customer Choice

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listRewardSelectionSubstitution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/rollback-recovery")
async def list_rollback_recovery(request: Request) -> dict:
    """Rollback & Recovery Management

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRollbackRecovery", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/rule-priority-conflict")
async def list_rule_priority_conflict(request: Request) -> dict:
    """Rule Priority, Conflict Resolution & Dynamic Pricing Test Console

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listRulePriorityConflict", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/sale-channel")
async def list_sale_channel(request: Request) -> dict:
    """Sales Channel Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSaleChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/scenario-modeling-what")
async def list_scenario_modeling_what(request: Request) -> dict:
    """Scenario Modeling & What-If Analysis

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listScenarioModelingWhat", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seasonal-calendar-day")
async def list_seasonal_calendar_day(request: Request) -> dict:
    """Seasonal, Calendar, Day & Timeslot Dynamic Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSeasonalCalendarDay", request.headers.get("x-scope-path", "uae"),
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


@app.get("/signal-data-quality")
async def list_signal_data_quality(request: Request) -> dict:
    """AI Signal Registry, Data Quality & Model Governance

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSignalDataQuality", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/special-price-guest")
async def list_special_price_guest(request: Request) -> dict:
    """Special Price & Guest Offer Configurator

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listSpecialPriceGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stacking-conflict")
async def list_stacking_conflict(request: Request) -> dict:
    """Stacking & Conflict Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listStackingConflict", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/targeting-conflict-frequency")
async def list_targeting_conflict_frequency(request: Request) -> dict:
    """Targeting Conflict, Frequency & Exclusion Controls

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listTargetingConflictFrequency", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/targeting-eligibility")
async def list_targeting_eligibility(request: Request) -> dict:
    """Targeting & Eligibility Command Center

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listTargetingEligibility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tax-fee-calculation")
async def list_tax_fee_calculation(request: Request) -> dict:
    """Tax, Fee & Calculation Command Center

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listTaxFeeCalculation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/threshold-action-automatic")
async def list_threshold_action_automatic(request: Request) -> dict:
    """Threshold Actions & Automatic Suspension

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listThresholdActionAutomatic", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/time-based-seasonal")
async def list_time_based_seasonal(request: Request) -> dict:
    """Time-Based & Seasonal Discount Rules

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listTimeBasedSeasonal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/timeslot-performance-time")
async def list_timeslot_performance_time(request: Request) -> dict:
    """Timeslot, Performance & Time-of-Day Pricing Rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listTimeslotPerformanceTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/unique-code-generation")
async def list_unique_code_generation(request: Request) -> dict:
    """Unique Code Generation & Batch Manager

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listUniqueCodeGeneration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upsell-cross-sell")
async def list_upsell_cross_sell(request: Request) -> dict:
    """Upsell, Cross-Sell & Attach-Rate Analytics

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listUpsellCrossSell", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upsell-rules")
async def list_upsell_rules(request: Request) -> dict:
    """List upsell and cross-sell rules

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listUpsellRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/usage-capacity-frequency")
async def list_usage_capacity_frequency(request: Request) -> dict:
    """Usage, Capacity & Frequency Control

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listUsageCapacityFrequency", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/validity-date-time")
async def list_validity_date_time(request: Request) -> dict:
    """Validity, Date & Time Control

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listValidityDateTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/volume-bulk-tier")
async def list_volume_bulk_tier(request: Request) -> dict:
    """Volume, Bulk & Tier Discount Configurator

    scope: venue · permission: PRICE_VIEW · offline: False
    """
    return await run("listVolumeBulkTier", request.headers.get("x-scope-path", "uae"),
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


@app.get("/weather-demand-impact")
async def list_weather_demand_impact(request: Request) -> dict:
    """Weather Intelligence & Demand Impact Configuration

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listWeatherDemandImpact", request.headers.get("x-scope-path", "uae"),
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


@app.put("/activation-scheduler")
async def publish_activation_scheduler(request: Request) -> dict:
    """Publication & Activation Scheduler

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishActivationScheduler", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/catalogue/bundles")
async def publish_bundle(request: Request) -> dict:
    """Compute, sign and publish a catalogue bundle

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishBundle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-availability")
async def publish_channel_availability(request: Request) -> dict:
    """Channel Publication & Availability

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishChannelAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-readiness-validation")
async def publish_channel_readiness_validation(request: Request) -> dict:
    """Channel Publication, Readiness & AI Validation

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishChannelReadinessValidation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pricing-effective-date")
async def publish_pricing_effective_date(request: Request) -> dict:
    """Pricing Publication & Effective-Date Scheduler

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("publishPricingEffectiveDate", request.headers.get("x-scope-path", "uae"),
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


@app.post("/channel-capacities/{channelCapacityId}/channel-allocations/release")
async def relinquish_channel_allocation(request: Request) -> dict:
    """Return unsold channel allocation to the general pool

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("relinquishChannelAllocation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/inventory-holds/{inventoryHoldId}")
async def relinquish_inventory_hold(request: Request) -> dict:
    """Return unsold units

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("relinquishInventoryHold", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/seat-blocks/{blockId}")
async def relinquish_seat_block(request: Request) -> dict:
    """Release a block back to sale

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("relinquishSeatBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/seat-holds/{holdId}")
async def relinquish_seat_hold(request: Request) -> dict:
    """Release a hold

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("relinquishSeatHold", request.headers.get("x-scope-path", "uae"),
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


@app.put("/booking-velocity-time")
async def set_booking_velocity_time(request: Request) -> dict:
    """Booking Velocity & Time-to-Event Rule Builder

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setBookingVelocityTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/bundle-component")
async def set_bundle_component(request: Request) -> dict:
    """Bundle Component Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setBundleComponent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/bundle-definition")
async def set_bundle_definition(request: Request) -> dict:
    """Bundle Definition & Setup

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setBundleDefinition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/buy-get-bogo")
async def set_buy_get_bogo(request: Request) -> dict:
    """Buy X Get Y / BOGO Rule Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setBuyGetBogo", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/campaign-budget-financial")
async def set_campaign_budget_financial(request: Request) -> dict:
    """Campaign Budget & Financial Limit Setup

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setCampaignBudgetFinancial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/catalogue-review")
async def set_catalogue_review(request: Request) -> dict:
    """AI Catalogue Builder & Configuration Review

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setCatalogueReview", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-capacities/{channelCapacityId}/channel-allocations")
async def set_channel_allocations(request: Request) -> dict:
    """Allocate envelope capacity across channels

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("setChannelAllocations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-fee-payment")
async def set_channel_fee_payment(request: Request) -> dict:
    """Channel Fees, Payment & Fulfillment Configuration

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setChannelFeePayment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-pricing-commercial")
async def set_channel_pricing_commercial(request: Request) -> dict:
    """Channel Pricing & Commercial Profile Assignment

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setChannelPricingCommercial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/code-distribution-manager")
async def set_code_distribution_manager(request: Request) -> dict:
    """Code Distribution & Assignment Manager

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setCodeDistributionManager", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/coupon-promo-code")
async def set_coupon_promo_code(request: Request) -> dict:
    """Coupon & Promo Code Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setCouponPromoCode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/cross-category-promotion")
async def set_cross_category_promotion(request: Request) -> dict:
    """Cross-Category Promotion Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setCrossCategoryPromotion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/demand-occupancy-availability")
async def set_demand_occupancy_availability(request: Request) -> dict:
    """Demand, Occupancy & Availability Rule Builder

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setDemandOccupancyAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/dynamic-pricing-strategy")
async def set_dynamic_pricing_strategy(request: Request) -> dict:
    """Dynamic Pricing Strategy Builder

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setDynamicPricingStrategy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/eligibility-rule")
async def set_eligibility_rule(request: Request) -> dict:
    """Eligibility Rule Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setEligibilityRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/fee-applicability-charging")
async def set_fee_applicability_charging(request: Request) -> dict:
    """Fee Applicability & Charging Rule Builder

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setFeeApplicabilityCharging", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/fixed-price-offer")
async def set_fixed_price_offer(request: Request) -> dict:
    """Fixed-Price & “N for X” Offer Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setFixedPriceOffer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/gift-free-product")
async def set_gift_free_product(request: Request) -> dict:
    """Gift, Free Product & Added-Value Offer Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setGiftFreeProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/guest-choice-build")
async def set_guest_choice_build(request: Request) -> dict:
    """Guest Choice & Build-Your-Own Bundle Designer

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setGuestChoiceBuild", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/lifecycle-statu-workflow")
async def set_lifecycle_statu_workflow(request: Request) -> dict:
    """Lifecycle Status & Workflow Configuration

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setLifecycleStatuWorkflow", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/seat-maps/{seatMapId}/zones")
async def set_map_zones(request: Request) -> dict:
    """Standing areas, suites, stages and obstructions

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("setMapZones", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/price-hierarchy-inheritance")
async def set_price_hierarchy_inheritance(request: Request) -> dict:
    """Price Hierarchy & Inheritance Configuration

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setPriceHierarchyInheritance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/price-list-master")
async def set_price_list_master(request: Request) -> dict:
    """Price List Master Configuration

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setPriceListMaster", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/price-lists/{priceListId}/prices")
async def set_prices(request: Request) -> dict:
    """Set prices in bulk

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setPrices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pricing")
async def set_pricing(request: Request) -> dict:
    """Pricing Simulation Studio

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setPricing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pricing-change-request")
async def set_pricing_change_request(request: Request) -> dict:
    """Pricing Change Request & Workspace

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setPricingChangeRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pricing-experiment")
async def set_pricing_experiment(request: Request) -> dict:
    """A/B Pricing Experiment Studio

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setPricingExperiment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/products/{productId}/attributes")
async def set_product_attributes(request: Request) -> dict:
    """Set the attribute axes for a product

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductAttributes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/product-catalogue")
async def set_product_catalogue(request: Request) -> dict:
    """Product & Catalogue Assignment

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductCatalogue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/product-categories")
async def set_product_categories(request: Request) -> dict:
    """setProductCategories

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductCategories", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/product-context-ownership")
async def set_product_context_ownership(request: Request) -> dict:
    """Product Context, Ownership & Assignment

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductContextOwnership", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/product-service-price")
async def set_product_service_price(request: Request) -> dict:
    """Product & Service Price Assignment

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setProductServicePrice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/promotion-rule")
async def set_promotion_rule(request: Request) -> dict:
    """Promotion Rule Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setPromotionRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/promotion-stacking-rule")
async def set_promotion_stacking_rule(request: Request) -> dict:
    """Promotion Stacking Rule Builder

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setPromotionStackingRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/promotions/{promotionId}/variants")
async def set_promotion_variants(request: Request) -> dict:
    """A/B test two versions against each other

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setPromotionVariants", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/rate-structure")
async def set_rate_structure(request: Request) -> dict:
    """Rate Structure Builder

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setRateStructure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/rule-test-recommendation")
async def set_rule_test_recommendation(request: Request) -> dict:
    """Rule Test, Simulation & AI Recommendation Workspace

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("setRuleTestRecommendation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/seat-maps/{seatMapId}/rules")
async def set_seating_rules(request: Request) -> dict:
    """Set seating rules

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("setSeatingRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tax-profile-jurisdiction")
async def set_tax_profile_jurisdiction(request: Request) -> dict:
    """Tax Profile & Jurisdiction Configuration

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setTaxProfileJurisdiction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tax-rule-treatment")
async def set_tax_rule_treatment(request: Request) -> dict:
    """Tax Rule & Treatment Builder

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setTaxRuleTreatment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/bundle-preview-recommendation")
async def simulate_bundle_preview_recommendation(request: Request) -> dict:
    """Bundle Preview, Simulation & AI Recommendation

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("simulateBundlePreviewRecommendation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/price-breakdown-calculation")
async def simulate_price_breakdown_calculation(request: Request) -> dict:
    """Price Breakdown, Calculation Simulation & Explainability

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("simulatePriceBreakdownCalculation", request.headers.get("x-scope-path", "uae"),
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

