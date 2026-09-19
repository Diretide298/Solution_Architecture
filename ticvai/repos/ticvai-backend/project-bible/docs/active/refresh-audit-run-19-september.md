# The refresh, the wallet, and nine files nothing rebuilds — 19 September 2026

> **Owner:** Chinmay · **Status:** complete, unpushed · **Commits:** `4931d46`…`23d5a8b`
>
> Follows `contract-run-result-19-september.md`, which added 346 operations and four
> contracts. This run did not add capability. It asked whether the package could tell when
> it was wrong, and the answer was no in four separate places.

---

## The finding this run turned on

**`refresh.sh` regenerates the package, and the things it cannot reach are the things most
likely to be wrong.**

Nine files in `handoff/` and `wireframes/` look exactly like derived artefacts. They sit
beside real ones, they are read by the pipeline and by the viewer, and **no tool in
`tools/` writes any of them.** From the refresh's point of view they are inputs, so it
reads them and says nothing.

`handoff/service-decomposition.json` was the worst of them. Its own note read *"How 28
contracts and 378 tables become 16 deployable services"* against 32 and 561, and `rental`
and `accreditation` appeared in it nowhere — while `check-package`, `derive-diagrams`,
`derive-burst-scope` and both workbooks read it to draw the service topology. **Four
contracts were absent from every service diagram and both workbooks, and every checker
passed.**

That is the shape of every defect below: not a missing feature, but an artefact that had
quietly stopped describing the thing it names.

---

## 1 · The blast radius, written down

`docs/contract-change-runbook.md` — four rings by how far a contract change has to travel
before it becomes visible.

| ring | what it covers | automatic? |
|---|---|---|
| 1 | data layer — lineage, schema, relationships, DDL, burst, sizing | yes, ~4 min |
| 2 | presentation and screens — diagrams, workbooks, the screens block | yes, ~6 min |
| 3 | registers, status, mirrors | yes, ~3 min |
| **4** | **nine authored inputs no tool rebuilds** | **no** |

Twelve steps around an edit, and the ordering constraints inside the chain with what each
one cost to learn. Cross-linked from the ingestion runbook.

## 2 · `refresh.sh` was missing eleven tools

`conflict-status.md` was **25 days older** than the register it indexes. The screen ledger,
estate audit, undrawn list and thin-screens workbook were 10 to 15 days stale. All eleven
are in now, `derive-board-flows` ahead of `derive-transitions-from-flows` so a new board
flow becomes an edge in the same run.

The checker loop carried a comment claiming *"every checking tool in tools/ is now in this
list"* while six sat outside it. **The script now fails if a file in `tools/` is neither run
nor named in `_EXCLUDED` with its reason** — a claim that checks itself rather than one
that ages.

## 3 · The wallet had 33 operations and every one was configuration

The acts were elsewhere: 13 of `retail.yaml`'s 37 — read a balance, top it up, adjust,
transfer, freeze, close, and the whole gift-card lifecycle — plus two in `games.yaml`.
**Rule and act in different contracts, which is the defect this run has been about, sitting
in the middle of the wallet domain.**

`wallet.yaml` is now 48 operations, `retail` 24, `games` 35.

**WalletService, because eight domains need a wallet and none owns it.** A Gold Membership
issues F&B credit, parking credits and ride credits into one wallet, so subscription, games
and F&B all read it, and `getWalletLiability` aggregates across every credit type. The
client declares Ride, Attraction and Redemption Ticket credit in the **wallet** module's
balance library, beside F&B, Retail and Parking — not in the games module. Games keeps 35
of its 37: readers, pricing, prizes, card lifecycle, eligibility. **The card is a
credential, not a wallet**; blocking a lost one leaves the balance untouched (board 7.7).

**The client's thirteen wallet types were never thirteen kinds.** Board 1.2 says "such as",
and read as presets they are `ownerKind × allowedCreditTypeIds × scopePath × channels` —
Membership and Closed-Loop differ by credit type, Event, Resort and Cashless Venue by
scope. **So no enum values were added.** What was missing is the capability half:
`storedValue`, `topUp`, `transfer`, `refund`, `giftCard`, `voucher`, `membershipCredit`,
`wearable` and `usageChannels`. That is also the answer to how three callers share one
operation — they all call `topUpWallet`, and the wallet type says whether that channel may.

