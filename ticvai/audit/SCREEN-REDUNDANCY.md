# Screen redundancy audit

**492 screens across 15 platforms · measured by contract operation signature · `ticvai/screens/*.yaml`**

Read by the contract operations each screen declares rather than by the name it carries, the 492
definitions resolve to **373 distinct behaviours**. So **105 screens do exactly what another screen
already does**, and 168 (34%) sit inside a cluster of two or more screens with an identical operation
set.

The gap is not spread evenly. It sits on eight workspaces that were drawn once per platform that
touches them, and on one guest product that was inventoried twice.

| | |
|---|---|
| Screens defined | **492** |
| Screens declaring operations | 478 |
| Distinct operation signatures | **373** |
| Exact functional duplicates | **105** |
| Screens inside an identical-signature cluster | **168** (34%) |
| Identical-signature clusters | **63** |
| Pairs sharing ≥80% of operations | 203 (134 screens) |
| Screens declaring no operations at all | **14** |

---

## 1. What was measured

Every screen was reduced to the set of contract operations it declares under `apis[].operationId`.
Two screens with the same set are treated as the same screen: they read the same data, offer the same
actions, and will need the same loading, empty, error and offline states.

Names, modules and platforms were **ignored while clustering**. Nothing in this report rests on two
screens happening to be *called* the same thing — where a name collision is the finding, it is named
as one.

Two thresholds are used throughout:

- **Identical** — the operation sets match exactly.
- **Near-identical** — sets overlap by ≥80% (Jaccard), counted only for screens declaring at least
  three operations, so a one-operation screen cannot match another by accident.

### What this method cannot see

Operations are a good proxy for *what* a screen does and a poor one for *who is standing in front of
it*. A gate device held in one hand and a desk in the back office can call the same endpoint and still
be two screens; the failure mode, not the payload, is what separates them.

**Fourteen screens declare no operations at all** — four of the eight accreditation screens among them
— so they are invisible to the clustering entirely. They are listed in Appendix C.

Every judgement below about *context* rather than data is a reading of the one-line `purpose` field.
That field is itself unreliable: **28 screens share one of just four sentences** (§6.2). Where a
finding here contradicts what the team knows about the user, the team is right — the value is that the
question now has specific screen ids attached to it.

---

## 2. Where the duplication sits

Share of each platform's screens sitting inside a cluster of two or more identical-signature screens.

| Code | Platform | Screens | In a cluster | Share |
|---|---|---:|---:|---:|
| P07 | Venue Scanner | 11 | 8 | **73%** |
| P01 | Guest Web | 46 | 30 | **65%** |
| P10 | Partner Portal | 21 | 10 | 48% |
| P02 | Guest App | 63 | 28 | 44% |
| P09 | Admin Console | 37 | 15 | 41% |
| P06 | Staff App | 66 | 26 | 39% |
| P11 | Accreditation | 8 | 3 | 38% |
| P05 | Guest Kiosk | 17 | 5 | 29% |
| P08 | Back Office | 143 | 37 | 26% |
| P15 | Kitchen Display | 10 | 2 | 20% |
| P12 | Support Console | 8 | 1 | 12% |
| P16 | Venue Analytics | 10 | 1 | 10% |
| P13 | White-Label CMS | 20 | 1 | 5% |
| P04 | Staff POS | 24 | 1 | 4% |
| P14 | Developer Portal | 8 | 0 | 0% |
| | **All platforms** | **492** | **168** | **34%** |

**P16 and P04 read low for opposite reasons.** The POS screens are genuinely distinct from each other,
which is why only one of the twenty-four lands in a cluster — a positive result worth keeping. Venue
Analytics scores low because its ten screens differ from each other by one or two operations apiece:
they are not *identical*, they are ten configurations of the same report screen, which the clustering
measure is the wrong instrument to catch. §5.1 covers it.

---

## 3. Tier 1 — hard duplicates

Groups where a name, a module or an exact operation set is shared and nothing in the definitions
explains why both screens exist.

### 3.1 Two name collisions inside one platform

**`F&B Order Management` — BO-020 and BO-047**

