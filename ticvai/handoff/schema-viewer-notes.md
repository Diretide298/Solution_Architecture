# Reading the schema graph

**Why clicking a catalogue table takes you to `platform`.**

Re-measured on 3 November 2026 against 1,173 tables with columns and 3,329 edges. Every number
below comes from `handoff/relationships.csv` and `handoff/schema-reference.json`; run
`tools/derive-relationships.py` to reproduce them. **The numbers are a dated measurement**; what
`tools/check-authored-inputs.py` holds current is the shape this page explains: which three tables
are the hubs and in what order, which edge kinds and `how` values exist, that `ambient` means a
lineage coupling, and which tables have no columns.

## The cause is the data, not the viewer

`identity.principal` is the target of **397 edges**. `platform.scope` of **214**. `pii.subject`
of **122**. (144, 94 and 69 at 625 tables on 21 September; 108, 72 and 55 at 564; 69, 64 and 25 at
378. **The order of the three has never changed and neither has the shape of the problem.**)

**The scope tree is `platform.scope`.** Earlier drafts of this file named it platform.org_unit,
a table that no longer exists.

Every table that belongs to a venue carries a scope column. Every table that records who did
something carries a `*_by_principal_id`. Those are correct, and they mean **three tables are
connected to almost everything**. On a force-directed graph they become gravity wells: the layout
collapses toward them, and following an edge out of a catalogue table is more likely to land in
`platform` or `identity` than anywhere else.

**733 of the 3,329 edges (22%) point at one of the three, measured on 3 November 2026; 727 of the
2,371 foreign-key edges (31%).** The share pointing at the hubs fell from 40% to 32% to 26% by
21 September (then counted over four hubs, the fourth being `orders.sales_order`) as the schema
grew. That is not the problem receding — it is the rest of the graph filling in around a constant
core.

**There is no longer a fourth hub worth the name.** On 21 September it was `orders.sales_order`;
now the fourth most-referenced table is `platform.outbox`, and 83 of its 84 edges are lineage
couplings (every operation that publishes an event writes it), not foreign keys. Among foreign
keys the fourth is `catalogue.product` with 58, a real relationship rather than an ambient one.

## The three kinds of edge, and what they no longer do

`handoff/relationships.csv` carries an `edge_kind` column.

| Kind | Count | What it means | Show by default |
|---|---|---|---|
| **`ambient`** | 958 | A lineage coupling: two tables one operation touches together, with no column saying so. Real, and not a foreign key | **No** |
| **`child`** | 234 | This row belongs to that row, read from the name: `orders.order_line` names `orders.sales_order` | **Yes, prominently** |
| **`reference`** | 2,137 | A foreign key between two things. `access.scan_event` to `access.access_point` | **Yes** |

**2,137 + 958 + 234 = 3,329: every edge has a kind.**

**`ambient` changed meaning, and this page said otherwise until 3 November.** Earlier drafts
defined it as *points at a hub* and proposed hiding it to remove the gravity wells. Since
`derive-relationships.py` took over the file (the hand-kept CSV had 515 rows against the graph's
846), **`ambient` is exactly the `lineage` edges**, and the foreign keys into the three hubs are
`reference` edges: 720 of the 727, the other 7 `child`. Hiding ambient therefore hides the lineage
couplings and **leaves every hub edge drawn**. Removing the gravity wells needs a filter on the
three target tables themselves, which is the viewer's call to add.

## Two smaller things

**Inferred versus declared, and the progress bar that was measuring the wrong thing.** The `how`
column says what each edge was read from.

| How | Count | |
|---|---|---|
| `declared` | 1,339 | The contract asserts it — a column carrying `referenceHow: declared` |
| `convention` | 966 | Inferred from a naming habit: a `*_id` stem that names a real table |
| `precedent` | 66 | Inferred from the same column name declared elsewhere: at least two other schemas declare it, all to one target |
| `lineage` | 958 | Derived from what operations touch together; always drawn `ambient` |

**`precedent` is new since this page was last written** and was missing from its table. It is
weaker than declared, like convention, and the viewer counts it as inferred (it is not in
`lib/relationships.mjs`'s declared set). Declared still outnumbers convention, 1,339 to 966 on
3 November 2026 — and **`declared` never meant DDL.** It means the contract asserted the
reference. Migrations do not feed this number; what moves it is a contract naming its target
explicitly instead of leaving a reader to infer one from a column name.

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
contract schema, no operation and no migration; the guest note the floor reads is
`marketing.guest_note`, which has all four. It survives only as a storage entry that derived
handoff artefacts copy forward, and it is invisible to `audit-unwired-tables`, which classifies
tables from the column reference and never sees a table that exists only in storage.

**101 of the 1,173 tables with columns carried no edge at all on 3 November 2026.**
`derive-relationships` reports 104 of 1,177 because its table set includes the four column-less
storage tables above.

## What a good default view looks like

    one schema at a time
      + child edges, drawn strongly
      + reference edges within the schema
      + reference edges leaving the schema, drawn faintly with a target label
      - edges into identity.principal, platform.scope and pii.subject, behind a toggle
      - ambient (lineage) edges, behind a toggle
      - default partitions, filtered

That gives `catalogue` as its own tables and their real relationships, rather than a handful of
tables and a rope to `platform`.
