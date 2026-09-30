# Partner Portal

> **One working file for the whole app** (decided 30 September): `return/Partner Portal.dc.html` in this folder. It starts from the B2B option the client picks (`../../B2B-OPTIONS/return/B2B-option-A.dc.html` or `-B`), and every batch below adds its screens to that one file.

The seventh app (decided 30 September): the partner and reseller portal (P10). Before the client picks, the two options are drawn in [`B2B-OPTIONS/`](../../B2B-OPTIONS/BRIEF.md).

## P10: partner web

**What it is.** The reseller portal. Hotels, travel agents and other partners sell the venue's tickets at partner prices, on credit.

**Who uses it.** Partner staff (PTR-001 to PTR-021) and TICVAI's partner team (PTR-022 to PTR-051, the workshop boards WS21 to WS23).

## Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for Option A, the POS-style portal.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: for Option B, the website-style portal.

Open the file and match it. Do not describe it in words.

## Where it stands

- **51 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Draw the two options first** ([`B2B-OPTIONS/`](../../B2B-OPTIONS/BRIEF.md)). The client picks one after review (MoM 29 September, section 3). The P10 batches below wait for that choice, because the shell and the sell screens change with it. The workshop batches WS21 to WS23 are TICVAI's internal partner screens and do not depend on it.

**Added once the option is finalised:** the partner cash drawer (Option A only), sent-ticket history, and an "opened" status on sent tickets have no operation yet. Draw them greyed out; see [`ADD-ON-FINALISE.md`](../../B2B-OPTIONS/ADD-ON-FINALISE.md).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P10-booking-quotes-01`](../../P10-booking-quotes-01/) | P10 · Booking & Quotes | 4 | to draw |  |
| [`P10-orders-fulfilment-01`](../../P10-orders-fulfilment-01/) | P10 · Orders & Fulfilment | 2 | to draw |  |
| [`P10-overview-01`](../../P10-overview-01/) | P10 · Overview | 1 | to draw |  |
| [`P10-reports-settlement-01`](../../P10-reports-settlement-01/) | P10 · Reports & Settlement | 3 | to draw |  |
| [`P10-support-01`](../../P10-support-01/) | P10 · Support | 1 | to draw |  |
| [`P10-access-account-01`](../../P10-access-account-01/) | P10 · Access & Account | 5 | to draw | 1 thin |
| [`P10-credit-settlement-01`](../../P10-credit-settlement-01/) | P10 · Credit & Settlement | 2 | to draw | 1 thin |
| [`P10-inventory-pricing-01`](../../P10-inventory-pricing-01/) | P10 · Inventory & Pricing | 3 | to draw | 1 thin |
| [`WS21`](../../WS21/) | B2B, Reseller & OTA Partner Management board 1 | 10 | to draw | 2 thin |
| [`WS22`](../../WS22/) | B2B, Reseller & OTA Partner Management board 2 | 10 | to draw | 2 thin |
| [`WS23`](../../WS23/) | B2B, Reseller & OTA Partner Management board 3 | 10 | to draw | 3 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, partner web. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is a desktop browser, 1440 wide; Option A is a till-like sell screen, Option B a storefront with a partner login. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then add them to the one working file for the whole app, handoff/design-batches/apps/7-partner-portal/return/Partner Portal.dc.html (it starts from the option file the client picked; keep every earlier screen working), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