- `BO-020` — module *Food & Beverage*, 11 kitchen and F&B order operations.
- `BO-047` — module *Orders & Money*, the 14 generic order operations — the same set as Order Detail,
  Held Orders and Group Bookings.

BO-047 is not an F&B screen. It is the order workspace wearing an F&B name.

**`Asset Register` — BO-031 and BO-069**

Same title, same module (*Access & Venue*), no distinguishing purpose. This has the shape of an id
that was never retired when the maintenance screens were folded into the section. BO-031 also shares
its exact operation set with `CMS-004 Logo & Assets` on the white-label platform.

### 3.2 The order workspace — one table, seven headings

Seven screens across four platforms declare an **identical fourteen-operation set**:

| Id | Screen | Platform |
|---|---|---|
| POS-006 | Held Orders | Staff POS |
| EMP-014 | Ticket lookup | Staff App |
| BO-022 | Order Detail | Back Office |
| BO-026 | Group Bookings | Back Office |
| BO-047 | F&B Order Management | Back Office |
| PTR-008 | Booking Creation | Partner Portal |
| PTR-015 | Order History | Partner Portal |

```
listOrders · getOrder · createOrder · modifyOrder · voidOrder · holdOrder · resumeOrder
rescheduleOrder · exchangeOrderLines · createRefund · listOrderRefunds · applyManualDiscount
reprintOrder · getOrderStatement
```

Four more sit one operation away:

- `BO-023 Refunds & Exchanges` — 13 of the 14.
- `BO-051 Purchase Orders`, `BO-070 Work Orders`, `PTR-016 Voucher / Ticket Download` — a second
  identical cluster on a 13-operation set.

**Eleven screens in total over one object.** The last three are a different question: a purchase order
and a ticket order are not the same thing, and the fact that they were given the ticket-order
operations is a *modelling* problem rather than a merge candidate. Worth resolving before either
screen is built on the wrong contract.

### 3.3 Eight navigation landings counted as screens

`BO-101` … `BO-108` each take their name from the module they head and declare exactly one operation:
`getVenueSettings`.

| Id | Name | Id | Name |
|---|---|---|---|
| BO-101 | Orders & Money | BO-105 | Stock & Supply |
| BO-102 | Sell | BO-106 | People & Access Rights |
| BO-103 | Access & Venue | BO-107 | Guests & Marketing |
| BO-104 | Food & Beverage | BO-108 | Venue Operations |

These are the eight items of the back-office navigation, plus `BO-100 Venue Home` as its root.
Counting them as screens inflates P08 and, under the four-states rule in `_schema.yaml`, commits the
team to writing loading, empty-first-run, error and offline states for a menu. The same question
applies to the four *Command Center* landings on P06, P15 and P16.

### 3.4 Shift and cash — five screens over one ledger

Identical 13-operation set: `EMP-009 End shift`, `BO-039 Shift Directory`, `BO-040 Variance Approval`,
`BO-041 Cash Movements`, `BO-042 Banking & Safe`.

`POS-001 Begin Shift` and `POS-007 Close Shift` carry all thirteen inside a set of seventeen —
supersets rather than copies, and defensible as the terminal's own view of the same ledger. Seven
screens in the family altogether.

### 3.5 Announcements, notifications and the emergency path

Six screens on an identical four-operation set (`listAnnouncements`, `publishAnnouncement`,
`acknowledgeAnnouncement`, `getAnnouncementReach`):

`EMP-007 Handover notes` · `EMP-037 Notifications` · `EMP-038 Broadcast to team` ·
`EMP-039 Announcements` · `EMP-047 Emergency mode` · `BO-066 Notification Settings`

**EMP-047 Emergency mode is the one to look at.** If an emergency really is a broadcast list with the
same four operations and the same states as handover notes, then the emergency path has not been
designed — it has been filed. That is a correctness question, not a screen count.

---

## 4. One guest product, inventoried twice

The largest single overlap. Twenty screens carry the same name on Guest Web and Guest App, and on
**every one of the twenty the two screens declare exactly the same operations**. P01 is 46 screens and
P02 is 63, so the overlap is a third of the mobile app.

