"""InventoryService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

50 operations · 18 tables touched · scope levels: region, tenant, venue
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="InventoryService", docs_url="/_docs")

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
    return {"service": "InventoryService", "operations": 50,
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



@app.post("/purchase-orders/{purchaseOrderId}/acknowledge")
async def acknowledge_purchase_order(request: Request) -> dict:
    """Record the supplier acknowledgement

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("acknowledgePurchaseOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/requisitions/{requisitionId}/approve")
async def approve_requisition(request: Request) -> dict:
    """Approve or reject a requisition

    scope: venue · permission: APPROVAL_ACT · offline: False
    """
    return await run("approveRequisition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/products/bulk")
async def bulk_update_products(request: Request) -> dict:
    """Change many products at once, with a preview

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("bulkUpdateProducts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/purchase-orders/{purchaseOrderId}/cancel")
async def cancel_purchase_order(request: Request) -> dict:
    """Cancel a purchase order

    scope: venue · permission: ORDER_CANCEL · offline: False
    """
    return await run("cancelPurchaseOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/requisitions/{requisitionId}/cancel")
async def cancel_requisition(request: Request) -> dict:
    """Cancel a requisition

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("cancelRequisition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts/{countId}/cancel")
async def cancel_stock_count(request: Request) -> dict:
    """Abandon a count

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("cancelStockCount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/purchase-orders/{purchaseOrderId}/close-short")
async def close_purchase_order_short(request: Request) -> dict:
    """Close an order accepting the balance will not arrive

    scope: venue · permission: LEDGER_APPROVE · offline: False
    """
    return await run("closePurchaseOrderShort", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-transfers/{transferId}/close-short")
async def close_transfer_short(request: Request) -> dict:
    """Close a transfer accepting the balance will not arrive

    scope: venue · permission: LEDGER_APPROVE · offline: False
    """
    return await run("closeTransferShort", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/requisitions/{requisitionId}/quotations")
async def compare_quotations(request: Request) -> dict:
    """Compare quotations for a requisition

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("compareQuotations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/goods-receipts")
async def create_goods_receipt(request: Request) -> dict:
    """Receive goods against a purchase order

    scope: venue · permission: PRODUCT_CONFIGURE · offline: True
    """
    return await run("createGoodsReceipt", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inventory-items")
async def create_inventory_item(request: Request) -> dict:
    """Create an inventory item

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createInventoryItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/purchase-orders")
async def create_purchase_order(request: Request) -> dict:
    """Raise a purchase order

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createPurchaseOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/requisitions")
async def create_requisition(request: Request) -> dict:
    """Raise a requisition

    scope: venue · permission: ORDER_CREATE · offline: True
    """
    return await run("createRequisition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-locations")
async def create_stock_location(request: Request) -> dict:
    """Create a stock location

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createStockLocation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-movements")
async def create_stock_movement(request: Request) -> dict:
    """Record an issue, return or adjustment

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createStockMovement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-transfers")
async def create_stock_transfer(request: Request) -> dict:
    """Send stock to another location

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createStockTransfer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/suppliers")
async def create_supplier(request: Request) -> dict:
    """Create a supplier

    scope: region · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createSupplier", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-counts/{countId}/variance")
