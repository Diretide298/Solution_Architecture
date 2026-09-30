# Guest App

> **One working file for the whole app** (decided 30 September): `return/TICVAI Guest App.dc.html` in this folder. Every batch below adds its screens to that one file.

The guest's app on every surface: the website (P01), the mobile app (P02) and the self-service kiosk (P05). One booking engine, three screens sizes, white-labelled per venue.

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: none; the marketing-site demos are in [DEMO-SITE](../../DEMO-SITE/).

Sections: P01, P02, P05

## P01: TICVAI Guest, web shell

**What it is.** The venue's own booking website. Guests browse, pick a date and tickets, pay and get their tickets. It is white-labelled: each venue's brand, not TICVAI's.

**Who uses it.** Guests, on a phone or laptop browser. Most arrive from a search or a social link, ready to buy.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes. The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-29-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

Open the file and match it. Do not describe it in words.

### Where it stands

- **50 screens.** 50 are Block A (the first 35 days of the build, from Monday 5 October).
- **49 have a frame; 48 of those are client-verified** (a capture of the client-approved prototype).

**WEB-050 Plan Your Visit is new** (the web opening of the visit planner). It has no frame yet. The other Block A screens that changed on 29 September keep their rev 3 frames until the client sees the new ones.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P01-discovery-browse-01`](../../P01-discovery-browse-01/) | P01 · Discovery & Browse | 5 | part drawn | 5 Block A; new: WEB-050 |
| [`P01-account-self-service-01`](../../P01-account-self-service-01/) | P01 · Account & Self-Service | 5 | drawn | 5 Block A; changed: WEB-016, WEB-017, WEB-018, WEB-019, WEB-020 |
| [`P01-booking-selection-01`](../../P01-booking-selection-01/) | P01 · Booking & Selection | 7 | drawn | 7 Block A; changed: WEB-005, WEB-006, WEB-007, WEB-008, WEB-047, WEB-048 |
| [`P01-cart-checkout-01`](../../P01-cart-checkout-01/) | P01 · Cart & Checkout | 5 | drawn | 5 Block A; changed: WEB-010, WEB-011, WEB-012 |
| [`P01-membership-loyalty-value-01`](../../P01-membership-loyalty-value-01/) | P01 · Membership, Loyalty & Value | 5 | drawn | 5 Block A; changed: WEB-021, WEB-023, WEB-024, WEB-043 |
| [`P01-transport-01`](../../P01-transport-01/) | P01 · Transport | 1 | drawn | 1 Block A; changed: WEB-049 |
| [`P01-engagement-support-01`](../../P01-engagement-support-01/) | P01 · Engagement & Support | 6 | drawn | 6 Block A; changed: WEB-044; 1 thin |
| [`P01-in-venue-services-01`](../../P01-in-venue-services-01/) | P01 · In-venue Services | 6 | drawn | 6 Block A |
| [`P01-promotions-01`](../../P01-promotions-01/) | P01 · Promotions | 1 | drawn | 1 Block A |
| [`P01-retail-01`](../../P01-retail-01/) | P01 · Retail | 2 | drawn | 2 Block A |
| [`P01-support-01`](../../P01-support-01/) | P01 · Support | 2 | drawn | 2 Block A |
| [`P01-ticketing-01`](../../P01-ticketing-01/) | P01 · Ticketing | 3 | drawn | 3 Block A |
| [`P01-high-demand-access-01`](../../P01-high-demand-access-01/) | P01 · High-Demand Access | 1 | drawn | 1 Block A; 1 thin |
| [`P01-system-states-01`](../../P01-system-states-01/) | P01 · System States | 1 | drawn | 1 Block A; 1 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, web shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/guest-rev3-29-september/TICVAI Visit Planner.dc.html`. This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P02: TICVAI Guest, mobile shell

**What it is.** The venue's own mobile app. Home, Explore, Plan and Tickets tabs, with a Buy tickets button on every screen. It is white-labelled per venue.

**Who uses it.** Guests before and during the visit. They plan the day, buy, show a ticket at the gate and order food in the park.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

Open the file and match it. Do not describe it in words.

### Where it stands

- **77 screens.** 77 are Block A (the first 35 days of the build, from Monday 5 October).
- **77 have a frame; 77 of those are client-verified** (a capture of the client-approved prototype).

**The frames were captures of the 28 September build (Mobile v2).** Mobile App v4 replaced it on 29 September. So:

1. **17 screens are views in v4** (GST-063, GST-012, GST-007, GST-008, GST-049, GST-041, GST-001, GST-002, GST-003, GST-004, GST-006, GST-051, GST-053, GST-054, GST-021, GST-022, GST-038). **Done: captured from v4 on 30 September** and re-imported, replacing their v2 frames. Do not draw these. The views and proof texts are in `tools/capture-plans/guest-mobile-v4.json`; the captures, with a manifest, in `wireframes/incoming/P02-mobile-v4/`. To capture again: `node tools/capture-prototype.mjs tools/capture-plans/guest-mobile-v4.json wireframes/incoming/P02-mobile-v4`, then `python tools/applied/guest-v4-capture-30-september.py --apply`.
2. **19 changed Block A screens have no v4 view** (GST-059, GST-019, GST-039, GST-042, GST-066, GST-073, GST-048, GST-050, GST-056, GST-058, GST-074, GST-075, GST-009, GST-031, GST-032, GST-052, GST-011, GST-015, GST-036). Draw these in the v4 look, in the batches below.
3. The other 41 screens keep their Mobile v2 frames for now. Restyle them to v4 when their batch comes round.