| P01 | Guest Web | P02 | Guest App | Ops |
|---|---|---|---|---:|
| WEB-002 | Event & Attraction Listing | GST-003 | Event & Attraction Listing | 4 |
| WEB-004 | Attraction Details | GST-004 | Attraction Details | 4 |
| WEB-007 | Interactive Seat Selection | GST-049 | Interactive Seat Selection | 3 |
| WEB-013 | Booking Confirmation | GST-010 | Booking Confirmation | 3 |
| WEB-015 | Branded Queue / Waiting Room | GST-046 | Branded Queue / Waiting Room | 3 |
| WEB-018 | My Tickets | GST-012 | My Tickets | 6 |
| WEB-019 | Order History | GST-019 | Order History | 4 |
| WEB-030 | Ticket Transfer | GST-014 | Ticket Transfer | 3 |
| WEB-031 | My Reservations | GST-016 | My Reservations | 3 |
| WEB-032 | Offers & Promotions | GST-037 | Offers & Promotions | 3 |
| WEB-034 | Lost & Found | GST-034 | Lost & Found | 3 |
| WEB-035 | Multi-Currency & Pricing | GST-044 | Multi-Currency & Pricing | 2 |
| WEB-036 | F&B – Browse & Order | GST-024 | F&B – Browse & Order | 8 |
| WEB-037 | Menu Item Detail | GST-061 | Menu Item Detail | 2 |
| WEB-038 | F&B – Order Tracking | GST-025 | F&B – Order Tracking | 3 |
| WEB-040 | Virtual Queue | GST-023 | Virtual Queue | 4 |
| WEB-041 | Parking – Reserve & Pay | GST-027 | Parking – Reserve & Pay | 3 |
| WEB-043 | Loyalty & Rewards | GST-036 | Loyalty & Rewards | 4 |
| WEB-044 | AI Concierge – Home | GST-031 | AI Concierge – Home | 5 |
| WEB-046 | In-Venue Notifications | GST-030 | In-Venue Notifications | 1 |

**Three P02 screens are genuinely mobile** and justify a native app: `GST-055 Dynamic QR Ticket` (a
rotating code the web cannot hold), `GST-059 Plan My Day – In Progress` (location through the day),
and the push path behind GST-030. Twenty duplicated storefront screens do not.

**Two of the twenty may not be screens at all.** `Multi-Currency & Pricing` is a property of every
price on every screen, not a destination. `Lost & Found` appears a third time as `EMP-028` in the staff
app, which is the only one of the three with a person on the other side of it.

**The purposes do not match.** Of the twenty pairs, only `WEB-018 / GST-012` share a purpose sentence.
The rest differ — but they differ as prose, not as behaviour. Nothing in either definition says what a
guest can *do* on one that they cannot do on the other.

---

## 5. Tier 2 — recurring by construction

Not accidental collisions. Each is a capability that was given its own screens on every platform that
touches it.

### 5.1 One report engine, twenty-five surfaces

Twenty-five screens across seven platforms call `runReport`, `getDashboard` or `getFinancialReport` —
ten on P08, nine on P16, one or two each on P04, P09, P10, P12 and P15.

**P16 Venue Analytics.** Nine of its ten screens are in that set; seven call both `getDashboard` and
`runReport`. Each differs from the next by one or two operations that fetch the figures —
`getStockValuation` on the margin screen, `listSegments` on the guest one. The difference between these
screens is the report they load. (`ANL-010 Suggestions & Advice` is the exception — it calls neither.)

**Identical, four ways.** `BO-029 Report Builder`, `BO-059 Sales Reports`, `BO-061 Scheduled Reports`
and `PTR-018 Reports & Sales Performance` share an **identical nine-operation signature**, including
the natural-language query and the report CRUD. `BO-058 Reporting Home`, `POS-008 Reports` and
`SUP-008 Agent Performance & SLA View` sit just outside it on the same operations.

### 5.2 The stock ledger, drawn for the floor and for the desk

P06's *Stock on the Floor* module is ten screens using 27 operations. **Nineteen of those — 70% — are
already used by P08's Stock & Supply** (fifteen screens, 60 operations).

