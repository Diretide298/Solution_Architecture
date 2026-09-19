# `seating.yaml` — the worked example, and the audit was wrong about it

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** two decisions to take
>
> First contract taken from [contract-audit-19-september](contract-audit-19-september.md), which
> ranked it **MISMATCHED** — 21 of 35 operations unused, 119 of 128 board screens unserved.
> **That verdict is wrong and the tool's rule is what made it wrong.**

---

## The audit inferred the wrong cause from the right numbers

The rule read *"many unused operations **and** many unserved board screens"* as evidence that the
contract models a different thing from the boards. For `seating` it is the exact opposite: the two
halves are **the same thing, never joined**.

Sorting the 35 operations by what they do makes it obvious:

| | operations | used |
|---|---|---|
| **Runtime** — holds, availability, blocks | `listSeats` `getSeatAvailability` `createSeatHold` `extendSeatHold` `relinquishSeatHold` `getSeatHold` `recommendSeats` `listSeatBlocks` `createSeatBlock` `allocateBlockedSeats` `relinquishSeatBlock` `listSeatMaps` `listSeatCategories` `listSeatMapTemplates` | **14 of 14** |
| **Authoring** — build, import, publish | `createSeatMap` `updateSeatMap` `publishSeatMap` `validateSeatMap` `getSeatMap` `updateSeats` `setMapZones` `setSeatingRules` `getSeatingRules` `createSeatCategory` `createSeatMapTemplate` `cloneSeatMap` `copySeatMapSection` `diffSeatMapVersions` `importSeatMap` `importSeatManifest` `importSeatGeometry` `commitImportJob` `getImportJob` `getSeatMapImport` `assignSeats` | **0 of 21** |

**The split is clean.** Every runtime operation is called; not one authoring operation is. That is
not a contract modelling the wrong domain — it is a contract whose authoring half has no screens
pointing at it, because the seat management boards were parsed on 18 September and never linked.

**Lesson for the audit tool:** unused operations plus unserved screens in one domain has two
possible causes, and they need opposite work. Either the contract is wrong, or the join is missing.
The tool cannot tell them apart and should say so rather than pick.

## Every one of the 21 is backed by the 21 August MoM

Rank 1, and it is specific:

> *"the platform will support both manual seat map building and AI-assisted import (PDF/image +
> Excel/CSV), plus **full and partial (section-level) copy-paste** between seat maps, and a
> **layout version-comparison view** showing seat-count/configuration differences."*

> *"**Best-seat ranking** (e.g., last-row-is-best vs. first-row-is-best, depending on venue
> sightlines) must be configurable per seat map/event."*

> *"A seat map is configured independently and then associated with one or more
> events/performances on a separate event-configuration screen."*

| MoM decision | operation | board screen |
|---|---|---|
| manual seat map building | `createSeatMap` · `updateSeatMap` | `BO-954` Venue Canvas |
| section types — standing, suite, stage, obstruction | `setMapZones` | `BO-955`–`BO-961` |
| AI import from PDF / image | `importSeatMap` | `BO-964` PDF & Image Import |
| companion Excel / CSV for row and seat naming | `importSeatManifest` | `BO-966` CSV & Excel Import |
| CAD / vector geometry | `importSeatGeometry` | `BO-965` SVG & CAD Import |
| validate before publishing | `validateSeatMap` | `BO-971` Validation & Correction |
| publish | `publishSeatMap` · `commitImportJob` | `BO-972`, `BO-982` |
| import progress | `getImportJob` · `getSeatMapImport` | `BO-963` Import Command Center |
| reuse a saved map | `cloneSeatMap` | `BO-976` Clone & Inheritance |
| **partial, section-level copy** | `copySeatMapSection` | `BO-976` |
| **layout version comparison** | `diffSeatMapVersions` | `BO-977` Version Compare |
| template library | `createSeatMapTemplate` | `BO-974` Template Library |
| best-seat ranking per map | `setSeatingRules` · `getSeatingRules` | `BO-962`, `BO-993` |

**Nothing needs authoring here.** The contract is right, MoM-backed, and idle.

---

## Decision 1 — wire the 21, do not write anything new

This is the whole fix for the "119 unserved" half. It is a linkage job, not a contract job, and it
takes `seating` from 14/35 operations reached to 35/35.

**It also removes seat entries from the 1,305-operation gap list**, which proposed authoring
`listSeatMap`, `setSeatMapTemplate` and similar — names derived from screen titles for operations
that already exist under better ones. **That is the concrete cost of the title matcher, measured:**
every one of those would have been a duplicate.

## Decision 2 — the boards contradict the MoM, and the MoM wins

Board 1 draws **seven** screens for what the MoM decided is **one**:

```
BO-954 Venue Canvas          BO-958 Suites & Boxes
BO-955 Sections & Zones      BO-959 Stage & Focal Point
BO-957 Standing Zones        BO-960 Entrances, Exits & Aisles
                             BO-961 Amenities & Obstructions
```

> **Decision (21 Aug):** *"section type (seated / non-seated-zone / standing / suite) will be a
> configurable attribute set **at the section level within a single seat map builder screen**,
> rather than requiring separate configuration screens per type **as shown in the reference
> tool**."*

The board reproduces the reference tool's shape — the very thing the minute rejected. Under the
precedence rule (**MoM > boards**) these collapse into one builder screen with section type as an
attribute.

**This is a step-2 compression decision that the triage missed**, because the triage scores a new
screen against *built* screens and these seven are all new — they are only redundant against a
decision, and no tool reads decisions.

**The open action is about how, not whether:** *"Chinmay's team to confirm how the seat map builder
will consolidate the reference tool's multiple configuration screens (canvas, standing zone, suite,
best-seats, entrance/exits) into one unified screen."* The decision line is unambiguous; the action
is the design of it.

### What is owed

- [ ] **Wire the 21 operations** to the board screens above — no new operations
- [ ] **Decide the collapse**: seven board-1 screens into one builder, per the 21 August decision.
      Six ids retired, nothing rendered lost — all seven have zero components
- [ ] **Re-run the audit** and confirm `seating` leaves the MISMATCHED row
- [ ] **Fix the audit tool's verdict** so unused-plus-unserved reports *"either drift or a missing
      join — read both halves"* rather than asserting drift
