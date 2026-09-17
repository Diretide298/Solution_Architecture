#!/usr/bin/env python3
"""Generate runnable service skeletons from the contracts, for topology benchmarking.

**The purpose is to measure deployment topology, not business logic.** A benchmark comparing
per-venue, per-tenant and shared placement needs services that connect, query the real schema, and
return — it does not need a working till.

**What the lineage already supplies**, per operation: verb, path, scope, permission, the tables it
reads and writes, and the stores it touches. That is the shape of the database work. **The
application CPU on top of it is the part nobody can predict from a spec**, and it is usually not
the bottleneck — the connections and the contended rows are.

**So a skeleton executes the real reads and writes against the real tables and does nothing else.**
Latency, connection count, cache behaviour and lease contention come out honest. Business-logic CPU
does not, and the harness says so rather than pretending.

Writes:

    services/<name>/app.py          FastAPI app, one route per operation
    services/<name>/queries.py      the reads and writes, generated
    services/<name>/Dockerfile
    services/<name>/requirements.txt
    services/compose.<topology>.yml shared | per-tenant | per-venue

Run: `python3 tools/derive-services.py [--apply]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "services"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _key_of(table: str, names) -> str | None:
    """The column a row is locked by. Same precedence as `derive-ddl.key_of`.

    **The two must agree** — this picks the column a benchmark locks and that one picks the column
    a foreign key points at, and a benchmark contending on a column nothing references is measuring
    a lock nobody takes in production.
    """
    if "id" in names:
        return "id"
    stem = table.split(".", 1)[1]
    for cand in (f"{stem}_id", f"{stem.rstrip('s')}_id", f"{stem}_code"):
        if cand in names:
            return cand
    return None


def route_path(p: str) -> str:
    """OpenAPI path to FastAPI path. Both use `{param}`, so this only normalises."""
    return p if p.startswith("/") else "/" + p


APP = '''"""{svc} — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

{n} operations · {tables} tables touched · scope levels: {scopes}
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="{svc}", docs_url="/_docs")

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
                       "postgres://ticvai:ticvai@pgbouncer:6432/{{database}}")
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
pools: dict[str, asyncpg.Pool] = {{}}
databases: dict[str, str] = {{}}
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
    return {{"service": "{svc}", "operations": {n},
            "coldStartMs": getattr(app.state, "cold_start_ms", None),
            "tenantPools": len(pools),
            "poolSize": sum(p.get_size() for p in pools.values()),
            "poolIdle": sum(p.get_idle_size() for p in pools.values()),
            "controlPoolSize": control_pool.get_size() if control_pool else 0}}


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
    return {{"op": op, "rows": rows, "ms": round((time.perf_counter() - t0) * 1000, 2)}}

{routes}
'''

ROUTE = '''

@app.{verb}("{path}")
async def {fn}(request: Request) -> dict:
    """{summary}

    scope: {scope} · permission: {perm} · offline: {offline}
    """
    return await run("{op}", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))
