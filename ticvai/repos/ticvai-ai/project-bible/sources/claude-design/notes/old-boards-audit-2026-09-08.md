# Audit — the older board set, merge readiness

**8 September 2026.** Uploaded set: `Updating old wireframes (2)`, packaged 31 August, 65 pack
boards, 552 frames. Copied to `sources/old-boards/` so the checks re-run.

## Verdict

**Mergeable, with seven corrections.** Every anchor the package declares resolves — 0 missing
files, 0 missing anchors. The only defects are in the `data-screen-id` codes, and they came from
one stamping pass, not from the boards themselves.

| | |
|---|---|
| Pack anchors the package declares | **133** |
| Resolve to the right frame, code agrees | **113** |
| Resolve, code still board-derived (safe to stamp) | **10** |
| Resolve, code claims a **different screen** | **10** |
| Missing file or missing anchor | **0** |

## Where the codes come from

`data-screen-id` exists in exactly one place: `adam/ticvai/wireframes/`, and this upload is
identical to it. **Every older copy carries `data-screen-label` only** — `Updating old
wireframes/`, `FnB Package/`, `POS Package/`, `Retail Package/`, `TICVAI Full Package/`,
`TICVAI Handoff/boards/`, `TICVAI Handoff v2/boards/` have no `data-screen-id` at all. So the ten
conflicts are not a disagreement between two board generations; they are one stamping pass, and
the README says how it worked: 113 codes from the package link map, 441 derived from the board's
own label.

## The ten conflicts, settled on frame titles

The frame's own title is the evidence — it is on the face of the frame and predates both codes.

### Seven where the stamped code is wrong — correct the board

`FnB Board 4` is a contiguous run stamped **+7 out**, which is a systematic slip, not seven
judgements:

| Anchor | Frame title | Correct to | Stamped |
|---|---|---|---|
| `fnb-4a` | Restaurant Service Command Center | **EMP-051** | EMP-058 |
| `fnb-4c` | Table & Seating Configuration | **EMP-053** | EMP-060 |
| `fnb-4d` | Reservation Calendar & Timeline | **EMP-054** | EMP-061 |
| `fnb-4f` | Walk-In & Waitlist Management | **EMP-056** | EMP-063 |
| `fnb-4g` | Guest Profile & Dining History | **EMP-057** | EMP-064 |
| `ret-4f` | Stock Count & Cycle Count Management | **EMP-066** | BO-079 |
| `ret-4j` | Barcode, RFID, Serialized Stock & Traceability | **EMP-069** | BO-114 |

In all seven the package name matches the frame title **exactly**. The two Retail ones also
crossed platform — `EMP-066` stamped as `BO-079 Stock Count`, which is a shorter title that a
loose match would prefer.

### Three where the package's link map is wrong — correct the package

| Anchor | Frame title | Package says | Frame actually draws |
|---|---|---|---|
| `pos-2b` | Till Configuration | POS-011 Returns, Refunds & Exchanges | **POS-016** |
| `pos-2d` | Cash In / Cash Out Operations | POS-013 Mobile POS, Event Sales & Offline | **POS-017** |
| `ret-5g` | Omnichannel Commerce & Journey Configuration | BO-013 Channel & Distribution | **BO-120** |

So `POS-011`, `POS-013` and `BO-013` have a `wireframe.board` pointing at a frame that draws
something else. Those three are undrawn, and their `board:` ref is currently a false positive in
any coverage count taken from the package side.

## Ten safe to stamp

Anchor correct, code still board-derived. No judgement needed:

`BO-015` `BO-016` `BO-019` `BO-053` `BO-093` `BO-094` `POS-004` `PTR-009` `EMP-070` `CMS-001`

## Not audited

The 441 board-derived codes outside the 133 declared anchors. The README is explicit that those
are the packagers' own codes for frames the link map marks unlinked, and its own title-matching
test returned one match and a false positive across all 558 frames. **They need real codes from
the package side; title matching will not close them** — the seven corrections above are what
title matching looks like when it goes wrong.

---

# Corrected again — there were never ten conflicts

**Applied to `sources/old-boards/`** — 17 frames in 8 files: the 7 corrections and the 10 stamps,
all matched exactly, none failed. `data-screen-id-origin="board"` dropped on the 10.

**Tally against `adam/ticvai/wireframes/`:** 552 frames compared, **535 identical, 17 differ** —
precisely the 17 applied. Your local copy is now 17 frames behind; the patch list is the two
tables above. Nothing else in either copy diverges.

## Pack coverage, recounted from the boards rather than the package

The boards are now the authority for what a pack frame draws, so coverage is counted from their
own `data-screen-id`:

| | Was | Now |
|---|---|---|
| Pack-framed screens | 133 (package refs) | **123** (board-declared) |
| Duplicate claims | — | **0** |

The ten lost are the ten conflicts, and losing them is the point: seven were counted against the
wrong screen (`BO-079`, `BO-114`, `EMP-058`, `EMP-060`, `EMP-061`, `EMP-063`, `EMP-064` were
never drawn — their frames belong to `EMP-051/053/054/056/057/066/069`, which were already
counted), and three (`POS-011`, `POS-013`, `BO-013`) had a `board:` ref pointing at a frame that
draws something else. **All ten were false positives in the old coverage number.**

