# The 19 September regeneration — what ran, what changed, what is left

> **Owner:** Chinmay · **Run:** 19 September 2026 · **Status:** in progress — placed, wired and
> flowed; generation and batching not yet run
>
> Governed by [source-precedence-19-september](source-precedence-19-september.md): **MoM > boards >
> specifications, and the matrix where all three are silent.** POS (`P04`) is final and is not
> touched by any step here.

---

## Where the package stands

| | before | after |
|---|---:|---:|
| **Screens, all platforms** | 1,629 | **2,427** |
| `P08` Venue Back Office | 614 | **1,182** |
| `P09` Platform Console | 446 | **676** |
| `P04` Point of Sale | 30 | **30 — untouched** |
| Flows | 203 | **289** |
| Screens with no `entryFrom` | 851 | **90** |

**44,609 lines added across four files.** `P08` grew by 31,868 lines and `P09` by 12,722.

---

## 1 · Placement — 798 screens, not 814

```
1924 pack entries: 1076 already have a screen, 798 added, 50 covered by a filter on another screen
```

**The 16-screen difference from the parsed 814 is the step-2 triage, and it is the point of the
step.** Sixteen pack screens were folded into screens that already existed — ten of them F&B board
2, already built in full as `EMP-051`–`EMP-060` with the same titles in the same order. A further
50 are covered by `BOARD_PLACEMENT: None`, where a whole board is a filter on an analytics screen
rather than a copy of it.

`derive-pack-screens.py` adds and does not rebuild, so none of the 1,629 existing screens were
overwritten.

**`P08` passed 999 and is now at `BO-1182`.** The id pattern was widened to four digits on 19
September across all four tools that repeat it; this run is the first to actually use the range.

## 2 · The wallet supersession — five screens re-pointed

All nineteen wallet screens on `P08` came from `Game_and_Ride_Module.pdf`, because the wallet pack
had never been parsed. The wallet pack's own acceptance condition decides which survive — *"new
wallet credit types can be introduced through configuration without development changes"* — so the
line is **does this screen configure the wallet system, or operate one credit type.**

| gaming screen | now points at |
|---|---|
| `BO-415` Wallet & Credit Type Configuration | `BO-1088` Credit & Balance Type Configuration |
| `BO-417` Top-Up Configuration | `BO-1095` Top-Up Rule Configuration — matrix 4.3.30 |
| `BO-418` Top-Up Bonus Rule Configuration | `BO-1105` Credit Issuance Rule Configuration |
| `BO-420` Bonus Validity & Expiry Configuration | `BO-1108` Expiry & Validity Policy Configuration |
| `BO-399` Wallet & Credit Acceptance Mapping | `BO-1106` Credit Usage & Eligibility Rules |

**All five had zero components, so nothing rendered is lost**, and the five kept — including
`BO-414`, the hub of 19 edges — mean no navigation is re-pointed.

**One correction against the decision doc.** It recorded `BO-399` as superseded by board 2's
*Channel & Funding Source Mapping*. That is wrong on the words: **acceptance is where credit may be
spent, not where it is loaded from**, so it points at board 3's usage and eligibility rules
instead. The doc has been corrected.

## 3 · Wiring — 798 screens given navigation

`tools/applied/wire-pack-boards-19-september.py`, a dated sibling of the 11 September tool as that
one was of the original. Screen 1 of a board is its hub, the hub hangs off the platform home
screen, every other screen hangs off the hub and back, both edges labelled, provenance leading with
`structural`.

**One change from the precedent.** The 11 September sibling named its four packs in a literal. This
one selects **every pack that still holds a screen with no `entryFrom`** — 36 packs is too many to
list by hand, and a hand-written list is precisely what silently omits one. The selection is
self-limiting, and the tool is idempotent regardless.

**90 screens still have no `entryFrom`**, all of them pre-existing rather than from this run.

## 4 · Flows — 86 written, 109 skipped

`derive-board-flows.py` is idempotent on the hub rather than the filename, so the 109 skips are
boards that already had a flow. Flows went 203 → 289.

---

## What has NOT run

**Generation.** `generate-screens-from-pack.py` has not been run over the new screens. They carry
pattern, layout and states from the placement tool, which is why only **185 of 2,427** screens have
no components at all — but they have not been through the richer generation pass the regeneration
plan describes.

**Batching.** No batch has been re-exported. `handoff/design-batches/` still holds the 10–14
September set: **191 batches, 13 built** (all `P01`), and **no `P04-*` batch exists**, so POS was
already excluded from that run and stays excluded from this one.

**This is the single export and single queue that was agreed**, and it has to happen after
generation, not before — a batch cut now would be re-cut immediately.

---

## The operations gap has not moved, and that is deliberate

```
contracts define : 1,630
reached          : 1,386
reaching nothing :   244
```

**1,338 screens declare `apis: []`.** The 798 new screens added none, because
`derive-pack-screens.py` invents no operations:

> *"The 1,924 pack screens imply roughly three thousand endpoints against the ~1,032 that exist,
> and authoring three thousand endpoints from a PDF is not derivation, it is fabricating an API
> surface."*

The gap is written out as named vocabulary per board in
[workshop-contract-gap](workshop-contract-gap.md) instead. **The 244 unreached operations are the
matrix fallback** under the precedence rule — contracted, traceable to a requirement, and drawn by
nothing.

## Storage — worth knowing before the next drop

**`P08` is now 104,740 lines in one file**, ~88 lines per screen, and it is loaded whole by every
generator, checker and exporter. That is why `check-screens` and `check-wireframes` take minutes
rather than seconds.

Splitting `P08` by nav section is a storage change, not a navigation one, and it is **a different
question from the id ceiling** — that was settled by widening the pattern, because over-999 ids
spread by allocation order rather than by module. Worth taking before the next pack drop rather
than after.
