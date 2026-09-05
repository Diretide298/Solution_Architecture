# ADR-0038 / ADR-0039 — what was done, and how to re-verify it

**A run log, kept by hand.** The package derives almost everything and can therefore answer *"what
is true now"* at any moment — but not *"what did we do, and when"*. This file is that second
question. Every claim below names the command that produced or re-checks it.

**Every number here was re-derived on 5 September against the package as it stands**, not copied
forward from the run that produced it. Several had already moved by the time this was written, and
that is the point of re-deriving them.

---

## What this implemented

ADR-0038 and ADR-0039 were accepted on 3 September and closed with *"This ADR decides the shape and
implements none of it."* This is that implementation.

| | Before | Now |
|---|---|---|
| Databases | one, `ticvai` | `control` + one per tenant |
| `backend/` layout | flat | `control/` and `tenant/` |
| Provisioning | none | `provision-tenant.sh`, `initdb-provision.sh` |
| Deployment configs reaching one shared database | 7 of 7 | 0 of 7 |
| Service routing | fixed DSN | tenant → database via `control.cell_tenant` |

---

## Current state

```bash
python tools/check-package.py | tail -2
```
→ **PASS · 36 warnings**, 0 errors.

```bash
python -c "import json; S=json.load(open('handoff/schema-reference.json',encoding='utf-8')); \
a={t for t in S['cols'] if '.' in t and ':' not in t}; c={t for t in a if t.startswith('control.')}; \
print(len(a),'tables |',len(c),'control |',len(a)-len(c),'tenant')"
```
→ **386 tables · 50 control · 336 tenant**

```bash
find backend -name '*.sql' | wc -l                              # 34
grep -c '^CREATE SCHEMA' backend/tenant/000-schemas.sql          # 26
grep -c '^CREATE SCHEMA' backend/control/000-schemas.sql         # 1
cat backend/*/900-foreign-keys.sql | grep -c 'ALTER TABLE'       # 574
cat backend/*/910-indexes.sql | grep -c 'CREATE INDEX'           # 276
grep -c '^-- ALTER TABLE ' backend/990-cross-database-references.sql  # 20
grep -rl 'PG_DSN' deploy/ | wc -l                                # 0
```

**The 20 cross-database references are the price of the split.** Postgres has no cross-database
foreign key, so they are emitted commented-out with the index kept in whichever database the column
is in — the join did not stop happening because Postgres stopped checking it.

---

## The chain, in order

Each of these is a step in `tools/refresh.sh`. Run in this order; each reads what the previous
wrote.

| # | Command | Writes |
|---|---|---|
| 10 | `python tools/derive-schema.py` | `handoff/schema-reference.json` |
| 11 | `python tools/derive-relationships.py` | `handoff/relationship-graph.json` |
| 12 | `python tools/derive-ddl.py --apply` | `backend/control/`, `backend/tenant/`, the provisioning scripts |
| 14 | `python tools/derive-table-notes.py --apply` | table descriptions |
| 20 | `python tools/build-schema-workbook.py` | the workbook, **both copies** |
| — | `python tools/derive-diagrams.py` | `diagrams/` |
| — | `python tools/derive-mirrors.py` | `repos/` |

`deploy/` is **hand-authored — no tool writes it.** `derive-burst-scope.py` and
`derive-services.py` only read it. This was stated the other way round earlier and was wrong.

---

## Defects found and corrected

Six, of which three were root causes and three were the symptoms they produced.

**1. A contract could not withdraw a column.** Removing `tenantId` from `Cell` did not remove
`control.cell.tenant_id`. `derive-schema.py` rebuilds columns from `relationship-graph.json`, which
`derive-relationships.py` generates *from* `schema-reference.json` one step later — the loop fed
itself, so a contract-side deletion could never reach the table. Fixed with
`x-ticvai-retired-columns`, honoured in three places.

```bash
grep -c x-ticvai-retired-columns contracts/satellite/subscription.yaml   # 1
python -c "import json; S=json.load(open('handoff/schema-reference.json',encoding='utf-8')); \
print(any(c['column']=='tenant_id' for c in S['cols']['control.cell']))"   # False
```

**Re-verified by running the loop twice** — schema → relationships → schema — and confirming the
column and its edge both stay gone.

**2. The viewer never looked where the workbook is written.** `build-schema-workbook.py` ended with
a bare `wb.save('TICVAI_Schema_Reference.xlsx')`, so it landed in whatever directory it ran from.
Two copies are tracked and `derive-overview.py` documents the `handoff/` one; only the root copy was
ever rewritten, so `handoff/` held an older build and `derive-mirrors.py` shipped it to six repos.
**Seven stale workbooks from one stale source.** It read as 520 viewer warnings that the DDL had
invented columns; the DDL was right every time. Both copies are now written from one build to
absolute paths.

**3. Rule 15 read a single line, and prose wraps.** An acknowledgement that landed one line after
the ADR reference failed anyway — five deploy files, then my own first fix to a sixth. **The rule
was committing the defect it exists to catch.** It now reads a window of one line either side.

```bash
python tools/check-package.py 2>&1 | grep -c "reasons from ADR"   # 0
```

**4. Four tables were never marked written** — `fnb.table`, `identity.session`, `marketing.case`,
`retail.return`. The regex stopped at the double quote, and those four are quoted precisely because
they are Postgres reserved words.

**5. The Modules sheet's `Written` column and the viewer's `module.written` were never connected.**
The sheet writes a count under `Written`; the viewer read prose from a `Status` column the sheet
does not have. Both halves existed, named differently, so every schema drew amber regardless of the
build.

