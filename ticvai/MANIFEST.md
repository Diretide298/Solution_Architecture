# TICVAI design package — what is in this drop

**31 August 2026. All ten checks pass. Every link resolves.**

```
1626 operations · 28 contracts · 386 tables · 975 relationships
124 state models · 29 events · 94 flows · 39 ADRs
1091 screens · 15 platforms · 12 apps · 83 boards
```

---

## Run it

```bash
bash tools/refresh.sh          # regenerates every derived file, then runs all ten checks
python3 tools/audit-links.py --detail
```

**`refresh.sh` is the only entry point.** Everything under `handoff/`, `diagrams/`, `backend/` and
`wireframes/P*.dc.html` is derived — **hand-editing any of it is overwritten on the next run**, and
that is the point rather than a limitation.

---

## The ten checks

| | What it refuses |
|---|---|
| `check-screens` | An operation that does not exist · an audience mismatch · a destructive button with no confirmation · a placeholder module · **a guest-callable operation with no guest screen** |
| `check-frontend` | A route with no component |
| `check-flows` | A step on a screen that is not there |
| `check-states` | A status enum with no model · **an event emitted without an outbox write** |
| `check-config-scope` | A configuration operation that does not declare its level |
| `check-wireframes` | A board anchor that does not exist · **a board this package did not generate** |
| `check-backlog` | A requirement with no operation |
| `check-traceability` | A requirement that reaches nothing |
| `check-package` | 41 rules — $ref resolution, closed vocabularies, currency columns, unbounded lists, orphan writes, duplicate YAML keys, **scope columns, DDL generations, lock contents** |
| `audit-links` | Nine directions of cross-layer integrity, plus anchor collisions |

**Warnings are not failures.** 119 on screens, 51 on flows, 36 on wireframes — each is a decision
somebody has to make, and the register says which.

---

## Layout

```
contracts/      28 OpenAPI files — the source of truth. Everything else derives from here.
screens/        1091 screens across 15 platforms
flows/          94 journeys, each naming its operations
states/         124 state models
events/         29 declared events
docs/adr/       37 architecture decisions
docs/active/    the working documents — audits, briefs, handoffs
docs/registers/ conflicts (CF-*), backlog, decisions

backend/        DDL, generated — 386 tables, 0 foreign keys, 0 indexes
services/       16 FastAPI skeletons for topology benchmarking
deploy/         four deployment configurations plus three burst variants
tools/          the generators and the checks
handoff/        derived artefacts for consumers — lineage, schema, burst scope, sizing
wireframes/     83 boards, 15 generated and 65 from client design packs
sources/        every client file — MoMs, RFP, board PDFs, requirements
```

---

## The derived files a consumer should read

**`handoff/api-data-lineage.json`** — every operation with its verb, path, scope, permission,
audience, service, reads and writes. **The join everything else resolves through.**

**`handoff/schema-reference.json`** — 386 tables, every column, every reference, and a description
for all of them.

**`handoff/burst-scope.json`** — what a flash-sale environment runs, and what it does not. **Thirteen
services with `deployed: false` are in it deliberately.**

**`handoff/sizing.json`** — the replica algorithm for normal operation and for a sale, with the
venue tiers behind it.

**`handoff/relationship-graph.json`** — 959 edges across three kinds: `declared`, `convention`,
`lineage`.

**Take counts from these, not from parsing.** They come from the same pass that writes the DDL, so
a disagreement means a parser is reading something the generator did not write.

---

## 🔴 Open, and blocking

**CF-161** — one database per cell or one per service. **ADR-0028 still reads Accepted while
contradicting what the client was told on 24 August.** ADR-0036 carves out the burst cell and
settles nothing about the permanent platform.

**CF-64** — AWS or Azure, pending DESC. Carries RPO and RTO, **which are stated nowhere in 37
ADRs.**

**CF-162** — three deployment scenarios. Answered in `docs/active/`, not yet with the client.

**CF-165** — retention and archival absent. Three failure tables now exist and none has a retention
rule.

---

## 🔴 Two things in this drop that are wrong

**The cost tables understate by roughly half.** `TICVAI_Hosting_Summary` and
`TICVAI_Deployment_Technical` quote $3,485 for the shared cell on Fargate pricing **while shipping a
compose file** — nobody running that file arrives at that figure. And **~$4,400 is missing**:
staging, dev, observability and support, of which staging and dev are $3,000 and are required by
Allam's own release workflow.

**Nothing has been benchmarked.** `tools/bench.py` exists and has never run against anything. Every
replica count, every per-replica figure and every latency target is a hypothesis with a named way
to falsify it. **`rpsPerReplica` is the one that matters most and the one least likely to be
right.**

---

## Where the real risk sits

**Design is 93% of in-scope requirements. Build is 0% of code, though the DDL now exists.**

**And the thing that cost a client relationship in Bahrain is contention, not throughput.** Thirty
thousand concurrent generates 3,750 RPS, which the arithmetic absorbs at 35 replicas. **What failed
was thirty thousand people wanting the same row**, and the only measurement that reaches it is
`holdContentionMs` under `--pattern hot-venue`.

**ADR-0037 should take that from 167 holds a second to 2,000 by removing a Redis round trip from
inside a lock.** Until it is measured, that is arithmetic.
