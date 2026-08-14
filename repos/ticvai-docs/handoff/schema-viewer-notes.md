# Reading the schema graph

**Why clicking a catalogue table takes you to `platform`.**

## The cause is the data, not the viewer

`platform.scope_node` is referenced by **64 tables**. `identity.principal` by **69**.
`pii.subject` by 25.

Every table that belongs to a venue carries `venue_id`. Every table that records who did
something carries a `*_by_principal_id`. Those are correct, and they mean **three tables are
connected to almost everything**. On a force-directed graph they become gravity wells: the
layout collapses toward them, and following any edge from a catalogue table has a 40% chance of
landing in `platform` or `identity`.

**163 of 406 edges point at one of four hub tables.** Hiding them removes the reason every
schema appears connected to every other.

## The fix: three kinds of edge

`handoff/relationships.csv` now carries an `edge_kind` column.

| Kind | Count | What it means | Show by default |
|---|---|---|---|
| **`ambient`** | 163 | Points at a hub — scope tree, principal, subject, tenant. True of nearly every table and therefore says nothing about *this* one | **No** |
| **`child`** | 55 | This row belongs to that row. `order_line` to `sales_order` | **Yes, prominently** |
| **`reference`** | 188 | A real relationship between two things. `scan_event` to `access_point` | **Yes** |

Hide ambient by default with a toggle to show it. The graph then answers the question you
actually have — *what does this table relate to* — rather than *what does every table relate
to*.

## Two smaller things

**Inferred versus declared.** The viewer already distinguishes these, and the ratio is worth
reading rather than ignoring: most edges are inferred from column names because **most tables
have no DDL yet**. As migrations are written, inferred edges become declared ones. The count of
inferred edges is a progress bar for the schema, not a defect list.

**Zero-column tables.** `scan_event_unassigned` shows no columns because it is a **default
partition** — it has no columns of its own and inherits from the parent. Same for
`sales_order_unassigned`. They are correct; they should be drawn differently, or filtered out
of the entity view entirely.

## What a good default view looks like

    one schema at a time
      + child edges, drawn strongly
      + reference edges within the schema
      + reference edges leaving the schema, drawn faintly with a target label
      - ambient edges, behind a toggle
      - default partitions, filtered

That gives `catalogue` as thirteen tables and their real relationships, rather than thirteen
tables and a rope to `platform`.
