# The three outstanding design packs — what is missing and what each must contain

**25 August 2026.** The all-boards index tracks **320 rows the package has never seen.** Three packs,
and they are not equally urgent — the numbers below are counted from the package rather than taken
from the index.

---

## The tally, reconciled first

**The index and the package count different things and both are right.**

| | Index | Package |
|---|---:|---:|
| Screens | 678 board rows | **492 screens** |
| Drawn | 216 frames | **84 screens** pointing at a drawn board |

**One screen can own many frames.** `BO-044` owns eighteen — nine F&B and nine Retail — because
configuring an outlet and configuring a store are the same screen under a different licence. **That
is the module system working**, and it is why a frame count and a screen count will never agree.

**Pack frames on disk: 160.** F&B 62, Retail 58, POS 34, Boards v2 6. The index says 161 for the
same three. **One frame apart, and worth finding.**

---

## 1 · Inventory & Procurement — boards 6 and 7 only

**Least urgent of the three, and the index overstates the gap.**

**50 of 50 inventory operations are already on screens, and 20 of 28 screens are already drawn** —
the Retail and F&B packs covered receiving, counting and requisitioning between them.

**Eight screens remain undrawn:**

```
P06  EMP-066  Stock Count & Cycle Count Management
P06  EMP-068  Reservation, Allocation & Omnichannel Inventory
P06  EMP-069  Barcode, RFID, Serialized Stock & Traceability
P06  EMP-070  Inventory Exceptions, AI Replenishment & Actions
P08  BO-050   Stock Position & Valuation
P08  BO-138   Production Execution & Batch Management
P08  BO-140   Product Availability, 86 & Operational Food Safety
P08  BO-141   Operational Alerts, AI Replenishment & Action Centre
```

**Ask for boards 6 and 7 specifically**, not the pack. Boards 1–5 have already been absorbed
through the F&B and Retail drops, and re-importing them risks a second frame set for screens that
already have one.

**The file the index links and the package lacks is `Inventory Board 1.dc.html`** —
`check-wireframes` has warned *"a board still to arrive"* for days, and if boards 1–5 are already
covered, that link should be removed rather than filled.

---

## 2 · Marketing & CRM Configuration — 120 rows, the largest gap

**96 operations, 42 screens touch them, 6 drawn.**

**MarketingService is the largest domain in the package** — 96 operations, 37 tables — and it is
walked at 41%. The 20 August workshop covered CRM, identity resolution, consent, segmentation,
loyalty, wallet, marketing automation and the Visual Journey Builder, **and no board came out of
it.**

**Spread across five platforms**, which is why one pack is the right shape rather than five:

```
P01 Guest Web        10 screens
P02 Guest App         9
P08 Venue Management  6
P12 Venue Support     6
P06 Venue Staff App   3
```

**What the pack must cover, from the 20 August minute:**

- Customer profiles — unique and mandatory fields, **family and guardian linking**
- **Duplicate detection, identity resolution and merge rules** — CF-160 settled that a merge takes
  the narrower of two consents; the screen that shows a proposed merge does not exist
- **Consent, retention and archival** — CF-165 is open precisely here: consent is modelled,
  **retention and archival are not**
- Audience segmentation and behavioural analytics
- Loyalty, membership tiers, wallet
- Marketing automation — campaigns, offers, **the Visual Journey Builder**
- RBAC for CRM and configuration modules
- AI chat, routing and case management
- Surveys and gamification

**The Journey Builder is the one to see drawn before it is built.** A visual canvas is the kind of
screen a specification describes badly and a board settles in one picture.

---

## 3 · Seat Management & Venue Mapping — 130 rows, zero drawn

**47 operations, 15 screens, none drawn.** The only pack where the package has nothing.

```
P08 Venue Management  8 screens
P01 / P02             4
P04 / P10             2
```

**Four operations were built on 24 August against the 21 August decision and none has a drawing:**

- `copySeatMapSection` — section-level copy between maps
- `diffSeatMapVersions` — layout version comparison, **counts and one readable sentence per change,
  with accessible seats counted separately**
- `importSeatMap` / `getSeatMapImport` — **AI-assisted import from PDF, image, Excel or CSV**

**The import is the one that most needs a board.** It proposes a draft and a person accepts it
(ADR-0020) — **and what that acceptance screen shows is the whole design.** Confidence, what it
could not read, and a way to correct it before publishing. A seat map wrong by two rows is worse
than one that took an afternoon, and the screen is what makes that visible.

**The diff needs one too, for the same reason.** 396 rows in `Seating_Manifest_1.xlsx`; a diff that
lists 396 changes is noise. *"Row H moved back two"* is a design decision, not an implementation
detail.

---

## What to ask for, in one sentence each

| Pack | Ask |
|---|---|
| **Inventory** | Boards 6 and 7 only — 1 to 5 are already absorbed |
| **Marketing & CRM** | The whole pack, and the Journey Builder before anything else |
| **Seat Management** | The whole pack, and the import-acceptance and diff screens before anything else |

---

## What this unblocks

**CF-164** — the F&B/Retail/Procurement/Inventory workshop is outstanding in three consecutive MoMs,
and the package built 96 F&B operations without it. **Boards 6 and 7 are not a substitute for the
workshop.**

**CF-165** — retention and archival. The Marketing pack is where the screen would show what happens
to a profile at the end of its life.

**CF-166** — closed on the contract side 24 August, **open on the drawing side.** Four operations
with no board.
