"""LedgerService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

56 operations · 25 tables touched · scope levels: region, tenant, venue
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="LedgerService", docs_url="/_docs")

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
    return {"service": "LedgerService", "operations": 56,
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



@app.post("/fiscal-periods/{periodId}/abandon-close")
async def abandon_period_close(request: Request) -> dict:
    """Abandon a close in progress

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("abandonPeriodClose", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/journal-entries/{entryId}/approve")
async def approve_journal_entry(request: Request) -> dict:
    """Approve a journal entry and post it

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("approveJournalEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fiscal-periods/{periodId}/begin-close")
async def begin_period_close(request: Request) -> dict:
    """Begin closing a period

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("beginPeriodClose", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tax/calculate")
async def calculate_tax(request: Request) -> dict:
    """Compute tax for a set of lines

    scope: venue · permission: LEDGER_VIEW · offline: True
    """
    return await run("calculateTax", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fiscal-periods/{periodId}/close")
async def close_fiscal_period(request: Request) -> dict:
    """Close a period and lock postings

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("closeFiscalPeriod", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/accounts")
async def create_account(request: Request) -> dict:
    """Create an account

    scope: region · permission: ACCOUNT_CONFIGURE · offline: False
    """
    return await run("createAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cost-centers")
async def create_cost_center(request: Request) -> dict:
    """Create a cost centre

    scope: region · permission: ACCOUNT_CONFIGURE · offline: False
    """
    return await run("createCostCenter", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/journal-entries")
async def create_journal_entry(request: Request) -> dict:
    """Post a manual journal voucher

    scope: region · permission: LEDGER_POST · offline: False
    """
    return await run("createJournalEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/legal-entities")
async def create_legal_entity(request: Request) -> dict:
    """Create a legal entity

    scope: tenant · permission: ACCOUNT_CONFIGURE · offline: False
    """
    return await run("createLegalEntity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/recognition-schedules")
async def create_recognition_schedule(request: Request) -> dict:
    """Define how a product class recognises revenue

    scope: region · permission: ACCOUNT_CONFIGURE · offline: False
    """
    return await run("createRecognitionSchedule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tax-codes")
async def create_tax_code(request: Request) -> dict:
    """Create a tax code

    scope: region · permission: TAX_CONFIGURE · offline: False
    """
    return await run("createTaxCode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/tax-exemptions")
async def create_tax_exemption(request: Request) -> dict:
    """Grant a tax exemption

    scope: region · permission: TAX_CONFIGURE · offline: False
    """
    return await run("createTaxExemption", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inter-entity-obligations/{obligationId}/dispute")
async def dispute_obligation(request: Request) -> dict:
    """One entity disagrees with the amount

    scope: tenant · permission: LEDGER_POST · offline: False
    """
    return await run("disputeObligation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/accounts/{accountId}")
async def get_account(request: Request) -> dict:
    """Read an account

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("getAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/deferred-revenue")
async def get_deferred_revenue(request: Request) -> dict:
    """Deferred revenue balance and ageing

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("getDeferredRevenue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reports/financial")
async def get_financial_report(request: Request) -> dict:
    """P&L, balance sheet or cash flow

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("getFinancialReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fx/foreign-tender")
async def get_foreign_tender_report(request: Request) -> dict:
    """What was taken in which currency

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("getForeignTenderReport", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/journal-entries/{entryId}")
async def get_journal_entry(request: Request) -> dict:
    """Read a journal entry

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("getJournalEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/settlements/{settlementId}")
async def get_settlement(request: Request) -> dict:
    """Settlement detail with match results

    scope: region · permission: SETTLEMENT_VIEW · offline: False
    """
    return await run("getSettlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ledger/trial-balance")
async def get_trial_balance(request: Request) -> dict:
    """Trial balance for a period

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("getTrialBalance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reconciliation/unified")
async def get_unified_reconciliation(request: Request) -> dict:
    """Every money source against the ledger, in one view

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("getUnifiedReconciliation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fx-rates/ingest")
async def ingest_fx_rates(request: Request) -> dict:
    """Pull rates from the configured provider

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("ingestFxRates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/settlements")
async def ingest_settlement_file(request: Request) -> dict:
    """Ingest a provider settlement file

    scope: region · permission: SETTLEMENT_RECONCILE · offline: False
    """
    return await run("ingestSettlementFile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/account-mappings")
async def list_account_mappings(request: Request) -> dict:
    """Which account each transaction type posts to

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("listAccountMappings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/accounts")
async def list_accounts(request: Request) -> dict:
    """List the chart of accounts

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("listAccounts", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cost-centers")
async def list_cost_centers(request: Request) -> dict:
    """List cost centres

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("listCostCenters", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fiscal-periods")
async def list_fiscal_periods(request: Request) -> dict:
    """List fiscal periods

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("listFiscalPeriods", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fx-rates")
async def list_fx_rates(request: Request) -> dict:
    """The rates in force

    scope: region · permission: LEDGER_VIEW · offline: True
    """
    return await run("listFxRates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fx/inter-entity")
async def list_inter_entity_obligations(request: Request) -> dict:
    """What one entity owes another

    scope: tenant · permission: LEDGER_VIEW · offline: False
    """
    return await run("listInterEntityObligations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/journal-entries")
async def list_journal_entries(request: Request) -> dict:
    """List journal entries

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("listJournalEntries", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ledger/entries")
async def list_ledger_entries(request: Request) -> dict:
    """Query the ledger

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("listLedgerEntries", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/legal-entities")
async def list_legal_entities(request: Request) -> dict:
    """List legal entities

    scope: tenant · permission: LEDGER_VIEW · offline: False
    """
    return await run("listLegalEntities", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/price-variances")
async def list_price_variances(request: Request) -> dict:
    """List price variances

    scope: venue · permission: LEDGER_VIEW · offline: False
    """
    return await run("listPriceVariances", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/recognition-schedules")
async def list_recognition_schedules(request: Request) -> dict:
    """List revenue recognition schedules

    scope: region · permission: LEDGER_VIEW · offline: False
    """
    return await run("listRecognitionSchedules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/settlements/{settlementId}/exceptions")
async def list_settlement_exceptions(request: Request) -> dict:
    """Unmatched or mismatched settlement lines

    scope: region · permission: SETTLEMENT_VIEW · offline: False
    """
    return await run("listSettlementExceptions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/settlements")
async def list_settlements(request: Request) -> dict:
    """List settlement batches

    scope: region · permission: SETTLEMENT_VIEW · offline: False
    """
    return await run("listSettlements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tax-codes")
async def list_tax_codes(request: Request) -> dict:
    """List tax codes

    scope: region · permission: LEDGER_VIEW · offline: True
    """
    return await run("listTaxCodes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tax-exemptions")
async def list_tax_exemptions(request: Request) -> dict:
    """List tax exemptions

    scope: region · permission: LEDGER_VIEW · offline: True
    """
    return await run("listTaxExemptions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/deposits")
async def record_deposit(request: Request) -> dict:
    """Money taken before the sale is complete

    scope: venue · permission: LEDGER_POST · offline: False
    """
    return await run("recordDeposit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inter-entity-obligations/{obligationId}/settle")
async def record_settlement(request: Request) -> dict:
    """One entity paid another

    scope: tenant · permission: LEDGER_POST · offline: False
    """
    return await run("recordSettlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/write-offs")
async def record_write_off(request: Request) -> dict:
    """Write off an uncollectable balance

    scope: tenant · permission: LEDGER_POST · offline: False
    """
    return await run("recordWriteOff", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/journal-entries/{entryId}/reject")
async def reject_journal(request: Request) -> dict:
    """Reject a journal awaiting approval

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("rejectJournal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fiscal-periods/{periodId}/reopen")
async def reopen_period(request: Request) -> dict:
    """Reopen a closed period

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("reopenPeriod", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/inter-entity-obligations/{obligationId}/resolve")
async def resolve_obligation_dispute(request: Request) -> dict:
    """Agree what is actually owed

    scope: tenant · permission: LEDGER_POST · offline: False
    """
    return await run("resolveObligationDispute", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/settlements/{settlementId}/exceptions")
async def resolve_settlement_exception(request: Request) -> dict:
    """Resolve a settlement exception

    scope: region · permission: SETTLEMENT_RECONCILE · offline: False
    """
    return await run("resolveSettlementException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/journal-entries/{entryId}/reverse")
async def reverse_journal_entry(request: Request) -> dict:
    """Reverse a posted entry

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("reverseJournalEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/price-variances/{varianceId}/review")
async def review_price_variance(request: Request) -> dict:
    """Record a review decision on an exception variance

    scope: venue · permission: LEDGER_APPROVE · offline: False
    """
    return await run("reviewPriceVariance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/fx/revaluation")
async def run_fx_revaluation(request: Request) -> dict:
    """Revalue monetary balances at close

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("runFxRevaluation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/recognition/run")
async def run_recognition(request: Request) -> dict:
    """Recognise earned revenue for a period

    scope: region · permission: LEDGER_POST · offline: False
    """
    return await run("runRecognition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/account-mappings")
async def set_account_mappings(request: Request) -> dict:
    """Set posting mappings

    scope: region · permission: ACCOUNT_CONFIGURE · offline: False
    """
    return await run("setAccountMappings", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/fx-rates/providers")
async def set_fx_provider(request: Request) -> dict:
    """Which provider serves which purpose

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("setFxProvider", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/fx-rates")
async def set_fx_rate(request: Request) -> dict:
    """Set a rate

    scope: region · permission: LEDGER_APPROVE · offline: False
    """
    return await run("setFxRate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/deposits/{depositId}/settle")
async def settle_deposit(request: Request) -> dict:
    """Convert to revenue, return it, or forfeit it

    scope: venue · permission: LEDGER_POST · offline: False
    """
    return await run("settleDeposit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/accounts/{accountId}")
async def update_account(request: Request) -> dict:
    """Rename, remap or deactivate an account

    scope: region · permission: ACCOUNT_CONFIGURE · offline: False
    """
    return await run("updateAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/tax-codes/{taxCodeId}")
async def update_tax_code(request: Request) -> dict:
    """Amend a tax code

    scope: region · permission: TAX_CONFIGURE · offline: False
    """
    return await run("updateTaxCode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/recognition-schedules/validate")
async def validate_recognition_schedules(request: Request) -> dict:
    """Find product kinds claimed by more than one schedule

    scope: tenant · permission: LEDGER_VIEW · offline: False
    """
    return await run("validateRecognitionSchedules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

