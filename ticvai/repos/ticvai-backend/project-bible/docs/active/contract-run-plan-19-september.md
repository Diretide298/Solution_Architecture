# The contract run — plan

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** in progress, Phase 0
>
> Ordered by **blast radius from the dependency graph**, not by size. A contract that many others
> read is done before the ones that read it, because changing it invalidates their work.
>
> Governed by [source-precedence-19-september](source-precedence-19-september.md) —
> **MoM > boards > specifications, matrix where all three are silent** — and
> [contract-audit-19-september](contract-audit-19-september.md), which ranked all 30.

---

## Why contracts first

Contracts sit at the top of the derivation chain: lineage → DDL → sizing → burst scope → diagrams
→ workbooks → screens → wireframes → mirrors. **A wrong contract does not announce itself.** It
produces a screen layer that cannot bind and a gap list proposing operations that already exist
under another name.

Both of those were measured on 19 September: **15.9% of components bound**, and a 1,305-operation
gap list whose seating entries were every one a duplicate.

## Phase 0 — the cheap test, before anything is written

**`seating` is why this phase exists.** It was ranked `MISMATCHED` on 21 unused operations against
119 unserved board screens, which reads as drift. Sorting its operations told the opposite story:

| | used |
|---|---|
| 14 runtime operations — holds, availability, blocks, recommend | **14 of 14** |
| 21 authoring operations — build, import, publish, clone, diff | **0 of 21** |

A clean split, and the 119 screens *were* the authoring half. **Wiring them took it to 0 unused
without one line of contract change.** Writing those 21 operations — which the gap list proposed —
would have produced 21 duplicates.

So before any contract is opened:

| | contract | ops | unused | unserved | verdict to reach |
|---|---|---:|---:|---:|---|
| 0.1 | `orders` | 168 | 23 | 178 | join or author |
| 0.2 | `catalogue` | 174 | 13 | 162 | join or author |
| 0.3 | `promotions` | 131 | 12 | 116 | join or author |
| 0.4 | `marketing-crm` | 167 | 25 | 107 | join or author |
| 0.5 | `approvals` | 38 | 1 | 74 | join or author |
| 0.6 | `resources` | 9 | 0 | 95 | **expected: author.** 0 unused means no idle half exists |

**Nothing is written in Phase 0.**

## Phase 1 — leaves, where nothing depends on the answer

| | contract | read by | work |
|---|---|---|---|
| 1.1 | ~~`seating`~~ | ai (5) | **done — 35 ops, 0 unused** |
| 1.2 | `resources` | **nothing** | author against 95 screens and the matrix |
| 1.3 | `approvals` | subscription (2), workforce (1) | per Phase 0 |
| 1.4 | `promotions` | orders (2), ai (1) | per Phase 0 |
| 1.5 | `white-label` | ai (3) | **stale** — decide the 20 unused |
| 1.6 | `retail` | orders (3), finance (1) | **stale** — decide the 16 unused |
| 1.7 | `cross-region` | — | **stale** — 12 of 16 unused and **no boards behind it**. Pure decision |

## Phase 2 — foundations, because everything reads them

| | contract | read by | issue |
|---|---|---|---|
| 2.1 | `identity` | marketing-crm (17), orders (12), fnb (10), access (10) | **42 matrix gaps** |
| 2.2 | `tenancy` | cross-region (28), shift (7), subscription (6), orders (6) | **24 matrix gaps** |

Their problem is requirement coverage rather than board pressure, so the work is closing matrix
rows, not drawing from boards.

## Phase 3 — core, in dependency order

| | contract | reads | read by | unserved |
|---|---|---|---|---:|
| 3.1 | `catalogue` | access (8), tenancy (3) | **orders (22)**, ai (11), access (8) | 162 |
| 3.2 | `orders` | **catalogue (22)**, access (19), identity (12) | shift (43), subscription (8) | 178 |
| 3.3 | `marketing-crm` | identity (17), catalogue (6) | identity (6), orders (4) | 107 |

**`catalogue` before `orders`** — orders reads 22 catalogue tables and catalogue reads 3 of orders'.

## Phase 4 — the five domains with no contract

New files, and each needs the MoM and the matrix read before an operation is written.

| | domain | screens | operations naming it | note |
|---|---|---:|---:|---|
| 4.1 | **Rental** | 100 | **0** | nothing exists under any name |
| 4.2 | **Licensing / subscription self-service** | 100 | 4 | may extend `subscription` rather than a new file |
| 4.3 | **Accreditation** | 79 | 3 | `P11` already exists with 8 screens |
| 4.4 | **Event Management** | 33 | **0** | likely extends `catalogue` — **after 3.1** |
| 4.5 | Finance Backend | 2 | 0 | trivial |
| — | ~~AI Forecasting~~ | 20 | 0 | **held back — the AI boards are not complete** |