async def get_count_variance(request: Request) -> dict:
    """Variance between counted and expected

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getCountVariance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inventory-items/{itemId}")
async def get_inventory_item(request: Request) -> dict:
    """Read an item with stock position

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getInventoryItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/purchase-orders/{purchaseOrderId}")
async def get_purchase_order(request: Request) -> dict:
    """Read a purchase order with receipt progress

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getPurchaseOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock")
async def get_stock_positions(request: Request) -> dict:
    """Stock on hand by item and location

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getStockPositions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-transfers/{transferId}")
async def get_stock_transfer(request: Request) -> dict:
    """One transfer, its manifest and where it is

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("getStockTransfer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock/valuation")
async def get_stock_valuation(request: Request) -> dict:
    """Stock value by location and category

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("getStockValuation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/requisitions/suggested")
async def get_suggested_requisitions(request: Request) -> dict:
    """Draft requisitions from reorder points

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getSuggestedRequisitions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-batches/expiring")
async def list_expiring_batches(request: Request) -> dict:
    """What is about to go out of date

    scope: venue · permission: INVENTORY_VIEW · offline: True
    """
    return await run("listExpiringBatches", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/goods-receipts")
async def list_goods_receipts(request: Request) -> dict:
    """List goods receipts

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listGoodsReceipts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inventory-items")
async def list_inventory_items(request: Request) -> dict:
    """List inventory items

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listInventoryItems", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/purchase-orders")
async def list_purchase_orders(request: Request) -> dict:
    """List purchase orders

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listPurchaseOrders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/requisitions")
async def list_requisitions(request: Request) -> dict:
    """List requisitions

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listRequisitions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/serialised-items")
async def list_serialised_items(request: Request) -> dict:
    """listSerialisedItems

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listSerialisedItems", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-counts")
async def list_stock_counts(request: Request) -> dict:
    """List stock counts

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listStockCounts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-locations")
async def list_stock_locations(request: Request) -> dict:
    """List stock locations

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listStockLocations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-movements")
async def list_stock_movements(request: Request) -> dict:
    """The movement ledger

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listStockMovements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/stock-transfers")
async def list_stock_transfers(request: Request) -> dict:
    """List transfers

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listStockTransfers", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/suppliers")
async def list_suppliers(request: Request) -> dict:
    """List suppliers

    scope: region · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listSuppliers", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/inventory-items/lookup")
async def lookup_inventory_item(request: Request) -> dict:
    """Look up by barcode or SKU

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("lookupInventoryItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts/{countId}/post")
async def post_stock_count(request: Request) -> dict:
    """Post a count and adjust stock

    scope: venue · permission: LEDGER_POST · offline: False
    """
    return await run("postStockCount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-transfers/{transferId}/receive")
async def receive_stock_transfer(request: Request) -> dict:
    """Receive a transfer

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("receiveStockTransfer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/suppliers/{supplierId}/quotations")
async def record_quotation(request: Request) -> dict:
    """Record a supplier quotation

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("recordQuotation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts/{countId}/recount")
async def recount_stock_count(request: Request) -> dict:
    """Send a count back to be recounted

    scope: venue · permission: LEDGER_APPROVE · offline: False
    """
    return await run("recountStockCount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/goods-receipts/{receiptId}/reject")
async def reject_received_goods(request: Request) -> dict:
    """Reject received goods

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("rejectReceivedGoods", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/requisitions/{requisitionId}/reject")
async def reject_requisition(request: Request) -> dict:
    """Reject a requisition

    scope: venue · permission: LEDGER_APPROVE · offline: False
    """
    return await run("rejectRequisition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/requisitions/{requisitionId}/return")
async def return_requisition(request: Request) -> dict:
    """Return a requisition for more information

    scope: venue · permission: LEDGER_APPROVE · offline: False
    """
    return await run("returnRequisition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/purchase-orders/{purchaseOrderId}/send")
async def send_purchase_order(request: Request) -> dict:
    """Issue the order to the supplier

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("sendPurchaseOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/stock-counts/daily")
async def set_daily_count(request: Request) -> dict:
    """Which items get counted every day

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setDailyCount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts")
async def start_stock_count(request: Request) -> dict:
    """Start a stock count

    scope: venue · permission: PRODUCT_CONFIGURE · offline: True
    """
    return await run("startStockCount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stock-counts/{countId}/lines")
async def submit_count_lines(request: Request) -> dict:
    """Submit counted quantities

    scope: venue · permission: PRODUCT_CONFIGURE · offline: True
    """
    return await run("submitCountLines", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/inventory-items/{itemId}")
async def update_inventory_item(request: Request) -> dict:
    """Amend an item

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateInventoryItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/requisitions/{requisitionId}/lines")
async def update_requisition_lines(request: Request) -> dict:
    """Change what an outlet is asking for, before it is approved

    scope: venue · permission: PRODUCT_CONFIGURE · offline: True
    """
    return await run("updateRequisitionLines", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/suppliers/{supplierId}")
async def update_supplier(request: Request) -> dict:
    """Change terms, or stop buying from them

    scope: tenant · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateSupplier", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

