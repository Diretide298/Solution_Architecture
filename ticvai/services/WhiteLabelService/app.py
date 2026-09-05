"""WhiteLabelService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

50 operations · 18 tables touched · scope levels: tenant
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="WhiteLabelService", docs_url="/_docs")

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
    return {"service": "WhiteLabelService", "operations": 50,
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



@app.post("/tenant-domains")
async def claim_custom_domain(request: Request) -> dict:
    """Claim a domain and get a verification token

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("claimCustomDomain", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/banners")
async def create_banner(request: Request) -> dict:
    """Create a banner

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("createBanner", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/content-blocks")
async def create_content_block(request: Request) -> dict:
    """Author a block of content

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("createContentBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/pages")
async def create_content_page(request: Request) -> dict:
    """Create a content page

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("createContentPage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/preview")
async def create_preview(request: Request) -> dict:
    """Generate a preview link

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("createPreview", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/promo-blocks")
async def create_promo_block(request: Request) -> dict:
    """Create a promotional block

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("createPromoBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/tenant-config/banners/{bannerId}")
async def delete_banner(request: Request) -> dict:
    """Delete a banner

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("deleteBanner", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/tenant-config/pages/{pageId}")
async def delete_content_page(request: Request) -> dict:
    """Delete a content page

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("deleteContentPage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/tenant-config/promo-blocks/{promoBlockId}")
async def delete_promo_block(request: Request) -> dict:
    """Delete a promotional block

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("deletePromoBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/versions/{version}/diff")
async def diff_config_version(request: Request) -> dict:
    """Compare a version against the working draft

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("diffConfigVersion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/app-icons")
async def get_app_icons(request: Request) -> dict:
    """Read app icon set

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getAppIcons", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/brand")
async def get_brand_identity(request: Request) -> dict:
    """Read brand identity

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getBrandIdentity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/features")
async def get_feature_toggles(request: Request) -> dict:
    """Read tenant feature toggles

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getFeatureToggles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/fonts")
async def get_fonts(request: Request) -> dict:
    """Read font configuration

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getFonts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/homepage")
async def get_homepage_layout(request: Request) -> dict:
    """Read homepage layout

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getHomepageLayout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/modules")
async def get_module_enablement(request: Request) -> dict:
    """Read module enablement

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getModuleEnablement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/navigation")
async def get_navigation(request: Request) -> dict:
    """Read navigation

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getNavigation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/status")
async def get_tenant_app_status(request: Request) -> dict:
    """App status and recent changes

    scope: tenant · permission: - · offline: True
    """
    return await run("getTenantAppStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config")
async def get_tenant_config(request: Request) -> dict:
    """Full working configuration

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getTenantConfig", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/theme")
async def get_theme(request: Request) -> dict:
    """Read colour theme

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("getTheme", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/banners")
async def list_banners(request: Request) -> dict:
    """List banners

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("listBanners", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/versions")
async def list_config_versions(request: Request) -> dict:
    """Version history

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("listConfigVersions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/pages")
async def list_content_pages(request: Request) -> dict:
    """List custom content pages

    scope: tenant · permission: TENANT_CONFIGURE · offline: True
    """
    return await run("listContentPages", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-domains")
async def list_custom_domains(request: Request) -> dict:
    """The domains this tenant has claimed

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("listCustomDomains", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/faqs")
async def list_faqs(request: Request) -> dict:
    """List FAQs

    scope: tenant · permission: TENANT_CONFIGURE · offline: True
    """
    return await run("listFaqs", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/policies")
async def list_policies(request: Request) -> dict:
    """List legal policies

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("listPolicies", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenant-config/promo-blocks")
async def list_promo_blocks(request: Request) -> dict:
    """List promotional blocks

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("listPromoBlocks", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/content-blocks/{blockId}/publish")
async def publish_content_block(request: Request) -> dict:
    """Publish now, or schedule it

    scope: tenant · permission: TENANT_PUBLISH · offline: False
    """
    return await run("publishContentBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/publish")
async def publish_tenant_config(request: Request) -> dict:
    """Publish the working draft

    scope: tenant · permission: TENANT_PUBLISH · offline: False
    """
    return await run("publishTenantConfig", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/tenant-domains/{domainId}")
async def release_custom_domain(request: Request) -> dict:
    """Give the domain up

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("releaseCustomDomain", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/versions/{version}/restore")
async def restore_config_version(request: Request) -> dict:
    """Restore a previous version

    scope: tenant · permission: TENANT_PUBLISH · offline: False
    """
    return await run("restoreConfigVersion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/app-icons")
async def set_app_icons(request: Request) -> dict:
    """Set app icons

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setAppIcons", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/brand")
async def set_brand_identity(request: Request) -> dict:
    """Set logo, favicon and splash

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setBrandIdentity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/faqs")
async def set_faqs(request: Request) -> dict:
    """Set FAQ categories and entries

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setFaqs", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/features")
async def set_feature_toggles(request: Request) -> dict:
    """Set feature toggles

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setFeatureToggles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/fonts")
async def set_fonts(request: Request) -> dict:
    """Set fonts

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setFonts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/footer")
async def set_footer(request: Request) -> dict:
    """Footer columns, legal links and social

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setFooter", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/header")
async def set_header(request: Request) -> dict:
    """Configure the header

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setHeader", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/homepage")
async def set_homepage_layout(request: Request) -> dict:
    """Set homepage section order

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setHomepageLayout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/languages")
async def set_languages(request: Request) -> dict:
    """Set enabled languages and default

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setLanguages", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/status")
async def set_maintenance_mode(request: Request) -> dict:
    """Enable or clear maintenance mode

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setMaintenanceMode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/modules")
async def set_module_enablement(request: Request) -> dict:
    """Enable or disable modules

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setModuleEnablement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/navigation")
async def set_navigation(request: Request) -> dict:
    """Set main and overflow navigation

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setNavigation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/policies/{policyKind}")
async def set_policy(request: Request) -> dict:
    """Publish a policy version

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/theme")
async def set_theme(request: Request) -> dict:
    """Set colour theme

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setTheme", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/tenant-config/banners/{bannerId}")
async def update_banner(request: Request) -> dict:
    """Amend or activate a banner

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("updateBanner", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenant-config/pages/{pageId}")
async def update_content_page(request: Request) -> dict:
    """Amend a content page

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("updateContentPage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/tenant-config/promo-blocks/{promoBlockId}")
async def update_promo_block(request: Request) -> dict:
    """Amend a promotional block

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("updatePromoBlock", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-config/validate")
async def validate_tenant_config(request: Request) -> dict:
    """Validate the working draft

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("validateTenantConfig", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tenant-domains/{domainId}/verify")
async def verify_custom_domain(request: Request) -> dict:
    """Check the record and issue the certificate

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("verifyCustomDomain", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

