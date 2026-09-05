# Audit — the 3 September dump, its checks, and what trickles down

**Scope.** Every file added or changed since `8974191`, the ten checks that guard them, and the
derivation chain from `contracts/` through `handoff/` to `backend/`, `services/` and `deploy/`.

**Headline.** `MANIFEST.md` opens with *"All ten checks pass. Every link resolves."* **Three of the
ten fail on a clean run**, and the DDL this drop ships cannot be applied to Postgres. Neither is
caught by anything in `tools/`, and that is the more useful half of the finding: the failures are
in the gaps between the checks, not inside them.

---

## 1. The checks, as run

| Check | Result |
|---|---|
| check-screens | PASS · 119 warnings |
| check-frontend | PASS · 1 warning |
| check-flows | PASS · 51 warnings |
| **check-states** | **FAIL — 4 errors** |
| check-config-scope | PASS |
| check-wireframes | PASS · 36 warnings |
| check-backlog | PASS · 1 warning |
| check-traceability | PASS |
| **check-package** | **FAIL — 9 errors, 19 warnings** |
| **audit-links** | **FAIL — 2 broken links** |

---

## 2. The root cause of most of it: `cross-cell.yaml` was never deleted

`contracts/spine/cross-region.yaml` is a **near-verbatim copy** of `contracts/spine/cross-cell.yaml`
— 1,261 lines against 1,268. The only differences are one word in a description and the
`x-ticvai-lock-excludes` block that ADR-0037 requires.

The rename is otherwise complete. **Nothing in the package references `cross-cell` any more** —
not one satellite contract, not `check-package.py:140`, not `build-schema-workbook.py:354`, not a
diagram. The old file is an orphan that is still being loaded.

`contract_io.py:94` and every check glob `contracts/*/*.yaml`, so **both files load and 16
operationIds are declared twice**:

```
createGuestLink · getGuestLink · revokeGuestLink · resolveGuestLink
propagateCrossRegionEntitlement · getCrossRegionEntitlement
revokeCrossRegionEntitlement · consumeCrossRegionEntitlement
reconcileRedemptions · authoriseWalletSpend · captureWalletAuthorisation
releaseWalletAuthorisation · getWalletAllocation · setWalletAllocationPolicy
createDsarRequest · getDsarRequest
```

**Two tools in the same pipeline resolve the same operationId to different files.**
`handoff/api-data-lineage.json` attributes `authoriseWalletSpend` to `cross-region` — a dict
overwrite, last file wins. `check-package.py:869` iterates files instead, reaches `cross-cell`
first, and reports:

> `authoriseWalletSpend: declares a lock and not what sits outside it — ADR-0037 requires x-ticvai-lock-excludes`

**The ADR-0037 fix was made. It landed in the file that does not win that loop.** Deleting
`contracts/spine/cross-cell.yaml` clears that error, the `tooltip and contract set disagree about
'cross-cell'` error, and brings the file count to the 28 contracts the docs already claim.

**Nothing detects the duplication.** There is no rule anywhere in the ten checks that a given
`operationId` appears in exactly one contract. `check-package` rule 18 catches duplicate keys
*inside one mapping* and stops there. Every count in the package reads 1,032 because every loader
de-duplicates by dict key on the way in.

---

## 3. `check-states` — four errors, all stale references

```
FAIL  entitlement.yaml: enum access.TicketStatus not found — that schema exists and is an
      object, not an enum, so these states are checked against nothing
FAIL  redemption-right.yaml: enum cross-cell.RedemptionRight.status not found
FAIL  redemption-right.yaml: transition active->exhausted names unknown operation 'consumeRedemptionRight'
FAIL  redemption-right.yaml: transition active->revoked names unknown operation 'revokeRedemptionRight'
```

`RedemptionRight` no longer exists in any contract. `states/redemption-right.yaml` and
`diagrams/lld/lifecycles/redemption-right.yaml` survived the August rename that produced
`CrossRegionEntitlement` / `consumeCrossRegionEntitlement` / `revokeCrossRegionEntitlement`.
`states/cross-region-entitlement.yaml` is the live model and it is in this drop.

`entitlement.yaml` is the subtler one, and `contracts/spine/access.yaml:1784` already documents it:
*"Not `TicketStatus` — that is a validation result with a misleading name."* The state model still
points at it. The lifecycle it means is `orders.EntitlementStatus`.

These two are also the two broken links `audit-links` reports. **Same defect, counted twice.**

---

## 4. The DDL does not apply

`backend/` is the largest new artefact — 29 files, 374 tables, 580 foreign keys, 254 indexes.
Parsed and checked against Postgres's own rules:

### 52 of 580 foreign-key statements will be rejected

**37 type mismatches.** Postgres will not create a foreign key between `uuid` and `text`:

```
orders.order_line.sales_order_id       uuid  ->  orders.sales_order.id             text
fnb.fnb_order_line.fnb_order_id        uuid  ->  fnb.fnb_order.id                  text
ledger.journal_line.journal_entry_id   uuid  ->  ledger.journal_entry.id           text
retail.sale_line.sale_id               uuid  ->  retail.sale.id                    text
access.scan_event.ticket_id            text  ->  catalogue.entitlement_template.id uuid
… 32 more
```

The pattern is systematic, not 37 oversights: **a parent whose `id` is a ULID (`text`) with a child
whose foreign key derived as `uuid`.** Every `*_line` table against its header shows it.

### 16 point at a column with no unique constraint

Postgres rejects these with *"no unique constraint matching given keys for referenced table"*:

```
resources.session_participant.session_id -> identity.session.principal_id
games.credit_ledger.card_id              -> games.card.card_code
ai.policy.tenant_id                      -> platform.tenant.home_region_id
marketing.guest_profile.guest_link_id    -> platform.guest_link.guest_link_id
```

`identity.session` is the clearest: it has no primary key, so the generator picked `principal_id` as
its addressable column — **one principal has many sessions**, so it is not a key and a participant
row pointing at it means nothing.

### 83 of 374 tables have no primary key

22% of the schema. `access.blacklist`, `control.subscription`, `fnb.recipe`, `identity.session`,
`orders.order_discount`, `ledger.journal_line`, `marketing.loyalty_position` and 76 others.

**`derive-ddl.py` already knows.** It reports *"14 declared reference(s) point at a table with no
addressable key"* and demotes each to an index with a comment (`910-indexes.sql:326`). That is the
right behaviour and it is honest. But it only notices the 14 that happen to be foreign-key targets;
the other 69 keyless tables pass in silence.

**`check-package` rule 30 is the check that should catch this and reads the wrong artefact.** It
tests `handoff/schema-reference.json` for a column that *could* serve as a key — `id`,
`<table>_id`, a declared parent, a natural-key suffix, or fewer than four columns. It never opens
the emitted DDL to see whether a `PRIMARY KEY` was actually written. Every one of the 83 satisfies
rule 30 and ships without a key.

### Smaller

- Comments truncate mid-word. `backend/010-access.sql:48` ends `"…which would have suspended it for every guest who held one. Han"`.
- `fk_waitlist_entry_subject_id` and three `fk_invitation_*` names each appear twice — on different tables (`catalogue.` / `fnb.`, `marketing.` / `orders.`), so Postgres accepts them. Legal, but the names are not schema-qualified and will collide in any migration tool that assumes global uniqueness.
- Two index names repeat across `marketing.invitation` and `orders.invitation`. Different schemas, so also legal. Worth naming deliberately rather than by luck.

---

## 5. The benchmark harness does not measure what it says it measures

`services/README.md` states plainly what it measures honestly and what it does not. The list is
good and one entry on it is wrong:

> **lease contention on a hot performance**, which is where a flash sale actually fails

`tools/bench.py:14` repeats it, and `deploy/c-flash-sale.yml` sends the reader there:
*"acquireInventoryHold serialises… Measure it with `tools/bench.py --pattern hot-venue`."*

**There is no write in the harness.** Across all 16 generated services, 2,433 SQL statements:

```
1,634  SELECT
  799  SELECT count(*)
    0  INSERT / UPDATE / DELETE
```

`derive-services.py:201` emits a declared write as `SELECT count(*) FROM <table>`. `app.py:77-81`
then wraps those in a transaction and raises `_Rollback` to undo it. **No row lock is ever taken,
so lease contention is not measured at all** — and the substitute distorts in both directions: a
full-table `count(*)` is a sequential scan, far heavier on I/O than the single-row `UPDATE … FOR
UPDATE` it stands in for, and free of the serialisation that is the whole point.

The rollback is also undisclosed. The README says a skeleton *"executes the declared reads and
writes and returns"*. It does not say the writes are discarded.

### And the three topologies are not comparable

> **The one rule.** Only placement changes between the three files… **Anything else differing
> invalidates the comparison.**

| | services | containers | scaled |
|---|---|---|---|
| `compose.hybrid.yml` | 28 | **39** | Catalogue 4, Order 4, Identity 3, Access 2, Tenancy 2, Marketing 2 |
| `compose.all-venue.yml` | 50 | **50** | none |
| `compose.all-tenant.yml` | 50 | **50** | none |

Images, CPU and memory limits are identical — that part holds. Replica counts are not, and they are
not placement. Hybrid runs 39 application containers against 50, with the difference concentrated in
the two services carrying the burst load. **Any latency or RPS number compared across these three
files confounds topology with size**, by the harness's own stated rule.

---

