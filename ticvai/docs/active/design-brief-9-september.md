# Design brief — 9 September 2026

**For Claude Design. The 1,091 screens are stable and 104 of them are the next thing to draw.**

This replaces the 8 September handoff. Read it before starting: five things changed underneath the
last drop, and two of the figures in that drop are wrong in ways that would waste a day.

---

## 1 · The number, and why it is 89

`wireframes/undrawn.json` is the file to work from. **The count moved from 104 to 89 on
9 September, and every one of the fifteen was your finding.** See §3 — the reconciliation is worth
reading, because the rule that produced it is now the rule.

| Wave | Undrawn | |
|---|---|---|
| 1 | 46 | |
| 2 | 43 | |
| **1 + 2** | **89** | **start here** |
| 3 | 593 | not yet — see §5 |
| **Total** | **682** | of 1,091 |

| Platform | Screens | Drawn | Undrawn | W1 | W2 | W3 |
|---|---|---|---|---|---|---|
| `P08` Venue Management — Back Office | 363 | 68 | **295** | 36 | 35 | 224 |
| `P09` TICVAI Web — Platform Console | 318 | 38 | **280** | 1 | — | 279 |
| `P13` Venue CMS — White Label | 60 | 20 | 40 | — | — | 40 |
| `P10` Partner Web — Reseller Portal | 51 | 21 | 30 | — | — | 30 |
| `P12` Venue Support — Agent Console | 28 | 8 | 20 | — | — | 20 |
| `P02` Guest App — Mobile | 71 | 54 | 17 | 9 | 8 | — |

**Nine platforms are finished** — `P01`, `P04`, `P05`, `P06`, `P07`, `P11`, `P14`, `P15`, `P16`.
`P04` and `P06` joined that list on 9 September and **you were right about both**; this brief said
otherwise until the reconciliation. `P08`'s 71 Wave 1–2 screens are four fifths of the tranche and
are the job.

**Nothing in the 89 is blocked, and that is a number rather than a claim: zero of them carry an
open question.** `openQuestions` was holding three things and read as 74 open items when 24 were
open. **41 were pre-contract residue**, all `P02`, all the same sentence: *"Inventory cites
`GET /tickets` — no matching operation. Written before the contracts existed."* The operation
exists; it is not called `GET /tickets`. Deleted. **Nine were answers** — `BO-006` from the
14 August minute, eight `P11` screens from the 7 September workshop — and moved to
`resolvedQuestions` rather than deleted, because losing which minute settled a thing is how it gets
asked again. The 24 that remain are open, and **not one is on a Wave 1 or 2 undrawn screen.**

---

## 2 · Five things changed under the last drop

**Re-read `screens/_schema.yaml` before writing any `wireframe` block.** It is enforced now; until
8 September it was documentation nothing read.

**(a) `wireframe.status` split in two, and the last drop's values are no longer legal.**
`status` was carrying intent and fact at once. It is now:

  `status` — `notStarted` · `inProgress` · `review` · `approved`. Workflow only. Hand-set.
  `provenance` — `generated` · `designed`. **How the frame came to exist.**

`status: designed` from the last drop is now `provenance: designed`, `status: notStarted`. All
1,091 were migrated (958 generated / 133 designed preserved). **A drawn screen is
`provenance: designed`** — that is the field the coverage count reads.

**(b) The `wireframe` block is `additionalProperties: false`.** Six keys that were in use and
undeclared are now declared — `board`, `workshopBoard`, `generatedFallback`, `derivedFrom`,
`source`, `note`. **Any key not on that list now fails.** There is no `origin` field; if the last
drop assumed one, that is where the confusion came from.

**(c) `publishGate` is a component and its rule is at ERROR level.** A screen whose title or
operations promise a publication declares it. 34 screens carry it. **A new one that publishes and
omits it fails the build** — this is not a warning any more.

**(d) `emptyNoEvents` is a distinct screen state,** on the 11 screens where *nothing is scheduled*
and *nothing matched your filter* are different sentences and only one of them is the user's fault.