| P06 Staff App | Relationship | P08 Back Office |
|---|---|---|
| EMP-065 Receiving & Store Put-Away | 3 shared ops | BO-052 Goods Receipt |
| EMP-066 Stock Count & Cycle Count Management | **all five count ops** | BO-079 Stock Count |
| EMP-063 Requisition & Smart Store Replenishment | 2 shared ops | BO-078 Requisitions |
| EMP-064 Store-to-Store & Warehouse Transfers | 1 shared op | BO-080 Stock Transfers |
| EMP-069 Barcode, RFID, Serialized Stock & Traceability | **identical** | BO-114 Variants, Attributes, Barcode & RFID Management |
| EMP-070 Inventory Exceptions, AI Replenishment & Action Center | **identical** | BO-141 Operational Alerts, AI Replenishment & Action Center |

The eight operations P06 has that P08 does not are the ones that argue for keeping a floor surface at
all: `logTemperature`, `logColdChain`, `getHaccpStatus`, `signCorrectiveAction`, `setDailyCount`. That
is a food-safety round done standing up with a device — **two or three screens, not ten**.

### 5.3 The kitchen queue, in three places

P15 is a ten-screen platform using 24 operations, and **seventeen of them already appear on other
platforms** — nine in P08's F&B section, seven at the point of sale.

- `KIT-002 Kitchen Display System` / `BO-046 Kitchen Display` / `POS-022 Send to Kitchen`
- `KIT-005 Kitchen Station Workload & Dynamic Routing` ≡ `BO-134 Kitchen & Preparation Stations`
  (identical two-operation set — the kitchen configures its stations, and the back office configures
  them again)
- `KIT-010 Kitchen Performance, AI & Operational Optimization` ≡ `ANL-008 Demand Forecasting`

### 5.4 One people directory, three owners

`BO-053 Staff Directory`, `ADM-020 Platform User Directory` and `PTR-003 Profile & Company Details`
declare exactly `listPrincipals`, `getPrincipal`, `createPrincipal`, `updatePrincipal` over the same
records. The scope differs — a venue's staff, the platform's users, a partner's own people — which is
exactly the shape of one screen with a scope parameter rather than three screens with three sets of
empty and permission states.

`BO-054 Role Assignment` and `ADM-021 Platform Role Management` are a second identical pair alongside
them.

### 5.5 Six admin screens on one infrastructure signature

Entirely inside P09: `ADM-013 Tenant Performance Monitor`, `ADM-014 Auto-Scaling Configuration`,
`ADM-030 Infrastructure Sizing & Scaling Policy`, `ADM-032 WAF & Security Policy View`,
`ADM-033 Backup & DR Status`, `ADM-034 Archival Job Monitor` — all six on the same seven
cell-management operations.

A WAF policy and an archival job have almost nothing in common operationally. This is most likely the
signature of an operation list applied to a whole section at once rather than screen by screen —
a **data-quality finding about the definitions** as much as a redundancy finding about the product. A
second P09 cluster of four does the same with two support-notice operations.

---

## 6. Tier 3 — weaker signals

Neither proves duplication on its own. Both reliably indicate a screen created because a section
needed a heading rather than because a person needed a page.

### 6.1 Naming formulas

Counts are screens whose name *contains* the phrase, across all fifteen platforms. (Read strictly as
suffixes the first three are 31, 9 and 5.)

| Formula | Screens | Note |
|---|---:|---|
| … Management | 33 | Eight platforms. Almost always a list plus a form. |
| … Configuration | 12 | Settings split by section, not by who may change them. |
| … Dashboard | 8 | Ten screens share one purpose sentence with these. |
| … Monitor | 7 | `EMP-031 Queue monitor` and `BO-005 Queue Monitor`. |
| … Directory | 6 | Queue, Product, Shift, Staff, Tenant, Platform User. |
| … Command Center | 4 | EMP-051, EMP-061, KIT-001, ANL-001 — all landings. |
| … Action Center | 3 | EMP-070, BO-141, ANL-009. Two are identical. |
| AI surfaces | 15 | Eight platforms, no shared component between them. |

### 6.2 Copy-pasted purposes

Four sentences are doing duty for **28 screens**, which means those 28 were never asked the question.

