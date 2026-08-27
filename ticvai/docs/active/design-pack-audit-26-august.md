# New design pack — audit, 26 August

**32 boards, 251 frames.** Twelve boards are new to the package: seven Inventory, four Seat, one
Dashboards. Nothing was lost; one shared board gained frames.

**Installed. Twenty screens mapped. `check-wireframes` at 7 warnings, all Inventory, and that is a
scope question rather than a mapping failure.**

---

## What came in

| | Boards | Frames | State |
|---|---:|---:|---|
| **Inventory** | 7 | **70** | **Not mapped — see below** |
| **Seat** | 4 | 15 | Mapped, 15 screens |
| **Dashboards** | 1 | 5 | Mapped, 5 screens |
| Retail Board 2 | — | +3 | `ret-2j`, `ret-2k`, `ret-2l` |
| F&B, POS, Retail, Boards v2 | 20 | 161 | Unchanged |

**Seat and Dashboards close CF-166's drawing half and the last of CF-162's dashboard gap.**

---

## The thing this pack does that the earlier three did not

**Its frames name their own screen.** `SEAT-1A · BO-093`, `data-screen-label="ADM-002"`.

**The F&B, POS and Retail packs had to be hand-assigned by board purpose** after three derivation
attempts produced nonsense — matching on shared operations gave *Outlet Management → Kitchen
Operations Command Centre* on one shared operation.

**A board that says what it draws removes the guess entirely.** Twenty screens mapped in one pass
with nothing to check by eye. **Worth asking for on every future pack.**

---

## 🔴 The Inventory pack is a different size from the Inventory in this package

**70 frames against 28 screens — and 20 of those 28 are already drawn** by the F&B and Retail drops.

**Seven boards of warehouse and procurement depth the contracts do not have:**

| The pack draws | Operations in the contract |
|---|---:|
| RFQ, quotation comparison, negotiation, award | **2** |
| Two-way and three-way matching, GRN, invoice capture | **0** |
| Warehouse zones, bins, put-away, picking, packing, dispatch | **0** |
| Demand forecasting and consumption planning | **0** |
| Supplier qualification, performance, scorecards | **0** |
| Serialisation, RFID, traceability | **1** |
| Unit-of-measure conversion | **0** |

**This is not a gap to fill by mapping.** It is a full WMS and procurement suite — sourcing to
award, receiving to three-way match, forecasting to replenishment planning — against a package with
50 inventory operations built for a venue stockroom.

**`docs/active/outstanding-design-packs.md` asked for boards 6 and 7 only**, on the grounds that
1–5 were absorbed through F&B and Retail. **That was right about the screens and wrong about the
scope**: the pack is not a redraw of what exists, it is a different product surface.

**Three ways this resolves and only the client can choose:**

**Contract it** — roughly 100 operations and 40 tables of WMS and procurement. A quarter's work.

**Scope it out** — the venue keeps a stockroom, and warehouse management is an ERP integration.
**`inventory` already has `x-ticvai-adaptor` precedent from queue systems.**

**Phase it** — take Board 1 (item master, UoM, locations, movement history), which maps onto
screens that exist, and defer 2 through 7.

**Recorded rather than guessed.** Mapping these frames onto seven back-office screens would claim a
coverage that is not there.

---

## Small findings

**`Inventory Board 1` uses a different anchor scheme from Boards 2–7** — `inv-2`, `inv-3`, `inv-10`
against `inv-2a`, `inv-3a`. **No collision** (checked all 251 anchors, zero duplicates across
boards), but `inv-2` and `inv-2a` living in different files invites one.

**`inv-1` and `inv-6` are not on Inventory Board 1.** They sit on `TICVAI Boards v2`, which also
carries `fnb-1a`, `ret-1a`, `pos-2a` and `pos-2f`. **Boards v2 is a scratch board holding six
frames that belong on five other boards** — worth folding in before it becomes the place frames go
to be forgotten.

**`ret-2h` is drawn and the index does not link it.** One frame of 251. **Every other anchor
resolves both ways** — 255 index links, zero broken.

**The index is clean.** 31 boards referenced, 31 present, no dead links. **Better than the copy in
the package, which had four links to an `Inventory Board 1` that had not arrived** — now superseded.

---

## What changed in the package

- 32 boards installed, `assets/` and `support.js` alongside
- **20 screens moved to `wireframe.status: designed`** with `boardFrames` set and the previous
  generated board kept in `generatedFallback`
- `TICVAI All Boards Index.dc.html` replaced with the pack's, which is current
- **All nine validators pass.** `check-wireframes` 7, every one an unmapped Inventory board

**Drawn screens: 64 → 84.**