## What that does to the totals

| | Before | After |
|---|---|---|
| Drawn somewhere | 999 | **991** |
| here only | 276 | **278** |
| repo only | 695 | **687** |
| both | 28 | **26** |
| Nowhere drawn | 92 | **100** |

Eight screens moved from *drawn* to *undrawn* because the frame credited to them draws another
screen. `TICVAI Boards v2.dc.html` is a real board holding `POS-001` and `POS-007`, not an index —
worth noting because its name invites exactly the exclusion that would lose them.


## The reason they dropped, found in the local files

**All ten "conflicts" are the ten pack anchors claimed by two screens.** 133 screens point at
**123 distinct pack frames**, and a single `data-screen-id` can name only one of them — so the
31 August stamping pass had to choose, and the choice looked like an error from either side.
Not one of the ten is a mistake:

| Frame | Claimed by |
|---|---|
| `POS Frontline Board 2#pos-2b` | POS-011 + POS-016 |
| `POS Frontline Board 2#pos-2d` | POS-013 + POS-017 |
| `FnB Board 4#fnb-4a` | EMP-051 + EMP-058 |
| `FnB Board 4#fnb-4c` | EMP-053 + EMP-060 |
| `FnB Board 4#fnb-4d` | EMP-054 + EMP-061 |
| `FnB Board 4#fnb-4f` | EMP-056 + EMP-063 |
| `FnB Board 4#fnb-4g` | EMP-057 + EMP-064 |
| `Retail Board 4#ret-4f` | EMP-066 + BO-079 |
| `Retail Board 4#ret-4j` | EMP-069 + BO-114 |
| `Retail Board 5#ret-5g` | BO-013 + BO-120 |

The pairs are asymmetric, which is what made one side look authoritative. `POS-011` carries
`source: Claude Design POS pack` and a note — *"the pack's frame is the specification; it carries
operations, states, entry params and exits"* — while `POS-016` carries only a
`generatedFallback`. `POS-013`'s note goes further: *"Drawn as POS-2D, POS-2E"*, one screen
across two frames. **The documented claimant is the one the stamp dropped**, so my seven
"corrections" swapped one legitimate claim for another and my three "package errors" were not
errors.

Workshop anchors, checked the same way: **zero double claims** across 590. This is a client-pack
phenomenon only — a pack frame drawn once and mapped to more than one package screen.

## Fixed at the model, not the codes

`data-screen-id` cannot express a many-to-one relation, so **every pack frame now carries
`data-screen-ids`** — a space-separated list of every screen that claims it. 123 frames
restamped across 30 files, 0 failures. Shared frames read
`data-screen-ids="EMP-051 EMP-058"`; the other 113 carry a single id in the same attribute, so
there is one shape to parse and nothing to special-case.

The ten stamps from the previous pass stand — those frames had exactly one claimant.

## Totals, settled

| | |
|---|---|
| Pack-framed screens | **133** across **123** frames |
| Duplicate claims silently dropped | **0** |
| Drawn somewhere | **999** |
| Generated only | **92** |
| here only · pack only · workshop only | 276 · 106 · 589 |
| here + pack · here + workshop | 27 · 1 |

`tracker-data.js` now carries a `drawnSomewhere` bitmask per screen (1 here, 2 pack,
4 workshop), so the number is derived from the three sources rather than restated, and the
tracker filters on it directly.

---

# Reply to `wireframes/board-index.json`

The index's structure is right — provenance per board, hash-keyed records, and refusing to count
a generated frame as a drawing. **Three of its numbers are short, from a cause this project
already fixed.**

## clientPack is 133, not 111

| | Index | Measured |
|---|---|---|
| Client-pack screens | 111 | **133** across **123** frames |
| Drawn by either | 394 | **410** |
| No drawn frame anywhere | 697 | **681** |
| Design ∩ client overlap | 21 | **27** |

**The shortfall is 22, and it is three known causes:**

1. **10 second claimants.** Ten pack frames are claimed by *two* package screens each —
   `pos-2b` ← POS-011 + POS-016, `fnb-4a` ← EMP-051 + EMP-058, `ret-5g` ← BO-013 + BO-120,
   and seven more. A single `data-screen-id` cannot hold two, so the 31 August stamping pass
   dropped one claimant per frame — always the documented one, since `POS-011` carries
   `source: Claude Design POS pack` and a note while `POS-016` carries only a
   `generatedFallback`. **Any scan reading `data-screen-id` inherits that loss.**
2. **10 frames the stamp never coded.** Their anchors are correct in the package
   (`BO-015`, `BO-016`, `BO-019`, `BO-053`, `BO-093`, `BO-094`, `POS-004`, `PTR-009`,
   `EMP-070`, `CMS-001`) but the frames carried board-derived codes, so a scan sees
   `SEAT-2A` where the package says `BO-015`.
3. **2 in `TICVAI Boards v2.dc.html`** — `POS-001` and `POS-007`. It is a real board holding
   frames, not an index. I lost the same two by excluding it on its name; if the index classes it
   as an index board rather than clientPack, that is the third cause.

