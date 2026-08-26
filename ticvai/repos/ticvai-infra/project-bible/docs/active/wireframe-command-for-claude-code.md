# Wireframes — the brief to hand Claude Code

Paste the block below. It replaces `viewer-command-for-claude-code.md` as the current handover;
the viewer briefs still stand for viewer work and are named in it.

---

## The command

> You are drawing wireframe boards for TICVAI. The design package is at the repo root: 477 screens
> across 15 platforms, 1,007 operations, 378 tables, 33 flows. **Nine validators must pass before
> and after anything you do** — run `bash tools/refresh.sh` and read the last nine lines.
>
> **Read `wireframes/README.md` and `docs/active/board-placement-strategy.md` first.** They carry
> the reasoning; this carries the instruction.
>
> ### What already exists
>
> **Three client packs are installed and mapped**: F&B (62 frames), POS (36), Retail (58).
> **156 frames, every one owned by exactly one screen**, recorded in `screen.boardFrames`. Do not
> redraw those — they are hi-fi, client-authored, and better specified than anything derived from a
> screen file.
>
> **Everything else is generated** by `tools/derive-wireframes.py` from the screen definitions.
> 385 screens, one board per platform, wired into `refresh.sh`.
>
> **The generator skips any screen whose `wireframe.board` points at a pack** —
> `wireframes/FnB…`, `wireframes/POS…`, `wireframes/Retail…`, `wireframes/TICVAI Boards v2…`.
> **Checked per screen, not per platform**, because P08 alone answers frames in three packs and
> holds a hundred screens in none.
>
> ### Your job, in order
>
> **1 — Improve the generated boards, not the packs.** Five platforms have no client pack at all
> and never will: P01 guest web (35), P02 guest app (63), P09 platform console (37), P10 partner
> (21), P13 CMS (20). **These are the boards a reviewer actually opens for those platforms**, and
> they are currently a wireframe generated from YAML.
>
> Read `wireframes/P07 Venue Scanner.dc.html` first — 11 screens, the smallest complete board, and
> the pattern the generator follows.
>
> **2 — Match the packs' fidelity where it matters, and only there.** The client packs are
> 1280×700 dashboards with real figures. **Do not try to reach that everywhere** — a wireframe
> that looks designed invites comment on the design, and a board of 63 guest screens is for
> checking that the right things are on the right screens.
>
> **What must be on every frame, and is already:** every declared state including `offline`, the
> component `notes` (they carry the reasoning), `OPERATIONS`, `ARRIVES WITH`, `GOES TO`, and the
> `named only` tag on screens a client listed but never specified.
>
> **3 — Do not invent.** A screen with no operations renders `OPERATIONS · none declared`.
> **That gap is real and should be visible** — thirteen screens are in that state and each one is a
> question somebody has to answer.
>
> ### Rules that are not negotiable
>
> **Never hand-edit a generated board.** They are written by `tools/derive-wireframes.py` and
> overwritten on every `refresh.sh`. Change the generator or change the screen.
>
> **Never edit anything under `repos/`.** Those are mirrors, `tools/derive-mirrors.py` writes them,
> and `check-package` fails on drift. **A file edited there is a file overwritten on the next
> refresh** — which is exactly how a state model spent two days anchored on an object with no
> values.
>
> **Never repoint a screen away from a pack.** If a screen's board starts with a pack prefix, the
> client drew it. Adding a generated version alongside is how 96 duplicate board files appeared in
> six mirrors on 20 August.
>
> **Run `bash tools/refresh.sh` after every change** and confirm nine PASS lines. `check-wireframes`
> resolves every anchor in both directions — a board drawing a screen that does not exist fails,
> and a screen naming an anchor that is not there fails.
>
> ### When a new pack arrives
>
> Three more are expected: Inventory & Procurement, Marketing & CRM, Seat Management & Venue
> Mapping. For each:
>
> 1. Copy the `.dc.html` files, `support.js` and `assets/` into `wireframes/`
> 2. Extract each frame's `data-screen-label` and its four traceability lines
> 3. **Check every operation the frames name against `handoff/board-operation-aliases.json`
>    before believing any of them are missing.** That file has 358 entries and **over 90% of what
>    three packs named already existed under a different word** — `scanItem` is `lookupMerchandise`,
>    `holdSupplier` is a status on `updateSupplier`, `completeSale` is `createRetailSale`.
> 4. Assign each frame to an owning screen **by board purpose, by hand.** Do not derive it —
>    three attempts produced plausible nonsense, the best of them matching *Outlet Management* to
>    *Kitchen Operations Command Center* on one shared operation out of four. **A reader who trusts
>    a bad table is worse off than one who has none.**
> 5. Set `screen.boardFrames` and repoint `screen.wireframe.board` at the pack anchor

---

## What not to ask it to do

**Do not ask it to redraw a client pack.** They are the specification for the screens they cover.

**Do not ask it to fix the numbers it sees.** 650 screen warnings, 385 screens on generated boards,
13 screens with no operations — **those are the package's gaps, not the boards', and a board that
hides them is worse than one that shows them.**

**Do not ask it to reconcile a frame to more than one screen.** Every frame owns exactly one, and
some screens own frames in two packs — `BO-044 F&B Outlets` answers nine F&B frames and nine Retail
frames, because **a venue configuring an outlet and a venue configuring a store are the same screen
with a different module licensed.** That is the module system working, not a duplication.

---

## Still current from the viewer briefs

`docs/active/viewer-redesign-brief.md` and `docs/active/viewer-update-brief-20aug.md` describe the
viewer, which reads this package and renders it as five layers. **They are unchanged and still
apply** — the boards and the viewer are separate work, and the viewer's Decisions layer is still
the highest-value thing in it.