| Uses | Sentence | Screens |
|---:|---|---|
| 10 | *"The screen this app sits on. Everything else is entered from here and returns to it."* | WEB-017, GST-001, GST-011, GST-031, ADM-002, ADM-003, ADM-031, PTR-002, ACC-001, SUP-002 |
| 8 | *"Find the right one quickly, and act on it without opening it."* | WEB-009, GST-003, GST-020, GST-023, ADM-005, ADM-020, ACC-006, SUP-004 |
| 6 | *"Answer a question without needing a person."* | WEB-025, GST-033, GST-040, ADM-026, ADM-035, PTR-021 |
| 4 | *"Take the money, and be unambiguous about whether it worked."* | GST-027, GST-041, PTR-012, PTR-014 |

---

## 7. What is **not** redundant

**P06 *Floor Service* survives unchanged.** It looks like exactly the same kind of duplicate as the
stock module beside it — ten screens over restaurant tables, next to P08's F&B section. It is not. The
two share **two operations out of twenty-nine each**. Table service is genuinely a different job from
F&B configuration.

**The scanning cluster is mostly an artefact of the definitions.** Eight screens across P06, P07 and
P08 share an identical seven-operation set, but a gate admission, an offline package status and a
back-office scan log are not one screen — that signature is an operation list applied to a whole
platform at once. The real finding there is narrower and sharper:

```
EMP-010 ≡ SCN-007      EMP-015 ≡ SCN-008      EMP-017 ≡ SCN-014
```

The staff app and the scanner restating each other, three pairs deep.

**The test applied throughout:** *would one screen with a parameter serve both people, on both devices,
in both failure modes?* Where the answer is no, the pair is left alone and marked intentional.

---

## 8. The inverse finding — the unread failure path

Raised separately, and it is the counterpart to everything above: not a screen that exists twice, but a
failure state that has no screen at all. Checked against the schema and the event definitions, the
three named tables come out differently from each other.

### `sync.rejection` — **covered**

It is a declared root in `handoff/schema-roots.md`, and `listSyncRejections` is called by **six
screens**:

`EMP-017 Sync & reconciliation` · `SCN-014 Sync & reconciliation` · `BO-037 Offline Package Status` ·
`BO-130 Offline Policy & Rules Configuration` · `BO-132 Offline Transaction Monitor & Sync Queue` ·
`BO-133 Offline Alerts, Limits & Audit`

If anything this one is over-covered — four of those six are in the offline cluster and BO-132 and
BO-133 are close neighbours.

### `platform.dead_letter` and `ai.index_failure` — **not declared anywhere**

Neither appears in `contracts/`, in `diagrams/lld/`, or as a root in `handoff/schema-roots.md`. The
`ai` root is `ai.index_source`; `platform` roots at `platform.org_unit` across 24 tables. So the
problem is one step earlier than "no screen reads them": **the tables do not exist yet.**

But the dead-letter *policy* does, and this is the sharp version of the finding:

`events/_schema.yaml` declares `onFailure: [retry, retryThenDeadLetter, deadLetterImmediately, ignore]`
on every consumer, with this note against `isCritical`:

> *"True where the business breaks if this consumer never runs. Drives alerting — a dead-lettered
> critical event is a page, not a dashboard."*

Across the event definitions:

| | |
|---|---:|
| Consumers that can dead-letter | **47** |
| Event types involved | **28** |
| Of those consumers, marked `isCritical` | **47 — all of them** |

**Forty-seven critical consumers can dead-letter, no table is declared to hold what they drop, and no
screen reads it.** The schema's own comment says this should be a page. There is no page, and there is
nowhere for the row to land.

`replayEvents` exists as an operation and is called by exactly one screen — `DEV-005 Webhooks` on the
developer portal — which is a partner-facing redelivery tool, not an operator's dead-letter queue.

**Recommended:** one screen, and the table behind it, before any of the six decisions below. It is the
only item in this document that makes an outage invisible rather than making a backlog larger.

---

## 9. Six decisions, in this order

Each row is a question with an owner, not a refactor. Answering them is what removes the screens.
Ordered by how much each unblocks: the first two decide what a third of the remaining wireframes even
look like.

