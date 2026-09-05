"""ReportingService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

29 operations · 22 tables touched · scope levels: tenant, venue
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="ReportingService", docs_url="/_docs")

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
    return {"service": "ReportingService", "operations": 29,
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



@app.post("/alerts/{alertId}/acknowledge")
async def acknowledge_alert(request: Request) -> dict:
    """Take responsibility for it

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("acknowledgeAlert", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reports/ask")
async def ask_reporting_question(request: Request) -> dict:
    """Natural-language reporting query

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("askReportingQuestion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/report-executions/{executionId}")
async def cancel_report_execution(request: Request) -> dict:
    """Cancel a running execution

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("cancelReportExecution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/dashboards")
async def create_dashboard(request: Request) -> dict:
    """Create a dashboard

    scope: tenant · permission: REPORT_MANAGE · offline: False
    """
    return await run("createDashboard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reports")
async def create_report(request: Request) -> dict:
    """Create a custom report definition

    scope: venue · permission: REPORT_MANAGE · offline: False
    """
    return await run("createReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/report-schedules")
async def create_report_schedule(request: Request) -> dict:
    """Schedule a report

    scope: venue · permission: REPORT_SCHEDULE · offline: False
    """
    return await run("createReportSchedule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/reports/{reportId}")
async def delete_report(request: Request) -> dict:
    """Retire a report definition

    scope: venue · permission: REPORT_MANAGE · offline: False
    """
    return await run("deleteReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/report-schedules/{scheduleId}")
async def delete_report_schedule(request: Request) -> dict:
    """Delete a schedule

    scope: venue · permission: REPORT_SCHEDULE · offline: False
    """
    return await run("deleteReportSchedule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/report-executions/{executionId}/export")
async def export_report_result(request: Request) -> dict:
    """Export a completed result

    scope: venue · permission: REPORT_EXPORT · offline: False
    """
    return await run("exportReportResult", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dashboards/{dashboardId}")
async def get_dashboard(request: Request) -> dict:
    """Read a dashboard with tile data

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("getDashboard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reports/{reportId}")
async def get_report(request: Request) -> dict:
    """Read a report definition

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("getReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/report-executions/{executionId}")
async def get_report_execution(request: Request) -> dict:
    """Execution status and result

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("getReportExecution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/report-exports/{exportId}")
async def get_report_export(request: Request) -> dict:
    """Export status and download link

    scope: venue · permission: REPORT_EXPORT · offline: False
    """
    return await run("getReportExport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/report-executions/{executionId}/result")
async def get_report_result(request: Request) -> dict:
    """Paged result rows

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("getReportResult", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/suppliers/{supplierId}/performance")
async def get_supplier_performance(request: Request) -> dict:
    """getSupplierPerformance

    scope: venue · permission: REPORT_VIEW · offline: False
    """
    return await run("getSupplierPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/alert-rules")
async def list_alert_rules(request: Request) -> dict:
    """What raises an alert, and when

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listAlertRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/alerts")
async def list_alerts(request: Request) -> dict:
    """What is currently raised

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listAlerts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dashboards")
async def list_dashboards(request: Request) -> dict:
    """List dashboards

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listDashboards", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/report-executions")
async def list_report_executions(request: Request) -> dict:
    """List executions

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listReportExecutions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/report-fields")
async def list_report_fields(request: Request) -> dict:
    """Fields available for a data source

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listReportFields", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/report-schedules")
async def list_report_schedules(request: Request) -> dict:
    """List scheduled reports

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listReportSchedules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reports")
async def list_reports(request: Request) -> dict:
    """List available report definitions

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listReports", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reports/seeded")
async def list_seeded_reports(request: Request) -> dict:
    """listSeededReports

    scope: venue · permission: REPORT_VIEW · offline: False
    """
    return await run("listSeededReports", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reports/{reportId}/run")
async def run_report(request: Request) -> dict:
    """Run a report

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("runReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reports/ask/{conversationId}/save")
async def save_natural_language_query(request: Request) -> dict:
    """Save a natural-language answer as a report definition

    scope: venue · permission: REPORT_MANAGE · offline: False
    """
    return await run("saveNaturalLanguageQuery", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/alert-rules")
async def set_alert_rule(request: Request) -> dict:
    """Raise an alert when a number leaves a range

    scope: venue · permission: REPORT_MANAGE · offline: False
    """
    return await run("setAlertRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/dashboards/{dashboardId}")
async def update_dashboard(request: Request) -> dict:
    """Update a dashboard

    scope: tenant · permission: REPORT_MANAGE · offline: False
    """
    return await run("updateDashboard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/reports/{reportId}")
async def update_report(request: Request) -> dict:
    """Publish a new version of a definition

    scope: venue · permission: REPORT_MANAGE · offline: False
    """
    return await run("updateReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/report-schedules/{scheduleId}")
async def update_report_schedule(request: Request) -> dict:
    """Amend, pause or resume a schedule

    scope: venue · permission: REPORT_SCHEDULE · offline: False
    """
    return await run("updateReportSchedule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