**(e) Boards moved and are now indexed.** Yours live in `wireframes/claude-design/` — 22 boards
and four data files, moved there on 8 September. Notes stayed in `sources/claude-design/notes/`.

Also: seven `release*` operations became `relinquish*` (releasing a *hold* and releasing *to the
public* were the same word), and `_id-register.yaml`'s `generatedPack` became `fromClientPack`
(it meant *the client drew it*, the opposite of `provenance: generated`).

**(f) Four more schema changes, 9 September — all of them affect what you write.**

  **`provenance` at screen level is now `sourceNote`.** It held prose (*"client board,
  specified"*) against `wireframe.provenance`'s enum, on 128 screens that carried both. **Third
  instance of one word doing two jobs** after `release` and `generatedPack`. `wireframe.provenance`
  is unchanged — that is still the field you set to `designed`.

  **`resolvedQuestions` is a new field**, holding an answered question with its answer.

  **`calendar` is a legal `layout.template`.** `BO-096 Resource Calendar` had declared it since
  August and passed every check because nothing read the enum. **You reported this as a CI
  failure; it was the opposite — a rule that did not exist.** The rule exists now and is at ERROR
  level, so a template outside the ten-plus-`calendar` list fails the build.

  **`duplicateMatch` is a new component, and the merge flow is now on two screens.**
  `EMP-055 Create / Edit Reservation` and `EMP-057 Guest Profile & Dining History` declare
  `matchGuest` and `mergeGuests` for the first time — the process was drawn on `FnB Board 4` and
  written into the contracts, and no screen referenced it. **Both screens already pointed at those
  exact frames.** Draw the proposal as candidates with the reason each one matched, never a bare
  score, and the merge itself as a `confirmDialog` stating that the losing record is superseded
  rather than deleted, that it is reversible for thirty days, and that consent takes the narrower
  of the two positions.

  **Ten screen-level keys are declared for the first time** — `source`, `sourceNote`,
  `implementation`, `density`, `densityReason`, `statesDerived`, `boardFrames`, `offline`,
  `audience`, `resolvedQuestions`. The schema described 18 of the 28 keys a screen actually
  holds. It describes all 28 now.

---

## 3 · The reconciliation — 104 against 96, settled at 89

**Both counts were wrong and each was wrong in a way the other could see.**

**Coverage was being counted from stamps.** A frame carries `<div id="pos-2f"
data-screen-label="POS-2F" data-screen-id="POS-007">`, and `index-boards.py` read the stamp.
**Ten client-pack frames carry a real anchor, a real title and no stamp at all** — `Seat Board
2.dc.html#seat-2a` is `BO-015` and the board never says so. All ten read as undrawn. Your side read
the screen's own `wireframe.board`, which names them.

**But a declaration is a claim.** Taking `wireframe.board` at face value counts a frame nobody
checked. **So the rule is now both: the claim is honoured where the board really has that anchor.**
Stronger than either input, and it is what closed the gap.

**Eighteen frames are claimed by two screens.** Counting both inflates by 22; dropping both hides
real drawings. **The frame's own title settles all eighteen** — `fnb-4a` is titled *Restaurant
Service Command Center*, which is `EMP-051`, while the frame is stamped `EMP-058`. Your seven
mis-stamps were the visible part of a set of eighteen, and **you were right on all seven**: the
title matched the screen you named, never the one stamped. The drawing is the evidence; the stamp
is an assertion about it. `board-index.json` now carries `contestedFrames` with the adjudication.

**`TICVAI Boards v2.dc.html` was being classified as a generated board** because its filename
starts with `TICVAI`. `derive-wireframes.py` writes `P## <name>.dc.html` and one index, nothing
else. It is a client board and holds `POS-001` and `POS-007`.

**Where we still differ: 144 pack-drawn against your 123.** Your `pack-frames.json` is
one-frame-one-screen; the index counts a screen drawn if any verified frame depicts it, and a
screen can appear on several. Neither is wrong — they answer different questions — but the tranche
is the same shape either way, and **89 is what the repo can now defend, by a rule written down in
`index-boards.py` and reproducible from a clean checkout.**

**The restamped packs were not needed**, exactly as your README predicted. Nothing from
`optional-restamped-client-packs/` was taken in.

### Three figures from the earlier drop

**`BP-001` is 337.** This brief first said 335, already stale: `ADM-240` and `CMS-044` gained
`searchField` in the 8 September patch. Your regeneration to 337 across 12 groups stands.

**`Marketing Board 1.dc.html` was not "never built".** It is in `wireframes/`, 149 KB, 3 September.
**There are two board universes** — your set is 22, the repository holds 170, zero filename
overlap. Check against `wireframes/board-index.json`, which covers all 170.

**`BO-096 Resource Calendar` did not fail CI** — `template: calendar` was outside the enum and
**nothing read the enum.** You reported a CI failure; it was a rule that did not exist. It exists
now, at ERROR level, and `calendar` is legal, because the screen renders a `timeline` of resource
availability and none of the other ten templates express a scheduling grid.

One correction the other way: **`PTR-010` was not an uncertain match.** It declared
`publishPromotion` outright. The defect underneath was larger — a partner reseller's cart screen
could create, publish, pause, end and unschedule promotions. Six authoring operations removed.

---

## 4 · What to produce, and how to hand it back

For each screen drawn:

  the **board file and anchor**, as `<board file>#<anchor>`, for `wireframe.board`
  `wireframe.provenance: designed`
  `wireframe.status` — `inProgress` or `review`, whichever is true

**The screen id goes in `data-screen-id`, and it is not the `id` attribute.** The boards already
carry three attributes per frame and this brief originally named the wrong one:

```
<div id="pos-2f" data-screen-label="POS-2F" data-screen-id="POS-007">
```

`id` is a lowercase label slug, `data-screen-label` is the human label, and **`data-screen-id` is
the package screen id** — upper-case, matching `screens/P*.yaml` exactly. Keep all three.
`board-index.json` reads `data-screen-id`; a frame that carries only a label is invisible to every
count in the package, which is how the first drawn-screen figure came out as 1,091 instead of 304.

New boards go in `wireframes/claude-design/`. Re-run `python3 tools/index-boards.py` after a drop —
it is hash-keyed, so unchanged boards are not re-read, and it will print the new coverage.

**Report anything in `screens/P*.yaml` that is wrong.** Four of the five defects found this week
came from reading the screens against something else, which is what drawing them is. In particular:
an operation that has no business on the screen declaring it. `BO-001`, `BO-002` and `BO-005` are
already known — `BO-005 Queue Monitor` is 63% campaign management, including `launchCampaign` and
`stopCampaign`, on a queue screen.

---

## 5 · What not to do

**Do not edit `screens/`, `contracts/`, `states/`, `flows/`, `events/`, `handoff/`, `diagrams/`,
`services/` or `repos/*/project-bible/`.** The last seven are derived — `tools/refresh.sh` rewrites
them and hand edits vanish silently. Propose screen changes; do not apply them.

**Do not touch `.dc.html` files at the top level of `wireframes/`.** 16 are regenerated from the
screen YAML on every refresh and 70 are client packs that are evidence — the only class in the
package that is a design decision rather than a restatement of it. Yours are the only ones to edit.

**Do not start Wave 3.** It is 593 of the 697 and `P09`'s 279 are all Wave 3 Commercial. Wave is
the delivery schedule; drawing Wave 3 first is 85% of the work against 0% of the next milestone.

**Do not invent operations.** A screen calls what its `apis` block declares. If a frame needs
something that is not there, that is a finding to report, not a frame to draw around.

---

## 6 · One thing only Chinmay can settle

**Does `P08`'s assembly-board routing count as drawn?** `P08 Assembly Board.dc.html` routes to P08
screens without framing them individually. `board-index.json` counts frames and therefore counts
them undrawn, which is why P08 reads 301. If the routing counts, P08's undrawn number falls
sharply and the 104 falls with it. **The index does not decide this deliberately** — it is a
judgement about what *drawn* means, and it changes the size of the job.
