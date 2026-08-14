# Contract viewer

A local browser for the TICVAI delivery package. The contracts link by `$ref`, screens link to
operations, flows link to screens, and every database table names the contract schema it came
from — so this reads the actual reference graph rather than matching text.

```bash
cd viewer
npm install      # once
npm start        # → http://localhost:4173
```

Flags: `--port 4173`, `--open` to launch a browser, `--dir contracts` to index somewhere else
(e.g. `--dir repos/ticvai-contracts/openapi` for the authoritative copy).

Nothing is written to disk and nothing leaves the machine — the server only reads files under
the project root.

## Three layers

The top-left switch picks which part of the system is on screen. **Contracts sit in the middle
deliberately: the API is the join between the other two**, and both outer layers are drawn by
resolving against it.

| | |
|---|---|
| **Frontend** | `screens/`, `flows/`, `frontend/` — Screen · Journey · Apps |
| **Contracts** | `contracts/` — Graph · Structure · ER · Reader |
| **Backend** | `backend/` — Data · Routing |

Each layer brings its own views, its own sidebar grouping and its own audit. Adding another —
services, when there are some — is one entry in the `LAYERS` array in `public/app.js` plus a
render function; nothing else hard-codes the list.

Keys `1` `2` `3` switch layer. A view shortcut for another layer follows you there.

## Frontend

**Screen** — the schematic a wireframe implements. Regions as blocks with their components
inside, each showing what it binds to and which permission hides it; the **four states** as their
own panel, with a required state that is not declared drawn as the finding it is; every operation
the screen calls, clickable into the contract; navigation in and out, clickable to the screen
either side; the platform's deployment block; and the app, route and component path that
implement it.

**Navigation says which kind it is.** 92 of the 102 navigation blocks carry `inferred: true` —
derived from module and flow order rather than drawn by anyone. Those render with dashed pills
under a heading that says so, because a sitemap that looks authoritative while being mostly
guessed is worse than no sitemap.

**Journey** — the flows in `flows/` drawn as what they are: one job a person came to do, traced
across screens. Steps run left to right; each carries its screen, the operations it calls and its
outcome. **The branches that can derail a step hang underneath it**, coloured by severity
(`recoverable` → `dataLoss`), with exit states at the end.

A track is wider than any window, so **drag anywhere to pan it** — the title and chips stay
pinned while the steps move. Movement under a few pixels is still a click, so cards and
operations open as before. The other sheets pan the same way.

**Apps** — the manifests in `frontend/`: which platforms each app serves, which contracts it
consumes, and its screens split by wave. Scaffolded apps are green-topped, the rest amber.

Nothing is inferred — every step, branch, screen link and route is declared, and the loader
reports any that points at something which does not exist.

## Backend

Two sources, read together: the **schema reference** `.xlsx` and the **versioned SQL** in
`backend/`.

The workbook is read directly rather than converted, so the spreadsheet stays the one source of
truth with no generated copy to drift from it. `lib/xlsx.mjs` is a zip and sheet reader in about
200 lines, no dependency. It is delivered to more than one folder and the copies drift, so **every
copy is found and the newest wins** — and a stale one is reported rather than silently preferred.

`lib/migrations.mjs` parses the DDL: `CREATE TABLE`, `REFERENCES`, `ALTER TABLE`, partitioning,
row-level security, generated columns and enum types. It reads the subset of SQL these files use
and ignores the rest rather than pretending to be a SQL parser. Its table counts agree with
`tools/check-migrations.py`.

**Data** — the ER diagram, at two zoom levels.

*Whole database* is one box per schema, each listing which other schemas its keys reach into and
how many columns do the reaching. 21 boxes rather than 211: every table at once is a hairball with
no room for labels. Click a schema to drill into it.

*One schema* is its tables as entity boxes, every column with its type and `•` marking required.
**Green means a migration creates it and it is really there; blue means it is derived from the
contracts and still only planned** — 27 of 211 are green. Amber is a table pulled in from another
schema because something here points at it.

**Relationships come in three kinds, strongest first.**

- **A `REFERENCES` clause** in the DDL — the database saying what is true. 34 of these, 9 of them
  composite `(id, level)` keys from V0003a. Drawn solid.
