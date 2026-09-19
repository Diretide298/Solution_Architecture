# TICVAI design package — what is in this drop

**10 September 2026. Fifteen of seventeen checks pass; the two that do not are named below.**

```
1974 operations · 32 contracts · 556 tables · 1189 relationships
125 state models · 29 events · 96 flows · 46 ADRs
2427 screens · 16 platforms · 13 frontends · 5 apps · 218 boards
```

**`96 flows` counts authored journeys.** 106 more are derived from the client boards and carry
`provenance: derived-from-board` — they route screens the client specified and do not yet say
why anyone walks them. `check-board-flows` reports the two apart, because a number a generator can
move is not a measure of progress.

**`13 frontends` and `5 apps` are different units and both are real.** A frontend is the build
unit, one per platform, each joining to a `frontend/*.yaml` manifest that `check-frontend` and
`check-package` validate. An app is what a user installs — guest, venue-pos,
venue-staff-mobile, venue-management, ticvai-control — decided 10 September and carried
as `platform.targetApp`.

---

## Run it

```bash
bash tools/refresh.sh          # regenerates every derived file, then runs all ten checks
python3 tools/audit-links.py --detail
```

**`refresh.sh` is the only entry point.** Everything under `handoff/`, `diagrams/`, `backend/` and
`wireframes/P*.dc.html` is derived — **hand-editing any of it is overwritten on the next run**, and
that is the point rather than a limitation.

---

## The seventeen checks

| | What it refuses |
|---|---|
| `check-screens` | An operation that does not exist · an audience mismatch · a destructive button with no confirmation · a placeholder module · **a guest-callable operation with no guest screen** |
| `check-frontend` | A route with no component |
| `check-flows` | A step on a screen that is not there |
| `check-states` | A status enum with no model · **an event emitted without an outbox write** |
| `check-config-scope` | A configuration operation that does not declare its level |
| `check-wireframes` | A board anchor that does not exist · **a board this package did not generate** |
| `check-backlog` | A requirement with no operation |
| `check-traceability` | A requirement that reaches nothing |
| `check-package` | 41 rules — $ref resolution, closed vocabularies, currency columns, unbounded lists, orphan writes, duplicate YAML keys, **scope columns, DDL generations, lock contents** |
| `check-board-flows` | **A client board no process flow describes** · a flow step naming a screen that does not exist |
| `check-screen-redundancy` | Two screens that are the same screen |
| `check-bindings` | A component bound to nothing |
| `check-migrations` | A schema change with no migration |
| `audit-links` | Nine directions of cross-layer integrity, plus anchor collisions |
| `audit-workbooks` | A workbook section that no longer matches the package |
| `audit-pack-citations` | A citation pointing at a pack or page that is not there |
| `audit-transitions` | **Coverage, not a rule** · the share of navigation edges carrying an authored label |

**Warnings are not failures.** 968 on screens, 37 on flows, 5 on wireframes — each is a
decision somebody has to make, and the register says which.

**Two checks do not pass, and both are real work rather than noise.**

- **`check-board-flows` — 4 dangling references.** `F06 Guest enters the venue` names `SCN-005`,
  `SCN-006`, `SCN-010` and `SCN-012` — its denial, override and offline paths — and none of
  those four screens exists. The flow does not lack a denial path; it describes one that was
  deleted out from under it.
- **`check-package` — 9 errors.** Long-standing and tracked in the registers: seven `release*` lineage
  entries renamed to `relinquish*`, and two notes naming a platform by an old name.

`audit-links` reports every link resolving.

---

## Layout

```
contracts/      28 OpenAPI files — the source of truth. Everything else derives from here.
screens/        2427 screens across 16 platforms
flows/          203 journey files · 106 derived from the client boards, one per board but B2B board 1
states/         125 state models
events/         29 declared events
docs/adr/       44 architecture decisions
docs/active/    the working documents — audits, briefs, handoffs
docs/registers/ conflicts (CF-*), backlog, decisions

backend/        DDL, generated — 556 tables, 571 foreign keys, 644 indexes
services/       16 FastAPI skeletons for topology benchmarking
deploy/         four deployment configurations plus three burst variants
tools/          the generators and the checks
handoff/        derived artefacts for consumers — lineage, schema, burst scope, sizing
wireframes/     218 boards · 16 per platform, 5 per shipped app, 1 index. All
                generated. The 65 client-pack boards were archived on 10 September, and
                every screen that pointed at one was repointed rather than orphaned.
                frames/ holds what a designer drew, one file per screen; the boards
                render around it. design-base/ holds the client-approved POS build,
                unpacked so it can be edited.
sources/        every client file — MoMs, RFP, board PDFs, requirements
```

---

## Where the screen design stands

**46 of 2427 screens are drawn.** 13 batches of P01 Guest Web came back on 10 September,
passed the import with nothing refused, and 45 of the 46 carry seeded values rather than
blank rows. Those frames are now the house style: a later batch that re-derives the look
instead of matching them produces a second product, not more of this one.

| | batches | screens |
|---|---|---|
| drawn | 13 | 46 |
| locked (P04, the client-approved POS build) | 6 | 30 |
| pending | 191 | 1,553 |

**About 57 hours of design work remains**, measured at 18 minutes a batch. `QUEUE.md` in
`handoff/design-batches/` orders it by shipped app, cheapest platforms first, with P08 and
P09 late because between them they hold 1,060 of the package's screens.