`topUpWallet` is **guest-callable** now. A screen named *Self-Service Wallet Top-Up* was on
the staff back-office calling a staff-only operation while Guest Web could transfer balance
but never add any. Game & Ride board 10.5 asks for exactly this.

`accreditation` moved to **TenancyService, not AccessService** — AccessService is the
edge-cached turnstile path, and accreditation is a back-office approve/issue workflow whose
writes would invalidate those caches.

## 4 · Two of the five documents were never documents

`api-list.md` claimed **581 operations against 1,974** and carried a
published/specified/not-specified key that stopped meaning anything once the contracts
became the source of truth. `LINKAGE.md` said **364 screens against 2,427**. Every column
either held is a field the contracts or the screens already carry, so both are now
`build-api-list.py` and `build-linkage.py`, wired in after `link-screens-contracts` —
which is where `x-ticvai-consumed-by` is written, so the consumers column is current rather
than a cycle behind.

**Ring 4 goes from nine files to seven.** A file that can be generated should be.

The other three were updated against the contracts:

- **`rag-index-sources.md`** — the seven events it said did not exist all exist now. In
  their place, a finding it could not have had: **six of its eleven sources name a text
  field the schema does not have.** `marketing.case` has no `resolution` column, so the
  source whose whole value is how the last complaint was resolved can only embed a subject
  line.
- **`artefact-audit.md`** — dated 17 August, predating the walk. All 142 sections are
  closed; 2,647 of 3,184 rows CONTRACTED, 98 a genuine gap. Twelve artefact classes it
  called missing are closed. **The two it got most right are the two still open**: retention
  still states contradictory periods with no register, and device/hardware is now the
  third-worst gap domain at 17 rows.
- **`schema-viewer-notes.md`** — numbers, not a rewrite. The hub pattern is unchanged and
  the same three tables lead it; the schema went 378 → 564 tables, so 306 of 953 edges now
  terminate in four tables where it said 163 of 406.

## 5 · Moving a table is not the same as changing one

The wallet move renamed three tables from the `retail` schema to `wallet`. The derived layer
kept rebuilding the old ones. Dropping them from `schema-reference.json` worked and did not
last.

**There is a cycle.** `derive-schema` reads `relationship-graph.json` for edges the
contracts do not declare — *486 of 514 references are conventions rather than `$ref`, so
the graph is the source* — and `derive-relationships` rebuilds that graph from
`schema-reference.json`. **Cleaning either alone is undone by the other.** They were dropped
three times before that was visible.

Above both sat the real source: **`derive-lineage` adds and never updates, and that applies
to `reads` and `writes`, not only to `contract` and `service`.** Twenty-six operations still
listed `retail.wallet`, so every refresh re-derived the tables from the lineage and
`backend/` emitted `CREATE TABLE` for both.

Repointed at source: 26 lineage operations, 27 names in `links.json`, 13 graph endpoints,
6 dangling column references, and `orders.yaml`'s `x-ticvai-lock-excludes` — the only place
a contract still named the old table.

The move also broke three things with nothing to do with the schema: two state machines
declaring `contract: retail`, **51 traceability rows** citing the moved operations against
`retail`, and `check-package`'s `CURRENCY_OK` allowlist.

## 6 · Generating a file silently emptied the viewer

`lib/consumers.mjs` is **the only place in the repo that maps an endpoint to a front-end
app**, and it read `api-list.md` by column index. Dropping the status column moved every
field one place left, the method test failed on every row, and the map came back empty —
**0 endpoints mapped**, which reads exactly like a package that declares no consumers.

No checker covers the viewer, so nothing failed. It reads by heading now: **1,783 endpoints
across all six apps.**

`decisions.mjs` had the same shape of damage — it parses an artefact-class table out of
`artefact-audit.md`, and the rewrite had no such table, so that panel went quietly empty.
Restored: **14 classes, 12 covered, 2 open.**

## 7 · The lineage is read by twenty tools and checked by none

`tools/check-lineage.py` — seven checks, all against the contracts rather than against
itself:

1. every entry names an operation a contract declares
2. every declared operation has an entry
3. `contract` matches the file that defines it
4. `service` matches `service-decomposition.json`
5. no null service — `derive-diagrams` raises on `None`
6. every table in `reads`/`writes` exists
7. every postgres table has exactly one owning service