- **Declared in a contract** — a column whose source property is a `$ref`. Drawn solid.
- **Inferred from a column name** — `_id` resolved by trying successively shorter suffixes, so
  `added_by_principal_id` finds `identity.principal`. A table in the column's own schema wins over
  one elsewhere, and a name owned by two schemas is refused rather than guessed at. Drawn dashed,
  counted separately, switchable off, and dropped entirely for any table the DDL covers.

**The DDL teaches the inference.** `venue_id` appears on 49 tables and there is no `venue` table —
a venue is a *level* of `platform.scope_node`, which only the migrations know. Where a migration
resolves a column name, that answer is reused for the same name elsewhere and labelled `per DDL`.

**Routing** — ADR-0016 made visible: every contract's operations split across primary-write,
primary-read, replica and analytical.

Selecting a table shows what the migration says about it — primary key, partitioning, whether row
security is merely enabled or `FORCED` — its real foreign keys with their `ON DELETE`, and any
`_id` column still pointing at no table at all.

## Tracing across the layers

The right-hand pane answers "what links to this" about whatever is selected:

- an **operation** → which screens call it, which flows traverse it, what `$ref`s it
- a **schema** → what references it, and **which table it is persisted as** — or, for 162 of
  them, why it deliberately has none
- a **screen** → which flows step through it, which screens reach it
- a **table** → what the DDL says about it, its real foreign keys, the contract schema it derives
  from, its inferred keys, and any `_id` column pointing at no table at all

Every one of those is a click, so a database column can be followed back to the screen that
displays it and forward to the migration that creates it.

## Contracts

**Left pane grouping** — the sidebar lists the contracts three ways, toggled at the top:

- **Contracts** — by `x-ticvai-tier` (spine / satellite / shared)
- **Modules** — by `x-ticvai-module`, in declared numbered order
- **Platforms** — by `x-ticvai-platforms`

The last two read the taxonomy the `info` blocks declare, so nothing is inferred. Platforms are
declared **per contract**, so a contract appears under every platform it names — contract-level
reach, not per-endpoint ownership. `All platforms` fans out across every coded platform.

**Structure** — a block diagram of what is actually *inside* a file, in two layouts:

- **Tree** (default) — left to right: each depth is a column, siblings stack down it. Every mapping
  and sequence is a block with a ▾/▸ chevron; scalar leaves are listed as **rows inside their
  parent block**, so an operation is one card showing `operationId`, `summary` and its four
  `x-ticvai-*` fields rather than eleven separate boxes. Turn **Fields** off for the bare skeleton.
- **Nested** — containment instead: each mapping wraps its children.

**$ref links** curve from a `$ref` to the block it points at when the target is in the same file;
selecting a block highlights every link in its subtree. Dashed means the exact target is folded
away and the link lands on the nearest visible container. Click folds one level, double-click folds
the whole branch. A fully expanded contract is enormous, so the default zoom is floored to keep
blocks readable; **Fit** overrides that.

**ER** — the schemas of one contract as entity boxes: every field with its type, `•` marking
required, `$ref` fields in the entity colour. Purple boxes are enums, amber are entities pulled in
from another contract. Click a field to open what it points at; drag a box to pin it.

This is for **API entities**. Screens have regions and components rather than entities, so they
are not here; the database's own tables are the Backend layer's Data view.

**Graph** — four scopes. *Files* is the contracts with edge weight by reference count; *Schemas* is
every component and the `$ref`s between them; *Permissions* maps contracts to the permission
vocabulary; *Local* is the two-hop neighbourhood of the selection.

**Reader** — the YAML for the selected node, syntax highlighted. Every `$ref` is a clickable link
that resolves across files, and every `PERMISSION_STRING` jumps to its definition. Unresolved refs
are underlined in red.

**Backlinks** (right pane) — *Referenced by* is the answer to "what breaks if I change this",
computed from resolved `$ref`s rather than search.

## Audit

Each layer audits its own material, and the badge counts that layer's errors.

