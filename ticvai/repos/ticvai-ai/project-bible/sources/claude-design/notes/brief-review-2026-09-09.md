# Review of the 9 September design brief — before it goes out

**Four corrections. One changes the size of the job.**

> **Corrected 9 September after review — §1 overstated the recovery. The tranche is 96, not 88
> and not 104; see §7. The cause is 10 frames with two claimants each, where one frame draws one
> screen.**

---

## 1 · The tranche is **88**, not 104. And two more platforms are finished.

`undrawn.json` inherits `board-index.json`'s client-pack blind spot: the indexer's
`ANCHOR` regex has no boundary before `id="`, so on client packs it matches the tail of
`data-screen-id="BO-045"` rather than the frame's real anchor (`fnb-4a`, `ret-2c` — which fail
`\d{2,4}`). It therefore sees exactly the 111 codes the 31 August stamping pass wrote, and misses
22 screens the package itself declares a pack frame for. **133 pack-framed, not 111.**

Sixteen of those 22 are in Wave 1–2 and are therefore in the 104:

| Screen | Wave | Pack frame |
|---|---|---|
| `EMP-051` Restaurant Service Command Center | 2 | `FnB Board 4#fnb-4a` |
| `EMP-053` Table & Seating Configuration | 2 | `FnB Board 4#fnb-4c` |
| `EMP-054` Reservation Calendar & Timeline | 2 | `FnB Board 4#fnb-4d` |
| `EMP-056` Walk-In & Waitlist Management | 2 | `FnB Board 4#fnb-4f` |
| `EMP-057` Guest Profile & Dining History | 2 | `FnB Board 4#fnb-4g` |
| `EMP-066` Stock Count & Cycle Count Management | 2 | `Retail Board 4#ret-4f` |
| `EMP-069` Barcode, RFID, Serialized Stock & Traceability | 2 | `Retail Board 4#ret-4j` |
| `EMP-070` Inventory Exceptions & AI Replenishment | 2 | `Inventory Board 1#inv-10` |
| `BO-013` Channel & Distribution | 2 | `Retail Board 5#ret-5g` |
| `BO-015` Session Calendar | 1 | `Seat Board 2#seat-2a` |
| `BO-016` Session Template | 1 | `Seat Board 2#seat-2b` |
| `BO-019` Closures & Blackouts | 2 | `Seat Board 2#seat-2d` |
| `BO-053` Staff Directory | 1 | `Marketing Board 1#crm-1b` |
| `BO-093` Map Import & Labelling | 2 | `Seat Board 1#seat-1a` |
| `BO-094` Map Editor & Publish | 2 | `Seat Board 1#seat-1b` |
| `POS-007` Close Shift | 1 | `TICVAI Boards v2#pos-2f` |

Ten of the sixteen are frames whose anchor is correct in the package but whose code the stamp
either dropped (a frame claimed by two screens can hold only one `data-screen-id`) or never wrote
(the code stayed board-derived, `SEAT-2A` where the package says `BO-015`). `POS-007` is in
`TICVAI Boards v2.dc.html`, which `classify()` files as `generated` on `startswith("TICVAI")`
although it is a client pack board holding real frames.

### Corrected schedule

| Platform | Undrawn | Wave 1 | Wave 2 | W1+2 |
|---|---|---|---|---|
| `P08` | 294 | 36 | 34 | **70** |
| `P02` | 17 | 9 | 8 | **17** |
| `P09` | 280 | 1 | — | **1** |
| `P13` | 40 | — | — | — |
| `P10` | 30 | — | — | — |
| `P12` | 20 | — | — | — |
| `P06` | **0** | — | — | **—** |
| `P04` | **0** | — | — | **—** |
| **Total** | **681** | **46** | **42** | **88** |

**`P06` and `P04` are finished** — all eight P06 undrawn screens and the one P04 screen are drawn
on client packs. That is **nine** complete platforms, not seven. Sending the brief as written asks
Design to redraw sixteen screens the client already drew, eight of them a whole platform.

---

## 2 · `board-index.json` does not find frames "by that anchor and nothing else"

§4 states that, and it is the sentence that will cause this to recur. On Claude Design's boards it
is true — their anchors really are `id="bo-001"`. On client packs the count comes from
`data-screen-id`, read by accident. **Fix the regex before the next index run, because the two
changes interact:**

```python
CODES  = re.compile(r'\bdata-screen-ids?="([^"]+)"')   # both shapes, then .split()
ANCHOR = re.compile(r'\sid="([^"]+)"')
```

The plural matters. The pack frames in `sources/old-boards/` have been restamped with
**`data-screen-ids`** — space-separated, every claimant listed — because ten frames are claimed by
two screens and one attribute cannot hold both. `ids="…"` does not match `id="…"`, so with the
current regex those boards read as **22** instead of 133, and because the index reuses records by
hash it degrades board by board as each file changes.

Also reclassify `TICVAI Boards v2.dc.html` as `clientPack`, or classify on content — a board is
`generated` when its frames' codes equal its own anchors, which is what a generated board is.

---

## 3 · The anchor instruction conflicts with the 304 frames already counted

§4 requires anchors "verbatim and upper-case — `id="BO-096"`". **Every one of the 304 existing
Claude Design frames uses lower-case** — `id="bo-001" data-screen-label="BO-001"` — and they
count correctly today because the indexer upper-cases what it matches (`a.upper()`).