| # | Decision | Screens |
|---|---|---:|
| 01 | **Is the guest app a second product, or a wrapper?** Twenty screens duplicated between P01 and P02, each pair declaring exactly the same operations. If the app is a shell over the same storefront, P02 keeps only the three screens that need the device and everything else becomes one definition with two breakpoints. If it is genuinely a second product, each of the twenty needs a sentence saying what is different on a phone. | 20 |
| 02 | **Is there one order workspace, or one per platform?** Seven screens declare the identical fourteen order operations. One screen taking an order id and a role replaces all seven; what differs is which actions the permission allows, which `_schema.yaml` already models on the component. Decide it before BO-051 and BO-070 inherit the same fourteen for a different object. | 6 |
| 03 | **Is Venue Analytics a platform, or a report library?** Nine of ten screens call a reporting operation, seven call both `getDashboard` and `runReport`, and BO-029 already builds them. If a saved report is a configuration rather than a screen, P16 becomes two screens — a library and a viewer. | 10 |
| 04 | **Which app owns scanning — the staff app or the scanner?** EMP-010/015/017 restate SCN-007/008/014 operation for operation. Both platforms are offline-capable, and two apps queueing admissions offline against the same gate is a reconciliation problem, not a duplication problem. Carries a correctness cost, not only a cost in screens. | 3 |
| 05 | **Does the floor need its own stock app, or a food-safety round?** 70% of P06's stock vocabulary is already in P08 and two screens are identical to back-office ones. What P06 has that P08 does not is the HACCP set. | 7 |
| 06 | **Are navigation landings screens?** BO-101–108 are the section menu, BO-100 its root. Under the four-states rule each owes four states. Either they are navigation and leave the inventory, or the rule does not apply to them. | 8 |
| | **Total** | **54** |

**492 → 438** if all six go the consolidating way.

The count is not the point. Fifty-four removed is fifty-four sets of loading, empty, error and offline
states nobody has to write, and fifty-four fewer wireframes to draw and review.

---

## 10. Two schema fields would stop it recurring

```yaml
sameAs: <screen id>
```

Declares that this screen is another screen at a different scope or on a different device, and names
what differs. A screen with `sameAs` inherits states rather than re-declaring them; one without it that
duplicates a signature fails the check — the way `check-screens.py` already fails an unknown operation
id.

```yaml
kind: screen | landing
```

A landing is navigation. It keeps an id and a route so links resolve, and it is exempt from the
four-states rule — which is honest about what BO-101 to BO-108 are, instead of leaving nine permanent
TODOs in the specified count.

---

## Appendix A — all 63 identical-signature clusters

168 screens. Clusters of 3+ listed individually; pairs grouped.

| # | Scr | Ops | Screens |
|---:|---:|---:|---|
| 1 | 8 | 7 | **Scanning & access** — EMP-010, EMP-015, SCN-007, SCN-008, SCN-009, SCN-013, SCN-015, BO-034 |
| 2 | 8 | 1 | **Back-office section landings** — BO-101 … BO-108 |
| 3 | 7 | 14 | **Order workspace** — POS-006, EMP-014, BO-022, BO-026, BO-047, PTR-008, PTR-015 |
| 4 | 6 | 4 | **Announcements** — EMP-007, EMP-037, EMP-038, EMP-039, EMP-047, BO-066 |
| 5 | 6 | 7 | **Platform infrastructure** — ADM-013, ADM-014, ADM-030, ADM-032, ADM-033, ADM-034 |
| 6 | 5 | 1 | **Ticket delivery** — GST-008, GST-045, GST-055, KSK-010, KSK-012 |
| 7 | 5 | 13 | **Shift & cash** — EMP-009, BO-039, BO-040, BO-041, BO-042 |
| 8 | 4 | 1 | **Help & system status** — WEB-025, WEB-028, WEB-029, GST-047 |
| 9 | 4 | 9 | **Reporting** — BO-029, BO-059, BO-061, PTR-018 |
| 10 | 4 | 2 | **Platform notices** — ADM-024, ADM-026, ADM-035, ADM-036 |
| 11 | 3 | 7 | **Guest account** — WEB-017, WEB-024, WEB-027 |
| 12 | 3 | 2 | **Rota** — EMP-021, EMP-022, EMP-023 |
| 13 | 3 | 11 | **Sessions** — BO-015, BO-016, BO-019 |
| 14 | 3 | 13 | **Order-shaped objects** — BO-051, BO-070, PTR-016 |
| 15 | 3 | 4 | **People directory** — BO-053, ADM-020, PTR-003 |

