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
either side; and the app, route and component path that implement it.

**Journey** — the flows in `flows/` drawn as what they are: one job a person came to do, traced
across screens. Steps run left to right; each carries its screen, the operations it calls and its
outcome. **The branches that can derail a step hang underneath it**, coloured by severity
(`recoverable` → `dataLoss`), with exit states at the end.

**Apps** — the manifests in `frontend/`: which platforms each app serves, which contracts it
consumes, and its screens split by wave. Scaffolded apps are green-topped, the rest amber.

Nothing is inferred — every step, branch, screen link and route is declared, and the loader
reports any that points at something which does not exist.

## Backend

The schema reference in `backend/` is an `.xlsx`, so it is **read directly rather than
converted**: the spreadsheet stays the one source of truth and there is no generated copy to
drift from it. The zip and sheet reader is `lib/xlsx.mjs` — about 200 lines, no dependency.

**Data** — the tables of one schema module as entity boxes, every column with its type and `•`
marking required. Green is a table in the module, blue a child table, amber one pulled in from
another module because something here points at it.

Relationships are only what is **declared**: the workbook's `Child of`, and columns whose source
property is a `$ref` in the contracts. A column called `tenant_id` is not treated as a foreign
key, because nothing declares it as one — so the diagram is thin where the truth is thin.

**Routing** — ADR-0016 made visible: every contract's operations split across primary-write,
primary-read, replica and analytical.

## Tracing across the layers

The right-hand pane answers "what links to this" about whatever is selected:

- an **operation** → which screens call it, which flows traverse it, what `$ref`s it
- a **schema** → what references it, and **which table it is persisted as**
- a **screen** → which flows step through it, which screens reach it
- a **table** → the contract schema it derives from, its children, and its declared keys

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

**Backend** — a table whose parent is not in the table list, a table deriving from a schema no
contract declares, a table with no columns.

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
| `server.mjs` | static server, `/api/index`, `/api/journeys`, `/api/backend`, `/api/file`, `/api/tree`, SSE |
| `public/graph.js` | force-directed canvas renderer |
| `public/structure.js` | tree and nested block renderers |
| `public/boxdiagram.js` | box-and-row force layout, used by ER and Data |
| `public/app.js` | layers, views, routing, search, reader |

Node ids are stable and live in the URL hash, so any operation or schema can be linked directly:
`#op:contracts/spine/orders.yaml%23listOrders`.

## Not represented yet

- **Screen-to-screen sitemap** — `entryFrom`/`exitTo` are shown per screen and are clickable, but
  there is no whole-platform navigation graph.
- **The 203 screens** on P02, P04, P06, P07, P08 and P13 have UI/UX boards rather than screen
  files, so they cannot appear until those are converted.

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
