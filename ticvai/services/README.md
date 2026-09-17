# Benchmark harness — three topologies, one workload

**Generated. `tools/derive-services.py` and `tools/derive-ddl.py` rebuild all of it.**

## Run it

```bash
docker compose -f services/compose.hybrid.yml up -d      # 28 services
docker compose -f services/compose.all-venue.yml up -d   # 50
docker compose -f services/compose.all-tenant.yml up -d  # 50

pip install aiohttp
python3 tools/bench.py --topology hybrid --pattern hot-venue --rps 1000 --seconds 300
```

**Postgres loads `backend/*.sql` on first start** — 388 tables, 569 foreign keys, 279 indexes.

## What is measured honestly

Latency avg/p95/p99 · achieved RPS against target · error rate and status codes · connection
count and pool saturation per service (`/_health`) · cold start to a filled pool · **lease
contention on a hot performance**, which is where a flash sale actually fails.

**A declared write is a `SELECT … FOR UPDATE` on the written table**, scoped where the table has a
`scope_path`, so `--pattern hot-venue` puts every caller on the same row. That is a real row lock
held to end of transaction, which is what makes contention measurable.

**It emitted `SELECT count(*)` until 3 September** — a sequential scan taking no lock at all — so
every contention figure produced before that date measured nothing and should be discarded.

## What is not, and the harness says so

**Application CPU under real business logic.** A skeleton executes the declared reads and writes
and returns; there is no pricing, no promotion evaluation, no PDF. **The database work is the part
that varies with topology and it is measured; the rest is not and should not be reported.**

**Write amplification.** The lock is real and the row change is not — a write runs inside a
transaction that always rolls back, so nothing accumulates and the second run measures the same
table as the first. **WAL volume, index maintenance and vacuum pressure are therefore absent**, and
a sustained-write projection cannot be taken from this harness.

**Autoscale reaction** needs an orchestrator. Compose gives fixed replicas, which measures a
topology at a size rather than its scaling behaviour.

## The one rule

**Only placement changes between the three files.** Same images, same Postgres flags, same Redis,
same CPU and memory limits, same pool ratios. **Anything else differing invalidates the
comparison**, and that is easy to do by accident when tuning one of them.