## Phase 5 — close the loop

| | step |
|---|---|
| 5.1 | `derive-pack-linkage --apply` and `derive-task-linkage` — new operations wire themselves |
| 5.2 | `check-bindings` — 15.9% bound should move, and the 526 winnable component bindings unblock |
| 5.3 | `refresh.sh` — lineage, DDL, sizing, diagrams and both workbooks all follow |
| 5.4 | `audit-contracts --write` — confirm the verdicts cleared |
| 5.5 | **one batch export, one queue, `P04` excluded** |

---

## Two things to expect

**Phase 0 may collapse most of this plan.** `seating` looked like 21 operations of contract work
and was none. If `orders` and `catalogue` split as cleanly, Phase 3 becomes wiring rather than
authoring and the 1,305-operation gap list shrinks sharply.

**`resources` is the one expected to be real.** Nine operations against 95 screens with **zero
unused** means there is no idle authoring half to find. That is genuine absence — and it is a leaf,
so it can start immediately, in parallel with Phase 0.

## Open decision carried from `seating`

Board 1 draws **seven** screens — Venue Canvas, Sections & Zones, Standing Zones, Suites & Boxes,
Stage & Focal Point, Entrances/Exits/Aisles, Amenities & Obstructions — for what the 21 August MoM
decided is **one**:

> *"section type will be a configurable attribute set **at the section level within a single seat
> map builder screen**, rather than requiring separate configuration screens per type **as shown in
> the reference tool**."*

All seven are wired to the same `setMapZones`, so the binding is right either way. **Six ids retire
if the collapse is taken**, and nothing rendered is lost — all seven carry zero components.

---

# Carried forward — do these before any frontend work

Added 19 September, after the coverage audit. **Each one changes a number the frontend reads**,
so doing them afterwards means rebuilding whatever was built on the old figure.

## 1. The reference graph is undercounting by about a fifth

`derive-schema` resolves 955 edges — 596 declared, 359 by convention — and leaves **234 columns
that are plainly keys with no target**, across **105 of 564 tables that show no outbound
reference at all**. That cannot be true of a venue-scoped schema where nearly every table carries
`venue_id`.

The misses are concentrated in exactly the hubs the schema-viewer notes are about:

| column | missed | should resolve to |
|---|---:|---|
| `venue_id` | 16 | `platform.scope` |
| `order_id` | 14 | `orders.sales_order` |
| `organisation_id` | 6 | `platform.scope` |
| `partner_id` | 4 | `platform.scope` |
| `parent_id` | 5 | the table itself |
| `*_ids` (`venue_ids`, `seat_ids`, `entitlement_ids`, `allowed_venue_ids`, `cell_ids`, …) | 19 | one-to-many — **a model change, not a lookup** |
| `*_ref` (`image_asset_ref`, `icon_asset_ref`, `credential_ref`, `signature_ref`) | 12 | soft reference by convention |

**The machinery already exists** — 359 edges are resolved by convention today — so the singular
cases are a lookup table away. The plural ones are not: a column holding many ids is a
one-to-many edge and the graph has no kind for it.

**True edge count is nearer 1,190 than 955, and hub concentration goes up rather than down**,
because 30 of the misses are `venue_id` and `order_id`. Every artefact built on the current
figure — the schema viewer, `relationship-graph.json`, the diagrams — is drawing a sparser graph
than the data supports.

## 2. Navigation the module structure implies

There will not be a button for every edge, but **module structure determines which edges are
worth offering as navigation** and that is derivable rather than authored. Do this after (1),
because it reads the corrected graph.

## 3. The three authored inputs still stale

`contract-backlog.json`, `backlog-clusters.json` and `traceability.json` are ring 4 and need a
walk, not a rewrite. `tools/check-authored-inputs.py` reports them on every refresh.

## 4. The seven ghost lineage entries

`releaseChannelAllocation`, `releaseCustomDomain`, `releaseInventoryHold`, `releaseSeatBlock`,
`releaseSeatHold`, `releaseStoredValue`, `releaseWalletAuthorisation` — orphaned by the
8 September `relinquish*` rename. `derive-lineage --apply` never removes, so they persist:
1,981 entries against 1,974 real operations. **Deletion is a decision, not a repair.**
