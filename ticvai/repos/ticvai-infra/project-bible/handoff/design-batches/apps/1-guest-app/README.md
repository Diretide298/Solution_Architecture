# Guest App

> **One working file for the whole app** (decided 30 September): `return/TICVAI Guest App.dc.html` in this folder. Every batch below adds its screens to that one file.

The guest's app on every surface: the website (P01), the mobile app (P02) and the self-service kiosk (P05). One booking engine, three screens sizes, white-labelled per venue.

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: none; the marketing-site demos are in [DEMO-SITE](../../DEMO-SITE/).

Sections: P01, P02, P05

## P01: TICVAI Guest, web shell

**What it is.** The venue's own booking website. Guests browse, pick a date and tickets, pay and get their tickets. It is white-labelled: each venue's brand, not TICVAI's.

**Who uses it.** Guests, on a phone or laptop browser. Most arrive from a search or a social link, ready to buy.

### Reference design to match

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

Open the file and match it. Do not describe it in words.

### Where it stands

- **50 screens.** 50 are Block A (the first 35 days of the build, from Monday 5 October).
- **50 have a frame; 49 of those are client-verified** (a capture of the client-approved prototype).

**The 30 September return was captured on 1 October** (viewport 1440 x 900): **11 screens are views in it and now carry its frames**: WEB-005 (the multi-park counters), WEB-006 (a surf session's tickets), WEB-049 (transport, stations filled in and departures listed), the At the venue tabs WEB-036, WEB-039, WEB-040, WEB-041, WEB-042, WEB-043, WEB-046, and **WEB-050 Plan Your Visit, from the Visit Planner, which had no frame**. Do not draw these. The views and proof texts are in `tools/capture-plans/guest-web-v2.json`; the captures, with a manifest, in `wireframes/incoming/P01-web-v2/`. WEB-002, WEB-004 and WEB-007 keep their 29 September captures and the rest their rev 3 (28 September) captures: this return does not change those views.

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
Build batch <BATCH ID> of TICVAI Guest, web shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`. This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
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

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

Open the file and match it. Do not describe it in words.

### Where it stands

- **77 screens.** 77 are Block A (the first 35 days of the build, from Monday 5 October).
- **77 have a frame; 58 of those are client-verified** (a capture of the client-approved prototype). The other 19 were drawn in the v4 look by Claude Code on 30 September and wait for the client's design reviewer (item 2 below).

**The frames were captures of the 28 September build (Mobile v2).** Mobile App v4 replaced it on 29 September. So:

1. **21 screens are views in v4** (GST-063, GST-012, GST-007, GST-008, GST-049, GST-041, GST-001, GST-002, GST-003, GST-004, GST-006, GST-051, GST-053, GST-054, GST-021, GST-022, GST-038, and the intercity transport screens GST-076, GST-077, GST-078, GST-079). **Done: captured from the 30 September return on 1 October** and re-imported (the first 17 had been captured from the 29 September build on 30 September; the transport four replace their Mobile v2 frames). **GST-021 is now the walking-navigation view**: the 3D map following the route, turn-by-turn above it. Do not draw these. The views and proof texts are in `tools/capture-plans/guest-mobile-v4.json`; the captures, with a manifest, in `wireframes/incoming/P02-mobile-v4/`.
2. **19 changed Block A screens have no v4 view** (GST-059, GST-019, GST-039, GST-042, GST-066, GST-073, GST-048, GST-050, GST-056, GST-058, GST-074, GST-075, GST-009, GST-031, GST-032, GST-052, GST-011, GST-015, GST-036). Drawn in the v4 look by Claude Code on 30 September (`designed`, not client-verified); refine them in the batches below.
3. The other 37 screens keep their Mobile v2 frames for now. Restyle them to v4 when their batch comes round.

**To capture again** (both platforms): `node tools/capture-prototype.mjs tools/capture-plans/guest-mobile-v4.json wireframes/incoming/P02-mobile-v4` and `node tools/capture-prototype.mjs tools/capture-plans/guest-web-v2.json wireframes/incoming/P01-web-v2`, then `python tools/applied/guest-30-september-return.py --apply`.

The manifest counts every P02 batch as drawn, because it counts frames on disk. It cannot see that the frames are one build old. The batches below are exported and current anyway.

**Three changes from the client meeting of 30 September, over the v4 captures.** The v4 views stay the layout; these add to them, on the web twins too (WEB-050, WEB-004).

- **Planner, multi-venue (MoM 4.7, Allam): GST-051, GST-053, GST-054, WEB-050.** In a multi-venue tenant each day is one park (a *Which park each day?* choice after the dates), and a day holds only that park's rides, dining and **retail: shops and kiosks now sit beside meals** as plan stops. A cuisine or shop the park lacks is never filled from another park: the chip says *Not at the parks you chose* before planning, and the day shows a *Not at this park* banner naming the park that has it. Draw the `preferenceNotAtVenue` state.
- **Ride detail video (MoM 4.8, Qossai): GST-004, WEB-004.** The info button reveals the details and plays the video in place. **No loader or loading screen in front of the video**: the poster frame shows while it buffers (`videoBuffering`), and a video that cannot play leaves the poster (`videoUnavailable`). Remove any spinner the v4 capture draws over the video.
- **In-park navigation in 3D (MoM 4.8, ADR-0069): GST-021, GST-038.** A 2D/3D toggle on the map; 3D shows the park model with the walking route on the paths and a live position dot, with turn-by-turn guidance to a chosen point. Draw the `map3dUnavailable` state (no 3D model: the 2D map with the same route and live position, the toggle hidden) and the `weakGps` state (an approximate position ring and *Position approximate*).

**Pending in design: what the 30 September return does not show yet.** These keep their specification and are built from it until a design shows them; the captures above stay the layout.

- **Planner, multi-venue with retail (GST-051, GST-053, GST-054, WEB-050).** The return's planner is still single-park: no *Which park each day?* step, no shops or kiosks as plan stops, no *Any shops you'd like to visit?* choice (its lunch step offers cuisines only), and no `preferenceNotAtVenue` chip or banner.
- **Ride video without a loader (GST-004, WEB-004).** The return's ride detail has no info button that plays a video in place, and no `videoBuffering` or `videoUnavailable` frame. Its only loader is on the app's intro video (*Loading video…* over the splash), which is not GST-004.
- **3D navigation, partly shown (GST-021, GST-038; web WEB-039).** Shown: the app's walking navigation in 3D (route on the paths, live position, turn-by-turn, the camera following the guest), and on the web a *3D view / 2D plan* switch. Not shown: a guest-facing 2D/3D toggle on the app (3D or 2D is a demo setting there), `map3dUnavailable` and `weakGps`.

**Also in the return, a prototype defect to raise with the design side:** on the multi-park flow the ticket's *Read more* panel still prices guests at single-park rates (Adult AED 325) and charges an infant AED 475, while the counters on the page are right (2 park ticket, Adult AED 475, infant free). The capture of WEB-005 shows the page, not the panel.

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
Build batch <BATCH ID> of TICVAI Guest, mobile shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html` and `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`. This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
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

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved guest look. The kiosk is the same product, narrower.
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
Build batch <BATCH ID> of TICVAI Guest, kiosk shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html` and `wireframes/reference/Kiosk Board 1.dc.html`. This is a portrait touch kiosk, 1080 x 1920, large touch targets, no keyboard, an attract screen when idle. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
