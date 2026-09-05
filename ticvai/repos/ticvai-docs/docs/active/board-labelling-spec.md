# How to label a TICVAI board

**A spec for Claude Design. 31 August 2026.**

**The package owns the screen list. You draw against it.** Every screen has a reference code —
`GST-049`, `BO-134`, `SCN-003` — and a board frame that carries its code links itself. One that
does not has to be matched by hand.

**533 frames have arrived. 96 link. The 437 that do not are all missing the same attribute.**

---

## The one thing to add

```html
<section id="gm-6c"
         data-screen-label="GM-6C"
         data-screen-id="GST-049">
```

**`data-screen-id` is the package's code for the screen this frame draws.** That is the whole
change.

**Keep `data-screen-label`.** Board position is useful when reading a board on its own, and the two
answer different questions — where the frame sits, and what it draws.

**`id` stays as it is.** Lowercase, hyphenated, matching the label. It is what the anchor link
targets and it already works.

---

## It already works in two of your packs

```html
<!-- Seat Board 1 -->
data-screen-label="SEAT-1A · BO-093"

<!-- Dashboards Board -->
data-screen-label="ADM-002"
```

**Both linked in one pass with no judgement.** Both are at 100%.

**Seat Platform, Marketing, Inventory and Guest Mobile are at 0–2%** and label by position only.
**Same designer, same tooling, different attribute.**

---

## Where the codes come from

**`ticvai-screens-to-draw.csv`** — 379 screens with no board yet. Five columns:

```
screen id   platform   name                              module      operations
GST-049     P02        Seat Selection                    seating     7
BO-134      P08        Kitchen & Preparation Stations    fnb         12
SCN-003     P07        Scan & Validate                   access      9
```

**Draw against a row, put its `screen id` in `data-screen-id`.** If a frame draws something not on
the list, leave the attribute out and tell us — **it is either a screen we are missing or a view of
one we have**, and both are worth knowing.

**`ticvai-frame-link-map.csv`** — all 533 frames already delivered, with the 437 marked `UNLINKED`.
**Retrofitting those is the larger win** and does not need a redraw, only the attribute.

---

## One code per frame, not one per board

**A screen can own several frames** — `BO-044` owns eighteen, nine F&B and nine Retail, because
configuring an outlet and configuring a store are the same screen under a different licence.

**Put the same `data-screen-id` on each.** Repetition is correct; we count distinct screens, not
frames.

---

## Why the title is not enough, since we tried

**All 533 frames carry a title, and we matched titles against screen names.** 45 candidates, 29
applied, then we stopped.

**A title match crosses platforms silently.** `Outlet Management` on an F&B board matched a
partner-portal screen at 0.85. **A mapping that is wrong and confident is worse than none** — it
puts a kitchen board behind a reseller's screen and nothing complains.

**And three frames matched one screen.** `Shift & Operator Dashboard`, `Offline Operations
Dashboard` and `Venue Operations Dashboard` all resolved to `POS-015`. **Either one screen owns
three views or two belong elsewhere, and a title cannot say which.**

---

## What we check when a pack arrives

**Every frame's `id` is unique across the whole set.** 533 checked, no collisions — keep it that
way.

**Every `data-screen-id` resolves to a real screen.** One that does not is reported rather than
guessed at.

**Every cross-board `href` points at a board in the pack.** `Guest Mobile Board 5` links to
`Retail Backend Board 3`, which is not in it — one dead click, and we unwrapped it.

**Anchor scheme is consistent within a pack.** `Inventory Board 1` uses `inv-2`, `inv-3`, `inv-10`;
Boards 2–7 use `inv-2a`, `inv-3a`. **No collision today, but `inv-2` and `inv-2a` in different files
invites one.**

---

## Two smaller things

**`TICVAI Boards v2` holds six frames belonging to five other boards** — `inv-1`, `inv-6`, `fnb-1a`,
`ret-1a`, `pos-2a`, `pos-2f`. **A scratch board is where frames go to be forgotten.** Fold them in.

**The undrawn list is not evenly urgent.** `P07 Venue Scanner` is eleven screens and **it is the
gate** — the highest-consequence surface in the venue, walked by three flows, nobody has drawn it.
`P05 Guest Kiosk` is seventeen and **it is the surface with no person standing there to help.**

---

## The whole ask, in one line

**Add `data-screen-id` from `ticvai-screens-to-draw.csv` to every frame, new and existing.**

**437 links follow with no judgement from either side.**
