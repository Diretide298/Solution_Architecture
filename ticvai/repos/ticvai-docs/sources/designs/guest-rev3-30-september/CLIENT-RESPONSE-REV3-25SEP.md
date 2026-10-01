# Website feedback (rev 3.0, 25 Sep): responses

**Prototypes:** `TICVAI Guest Booking v2.dc.html` (web) and `TICVAI Guest Booking Mobile v2.dc.html` (mobile). The previous versions are unchanged.

**Where the settings live:** every new option is in Config → **Booking rules (Rev 3)**, and the same options are exposed as engine properties (Tweaks) so they can be set per tenant. Venues and flows are switched from the Config drawer.

**Mobile:** the mobile prototype has a new **Rev 3 feedback** group in Account → All screens (22 screens). These are clickable screens showing each flow. They are not wired to the booking engine the way the web prototype is.

---

## Performance display

**1. Many performances should resize and page; filter by morning, afternoon, evening**
Done. When a venue has more than eight times, they show as compact time tiles (like the Access Time grid) and page 24 at a time with Earlier / Later buttons. Filter chips above them (All times, Morning, Afternoon, Evening) show how many times fall in each part of the day.
- See: Summit Peaks → *Timed access — 10-minute slots* (64 times, 07:30–18:00).
- Config: **Times per page** (8, 12, 24, Show all; default 24) and **Morning / afternoon / evening filter** (on/off).

**2. Step 1 date, step 2 time (only after the date), step 3 ticket (only after date and time)**
Done for every flow that has a date. Time options move up to sit straight after the date and stay hidden until a date is picked. Tickets stay hidden until a time is picked. A short hint in their place tells the guest what to pick next, and Continue stays off until both are chosen.
- Config: **Performance reveal**: Date → time → ticket (default) or All at once.

## Stadium and theatre seats

**3. The sign-in screen should appear after Add-ons**
Done. Sign-in (or the guest code, if guest checkout is on) is asked for when the guest leaves the Add-ons step. The basket is kept.
- Config: **Ask to sign in**: After add-ons (default) or At payment.

**4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map)**
Both are built for the stadium and the theatre.
- Flow 1: Union Arena → *Flow 1 · Fixed date → zone → seat map*, and Grand Playhouse → *Flow 1 · Single performance → seat map*. These go straight to the map.
- Flow 2: Union Arena → *Flow 2 · Choose date & time → seat map* (Desert Nights, two shows a night) and Grand Playhouse → *Flow 2 · Date & time → seat map*.
- Option 1 (pop-up) and Option 2 (timed-ticket style) are both available. Config: **Date & time on seat events**: Inline step (timed-ticket style) or Pop-up on the seat map. With the pop-up, the guest lands on the seat map and a dialog asks for the date and time first.

**5. CMS option to show the seat view right, left, top or bottom**
Done. Config: **Seat view box**: Bottom (current), Right, Left or Top of the seat map. On narrow screens it drops below the map.

**6. Time selection on top, configurable**
Done in two places:
- On the selection step, time now sits directly under the date, above language & format and tickets (see item 2).
- On the seat map, a time bar at the top shows the chosen performance, lets the guest switch show, and has a Change date button. Changing the show releases any held seats. Config: **Time bar above seat map** (on/off).

**7. Theatre flow should be similar to the stadium flow**
Done, with its own seat map. The theatre no longer borrows the stadium bowl. Grand Playhouse has an auditorium plan: a stage (or a screen for cinema) at the front, then Stalls (rows A–K), Circle (A–E) and Balcony (A–D), with curved rows, aisles and Premium / Standard / Economy pricing. Choosing the show and choosing the seats now happen on one step: date, time, show (and language & format for cinema), then the seat map below on the same page. Up to ten seats per booking; the basket lists each one (e.g. "Stalls · Row F, Seat 9").

## Dining

**8. Unable to complete the table booking flow**
Fixed. A table reservation had nothing priced in the basket, so Continue never switched on. Picking a date, time and party size now adds "Table for 4 · 19:30 · no card needed" to the basket and the flow completes. The deposit hold and waitlist flows are fixed the same way; the deposit hold adds AED 100 per guest.

**9. Add-ons and modifiers for F&B menu items**
Done. In the takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice) and optional add-ons with prices (sides, dips, toppings, leave-outs), plus a quantity. The total updates live, and the basket line lists the choices (for example "Hot, Burnt butter rice").
- Config: **F&B add-ons & modifiers** (on/off).