**107 of the 191 pending batches are `WS##` workshop boards** — 1,067 of the pending screens, about 32 hours.
Their screens already live on a platform. Whether they are wanted as separate drawings is a
decision nobody has made; they are counted here because pretending they are not in the queue
would make the queue lie. 34 of them arrived on 11 September with `Latest Docs.zip` (DAM, Game &
Ride, Rental, Subscription), and their codes are `WS74`–`WS107`: **a `WS` code is issued once, in
`screens/_workshop-boards.yaml`, and never renumbered** — before that day the codes were
positions, and those four books moved 47 of them.

**Rental boards 6–8 are drawn twice, on purpose** — as `WS93`–`WS95` on P08 and as
`P06-rentals-01`–`03` on the staff app, decided 11 September. A counter attendant's handheld and a
supervisor's desk are different drawings of the same work.

**The Subscription book was placed by who works each screen**, 11 September. Boards 7 and 8 and
screen 6.10 are the new customer's own admin and moved to P08 (`WS104`, `WS105`,
`P08-setup-go-live-01`). **P17 TICVAI Sign-up** is new: three batches holding 24 of the book's screens, the ones a prospect sees
before they are a tenant, copied from boards 2, 4 and 5, which P09 keeps for the operator-led sale.

**54 pending batches have no operation behind any screen**, and `QUEUE.md` puts them last in a
section of their own. There is no data to seed and no control to gate, so under the finished-screen
brief they are the weakest ask in the queue; a night that runs short should lose these first.

**Every pending batch has its bundle.** `export-design-batch.py` writes
`handoff/design-batches/<id>/BUNDLE.md` — the brief plus every field of every screen, its
operations and its schemas, in one file. All 191 exist, on the brief that leads with the person
and bans spec vocabulary, and each one's screens match the manifest's batch.

**What the design sessions build from is the YAML, never the boards.** The bundle is derived
from `screens/P*.yaml` and carries `bindsTo`, `columns` and the operation behind each
component. The boards are an output. A session that reads a board instead is copying a
generator's placeholder — which is why the 22 stale renders were deleted on 10 September
rather than left on disk to be found.

**1,292 of 7,679 component labels are scaffolding, not copy.** 593 read `Every <screen name>`
and 663 read `The selected <screen name>` -- a generator naming a table after the screen it sits
on, because nobody had named it. `SCN-016 Gate mode` offers a designer "Every gate mode" and "The
selected gate mode" and nothing else. **These are placeholders to be replaced, and a build that
sets them in type has published a generator's shrug.** The 83% that remain were written by a
person and should be kept.

**719 of the 2427 screens cannot be drawn faithfully from what they declare.** They carry fewer
than four components, 224 carry none, and `purpose` runs to a median of 84 characters (measured
11 September). The bundle says
so where a designer will see it. Drawing over that gap invents requirements; the gap is a
specification problem and belongs in the log, not in a picture.

---

## The derived files a consumer should read

**`handoff/api-data-lineage.json`** — every operation with its verb, path, scope, permission,
audience, service, reads and writes. **The join everything else resolves through.**

**`handoff/schema-reference.json`** — 556 tables, every column, every reference, and a description
for all of them.

**`handoff/burst-scope.json`** — what a flash-sale environment runs, and what it does not. **Thirteen
services with `deployed: false` are in it deliberately.**

**`handoff/sizing.json`** — the replica algorithm for normal operation and for a sale, with the
venue tiers behind it.

**`handoff/relationship-graph.json`** — 959 edges across three kinds: `declared`, `convention`,
`lineage`.

**Take counts from these, not from parsing.** They come from the same pass that writes the DDL, so
a disagreement means a parser is reading something the generator did not write.

---

## 🔴 Open, and blocking

**CF-161** — one database per cell or one per service. **ADR-0028 still reads Accepted while
contradicting what the client was told on 24 August.** ADR-0036 carves out the burst cell and
settles nothing about the permanent platform.

**CF-64** — AWS or Azure, pending DESC. Carries RPO and RTO, **which are stated nowhere in 37
ADRs.**

**CF-162** — three deployment scenarios. Answered in `docs/active/`, not yet with the client.

**CF-165** — retention and archival absent. Three failure tables now exist and none has a retention
rule.

---

## 🔴 Two things in this drop that are wrong

**The cost tables understate by roughly half.** `TICVAI_Hosting_Summary` and
`TICVAI_Deployment_Technical` quote $3,485 for the shared cell on Fargate pricing **while shipping a
compose file** — nobody running that file arrives at that figure. And **~$4,400 is missing**:
staging, dev, observability and support, of which staging and dev are $3,000 and are required by
Allam's own release workflow.

**Nothing has been benchmarked.** `tools/bench.py` exists and has never run against anything. Every
replica count, every per-replica figure and every latency target is a hypothesis with a named way
to falsify it. **`rpsPerReplica` is the one that matters most and the one least likely to be
right.**

---

## Where the real risk sits

**Design is 90% of in-scope requirements. Build is 33%, and the DDL exists.**

**And the thing that cost a client relationship in Bahrain is contention, not throughput.** Thirty
thousand concurrent generates 3,750 RPS, which the arithmetic absorbs at 35 replicas. **What failed
was thirty thousand people wanting the same row**, and the only measurement that reaches it is
`holdContentionMs` under `--pattern hot-venue`.

**ADR-0037 should take that from 167 holds a second to 2,000 by removing a Redis round trip from
inside a lock.** Until it is measured, that is arithmetic.