So the requirement is either unnecessary or a second convention: enforce it and 304 frames are
non-conforming; state it as written and the next drop's boards will not match its predecessors.
**Say "the screen id, case-insensitive — `id="bo-096"` or `id="BO-096"`, and never a board label
like `seat-2a`"** — the real requirement is *the id rather than the label*, which is exactly what
the 441 board-derived codes on the client packs got wrong.

---

## 4 · `BP-001` is **337**, not 335

335 was right when the 8 September zip was cut. `searchField` has since been added to `ADM-240`
and `CMS-044` — the last two screens carrying `split` + `dataTable` + `detailPanel` without it,
and the two `pattern-data.js` said would match BP-001 once BP-010 folded. **Zero screens now carry
the signature without a search field**, so the number the regeneration must produce is 337.

---

## On §6 — does P08's assembly routing count as drawn?

It is two populations, and they should not share a number. Of P08's 294 undrawn:

- **230 are routed to a drawn pattern frame** — `BP-001` 125, `BP-002` 58, `BP-003` 38,
  `BP-006-P` 6, `BP-006` 3. A drawn frame exists for the pattern; the work is instantiating it.
- **64 have no drawing and no pattern.** That is the genuine P08 design queue.

The index is right not to call routing a frame. But `drawn` / `patternRouted` / `neither`, with
the pattern id on the routed ones, stops the next reader either inflating coverage by counting
routing as drawing or calling 294 undrawn when 64 are the real queue.

---

## Everything else in the brief checks out

The schema split, `additionalProperties: false`, the six declared keys, `publishGate` at ERROR on
34 screens, `emptyNoEvents` on 11, the `relinquish*` rename, `generatedPack` → `fromClientPack`,
the two-board-universe explanation for Marketing Board 1, and `BO-096`'s `template: calendar`
passing silently because nothing validates the template field — all confirmed against the source.

The `PTR-010` correction is accepted and is the better fix: six authoring operations removed from
a reseller's cart, five reads kept, so it is no longer a gate at all. Real gates are **34**, all
declared, none missing.

---

## 7 · Correction to §1 — the tranche is 96

**My 88 was wrong.** Ten pack frames are claimed by two screens each, and I credited both. One
frame is one drawing: it draws the screen whose title it carries. Corrected — `pack-frames.json`
now holds **123**, one per frame.

| | |
|---|---|
| Frames on client packs | 123 |
| Screens drawn on them | **123** (was 133) |
| Drawn here | 304 · overlap 25 |
| **Drawn by either** | **402** |
| **No drawn frame** | **689** |
| **Wave 1+2 tranche** | **96** (w1 47 · w2 49) |

### The index's 104 is right for a reason that hides a swap

Fixing the regex and the classifier moved nothing, as reported — but not because nothing was
wrong. On **7 of the 10 shared frames the wrong claimant is stamped**, so the index has seven
screens drawn that are not, and seven drawn screens counted undrawn. The frame title settles each:

| Frame | Title | Draws | Stamped |
|---|---|---|---|
| `fnb-4a` | Restaurant Service Command Center | **EMP-051** | EMP-058 |
| `fnb-4c` | Table & Seating Configuration | **EMP-053** | EMP-060 |
| `fnb-4d` | Reservation Calendar & Timeline | **EMP-054** | EMP-061 |
| `fnb-4f` | Walk-In & Waitlist Management | **EMP-056** | EMP-063 |
| `fnb-4g` | Guest Profile & Dining History | **EMP-057** | EMP-064 |
| `ret-4f` | Stock Count & Cycle Count Management | **EMP-066** | BO-079 |
| `ret-4j` | Barcode, RFID, Serialized Stock & Traceability | **EMP-069** | BO-114 |

`pos-2b`, `pos-2d` and `ret-5g` are stamped correctly. **Net effect on Wave 1+2 is zero, which is
why both defect fixes moved nothing — it is a swap, not a recovery.** But the membership is wrong
in 14 places, and `BO-079` is Wave 1 while `EMP-066` is Wave 2, so even the per-wave split shifts.

### The remaining 8 need no delivery

96 vs 104 is exactly eight screens, and every one is provable in the repo today:

`BO-015` `BO-016` `BO-019` `BO-053` `BO-093` `BO-094` `EMP-070` `POS-007`

```
screens/P08-venue-back-office.yaml  BO-015  board: wireframes/Seat Board 2.dc.html#seat-2a
wireframes/Seat Board 2.dc.html:37  <div id="seat-2a" data-screen-label="SEAT-2A"
                                         data-screen-id="SEAT-2A" data-screen-id-origin="board">
```

**The frame exists, at exactly the anchor `wireframe.board` names.** Seven of the eight carry
`data-screen-id-origin="board"` — the packagers' own flag for *this code is ours, not the
package's*, set because the link map marked the frame unlinked. `POS-007` is different again:
`pos-2f` already carries the correct code and is excluded only because its board is classed
`unrecognised`.

**So the fix is not a delivery — it is one rule.** Honour `wireframe.board`: if a screen names a
board and an anchor, and that anchor exists in that file, the screen is framed on it. The board
need not re-declare the id. That is the package's own claim about its own frames, checkable with
the two greps above, and it needs nothing from `sources/old-boards/` — which is mine and
correctly not in the repo.

Under that rule: **96**, with the code attribute used only to catch the seven mis-stamps above.