**6. `b-shared-platform.yml` bypassed its own pooler.** Its 24 services pointed at `postgres:5432`
while `pgbouncer` sat beside them unused, and their `depends_on` named postgres. **This was mine**,
introduced by the same patch that added tenant routing, and it is the one configuration where it
matters most — it is the multi-tenant scenario. Without the pooler its ceiling is 24 services × 20
connections × 3 tenants = 1,440 against `max_connections = 500`.

```bash
grep -c '@pgbouncer:5432' deploy/b-shared-platform.yml    # 48
grep -c '    - postgres$' deploy/b-shared-platform.yml    # 1, pgbouncer's own
```

---

## The package moved underneath this work

**A dump landed on 4 September between 18:46 and 19:32**, after the implementation and before this
log. `contracts/spine/cross-cell.yaml` became `cross-region.yaml`, the contracts were rewritten, and
the derivers ran on top.

**All seven changes survived and were used by that refresh** — `backend/tenant/` was rebuilt at
18:46 by the patched `derive-ddl.py`. But every number moved:

| | 4 Sep am | 5 Sep |
|---|---:|---:|
| tables | 377 | **386** |
| control tables | 46 | **50** |
| tenant schemas | 25 | **26** |
| `check-package` warnings | 17 | **36** |

**A `subscription` schema arrived** carrying `subscription.partner_quote`, and ADR-0039 said in two
places that the tenant template is 25 schemas. **Corrected to state the rule rather than the
count** — the template is every schema except `control`; the count is an output of ADR-0028's
decomposition, not of ADR-0039's decision. ADR-0038's diagram was corrected the same way.

**This is the failure `docs/active/package-edit-protocol.md` documents**: no error, no conflict,
only a changed count.

---

## ADR-0032 — answered 5 September

**The missing figure was concurrent tenants. The answer is ten at go-live, growing.**

`default_pool_size` caps server connections *per database*, so what reaches Postgres is that figure
times the number of tenant databases, plus one for `control`:

| tenants | databases | server connections | of `max_connections = 500` |
|---:|---:|---:|---:|
| 3 | 4 | 160 | 32% |
| **10** | **11** | **440** | **89%** |
| 11 | 12 | 480 | 97% |
| 12 | 13 | 520 | **over** |

**The ceiling is eleven tenants and go-live is ten — the configuration runs out one client after
launch.** ADR-0038 estimated twenty-five by leaving the control database out of the division.

**Idle tenants are free**: `min_pool_size` is unset, so pgbouncer opens connections on demand. 440
is the Saturday-evening worst case where every venue trades at once, which is when they do.

**The lever is `default_pool_size`, not `max_connections`** — halving it to 20 puts the ceiling at
24 tenants inside the same primary, where raising `max_connections` buys the same headroom and pays
for it in memory on every backend. **Not yet applied to `deploy/`** — see below.

---

## Open

**1. `PARTITION BY LIST (venue_id)` — ADR-0005 has been owed it since 12 August.** `backend/`
contains none. The rule has to be stated before it can be generated, and the choice is not obvious:

```bash
grep -rh '^\s*venue_id ' backend/tenant/*.sql | wc -l              # 68 tables carry it
grep -rh '^\s*venue_id .*NOT NULL' backend/tenant/*.sql | wc -l    # 32 of them NOT NULL
```

| Rule | Tables | Note |
|---|---:|---|
| **A — every table with a NOT NULL `venue_id`** | 32 across 14 schemas | The only set that works as written: Postgres requires the partition key to be NOT NULL and part of every unique key |
| **B — the purchase and admission path only** | 14 (`orders` 6, `catalogue` 5, `access` 3) | Where the contention actually is |
| **C — every table carrying `venue_id`** | 68 | Needs 36 columns made NOT NULL first, which is a data-model change, not a partitioning one |

**The cost driver is not the table count.** Partitioning a table forces its primary key to include
`venue_id`, so every foreign key pointing at it becomes composite:

```bash
# foreign keys pointing at the 32 NOT NULL venue_id tables
```
→ **108**. That is the blast radius of rule A, and the reason B exists.

**2. `default_pool_size` is still 40 in all seven configs.** ADR-0032 now says 20. Changing it is a
one-line edit per config plus a re-read of the burst scenarios, which assume 80.

**3. Four tables have no description** — `approvals.accreditation_badge`, `control.archival_job`,
`control.backup_run`, `control.scaling_policy`. All arrived in the 4 September dump. Fix is
`WHAT` in `tools/derive-table-notes.py`, then a tooltip each.

**4. `subscription` has no row on the Modules sheet.** A real Postgres schema, unlike the `cache:*`
stores — the viewer flags it and it should be listed.

**5. Change B — the product split** (Catalogue keeps ticket and parking; F&B and Retail own theirs;
all three through OrderService) is **not started**. It needs three decisions first: where
`giftCard` / `rental` / `addOn` go, whether F&B and Retail need a lease
(`catalogue.inventory_hold`), and whether `searchCatalogue` still spans all three.

**6. The Modules sheet says `control` has 41 tables; the DDL creates 50.** The `Tables` column is
read from `handoff/modules.json`, which is hand-maintained, while `Written` beside it is counted
from the DDL — so the same row of the same sheet reads **41 and 50**. Worth reconciling before the
provisioning script is generated from either.

```bash
python -c "import json; S=json.load(open('handoff/schema-reference.json',encoding='utf-8')); print(len([t for t in S['cols'] if t.startswith('control.')]))"    # 50
```