## Basket

**10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic**
Done. Config → Layout & locale → **Cart & summary** now has Cart sidebar (fixed right), Cart sidebar (left), Slide-in right, Slide-up bottom, **Floating cart icon** (new: a round basket button with an item count that opens the slide-in basket) and Single column.
- New: **Cart side in Arabic**: Keep on right (default) or Mirror to left.

## Choosing products

**11. Show products based on questions (Help me choose)**
Extended. Help me choose was on the Kids Club only. It now also runs on Coastal Aqua (slides, surf or a cabana; who is coming) and on Tidewater Museum (on my own, with a guide, or a course). The last answer opens the matching flow.
- Config → Build your experience: **Help me choose** (button, pop-up on arrival, off) and **Questions** (1 or 2).

**12. Experience flow: show the product directly, not the ticket category**
Done. House of Pages → *Experience — product first* lists each experience (author talk, calligraphy workshop, story hour, rooftop reading night) with its own date, time and tickets. There is no category step.

**13. House of Wisdom: meeting room flow**
Done as a new venue type, House of Pages (library and rooms). *Meeting room by the hour*: date → start time → length (1 hour, 2 hours, half day, full day) → room (focus pod, majlis room, boardroom, auditorium) → attendees → add-ons (coffee break, working lunch, AV technician). The room price multiplies by the length.

**14. Show a ticket category with details, with booking turned on or off in the CMS (e.g. student courses shown but not bookable)**
Done. A product can be marked as information only. It keeps its details and photo, shows an "Info only" or "Not bookable online" label, and opens its details instead of adding to the basket.
- See: Tidewater Museum → *Courses (some info-only)*, and the Courses & workshops category in *Category → subcategory tickets*.
- Config: **Show info-only products** (on/off).

**15. Book the product from the map (e.g. pick an available cabana and add it to the cart)**
Done. Coastal Aqua → *Cabana & locker rentals* now opens a cabana map: wave-view cabanas by the wave pool, riverside cabanas along the lazy river and private decks. Taken cabanas are greyed out. Tapping an available one adds "Cabana W2 · Wave-view cabana" to the basket at its own price, and Continue switches on.

