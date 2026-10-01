# POS

> **One working file for the whole app** (decided 30 September): `return/TICVAI POS.dc.html` in this folder. Every batch below adds its screens to that one file.

The venue's point of sale on terminal and tablet (P04), with the Kitchen Display at the pass and the stations (P15). Sells offline.

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: none.

Sections: P04

## P04 + P15: TICVAI POS: the till (P04) and the kitchen display (P15)

**What it is.** The venue's till for tickets, food and retail, and the kitchen display that shows the same orders to the kitchen. One app: the kitchen display is the till signed in with a kitchen role.

**Who uses it.** Cashiers and supervisors at the till. Cooks and expediters at the kitchen pass and stations.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_v2.html`: **the POS reference from 1 October.** Our improved build of the client-approved terminal (`TICVAI POS Terminal (3).html`). It is a **candidate, not client-approved**: the 14 screens captured from it are `designed`, in `review`, with a `wireframe.candidate` block, never client-verified (tools/applied/pos-v2-1-october.py). The file is 9.7 MB and **kept out of git**: it is on Chinmay's disk at that path, and the captures in `wireframes/incoming/P04-pos-v2/` are the record.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the build the client signed off (10 September). It stays as it is; each screen's `wireframe.prototype` block still cites its view. When the client approves v2, v2 takes its place.

**The kitchen display (P15) builds on v2.** Neither build has a kitchen display view. The nearest thing is v2's guest status board on the Queue (order numbers under Preparing and Ready for pickup, "mirrors the kitchen display"): draw the kitchen screens in v2's look so the two agree.

Open the file and match it. Do not describe it in words.

### Where it stands

- **40 screens.** 40 are Block A (the first 35 days of the build, from Monday 5 October).
- **30 have a frame** (all of P04): **14 are v2 captures** (candidate, in review: POS-000 to 006, 012, 021, 022, 023, 025, 028, 029), **9 are client-verified** (views v2 did not change: POS-007, 008, 011, 013, 014, 016, 020, 026, 027) and 7 were drawn in Claude Design on 29 September in the prototype's style. The 10 kitchen screens have none.
- v2 also has views with **no P04 screen** (sales journal, cart history, reservations with ticket encoding, a shift management panel). They are captured for review in `wireframes/incoming/P04-pos-v2/` (V2-*) and are questions for Chinmay, not screens: do not draw them as P04 screens.

**P04 is locked.** The v2 build is the design (pending the client's approval), so no batch is cut for it. Only the kitchen display (P15) is drawn here.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P15-kitchen-01`](../../P15-kitchen-01/) | P15 · Kitchen | 10 | to draw | 10 Block A |

#### Locked (the v2 build is the design, pending client approval)

| batch | label | screens | status | notes |
|---|---|---|---|---|
| `P04-payment-01` (no folder: locked) | P04 · Payment | 1 | locked | 1 Block A |
| `P04-reports-01` (no folder: locked) | P04 · Reports | 1 | locked | 1 Block A |
| `P04-sell-01` (no folder: locked) | P04 · Sell (1 of 3) | 10 | locked | 10 Block A; changed: POS-002, POS-011 |
| `P04-sell-02` (no folder: locked) | P04 · Sell (2 of 3) | 10 | locked | 10 Block A |
| `P04-sell-03` (no folder: locked) | P04 · Sell (3 of 3) | 4 | locked | 4 Block A; changed: POS-026, POS-029 |
| `P04-shift-01` (no folder: locked) | P04 · Shift | 4 | locked | 4 Block A; changed: POS-001 |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI POS: the till (P04) and the kitchen display (P15). Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_v2.html` (our v2 build; the kitchen display builds on it). This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/2-pos/return/TICVAI POS.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the POS file". Claude Code captures each of that batch's screens from `return/TICVAI POS.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
