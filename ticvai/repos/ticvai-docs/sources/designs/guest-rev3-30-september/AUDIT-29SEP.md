# Functionality audit: Mobile App v4 vs Guest Booking v2 (web)

All items marked Fix in the first pass are now closed. Each line says what changed and where to see it.

## Booking engine (shared)
- Every web flow is available on mobile through the embedded engine. Step order is tailored per flow, with a toggle to switch back to one decision per screen.
- **Fixed:** Signed in, the details step is skipped on web and mobile. On mobile the pay step now shows who you are signed in as and the T&C tick, and payment waits for it.
- **Fixed:** Add-on quantities: when *Quantities on add-ons* is on, a ticked mobile extra shows a − / + stepper and the price multiplies. The cart button now sits in the booking header too, with a count, and opens the cart.
- **Fixed:** Mobile reads the web *Performance reveal* and *Times per page* settings (and has its own copies in Config → Booking rules). "Date → time → ticket" reveals times only after a date; paged times show as a grid with page buttons instead of the slider. "Show all" keeps the slider.
- **Fixed:** Location switcher: Kids Club on mobile starts with *Which location?* (Al Barsha, Mirdif, Yas Island, Sharjah) and keeps a *Change* bar on later steps. Controlled by *Location switcher*.
- **Fixed:** Help me choose for the museum asks "Who is the course for?" on the Courses path and filters by age, on web and mobile.

## Seats
- **Fixed:** Web and mobile both draw zoomed-in seats with `seatzoom.grid`.
- **Fixed:** Mobile seat maps have − / + zoom and a full-screen button (stadium and theatre).
- **Fixed:** Theatre plan on mobile supports pinch zoom and the − / + buttons, and scrolls in both directions when zoomed.
- **Fixed:** Mobile has the seat view box: a view-from-seat panel under the map for the chosen section (stadium) or the last seat picked (theatre). Toggle: *Seat view box*.

## Venue-specific
- **Fixed:** Cabana hold: picking a hut on mobile starts an 8-minute countdown banner. It turns amber under 2 minutes; when it runs out the step and payment are blocked until the hut is picked again.
- **Fixed:** Transport on mobile has One-way, Multi-trip and Favourites tabs. Multi-trip lists the 5-trip, 10-trip, weekly and monthly cards priced for the chosen stations; routes can be saved and reopened from Favourites.
- Meeting rooms: buffer rules are shared through the engine. OK.
- **Fixed:** Dining delivery on mobile shows the minimum-order check (AED 90, blocks payment below it) and the free-delivery gap (AED 200). Takeaway shows the 20-minute hold note.

## At venue
- **Fixed (web):** At the venue now has *Happening now* (live food order, queue, tables, shop collections and parking, with a count on the tab), *Book a table* (outlet, party size, tonight's times, seating, deposit rule for 6+, cancel), and *Shop* with a choice of collection point (Collect at the gate, car park kiosk, home delivery) and a collection code after paying.
- **Fixed:** Mobile map has *Start* on the destination card: a turn-by-turn banner (next turn and distance, metres to go, arrival time, progress bar) and the "you are here" dot moves along the route. *End navigation* stops it.

## Account and services
- **Fixed:** Mobile membership statements open a full statement (charges, VAT, invoice number, member savings, send as PDF or CSV, other statements). *Download my data* is a flow: choose categories and format, then a tracked request through to *Ready to download*.

## Content and UI
- **Fixed:** Transport has two more sample routes: E201 Abu Dhabi – Al Ain and E700 Dubai – Fujairah, on web and mobile.
- **Fixed:** Arabic for Happening now, cart, resume, shop items, ticket types, config and all strings added today, in `ticvai-ar-29sep.js` (loaded by web and mobile).
- **Closed:** The "Open v2 screens" link is no longer in Mobile v4.

## Offline and publish
- **Fixed:** Mobile pools are cut to 4 images per venue, and the booking engine loads on demand (first booking, or opening Buy tickets) instead of at launch. The mobile single file is now 23 MB. It loads the engine from `TICVAI Guest Booking v2 (single file).html`, so keep the two files in the same folder.
- **Fixed:** The Visit Planner single file now includes its images (data-src with the safeImg ref pattern).
