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

For anyone who has not used it before, `manual/TICVAI-Viewer-Manual.pdf` is a 55-page illustrated
manual covering every layer, view and control. Its figures are captured from the running app rather
than drawn, so they cannot drift — see `manual/README.md` to regenerate it.

**Hover anything you do not recognise.** Component kinds, schema names, tier badges, edge kinds,
failure policies, every view tab and every toggle explain themselves on hover — from the delivery's
own descriptions where there is one (`screens/_components.yaml`, the workbook's "why it is
separate", an event consumer's purpose) and from a built-in glossary otherwise.

## Four layers

The top-left switch picks which part of the system is on screen. **Contracts sit near the middle
deliberately: the API is the join between the outer two**, and every other layer is drawn by
resolving against it.

| | |
|---|---|
| **Frontend** | `screens/`, `flows/`, `frontend/`, `wireframes/`, `designs/` — Screen · Journey · Apps |
| **Contracts** | `contracts/` — Spine · Graph · Structure · ER · Reader |
| **Domain** | `states/`, `events/` — States · Events |
| **Backend** | `backend/` SQL + `handoff/` reference — Data · Migrations · Routing |

Each layer brings its own views, its own sidebar grouping and its own audit. Adding another is one
entry in the `LAYERS` array in `public/app.js` plus a render function; nothing else hard-codes the
list — the Domain layer was added that way.

Keys `1` `2` `3` switch layer. A view shortcut for another layer follows you there.

## Wireframes

`wireframes/` holds a rendered wireframe for **every screen, every flow and every platform** —
framed live on the Screen, Journey and Apps views rather than screenshotted, so they scroll and
respond as they do standalone.

Nothing here is inferred. A wireframe is named for exactly the thing it draws — `screens/pos-002.html`
is screen POS-002, `flow-f01.html` is flow F01, `p04.html` is platform P04 — so there is no matching
to get wrong, and the two sides line up exactly: **180 screens, 180 wireframes, none missing and
none left over.** Either side drifting is reported.

They are *structure*, and they say so at the top: generated from the same `screens/` YAML the Screen
view reads, showing what is on a screen and where, not what it will look like. The design boards in
`designs/` are the other thing — a designer's artboard covering a whole platform, attached to a
screen by a `wireframe.owner` declaration or, failing that, by reading the file name and saying so.

## Domain

The two artefacts that check each other. The contracts declare **38 status enums**, and not one of
them says which moves between those states are allowed — so nothing catches an order going from
`held` to `refunded` without ever having been paid. The enum permits it; the business does not; no
artefact said so. `states/` is where that is said, and `events/` says what crosses the outbox when
a transition happens.

**States** — one machine per entity, laid out left to right by longest path from an initial state.
Direction is the whole point here, so every transition carries an arrowhead:

- **initial** states get an entry stub, **terminal** states a second rule down the right edge
- a transition caused by an operation is solid blue; one caused by a **timer or a job is dashed**,
  because nothing in any contract causes it
- a **reversal** is amber and bows below the row — that is money or entitlement moving backwards,
  and it is worth being able to see at a glance. `✓` on a label means it needs approval
- reversals are excluded from the depth calculation, so a refund reaching back from `completed`
  does not drag the tail of the machine leftwards
- **offline** under a state name means a terminal can reach it with no network. On a POS that is
  the difference between a sale that completes and one that cannot
- hover a transition for its **guard** — the condition that must hold, stated here rather than
  living only in whoever wrote the handler

Select a state and the right pane lists every way it is left and reached, with the operation, the
guard, and what the transition publishes. The operation name opens it in the contracts; the event
chip opens it in the catalogue.

**Events** — the catalogue as a ledger of who tells whom. Each event shows its publisher, the
transition that emits it, and every consumer, with **critical** ones marked: a dead-lettered
`order.paid` means a guest paid and holds nothing, so it pages rather than logs. Open one for its
payload, its consumers with their idempotency keys, and a link back to the transition in the state
machine.

The sidebar's third group is the one to act on: **the status enums with no model**. Nineteen of the
thirty-eight have states and no statement of which moves between them are legal.

Everything is cross-checked, and this is where `tools/check-states.py` and the viewer disagree —
see the audit note below.

## Frontend

**Screen** — the schematic a wireframe implements. Regions as blocks with their components
inside, each showing what it binds to and which permission hides it; the **four states** as their
own panel, with a required state that is not declared drawn as the finding it is; every operation
the screen calls, clickable into the contract; navigation in and out, clickable to the screen
either side; the platform's deployment block; and the app, route and component path that
implement it.

**Navigation says which kind it is.** 160 of the 179 navigation blocks carry `inferred: true` —
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

**Design boards** — the exported UI/UX HTML in `designs/`, framed live rather than screenshotted,
so scrolling and hovering them works. `frontend/README.md` says the boards are what the frontend
plan was built from, and that the two apps missed were missed because they had no board — so they
belong beside the screens rather than in a folder nobody opens.

A board appears in three places: on any **screen** drawn from it, on any **journey** whose platform
has one, and on **Apps**, which lists them all. It also opens as a page of its own from the sidebar
— which is how a platform with a board but no screen files stays reachable.

**How a board finds its platform is shown, because there are two ways.** P04's nine screens name
theirs in `wireframe.owner` — `design — Park_POS_dc.html` — so that one is **declared**. Nothing
names `Park_POS_v1_dc.html`, so its platform is **inferred** from the file name (the app slug `pos`
→ P04) and drawn with a dashed chip and a note saying so. A name that could mean two platforms is
refused rather than guessed at. An earlier revision is not shown beside the board it is a revision
of; it is reachable from that board's page.

Nothing else here is inferred — every step, branch, screen link and route is declared, and the
loader reports any that points at something which does not exist.

## Backend

Two sources with different standing, and the layer keeps them apart:

- **`backend/` is the database as it stands** — six versioned `.sql` migrations. 39 tables.
- **`handoff/TICVAI_Schema_Reference.xlsx` is the database as it is meant to become** — 224
  tables derived from the API contracts. 185 of them are not written yet.

Green means the SQL exists; amber or blue means it is still only planned. The sidebar's
**Status** grouping splits the two outright.

The workbook is read directly rather than converted, so the spreadsheet stays the one source of
truth with no generated copy to drift from it. `lib/xlsx.mjs` is a zip and sheet reader in about
200 lines, no dependency. It is delivered to more than one folder and the copies drift, so **every
copy is found and the newest wins** — and a stale one is reported rather than silently preferred.

`lib/migrations.mjs` parses the DDL: `CREATE TABLE`, `REFERENCES`, `ALTER TABLE`, partitioning,
row-level security, generated columns and enum types. It reads the subset of SQL these files use
and ignores the rest rather than pretending to be a SQL parser. Its table counts agree with
`tools/check-migrations.py`.

**Migrations** — what `backend/` actually contains: each `.sql` file in apply order, the tables
it creates, its policies and row-security coverage, and totals for partitioning, composite keys,
generated columns and enum types. Click any table to open it in the Data view. The 21 storage-only
tables are listed with the reason each has no contract schema, so the gap reads as a decision.

**Data** — the ER diagram, at two zoom levels.

*Whole database* is one box per schema, each listing which other schemas its keys reach into and
how many columns do the reaching. 21 boxes rather than 224: every table at once is a hairball with
no room for labels. Click a schema to drill into it.

*One schema* is its tables as entity boxes, every column with its type and `•` marking required.
**Green means a migration creates it and it is really there; blue means it is derived from the
contracts and still only planned** — 39 of 224 are green. Amber is a table pulled in from another
schema because something here points at it.

**Relationships come in three kinds, strongest first.**

- **A `REFERENCES` clause** in the DDL — the database saying what is true. 52 of these, 12 of them
  composite `(id, level)` keys from V0003a. Drawn solid.
- **Declared in a contract** — a column whose source property is a `$ref`. Drawn solid.
- **Inferred from a column name** — `_id` resolved by trying successively shorter suffixes, so
  `added_by_principal_id` finds `identity.principal`. A table in the column's own schema wins over
  one elsewhere, and a name owned by two schemas is refused rather than guessed at. Drawn dashed,
  counted separately, switchable off, and dropped entirely for any table the DDL covers.

**The DDL teaches the inference.** `venue_id` appears on 50 tables and there is no `venue` table —
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
- a **schema** → what references it, and **which table it is persisted as** — or, for 168 of
  them, why it deliberately has none
- a **screen** → which flows step through it, which screens reach it
- a **table** → what the DDL says about it, its real foreign keys, the contract schema it derives
  from, its inferred keys, and any `_id` column pointing at no table at all

Every one of those is a click, so a database column can be followed back to the screen that
displays it and forward to the migration that creates it.

The reader itself carries the same trail, so it does not need the pane to be open:

- a **schema** says which tables it is **stored as** — 182 of the 554 become one, and 21 become
  more than one, which is the case a link in only the other direction hides
- an **operation** says which tables it **reaches**, which of them it writes, and the service
  behind it — or, for 318 of the 654, that the lineage carries nothing for it. That is stated as
  a gap in `handoff/api-data-lineage.json`, never as a finding that the operation touches nothing

A screen's **reaches** block names the operations in the same position. It used to print the
union of what resolved and stop there: the Home Landing said "1 table" while two of the three
operations behind it — `listProducts` among them — had no lineage at all. It now names them and
says the count is a floor.

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

**Graph** — five scopes, opening on *Spine*.

*Spine* is the architecture picture the project had never had. It exists because the obvious one
does not work: the *Files* scope draws 24 contracts and 44 `$ref` links, and **every single one of
those links points at `shared/common` or `shared/permissions`**. No contract `$ref`s another. The
result is a two-pointed starburst that is true of everything and distinguishes nothing — the same
defect `handoff/schema-viewer-notes.md` calls out for `venue_id` and `principal_id` in the data
view, and the reason the *Ambient keys* toggle exists there.

The contracts are not joined by `$ref`s. **They are joined by events** — `order.paid` is published
by `orders` and consumed by `catalogue`, `finance`, `inventory`, `marketing` and `reporting` — and
until `events/` arrived there was nothing to draw that from. So:

- `shared/` sits at the centre, spine contracts in the inner ring, satellites outside
- **position carries meaning, so the force layout is off.** Within each ring the order is settled by
  pulling contracts that exchange events next to each other, which keeps the arrows short. Drag a
  contract and it stays where you put it
- dots are sized by **operation count**. The old *Files* view sized them by degree, which is zero
  for every contract, so they were all identical
- an arrow runs publisher → consumer, **amber where a consumer is critical**
- the 44 `shared/` `$ref`s are behind a toggle, off by default, for the same reason ambient keys are

Hover a contract to isolate its events. *Files* is still there, and now says what it is showing.
*Schemas* is every component and the `$ref`s between them; *Permissions* maps contracts to the
permission vocabulary; *Local* is the neighbourhood of the selection — two hops from a component,
one from a whole contract.

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

The server watches `contracts/`, `flows/`, `screens/`, `frontend/`, `backend/` and `designs/` and
re-indexes on save — including the `.xlsx`, so editing the schema reference in Excel updates the Data view. The
open page updates itself; no refresh, no restart.

Keys: `Ctrl`/`Cmd`+`K` search · `1` `2` `3` layer · `q` `w` `e` `r` `t` `y` `u` pick the view,
positionally — the letter matches the tab above it, left to right, so the third key is the third
tab of *this* layer rather than a fixed view somewhere else · `m` cycle the sidebar grouping ·
`l` local graph of selection · `Esc` out.

On any diagram — the galaxies, the graph, the structure tree, the ER and data maps, the state
machines — the **arrow keys** move it and `+` / `-` zoom it, with `Shift` for a longer step. A
galaxy turns where a flat diagram slides, which is what a drag does to each of them. Until this
landed, every canvas panned by drag and zoomed by wheel and by nothing else, so a reader working
from the keyboard could open a graph and then not move it.

*The list above used to name `w` screen, `g` graph, `s` structure and so on. Those were the keys
before the row became positional, and they had been wrong here for a while — `MODE_ROW` in
`public/app.js` is the one that decides.*

## What it costs to open

Opening the viewer once fetched all seven payloads — 4.8 MB, seven requests, four seconds before
anything could be read — and six of the seven were for layers nobody had opened. Three changes,
in the order they mattered:

**Each part is fetched when a layer needs it.** A part a layer cannot draw without is required; a
part only its side pane reads is fetched behind the layer once it is on screen. That distinction
is the one the first attempt missed, and it failed quietly rather than loudly — the Lineage view
drew perfectly, then marked all 671 of its table chips "not in the schema reference" because the
list it checks them against had not been asked for.

**Two fields left the index.** `/api/index` was 1.9 MB and, unlike the other parts, every layer
needs it — so the split above could not touch it. The fields of all 554 schemas and the prose on
every node are three tenths of its weight, and neither is read for more than one contract at a
time. They are served per contract by `/api/detail` and merged back onto the nodes the client
already has, so every existing reader of `node.description` goes on working unchanged.

**Everything is gzipped.** JSON full of repeated keys and repeated contract paths is close to the
best case for it.

| | before | now |
|---|---|---|
| opening on Contracts | 4.77 MB · 7 requests | **179 KB** · 3 requests |
| `/api/index` alone | 1.93 MB | 98 KB |
| the Lineage view | 7,098 elements at once | 106, and a group's rows when it is opened |

The last row is a different saving from the first two: gzip makes bytes cheaper to move, the
split makes them cheaper to parse, and neither stops a browser building 7,098 elements for a list
of which one group is ever open. A contract's rows are built when its group is first opened, and
above 60 they arrive a page at a time on a button that says how many are left.

## Layout

| | |
|---|---|
| `lib/indexer.mjs` | parses the contracts into nodes and `$ref` edges, and produces the audit |
| `lib/structure.mjs` | turns one document into a positioned structural tree |
| `lib/consumers.mjs` | reads declared consumers from `api-list.md` and the app roster |
| `lib/journeys.mjs` | joins `flows/` → `screens/` → the contracts, and reads `frontend/` |
| `lib/boards.mjs` | the design boards in `designs/`, and which platform each belongs to |
| `lib/wireframes.mjs` | the rendered wireframes in `wireframes/`, matched to screens, flows and platforms by id |
| `lib/xlsx.mjs` | minimal zip + sheet reader, so the workbook needs no dependency |
| `lib/backend.mjs` | the schema reference and ADRs, joined back to contract schemas |
| `lib/migrations.mjs` | the versioned SQL — tables, keys, partitioning, row security |
| `lib/relationships.mjs` | `handoff/relationships.csv` — the stated relationships and their kind |
| `lib/domain.mjs` | `states/` and `events/`, cross-checked against each other and the contracts |
| `server.mjs` | static server, `/api/index`, `/api/detail`, `/api/journeys`, `/api/domain`, `/api/backend`, `/api/file`, `/api/tree`, SSE — gzipped |
| `public/graph.js` | canvas node-link renderer — force-directed, or placed and directed for Spine |
| `public/structure.js` | tree and nested block renderers |
| `public/boxdiagram.js` | box-and-row layered layout, used by ER and Data |
| `public/statemachine.js` | directed state machine renderer, used by States |
| `public/tips.js` | the hover tips — a delegated panel and the glossary behind it |
| `public/app.js` | layers, views, routing, search, reader |

Node ids are stable and live in the URL hash, so any operation or schema can be linked directly:
`#op:contracts/spine/orders.yaml%23listOrders`.

## Not represented yet

- **Screen-to-screen sitemap** — `entryFrom`/`exitTo` are shown per screen and are clickable, but
  there is no whole-platform navigation graph. Worth building only once more of the 160 inferred
  navigation blocks are confirmed.
- **Platforms with no screen files** — none are left. The sidebar note counts them from the
  deployment table rather than asserting a list, which is why it stayed right while they landed:
  P02, P04 and P08 in the 14 August drop, the rest since. All twelve platform codes now have a
  file and 376 screens are defined. The retired code this line used to name was the kiosk before
  it was renumbered; naming a dead code anywhere in the tree is what `tools/check-package.py`
  rule 11 exists to catch, so it is not repeated here.
- **`docs/`** — the ADRs and registers are on disk but only ADR-0016 is surfaced, on Routing.
- **A context-to-context graph of its own.** The Domain layer lists contexts in the sidebar and in
  the right pane; the *drawing* of them is the Contracts layer's Spine scope. That is deliberate —
  they are the same 24 nodes — but it means the event topology has no view where events, rather
  than contracts, are the nodes.
- **Row-security policies** — the viewer says a table is `FORCED`, not what the 16 policies say.
- **Board-to-screen at the region level** — a board is attached to a screen, not to the part of the
  board that screen is. Splitting one exported board into nine screens is a manual read.

## Findings

**`states/entitlement.yaml` is anchored to a schema that is not an enum.** It declares
`contract: access, enum: TicketStatus`, and `access.TicketStatus` is an *object* — `ticketId`,
`isValid`, `entriesUsed` — with no enum values at all. None of `issued`, `partiallyConsumed`,
`fullyConsumed`, `expired`, `cancelled` or `surrendered` appears anywhere in any contract. So the
one model covering the entity that `access.validated` and `entitlement.issued` are both about is
checked against nothing, which is the single thing the folder exists to prevent.

**`tools/check-states.py` cannot see this**, and reports errors that are not real, because line 36
looks for the contracts as a *sibling* of the project root:

```python
CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"
```

Neither that nor its fallback exists here, so it loads zero enums and zero operations and every
lookup fails identically. Repointed at `contracts/` it passes. `tools/check-frontend.py` has the
same bug. The viewer resolves against the contracts it has already indexed, so it cannot go looking
in the wrong place.

**`entitlement.issued` is catalogued and no transition emits it.** Twelve of the sixteen events name
a transition in `states/` that publishes them; this one does not, which means either the transition
is not written down or it is published from somewhere the models do not cover.

**Nineteen of the thirty-eight status enums have no model** — `RequisitionStatus`,
`TenantMigrationStatus`, `TableStatus` and sixteen more. They are listed in the Domain sidebar
rather than counted, because the list is the to-do.

## What the contract audit found

**Platform code `P09` is used with two different names** — `"P09 Platform Admin Console"` and
`"P09 Platform Admin"`. One code meaning two things is the same failure mode `permissions.yaml`
warns about for permission strings, and it splits that platform into two sidebar entries. The only
error the Contracts layer now reports.

Two earlier findings are **fixed** in the current package: the duplicate `/reservations` block that
made `createReservation` unreachable, and the broken `whitelabel.homepage_section_section` parent
link. The Frontend layer is clean at every severity.

## One the viewer was caught by

The 14 August workbook renamed a column on the Modules sheet from `Columns` to `Cols`. The reader
required every identifying header to match exactly, so the header row was never found and the sheet
read as empty — **230 tables and zero schemas**, which took the whole Data view down with it.

Identifying headers now accept a list of names the workbook has used for the same thing, a sheet
that still cannot be read is an error in the audit, and no view indexes `[0]` of a list the audit
has already reported as empty. A rename should cost a column, not a layer.
