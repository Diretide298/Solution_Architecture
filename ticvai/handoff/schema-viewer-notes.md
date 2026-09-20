# Reading the schema graph

**Why clicking a catalogue table takes you to `platform`.**

Re-measured 20 September against 623 tables and 1,349 edges. Every number below comes from
`handoff/relationships.csv` and `handoff/schema-reference.json`; run `tools/derive-relationships.py`
to reproduce them.

## The cause is the data, not the viewer

`identity.principal` is the target of **143 edges**. `platform.scope` of **94**. `pii.subject`
of **68**. (Previously 108, 72 and 55 at 564 tables, and 69, 64 and 25 at 378. **The order of
the three has never changed and neither has the shape of the problem.**)

**`platform.org_unit` is now `platform.scope`** — the earlier drafts of this file name a table
that no longer exists.

Every table that belongs to a venue carries a scope column. Every table that records who did
something carries a `*_by_principal_id`. Those are correct, and they mean **three tables are
connected to almost everything**. On a force-directed graph they become gravity wells: the
layout collapses toward them, and following an edge out of a catalogue table is more likely to
land in `platform` or `identity` than anywhere else.

**352 of 1,349 edges point at one of four hub tables** — `identity.principal`, `platform.scope`,
`pii.subject` and `orders.sales_order`. **The fourth hub has changed**: `maintenance.asset` was
the fourth at 564 tables and is not now, because the F&B and retail order operations written in
September pointed 47 edges at `sales_order`. Hiding the four removes the reason every schema
appears connected to every other.

The share has fallen from 40% to 32% to **26%** as the schema grew. That is not the problem
receding — it is the rest of the graph filling in around a constant core. A quarter of all edges
still terminate in four places.

## The fix: three kinds of edge

`handoff/relationships.csv` carries an `edge_kind` column.

| Kind | Count | What it means | Show by default |
|---|---|---|---|
| **`ambient`** | 227 | Points at a hub — scope tree, principal, subject, tenant. True of nearly every table and therefore says nothing about *this* one | **No** |
| **`child`** | 84 | This row belongs to that row. `order_line` to `sales_order` | **Yes, prominently** |
| **`reference`** | 1,038 | A real relationship between two things. `scan_event` to `access_point` | **Yes** |

**These now account for every edge.** The earlier version of this table summed to 406 of 953 —
more than half the graph was unclassified while the table read as though it described all of it.
1,038 + 227 + 84 = 1,349.

Hide ambient by default with a toggle to show it. The graph then answers the question you
actually have — *what does this table relate to* — rather than *what does every table relate to*.

## Two smaller things

**Inferred versus declared, and the progress bar that was measuring the wrong thing.**

| | | |
|---|---|---|
| `declared` | 662 | The contract asserts it — a column carrying `referenceHow: declared` |
| `convention` | 460 | Inferred from a naming habit: a `*_id` stem that names a real table |
| `lineage` | 227 | Derived from what operations touch together; always drawn `ambient` |

Earlier drafts said *"most edges are inferred from column names because most tables have no DDL
yet"* and called the inferred count a progress bar that would fall as migrations were written.
**Both halves are wrong.** Declared now outnumbers inferred, 662 to 460 — and more to the point,
**`declared` never meant DDL.** It means the contract asserted the reference. Migrations do not
feed this number and writing them would not move it; what moves it is a contract naming its
target explicitly instead of leaving a reader to infer one from a column name.

**Reading `referenceHow` rather than `references` is load-bearing.** `derive-schema` annotates a
column *from* this graph and `derive-relationships` reads it back, so taking `references` alone
promotes last run's inference to this run's assertion. On 18 August that inflated declared edges
from 518 to 705 in a single pass and would have kept climbing. **A number that grows because it
was measured is the worst kind of drift: it looks like progress.**

**Tables with no columns.** Four, all in the storage set rather than the column reference:
`access.scan_event_unassigned` and `orders.sales_order_unassigned` are **default partitions** —
they have no columns of their own and catch rows whose scope matches no configured partition, so
a misconfiguration is loud rather than silently lossy. `platform.schema_version` is the migration
runner's bookkeeping. All three are in `handoff/schema-storage-only.md` and should be drawn
differently or filtered out of the entity view.

**The fourth, `fnb.guest_note`, is a phantom and should be removed.** It has no columns, no
contract schema, no operation, no inbound edge and no entry in the storage-only document, and it
appears in no contract, migration or workbook — only in derived handoff artefacts that have
copied it forward. It is also invisible to `audit-unwired-tables`, which classifies tables from
the column reference and never sees a table that exists only in storage.

**66 of 623 tables carry no edge at all.** `derive-relationships` reports 70 of 627 because its
table set includes the four column-less storage tables above.

## What a good default view looks like

    one schema at a time
      + child edges, drawn strongly
      + reference edges within the schema
      + reference edges leaving the schema, drawn faintly with a target label
      - ambient edges, behind a toggle
      - default partitions, filtered

That gives `catalogue` as its own tables and their real relationships, rather than a handful of
tables and a rope to `platform`.