**16. Choose category, then subcategory, configurable in the CMS**
Done. Tidewater Museum → *Category → subcategory tickets*: category tiles (Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then the tickets in that category, each with Adult / Child / Student counters.
- Config: **Ticket categories**: Category → subcategory, or Flat list (all tickets under category headings).

**17. Guided tour times based on the tour language**
Done. Tidewater Museum → *Guided tour by language*: pick a language (English, العربية, Français, Deutsch, 中文, Русский) and only tours in that language are listed.

## Multi-location and sessions

**18. One tenant with an attraction in several locations; change location on the booking screen**
Done on the Kids Club (Al Barsha, Mirdif, Yas Island, Sharjah). The guest picks a location first. After that, a "Booking at" bar at the top of the booking screen has a Change location menu. Selections are kept, and times and prices refresh for the new location.
- Config: **Location switcher** (on/off).

**19. Surf sessions with filters (as on The Wave)**
Done. Coastal Aqua → *Surf sessions with filters*: two dropdowns, **Choose your experience** (surf, lessons and coaching, swim and play, sauna) and **Select surf level** (beginner to expert), plus a Reset filters button, the morning / afternoon / evening chips and paging. Each session shows its price per surfer and places left. Sold-out sessions are greyed out.

**20. Enable or disable a Quick Tour that describes the customer journey**
Done. On a guest's first booking visit, a four-step tour highlights the date, the time, the tickets and the basket, with Back, Next / Done and End tour buttons. A **Quick tour** button on the booking page replays it.
- Config: **Quick tour** (on/off).

## Transport

**21. Sell transport tickets: one trip, multi trip, favourites, departure and arrival station for a date and time period, and a map of the route**
Done as a new venue type, Emirates Link (intercity coaches, Sharjah – Dubai – Abu Dhabi, line E101).
- **One-way trip:** From and To station menus with a swap button, travel date, time period (morning, afternoon, evening, night) with the number of departures in each, then departure cards with arrival time, duration, seats left and fare. Passengers: adult, child (half fare), student (half fare), person of determination (free).
- **Multi-trip:** 5-trip and 10-trip cards, weekly and monthly unlimited, for the chosen route, each showing the saving.
- **Favourites:** saved routes with Book this route. Save route on the one-way tab adds one.
- **Route and map:** the stop list from departure to arrival (with Show full route), next to a route diagram with the journey highlighted and the departure and arrival marked.

---

## Flow review (28 Sep): repeated steps removed

Every flow on every venue was walked step by step to find anything asked twice or split across steps for no reason.

- **Add-ons asked twice.** Some flows had add-ons on the ticket page and again on the Add-ons step (for example, Summit Peaks Fast Track and lockers, the Kids Club workshop chaperone, House of Pages coffee and AV). All add-ons now sit on the Add-ons step only, and duplicates such as "Large locker" appear once.
- **Cabana chosen twice.** The cabana flow asked for a cabana zone, then asked again on the map. The zone step is gone: the guest picks the cabana on the map, which sets the zone and price. The rentals list moved to Add-ons, where the same items already were.
- **Dinner event table zone chosen twice.** The Table zone choice before the table map is gone. The zone is picked on the map.
- **Height asked twice.** The Summit Peaks height gate asked for the tallest guest, then checked every guest's height in the eligibility check. The first question is gone.
- **Water park heights asked twice.** The day pass priced each guest by height band and then asked every guest's height again in the eligibility check. The height bands are the check now, so the second question is gone.
- **Dinner deals on three screens.** Party size now sits with the date and time, so the flow is two screens: when and how many, then the offer.
- **Party and school details typed twice.** The birthday party and school trip summary now fills in the headcount, child's name and age from the form the guest already filled in.
- **Steps with nothing to decide.** On the one-decision-per-screen layout (Saffron Table, Kids Club), information blocks (notes, "what happens next", "what's included") no longer get a screen of their own. They stay on the screen before them, and up to three quick choices share one screen. The result:
  - Table reservation: 2 screens to 1 (date, time, party size).
  - Deposit hold: 2 to 1.
  - Waitlist, Takeaway, Delivery and Private dining enquiry: 3 to 2 each.
- **Show and seats on one step (theatre).** Already done: picking the performance and the seats happens on one page.

Flows that were already one decision per step, with nothing repeated, are unchanged.

---

## Still needed from you

- The real station list, fares and timetable for transport. The prototype uses sample stations and a flat per-stop fare.

---

## Update 28 Sep

- **Basket in Arabic.** Confirmed: the basket stays on the right in Arabic. This is the default, and it can still be switched to "Mirror to left" in Config.
- **Arabic copy.** Interface text added in the Rev 3 round now has Arabic, stored in a separate file (ticvai-ar-rev3.js) so it can be edited without touching the prototype.

## Built to match your examples (28 Sep)

Each item below now follows the screenshot in the feedback document.

- **Swim question (water park).** A pop-up in the venue's own theme asks "Are you able to swim?" with "Yes, I can swim" / "No, I can't swim" and Next. It appears once, after the guest picks a session or date, on any water park flow. "Yes" clears the swimmer check for the booking. Config: **Swim consent pop-up (water park)** (on/off).
- **Help me choose banner.** Below the products, a dark banner reads "Choose from the experiences above or let us help you decide", with a HELP ME CHOOSE button that opens the questions.
- **Book a cabana from the map.** Coastal Aqua → *Cabana & locker rentals*. The map is on the first screen, under the date and party. It uses the water park map, with 34 numbered cabanas across Riverside (R01–R10), Tower (T01–T08), Splash Zone (S01–S06) and Beach (B01–B10). Each cabana shows how many guests it seats. Sold-out cabanas are greyed and marked. Tapping an available one adds it to the basket (for example "Cabana B09 · Large cabana · Beach, AED 1,855"), and a "Remaining time" counter starts.
- **Surf sessions.** A four-day calendar ("26 Sept – 29 Sept", with arrows to move a week) shows sessions stacked by time in each day column, with places left and price. The two dropdowns, **Choose your experience** and **Select surf level**, show a short description under each option. A Reset button clears both.
- **Transport.** The screen follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), "01 · Step 1 of 3 · Select Bus Station, Route & Schedule", the One-way Trip / Multi-Trip / Favourite tabs, and a single row with From, To, Select Date & Time and Passengers. **Search Trips** lists departures. **Next Available Trip** picks the next departure straight away. The chosen trip shows a price card (E101-Out, departure, arrival, seats available) next to a street map with the route, the departure pin and the arrival pin. The map needs an internet connection.

The mobile prototype has matching screens in Account → All screens → Rev 3 feedback (now 25 screens): Swim consent pop-up, Help me choose banner and Cabana map are new, and Surf sessions and Intercity bus are updated.
