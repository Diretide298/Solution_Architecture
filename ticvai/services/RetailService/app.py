"""RetailService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

37 operations · 15 tables touched · scope levels: venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="RetailService", docs_url="/_docs")

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
    return {"service": "RetailService", "operations": 37,
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



@app.post("/gift-cards/{giftCardId}/activate")
async def activate_gift_card(request: Request) -> dict:
    """Activate a card at the point of sale

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("activateGiftCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallets/{subjectId}/adjust")
async def adjust_wallet(request: Request) -> dict:
    """Manually adjust a wallet balance

    scope: venue · permission: LEDGER_POST · offline: False
    """
    return await run("adjustWallet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/gift-cards/{cardCode}/block")
async def block_gift_card(request: Request) -> dict:
    """Block a gift card

    scope: venue · permission: PRICE_CONFIGURE · offline: False
    """
    return await run("blockGiftCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/merchandise-reservations/{reservationId}/cancel")
async def cancel_merchandise_reservation(request: Request) -> dict:
    """Release a reservation

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("cancelMerchandiseReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallets/{walletId}/close")
async def close_wallet(request: Request) -> dict:
    """Close a wallet

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("closeWallet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/merchandise-reservations/{reservationId}/collect")
async def collect_merchandise_reservation(request: Request) -> dict:
    """The guest picked it up

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("collectMerchandiseReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shop-and-drop/{dropId}/collect")
async def collect_shop_and_drop(request: Request) -> dict:
    """Hand the goods over

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("collectShopAndDrop", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/merchandise")
async def create_merchandise(request: Request) -> dict:
    """Create a merchandise item

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("createMerchandise", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/retail-exchanges")
async def create_retail_exchange(request: Request) -> dict:
    """Exchange one item for another

    scope: venue · permission: ORDER_EXCHANGE · offline: False
    """
    return await run("createRetailExchange", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/retail-returns")
async def create_retail_return(request: Request) -> dict:
    """Accept a return

    scope: venue · permission: ORDER_REFUND · offline: False
    """
    return await run("createRetailReturn", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/retail-sales")
async def create_retail_sale(request: Request) -> dict:
    """Sell merchandise

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("createRetailSale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shop-and-drop")
async def create_shop_and_drop(request: Request) -> dict:
    """Buy now, collect on the way out

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("createShopAndDrop", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shop-and-drop/{dropId}/dispose")
async def dispose_shop_and_drop(request: Request) -> dict:
    """Dispose of an uncollected item

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("disposeShopAndDrop", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/gift-cards/{cardCode}")
async def get_gift_card(request: Request) -> dict:
    """Check a gift card balance

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getGiftCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/outlets/{outletId}/stock-check")
async def get_outlet_stock(request: Request) -> dict:
    """Stock across an outlet

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("getOutletStock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/retail-sales/{saleId}")
async def get_retail_sale(request: Request) -> dict:
    """Read a retail sale

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getRetailSale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/outlets/{outletId}/return-policy")
async def get_return_policy(request: Request) -> dict:
    """Read the retail return policy

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getReturnPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/wallets/{subjectId}")
async def get_wallet(request: Request) -> dict:
    """Read a guest wallet

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getWallet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/gift-cards")
async def issue_gift_card(request: Request) -> dict:
    """Issue or activate a gift card

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("issueGiftCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/merchandise")
async def list_merchandise(request: Request) -> dict:
    """List merchandise

    scope: venue · permission: PRODUCT_VIEW · offline: True
    """
    return await run("listMerchandise", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/retail-returns")
async def list_retail_returns(request: Request) -> dict:
    """List returns

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listRetailReturns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/retail-sales")
async def list_retail_sales(request: Request) -> dict:
    """List retail sales

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listRetailSales", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/store-rules")
async def list_store_rules(request: Request) -> dict:
    """Rules and controls in force in the store

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("listStoreRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/wallets/{subjectId}/transactions")
async def list_wallet_transactions(request: Request) -> dict:
    """Wallet transaction history

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listWalletTransactions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/merchandise/lookup")
async def lookup_merchandise(request: Request) -> dict:
    """Price and stock check by barcode

    scope: venue · permission: PRODUCT_VIEW · offline: False
    """
    return await run("lookupMerchandise", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/retail-sales/lookup")
async def lookup_retail_sale(request: Request) -> dict:
    """Find a sale from a receipt

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("lookupRetailSale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/shop-and-drop/lookup")
async def lookup_shop_and_drop(request: Request) -> dict:
    """Find a guest's dropped goods

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("lookupShopAndDrop", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/gift-cards/{giftCardId}/redeem")
async def redeem_gift_card(request: Request) -> dict:
    """Spend against a card

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("redeemGiftCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallets/{walletId}/reinstate")
async def reinstate_wallet(request: Request) -> dict:
    """Unfreeze a wallet

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("reinstateWallet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/retail-sales/{saleId}/reprint")
async def reprint_receipt(request: Request) -> dict:
    """Reprint or resend a receipt

    scope: venue · permission: ORDER_REPRINT · offline: False
    """
    return await run("reprintReceipt", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/outlets/{outletId}/reserve")
async def reserve_merchandise(request: Request) -> dict:
    """Reserve an item for collection

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("reserveMerchandise", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/outlets/{outletId}/return-policy")
async def set_return_policy(request: Request) -> dict:
    """Set the retail return policy

    scope: venue · permission: REGION_CONFIGURE · offline: False
    """
    return await run("setReturnPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/store-rules")
async def set_store_rules(request: Request) -> dict:
    """Change a store rule

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("setStoreRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallets/{walletId}/suspend")
async def suspend_wallet(request: Request) -> dict:
    """Freeze a wallet

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("suspendWallet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallets/{subjectId}/top-ups")
async def top_up_wallet(request: Request) -> dict:
    """Add value to a wallet

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("topUpWallet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallets/{walletId}/transfer")
async def transfer_wallet_balance(request: Request) -> dict:
    """Send balance to another guest

    scope: venue · permission: WALLET_MANAGE · offline: False
    """
    return await run("transferWalletBalance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/merchandise/{merchandiseId}")
async def update_merchandise(request: Request) -> dict:
    """Amend a merchandise item

    scope: venue · permission: PRODUCT_CONFIGURE · offline: False
    """
    return await run("updateMerchandise", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

