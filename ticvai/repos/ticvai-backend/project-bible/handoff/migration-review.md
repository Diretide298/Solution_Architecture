# Migration changes for a person

**Written by `tools/derive-ddl.py` in frozen mode (20261007). Do not edit; it is rewritten on every run.**

The baseline migrations under `backend/` are frozen at `r1 (9cec72d)` (`tools/check-migration-freeze.py`). `derive-ddl.py` writes additive changes (new tables, columns and indexes) as the next forward migration, `backend/<area>/V<nnnn>__*.sql`. **The changes below it does not write**, because each has a data question behind it: which rows survive a drop, what fills a new NOT NULL column, whether a rename is a rename. Write each as a forward migration by hand; once a forward migration carries it, it leaves this list.

**1 change(s).**

| Kind | Database | Object | Change | What a person does |
|---|---|---|---|---|
| not null | tenant | `orders.pos_shift.cashier_reason` | still nullable in the databases; the schema reference says NOT NULL | backfill, then ALTER COLUMN ... SET NOT NULL |
