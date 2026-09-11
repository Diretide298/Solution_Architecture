# The TICVAI booking engine, without any one client's version of it

Built from `TICVAI Booking Skeletons.dc.html` in `Venue ticketing platform design.zip`.

That pack ships **36 flows across five verticals** — Summit Peaks, Coastal Aqua, Union Arena,
Grand Playhouse, Saffron Table. **Those are five clients' configurations, not TICVAI's.** The venue
names are invented, the prices are invented, and each palette is sampled from a different brand's
logo (`ferrari-world`, `maf`, `deepdive`, `explorers`). Reading them as a specification would build
one client's product.

What is TICVAI's is the layer underneath: **one step spine, 16 module factories, and 21 flow
archetypes**, of which nine recur across verticals. That layer is what this file records, because
it is the part every client instance is a configuration of.

## The spine

    Select  ->  Seats  ->  Extras  ->  Details  ->  Payment  ->  Confirmed
                (conditional)  (skippable)

Fixed. No flow reorders it, and no flow adds a step. `seatMode` is `rows` or `tables`.

## The 16 module factories

    chips  date  note  counters  cards  form  timeline  event
    benefits  heights  toggle  spec  sessions  menu  matrix  expand

**The pack's own README says 14 and omits `date()` and `toggle()`; it also says 34 flows where the
code has 36.** Both counts here are read off the code, which is the one that renders.

## The 21 archetypes

`use` is how many of the five verticals declare it. **The nine used more than once are the
platform's; the twelve used once are a vertical's.** A new client starts from the nine.

| archetype | use | pay | requires | modules |
|---|---|---|---|---|
| day | 2 | full | consent, lead | date note expand toggle sessions heights |
| timed | 2 | full | consent, lead | date chips counters sessions heights |
| gate | 2 | full | consent, guests, lead, waiver | chips date spec counters note heights |
| group | 2 | invoice | consent, lead | form |
| best | 2 | full | consent, lead | counters event note cards chips |
| season | 2 | deposit | consent, guests, id, lead | benefits |
| access | 2 | full | consent, guests, lead | chips counters form event cards |
| deferred | 2 | full | consent, guests, lead | event chips counters timeline |
| block | 2 | invoice | consent, lead | form |
| combo | 1 | full | consent, lead | cards date counters |
| annual | 1 | full | consent, guests, id, lead | benefits |
| fast | 1 | full | consent, lead | benefits |
| hosp | 1 | invoice | consent, lead | benefits |
| table | 1 | none | consent, lead | chips date note |
| prepaid | 1 | full | consent, guests, lead | cards date chips counters toggle |
| deposit | 1 | deposit | consent, lead | chips date note |
| offer | 1 | none | consent, lead | chips cards date |
| waitlist | 1 | none | lead | chips note form |
| takeaway | 1 | full | consent, lead | menu chips spec note |
| delivery | 1 | full | consent, lead | menu form |
| large | 1 | invoice | consent, lead | form |

`pay` is `full | deposit | none | invoice`.
`requires` is drawn from `lead, guests, id, waiver, cert, plate, consent` and decides what the
**Details** step renders.

## Why this matters for our screens

**`requires` is applied at Details and decided at Select.** WEB-011 cannot be drawn correctly
without knowing which archetype WEB-005 offered, and `pay` changes both Extras and Payment. So a
booking flow is configured whole or not at all -- which is why the spine is taken as one assignment
and not as the two batches `design-manifest.json` cuts it into.

Our P01 spine, screen by screen:

| step | screen |
|---|---|
| Select | WEB-005 Ticket Type Selection, WEB-006 Date & Session Selection |
| Seats | WEB-007 Interactive Seat Selection |
| Extras | WEB-008 Add-ons & Upsell |
| Details | WEB-011 Guest Details & Attendee Forms |
| Payment | WEB-012 Checkout - Payment |
| Confirmed | WEB-013 Booking Confirmation |

## What not to copy

The prices, the venue names, the five palettes and the logo files. **The palette is derived by
sampling logo pixels through a canvas**, which needs a same-origin image -- it works inside the
pack and produces nothing anywhere else. A TICVAI reference build uses TICVAI's own tokens from
`screens/_design-tokens.yaml`.
