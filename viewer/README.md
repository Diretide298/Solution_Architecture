# Contract viewer

A local browser for the TICVAI delivery package. The contracts link by `$ref`, screens link to
operations, and flows link to screens — so this reads the actual reference graph rather than
matching text.

```bash
cd viewer
npm install      # once
npm start        # → http://localhost:4173
```

Flags: `--port 4173`, `--open` to launch a browser, `--dir contracts` to index somewhere else
(e.g. `--dir repos/ticvai-contracts/openapi` for the authoritative copy).

Nothing is written to disk and nothing leaves the machine — the server only reads `.yaml` files
under the project root.

## What it does

**Left pane grouping** — the sidebar lists the contracts three ways, toggled at the top:

- **Contracts** — by `x-ticvai-tier` (spine / satellite / shared)
- **Modules** — by `x-ticvai-module`, in declared numbered order
- **Platforms** — by `x-ticvai-platforms`

The last two read the taxonomy the `info` blocks declare, so nothing is inferred. Platforms are
declared **per contract**, so a contract appears under every platform it names — contract-level
reach, not per-endpoint ownership. `All platforms` fans out across every coded platform.

**Journey** — the flows in `flows/` drawn as what they are: one job a person came to do, traced
across screens. Steps run left to right; each carries its screen, the operations it calls and its
outcome. **The branches that can derail a step hang underneath it**, coloured by severity
(`recoverable` → `dataLoss`), with exit states at the end. Click an operation to jump into the
contract that declares it.

Nothing is inferred — every step, branch and screen link is declared in `flows/` and `screens/`,
and the loader reports any that point at something which does not exist.

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

This is for **data entities** — schemas with fields and relationships. Screens have regions and
components rather than entities, so they are not represented here.

**Graph** — four scopes. *Files* is the contracts with edge weight by reference count; *Schemas* is
every component and the `$ref`s between them; *Permissions* maps contracts to the permission
vocabulary; *Local* is the two-hop neighbourhood of the selection.

**Reader** — the YAML for the selected node, syntax highlighted. Every `$ref` is a clickable link
that resolves across files, and every `PERMISSION_STRING` jumps to its definition. Unresolved refs
are underlined in red.

**Backlinks** (right pane) — *Referenced by* is the answer to "what breaks if I change this",
computed from resolved `$ref`s rather than search.

**Audit** — duplicate path keys, `$ref`s that do not resolve, operations missing any of the four
required `x-ticvai-*` extensions, permissions used but absent from the enum, permissions declared
but unused, components nothing references, taxonomy gaps and platform-code collisions.

**Live** — the server watches `contracts/`, `flows/` and `screens/` and re-indexes on save. The open
page updates itself; no refresh, no restart.

Keys: `Ctrl`/`Cmd`+`K` search · `m` cycle the sidebar grouping · `g` graph · `s` structure ·
`e` ER · `j` journey · `r` reader · `a` audit · `l` local graph of selection.

## Layout

| | |
|---|---|
| `lib/indexer.mjs` | parses the contracts into nodes and `$ref` edges, and produces the audit |
| `lib/structure.mjs` | turns one document into a positioned structural tree |
| `lib/consumers.mjs` | reads declared consumers from `api-list.md` and the app roster |
| `lib/journeys.mjs` | joins `flows/` to `screens/` to the contracts |
| `server.mjs` | static server, `/api/index`, `/api/journeys`, `/api/file`, `/api/tree`, SSE |
| `public/graph.js` | force-directed canvas renderer |
| `public/structure.js` | tree and nested block renderers |
| `public/boxdiagram.js` | box-and-row force layout, used by ER |
| `public/app.js` | views, routing, search, reader, journey |

Node ids are stable and live in the URL hash, so any operation or schema can be linked directly:
`#op:contracts/spine/orders.yaml%23listOrders`.

## Not represented yet

- **`frontend/`** — the per-app manifests are derived from `screens/`; the viewer does not surface
  app-level coverage (contracts consumed, screens by wave, scaffold status) yet.
- **`screens/`** — screens are read and linked, but there is no screen view showing regions,
  components and the four states as a layout schematic.
- **`backend/`** — an ADR and an `.xlsx`. The spreadsheet would need converting to YAML or CSV
  before anything could read it.

## Two things the audit found

**`/reservations` is defined twice** in `contracts/spine/orders.yaml`. YAML keeps only the last
block, so `createReservation` — `POST /reservations` — is silently discarded: the spec has no way to
create a reservation. Merging the two blocks under one `/reservations:` key fixes it.

**Platform code `P09` is used with two different names** — `"P09 Platform Admin Console"` and
`"P09 Platform Admin"`. One code meaning two things is the same failure mode `permissions.yaml`
warns about for permission strings, and it splits that platform into two sidebar entries.
