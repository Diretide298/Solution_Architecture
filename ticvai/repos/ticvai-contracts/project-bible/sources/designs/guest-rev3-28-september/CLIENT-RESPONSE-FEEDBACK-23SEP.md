# Website feedback (rev 23 Sep): responses

**Prototype:** `TICVAI Guest Booking.dc.html` (web). Each answer says what changed and where to see it. The mobile prototype hasn't been updated yet.

---

## Header

**1. One profile icon in the header that opens login / register (currently "Sign in / Create account")**
Done. Sign in and Create account are now a single profile icon. Clicking it opens one screen with Log in and Register tabs. Signed-in guests see their account menu instead.

**2. Language icon in the header**
Done, on web and mobile. A language button (EN / العربية) sits next to the profile icon.
- Arabic flips the whole layout to right-to-left and switches the interface text: navigation, buttons, booking steps, ticket names and tags, the cart, the seat map, checkout and account.
- EN switches everything back.
- Venue, show and dish names stay as written. Longer descriptions stay in English until final Arabic copy is supplied.

## Tickets

**3. "Read more" should carry tags that can be customised per ticket type (e.g. 1 Hour, Min 75 cm, Free Adult Entries)**
Done. Ticket cards, Read more and the listing side panel show tags such as "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID".
- A ticket's own tags are used when the venue sets them. Otherwise they come from its duration, validity and the venue's height rule.
- They can be switched off in Config → Steps & cards → **Tags on tickets**.

**4. Video or image should show**
Done. Read more opens with the ticket's video or photo, and each ticket in a listing now has its own photo.

**5. Clicking Dated Day Pass should show the tickets on the same screen (side or below), without the extra "Select Tickets" step**
Done. Clicking a ticket opens the Adult / Child / Senior / Infant counters in the side panel on the same screen, and Continue carries the quantities into the booking. On the listing page, **Book** goes straight into the booking, and the side panel is open by default.

**6. Extra information for each ticket in the ticket section**
Done. Each Adult / Child / Senior / Infant row has an (i) button that shows who the ticket is for and what it includes.

**7. Show the ticket category directly instead of Dated Pass → Single Day Pass**
Done. The categories (Single day, Two-day flexible, UAE resident) are shown directly; there's no "Dated day pass" step in between.

**8. Show the single day ticket category on the B2C home page**
Done. The home page lists the ticket categories directly, and clicking one opens its counters on the same screen.

## Cart

**9. Show the date of visit in the cart**
Done. The cart shows the date of visit: the match date for the stadium and the reservation date for dining.

**10. Show upgrades only after the main ticket is in the cart**
Done. "Upgrade your day" stays hidden until a main ticket is in the cart.

**11. Show add-ons only on the Add-ons / Extras page**
Done. Add-ons are gone from the ticket panels and appear only on the Extras step.

**12. No quantity field for the selected ticket**
Done. Season and membership packages have a quantity stepper once selected.

**13. Cart summary: "Slide in right" shows at the bottom**
Fixed. With "Slide in right" selected, the summary is a tab on the right edge that slides in from the right.

## Seat map

**14. Show the view to the stage in the small window**
Done. Picking a section shows the view from that section. In concert mode it shows the stage; closer sections see a larger stage with fewer rows in front.

**15. Selected seats should be added to the cart**
Done. Each seat you pick goes into the cart with its section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"). Tapping it again removes it.

**16. 2D map: show the full seat map, and clicking a section should show its seats directly**
Done. The whole map shows each section in its price colour with a price key.
- Clicking a section zooms into it on the same map, with no new screen, and you pick seats there.
- In 3D, clicking a stand switches to the 2D map, zoomed into that stand.
- For stadium seat bookings, the separate "Your fixture" page has been removed. The fixture details are a strip at the top of the seat step, so booking opens straight on the map.

**17. When zoomed in, show the available seats across the map**
Done. When zoomed in, every nearby section shows its seats as dots of the same size:
- available seats in the section's price colour
- taken seats in grey
- the seat you picked highlighted

Zoom in, zoom out and "Whole map" buttons sit under the map.

## Settings

**18. Changing the category display makes no difference**
Fixed. Config → **Category display** (Grid / Row strip) now changes the product cards.

**19. Why is there a date selection in the header?**
The date list in the event banner was meant for events that run on several dates. It is now **off by default** and is a setting, Config → **Dates in event banner**. On every booking screen and preset, the date picker now always sits at the top of the booking step.

**20. How "Build your experience" is set up; it should be in the CMS configuration**
Done. It has its own Config section, **Build your experience**:
- how it shows: a button, a pop-up on arrival, or off
- one or two questions
- the answers and which product each one recommends

How a venue sets it up is written up in `handoff/BUILD-YOUR-EXPERIENCE.md`.

---

## Also changed in this round
- The loading screen shows the mascot instead of the TICVAI logo.
- Buttons that only showed a loading message (Add to wallet, Save PDF, Call, Redeem points and the like) now end with a confirmation message.
- Softlabs' 23 September design-gap items are now in the web prototype: guest checkout with a one-time code, the billing statement with payment retry, height and age checks, school trips and parties, and delivery rules. See `handoff/DESIGN-GAP-RESPONSE-23SEP.md`.

## Mobile prototype (updated)
`TICVAI Guest Booking Mobile.dc.html` now has:
- the language button (switches layout and text to Arabic and back) and a single profile icon that opens log in / register (points 1–2)
- ticket tags, and a Read more that opens a photo and description for each ticket (points 3, 4 and 6)
- the date of visit in the cart bar (point 9)
- the 2D seat map zooming into the tapped section on the same screen, with round seats of equal size; picked seats go into the cart line and total (points 15–17)
- the view from the section, which is larger the closer you sit (point 14)
- the 3D stadium map now loads on first open and after switching between 2D and 3D; before, it could come up blank
- the mascot on the loading screen
- guest checkout that only accepts a six-digit code, followed by the matched-profile prompt
- membership billing with soft decline, hard decline, declined again and paid states, including Retry now and Use another card

## Offline single files
Both are re-exported (24 Sep) and include the language switch: `TICVAI Guest Booking (single file).html` (web) and `TICVAI Guest Booking Mobile (single file).html`.

## Fixture photo
The fixture strip shows a date tile until a real photo is provided. Save a football or Union Arena photo as `images/lib/stadium-football.jpg` and the strip uses it automatically; no code change is needed.
