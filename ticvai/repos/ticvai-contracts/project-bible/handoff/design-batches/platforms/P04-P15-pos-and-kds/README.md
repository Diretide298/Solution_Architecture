# P04 + P15: TICVAI POS: the till (P04) and the kitchen display (P15)

**What it is.** The venue's till for tickets, food and retail, and the kitchen display that shows the same orders to the kitchen. One app: the kitchen display is the till signed in with a kitchen role.

**Who uses it.** Cashiers and supervisors at the till. Cooks and expediters at the kitchen pass and stations.

## Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS build. It is the design for all 30 POS screens and has a kitchen display view.

Open the file and match it. Do not describe it in words.

## Where it stands

- **40 screens.** 40 are Block A (the first 35 days of the build, from Monday 5 October).
- **30 have a frame; 23 of those are client-verified** (a capture of the client-approved prototype).

**P04 is locked.** The client-approved terminal is the design, so no batch is cut for it. Only the kitchen display (P15) is drawn here.

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P15-kitchen-01`](../../P15-kitchen-01/) | P15 · Kitchen | 10 | to draw | 10 Block A |

### Locked (the client-approved build is the design)

| batch | label | screens | status | notes |
|---|---|---|---|---|
| `P04-payment-01` (no folder: locked) | P04 · Payment | 1 | locked | 1 Block A |
| `P04-reports-01` (no folder: locked) | P04 · Reports | 1 | locked | 1 Block A |
| `P04-sell-01` (no folder: locked) | P04 · Sell (1 of 3) | 10 | locked | 10 Block A; changed: POS-002, POS-011 |
| `P04-sell-02` (no folder: locked) | P04 · Sell (2 of 3) | 10 | locked | 10 Block A |
| `P04-sell-03` (no folder: locked) | P04 · Sell (3 of 3) | 4 | locked | 4 Block A; changed: POS-026, POS-029 |
| `P04-shift-01` (no folder: locked) | P04 · Shift | 4 | locked | 4 Block A; changed: POS-001 |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI POS: the till (P04) and the kitchen display (P15). Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html`. This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
