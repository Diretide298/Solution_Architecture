"""AiService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

30 operations · 45 tables touched · scope levels: region, tenant, venue
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="AiService", docs_url="/_docs")

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
    return {"service": "AiService", "operations": 30,
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



@app.post("/conversations")
async def create_ai_conversation(request: Request) -> dict:
    """Open a conversation

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("createAiConversation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/collections")
async def create_knowledge_collection(request: Request) -> dict:
    """Create a collection

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("createKnowledgeCollection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/proposed-actions/{actionId}/decide")
async def decide_proposed_action(request: Request) -> dict:
    """Approve or reject a proposal

    scope: venue · permission: AI_APPROVE · offline: False
    """
    return await run("decideProposedAction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/generate/configuration")
async def generate_configuration(request: Request) -> dict:
    """Draft a configuration from a description

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("generateConfiguration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/generate/venue-layout")
async def generate_venue_layout(request: Request) -> dict:
    """Draft a seat map from an uploaded plan

    scope: venue · permission: CAPACITY_CONFIGURE · offline: False
    """
    return await run("generateVenueLayout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/policy")
async def get_ai_policy(request: Request) -> dict:
    """What the assistant may do here

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("getAiPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/usage")
async def get_ai_usage(request: Request) -> dict:
    """Usage, cost and performance

    scope: tenant · permission: AI_AUDIT_VIEW · offline: False
    """
    return await run("getAiUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/collections/{collectionId}/documents")
async def ingest_knowledge_document(request: Request) -> dict:
    """Add a document

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("ingestKnowledgeDocument", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/conversations")
async def list_ai_conversations(request: Request) -> dict:
    """A principal's conversation history

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("listAiConversations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/interactions")
async def list_ai_interactions(request: Request) -> dict:
    """Every prompt, response and action

    scope: tenant · permission: AI_AUDIT_VIEW · offline: False
    """
    return await run("listAiInteractions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/providers")
async def list_ai_providers(request: Request) -> dict:
    """Configured providers and their order

    scope: region · permission: AI_CONFIGURE · offline: False
    """
    return await run("listAiProviders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/index-jobs")
async def list_index_jobs(request: Request) -> dict:
    """Indexing in flight and recently finished

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("listIndexJobs", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/index-sources")
async def list_index_sources(request: Request) -> dict:
    """What is indexed, and how current it is

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("listIndexSources", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/collections")
async def list_knowledge_collections(request: Request) -> dict:
    """Collections available to this tenant

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("listKnowledgeCollections", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/proposed-actions")
async def list_proposed_actions(request: Request) -> dict:
    """What the assistant has proposed and nobody has decided

    scope: venue · permission: AI_APPROVE · offline: False
    """
    return await run("listProposedActions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai/translate")
async def propose_translations(request: Request) -> dict:
    """proposeTranslations

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("proposeTranslations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai/venue-map/{mapId}/propose-labels")
async def propose_venue_labels(request: Request) -> dict:
    """Suggest what each extracted shape is

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("proposeVenueLabels", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai/venue-map/{mapId}/propose-walkways")
async def propose_walkways(request: Request) -> dict:
    """Find walkable space in a drawing that has no vectors

    scope: venue · permission: VENUE_MAP_MANAGE · offline: False
    """
    return await run("proposeWalkways", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai/suggestions/{suggestionId}/outcome")
async def record_suggestion_outcome(request: Request) -> dict:
    """recordSuggestionOutcome

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("recordSuggestionOutcome", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/index-sources/{sourceId}/reindex")
async def reindex_source(request: Request) -> dict:
    """Rebuild a source

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("reindexSource", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/index-sources/{sourceId}/entries/{entryId}")
async def remove_index_entry(request: Request) -> dict:
    """Remove one record from the index

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("removeIndexEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai/suggestions")
async def request_suggestion(request: Request) -> dict:
    """requestSuggestion

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("requestSuggestion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/search")
async def semantic_search(request: Request) -> dict:
    """Search meaning, not words

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("semanticSearch", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/messages")
async def send_ai_message(request: Request) -> dict:
    """Ask

    scope: venue · permission: AI_USE · offline: False
    """
    return await run("sendAiMessage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/ai-providers/{providerId}/credential")
async def set_ai_credential(request: Request) -> dict:
    """Store or rotate a provider key

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("setAiCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/policy")
async def set_ai_policy(request: Request) -> dict:
    """Set the policy

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("setAiPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/providers")
async def set_ai_provider(request: Request) -> dict:
    """Configure a provider

    scope: region · permission: AI_CONFIGURE · offline: False
    """
    return await run("setAiProvider", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/index-sources")
async def set_index_source(request: Request) -> dict:
    """Declare a source indexed

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("setIndexSource", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/ai/suggestion-providers")
async def set_suggestion_provider(request: Request) -> dict:
    """setSuggestionProvider

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("setSuggestionProvider", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/ai-providers/{providerId}/test")
async def test_ai_provider(request: Request) -> dict:
    """Check the key works before anyone relies on it

    scope: tenant · permission: AI_CONFIGURE · offline: False
    """
    return await run("testAiProvider", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

