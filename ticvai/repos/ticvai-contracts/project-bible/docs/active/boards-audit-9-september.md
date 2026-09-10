# Boards audit — 9 September 2026

**170 boards, 18.6 MB, 2,105 stamped frames, against 1,091 screens.** Every figure here is
recomputed by `tools/index-boards.py` from the files themselves and recorded in
`wireframes/board-index.json`, keyed by content hash so an unchanged board is never re-read.

This supersedes the 8 September audit. **Three of its numbers were wrong** and all three came from
counting stamps instead of drawings — see §4.

---

## 1 · What is on disk

| Provenance | Boards | Stamped frames | Size | What it is |
|---|---|---|---|---|
| `clientPack` | 71 | 114 | 9.0 MB | **The client drew it.** The only class that is evidence of a design decision rather than a restatement of the package |
| `workshop` | 59 | 590 | 2.1 MB | `derive-pack-boards.py` output, ten screens per board |
| `claudeDesign` | 22 | 310 | 3.4 MB | Claude Design's own set, `wireframes/claude-design/` |
| `generated` | 16 | 1,091 | 3.0 MB | `derive-wireframes.py` output — every screen, rewritten on refresh |
| `unrecognised` | 2 | 0 | 1.0 MB | Indexes this package did not write and cannot attribute |
| **Total** | **170** | **2,105** | **18.6 MB** | |

**A frame in a `generated` board is not a drawn screen.** It is the screen's own YAML rendered as
boxes, which is why all 1,091 screens having a `wireframe.board` says nothing about coverage. The
`generated` row covering every screen is the clearest illustration: it is the package looking at
itself.

---

## 2 · Coverage

| | |
|---|---|
| Screens | 1,091 |
| **Drawn by somebody** | **409** |
| — by Claude Design | 304 |
| — on a client pack | 144 |
| — on both | 39 |
| **No drawn frame anywhere** | **682** |
| Of those, Wave 1 or 2 | **89** |

**Nine platforms are fully drawn** — `P01`, `P04`, `P05`, `P06`, `P07`, `P11`, `P14`, `P15`, `P16`.
The undrawn are concentrated in two: `P08` at 295 and `P09` at 280 are **575 of the 682**.

The Design ∩ client-pack overlap is only 39 screens, so the two sources are **complementary rather
than corroborating** — which also means neither can be used to check the other.

---

## 3 · What the client drew that the package never specified

**39 of the 71 client-pack boards cover no package screen at all — 305 drawn frames with nothing
written against them.**

| Family | Unused boards | Frames with no screen | Screens it does cover |
|---|---|---|---|
| **Seat Platform Board** | 11 | **110** | 2 |
| **Marketing Board** | 10 | **100** | 2 |
| **Inventory Board** | 6 | **60** | 1 |
| **Guest Mobile Board** | 7 | **35** | 1 |
| FnB Board | 0 | 0 | 53 |
| Retail Board | 0 | 0 | 48 |
| POS Board | 0 | 0 | 25 |
| Kiosk Board | 0 | 0 | 17 |
| Seat Board | 0 | 0 | 15 |

**The split is total, not gradual.** Five families are fully absorbed and four are almost entirely
untouched — Seat Platform covers 2 screens across 13 boards, Marketing 2 across 12. This is not a
package that drifted from its sources; it is a package that read some of them and never opened the
rest.

**This is CF-169 measured from the board side**, and larger than that entry states. It records
`seatp` at 130 screens and `crm` at 120 with no package counterpart. The frame count here is 305
because a frame is not a screen — but the shape is the same, and it is the same finding as the 26
uncited client packs in CF-171. **Three registers are describing one gap from three directions**:
operations nobody drafted, screens nobody wrote, frames nobody claimed.

---

## 4 · Three corrections to the 8 September audit

**Coverage was counted from stamps, and ten drawings carry no stamp.** A frame renders as
`<div id="pos-2f" data-screen-label="POS-2F" data-screen-id="POS-007">`. Ten client-pack frames
carry a real anchor, a real title and **no `data-screen-id` at all** — `Seat Board 2.dc.html#seat-2a`
is `BO-015` and the board never says so. All ten read as undrawn.

**The rule is now the screen's claim, verified against the board.** `wireframe.board` names the
frame; the frame must really exist at that anchor. **Stronger than either half** — a stamp can be
absent and a claim can be wrong, and this catches both.

**Eighteen frames are claimed by two screens, and the frame's own title settles all eighteen.**
`fnb-4a` is titled *Restaurant Service Command Center*, which is `EMP-051`, while the frame is
stamped `EMP-058`. **The drawing is the evidence; the stamp is an assertion about it.** Claude
Design found seven of the eighteen independently and was right on all seven. The adjudication is
in `board-index.json` under `contestedFrames`.

**`TICVAI Boards v2.dc.html` was classified `generated` because its filename starts with
`TICVAI`.** `derive-wireframes.py` writes `P## <name>.dc.html` and one index, nothing else — the
rule was a guess at the naming rather than a reading of the tool, and it swept up three files,
one of which holds hand-drawn `POS-001` and `POS-007`.

**And the fix did not take on the first run.** The index caches by content hash, and it was caching
the *classification* alongside the parse. **Provenance is a function of the tool's rules, not the
board's bytes**, so a corrected classifier ran against 170 unchanged boards and changed nothing
while reporting success. Now re-derived every run.

Net effect: undrawn moved from 697 to **682**, and the Wave 1–2 tranche from 104 to **89**.

---

## 5 · P08's assembly routing — decided

**Routing is not drawing. Decided 9 September; the routed screens stay in the undrawn list.**

Every one of P08's 363 screens carries a route to a frame a builder would work from. Of the 295
undrawn, **294 route to a frame that exists on a board somebody drew** — but to only **ten distinct
frames**, and **172 of them point at `Pattern Boards.dc.html#bp-001` alone.**

**One frame is the exemplar for 172 screens.** That is a precedent, not a design: it says *this
screen looks like that kind of screen*, which is worth having and is not a drawing of the screen.
Counting it as coverage would have reported P08 as 94% drawn when 68 of its 363 screens have a
frame of their own.

The routing is recorded rather than discarded — `undrawn.json` carries `patternFrame`, `pattern`
and `patternFrameDrawn` per screen, because **a screen with a worked example is a morning's work
and one without is a blank page**, and a single undrawn number hides which.

---

## 6 · Loose ends

**51 boards frame no package screen**, of which 44 are client packs (§3), 4 are Claude Design's
index and pattern boards, 2 are unattributable indexes, and 1 is generated.

**7 orphan frames** — anchors shaped like a screen id that no screen has: six `BP-*` pattern ids
and one `INV-*`. Harmless, but they are the residue a rename leaves.

**Two board universes still.** The repository holds 170 boards; Claude Design's set is 22, with
zero filename overlap. Of the 54 boards `board-data.js` references, 35 are in `wireframes/` and 19
in Design's set. **Checking a board reference against one directory reports two thirds of them
missing**, which is how `Marketing Board 1.dc.html` was reported as never built while sitting in
`wireframes/` at 149 KB. `board-index.json` is the only thing that covers all 170.

**The restamped client packs were not taken in.** Claude Design offered 65 boards restamped with
plural `data-screen-ids`; their own README called them *probably not needed*, and they were not —
the ten unstamped frames resolve from `wireframe.board`, and the eighteen contested ones from the
frame titles. **Nothing in the tranche depends on a board this repository does not hold.**
