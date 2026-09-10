# TICVAI design package — what is in this drop

**10 September 2026. Fifteen of seventeen checks pass; the two that do not are named below.**

```
1628 operations · 28 contracts · 388 tables · 978 relationships
125 state models · 29 events · 96 flows · 44 ADRs
1235 screens · 15 platforms · 12 frontends · 5 apps · 21 boards
```

**`96 flows` counts authored journeys.** 72 more are derived from the client boards and carry
`provenance: derived-from-board` — they route screens the client specified and do not yet say
why anyone walks them. `check-board-flows` reports the two apart, because a number a generator can
move is not a measure of progress.

**`12 frontends` and `5 apps` are different units and both are real.** A frontend is the build
unit, one per platform, each joining to a `frontend/*.yaml` manifest that `check-frontend` and
`check-package` validate. An app is what a user installs — guest, venue-pos,
venue-staff-mobile, venue-management, ticvai-control — decided 10 September and carried
as `platform.targetApp`.

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

## The seventeen checks

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
| `check-board-flows` | **A client board no process flow describes** · a flow step naming a screen that does not exist |
| `check-screen-redundancy` | Two screens that are the same screen |
| `check-bindings` | A component bound to nothing |
| `check-migrations` | A schema change with no migration |
| `audit-links` | Nine directions of cross-layer integrity, plus anchor collisions |
| `audit-workbooks` | A workbook section that no longer matches the package |
| `audit-pack-citations` | A citation pointing at a pack or page that is not there |
| `audit-transitions` | **Coverage, not a rule** · the share of navigation edges carrying an authored label |

**Warnings are not failures.** 913 on screens, 37 on flows, 5 on wireframes — each is a
decision somebody has to make, and the register says which.

**Two checks do not pass, and both are real work rather than noise.**

- **`check-board-flows` — 4 dangling references.** `F06 Guest enters the venue` names `SCN-005`,
  `SCN-006`, `SCN-010` and `SCN-012` — its denial, override and offline paths — and none of
  those four screens exists. The flow does not lack a denial path; it describes one that was
  deleted out from under it.
- **`check-package` — 16 errors.** Long-standing and tracked in the registers.

`audit-links` reports 23 broken links, which is the standing baseline rather than a regression.

---

## Layout

```
contracts/      28 OpenAPI files — the source of truth. Everything else derives from here.
screens/        1235 screens across 15 platforms
flows/          168 journeys · 96 authored, 72 derived from the client boards
states/         125 state models
events/         29 declared events
docs/adr/       44 architecture decisions
docs/active/    the working documents — audits, briefs, handoffs
docs/registers/ conflicts (CF-*), backlog, decisions

backend/        DDL, generated — 388 tables, 574 foreign keys, 278 indexes
services/       16 FastAPI skeletons for topology benchmarking
deploy/         four deployment configurations plus three burst variants
tools/          the generators and the checks
handoff/        derived artefacts for consumers — lineage, schema, burst scope, sizing
wireframes/     21 boards · 15 per platform, 5 per shipped app, 1 index. All
                generated. The 65 client-pack boards were archived on 10 September, and
                every screen that pointed at one was repointed rather than orphaned.
sources/        every client file — MoMs, RFP, board PDFs, requirements
```

---

## The derived files a consumer should read

**`handoff/api-data-lineage.json`** — every operation with its verb, path, scope, permission,
audience, service, reads and writes. **The join everything else resolves through.**

**`handoff/schema-reference.json`** — 388 tables, every column, every reference, and a description
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

**Design is 90% of in-scope requirements. Build is 33%, and the DDL exists.**

**And the thing that cost a client relationship in Bahrain is contention, not throughput.** Thirty
thousand concurrent generates 3,750 RPS, which the arithmetic absorbs at 35 replicas. **What failed
was thirty thousand people wanting the same row**, and the only measurement that reaches it is
`holdContentionMs` under `--pattern hot-venue`.

**ADR-0037 should take that from 167 holds a second to 2,000 by removing a Redis round trip from
inside a lock.** Until it is measured, that is arithmetic.
