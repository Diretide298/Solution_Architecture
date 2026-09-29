# TICVAI demo site: brief

> **What:** a section of the TICVAI marketing site that demos each platform with a simple, self-running simulation.
> **Decided:** MoM 29 September, section 3: "TICVAI marketing site should also showcase demo versions of each platform (POS, kiosk, mobile app, menu management)." Guest web booking and the CMS flow builder are added here.
> **Audience:** prospects. Owners and managers of theme parks, water parks, museums, attractions and restaurants. They are not users yet, and they give each page about 30 seconds.
> **Brand:** TICVAI's own, not a venue's.

This is marketing, not a product screen. There is no batch, no bundle and no import. It borrows the product's look so the demo is honest.

## What to build

**One overview page and seven product pages.** Each product page has a headline, three short benefit lines, and **a live simulation that runs by itself** in a device frame. The visitor can pause it, replay it, or take over and click.

| page | device frame | the simulation, one loop of 30 to 60 seconds | start from |
|---|---|---|---|
| POS | touch terminal, landscape | A cashier rings up two day passes and a meal combo, takes a card, the receipt prints (paper slides out), the drawer opens, the next guest starts. | `sources/designs/TICVAI_POS_Terminal_client_approved.html` |
| Kiosk | portrait kiosk | The attract loop plays; a guest taps, picks a language, chooses two tickets and a time, taps a card, the tickets print. | `wireframes/reference/Kiosk Board 1.dc.html` and `Kiosk Board 2.dc.html`, in the look of Guest Booking v2 |
| Mobile app | phone | The app opens on Home, the intro video skips, the guest opens **Plan**, answers party size, heights and pace, gets a day plan, taps Book this plan, pays, and the ticket appears in Tickets with its moving QR code. | `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html` and `TICVAI Visit Planner.dc.html` |
| Guest web booking | laptop | A guest picks a date, a time slot, two adults and a child, adds a fast track, checks out with only an email and a code, and gets the confirmation. | `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` |
| Kitchen display | wall screen | Orders arrive from the till and the app, split to grill and drinks stations, turn amber then red as they age, are bumped to the pass, and the guest's buzzer fires. | The kitchen display view in the POS terminal file (search "KDS"), and the P15 screens (`handoff/design-batches/P15-kitchen-01/`) |
| Menu management | laptop, with a phone beside it | A manager edits a burger's price and photo, marks fries unavailable, publishes; the phone beside it updates the menu in the app and the kiosk. | The F&B screens BO-045 Menu Management and BO-109 Menu Builder (`screens/P08-venue-back-office.yaml`), in the back-office look; the phone uses Mobile App v4's food ordering |
| CMS flow builder | laptop, with a phone beside it | The operator picks a preset, picks "Timed entry", drags the extras step, changes the brand colour and logo, taps Publish; the phone beside it shows the guest site change. | `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html` and the configuration panel in Guest Booking v2; the flow in `../CMS-FLOW-BUILDER/BRIEF.md` |

**The overview page** shows all seven as tiles, each with a short looping clip of its simulation, and one line: what it is and who uses it.

## How the simulations work

- **Scripted, not live.** A timeline of steps drives the prototype's own screens: a fake cursor or finger moves, taps, types. No back end, no network.
- **Reuse the prototype files where you can.** Load the relevant screens from the files above rather than redrawing them. Where a prototype is too heavy to embed, take its components and styles.
- **Captions** under the device name each step in a few words: "Pick a time", "Pay by card", "Ticket printed".
- **Controls:** play, pause, replay, and "Try it yourself", which hands the prototype to the visitor with the data reset.
- **Respect reduced motion.** With it on, show the steps as a still sequence with the captions.
- **Works on a phone.** Each device frame scales down; the page stacks.

## Seeded data

UAE, AED, English and Arabic. **Fictional venues only**, for example Coastal Aqua (water park, Abu Dhabi), Dune Park (theme park, Dubai), the Pearl Museum (Sharjah), and a food court called Harbour Kitchen. Real-looking prices, times and names.

**No real client or venue names, and no real logos.** The prototype folder has logos of real venues (`sources/designs/guest-rev3-29-september/logos/`). Do not use them. Do not name the client, its venues, or the real parks the minutes cite as examples.

## Deliverable

In `return/`:

1. `return/DEMO-SITE.dc.html`: one self-contained file with the overview and the seven product pages, reachable by `#overview`, `#pos`, `#kiosk`, `#mobile-app`, `#web-booking`, `#kitchen-display`, `#menu-management`, `#cms`. No external requests except Google Fonts. Images inline or drawn.
2. `return/NOTES.md`: which prototype each simulation reuses, what was redrawn and why, and anything the prototypes lack.

## After the demo

This is reviewed with the client like a design batch. It does not go into the product boards and nothing is imported.