The manifest counts every P02 batch as drawn, because it counts frames on disk. It cannot see that the frames are one build old. The batches below are exported and current anyway.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P02-discovery-01`](../../P02-discovery-01/) | P02 · Discovery | 1 | drawn | 1 Block A; changed: GST-063 |
| [`P02-engagement-support-02`](../../P02-engagement-support-02/) | P02 · Engagement & Support (2 of 2) | 2 | drawn | 2 Block A; changed: GST-059 |
| [`P02-account-self-service-01`](../../P02-account-self-service-01/) | P02 · Account & Self-Service (1 of 2) | 10 | drawn | 10 Block A; changed: GST-012, GST-019, GST-039, GST-042, GST-066; 1 thin |
| [`P02-account-self-service-02`](../../P02-account-self-service-02/) | P02 · Account & Self-Service (2 of 2) | 4 | drawn | 4 Block A; changed: GST-073; 1 thin |
| [`P02-booking-selection-01`](../../P02-booking-selection-01/) | P02 · Booking & Selection | 10 | drawn | 10 Block A; changed: GST-007, GST-008, GST-048, GST-049, GST-050, GST-056, GST-058, GST-074, GST-075; 1 thin |
| [`P02-cart-checkout-01`](../../P02-cart-checkout-01/) | P02 · Cart & Checkout | 3 | drawn | 3 Block A; changed: GST-009, GST-041; 1 thin |
| [`P02-discovery-browse-01`](../../P02-discovery-browse-01/) | P02 · Discovery & Browse | 7 | drawn | 7 Block A; changed: GST-001, GST-002, GST-003, GST-004, GST-006; 1 thin |
| [`P02-engagement-support-01`](../../P02-engagement-support-01/) | P02 · Engagement & Support (1 of 2) | 10 | drawn | 10 Block A; changed: GST-031, GST-032, GST-051, GST-052, GST-053, GST-054; 2 thin |
| [`P02-in-venue-services-01`](../../P02-in-venue-services-01/) | P02 · In-venue Services | 10 | drawn | 10 Block A; changed: GST-021, GST-022, GST-038; 2 thin |
| [`P02-membership-loyalty-value-01`](../../P02-membership-loyalty-value-01/) | P02 · Membership, Loyalty & Value | 3 | drawn | 3 Block A; changed: GST-011, GST-015, GST-036; 2 thin |
| [`P02-marketing-01`](../../P02-marketing-01/) | P02 · Marketing | 1 | drawn | 1 Block A |
| [`P02-promotions-01`](../../P02-promotions-01/) | P02 · Promotions | 1 | drawn | 1 Block A |
| [`P02-retail-01`](../../P02-retail-01/) | P02 · Retail | 1 | drawn | 1 Block A |
| [`P02-support-01`](../../P02-support-01/) | P02 · Support | 1 | drawn | 1 Block A |
| [`P02-high-demand-access-01`](../../P02-high-demand-access-01/) | P02 · High-Demand Access | 1 | drawn | 1 Block A; 1 thin |
| [`P02-in-venue-experience-01`](../../P02-in-venue-experience-01/) | P02 · In-Venue Experience | 2 | drawn | 2 Block A; 1 thin |
| [`P02-ticketing-01`](../../P02-ticketing-01/) | P02 · Ticketing | 4 | drawn | 4 Block A; 1 thin |
| [`P02-transport-01`](../../P02-transport-01/) | P02 · Transport | 4 | drawn | 4 Block A; 1 thin |
| [`P02-system-states-01`](../../P02-system-states-01/) | P02 · System States | 2 | drawn | 2 Block A; 2 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, mobile shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html` and `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P05: TICVAI Guest, kiosk shell

**What it is.** The self-service kiosk at the venue entrance. The guest product in a fixed frame, with no keyboard.

**Who uses it.** Guests at the gate who did not buy online. They want a ticket fast and a printed receipt.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved guest look. The kiosk is the same product, narrower.
- `wireframes/reference/Kiosk Board 1.dc.html`: the client's kiosk board, for layout (and Kiosk Board 2).

Open the file and match it. Do not describe it in words.

### Where it stands

- **17 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P05-ai-01`](../../P05-ai-01/) | P05 · AI | 1 | to draw |  |
| [`P05-sell-02`](../../P05-sell-02/) | P05 · Sell (2 of 2) | 6 | to draw | 3 thin |
| [`P05-sell-01`](../../P05-sell-01/) | P05 · Sell (1 of 2) | 10 | to draw | 6 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, kiosk shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `wireframes/reference/Kiosk Board 1.dc.html`. This is a portrait touch kiosk, 1080 x 1920, large touch targets, no keyboard, an attract screen when idle. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
