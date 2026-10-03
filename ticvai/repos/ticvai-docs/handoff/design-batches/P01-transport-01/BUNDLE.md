# P01-transport-01 — P01 · Transport

**1 screens · 13 operations · 24 schemas · 0 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale)

A guest finds something to do, picks when and how many, holds capacity, pays, and receives a ticket they can show at the gate, transfer or resell. The same booking engine serves the guest website (P01, WEB-), the guest app (P02, GST-) and, through the same catalogue, cart and order operations, the kiosk (P05), the cashier at the till (P04) and the staff handheld (P06); partners book on credit through the partner portal (P10). Guest surfaces are white-label (venue logo, colours, fonts, card layouts, step indicator style, cart placement) with "Powered by TICVAI" kept; the till and handheld stay TICVAI-branded. The booking runs in a fixed order that the client set on 29 September and confirmed on 30 September: for a dated product, the date first, then the time (hidden until a date), then the tickets (hidden until a time); undated products go straight to the tickets; product-first flows (workshops) pick the product, then the date; seated events with one performance open on the seat map, sections first, zoom into a section, pinch out to compare. Choosing a date, time or session commits nothing; capacity is held only when a quantity is set (a 15-minute basket window, 8 minutes for seats and cabanas, one extension). The guest counters (adult, child, senior, infant, person of determination) belong to the chosen ticket and take its prices, so a basket line is "<ticket> · <guest type> × <n>"; group and school products start from group ticket cards and a typed headcount (minus, plus, and +10 on the app), supervisors free. Help me choose filters the catalogue on the server (never a consent step) with Show everything; consent questions such as "Are you able to swim?" are asked once after the session is picked and never again where the page already asked. Sign-in or the six-digit guest code is asked when the guest leaves Add-ons (or at payment, per venue), only the fields the venue configured; after the code, only the T&Cs tick remains (W1). Payment creates the order first and treats an unknown outcome as "checking with your bank", never a second charge; tickets issue on payment, go to Apple or Google Wallet, and a dynamic-QR event's ticket lives in the app. The guest app is deliberately not a copy of the website (30 September): its structure is Home, Explore, Plan and Tickets tabs with a persistent Buy tickets button, item pages that propose the right product (a restaurant's meal combo that includes admission), ride videos that play with no loader, a visit planner that plans each day at one park from that park's rides, dining and shops only, and in-park walking navigation; the booking flow inside it is functionally identical to the web. Vocabulary in guest copy follows the glossary's recorded exceptions (Booking, Session, QR). source: [F01, F02, F03, F07, F49, F52, F55, F57, F58, F59, MoM 29 Sep 1 (W1-W12), MoM 29 Sep 2, MoM 29 Sep 3, MoM 30 Sep 4.4-4.8, CLIENT-RESPONSE-30SEP 1-6, CLIENT-RESPONSE-REV3-25SEP, REV3-1, REV3-2, REV3-3, REV3-4, REV3-26, DI-1086 …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Booking | An order or reservation as the guest reads it (Booking Confirmation, Group Booking, My bookings). Code says Order or Reservation. | Order (in guest copy), Purchase record, Transaction | docs/glossary.md (Recorded exceptions, Booking, audit R145) |
| Session | A dated, timed performance as the guest reads it (Pick a session, Surf sessions). Staff screens (POS, back office) keep Performance. | Slot, Showtime, Performance (in guest copy) | docs/glossary.md (Recorded exceptions, Session, rev 3 CFG-10); DI-1064 |
| Basket | The guest's unpaid selection with its held capacity (Add to basket, Your basket). Never a paid order. The till and staff screens say Cart. | Cart (in guest copy), Bag, Order (for an unpaid selection) | CLIENT-RESPONSE-REV3-25SEP (Basket, 10) … |
| Ticket | The issued instrument a guest shows at the gate. Product names from the catalogue keep their own words (Day Pass, Annual pass, 2 park ticket); the interface around them says ticket. | Admission, Voucher (for a ticket), Pass (in interface copy) | docs/glossary.md (Ticket) |
| Adult, Child, Senior, Infant, Person of determination | The guest types of a ticket, each with its age or height band shown under it (Child 3-12, Under 1.20 m). A companion of a person of determination is its own free type where the product has one. | Disabled, Handicapped, Kid, Pax | DI-686; screens/P01-guest-web-storefront.yaml#WEB-049 (Passengers notes) … |
| Held for | The countdown on held capacity ("Your seats are held for 7:42"); the release is Release hold. | Lease, Reserved for (a reservation is a different thing), Locked | contracts/spine/orders.yaml#/components/schemas/CartLine (leaseExpiresAt) … |
| Reservation | Booked and not yet paid; holds capacity and expires (My Reservations). Paid tickets are in Tickets or My Tickets. | Booking (for an unpaid hold in lists), Pending order | docs/glossary.md (Reservation); DI-199 |
| Help me choose | The venue's questions whose answers filter the products; Show everything clears them. | Quiz, Wizard, Experience builder, Consent | MoM 29 Sep W4; REV3-11 |
| Info only / Not bookable online | A product listed with full details that cannot be booked online; it shows Contact sales to book with Call sales and Email sales. | Unavailable, Sold out, Coming soon | REV3-14; MoM 29 Sep W3 |
| Guest code | The six-digit code sent to the guest's email or mobile to prove the contact at guest checkout; the copy says six digits. | OTP, PIN, Token, Verification key | DI-1034; MoM 29 Sep W1 |
| How many people | The typed headcount of a group or school booking (number box with minus and plus; +10 on the app), with Supervisors listed separately and free. | Group size (the removed dropdown), Pax | DI-1104; DI-1105; CLIENT-RESPONSE-30SEP 1 |
| Waiting room | The on-sale queue in front of a high-demand performance's sale (WEB-015, GST-046). | Virtual queue (that is the ride queue), Lobby | screens/P01-guest-web-storefront.yaml#WEB-015 notes (ADR-0066) |
| QR | The code a guest shows, in guest copy only (Dynamic QR). Staff screens say Media code. | Barcode, Serial, Media code (in guest copy) | docs/glossary.md (Recorded exceptions, QR, audit R210) |
| Not at this park | The planner's per-day notice that the day's park cannot meet a preference, naming the park that can. | Unavailable, No results | DI-1113 |
| Book this plan | Turns the whole visit plan (tickets, Fast Track, meal combos) into basket lines. | Checkout plan, Buy itinerary | screens/P02-guest-mobile-app.yaml#GST-053 (Book this plan) |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-049` | Transport — Route & Schedule | A | 29 | 66 | 6 | 4 | 5 | 6 | guest | review (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-049` Transport — Route & Schedule

**Find a departure between two stations and buy a trip, a multi-trip or unlimited pass, or rebook a saved route.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Transport · wave 1 · needs the `transport` module |
| Block | Block A · task APP-WEB-WEB-049 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `searchTransportDepartures` reads the population of departures and one is chosen for a price card and a route — list, select, act; the prototype draws one-way, multi-trip and favourites as tabs of … |
| Offline | **The offline banner shows.** A route's stop list and schematic line already loaded stay readable with their age; the street map needs the connection. Searching departures, buying a trip or a pass and saving a favourite route need the connection. |
| Opens with | `cartId` (session), `favouriteId` (navigation), `routeId` (navigation) · cold entry: Arrives with nothing; the venue comes from the site. **Opened from a route** (a route card or a transport product, client feedback 30 September), `routeId` … |
| Route | `/transport/route-and-schedule` |

**What the spec says about it.** **New 29 September** (decided 29 September, rev 3 REV3-21: transport ticketing is in scope — stations, routes, timetabled departures, one-way trips, multi-trip passes, favourite routes and a route map). **One-way:** From and To stations with a swap, the travel date (timetables are released 30 days ahead), the passengers (adult; child and student half fare; a person of determination travels free — proof is checked by the driver at boarding), a time period with its departure count, then departure cards (departs, arrives, duration, seats left, fare). **Next Available Trip** jumps to the first departure with room. A chosen departure shows a price card and the stop list with *Show full route* and a street map. **The street map needs the internet** and a third-party tile provider approved under audit R038; the stop list and schematic line need neither. Buying a trip is `addCartLine` with `attributes.transport` (route, stations, passenger type); the price comes from `quoteTransportFare`, and a departure with a seat map goes through seat selection on its `performanceId`. **Multi-trip:** 5- and 10-trip cards and weekly or monthly unlimited passes for the station pair, with the saving. **Favourites:** saved routes, *Book this route* prefills one-way; remove. *Change your trip free up to two hours before departure* is the proposed default of the venue's modification policy, client to correct. **The real network (stations, fares, timetable) is an open value from the client**; the prototype's Emirates Link data is illustrative. **30 September (client feedback, CLIENT-RESPONSE-30SEP 5 …

**Known gaps.**  Open: The real network — stations, routes, fares and timetable — is an open value from the client (decided 29 September, rev 3 REV3-21); the prototype's Emirates Link stations and prices are illustrative. The street-map tile provider needs approval under audit R038; the approver is still to be named by the client.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Buy intercity coach travel (Emirates Link): a one-way trip, a multi-trip or unlimited pass, or a saved favourite route. Block A. The 30 September feedback changed the order: a route opens with its stations filled in, departures list at once without a search, and passengers appear only after a departure is chosen. The proposed Popular routes card view (route cards with a from-fare and Book) is the first transport screen.

**Fixed on main** (the package already carries these; draw what it says): The layout keeps Passengers in the top filter row and a primary "Search Trips" button. (CHG-SGU-020).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are each popular route's from-fare, featured order and image set per route in the back office?** → Drawn default accepted: Routes carry a featured order and an image; the from-fare is the lowest fare. *(decided by Chinmay, 2026-10-02; DEC-123 / CHG-NOTE-007)*
- **Who approves the street-map tile provider?** → Drawn default accepted: Draw the map; hide it offline. *(decided by Chinmay, 2026-10-02; DEC-124 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Trip type | select field | — | — | — | — | One-way trip, Multi-trip, Favourites (tabs). | — |
| From | select field | — | — | — | — | — | — |
| To | select field | — | — | — | — | — | — |
| Travel date | date picker | — | — | — | — | Timetables are released 30 days ahead. | — |
| Time period | select field | — | — | — | — | Morning, Afternoon, Evening, Night, each with its count of departures. | — |
| Passengers | number field | — | — | — | — | Asked after a departure is chosen (DI-1110): Adult, child 5-11 and student at half fare, person of determination free (one companion at the adult fare); proof is checked at boarding. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include inactive | toggle | off | — | `listTransportStations` ?includeInactive |
| At | date and time picker | — | — | `getTransportFareTable` ?at |
| From station | picker: choose a from station | — | — | `searchTransportDepartures` ?fromStationId |
| To station | picker: choose a to station | — | — | `searchTransportDepartures` ?toStationId |
| Date | date picker | — | — | `searchTransportDepartures` ?date |
| Period | radio group | — | Morning · Afternoon · Evening · Night | `searchTransportDepartures` ?period |
| Passengers | list of values (chips) | — | at most 10 | `searchTransportDepartures` ?passengers |
| From station | picker: choose a from station | — | — | `getTransportRouteMap` ?fromStationId |
| To station | picker: choose a to station | — | — | `getTransportRouteMap` ?toStationId |
| From station | picker: choose a from station | — | — | `listTransportPassOffers` ?fromStationId |
| To station | picker: choose a to station | — | — | `listTransportPassOffers` ?toStationId |

**Form: Remove favourite** (confirmDialog, opened by *Remove favourite*; *Remove* calls `deleteFavouriteRoute`, *Keep it* sends nothing)

**Remove this saved route?** It leaves Favourites; nothing already booked on it changes.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Sent by *Add to basket*** (`addCartLine`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

**Sent by *Save route*** (`saveFavouriteRoute`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `saveFavouriteRoute` body |
| From station `fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | — | `saveFavouriteRoute` body |
| To station `toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | — | `saveFavouriteRoute` body |
| Label `label` | text field | optional | — | max length 60 | — | — | `saveFavouriteRoute` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Popular routes**: Route cards styled like the dated ticket cards, each with its from-fare, image or badge and Book. Book, then the date, then that route's departures, then passengers. *(source: DI-1111; CLIENT-RESPONSE-30SEP 6; DI-1119)*
- **From and To**: Prefilled with the route's first and last stops when entered from a route (e.g. E201 Abu Dhabi Central Bus Station to Al Ain Central Bus Station); still changeable, with a swap button that also picks the paired route the other way. *(source: DI-1109; CLIENT-RESPONSE-30SEP 5)*
- **time period**: Morning, Afternoon, Evening, Night chips with their departure counts acting as filters; tapping the selected chip again shows all departures. Departures load on open and on every change; no Search Trips needed. *(source: DI-1109)*
- **passengers**: Only after a departure is chosen. Adult; child 5-11 and student at half fare; person of determination free with one companion at the adult fare; proof checked at boarding. *(source: DI-1110; screens/P01-guest-web-storefront.yaml#WEB-049 (Passengers notes))*
- **travel date**: Timetables are released 30 days ahead; later dates are disabled with that reason. *(source: screens/P01-guest-web-storefront.yaml#WEB-049 (Travel date notes))*

#### Outputs: what the screen shows and produces

**Shown**

**Departures** (card list, from `searchTransportDepartures`): Departures list as soon as From, To and the date are set; there is no Search button (DI-1109).

| Shows | Format | Notes |
|---|---|---|
| Route code | text | The price card's label, e.g. `E101-Out`. |
| Departs at | 1 Oct 2026, 14:30 | At the boarding stop. |
| Arrives at | 1 Oct 2026, 14:30 | At the alighting stop. |
| Duration minutes | 1,234 | — |
| Seats left | 1,234 | Catalogue availability for the performance. Display only; the hold decides the sale. |
| Fare | AED 1,234.50 | One adult, one way. |

**Multi-trip cards** (card list, from `listTransportPassOffers`): The Multi-trip tab.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Trips | 1,234 | — |
| Validity days | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Saving | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Favourite routes** (card list, from `listMyFavouriteRoutes`): The Favourites tab; *Book this route* prefills the one-way tab. Signed-in guests only.

| Shows | Format | Notes |
|---|---|---|
| From station name | text | — |
| To station name | text | — |
| Adult fare | AED 1,234.50 | The current fare, read on list. |

**Price card** (detail panel, from `quoteTransportFare`): Line code and direction (e.g. E101-Out), departs, arrives, seats available, fare per passenger type and total.

| Shows | Format | Notes |
|---|---|---|
| Route | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Stops travelled | 1,234 | — |
| Adult fare | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Lines | list or chips (count when long) | — |
| Code | text | — |
| Catalogue variant | the name it points at, never the id | — |
| Count | 1,234 | — |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Line total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Pass type | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Saving | AED 1,234.50 | With `passTypeId`, single adult fare × `referenceTrips` minus the pass price. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Stops** (timeline, from `getTransportRouteMap`): From and To with the stops between folded: *Show full route (n stops)*.

| Shows | Format | Notes |
|---|---|---|
| Route | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Line code | text | — |
| Colour | text | — |
| Stops | list or chips (count when long) | Every stop in route order. |
| Station | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Sequence | 1,234 | — |
| Name | text | Localised to the caller. |
| Short name | text | — |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Offset minutes | 1,234 | — |
| On journey | yes / no (icon or chip) | Between the boarding and alighting stops |
| Is boarding | yes / no (icon or chip) | — |
| Is alighting | yes / no (icon or chip) | — |
| Intermediate stop count | 1,234 | Stops between boarding and alighting — the number behind "Show full route (n stops)". |
| Bounds | grouped details | The box around the stops with coordinates, for the map's initial view. |
| South | 1,234.5 | — |
| West | 1,234.5 | — |
| North | 1,234.5 | — |
| East | 1,234.5 | — |

**Street map** (detail panel, from `getTransportRouteMap`): Needs the internet and a third-party tile provider approved under audit R038; hidden offline, where the stop list and schematic line remain.

| Shows | Format | Notes |
|---|---|---|
| Route | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Line code | text | — |
| Colour | text | — |
| Stops | list or chips (count when long) | Every stop in route order. |
| Station | the name it points at, never the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order … |
| Sequence | 1,234 | — |
| Name | text | Localised to the caller. |
| Short name | text | — |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Offset minutes | 1,234 | — |
| On journey | yes / no (icon or chip) | Between the boarding and alighting stops |
| Is boarding | yes / no (icon or chip) | — |
| Is alighting | yes / no (icon or chip) | — |
| Intermediate stop count | 1,234 | Stops between boarding and alighting — the number behind "Show full route (n stops)". |
| Bounds | grouped details | The box around the stops with coordinates, for the map's initial view. |
| South | 1,234.5 | — |
| West | 1,234.5 | — |
| North | 1,234.5 | — |
| East | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Swap stations (icon button) | `listTransportRoutes` GET `/transport/routes` | — | TransportRoute (paged) | — | — |
| Next Available Trip (secondary button) | `getNextTransportDeparture` GET `/transport/departures/next` | — | DepartureOffer | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 The stations are the same, or no active route serves them in this order. | — |
| Add to basket (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | — |
| Save route (secondary button) | `saveFavouriteRoute` POST `/transport/favourite-routes` | inline | FavouriteRoute | 409 The guest already has the maximum number of saved routes.; 422 The stations are the same, or no active route serves them in this order. | — |
| Remove favourite (destructive button) | `deleteFavouriteRoute` DELETE `/transport/favourite-routes/{favouriteId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens confirmDialog first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **departure card**: Departs and arrives (24-hour), duration, seats left, fare from; a full departure greyed, not hidden. *(source: REV3-21; DI-1061)*
- **price card and route**: Line and direction (E101-Out), departs, arrives, seats available, fare per passenger type and total; the stop list with "Show full route (n stops)" and a street map that needs the internet (hidden offline, the stop list and schematic line remain). *(source: screens/P01-guest-web-storefront.yaml#WEB-049 contextPanel)*
- **multi-trip cards**: 5-trip, 10-trip, weekly and monthly unlimited for the station pair, each with the saving against single fares. *(source: REV3-21; AUDIT-29SEP (Transport))*
- **change policy line**: "Change your trip free up to two hours before departure" (proposed default, client to correct). *(source: screens/P01-guest-web-storefront.yaml#WEB-049 notes)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Next available trip**: Selects the first departure with room for the party. *(source: contracts/satellite/transport.yaml#getNextTransportDeparture)*
- **Choose seats**: For a departure with a seat map, step 2 of 3 opens the seat map (WEB-007) on that departure. *(source: screens/P01-guest-web-storefront.yaml#WEB-049 transitions)*
- **Save route**: Adds to Favourites (signed-in only); Book this route prefills the one-way tab. *(source: REV3-21)*

**Data it reads**: `listTransportStations` (onLoad, The stations to pick From and To); `getTransportFareTable` (onLoad, Passenger types and fares of the route); `searchTransportDepartures` (onLoad, Departures for the stations, date, period and party, with …); `getTransportRoute` (onLoad, The route and its stops); `getTransportRouteMap` (onLoad, Stop list, line and bounds for the map); `listTransportPassOffers` (onLoad, Multi-trip and unlimited passes for the station pair); `listMyFavouriteRoutes` (onLoad, The guest's saved routes Only when signed in (decided 2 …)

**Where the user goes next**

- → `WEB-007` Interactive Seat Selection: *Choose seats on this departure*; carries `performanceId`; only when the departure has a seat map
- → `WEB-010` Shopping Cart: *Continue to payment*; carries `cartId`; calls `addCartLine`
- → `WEB-016` Login / Register: *Sign in to save or see favourite routes*; carries `subjectId`
- → `WEB-001` Home / Landing: *Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stations, routes and passenger types. |
| Error (`?state=error`) | Could not load. Names which read failed; nothing is bought. |
| Empty, first run (`?state=emptyFirstRun`) | **No routes are published for this venue yet.** Says so; the client still owes the real network (stations, fares, timetable). |
| Empty, no results (`?state=emptyNoResults`) | No departure in that period. Names the period and offers **Next Available Trip** or another period or date. |
| Permission denied (`?state=emptyNoAccess`) | Searching and buying need no account. **Favourites need a signed-in guest**: a guest who is not signed in is offered sign-in and brought back, never shown an empty list. |
| Offline (`?state=offline`) | **The offline banner shows.** A route's stop list and schematic line already loaded stay readable with their age; the street map needs the connection. Searching departures, buying a trip or a pass and saving a favourite route need the connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 409 The guest already has the maximum number of saved routes.; 422 A station is not on this route, or the alighting stop comes before the boarding stop.; 422 Stations not on the route or in the wrong order, an unknown passenger type, no passengers, or a pass type not offered on this route. |

#### Edge cases to draw

- **No departure in the chosen period**: Names the period and offers Next available trip, another period or date. *(source: screens/P01-guest-web-storefront.yaml#WEB-049 states.emptyNoResults)*

#### Consistency with other screens

- Match `GST-076`: Same route cards first, same prefilled stations and passengers-after-departure order.
- Match `GST-077`: The app splits route and passengers onto their own screen; the order is the same.
- Match `GST-078`: Multi-trip passes, same cards.
- Match `GST-079`: Favourites, same Book this route.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
routes:
- route: Dubai to Abu Dhabi · E101
  from: AED 25
- route: Sharjah to Dubai
  from: AED 10
- route: Abu Dhabi to Al Ain · E201
  from: AED 28
- route: Dubai to Fujairah · E700
  from: AED 30
departure: E201-Out · 07:30 → 09:10 · 1 h 40 m · 18 seats left
passengers: Adult × 2, Child × 1 (half fare)
```

#### Permissions

- `listTransportStations` → no permission · guest, public, staff
- `listTransportRoutes` → no permission · guest, public, staff
- `getTransportFareTable` → no permission · guest, public, staff
- `searchTransportDepartures` → no permission · guest, public
- `getNextTransportDeparture` → no permission · guest, public
- `getTransportRoute` → no permission · guest, public, staff
- `getTransportRouteMap` → no permission · guest, public
- `quoteTransportFare` → no permission · guest, public, service
- `listTransportPassOffers` → no permission · guest, public
- `listMyFavouriteRoutes` → no permission · guest
- `saveFavouriteRoute` → no permission · guest
- `deleteFavouriteRoute` → no permission · guest
- `addCartLine` → no permission · guest, partner, staff

**A refused user sees:** Searching and buying need no account. **Favourites need a signed-in guest**: a guest who is not signed in is offered sign-in and brought back, never shown an empty list.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)*
- Transport "Popular routes" card view: cards per route (e.g. Dubai to Abu Dhabi, Sharjah to Dubai, Abu Dhabi to Al Ain, Dubai to Fujairah) styled like the dated ticket cards, each with the "from" fare and a Book button. Book → date → departures → passengers. On mobile it is the first transport product. *(client request · design review 30 Sep 2026, 6. Proposed UI: route cards with a Book button · DI-1111)*
- Transport passengers appear only after a departure is chosen (performance first, then tickets). *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1110)*
- A route flow opens with its stations filled in (e.g. Abu Dhabi Central Bus Station → Al Ain Central Bus Station, still changeable/swappable) and departures show straight away without Search Trips. Time-period buttons act as a filter; tapping one again shows all departures. *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1109)*
- Transport (intercity coach) follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), tabs One-way Trip / Multi-Trip / Favourite, one row with From (swap), To, Date & Time, Passengers; departure cards (arrival, duration, seats left, fare); price card beside a street map of the route. *(agreed · rev 3 design review 29 Sep 2026, REV3-21 · 21. Sell transport tickets (one trip, multi trip, favourites, stations, route map) · DI-1061)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-049` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Engine controls → Transport → Route & schedule · one-way, multi-trip, favourites → Book → Fri (stations filled in, departures without a search)*. Differences: 30 September: the route opens with its stations filled in and the departures listed without a search; the time-period buttons filter them. The engine's other transport flow, Popular routes (card view), is route cards with a from-fare and Book, then the date, the departures and the passengers. The route map needs a street-map tile provider (audit R038).
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (66 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Swap stations, Next Available Trip, Add to basket, Save route, Remove favourite.
- [ ] Every transition is wired: `WEB-007`, `WEB-010`, `WEB-016`, `WEB-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | body text on the background |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-009` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-009` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-009` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-009` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-009` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-009` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-009` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-009` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-009` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001`, `ADM-424` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Decided for every guest screen:** **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035). ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036). **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040). **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

**Never configurable:** A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"deleteFavouriteRoute": {"method":"DELETE","path":"/transport/favourite-routes/{favouriteId}","contract":"transport","summary":"Remove a saved route","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getNextTransportDeparture": {"method":"GET","path":"/transport/departures/next","contract":"transport","summary":"Next Available Trip","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"fromStationId","in":"query","required":true},{"name":"toStationId","in":"query","required":true},{"name":"after","in":"query","required":null},{"name":"passengers","in":"query","required":null}],"requestBody":null,"responds":"DepartureOffer"},
"getTransportFareTable": {"method":"GET","path":"/transport/routes/{routeId}/fare-table","contract":"transport","summary":"A route's fares and passenger types","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":false}],"requestBody":null,"responds":"FareTable"},
"getTransportRoute": {"method":"GET","path":"/transport/routes/{routeId}","contract":"transport","summary":"A route with its stops","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TransportRoute"},
"getTransportRouteMap": {"method":"GET","path":"/transport/routes/{routeId}/map","contract":"transport","summary":"The route drawn for a map, with the journey highlighted","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"fromStationId","in":"query","required":null},{"name":"toStationId","in":"query","required":null}],"requestBody":null,"responds":"RouteMap"},
"listMyFavouriteRoutes": {"method":"GET","path":"/transport/favourite-routes","contract":"transport","summary":"The caller's saved routes","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportPassOffers": {"method":"GET","path":"/transport/pass-offers","contract":"transport","summary":"Multi-trip passes for a pair of stations, priced, with the saving","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"fromStationId","in":"query","required":true},{"name":"toStationId","in":"query","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportRoutes": {"method":"GET","path":"/transport/routes","contract":"transport","summary":"Routes, optionally those serving a pair of stations","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"fromStationId","in":"query","required":null},{"name":"toStationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTransportStations": {"method":"GET","path":"/transport/stations","contract":"transport","summary":"Stations of a venue's transport network","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"quoteTransportFare": {"method":"POST","path":"/transport/fare-quotes","contract":"transport","summary":"Price a one-way trip or a pass for a party","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":"FareQuoteRequest","responds":"FareQuote"},
"saveFavouriteRoute": {"method":"POST","path":"/transport/favourite-routes","contract":"transport","summary":"Save route","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FavouriteRoute"},
"searchTransportDepartures": {"method":"GET","path":"/transport/departures","contract":"transport","summary":"Search Trips — departures between two stations on a date","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"fromStationId","in":"query","required":true},{"name":"toStationId","in":"query","required":true},{"name":"date","in":"query","required":true},{"name":"period","in":"query","required":null},{"name":"passengers","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"CreateStationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","code","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"Short operator code, e.g. `SHJ-JUB`. Unique in the venue."},"name":{"$ref":"#/components/schemas/LocalisedText"},"shortName":{"$ref":"#/components/schemas/LocalisedText","description":"The label on the route diagram and the map pin (`Union Sq`, `MoE`)."},"latitude":{"type":"number","minimum":-90,"maximum":90,"nullable":true},"longitude":{"type":"number","minimum":-180,"maximum":180,"nullable":true}}},
"CreateTransportRouteRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","code","name","stops"],"properties":{"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"The line and direction, e.g. `E101-Out`. Unique in the venue."},"lineCode":{"type":"string","maxLength":16,"description":"The public line number shared by both directions, e.g. `E101`."},"name":{"$ref":"#/components/schemas/LocalisedText"},"colour":{"type":"string","pattern":"^#[0-9a-fA-F]{6}$"},"pairedRouteId":{"type":"string","format":"uuid","nullable":true,"description":"The same line run the other way. The swap button lands on it."},"bookingCutoffMinutes":{"type":"integer","minimum":0,"maximum":1440,"default":5,"description":"How long before a departure leaves the boarding stop that online sale stops. Proposed default 5, from the prototype's \"Boarding closes five minutes before departure\", client to correct (rev 3 REV3-21).\n"},"stops":{"type":"array","minItems":2,"maxItems":100,"items":{"$ref":"#/components/schemas/RouteStopInput"}}}},
"DepartureOffer": {"x-ticvai-persistence":"none — projection","type":"object","required":["departureId","performanceId","routeId","departsAt","arrivesAt","durationMinutes","seatsLeft","fare","period"],"properties":{"departureId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"performanceId":{"type":"string","format":"uuid"},"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"routeCode":{"type":"string","description":"The price card's label, e.g. `E101-Out`."},"departsAt":{"type":"string","format":"date-time","description":"At the boarding stop."},"arrivesAt":{"type":"string","format":"date-time","description":"At the alighting stop."},"durationMinutes":{"type":"integer","minimum":0},"period":{"$ref":"#/components/schemas/TimePeriod"},"seatsLeft":{"type":"integer","minimum":0,"description":"Catalogue availability for the performance. Display only; the hold decides the sale."},"fitsParty":{"type":"boolean"},"fare":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"One adult, one way."},"partyTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FareQuote": {"x-ticvai-persistence":"none — computed","type":"object","required":["routeId","stopsTravelled","adultFare","total"],"properties":{"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"stopsTravelled":{"type":"integer","minimum":1},"adultFare":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["code","count","unitPrice","lineTotal"],"properties":{"code":{"type":"string"},"catalogueVariantId":{"type":"string","format":"uuid"},"count":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"passTypeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"saving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"With `passTypeId`, single adult fare × `referenceTrips` minus the pass price."},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FareQuoteRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["fromStationId","toStationId"],"properties":{"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id","description":"Omitted, the active route serving the two stations in this order."},"fromStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"toStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"passengers":{"type":"array","maxItems":10,"description":"Omitted, one of the default type. Ignored with `passTypeId`.","items":{"type":"object","required":["code","count"],"properties":{"code":{"type":"string"},"count":{"type":"integer","minimum":0,"maximum":99}}}},"passTypeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"travelAt":{"type":"string","format":"date-time","description":"**When the trip is travelled** (the departure's time; for a pass, its first valid day). The fare table in force at this instant prices the quote (CHG-RUL-012). Default `at`, else now.\n"},"at":{"type":"string","format":"date-time","deprecated":true,"description":"Deprecated on 3 October (CHG-RUL-012): quotes price at travel time, so send `travelAt`. Kept for clients built at r1; read as `travelAt` when `travelAt` is absent.\n"}}},
"FareTable": {"x-ticvai-persistence":"transport.fare_table + transport.fare_passenger_type + transport.fare_matrix_cell","allOf":[{"$ref":"#/components/schemas/SetFareTableRequest"},{"type":"object","required":["id","routeId"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the next version takes over; null when none is set (CHG-RUL-012). Versions of a route never overlap: one table is in force at any instant.\n"},"upcoming":{"type":"object","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The next version, set and not yet in force (CHG-RUL-012); null when none.","properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"effectiveFrom":{"type":"string","format":"date-time"}}}}}]},
"FavouriteRoute": {"x-ticvai-persistence":"transport.favourite_route","type":"object","required":["id","venueId","fromStationId","toStationId","createdAt"],"description":"Unique per guest, venue and ordered pair of stations.","properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"venueId":{"type":"string","format":"uuid"},"fromStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"toStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"fromStationName":{"type":"string","readOnly":true},"toStationName":{"type":"string","readOnly":true},"label":{"type":"string","nullable":true},"adultFare":{"$ref":"../shared/common.yaml#/components/schemas/Money","readOnly":true,"x-ticvai-persisted":false,"description":"The current fare, read on list."},"createdAt":{"type":"string","format":"date-time"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PassOffer": {"x-ticvai-persistence":"none — projection","type":"object","required":["passTypeId","catalogueProductId","name","price","validityDays"],"properties":{"passTypeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"catalogueProductId":{"type":"string","format":"uuid"},"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"name":{"type":"string"},"description":{"type":"string"},"kind":{"type":"string","enum":["multiTrip","unlimited"]},"trips":{"type":"integer","nullable":true},"validityDays":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"saving":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"RouteMap": {"x-ticvai-persistence":"none — projection","type":"object","required":["routeId","stops"],"properties":{"routeId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"lineCode":{"type":"string"},"colour":{"type":"string"},"stops":{"type":"array","description":"Every stop in route order.","items":{"type":"object","required":["stationId","sequence","name","onJourney"],"properties":{"stationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"sequence":{"type":"integer"},"name":{"type":"string","description":"Localised to the caller."},"shortName":{"type":"string"},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"offsetMinutes":{"type":"integer"},"onJourney":{"type":"boolean","description":"Between the boarding and alighting stops","inclusive.":null},"isBoarding":{"type":"boolean"},"isAlighting":{"type":"boolean"}}}},"intermediateStopCount":{"type":"integer","description":"Stops between boarding and alighting — the number behind \"Show full route (n stops)\"."},"bounds":{"type":"object","nullable":true,"description":"The box around the stops with coordinates, for the map's initial view.","properties":{"south":{"type":"number"},"west":{"type":"number"},"north":{"type":"number"},"east":{"type":"number"}}}}},
"RouteStop": {"x-ticvai-persistence":"transport.route_stop","allOf":[{"$ref":"#/components/schemas/RouteStopInput"},{"type":"object","required":["id","sequence"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"sequence":{"type":"integer","minimum":1,"description":"1 for the origin."},"station":{"$ref":"#/components/schemas/Station"}}}]},
"SetFareTableRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["model","passengerTypes","effectiveFrom"],"properties":{"model":{"$ref":"#/components/schemas/FareModel"},"baseFare":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"`stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21)."},"perStopFare":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"`stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21)."},"matrix":{"type":"array","description":"`matrix` only. One adult fare per ordered pair of stops the route serves; the reverse pair is its own row.","items":{"type":"object","required":["fromStationId","toStationId","fare"],"properties":{"fromStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"toStationId":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"fare":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"passengerTypes":{"type":"array","minItems":1,"maxItems":10,"items":{"$ref":"#/components/schemas/PassengerType"}},"effectiveFrom":{"type":"string","format":"date-time"}}},
"Station": {"x-ticvai-persistence":"transport.station","allOf":[{"$ref":"#/components/schemas/CreateStationRequest"},{"type":"object","required":["id","active"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"active":{"type":"boolean","default":true}}}]},
"TimePeriod": {"type":"string","description":"Proposed, client to correct (rev 3 REV3-21): `morning` 05:00–11:59, `afternoon` 12:00–16:59, `evening` 17:00–20:59, `night` 21:00–04:59.\n","enum":["morning","afternoon","evening","night"]},
"TransportRoute": {"x-ticvai-persistence":"transport.route + transport.route_stop","allOf":[{"$ref":"#/components/schemas/CreateTransportRouteRequest"},{"type":"object","required":["id","status"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"status":{"$ref":"#/components/schemas/TransportRouteStatus"},"stops":{"type":"array","items":{"$ref":"#/components/schemas/RouteStop"}},"totalMinutes":{"type":"integer","readOnly":true,"description":"The last stop's offset."},"catalogueEventId":{"type":"string","format":"uuid","readOnly":true,"description":"The catalogue event its departures are performances of. Created with the route."},"catalogueProductId":{"type":"string","format":"uuid","readOnly":true,"description":"The one-way trip product (kind `timedAdmission`); one variant per passenger type. Created with the route.\n"}}}]},
"TransportRouteStatus": {"type":"string","enum":["draft","active","suspended","retired"]}
}
```
