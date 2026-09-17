"""OrderService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

187 operations · 59 tables touched · scope levels: tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="OrderService", docs_url="/_docs")

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
    return {"service": "OrderService", "operations": 187,
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



@app.delete("/carts/{cartId}")
async def abandon_cart(request: Request) -> dict:
    """Empty it deliberately

    scope: venue · permission: - · offline: False
    """
    return await run("abandonCart", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/accept-variance")
async def accept_shift_variance(request: Request) -> dict:
    """Accept an over/short beyond the threshold

    scope: venue · permission: OVERSHORT_ACCEPT · offline: False
    """
    return await run("acceptShiftVariance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/carts/{cartId}/lines")
async def add_cart_line(request: Request) -> dict:
    """Add something

    scope: venue · permission: - · offline: False
    """
    return await run("addCartLine", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payments/{paymentId}/tip")
async def add_tip(request: Request) -> dict:
    """Record a tip against a payment

    scope: workstation · permission: ORDER_MODIFY · offline: True
    """
    return await run("addTip", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/deposit-boxes/{boxId}/adjust-float")
async def adjust_deposit_box_float(request: Request) -> dict:
    """Change the initial fund

    scope: venue · permission: CASH_ADD · offline: False
    """
    return await run("adjustDepositBoxFloat", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/deposit-boxes")
async def allocate_deposit_box(request: Request) -> dict:
    """Give a cashier a box and a float

    scope: venue · permission: SHIFT_OPEN · offline: True
    """
    return await run("allocateDepositBox", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/media/{mediaCode}/entitlements")
async def append_entitlement_to_media(request: Request) -> dict:
    """Add something to a ticket the guest already holds

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("appendEntitlementToMedia", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/discounts")
async def apply_manual_discount(request: Request) -> dict:
    """Apply a discount a cashier chose

    scope: workstation · permission: ORDER_DISCOUNT · offline: True
    """
    return await run("applyManualDiscount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/exception-service-recovery")
async def approve_exception_service_recovery(request: Request) -> dict:
    """Approval, Exception & Service Recovery Management

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("approveExceptionServiceRecovery", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/group-discount-exception")
async def approve_group_discount_exception(request: Request) -> dict:
    """Group Discount, Exception & Approval Workflow

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("approveGroupDiscountException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/listing-moderation")
async def approve_listing_moderation(request: Request) -> dict:
    """Listing Approval & Moderation

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("approveListingModeration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/refunds/{refundId}/approve")
async def approve_refund(request: Request) -> dict:
    """Approve a refund held for approval

    scope: venue · permission: ORDER_REFUND_APPROVE · offline: False
    """
    return await run("approveRefund", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/approve-open")
async def approve_shift_open(request: Request) -> dict:
    """Approve a shift opening outside tolerance

    scope: venue · permission: SHIFT_APPROVE_OPEN · offline: False
    """
    return await run("approveShiftOpen", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stored-value/authorisations")
async def authorise_stored_value(request: Request) -> dict:
    """Hold a balance on any stored-value instrument

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("authoriseStoredValue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/reservations/{reservationId}")
async def cancel_reservation(request: Request) -> dict:
    """Cancel a reservation

    scope: venue · permission: ORDER_CANCEL · offline: False
    """
    return await run("cancelReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payments/{paymentId}/capture")
async def capture_payment(request: Request) -> dict:
    """Capture a previously authorised payment

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("capturePayment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stored-value/authorisations/{authorisationId}/capture")
async def capture_stored_value(request: Request) -> dict:
    """Take some or all of a held balance

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("captureStoredValue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/carts/{cartId}/checkout")
async def checkout_cart(request: Request) -> dict:
    """Turn the cart into an order

    scope: venue · permission: - · offline: False
    """
    return await run("checkoutCart", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/carts/{cartId}/claim")
async def claim_cart(request: Request) -> dict:
    """Attach an anonymous cart to a guest

    scope: venue · permission: - · offline: False
    """
    return await run("claimCart", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ticket-transfers/{transferId}/claim")
async def claim_ticket_transfer(request: Request) -> dict:
    """Claim transferred tickets

    scope: venue · permission: - · offline: False
    """
    return await run("claimTicketTransfer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/deposit-boxes/close")
async def close_deposit_boxes(request: Request) -> dict:
    """Close one box or all of them

    scope: venue · permission: SHIFT_CLOSE · offline: False
    """
    return await run("closeDepositBoxes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/close")
async def close_shift(request: Request) -> dict:
    """Blind close-out

    scope: workstation · permission: SHIFT_CLOSE · offline: True
    """
    return await run("closeShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reservations/{reservationId}/convert")
async def convert_reservation(request: Request) -> dict:
    """Convert a reservation into an order

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("convertReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/convert-to-term")
async def convert_to_term_product(request: Request) -> dict:
    """Turn a visit into a membership or season pass

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("convertToTermProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/refunds/bulk")
async def create_bulk_refund(request: Request) -> dict:
    """Refund every order against an event, performance or date

    scope: venue · permission: ORDER_REFUND_BULK · offline: False
    """
    return await run("createBulkRefund", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/carts")
async def create_cart(request: Request) -> dict:
    """Start a cart

    scope: venue · permission: - · offline: False
    """
    return await run("createCart", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/cash-movements")
async def create_cash_movement(request: Request) -> dict:
    """Record a cash lift or add

    scope: venue · permission: CASH_LIFT · offline: True
    """
    return await run("createCashMovement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/listing-seller")
async def create_listing_seller(request: Request) -> dict:
    """Listing Creation & Seller Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createListingSeller", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders")
async def create_order(request: Request) -> dict:
    """Create an order

    scope: workstation · permission: ORDER_CREATE · offline: True
    """
    return await run("createOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/order-source-channel")
async def create_order_source_channel(request: Request) -> dict:
    """Order Creation & Source/Channel Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createOrderSourceChannel", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payments")
async def create_payment(request: Request) -> dict:
    """Take a payment against an order

    scope: workstation · permission: ORDER_CREATE · offline: True
    """
    return await run("createPayment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payment-links")
async def create_payment_link(request: Request) -> dict:
    """Send a guest a link to pay later

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createPaymentLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/refunds")
async def create_refund(request: Request) -> dict:
    """Refund an order, wholly or in part

    scope: venue · permission: ORDER_REFUND · offline: False
    """
    return await run("createRefund", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/refund-requests")
async def create_refund_request(request: Request) -> dict:
    """Guest-initiated refund request

    scope: venue · permission: - · offline: False
    """
    return await run("createRefundRequest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/resale-listings")
async def create_resale_listing(request: Request) -> dict:
    """List an entitlement for resale

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createResaleListing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reservations")
async def create_reservation(request: Request) -> dict:
    """Hold without payment

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/upgrade-credential-regeneration")
async def create_upgrade_credential_regeneration(request: Request) -> dict:
    """Upgrade Execution, Credential Regeneration & Channel Controls

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("createUpgradeCredentialRegeneration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/exchanges")
async def exchange_order_lines(request: Request) -> dict:
    """Exchange lines for different products or dates

    scope: venue · permission: ORDER_EXCHANGE · offline: False
    """
    return await run("exchangeOrderLines", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/carts/{cartId}/extend")
async def extend_cart(request: Request) -> dict:
    """Give the guest more time

    scope: venue · permission: - · offline: False
    """
    return await run("extendCart", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reservations/{reservationId}/extend")
async def extend_reservation(request: Request) -> dict:
    """Extend a reservation

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("extendReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/b2b-accounts/{accountId}/credit")
async def get_b2b_credit(request: Request) -> dict:
    """Partner credit position

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getB2bCredit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/carts/{cartId}")
async def get_cart(request: Request) -> dict:
    """The cart, priced and checked, right now

    scope: venue · permission: - · offline: False
    """
    return await run("getCart", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/shifts/current")
async def get_current_shift(request: Request) -> dict:
    """The open or suspended shift on the session's workstation

    scope: workstation · permission: SHIFT_OPEN · offline: True
    """
    return await run("getCurrentShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-bookings/{groupBookingId}")
async def get_group_booking(request: Request) -> dict:
    """getGroupBooking

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getGroupBooking", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media/{mediaCode}/entitlements")
async def get_media_entitlements(request: Request) -> dict:
    """What is already on this media

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getMediaEntitlements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/orders/{orderId}")
async def get_order(request: Request) -> dict:
    """Read an order

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/orders/{orderId}/statement")
async def get_order_statement(request: Request) -> dict:
    """Full financial history of an order

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getOrderStatement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/payment-links/{token}")
async def get_payment_link(request: Request) -> dict:
    """getPaymentLink

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getPaymentLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venues/{venueId}/refund-policy")
async def get_refund_policy(request: Request) -> dict:
    """Read a venue's refund policy

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getRefundPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reservations/{reservationId}")
async def get_reservation(request: Request) -> dict:
    """Read a reservation

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/shifts/{shiftId}")
async def get_shift(request: Request) -> dict:
    """Read a shift

    scope: venue · permission: REPORT_VIEW_WORKSTATION · offline: True
    """
    return await run("getShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/hold")
async def hold_order(request: Request) -> dict:
    """Park a sale and free the till

    scope: workstation · permission: ORDER_MODIFY · offline: True
    """
    return await run("holdOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payments/{paymentId}/inquiry")
async def inquire_payment_status(request: Request) -> dict:
    """Ask the provider what actually happened

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("inquirePaymentStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invitations")
async def issue_invitation(request: Request) -> dict:
    """Issue a complimentary entitlement, with no payment expected

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("issueInvitation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallet-passes")
async def issue_wallet_pass(request: Request) -> dict:
    """Generate an Apple or Google wallet pass

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("issueWalletPass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/carts/abandoned")
async def list_abandoned_carts(request: Request) -> dict:
    """Carts that lapsed without checking out

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("listAbandonedCarts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/amendment-after-sale")
async def list_amendment_after_sale(request: Request) -> dict:
    """Amendment & After-Sales Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listAmendmentAfterSale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/amendment-after-sale")
async def list_amendment_after_sale2(request: Request) -> dict:
    """Amendment History, Audit & After-Sales Analytics

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listAmendmentAfterSale2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/bulk-group-assisted")
async def list_bulk_group_assisted(request: Request) -> dict:
    """Bulk, Group & Assisted Upgrade Operations

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listBulkGroupAssisted", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/buyer-checkout-inventory")
async def list_buyer_checkout_inventory(request: Request) -> dict:
    """Buyer Checkout, Inventory Hold & Secure Payment

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listBuyerCheckoutInventory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/buyer-purchase-resale")
async def list_buyer_purchase_resale(request: Request) -> dict:
    """Buyer Purchase & Resale Order Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listBuyerPurchaseResale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/capacity-inventory-reconciliation")
async def list_capacity_inventory_reconciliation(request: Request) -> dict:
    """Capacity & Inventory Reconciliation

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listCapacityInventoryReconciliation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/capacity-reservation-inventory")
async def list_capacity_reservation_inventory(request: Request) -> dict:
    """Capacity Reservation & Inventory Commitment

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listCapacityReservationInventory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/shifts/{shiftId}/cash-movements")
async def list_cash_movements(request: Request) -> dict:
    """Lifts, adds and the opening float

    scope: venue · permission: REPORT_VIEW_WORKSTATION · offline: True
    """
    return await run("listCashMovements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/chargebacks")
async def list_chargebacks(request: Request) -> dict:
    """Open disputes, by deadline

    scope: venue · permission: ORDER_REFUND_APPROVE · offline: False
    """
    return await run("listChargebacks", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/create-listing-resale")
async def list_create_listing_resale(request: Request) -> dict:
    """Create Listing & Resale Price Selection

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listCreateListingResale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-revocation-regeneration")
async def list_credential_revocation_regeneration(request: Request) -> dict:
    """Credential Revocation & Regeneration

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listCredentialRevocationRegeneration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/denominations")
async def list_denominations(request: Request) -> dict:
    """listDenominations

    scope: venue · permission: SHIFT_OPEN · offline: True
    """
    return await run("listDenominations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/deposit-boxes")
async def list_deposit_boxes(request: Request) -> dict:
    """Cash boxes and who holds them

    scope: venue · permission: SHIFT_OPEN · offline: True
    """
    return await run("listDepositBoxes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/deposit-partial-payment")
async def list_deposit_partial_payment(request: Request) -> dict:
    """Deposit, Partial Payment & Outstanding Balance Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listDepositPartialPayment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/external-payment-partner")
async def list_external_payment_partner(request: Request) -> dict:
    """External Payment, Partner & Settlement Reference Mapping

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listExternalPaymentPartner", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fee-seller-proceed")
async def list_fee_seller_proceed(request: Request) -> dict:
    """Fees, Seller Proceeds & Listing Confirmation

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listFeeSellerProceed", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/financial-traceability")
async def list_financial_traceability(request: Request) -> dict:
    """Financial Traceability, Control & Audit Explorer

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listFinancialTraceability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fraud-rules")
async def list_fraud_rules(request: Request) -> dict:
    """listFraudRules

    scope: tenant · permission: ORDER_VIEW · offline: False
    """
    return await run("listFraudRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-amendment-cancellation")
async def list_group_amendment_cancellation(request: Request) -> dict:
    """Group Amendments, Cancellation & Refund Operations

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupAmendmentCancellation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-arrival-check")
async def list_group_arrival_check(request: Request) -> dict:
    """Group Arrival, Check-In & Admission Operations

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupArrivalCheck", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-booking")
async def list_group_booking(request: Request) -> dict:
    """Group Booking Operations Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupBooking", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-booking-reconciliation")
async def list_group_booking_reconciliation(request: Request) -> dict:
    """Group Booking Reconciliation, Closure & Performance

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupBookingReconciliation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-customer-organization")
async def list_group_customer_organization(request: Request) -> dict:
    """Group Customer & Organization Profile

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupCustomerOrganization", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-enquiry-opportunity")
async def list_group_enquiry_opportunity(request: Request) -> dict:
    """Group Enquiry & Opportunity Capture

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupEnquiryOpportunity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-payment-deposit")
async def list_group_payment_deposit(request: Request) -> dict:
    """Group Payment, Deposit & Balance Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupPaymentDeposit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-requirement-availability")
async def list_group_requirement_availability(request: Request) -> dict:
    """Group Requirements, Availability & Capacity Planner

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupRequirementAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-sale")
async def list_group_sale(request: Request) -> dict:
    """Group Sales Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupSale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-sale")
async def list_group_sale2(request: Request) -> dict:
    """Group Sales Analytics & AI Intelligence Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupSale2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-ticket-fulfillment")
async def list_group_ticket_fulfillment(request: Request) -> dict:
    """Group Ticket Fulfillment & Distribution

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupTicketFulfillment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-ticket-seat")
async def list_group_ticket_seat(request: Request) -> dict:
    """Group Ticket, Seat & Entitlement Allocation

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listGroupTicketSeat", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/invitations/allowances")
async def list_invitation_allowances(request: Request) -> dict:
    """Who may issue comps, and how many are left

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listInvitationAllowances", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/listing-lifecycle-expiry")
async def list_listing_lifecycle_expiry(request: Request) -> dict:
    """Listing Lifecycle, Expiry & Cancellation

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listListingLifecycleExpiry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/my/orders")
async def list_my_orders(request: Request) -> dict:
    """The orders this guest placed

    scope: tenant · permission: - · offline: False
    """
    return await run("listMyOrders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/official-resale-marketplace")
async def list_official_resale_marketplace(request: Request) -> dict:
    """Official Resale Marketplace & Buyer Discovery

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOfficialResaleMarketplace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/order-financial-reconciliation")
async def list_order_financial_reconciliation(request: Request) -> dict:
    """Order Financial Analytics & AI Reconciliation Intelligence

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOrderFinancialReconciliation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/order-lifecycle-timeline")
async def list_order_lifecycle_timeline(request: Request) -> dict:
    """Order Lifecycle Timeline, SLA, Exceptions & AI Operations

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOrderLifecycleTimeline", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/order-line-product")
async def list_order_line_product(request: Request) -> dict:
    """Order Line, Product & Entitlement Composition

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOrderLineProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/order-payment-detail")
async def list_order_payment_detail(request: Request) -> dict:
    """Order Payment Detail & Transaction Ledger

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOrderPaymentDetail", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/orders/{orderId}/refunds")
async def list_order_refunds(request: Request) -> dict:
    """List refunds against an order

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("listOrderRefunds", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/order-reservation")
async def list_order_reservation(request: Request) -> dict:
    """Order & Reservation Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOrderReservation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/order-split-merge")
async def list_order_split_merge(request: Request) -> dict:
    """Order Split, Merge & Transaction Relationship Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listOrderSplitMerge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/orders")
async def list_orders(request: Request) -> dict:
    """List orders

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("listOrders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/participant-guest-list")
async def list_participant_guest_list(request: Request) -> dict:
    """Participants, Guest Lists & Group Structure

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listParticipantGuestList", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/payment-order-financial")
async def list_payment_order_financial(request: Request) -> dict:
    """Payment & Order Financial Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listPaymentOrderFinancial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/payment-providers")
async def list_payment_providers(request: Request) -> dict:
    """Gateways configured for this scope

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listPaymentProviders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/payment-reconciliation-exception")
async def list_payment_reconciliation_exception(request: Request) -> dict:
    """Payment Reconciliation & Exception Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listPaymentReconciliationException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/payment-tokens")
async def list_payment_tokens(request: Request) -> dict:
    """A guest's saved payment methods

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listPaymentTokens", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/person-type-product")
async def list_person_type_product(request: Request) -> dict:
    """Person-Type, Product & Entitlement Conversion Rules

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listPersonTypeProduct", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/quote-booking-conversion")
async def list_quote_booking_conversion(request: Request) -> dict:
    """Quote-to-Booking Conversion & Confirmation

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listQuoteBookingConversion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/quote-revision-negotiation")
async def list_quote_revision_negotiation(request: Request) -> dict:
    """Quote Revision, Negotiation & Version Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listQuoteRevisionNegotiation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/refund-dispute-resale")
async def list_refund_dispute_resale(request: Request) -> dict:
    """Refunds, Disputes & Resale Exceptions

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listRefundDisputeResale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/related-order-transaction")
async def list_related_order_transaction(request: Request) -> dict:
    """Related Order & Transaction Relationship Explorer

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listRelatedOrderTransaction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale")
async def list_resale(request: Request) -> dict:
    """Resale Operations Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale")
async def list_resale2(request: Request) -> dict:
    """Resale Analytics & AI Intelligence

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResale2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-confirmation-ownership")
async def list_resale_confirmation_ownership(request: Request) -> dict:
    """Resale Confirmation, Ownership Transfer & Ticket Delivery

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleConfirmationOwnership", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-eligibility-ticket")
async def list_resale_eligibility_ticket(request: Request) -> dict:
    """Resale Eligibility & Ticket Selection

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleEligibilityTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-fee-commission")
async def list_resale_fee_commission(request: Request) -> dict:
    """Resale Fees, Commission & Seller Proceeds

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleFeeCommission", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-fraud-duplicate")
async def list_resale_fraud_duplicate(request: Request) -> dict:
    """Resale Fraud & Duplicate Sale Protection

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleFraudDuplicate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-inventory-availability")
async def list_resale_inventory_availability(request: Request) -> dict:
    """Resale Inventory & Availability Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleInventoryAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-listing-seller")
async def list_resale_listing_seller(request: Request) -> dict:
    """My Resale Listings & Seller Dashboard

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleListingSeller", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-marketplace")
async def list_resale_marketplace(request: Request) -> dict:
    """Resale Marketplace Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleMarketplace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-ownership")
async def list_resale_ownership(request: Request) -> dict:
    """Resale Audit & Ownership History

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleOwnership", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-policy-marketplace")
async def list_resale_policy_marketplace(request: Request) -> dict:
    """Resale Policy & Marketplace Settings

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResalePolicyMarketplace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-pricing-price")
async def list_resale_pricing_price(request: Request) -> dict:
    """Resale Pricing & Price Guardrails

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResalePricingPrice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/resale-ticket-detail")
async def list_resale_ticket_detail(request: Request) -> dict:
    """Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listResaleTicketDetail", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reservation-confirmation-expiry")