**Fixed at the model, not the codes.** Every pack frame in `sources/old-boards/` now carries
**`data-screen-ids`** — space-separated, every claimant listed, one shape to parse:
`data-screen-ids="EMP-051 EMP-058"`. 123 frames restamped, 0 failures. Re-run `index-boards.py`
against that attribute and clientPack comes out at 133 without special-casing.

Worth noting the **984 screens framed on more than one board** is the same phenomenon seen from
the other direction, and confirms the dedupe is load-bearing.

## Your first question — P05: **yes, covered. 14 unconditionally, 3 pending a relabel.**

All 17 sit on `Kiosk Board 1` and `Kiosk Board 2`, every one with a real package code, single
claimant, none derived. These are drawings, not generated boxes — so the absence of a Claude
Design board for P05 is not a gap, it is work the client already did.

**The condition:** the packagers' own README flags `KSK-015/016/017` — their boards order them
*Order Food, Shop, Assistant* against the package CSV's *Assistant, Order Food, Shop*. Same three
screens, different codes. So three of the 17 resolve to the wrong frame until the package
relabels. **No redraw either way** — it is a label fix, and the README says the package side
should make it.

## Your second question — P08: **neither. It is two populations, 230 and 64.**

Of P08's undrawn screens, **230 carry a drawn pattern frame and 64 carry nothing**:

| Pattern | Undrawn screens routed to it |
|---|---|
| `BP-001` | 125 |
| `BP-002` | 58 |
| `BP-003` | 38 |
| `BP-006-P` | 6 |
| `BP-006` | 3 |
| **no pattern at all** | **64** |

**The index is right not to count assembly routing as a frame** — a routed screen has no frame of
its own, and `BP-001` at 337 screens on two worked examples is exactly the thin-evidence problem
the pattern boards were built to name. But the two populations need different work and should not
share a number:

- **230 are assembly.** A drawn frame exists for the pattern; the work is instantiating it, not
  designing. This is the population `P08 Assembly Board` was built for.
- **64 are the genuine P08 design queue.** No drawing, no pattern, nothing to assemble against.

**Recommend the index carry three states rather than a boolean** — `drawn` /
`patternRouted` / `neither` — with the pattern id on the routed ones. Otherwise the next reader
either inflates coverage by counting routing as drawing, or inflates the gap by calling 294
undrawn when 64 of them are the actual queue.

## The 51 boards that frame no package screen

That is the 441 board-derived codes seen from the board side, and it cannot be closed by
matching. The packagers tested exactly that: **one match and a cross-platform false positive
across all 558 frames.** The seven bad stamps corrected above are what that failure produces when
it is trusted. Those 51 boards need codes issued package-side; nothing in the boards themselves
can supply them.

## Where the 111 actually comes from — the regex matches the wrong attribute

`ANCHOR = re.compile(r'id="([A-Za-z]{2,4}-\d{2,4})"')` has no boundary before `id="`, so it also
matches the tail of **`data-screen-id="BO-045"`**. On the client packs that is the only thing it
matches: their real anchors are `fnb-2a`, `ret-2c`, `seat-1b`, which fail `\d{2,4}` — one digit
then a letter.

Measured: applying the indexer's own rule to the pack boards' **anchors** yields **22** screens
(the `KSK-001`-style Kiosk and Dashboards boards). It reports 111. **The other 89 come from
`data-screen-id`, read by accident.** On Claude Design's 22 boards the rule is correct for a
different reason — those anchors really are `id="bo-001"` — which is why 304 is right.

So `screensOnClientPacks: 111` is exactly the 31 August stamp count, and it inherits precisely
the stamp's three losses: 10 second claimants + 10 board-derived codes + `POS-001`/`POS-007` in
`TICVAI Boards v2.dc.html`, which `classify()` sends to **`generated`** on
`name.startswith("TICVAI")`. **111 + 10 + 10 + 2 = 133.** Fully reconciled.

### Two consequences

1. **`data-screen-ids` will not match.** `ids="…"` is not `id="…"`, so the moment the restamped
   boards land, clientPack drops from 111 to **22** — and the hash reuse means it happens board by
   board as each one changes, which is the hardest version of that bug to spot.
2. **`TICVAI Boards v2.dc.html` is misclassified.** It is a client pack board holding real frames;
   the `startswith("TICVAI")` test files it as generated, so its screens are excluded from the
   drawn count by construction.

### The fix, both at once

Read the attribute you mean, and split it:

```python
CODES = re.compile(r'\bdata-screen-ids?="([^"]+)"')   # plural first, both shapes
ANCHOR = re.compile(r'\sid="([^"]+)"')                # real anchors, for href checking
# per frame: codes = CODES.findall(text) → [c for v in codes for c in v.split()]
```

and classify on content rather than filename — a board is `generated` if its frames' codes equal
its own anchors, which is what a generated board *is*. Failing that, exclude `Boards v2` from the
`TICVAI` prefix test explicitly.

With both, clientPack = **133**, drawn by either = **410**, no drawn frame = **681**, overlap = **27**.
