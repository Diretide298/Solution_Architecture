"""PlatformService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

167 operations · 62 tables touched · scope levels: platform, region, tenant, venue
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="PlatformService", docs_url="/_docs")

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
    return {"service": "PlatformService", "operations": 167,
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



@app.post("/tenants/{tenantId}/licences/add-ons")
async def add_licence_add_on(request: Request) -> dict:
    """License a module outside the plan

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("addLicenceAddOn", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/migrations/apply")
async def apply_migration(request: Request) -> dict:
    """Apply a planned migration run

    scope: tenant · permission: PLATFORM_MIGRATION_APPLY · offline: False
    """
    return await run("applyMigration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/booking-limit-commercial")
async def approve_booking_limit_commercial(request: Request) -> dict:
    """Booking Limits, Commercial Exceptions & Approval

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("approveBookingLimitCommercial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/membership-product-validation")
async def approve_membership_product_validation(request: Request) -> dict:
    """Membership Product Validation, Approval, Publication & Versioning

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("approveMembershipProductValidation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/partner-statu-lifecycle")
async def approve_partner_statu_lifecycle(request: Request) -> dict:
    """Partner Approval, Status & Lifecycle Management

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("approvePartnerStatuLifecycle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cells/{cellId}/cancel-decommission")
async def cancel_decommission(request: Request) -> dict:
    """Halt a decommission

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("cancelDecommission", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invoices/{invoiceId}/cancel")
async def cancel_invoice(request: Request) -> dict:
    """Cancel or credit an invoice

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("cancelInvoice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/subscriptions/{subscriptionId}/cancel")
async def cancel_subscription(request: Request) -> dict:
    """Terminate a tenant subscription

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("cancelSubscription", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/listings/{listingId}/certify")
async def certify_integration(request: Request) -> dict:
    """Approve, reject or revoke a certification

    scope: tenant · permission: DEVELOPER_ADMIN · offline: False
    """
    return await run("certifyIntegration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/api-clients")
async def create_api_client(request: Request) -> dict:
    """Create a client with scopes and an environment

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("createApiClient", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/partner-agreements")
async def create_partner_agreement(request: Request) -> dict:
    """Agree commercial terms with a partner

    scope: tenant · permission: PARTNER_MANAGE · offline: False
    """
    return await run("createPartnerAgreement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/partner-quotes")
async def create_partner_quote(request: Request) -> dict:
    """Raise a quote

    scope: tenant · permission: PARTNER_MANAGE · offline: False
    """
    return await run("createPartnerQuote", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/partners/{partnerId}/users")
async def create_partner_user(request: Request) -> dict:
    """Add a user to a partner branch

    scope: tenant · permission: PARTNER_MANAGE · offline: False
    """
    return await run("createPartnerUser", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/plans")
async def create_plan(request: Request) -> dict:
    """Create a subscription plan

    scope: tenant · permission: PLATFORM_PLAN_MANAGE · offline: False
    """
    return await run("createPlan", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/plans/{planId}")
async def create_plan_version(request: Request) -> dict:
    """Publish a new version of a plan

    scope: tenant · permission: PLATFORM_PLAN_MANAGE · offline: False
    """
    return await run("createPlanVersion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/releases")
async def create_release(request: Request) -> dict:
    """Cut a release

    scope: tenant · permission: PLATFORM_RELEASE_MANAGE · offline: False
    """
    return await run("createRelease", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/sandboxes")
async def create_sandbox(request: Request) -> dict:
    """Provision a sandbox with synthetic data

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("createSandbox", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants")
async def create_tenant(request: Request) -> dict:
    """Create a tenant

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("createTenant", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/webhook-subscriptions")
async def create_webhook_subscription(request: Request) -> dict:
    """Subscribe to business events

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("createWebhookSubscription", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/burst-environments/{burstEnvironmentId}/decommission")
async def decommission_burst_environment(request: Request) -> dict:
    """Tear it down

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("decommissionBurstEnvironment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cells/{cellId}/decommission")
async def decommission_cell(request: Request) -> dict:
    """Begin decommissioning a cell

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("decommissionCell", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/api-versions/{version}/deprecate")
async def deprecate_api_version(request: Request) -> dict:
    """Announce a sunset date and notify subscribers

    scope: tenant · permission: DEVELOPER_ADMIN · offline: False
    """
    return await run("deprecateApiVersion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invoices/{invoiceId}/dispute")
async def dispute_invoice(request: Request) -> dict:
    """Raise a dispute

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("disputeInvoice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/burst-environments/{burstEnvironmentId}/drain")
async def drain_burst_environment(request: Request) -> dict:
    """Stop taking orders, let in-flight ones finish

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("drainBurstEnvironment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-migrations/{migrationId}/execute")
async def execute_tenant_migration(request: Request) -> dict:
    """Move the tenant

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("executeTenantMigration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/partners/{partnerId}/invoice-export")
async def export_partner_invoice(request: Request) -> dict:
    """Partner invoice and settlement, in an ERP format

    scope: tenant · permission: LEDGER_VIEW · offline: False
    """
    return await run("exportPartnerInvoice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants/{tenantId}/invoices")
async def generate_invoice(request: Request) -> dict:
    """Generate an invoice for a period

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("generateInvoice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/api-usage")
async def get_api_usage(request: Request) -> dict:
    """Calls, errors, latency and success rate

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("getApiUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cells/{cellId}")
async def get_cell(request: Request) -> dict:
    """Read a cell

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("getCell", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cells/{cellId}/capacity")
async def get_cell_capacity(request: Request) -> dict:
    """Load against headroom

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("getCellCapacity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cells/{cellId}/health")
async def get_cell_health(request: Request) -> dict:
    """Cell health and schema version

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("getCellHealth", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-agreements/{agreementId}/commission-statement")
async def get_commission_statement(request: Request) -> dict:
    """What the partner earned and what is owed

    scope: tenant · permission: PARTNER_VIEW · offline: False
    """
    return await run("getCommissionStatement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}/entitlement-usage")
async def get_entitlement_usage(request: Request) -> dict:
    """Usage against licensed limits

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("getEntitlementUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/migrations/runs/{runId}")
async def get_migration_run(request: Request) -> dict:
    """Migration run progress per cell

    scope: tenant · permission: PLATFORM_MIGRATION_VIEW · offline: False
    """
    return await run("getMigrationRun", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/plans/{planId}")
async def get_plan(request: Request) -> dict:
    """Read a plan

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("getPlan", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/releases/{reinventoryHoldId}")
async def get_release(request: Request) -> dict:
    """Read a release with its rollout state

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("getRelease", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/releases/{reinventoryHoldId}/readiness")
async def get_release_readiness(request: Request) -> dict:
    """Whether a release can be promoted, and what blocks it

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("getReleaseReadiness", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/rollouts/{rolloutId}")
async def get_rollout(request: Request) -> dict:
    """Rollout progress per cell

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("getRollout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/scaling-policies")
async def get_scaling_policy(request: Request) -> dict:
    """The floors, ceilings and target utilisation a cell scales on

    scope: region · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("getScalingPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}/subscription")
async def get_subscription(request: Request) -> dict:
    """Read the current subscription

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("getSubscription", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}")
async def get_tenant(request: Request) -> dict:
    """Read a tenant with cells and subscription

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("getTenant", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}/licences")
async def get_tenant_licences(request: Request) -> dict:
    """What a tenant is licensed to use

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: True
    """
    return await run("getTenantLicences", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}/usage")
async def get_usage_metering(request: Request) -> dict:
    """Metered usage for a period

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("getUsageMetering", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/migrations/version-skew")
async def get_version_skew(request: Request) -> dict:
    """Schema and application version across every cell

    scope: tenant · permission: PLATFORM_MIGRATION_VIEW · offline: False
    """
    return await run("getVersionSkew", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/oauth/token")
async def issue_api_token(request: Request) -> dict:
    """Exchange a credential for an access token

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("issueApiToken", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cell-clusters")
async def launch_cell_cluster(request: Request) -> dict:
    """Launch an identical cluster

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("launchCellCluster", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/api-clients")
async def list_api_clients(request: Request) -> dict:
    """Registered clients for this developer

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("listApiClients", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/api-versions")
async def list_api_versions(request: Request) -> dict:
    """Versions, their status and their sunset dates

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("listApiVersions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/archival-jobs")
async def list_archival_jobs(request: Request) -> dict:
    """Archival and retention jobs

    scope: region · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listArchivalJobs", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/backup-runs")
async def list_backup_runs(request: Request) -> dict:
    """Backups taken and what they cover

    scope: region · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listBackupRuns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/burst-environments")
async def list_burst_environments(request: Request) -> dict:
    """On-sale environments

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listBurstEnvironments", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cell-clusters")
async def list_cell_clusters(request: Request) -> dict:
    """Clusters in a region

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listCellClusters", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cells/{cellId}/jobs")
async def list_cell_jobs(request: Request) -> dict:
    """Provisioning, migration and maintenance jobs

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listCellJobs", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/channel-listings")
async def list_channel_listings(request: Request) -> dict:
    """What is listed on which OTA

    scope: venue · permission: PARTNER_VIEW · offline: False
    """
    return await run("listChannelListings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commercial-agreement")
async def list_commercial_agreement(request: Request) -> dict:
    """Commercial Agreement Command Center

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listCommercialAgreement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commercial-agreement-health")
async def list_commercial_agreement_health(request: Request) -> dict:
    """Commercial Agreement 360°, Health & AI Review

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listCommercialAgreementHealth", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commercial-allocation-quota")
async def list_commercial_allocation_quota(request: Request) -> dict:
    """Commercial Allocation, Quota & Commitment Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listCommercialAllocationQuota", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commission-calculation-settlement")
async def list_commission_calculation_settlement(request: Request) -> dict:
    """Commission Calculation & Settlement Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listCommissionCalculationSettlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/commission-margin-incentive")
async def list_commission_margin_incentive(request: Request) -> dict:
    """Commission, Margin & Incentive Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listCommissionMarginIncentive", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credit-limit-exposure")
async def list_credit_limit_exposure(request: Request) -> dict:
    """Credit Limit & Exposure Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listCreditLimitExposure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dead-letters")
async def list_dead_letters(request: Request) -> dict:
    """Undeliverable events

    scope: platform · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listDeadLetters", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/deposit-guarantee-financial")
async def list_deposit_guarantee_financial(request: Request) -> dict:
    """Deposit, Guarantee & Financial Security Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listDepositGuaranteeFinancial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/environments")
async def list_environments(request: Request) -> dict:
    """The environment registry

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("listEnvironments", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/listings")
async def list_integration_listings(request: Request) -> dict:
    """Published third-party integrations

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("listIntegrationListings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/member")
async def list_member(request: Request) -> dict:
    """Member Operations Command Center

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMember", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/member-exception-override")
async def list_member_exception_override(request: Request) -> dict:
    """Member Exceptions, Overrides & Service Recovery

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMemberExceptionOverride", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/member-lifecycle-case")
async def list_member_lifecycle_case(request: Request) -> dict:
    """Member Lifecycle History, Audit & Case Timeline

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMemberLifecycleCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-activation-credential")
async def list_membership_activation_credential(request: Request) -> dict:
    """Membership Activation, Assignment & Credential Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipActivationCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-annual-pass")
async def list_membership_annual_pass(request: Request) -> dict:
    """Membership & Annual Pass Command Center

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipAnnualPass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-commercial-pricing")
async def list_membership_commercial_pricing(request: Request) -> dict:
    """Membership Commercial, Pricing & Channel Association

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipCommercialPricing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-freeze-suspension")
async def list_membership_freeze_suspension(request: Request) -> dict:
    """Membership Freeze, Suspension & Reactivation Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipFreezeSuspension", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-renewal-retention")
async def list_membership_renewal_retention(request: Request) -> dict:
    """Membership Analytics, Renewal Intelligence & AI Retention Center

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipRenewalRetention", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-upgrade-downgrade")
async def list_membership_upgrade_downgrade(request: Request) -> dict:
    """Membership Upgrade, Downgrade & Product Migration Operations

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipUpgradeDowngrade", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/membership-usage-visit")
async def list_membership_usage_visit(request: Request) -> dict:
    """Membership Usage, Visit & Consumption Rules

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listMembershipUsageVisit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/migrations")
async def list_migrations(request: Request) -> dict:
    """The migration register

    scope: tenant · permission: PLATFORM_MIGRATION_VIEW · offline: False
    """
    return await run("listMigrations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner")
async def list_partner(request: Request) -> dict:
    """Partner Management Command Center

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartner", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner")
async def list_partner2(request: Request) -> dict:
    """Partner Operations Command Center

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartner2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-access-role")
async def list_partner_access_role(request: Request) -> dict:
    """Partner Access, Roles & Permission Profile

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerAccessRole", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-agreements")
async def list_partner_agreements(request: Request) -> dict:
    """Commercial agreements with B2B partners

    scope: tenant · permission: PARTNER_MANAGE · offline: False
    """
    return await run("listPartnerAgreements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-cancellation-refund")
async def list_partner_cancellation_refund(request: Request) -> dict:
    """Partner Cancellations, Refunds & Amendments

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerCancellationRefund", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-contact-user")
async def list_partner_contact_user(request: Request) -> dict:
    """Partner Contacts & User Administration

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerContactUser", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-dispute-case")
async def list_partner_dispute_case(request: Request) -> dict:
    """Partner Disputes, Cases & Service Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerDisputeCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-documentation-compliance")
async def list_partner_documentation_compliance(request: Request) -> dict:
    """Partner Documentation & Compliance Repository

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerDocumentationCompliance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-onboarding-application")
async def list_partner_onboarding_application(request: Request) -> dict:
    """Partner Onboarding & Application Workflow

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerOnboardingApplication", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-order-booking")
async def list_partner_order_booking(request: Request) -> dict:
    """Partner Orders & Booking Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerOrderBooking", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-performance-scorecard")
async def list_partner_performance_scorecard(request: Request) -> dict:
    """Partner Performance Scorecard & Risk Monitoring

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerPerformanceScorecard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-profile-readiness")
async def list_partner_profile_readiness(request: Request) -> dict:
    """Partner 360° Profile, Readiness & AI Review

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerProfileReadiness", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-quotes")
async def list_partner_quotes(request: Request) -> dict:
    """Quotes offered to this partner

    scope: tenant · permission: PARTNER_VIEW · offline: False
    """
    return await run("listPartnerQuotes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-reconciliation-exception")
async def list_partner_reconciliation_exception(request: Request) -> dict:
    """Partner Reconciliation & Exception Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerReconciliationException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-relationship")
async def list_partner_relationship(request: Request) -> dict:
    """Partner AI Intelligence & Relationship Optimization

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerRelationship", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partner-statement-account")
async def list_partner_statement_account(request: Request) -> dict:
    """Partner Statement & Account Activity

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPartnerStatementAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/partners/{partnerId}/users")
async def list_partner_users(request: Request) -> dict:
    """Users beneath a partner, by branch

    scope: tenant · permission: PARTNER_VIEW · offline: False
    """
    return await run("listPartnerUsers", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/plans")
async def list_plans(request: Request) -> dict:
    """List subscription plans

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listPlans", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/releases")
async def list_releases(request: Request) -> dict:
    """List releases

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("listReleases", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/renewal-auto")
async def list_renewal_auto(request: Request) -> dict:
    """Renewal Operations & Auto-Renewal Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listRenewalAuto", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reservation-hold-release")
async def list_reservation_hold_release(request: Request) -> dict:
    """Reservations, Holds & Release Management

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listReservationHoldRelease", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/rollouts")
async def list_rollouts(request: Request) -> dict:
    """List rollouts

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("listRollouts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/sandboxes")
async def list_sandboxes(request: Request) -> dict:
    """Sandbox environments

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("listSandboxes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}/invoices")
async def list_subscription_invoices(request: Request) -> dict:
    """List subscription invoices

    scope: tenant · permission: PLATFORM_BILLING_VIEW · offline: False
    """
    return await run("listSubscriptionInvoices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/support-notices")
async def list_support_notices(request: Request) -> dict:
    """End-of-support notices

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("listSupportNotices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/{tenantId}/cells")
async def list_tenant_cells(request: Request) -> dict:
    """List a tenant's cells

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listTenantCells", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-migrations")
async def list_tenant_migrations(request: Request) -> dict:
    """Tenant moves between cells

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listTenantMigrations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants")
async def list_tenants(request: Request) -> dict:
    """List tenants

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listTenants", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/territory-market-distribution")
async def list_territory_market_distribution(request: Request) -> dict:
    """Territory, Market & Distribution Rights

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listTerritoryMarketDistribution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/upgrade-schedules")
async def list_upgrade_schedules(request: Request) -> dict:
    """Scheduled tenant upgrades

    scope: tenant · permission: PLATFORM_RELEASE_VIEW · offline: False
    """
    return await run("listUpgradeSchedules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venue-type-templates")
async def list_venue_type_templates(request: Request) -> dict:
    """Starting configurations by venue kind

    scope: tenant · permission: TENANT_VIEW · offline: False
    """
    return await run("listVenueTypeTemplates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/visit-admission-entitlement")
async def list_visit_admission_entitlement(request: Request) -> dict:
    """Visit, Admission & Entitlement Usage Monitor

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("listVisitAdmissionEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waf-policies")
async def list_waf_rules(request: Request) -> dict:
    """Web application firewall rules in force

    scope: region · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("listWafRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/webhook-subscriptions/{subscriptionId}/deliveries")
async def list_webhook_deliveries(request: Request) -> dict:
    """What was sent, what failed, and why

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("listWebhookDeliveries", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/webhook-subscriptions")
async def list_webhook_subscriptions(request: Request) -> dict:
    """What this client is subscribed to

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("listWebhookSubscriptions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/rollouts/{rolloutId}/pause")
async def pause_rollout(request: Request) -> dict:
    """Halt a rollout in progress

    scope: tenant · permission: PLATFORM_RELEASE_PROMOTE · offline: False
    """
    return await run("pauseRollout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/migrations/plan")
async def plan_migration(request: Request) -> dict:
    """Plan a migration run without applying it

    scope: tenant · permission: PLATFORM_MIGRATION_VIEW · offline: False
    """
    return await run("planMigration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-migrations")
async def plan_tenant_migration(request: Request) -> dict:
    """Plan moving a tenant to another cell

    scope: tenant · permission: PLATFORM_CELL_VIEW · offline: False
    """
    return await run("planTenantMigration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants/{tenantId}/subscription/preview")
async def preview_subscription_change(request: Request) -> dict:
    """Preview the effect of a plan change

    scope: tenant · permission: PLATFORM_TENANT_VIEW · offline: False
    """
    return await run("previewSubscriptionChange", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/releases/{reinventoryHoldId}/promote")
async def promote_release(request: Request) -> dict:
    """Promote a release to the next environment

    scope: tenant · permission: PLATFORM_RELEASE_PROMOTE · offline: False
    """
    return await run("promoteRelease", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants/{tenantId}/cells")
async def provision_cell(request: Request) -> dict:
    """Provision a cell for a region

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("provisionCell", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/support-notices")
async def publish_support_notice(request: Request) -> dict:
    """Publish an end-of-support notice

    scope: tenant · permission: PLATFORM_RELEASE_MANAGE · offline: False
    """
    return await run("publishSupportNotice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants/{tenantId}/reactivate")
async def reactivate_tenant(request: Request) -> dict:
    """Lift a suspension

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("reactivateTenant", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/burst-environments/{burstEnvironmentId}/reconcile")
async def reconcile_burst_environment(request: Request) -> dict:
    """Move the orders into the permanent platform

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("reconcileBurstEnvironment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invoices/{invoiceId}/payment")
async def record_invoice_payment(request: Request) -> dict:
    """Record payment against an invoice

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("recordInvoicePayment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/usage-records")
async def record_usage(request: Request) -> dict:
    """Record metered usage

    scope: tenant · permission: - · offline: False
    """
    return await run("recordUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/developers")
async def register_developer(request: Request) -> dict:
    """Register a developer or organisation

    scope: tenant · permission: DEVELOPER_VIEW · offline: False
    """
    return await run("registerDeveloper", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/environments")
async def register_environment(request: Request) -> dict:
    """Register an environment

    scope: tenant · permission: PLATFORM_RELEASE_MANAGE · offline: False
    """
    return await run("registerEnvironment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/partner-registrations")
async def register_partner(request: Request) -> dict:
    """A business applies to become a partner

    scope: tenant · permission: - · offline: False
    """
    return await run("registerPartner", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/releases/{reinventoryHoldId}/reject")
async def reject_release(request: Request) -> dict:
    """Reject a release back a stage

    scope: tenant · permission: PLATFORM_RELEASE_PROMOTE · offline: False
    """
    return await run("rejectRelease", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/tenants/{tenantId}/licences/add-ons")
async def remove_licence_add_on(request: Request) -> dict:
    """Remove an add-on

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("removeLicenceAddOn", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/dead-letters/{deadLetterId}/replay")
async def replay_dead_letter(request: Request) -> dict:
    """Re-enter the delivery path

    scope: platform · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("replayDeadLetter", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/webhook-subscriptions/{subscriptionId}/replay")
async def replay_events(request: Request) -> dict:
    """Re-deliver events from a point in time

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("replayEvents", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/burst-environments")
async def request_burst_environment(request: Request) -> dict:
    """Stand one up for a performance

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("requestBurstEnvironment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/sandboxes/{sandboxId}/reset")
async def reset_sandbox(request: Request) -> dict:
    """Back to a clean synthetic dataset

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("resetSandbox", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invoices/{invoiceId}/resolve-dispute")
async def resolve_invoice_dispute(request: Request) -> dict:
    """Resolve a dispute

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("resolveInvoiceDispute", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/api-clients/{clientId}/credentials")
async def revoke_api_credential(request: Request) -> dict:
    """Revoke immediately

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("revokeApiCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/migrations/runs/{runId}/rollback")
async def rollback_migration_run(request: Request) -> dict:
    """Roll a migration run back

    scope: tenant · permission: PLATFORM_MIGRATION_APPLY · offline: False
    """
    return await run("rollbackMigrationRun", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/rollouts/{rolloutId}/rollback")
async def rollback_rollout(request: Request) -> dict:
    """Roll a rollout back

    scope: tenant · permission: PLATFORM_RELEASE_PROMOTE · offline: False
    """
    return await run("rollbackRollout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-migrations/{migrationId}/rollback")
async def rollback_tenant_migration(request: Request) -> dict:
    """Roll a cutover back

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("rollbackTenantMigration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/api-clients/{clientId}/credentials")
async def rotate_api_credential(request: Request) -> dict:
    """Issue a new secret, with an overlap window

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("rotateApiCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/upgrade-schedules")
async def schedule_tenant_upgrade(request: Request) -> dict:
    """Schedule or defer a tenant upgrade

    scope: tenant · permission: PLATFORM_RELEASE_MANAGE · offline: False
    """
    return await run("scheduleTenantUpgrade", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/agreement-contract-term")
async def set_agreement_contract_term(request: Request) -> dict:
    """Agreement & Contract Terms Builder

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setAgreementContractTerm", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/api-licensing")
async def set_api_licensing(request: Request) -> dict:
    """Which API modules a tenant has licensed, and on what terms

    scope: tenant · permission: DEVELOPER_ADMIN · offline: False
    """
    return await run("setApiLicensing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/api-quotas")
async def set_api_quota(request: Request) -> dict:
    """Rate limits and throttling per client

    scope: tenant · permission: DEVELOPER_ADMIN · offline: False
    """
    return await run("setApiQuota", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-listings")
async def set_channel_listing(request: Request) -> dict:
    """List a product on a channel, with its own allocation

    scope: venue · permission: PARTNER_MANAGE · offline: False
    """
    return await run("setChannelListing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/developers/{developerId}/members")
async def set_developer_members(request: Request) -> dict:
    """Who at this organisation may do what

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("setDeveloperMembers", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/family-household-dependent")
async def set_family_household_dependent(request: Request) -> dict:
    """Family, Household & Dependent Membership Configuration

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setFamilyHouseholdDependent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/member-membership-account")
async def set_member_membership_account(request: Request) -> dict:
    """Member 360° Membership Account Workspace

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setMemberMembershipAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/membership-eligibility-qualification")
async def set_membership_eligibility_qualification(request: Request) -> dict:
    """Membership Eligibility & Qualification Rule Builder

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setMembershipEligibilityQualification", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/membership-entitlement-admission")
async def set_membership_entitlement_admission(request: Request) -> dict:
    """Membership Entitlement & Admission Benefit Builder

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setMembershipEntitlementAdmission", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/membership-product-tier")
async def set_membership_product_tier(request: Request) -> dict:
    """Membership Product & Tier Builder

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setMembershipProductTier", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/partner-brand-venue")
async def set_partner_brand_venue(request: Request) -> dict:
    """Partner Brand, Venue & Business Scope Assignment

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setPartnerBrandVenue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/partner-profile-organization")
async def set_partner_profile_organization(request: Request) -> dict:
    """Partner Profile & Organization Setup

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setPartnerProfileOrganization", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/partner-rate-net")
async def set_partner_rate_net(request: Request) -> dict:
    """Partner Rate & Net Pricing Configuration

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setPartnerRateNet", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/payment-term-billing")
async def set_payment_term_billing(request: Request) -> dict:
    """Payment Terms, Billing & Account Configuration

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setPaymentTermBilling", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/renewal-auto-membership")
async def set_renewal_auto_membership(request: Request) -> dict:
    """Renewal, Auto-Renewal & Membership Continuity Configuration

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setRenewalAutoMembership", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/scaling-policies")
async def set_scaling_policy(request: Request) -> dict:
    """Change the scaling policy

    scope: region · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setScalingPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenants/{tenantId}/subscription")
async def set_subscription(request: Request) -> dict:
    """Assign or change a subscription

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("setSubscription", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/validity-activation-expiry")
async def set_validity_activation_expiry(request: Request) -> dict:
    """Validity, Activation & Expiry Configuration

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setValidityActivationExpiry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/waf-policies")
async def set_waf_policy(request: Request) -> dict:
    """Change the firewall policy

    scope: region · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("setWafPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai-usage/settle")
async def settle_ai_usage(request: Request) -> dict:
    """Turn metered AI interactions into a billable usage record

    scope: tenant · permission: PLATFORM_BILLING_MANAGE · offline: False
    """
    return await run("settleAiUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/rollouts/{rolloutId}/cells/{cellId}/skip")
async def skip_rollout_cell(request: Request) -> dict:
    """Exclude a cell from this wave

    scope: platform · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("skipRolloutCell", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/rollouts/{rolloutId}/start")
async def start_rollout(request: Request) -> dict:
    """Start or continue a rollout

    scope: tenant · permission: PLATFORM_RELEASE_PROMOTE · offline: False
    """
    return await run("startRollout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/listings")
async def submit_integration_listing(request: Request) -> dict:
    """Submit an integration for certification and listing

    scope: tenant · permission: DEVELOPER_MANAGE · offline: False
    """
    return await run("submitIntegrationListing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/onboarding-applications")
async def submit_onboarding_application(request: Request) -> dict:
    """A prospect signs themselves up

    scope: tenant · permission: TENANT_VIEW · offline: False
    """
    return await run("submitOnboardingApplication", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants/{tenantId}/suspend")
async def suspend_tenant(request: Request) -> dict:
    """Suspend a tenant

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("suspendTenant", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenants/{tenantId}/terminate")
async def terminate_tenant(request: Request) -> dict:
    """Begin termination

    scope: tenant · permission: PLATFORM_TENANT_TERMINATE · offline: False
    """
    return await run("terminateTenant", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/cells/{cellId}")
async def update_cell_tier(request: Request) -> dict:
    """Change a cell's tier

    scope: tenant · permission: PLATFORM_CELL_MANAGE · offline: False
    """
    return await run("updateCellTier", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/partner-agreements/{agreementId}")
async def update_partner_agreement(request: Request) -> dict:
    """Amend, suspend or terminate

    scope: tenant · permission: PARTNER_MANAGE · offline: False
    """
    return await run("updatePartnerAgreement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/tenants/{tenantId}")
async def update_tenant(request: Request) -> dict:
    """Amend tenant details

    scope: tenant · permission: PLATFORM_TENANT_MANAGE · offline: False
    """
    return await run("updateTenant", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/releases/{reinventoryHoldId}/withdraw")
async def withdraw_release(request: Request) -> dict:
    """Withdraw a release

    scope: tenant · permission: PLATFORM_RELEASE_MANAGE · offline: False
    """
    return await run("withdrawRelease", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