async def list_reservation_confirmation_expiry(request: Request) -> dict:
    """Reservation Confirmation, Expiry & Fulfillment Readiness

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listReservationConfirmationExpiry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reservations")
async def list_reservations(request: Request) -> dict:
    """List reservations

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listReservations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/seller-settlement-payout")
async def list_seller_settlement_payout(request: Request) -> dict:
    """Seller Settlement & Payout Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listSellerSettlementPayout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/shifts")
async def list_shifts(request: Request) -> dict:
    """List shifts

    scope: venue · permission: REPORT_VIEW_WORKSTATION · offline: False
    """
    return await run("listShifts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/sync/rejections")
async def list_sync_rejections(request: Request) -> dict:
    """Entries the server refused

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listSyncRejections", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ticket-ownership-transfer")
async def list_ticket_ownership_transfer(request: Request) -> dict:
    """Ticket Ownership Transfer Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listTicketOwnershipTransfer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ticket-reissue-fulfillment")
async def list_ticket_reissue_fulfillment(request: Request) -> dict:
    """Ticket Reissue & Fulfillment Regeneration

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listTicketReissueFulfillment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ticket-resale-marketplace")
async def list_ticket_resale_marketplace(request: Request) -> dict:
    """My Tickets & Resale Marketplace Entry

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listTicketResaleMarketplace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upgrade-conversion")
async def list_upgrade_conversion(request: Request) -> dict:
    """Upgrade & Conversion Command Center

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listUpgradeConversion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upgrade-eligibility-qualification")
async def list_upgrade_eligibility_qualification(request: Request) -> dict:
    """Upgrade Eligibility & Qualification Rules

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listUpgradeEligibilityQualification", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upgrade-exception")
async def list_upgrade_exception(request: Request) -> dict:
    """Upgrade History, Exception Management & Audit Explorer

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listUpgradeException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upgrade-financial-treatment")
async def list_upgrade_financial_treatment(request: Request) -> dict:
    """Upgrade Financial Treatment & Price Difference Rules

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listUpgradeFinancialTreatment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upgrade-timing-usage")
async def list_upgrade_timing_usage(request: Request) -> dict:
    """Upgrade Timing, Usage & Ticket Status Rules

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listUpgradeTimingUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/void-reversal-same")
async def list_void_reversal_same(request: Request) -> dict:
    """Void, Reversal & Same-Day Correction Management

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listVoidReversalSame", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/white-label-marketplace")
async def list_white_label_marketplace(request: Request) -> dict:
    """White-Label Marketplace Deployment & Experience Architecture

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("listWhiteLabelMarketplace", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/modify")
async def modify_order(request: Request) -> dict:
    """Add or remove lines on an existing order

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("modifyOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guest-credit-accounts")
async def open_guest_credit_account(request: Request) -> dict:
    """A credit limit for an individual booking ahead

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("openGuestCreditAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts")
async def open_shift(request: Request) -> dict:
    """Open a shift

    scope: workstation · permission: SHIFT_OPEN · offline: True
    """
    return await run("openShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/b2b-accounts/{accountId}/credit/override")
async def override_credit_limit(request: Request) -> dict:
    """Authorise an order beyond the credit limit

    scope: venue · permission: CREDIT_OVERRIDE · offline: False
    """
    return await run("overrideCreditLimit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payment-links/{token}/pay")
async def pay_by_link(request: Request) -> dict:
    """payByLink

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("payByLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ticket-templates/{templateId}/proof")
async def print_ticket_proof(request: Request) -> dict:
    """Print a sample without selling anything

    scope: venue · permission: ORDER_REPRINT · offline: True
    """
    return await run("printTicketProof", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/wallet-passes/{passId}/push")
async def push_wallet_pass_update(request: Request) -> dict:
    """Push a change to every device holding it

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("pushWalletPassUpdate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/upgrade-quote")
async def quote_upgrade(request: Request) -> dict:
    """What an upgrade costs, pro-rata

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("quoteUpgrade", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/no-sale")
async def record_no_sale(request: Request) -> dict:
    """Open the drawer without a sale

    scope: workstation · permission: SHIFT_SUSPEND · offline: True
    """
    return await run("recordNoSale", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/entitlements/{entitlementId}/reissue")
async def reissue_entitlement(request: Request) -> dict:
    """Zero-value reissue of an expired entitlement for a later date

    scope: venue · permission: ORDER_EXCHANGE · offline: False
    """
    return await run("reissueEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stored-value/authorisations/{authorisationId}/release")
async def release_stored_value(request: Request) -> dict:
    """Give a hold back

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("releaseStoredValue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/stored-value/authorisations/{authorisationId}/release")
async def relinquish_stored_value(request: Request) -> dict:
    """Give a hold back

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("relinquishStoredValue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/carts/{cartId}/lines/{lineId}")
async def remove_cart_line(request: Request) -> dict:
    """Take something out

    scope: venue · permission: - · offline: False
    """
    return await run("removeCartLine", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/reopen")
async def reopen_shift(request: Request) -> dict:
    """Reopen a shift closed in error

    scope: venue · permission: SHIFT_REOPEN · offline: False
    """
    return await run("reopenShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/reprints")
async def reprint_order(request: Request) -> dict:
    """Reprint or resend tickets

    scope: venue · permission: ORDER_REPRINT · offline: True
    """
    return await run("reprintOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/reschedule")
async def reschedule_order(request: Request) -> dict:
    """Move an order to another performance

    scope: venue · permission: ORDER_RESCHEDULE · offline: False
    """
    return await run("rescheduleOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payment-links/{linkId}/resend")
async def resend_payment_link(request: Request) -> dict:
    """resendPaymentLink

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("resendPaymentLink", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/chargebacks/{chargebackId}/respond")
async def respond_to_chargeback(request: Request) -> dict:
    """Submit evidence, or accept the loss

    scope: venue · permission: ORDER_REFUND_APPROVE · offline: False
    """
    return await run("respondToChargeback", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/resume")
async def resume_order(request: Request) -> dict:
    """Bring a parked sale back to a till

    scope: workstation · permission: ORDER_MODIFY · offline: False
    """
    return await run("resumeOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/resume")
async def resume_shift(request: Request) -> dict:
    """Resume a suspended shift

    scope: workstation · permission: SHIFT_OPEN · offline: True
    """
    return await run("resumeShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/after-sale-financial")
async def set_after_sale_financial(request: Request) -> dict:
    """After-Sales Financial Settlement & Adjustment Workspace

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setAfterSaleFinancial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/amendment-eligibility-policy")
async def set_amendment_eligibility_policy(request: Request) -> dict:
    """Amendment Eligibility & Policy Rule Builder

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setAmendmentEligibilityPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/b2b-accounts/{accountId}/credit")
async def set_b2b_credit_limit(request: Request) -> dict:
    """Set a partner credit limit

    scope: venue · permission: CREDIT_MANAGE · offline: False
    """
    return await run("setB2bCreditLimit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/cancellation-partial-policy")
async def set_cancellation_partial_policy(request: Request) -> dict:
    """Cancellation & Partial Cancellation Policy Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setCancellationPartialPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/customer-guest-account")
async def set_customer_guest_account(request: Request) -> dict:
    """Customer, Guest & Account Assignment

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setCustomerGuestAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/fraud-rules")
async def set_fraud_rules(request: Request) -> dict:
    """setFraudRules

    scope: tenant · permission: ORDER_MODIFY · offline: False
    """
    return await run("setFraudRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/group-booking-handover")
async def set_group_booking_handover(request: Request) -> dict:
    """Group Booking 360° & Handover Workspace

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setGroupBookingHandover", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/group-operational-planning")
async def set_group_operational_planning(request: Request) -> dict:
    """Group Operational Planning & Task Workspace

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setGroupOperationalPlanning", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/group-package-experience")
async def set_group_package_experience(request: Request) -> dict:
    """Group Package & Experience Builder

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setGroupPackageExperience", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/group-quotation-proposal")
async def set_group_quotation_proposal(request: Request) -> dict:
    """Group Quotation Builder & Proposal Generation

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setGroupQuotationProposal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/multi-payment-split")
async def set_multi_payment_split(request: Request) -> dict:
    """Multi-Payment, Split Tender & Payment Allocation Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setMultiPaymentSplit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/order-amendment")
async def set_order_amendment(request: Request) -> dict:
    """Order Amendment Workspace

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setOrderAmendment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/order-detail-transaction")
async def set_order_detail_transaction(request: Request) -> dict:
    """Order Detail & Transaction Workspace

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setOrderDetailTransaction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/order-reservation-statu")
async def set_order_reservation_status(request: Request) -> dict:
    """Order & Reservation Status Lifecycle Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setOrderReservationStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/payment-providers")
async def set_payment_provider(request: Request) -> dict:
    """Configure a gateway and its routing

    scope: venue · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setPaymentProvider", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pro-rata-residual")
async def set_pro_rata_residual(request: Request) -> dict:
    """Pro-Rata, Residual Value & Entitlement Credit Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setProRataResidual", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/venues/{venueId}/refund-policy")
async def set_refund_policy(request: Request) -> dict:
    """Set a venue's refund policy

    scope: venue · permission: REGION_CONFIGURE · offline: False
    """
    return await run("setRefundPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/resale-eligibility-rule")
async def set_resale_eligibility_rule(request: Request) -> dict:
    """Resale Eligibility Rule Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setResaleEligibilityRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/resale-marketplace-recommendation")
async def set_resale_marketplace_recommendation(request: Request) -> dict:
    """AI Resale Configuration & Marketplace Recommendations

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setResaleMarketplaceRecommendation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/reservation-hold-policy")
async def set_reservation_hold_policy(request: Request) -> dict:
    """Reservation & Hold Policy Configuration

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setReservationHoldPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/upgrade-conversion-path")
async def set_upgrade_conversion_path(request: Request) -> dict:
    """Upgrade & Conversion Path Builder

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("setUpgradeConversionPath", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/entitlements/{entitlementId}/share")
async def share_entitlement(request: Request) -> dict:
    """Let somebody else use this, without giving it away

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("shareEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/split")
async def split_order(request: Request) -> dict:
    """Break one order into independent orders

    scope: venue · permission: ORDER_MODIFY · offline: False
    """
    return await run("splitOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payment-tokens")
async def store_payment_token(request: Request) -> dict:
    """Save a payment method for future use

    scope: venue · permission: ORDER_CREATE · offline: False
    """
    return await run("storePaymentToken", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/shifts/{shiftId}/suspend")
async def suspend_shift(request: Request) -> dict:
    """Suspend a shift so another user can log in

    scope: workstation · permission: SHIFT_SUSPEND · offline: True
    """
    return await run("suspendShift", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/sync/orders")
async def sync_orders(request: Request) -> dict:
    """Replay orders recorded offline

    scope: workstation · permission: ORDER_CREATE · offline: False
    """
    return await run("syncOrders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/transfer")
async def transfer_order_tickets(request: Request) -> dict:
    """Transfer tickets to another guest

    scope: venue · permission: - · offline: False
    """
    return await run("transferOrderTickets", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/carts/{cartId}/lines/{lineId}")
async def update_cart_line(request: Request) -> dict:
    """Change a quantity

    scope: venue · permission: - · offline: False
    """
    return await run("updateCartLine", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/orders/{orderId}/voids")
async def void_order(request: Request) -> dict:
    """Void an order

    scope: venue · permission: ORDER_VOID · offline: True
    """
    return await run("voidOrder", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/payments/{paymentId}/void")
async def void_payment(request: Request) -> dict:
    """Release an authorisation before it is captured

    scope: venue · permission: PAYMENT_VOID · offline: False
    """
    return await run("voidPayment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/deposit-boxes/{boxId}/withdraw")
async def withdraw_from_deposit_box(request: Request) -> dict:
    """A supervisor takes cash out mid-shift

    scope: venue · permission: CASH_LIFT · offline: True
    """
    return await run("withdrawFromDepositBox", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

