# Two things that need a decision before more screens are drawn

**7 September 2026.** Both were found by drawing, not by reading. Neither is blocking build —
nothing is being built — but both change what gets drawn next, and one of them is 96 screens
of work that may not need doing.

---

## 1. Ninety-six command centres

**The finding.** 115 of the 816 unboarded screens share one layout — `dashboard` template,
`dataTable` + `metricTile`, nothing else. **96 of those 115 are named "Command Center",
"Control Center" or "Monitor".** They fall out like this:

| Platform · module | Command centres |
|---|---:|
| P09 · Commercial | 47 |
| P08 · Access & Venue | 26 |
| P09 · Platform | 10 |
| P08 · Sell | 7 |
| P13 · Policy | 7 |
| P08 · Orders & Money, P10 · Partners, P12 · Support, P09 · Catalogue | 18 |

Read the names together and the mechanism is plain: **Commercial Pricing Command Center,
Pricing Rule Command Center, Tax Fee & Calculation Command Center, Pricing Governance Command
Center** — one per module boundary, in the same module family, on the same platform, with the
same two components.

**Why it is not a drawing problem.** A dashboard exists so somebody can see what needs doing
and start doing it. That is a property of a *role*, not of a module. A pricing manager opening
four pricing command centres in sequence has been handed a filing system, not a dashboard —
and the four have no stated precedence between them, which is the same defect the P09 review
raised nine times as duplicate pairs.

**The counter-argument, stated fairly.** Module-level dashboards are cheap to generate, they
give every module an obvious landing route, and a platform console genuinely does have staff
who work inside one module all day. If the org chart really is per-module, 96 is not
unreasonable. **That is the question — is it?**

**What is blocked behind it.** `CF-134` is open: *nothing in the platform raises an alert, and
five sections of the matrix ask for one.* Every threshold, every amber cell and every "needs a
decision today" row on a command centre is drawn against a capability with no contract behind
it. Consolidating first means writing the alert contract once rather than 96 times.

**Recommendation.** Consolidate to one dashboard per role, and count the roles before drawing
any of them. `BP-003` on **Pattern Boards** is drawn as the frame whatever survives will use —
one screen, four tiles, a table sorted by whether something stops a sale. If the answer is
that 96 stand, the frame serves all 96 unchanged and nothing is lost by asking.

**Needs:** Chinmay. One decision. Blocks 115 screens.

---

## 2. Seat management and CRM are drawn and specified nowhere

**The finding.** Two client packs — 250 screens across 25 boards — have no counterpart in the
package. This is the reverse of every other gap on the board: **the design exists and the
specification does not.**

### `seatp` — Seat Management & Venue Mapping · 130 screens

**114 of the 130 have no package screen at all.** Searching all 1,091 screen names:

```
/canvas/          0     /section/     0     /seating chart/  0     /suite/  0
/seat map/        1     POS-004 — selling from a map, not building one
/map builder|editor|designer/  2   BO-094 Map Editor & Publish · BO-150 Access Control Map Designer
```

The boards carry Venue Canvas, Sections & Zones, Rows & Seats, Standing Zones, Suites & Boxes,
Stage & Focal Point, Numbering Scheme, Sightline Survey. **Nothing in the platform authors
seating geometry.** Its two nearest screens are about access zones.

**This is larger than a board gap.** ADR-0005 partitions on `venue_id`. The `seating` schema
holds **14 tables**. ADR-0019 defines a standing zone as *"a capacity without individual
seats"*. `CF-122` fixed four silent failures in the seat importer, and `CF-166` settled seat
map reuse. **The data model, the ADRs and the importer all exist; the surface that authors
them does not.** Retiring these boards would delete the only design for it.

### `crm` — Marketing & CRM Configuration · 120 screens

**79 unmatched.** No Guest Directory, no Activity Timeline, no Corporate & Groups. Adjacent
things do exist — `ADM-200` CRM & Customer Segment Manager, `SUP-010` Customer 360° Service
Profile, `EMP-057` Guest Profile & Dining History, `BO-290` Family, Household & Dependent
Membership — **but the directory itself is not there.** `CF-132` already records that the
matrix asks for a guest portfolio ten times across ten sections.

**Recommendation.** Do not draw over these and do not retire them. Raise the 114 and the 79 as
a **package** gap — screens to be specified against boards that already exist — and keep both
packs on the index marked as design-ahead-of-spec, which is how they now render.

**Needs:** Chinmay to route. Not a design decision.

---

## What was decided without asking

For the record, because these were mine and they are reversible:

- **Five packs retired** — F&B, Retail, POS, Inventory, Seat sampler. 33 boards, 246 frames.
  Their subject matter is in the package under other names (`INV-2 Inventory Item Master` is
  `BO-081 Inventory Items`; `FNB-2B Menu Builder` is `BO-109`). Say the word and they come back.
- **36 boards whose files are absent are marked pending, not deleted** — 312 frames. They were
  rendering as links that went nowhere.
- **P09 wired to its board.** `TICVAI Web Board.dc.html` held 37 real frames that no module
  referenced, so every count reported 3.
