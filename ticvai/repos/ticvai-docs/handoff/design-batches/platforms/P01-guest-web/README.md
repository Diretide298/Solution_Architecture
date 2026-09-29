# P01: TICVAI Guest, web shell

**What it is.** The venue's own booking website. Guests browse, pick a date and tickets, pay and get their tickets. It is white-labelled: each venue's brand, not TICVAI's.

**Who uses it.** Guests, on a phone or laptop browser. Most arrive from a search or a social link, ready to buy.

## Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes. The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-29-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

Open the file and match it. Do not describe it in words.

## Where it stands

- **50 screens.** 50 are Block A (the first 35 days of the build, from Monday 5 October).
- **49 have a frame; 48 of those are client-verified** (a capture of the client-approved prototype).

**WEB-050 Plan Your Visit is new** (the web opening of the visit planner). It has no frame yet. The other Block A screens that changed on 29 September keep their rev 3 frames until the client sees the new ones.

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

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

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, web shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/guest-rev3-29-september/TICVAI Visit Planner.dc.html`. This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