**Pairs (clusters 16–63), grouped:**

- **The 20 Guest Web / Guest App pairs** listed in §4.
- **Guest / kiosk siblings** — WEB-006/KSK-005, WEB-008/GST-048, WEB-009/GST-020, WEB-033/KSK-017,
  GST-002/KSK-003, GST-022/ACC-006
- **Staff-side pairs** — EMP-017/SCN-014, EMP-004/EMP-005, EMP-019/EMP-020, EMP-033/BO-017,
  EMP-035/PTR-012, EMP-024/BO-056, EMP-026/BO-072, EMP-028/PTR-021, EMP-040/EMP-041, EMP-069/BO-114,
  EMP-070/BO-141, SCN-002/SCN-016
- **Back office, admin, partner, kitchen** — BO-025/PTR-014, BO-031/CMS-004, BO-054/ADM-021,
  BO-062/BO-065, BO-134/KIT-005, ADM-001/SUP-001, ADM-022/ADM-023, PTR-011/PTR-017, ACC-002/ACC-005,
  KIT-010/ANL-008

## Appendix B — near-duplicates (≥80% shared, not identical)

62 pairs, 47 distinct screens.

Almost all of them are one family. **`BO-023 Refunds & Exchanges` shares 13 of 14 operations with every
member of the order workspace cluster**, and BO-051, BO-070 and PTR-016 sit at the same distance. With
the seven identical screens that is eleven over one object, and it accounts for the large majority of
the 62 pairs.

The genuine near-misses worth looking at individually:

- `WEB-016 Login / Register` ↔ `GST-042 Simple Registration & OTP` — **95%**
- `EMP-004 Task list` ↔ `EMP-006 Raise a task` — **94%**
- `EMP-005 Task detail` ↔ `EMP-006 Raise a task` — **94%**

A list, a detail and a create form sharing almost every operation is the ordinary CRUD case, but it is
worth confirming EMP-006 is a distinct screen rather than a modal on the other two.

## Appendix C — screens declaring no operations

| Id | Screen | Platform |
|---|---|---|
| GST-043 | Arabic / RTL Experience | Guest App |
| KSK-001 | Attract Loop | Guest Kiosk |
| KSK-014 | Out of service | Guest Kiosk |
| EMP-044 | Accessibility | Staff App |
| EMP-045 | Arabic / RTL | Staff App |
| BO-067 | Integrations | Back Office |
| PTR-019 | API Credentials & Integration | Partner Portal |
| ACC-001 | Landing / Programme Overview | Accreditation |
| ACC-003 | Application Review & Submit | Accreditation |
| ACC-004 | Application Status Tracking | Accreditation |
| ACC-008 | Credential Register | Accreditation |
| SUP-006 | Knowledge Base Search | Support Console |
| CMS-013 | SEO & Metadata | White-Label CMS |
| CMS-017 | Domain & Certificate | White-Label CMS |

Some are correct — an attract loop and an out-of-service screen genuinely call nothing. **Four of the
eight accreditation screens are here, which is the one that stands out:** ACC-003 Application Review &
Submit and ACC-004 Application Status Tracking must read and write something. Those two are missing
definitions, not screens without behaviour.

## Appendix D — `screens/README.md` is stale

It describes **364 screens across twelve platforms** with a table totalling 347, and reports 27 screens
as fully specified. The YAML now holds **492 across fifteen platforms**, all carrying non-stub states
and a layout, 478 of them carrying operations.

The dependent claims are stale too — it says sixteen venue-scanner screens carry `TODO` offline states;
P07 has 11 screens and no TODO states remain. Worth regenerating before its numbers are quoted
anywhere else.