## 6. Counts do not agree with each other

Nine artefacts state a table count. There are five different numbers, and the true one is **374**:

| Source | Tables | Indexes |
|---|---|---|
| `backend/*.sql` (counted) | **374** | **254** |
| `derive-ddl.py` (run) | 374 | 254 |
| `check-package` (run) | 382 | — |
| `README.md`, `OVERVIEW.md`, `COVERAGE.md`, `MANIFEST.md:6` | 383 | — |
| `MANIFEST.md:58`, `backend/README.md` | 373 | 250 |
| `deploy/c-flash-sale.yml` | 373 | — |
| `services/README.md` | 369 | 194 |

Others:

- **Relationships** — `MANIFEST.md` 959, `COVERAGE.md` 499, `910-indexes.sql` header *"486 of 932"*.
- **Contracts** — 31 files on disk (30 once the orphan goes, 28 excluding `shared/`). `README.md:31` says *"25 files"*.
- **State models** — 127 files, `check-states` loads 126, docs claim 124. Two are new in this drop (`burst-environment`, `journey-entrant`) and the headline was not moved.
- **Flows** — 95 files, docs claim 94.
- **ADRs** — 37. Correct everywhere.
- **Burst scope** — `handoff/burst-scope.json` embeds a note saying *"six services see no part of a ticket sale"*, in a file whose own data says **13 of 16 are `deployed: false`**. `MANIFEST.md` says thirteen and is right. `deploy/c-flash-sale.yml` names six, one of which (Maintenance) is not among the 16 services at all.

`tools/sync-counts.py` exists to prevent exactly this and runs last in `refresh.sh`. Whatever it
covers, it does not cover these.

---

## 7. Trickle-down — what the pipeline does and does not catch

**Caught, correctly.** `check-package` reports six mirrors out of sync (663 files each) and two
diagrams older than their sources, with the fix named in the message. `refresh.sh` orders mirrors
last with a comment explaining why. `derive-ddl` reports demoted references. The staleness
machinery works.

**Not caught — five gaps, each proven by something in this drop:**

1. **An operationId declared in two contracts.** 16 of them, invisible to all ten checks.
2. **A foreign key that cannot execute.** 52 statements. Nothing type-checks the emitted DDL against itself; the schema reference is validated, its output is not.
3. **A table with no `PRIMARY KEY` in the DDL.** 83 tables. Rule 30 checks the JSON, not the SQL.
4. **A markdown link between ADRs.** Three are broken, two of them new:
   - `0034-ai-retrieval-and-cost.md` → `0020-ai-proposes-a-person-accepts.md` (file is `0020-ai-isolation-boundary.md`)
   - `0034-ai-retrieval-and-cost.md` → `0021-qdrant-collections-and-shards.md` (file is `0021-qdrant-partitioning.md`)
   - `0030-deep-link-cold-entry.md` → `0002-user-driven-authorisation.md` (pre-existing)

   `audit-links.py` covers nine directions of cross-layer integrity and prose links are not among them.
5. **A generated artefact contradicting its own generated data.** The burst-scope note against its own service list.

Two smaller notes on the check code itself:

- `check-screens.py:75` and `check-flows.py:66` `continue` past a contract that fails to parse. A YAML error there silently reduces the known-operation set; the resulting failures point at the screens rather than at the file that broke.
- `check-package` claims 41 rules. The numbered comments give **39 distinct numbers** — 1 and 20 are absent, and 19, 32 and 34 each appear twice on different rules.

---

## 8. What to do, in order

1. **Delete `contracts/spine/cross-cell.yaml`.** Clears two `check-package` errors and the ambiguity underneath 16 operations. Re-run `refresh.sh` afterwards.
2. **Retire `states/redemption-right.yaml`** and its diagram; **repoint `states/entitlement.yaml`** at `orders.EntitlementStatus`. Clears `check-states` and both `audit-links` breaks — all ten green.
3. **Fix the ULID/uuid column types in the schema reference**, then regenerate. 37 foreign keys.
4. **Give the 83 keyless tables a key**, or declare them keyless deliberately and have `derive-ddl` say so. The 16 non-unique targets fall out of the same pass.
5. **Emit real DML in the service skeletons** — or delete the contention claim from `services/README.md`, `tools/bench.py` and `deploy/c-flash-sale.yml`. Either is defensible; the current pair is not.
6. **Equalise replicas across the three compose files**, or state in the README that hybrid is measured at a different size and why.
7. **Reconcile the counts** and extend `sync-counts.py` to the seven artefacts above.
8. **Add four rules**: unique operationId across contracts · FK type and target-uniqueness against the emitted DDL · `PRIMARY KEY` present in the DDL · markdown link resolution in `docs/`. Each is a defect this drop actually contains.


---