**Contracts** — duplicate path keys, `$ref`s that do not resolve, operations missing any of the
four required `x-ticvai-*` extensions, permissions used but absent from the enum, permissions
declared but unused, components nothing references, taxonomy gaps, platform-code collisions.

**Frontend** — screens calling an operation no contract declares; component kinds and region refs
outside `_components.yaml`; the four-states rule, with `offline` required only where the platform
is offline-capable; navigation pointing at a screen that does not exist; flow steps calling an
operation their own screen never declares; route collisions within an app; an offline-capable app
with no offline package.

**Backend** — a table the workbook marks written with no migration behind it, a foreign key
pointing at a table no migration creates, a table created twice, columns the DDL has that the
workbook does not list, a table deriving from a schema no contract declares, and any `_id` column
name used five or more times with no table behind it.

A second copy of the workbook that is older than the one being read is reported too. `backend/`
held a build behind `handoff/` for a while, and whichever folder you happened to open decided
which numbers you believed.

## Live

The server watches `contracts/`, `flows/`, `screens/`, `frontend/` and `backend/` and re-indexes on
save — including the `.xlsx`, so editing the schema reference in Excel updates the Data view. The
open page updates itself; no refresh, no restart.

Keys: `Ctrl`/`Cmd`+`K` search · `1` `2` `3` layer · `m` cycle the sidebar grouping · `w` screen ·
`j` journey · `p` apps · `g` graph · `s` structure · `e` ER · `r` reader · `d` data · `o` routing ·
`a` audit · `l` local graph of selection.

## Layout

| | |
|---|---|
| `lib/indexer.mjs` | parses the contracts into nodes and `$ref` edges, and produces the audit |
| `lib/structure.mjs` | turns one document into a positioned structural tree |
| `lib/consumers.mjs` | reads declared consumers from `api-list.md` and the app roster |
| `lib/journeys.mjs` | joins `flows/` → `screens/` → the contracts, and reads `frontend/` |
| `lib/xlsx.mjs` | minimal zip + sheet reader, so the workbook needs no dependency |
| `lib/backend.mjs` | the schema reference and ADRs, joined back to contract schemas |
| `lib/migrations.mjs` | the versioned SQL — tables, keys, partitioning, row security |
| `server.mjs` | static server, `/api/index`, `/api/journeys`, `/api/backend`, `/api/file`, `/api/tree`, SSE |
| `public/graph.js` | force-directed canvas renderer |
| `public/structure.js` | tree and nested block renderers |
| `public/boxdiagram.js` | box-and-row force layout, used by ER and Data |
| `public/app.js` | layers, views, routing, search, reader |

Node ids are stable and live in the URL hash, so any operation or schema can be linked directly:
`#op:contracts/spine/orders.yaml%23listOrders`.

## Not represented yet

- **Screen-to-screen sitemap** — `entryFrom`/`exitTo` are shown per screen and are clickable, but
  there is no whole-platform navigation graph. Worth building only once more of the 92 inferred
  navigation blocks are confirmed.
- **The 203 inventoried screens** on P02, P03, P04, P07, P08 and P13 have UI/UX boards rather than
  screen files, so they cannot appear until those are converted. 232 inventoried, 102 defined.
- **`docs/`** — the ADRs and registers are on disk but only ADR-0016 is surfaced, on Routing.
- **Row-security policies** — the viewer says a table is `FORCED`, not what the 13 policies say.

## Three things the audit found

**`/reservations` is defined twice** in `contracts/spine/orders.yaml`. YAML keeps only the last
block, so `createReservation` — `POST /reservations` — is silently discarded: the spec has no way to
create a reservation. Merging the two blocks under one `/reservations:` key fixes it.

**Platform code `P09` is used with two different names** — `"P09 Platform Admin Console"` and
`"P09 Platform Admin"`. One code meaning two things is the same failure mode `permissions.yaml`
warns about for permission strings, and it splits that platform into two sidebar entries.

**`whitelabel.homepage_section_section` is a child of `whitelabel.homepage_section`**, which is
not in the table list. The doubled suffix reads like whatever generates the workbook appended
`_section` to a table already named for the section, so the parent it points at was never
emitted. It is the only broken parent link in 197 tables.