'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    sch = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    # Only what Postgres holds gets SQL. A Redis-stored table — the two session registries — is
    # touched as a cache key, which is what the deployed service would do; querying it as a table
    # measured a store the topology does not have.
    store = sch.get("store") or {}
    redis_tables = {t for t, v in store.items() if v == "redis" and ":" not in t}
    real = {t for t in sch["cols"] if "." in t and ":" not in t
            and store.get(t, "postgres") in ("postgres", "postgres-analytical")}

    by_svc: dict[str, list] = defaultdict(list)
    for op, v in lin.items():
        if v.get("service"):
            by_svc[v["service"]].append((op, v))

    made = 0
    for svc, ops in sorted(by_svc.items()):
        routes = []
        reads: dict[str, list] = {}
        writes: dict[str, list] = {}
        caches: dict[str, list] = {}
        seen_fn = set()
        tables = set()

        for op, v in sorted(ops):
            fn = snake(op)
            if fn in seen_fn:
                continue
            seen_fn.add(fn)

            # **A read is a scope-filtered select on the declared table.** The filter is what makes
            # the query realistic — an unfiltered count measures the table size, not the workload.
            r = []
            for t in v.get("reads", []):
                if t not in real:
                    continue
                tables.add(t)
                cols = {c["column"] for c in sch["cols"][t]}
                if "scope_path" in cols:
                    r.append(f"SELECT * FROM {t} WHERE scope_path LIKE $1 LIMIT 50")
                else:
                    r.append(f"SELECT * FROM {t} LIMIT 50")
            if r:
                reads[op] = r

            # **A write takes the row lock a write takes.** Until 3 September this emitted
            # `SELECT count(*) FROM <table>` — a sequential scan that locks nothing. Across all
            # sixteen services that was 799 statements and **not one row lock**, while
            # `services/README.md`, `tools/bench.py` and `deploy/c-flash-sale.yml` all sent the
            # reader here to measure lease contention. **The one number the burst work exists for
            # was the one number the harness could not produce.**
            #
            # `SELECT … FOR UPDATE` takes a real lock held to end of transaction, without having to
            # invent a value for every NOT NULL column in 374 tables — **and invented values
            # distort a measurement as much as a missing lock does.**
            #
            # **Scoped, so `--pattern hot-venue` concentrates on one row.** That is what the
            # pattern is for: 30,000 people buying for one event at one venue is not more requests,
            # it is the same requests against the same rows.
            w = []
            for t in v.get("writes", []):
                if t not in real:
                    continue
                tables.add(t)
                cols = {c["column"] for c in sch["cols"][t]}
                key = _key_of(t, cols)
                if not key:
                    continue
                if "scope_path" in cols:
                    w.append(f"SELECT {key} FROM {t} WHERE scope_path LIKE $1 "
                             f"ORDER BY {key} LIMIT 1 FOR UPDATE")
                else:
                    w.append(f"SELECT {key} FROM {t} ORDER BY {key} LIMIT 1 FOR UPDATE")
            if w:
                writes[op] = w[:2]

            c = [k if k.startswith("cache:") else f"cache:{k}"
                 for k in v.get("reads", []) + v.get("writes", [])
                 if k.startswith("cache:") or k in redis_tables]
            if c:
                caches[op] = [f"{k}:bench" for k in dict.fromkeys(c)]

            routes.append(ROUTE.format(
                verb=v["verb"].lower(), path=route_path(v["path"]), fn=fn, op=op,
                summary=(v.get("summary") or op).replace('"', "'")[:90],
                scope=v.get("scope") or "-", perm=v.get("perm") or "-",
                offline=bool(v.get("offline"))))

        scopes = sorted({v.get("scope") for _, v in ops if v.get("scope")})
        app_py = APP.format(svc=svc, n=len(seen_fn), tables=len(tables),
                            scopes=", ".join(scopes), routes="".join(routes))
        q_py = (
            '"""Generated. The declared reads and writes of each operation."""\n\n'
            f"READS = {json.dumps(reads, indent=1)}\n\n"
            f"WRITES = {json.dumps(writes, indent=1)}\n\n"
            f"CACHE = {json.dumps(caches, indent=1)}\n")

        if a.apply:
            d = OUT / svc
            d.mkdir(parents=True, exist_ok=True)
            (d / "app.py").write_text(app_py, encoding="utf-8")
            (d / "queries.py").write_text(q_py, encoding="utf-8")
            (d / "requirements.txt").write_text(
                "fastapi==0.115.0\nuvicorn[standard]==0.30.6\nasyncpg==0.29.0\nredis==5.0.8\n",
                encoding="utf-8")
            (d / "Dockerfile").write_text(
                "FROM python:3.12-slim\n"
                "WORKDIR /app\n"
                "COPY requirements.txt .\n"
                "RUN pip install --no-cache-dir -r requirements.txt\n"
                "COPY . .\n"
                '# **One worker per container.** Horizontal scaling is what is being measured;\n'
                '# adding workers inside a container hides the topology behind process count.\n'
                'CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]\n',
                encoding="utf-8")
        made += 1

    print(f"  {made} services · {sum(len(v) for v in by_svc.values())} operations")
    if not a.apply:
        print("  nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