# Resolution — 3 September, same day

**All ten checks pass.** `check-package` passes with four more rules than it had. The DDL parses
back clean: **374 tables, 0 without a `PRIMARY KEY`, 594 foreign keys, 0 that Postgres rejects.**

## What was done

| | Before | After |
|---|---|---|
| Checks failing | 3 of 10 | **0** |
| Tables with no `PRIMARY KEY` | 84 | **0** |
| Foreign keys Postgres rejects | 52 | **0** |
| Foreign key constraints emitted | 580 | **594** |
| Locking statements in the harness | 0 | **820** |
| Broken markdown links | 3 | **0** |
| Duplicated operationIds | 16 | **0** |

**1. Five superseded files deleted.** `contracts/spine/cross-cell.yaml` and its diagram;
`states/entitlement.yaml`, `states/redemption-right.yaml` and its diagram. Each was verified as an
exact subset of its survivor first.

**2. `derive-schema.py` gained three passes**, in order: a surrogate key for the 81 tables with no
addressable column, marked `synthesised` so they stay a worklist rather than reading as declared;
five mistargeted references repointed from `catalogue.entitlement_template` to `access.entitlement`;
and every declared reference column retyped to its target key. **The root cause was one line** —
`resolve_type` returned the literal `uuid` for any `$ref` to a persisted schema, whatever that
target was keyed by.

**3. `derive-ddl.py` emits a key where `key_of` finds one**, rather than only where a column is
named `id`. That function already sat in the same file, used for foreign keys and not for keys.

**4. The benchmark takes locks.** `derive-services.py` emits `SELECT <key> … FOR UPDATE`, scoped
where the table carries a `scope_path`, in place of `SELECT count(*)`. The rollback wrapper stays —
a lock inside a rolled-back transaction is still taken and still held.

**5. Replicas equalised** across the three compose files, with the removed figures recorded as a
comment pointing at `handoff/sizing.json`.

**6. Counts come from one place.** `build-status.py` defines `tables` as the Postgres count and
counts pseudo-stores separately; foreign keys and indexes are counted from the DDL rather than
remembered. `sync-counts.py` now covers six documents rather than two, and syncs markdown table
rows by label — `COVERAGE.md` was still reading 753 operations, 76 state models and 23 flows.

**7. Four rules added** to `check-package.py`: one contract per operationId (42), the emitted DDL
applies (43), every table has a key in the SQL (44), markdown links resolve (45). Rule 45 caught
its three on the first run. An unparseable contract is now a hard failure in `check-screens` and
`check-flows` rather than a silent skip.

## Corrections to this audit

**The flow count was wrong.** 95 files, of which `_schema.yaml` is a template — 94 flows is
correct and always was.

**84 tables had no key, not 83.** The first parse missed the four tables whose names are reserved
words and therefore quoted: `fnb."table"`, `identity."session"`, `marketing."case"`,
`retail."return"`.

**Step 2 was a delete, not a repoint.** `states/entitlement-status.yaml` already carried the note
*"Merged with `states/entitlement.yaml` on 18 August"*. The merge had happened and the old file was
never removed — the same defect as `cross-cell.yaml`, not a different one.

## Found while fixing, not in the original audit

**`build-schema-workbook.py` read three paths under `/home/claude`** on another machine. Every glob
matched nothing, silently, which is why the workbook reported 383 tables and **0 written as DDL**
long after `backend/` existed. Pointed at this repo, it now reports 374 and 374.
`build-services-workbook.py` has the same defect — `refresh.sh` wraps it in `2>/dev/null || true`,
which is how it went unnoticed.

**Two tools cannot run on this interpreter.** `derive-domain.py` and `render-domain.py` nested
same-type quotes inside an f-string, which is Python 3.12 syntax and a `SyntaxError` on the 3.9
here. Both are in `refresh.sh`. Fixed.

**Eleven tools crashed on their own closing line** — a unicode arrow against a cp1252 console,
raised after the file had been written. A traceback on a run that succeeded is the most misleading
shape an error can take. All now carry the guard the other tools already had.

**`sync-counts.py` corrupted a number the moment it met a thousands separator.** Pointing it at
`MANIFEST.md` turned `1,032 operations` into `1,1032` — its patterns matched the digit run after
the comma. The digit run now spans the separator.

## Still open

- **The DDL has never been executed.** Every claim above rests on parsing it, not on `psql -f`.
- **81 synthesised keys** are a reported warning and a real modelling debt: those tables were built
  from response shapes, and a surrogate key makes the SQL apply without making the model right.
- **The 19 pre-existing warnings** — tables written and never read, three missing descriptions.
- **`COVERAGE.md` rows that are not wired**: API schemas, permissions, requirements coverage and
  configuration levels are still hand-typed and cannot be checked.