**It would have caught all three of this run's failures.** Only one was visible to
`check-package`.

It also found **50 unowned tables** — a service carries `contracts` and `schemas` as two
lists that do not map one to one (`venue-map`→`venuemap`, `tenancy`→`platform`,
`subscription`→`control`), and only one had been updated. **Now 556 owned, 0 unowned, no
schema claimed twice.**

## 8 · Machine-called operations are finished

Thirteen declare `service` or `device` as their only audience. Counting them against screen
coverage makes the figure permanently unreachable and buries the operations that really do
lack a surface.

```
surfaced by a screen    1798   91.1%
machine-called, no UI     13    0.7%   complete
──────────────────────────────────
accounted for           1811   91.7%
no surface yet          163    8.3%
```

**Twelve wiring gaps closed** — each acts on a noun its screen already shows, on a screen
that already receives the identifier, for an audience that already uses that platform.
`ANL-039` could preview a report execution and not cancel it; `EMP-059` is *Table Order,
Bill & Payment* with no way to ask for the bill.

**Twenty-one more look identical and were left alone.** No screen both receives their
identifier and makes sense of the verb, and matching on the parameter alone proposes
`cancelSubscription` on *Integrations* and `reinstateEntitlement` on *Receipt & Reprint* —
plausible, wrong, and the same title-matching failure this run has been about.

---

## Where the package stands

| | |
|---|---|
| contracts | 34 files, **32 deployable** |
| operations | **1,974** · 1,798 wired (91.1%) · 13 machine-called · 163 with no surface |
| screens | **2,427** · 4,988 api references · **0 naming an operation that does not exist** |
| tables | **561** · 5,793 columns · 556 owned by exactly one service |
| services | **17** in 5 tiers |
| flows | 289 · events 29 · boards 218 |
| requirements | 3,184 rows, 142/142 sections closed, **83.1% contracted** |

**Checkers** — `check-screens` PASS · `check-states` PASS · `check-traceability` PASS 0
warnings · `check-board-flows` PASS · `check-wireframes` PASS · `check-migrations` PASS ·
`check-flows` PASS · `check-frontend` PASS · `audit-links`/`workbooks`/`pack-citations`
PASS · transition coverage **95%**.

Not at PASS: `check-package` **9**, `check-lineage` **7**, `check-config-scope` **57**,
`check-authored-inputs` **3 stale**.

---

## Open, with what each needs

**Decisions only you can make**

- **7 ghost `release*` lineage entries** — orphaned by the 8 September rename. `--apply`
  never removes, so they persist. Deletion is a decision, not a repair.
- **21 wiring gaps with no sensible target** — each needs a screen or a placement.
- **6 apps in `repos/ticvai-frontend/apps` against 13 in `frontend/`** — the viewer treats
  the 6 as canonical, deliberately. The scaffold is behind the design.
- **Three table counts in circulation** — `derive-ddl` 552, `schema-reference.cols` 561,
  the viewer's `storage` 565. The difference is partition siblings and
  `platform.schema_version`. Nothing names which the handoff means.

**Queued in the plan, before frontend work**

- **The reference graph undercounts by about a fifth.** 234 columns are plainly keys with
  no target, across 105 of 564 tables showing no outbound reference — impossible in a
  venue-scoped schema. `venue_id` is missed 16 times and `order_id` 14. True edge count is
  nearer **1,190 than 955**, and hub concentration goes up rather than down.
- **Module-implied navigation** — needs the above.
- **137 features with no screen.** The boards cannot finish them: 1,866 of 1,924 board
  entries are already drafted, and `derive-task-linkage --all` reaches 14 of 188. **There is
  no White Label / CMS module among the 36 pack decks** — those 15 operations were authored
  from the specifications, not drawn by the client.

**Found here, not yet actioned**

- 6 RAG sources name a column that does not exist
- 22 tables written and never read; 39 touched by nothing
- `WalletService` has no `readsFrom`/`writesOutside` — derivable
- `SCN-003` has no outcome states, though the 18 August absorption note says it kept them
- `check-contract-split` flags device-management operations sitting in `tenancy`
- **The derived layer is one refresh behind** — twelve api references were added after the
  last full run.
