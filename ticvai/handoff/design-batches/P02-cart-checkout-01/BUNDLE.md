# P02-cart-checkout-01 — P02 · Cart & Checkout

**3 screens · 21 operations · 32 schemas · 4 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ORDER_CREATE, ORDER_REPRINT, ORDER_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **7 of these operations work offline**: createOrder, createPayment, getOrder, getPerformance, getPublishedBookingFlow, listProductVariants, reprintOrder
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `GST-009` | Review & Payment | A | 80 | 20 | 5 | 40 | 23 | 0 | guest | notStarted (designed) |
| `GST-010` | Booking Confirmation | A | 10 | 16 | 5 | 15 | 4 | 6 | guest | notStarted (client-verified) |
| `GST-041` | Checkout Entry | A | 12 | 36 | 6 | 23 | 14 | 6 | guest | notStarted (client-verified) |

## Thin screens in this batch

**GST-010 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-009` Review & Payment

**Check what you are buying and pay for it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Cart & Checkout · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17996 (APP-MOB-GST-009) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getCart` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available, and the offline banner says why.** A payment needs the gateway, and pretending otherwise takes money nobody can confirm. What was typed stays on screen so nothing is entered twice. |
| Opens with | `cartId` (session), `orderId` (deepLink), `paymentId` (deepLink), `token` (deepLink), `venueId` (session) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/general/review-and-payment` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createPayment` added 18 August** — the guest app's payment screen did not declare the operation that takes a payment, and F11 routed food payment through the AI concierge instead. **Card or wallet** (TenderKind `card`, `wallet`, as `createPayment` and flow F11 step 4 say; decided 28 September, audit R080 (a)), **both in base currency, so tender currency equals base currency**; a foreign card is converted by the guest's own issuer at their rate, which is not ours and is not recorded as ours. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **No 'is this you?' at checkout** (decided 28 September, audit R120 (b)): a verified contact that matches an existing profile attaches the order automatically inside `checkoutCart` (ADR-0045), so `checkGuestCheckoutMatch` and `decideGuestCheckoutMatch` were removed from this screen; only unverified matches go to staff review. **The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Terms and conditions | consent block | — | — | — | — | **After the code the guest goes straight to the T&Cs tick and completes** (W1): no second name, email or phone form. The profile is created by `checkoutCart` and completed later. | — |
| Send me offers and news | toggle | — | — | — | — | **Marketing opt-in beside the T&Cs, never pre-ticked** (M18-15), sent as `marketingConsents[]` on `checkoutCart`, bound to the order and the verified contact and attached to the profile on match. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getPublishedBookingFlow` ?productId |
| Product category | picker: choose a product category | — | — | `getPublishedBookingFlow` ?productCategoryId |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `getPublishedBookingFlow` ?flowTypeKey |

**Form: Add to cart** (modal, opened by *Add to cart*; *Add to cart* calls `addCartLine`, *Cancel* sends nothing)

**Collects what `addCartLine` sends before it is called; the cart takes the hold server-side.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.

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

Errors to draw in the form: 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem)

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Pay by link** (modal, opened by *Pay by link*; *Pay by link* calls `payByLink`, *Cancel* sends nothing)

**Collects what `payByLink` sends before it is called.** Required: `providerToken`. Optional: `email`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider token `providerToken` | text field | required | — | — | — | — | `payByLink` body |
| Email `email` | email field | optional | — | — | name@example.ae | Optional, and only to send the ticket. Requiring an account before taking money is how a paid booking becomes an abandoned one. | `payByLink` body |

Errors to draw in the form: 409 The hold went while they were paying (`linesUnavailable`). Rare and real — a link near its expiry and a guest reading slowly. (PaymentLinkProblem)

**Form: Transfer order tickets** (modal, opened by *Transfer order tickets*; *Transfer order tickets* calls `transferOrderTickets`, *Cancel* sends nothing)

**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tickets `ticketIds` | multi-picker: choose tickets | required | — | at least 1 | — | The entitlements to hand over. A ticket is an entitlement, so each value is an `Entitlement.id` on this order — the ids in `OrderLine.entitlementIds`. | `transferOrderTickets` body |
| Recipient `recipient` | group | required | — | — | — | — | `transferOrderTickets` body |
| Channel `recipient.channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `transferOrderTickets` body |
| Address `recipient.address` | text field | required | — | — | — | — | `transferOrderTickets` body |
| Message `message` | text area | optional | — | max length 500 | — | — | `transferOrderTickets` body |

Errors to draw in the form: 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem)

**Form: Create payment** (modal, opened by *Create payment*; *Create payment* calls `createPayment`, *Cancel* sends nothing)

**Collects what `createPayment` sends before it is called.** Required: `id`, `orderId`, `tender`, `amount`, `recordedAt`. Optional: `tenderCurrency`, `tenderAmount`, `walletAuthorisationId`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `createPayment` body |
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createPayment` body |
| Tender `tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createPayment` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPayment` body |
| Tender currency `tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `createPayment` body |
| Tender amount `tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `createPayment` body |
| Wallet authorisation `walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `createPayment` body |
| Wallet hold `walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `createPayment` body |
| Return URL `returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `createPayment` body |
| Terminal `terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `createPayment` body |
| Device `deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `createPayment` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPayment` body |

Errors to draw in the form: 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender other than card … (PaymentProblem)

**Form: Checkout cart** (modal, opened by *Checkout cart*; *Checkout cart* calls `checkoutCart`, *Cancel* sends nothing)

**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the order is for. A guest caller may name only themselves (`guestAuth` never widens to another subject); omitted, the cart's own `subjectId` is used. | `checkoutCart` body |
| Marketing consents `marketingConsents` | repeatable rows | optional | — | — | — | Marketing opt-ins given at checkout (29 September, M18-15). Shown unticked beside the terms; one entry per channel and purpose the guest ticked. | `checkoutCart` body |
| Channel `marketingConsents[].channel` | radio group | required | — | Email · SMS · Whatsapp · Push | — | — | `checkoutCart` body |
| Purpose `marketingConsents[].purpose` | text field | required | — | max length 60 | — | The consent purpose code (marketing ConsentPurpose), for example `marketing`. | `checkoutCart` body |
| Granted `marketingConsents[].granted` | toggle | required | — | True only when the guest ticked it. | — | True only when the guest ticked it. Never pre-ticked. | `checkoutCart` body |
| Notice version `marketingConsents[].noticeVersion` | text field | optional | — | max length 40 | — | The version of the consent notice shown. | `checkoutCart` body |
| Attendees `attendees` | repeatable rows | optional | — | — | — | The named holder for each cart line that needs one. Becomes `CreateOrderLine.holderName` on the order's matching line. | `checkoutCart` body |
| Line `attendees[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | A `CartLine.id` in this cart. | `checkoutCart` body |
| Holder name `attendees[].holderName` | text field | required | — | — | — | — | `checkoutCart` body |

Errors to draw in the form: 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 422 A required consent question is unanswered (`consentRequired`), or an answer blocks the booking (`consentAnswerBlocks`), with the lines in `lineIds` (decided 29 … (CartProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Token | text | How an anonymous guest returns to their cart, including from a recovery email. Rotated on claim, so a link shared before signing in does … |
| Venue | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Subject | the name it points at, never the id | Null while anonymous. Set by `claimCart`. |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Conflicts | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**The payment link** (detail panel, from `getPaymentLink`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Issued, Viewed, Paid, Expired, Cancelled, Superseded | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Release hold on expiry | yes / no (icon or chip) | — |

**Booking steps** (progress indicator, from `getPublishedBookingFlow`): The steps of the published flow in their `sortOrder`, this one (review and payment) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.

| Shows | Format | Notes |
|---|---|---|
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer order tickets (primary button) | `transferOrderTickets` POST `/orders/{orderId}/transfer` | inline | TicketTransfer | 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) | opens modal first; produces a document or message: Transfer tickets to another guest |
| Create payment (secondary button) | `createPayment` POST `/payments` | CreatePaymentRequest | Payment | 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender … | emits `payment.captured`, `order.paid`; works offline; opens modal first |
| Inquire payment status (secondary button) | `inquirePaymentStatus` POST `/payments/{paymentId}/inquiry` | — | Payment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Checkout cart (secondary button) | `checkoutCart` POST `/carts/{cartId}/checkout` | inline | Order | 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and … | emits `order.created`; opens modal first |
| Acquire inventory hold (secondary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |
| Create order (secondary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | works offline; opens modal first |
| Pay by link (secondary button) | `payByLink` POST `/payment-links/{token}/pay` | inline | inline | 409 The hold went while they were paying (`linesUnavailable`). Rare and real — a link near its expiry and a guest reading slowly. (PaymentLinkProblem) | opens modal first |

**Data it reads**: `getCart` (onLoad, The cart, priced and checked, right now); `getPaymentLink` (onLoad, Open a payment link sent to this guest); `getPublishedBookingFlow` (onLoad, The published booking flow for this product: which steps it …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `BO-020` F&B Order Management: *Kitchen accepts and prepares*; carries `orderId`; calls `createPayment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The review payment, read by `getCart`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the review payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No review payment yet. Offers Create payment (`createPayment`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getPaymentLink` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** A payment needs the gateway, and pretending otherwise takes money nobody can confirm. What was typed stays on screen so nothing is entered twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 409 No capacity, or the product is … |

#### Permissions

- `transferOrderTickets` → no permission · guest
- `createPayment` → `ORDER_CREATE` (operate) · staff, guest, partner
- `inquirePaymentStatus` → `ORDER_CREATE` (operate) · staff, guest, partner
- `checkoutCart` → no permission · guest, partner
- `getCart` → no permission · guest, partner, staff
- `addCartLine` → no permission · guest, partner, staff
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `getPaymentLink` → `ORDER_VIEW` (read) · guest, anonymous
- `payByLink` → `ORDER_CREATE` (operate) · guest, anonymous
- `getPublishedBookingFlow` → no permission · guest

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getPaymentLink` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

40 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.13 | Ticket Transfer - System shall support ticket transfers. | Guest Mobile App & Branding | CONTRACTED | `transferOrderTickets` |
| 1.1.27 | System shall support ticket ownership transfer between guests according to configurable policies, fees and approval workflows. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 1.6.17 | System shall expose marketplace functionality through APIs for websites, mobile applications, partner platforms, and third-party integrations. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 2.6.39 | Customer should have the ability to view the order transactions with all the details for the logged in users and should be able to resend the tickets / Transfer Tickets to Friend / Download tickets | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 2.13.37 | Ticket Transfer & Reassignment | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 2.6.23 | Payment can be done online. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.12.35 | System shall support multiple payment methods within a single transaction including cash, credit card, wallet, loyalty points, vouchers, gift cards, bank transfers, and credit balances. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.13.2 | The operator can register the payment. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.15.3 | The operator can register the payment and print the pass. | Ticketing Sales | CONTRACTED | `createPayment` |
| 4.2.6 | The system should be able to accept several currencies in one transaction (a guest pays in USD and gets the change in AED). | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.7 | The system should be accept multiple payments in one transaction. For example, there must be an option to split the payment within a group of guests | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.13 | The system should be able to support payment of one transaction with multiple payment methods. | Bundles and Promotions | CONTRACTED | `createPayment` |
| … 28 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Checkout completes in 4 steps, supporting Apple Pay/card payment, and adds the resulting ticket to Apple Wallet or Google Wallet. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1096)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Marketing opt-in ("Send me offers and news") sits beside the T&Cs at checkout and is never pre-ticked. Open: whether a guest-checkout customer may be marketed on it; until confirmed it stays unticked and nothing is sent without it. *(agreed · MoM 18 Sep 2026, M18-15 · DI-954)*
- Checkout captures marketing/newsletter opt-in and preferred contact method (email vs phone). *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-616)*
- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*
- Support both redirect to the gateway's hosted page and embedded/iframe capture (card, Apple Pay, Tabby) on the platform's own checkout preserving its look and feel, for Network International and Stripe; embedded needs extra security certification to reassure guests. *(agreed · MoM 31 Aug 2026, 4.13 Payment gateway approach · DI-589)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Date-change flow detects conflicts across an existing multi-ticket cart and lets the guest shift the whole booking to a new date in one action. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-587)*
- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*
- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)*
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*
- Platinum List reference seat step: interactive seat map colour-coded by price tier → seat selection with a live cart hold and countdown timer → checkout via Quick Order / Apple ID / Google ID. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-409)*
- Once a delivery address is entered, the applicable shipping fee is shown automatically for the customer to accept before payment. *(client request · MoM 19 Aug 2026, 4.8 Online Order Fulfilment & Shipping Configuration · DI-360)*
- **Open question.** Open: alongside curated pre-built packages, let guests build their own bundle in the cart, with the system detecting eligible combinations and applying an automatic discount (e.g. 5–10%). *(open · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-221)*
- Foreign-currency display: an approximate conversion at a back-office rate so the guest sees roughly what they pay while settling in base currency, and/or full DCC at the gateway where the guest is charged in their own currency; records always in the venue base currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-211)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*
- Per-ticket "ticket owner" details are captured separately from the "reservation owner" (buyer) and can enforce rules such as a minimum age per ticket holder. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-178)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Custom fields gate purchase where configured — e.g. a checkbox confirming a guest is not pregnant before a specific product can be bought, or a weight-range field for an activity. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-156)*
- Qossai: the POS-style right-to-left slide-in drawer could also suit the B2C cart/checkout. *(client request · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-124)*
- Separate "ticket holder" (per-ticket details captured where required) from "reservation owner"/buyer (single contact captured once per booking who receives the tickets by email). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-122)*
- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*

Also apply: 6 for P02 · Cart & Checkout, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| … 36 more | | | `WHITE-LABEL.md` |

Also set there, as content the tenant writes: venue overrides: settings.

*Booking flows: steps, their order and per-flow settings*, set in `CMS-102` Site Builder, `CMS-103` Booking Flows:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

Also set there, as content the tenant writes: settings.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-009` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- Flow F11 *Guest orders food to a lounger*, step 4: Pays → Card or wallet
- Flow F11 branch at step 4 (recoverable): when Payment unresolved, Held, inquired, and the kitchen is not told until it resolves. Preparing food against a payment that may not exist is a loss nobody records.
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)
- ADR-0027 *A payment link is a credential, and payment converts the reservation* (`docs/adr/0027-payment-links.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (80), with its required mark, default, format and its error state (400, 402, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-009?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer order tickets, Create payment, Inquire payment status, Checkout cart, Acquire inventory hold, Create order, Pay by link.
- [ ] Every transition is wired: `GST-001`, `BO-020`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 23 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-010` Booking Confirmation

**Confirm it worked, and give them what they need to prove it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Cart & Checkout · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17911 (APP-MOB-GST-010) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getOrder` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `orderId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/general/booking-confirmation` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August from review**: getOrder. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe. **Cross-surface parity, 31 August**: added reprintOrder. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.

#### Inputs: what the user enters or picks

**Form: Transfer order tickets** (modal, opened by *Transfer order tickets*; *Transfer order tickets* calls `transferOrderTickets`, *Cancel* sends nothing)

**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tickets `ticketIds` | multi-picker: choose tickets | required | — | at least 1 | — | The entitlements to hand over. A ticket is an entitlement, so each value is an `Entitlement.id` on this order — the ids in `OrderLine.entitlementIds`. | `transferOrderTickets` body |
| Recipient `recipient` | group | required | — | — | — | — | `transferOrderTickets` body |
| Channel `recipient.channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `transferOrderTickets` body |
| Address `recipient.address` | text field | required | — | — | — | — | `transferOrderTickets` body |
| Message `message` | text area | optional | — | max length 500 | — | — | `transferOrderTickets` body |

Errors to draw in the form: 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer order tickets (primary button) | `transferOrderTickets` POST `/orders/{orderId}/transfer` | inline | TicketTransfer | 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) | opens modal first; produces a document or message: Transfer tickets to another guest |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | works offline; opens modal first; produces a document or message: Reprint or resend tickets |

**Data it reads**: `getOrder` (onLoad, Read an order)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking confirmation, read by `getOrder`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the booking confirmation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No booking confirmation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) |

#### Permissions

- `transferOrderTickets` → no permission · guest
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.13 | Ticket Transfer - System shall support ticket transfers. | Guest Mobile App & Branding | CONTRACTED | `transferOrderTickets` |
| 1.1.27 | System shall support ticket ownership transfer between guests according to configurable policies, fees and approval workflows. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 1.6.17 | System shall expose marketplace functionality through APIs for websites, mobile applications, partner platforms, and third-party integrations. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 2.6.39 | Customer should have the ability to view the order transactions with all the details for the logged in users and should be able to resend the tickets / Transfer Tickets to Friend / Download tickets | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 2.13.37 | Ticket Transfer & Reassignment | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 2.7.43 | The system should have the ability for B2B client and resellers to issue and re-issue tickets online, sending the final ticket to guests via email and/or mobile SMS - printing in PDF. | Ticketing Sales | CONTRACTED | `reprintOrder` |
| 2.7.46 | The system should allow Partners to come and print their tickets with a booking number: the number of allowed tickets to print and type of tickets (open-dated, dated, etc.) must be configurable.(the … | Ticketing Sales | CONTRACTED | `reprintOrder` |
| 2.7.47 | The system should record reissuing or reprinting of a ticket media. | Ticketing Sales | CONTRACTED | `reprintOrder` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Checkout completes in 4 steps, supporting Apple Pay/card payment, and adds the resulting ticket to Apple Wallet or Google Wallet. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1096)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*
- Ticket delivery: "Add to Wallet" (Apple or Google Wallet by device), and WhatsApp, SMS or email per the guest's chosen method, selectable at checkout/confirmation; tickets can also be emailed to a third party. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-198)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*

Also apply: 6 for P02 · Cart & Checkout, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-010` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 1 → Booking confirmation (#confirm)*. Differences: Prototype offers "Set a password" to turn a guest-checkout profile into an account (linkGuestCheckout, GST-042); not declared on this screen in YAML.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-010?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer order tickets, Reprint order.
- [ ] Every transition is wired: `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-041` Checkout Entry

**Take the money, and be unambiguous about whether it worked.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Cart & Checkout · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17997 (APP-MOB-GST-041) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getCart` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `cartId` (session), `lineId` (navigation), `productId` (navigation), `performanceId` (navigation), `holdId` (navigation), `venueId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. **A cold arrival without a verified sign-in is offered the fork here** — sign in, or prove the … |
| Route | `/general/checkout-entry` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Promo code added 28 September** (decided 28 September, audit R073 (e)) — the web cart WEB-010 has the field, and the two shells are one product. **Rev 3 (decided 29 September).** **Sign-in (REV3-3):** with `signInAt` `afterAddOns` (default) the sign-in or guest-code choice is asked when the guest leaves the tickets and add-ons step (GST-008 → GST-042); with `atPayment` it is asked here, on the way to payment. The basket is kept either way; guest checkout and matching are unchanged (DG-1). Visit date per line (23SEP-9). **On mobile the basket stays a bottom bar with the running total**; the floating icon and the cart side apply to the website (REV3-10). A spot held on the venue map counts down from its `ResourceHold.expiresAt` (REV3-15). `checkoutCart` `422 consentRequired` or `consentAnswerBlocks` sends the guest back to the consent questions (REV3-26). **The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`. **29 September.** **W1:** after …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Promo code | text field | optional | — | min length 1; max length 100 | — | **Applied to the cart at once** with `applyCartPromoCode` (POST /carts/{cartId}/promo-codes, body `{code}`; decided 28 September, audit R073 (e)). The two refusals read differently: 422 … | `ApplyCartPromoCodeRequest.code` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getPublishedBookingFlow` ?productId |
| Product category | picker: choose a product category | — | — | `getPublishedBookingFlow` ?productCategoryId |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `getPublishedBookingFlow` ?flowTypeKey |

**Form: Save cart line** (modal, opened by *Save cart line*; *Save cart line* calls `updateCartLine`, *Cancel* sends nothing)

**Collects what `updateCartLine` sends before it is called.** Required: `quantity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Quantity `quantity` | number field | required | — | min 0 | — | The new quantity. 0 removes the line (audit R123 (1)). | `updateCartLine` body |

Errors to draw in the form: 409 Not enough capacity to increase (`noCapacity`). (CartProblem); 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Checkout cart** (modal, opened by *Checkout cart*; *Checkout cart* calls `checkoutCart`, *Cancel* sends nothing)

**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the order is for. A guest caller may name only themselves (`guestAuth` never widens to another subject); omitted, the cart's own `subjectId` is used. | `checkoutCart` body |
| Marketing consents `marketingConsents` | repeatable rows | optional | — | — | — | Marketing opt-ins given at checkout (29 September, M18-15). Shown unticked beside the terms; one entry per channel and purpose the guest ticked. | `checkoutCart` body |
| Channel `marketingConsents[].channel` | radio group | required | — | Email · SMS · Whatsapp · Push | — | — | `checkoutCart` body |
| Purpose `marketingConsents[].purpose` | text field | required | — | max length 60 | — | The consent purpose code (marketing ConsentPurpose), for example `marketing`. | `checkoutCart` body |
| Granted `marketingConsents[].granted` | toggle | required | — | True only when the guest ticked it. | — | True only when the guest ticked it. Never pre-ticked. | `checkoutCart` body |
| Notice version `marketingConsents[].noticeVersion` | text field | optional | — | max length 40 | — | The version of the consent notice shown. | `checkoutCart` body |
| Attendees `attendees` | repeatable rows | optional | — | — | — | The named holder for each cart line that needs one. Becomes `CreateOrderLine.holderName` on the order's matching line. | `checkoutCart` body |
| Line `attendees[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | A `CartLine.id` in this cart. | `checkoutCart` body |
| Holder name `attendees[].holderName` | text field | required | — | — | — | — | `checkoutCart` body |

Errors to draw in the form: 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 422 A required consent question is unanswered (`consentRequired`), or an answer blocks the booking (`consentAnswerBlocks`), with the lines in `lineIds` (decided 29 … (CartProblem)

**Sent by *Apply code*** (`applyCartPromoCode`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | min length 1; max length 100 | — | The code as the guest typed it. | `applyCartPromoCode` body |

#### Outputs: what the screen shows and produces

**Shown**

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Token | text | How an anonymous guest returns to their cart, including from a recovery email. Rotated on claim, so a link shared before signing in does … |
| Venue | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Subject | the name it points at, never the id | Null while anonymous. Set by `claimCart`. |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Conflicts | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**Every product variant** (data table, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |
| Is default | yes / no (icon or chip) | Taken from their variant tables. Which variant a product page opens on. |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |

**Visit date per line** (card list, from `getPerformance`): `Performance.startsAt` on each line (the match date for a fixture).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |
| Format | text | How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. |

**Booking steps** (progress indicator, from `getPublishedBookingFlow`): The steps of the published flow in their `sortOrder`, this one (basket) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.

| Shows | Format | Notes |
|---|---|---|
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Apply code (secondary button) | `applyCartPromoCode` POST `/carts/{cartId}/promo-codes` | ApplyCartPromoCodeRequest | Cart | 410 Expired (`cartExpired`), as for `getCart`. (CartProblem); 422 The code is not accepted: no such code, voided or used up (`promoCodeInvalid`), or a real code that nothing in this cart qualifies for … (CartProblem) | — |
| Checkout cart (primary button) | `checkoutCart` POST `/carts/{cartId}/checkout` | inline | Order | 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and … | emits `order.created`; opens modal first |
| Abandon cart (destructive button) | `abandonCart` DELETE `/carts/{cartId}` | — | — | 409 The cart is not `active` or `expiring` (`cartNotOpen`) — an expired cart has nothing left to release, and a checked-out cart's leases already belong to its … (CartProblem) | — |
| Claim cart (secondary button) | `claimCart` POST `/carts/{cartId}/claim` | — | CartMergeResult | — | — |
| Extend cart (secondary button) | `extendCart` POST `/carts/{cartId}/extend` | — | Cart | 409 Extension cap reached (`extensionCapReached`), or a lease could not be extended because the capacity has gone (`noCapacity`, naming the lines in `lineIds`). (CartProblem) | — |
| Remove cart line (destructive button) | `removeCartLine` DELETE `/carts/{cartId}/lines/{lineId}` | — | Cart | — | — |
| Save cart line (secondary button) | `updateCartLine` PATCH `/carts/{cartId}/lines/{lineId}` | inline | Cart | 409 Not enough capacity to increase (`noCapacity`). (CartProblem); 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `getCart` (onLoad, The cart, priced and checked, right now); `getPerformance` (onLoad, The visit date of each line (`Performance.startsAt`)); `getResourceHold` (onInterval, The countdown of a spot held on the venue map); `getPublishedBookingFlow` (onLoad, The published booking flow for this product: which steps it …)

**Where the user goes next**

- → `GST-042` Simple Registration & OTP: *Signs in, or proves the contact the tickets go to*; carries `cartId`; only when no verified guest session. This screen is the checkout page, so the fork sits here rather than in front of the cart …
- → `GST-001` Home: *Home – Default*
- → `GST-059` Plan in Progress: *They follow it through the day*

**What opens over it**

- confirmDialog *Abandon cart*: **Names what `abandonCart` changes and what it leaves alone**, in the consequence rather than the verb. A checkout entry this affects should be identified in the dialog, not just counted.
- confirmDialog *Remove cart line*: **Names what `removeCartLine` changes and what it leaves alone**, in the consequence rather than the verb. A checkout entry this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Terminal or gateway state, shown plainly |
| Error (`?state=error`) | **Declined reads differently from unresolved.** An unresolved payment inquires rather than retries, and nothing is issued until it resolves |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listProductVariants` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | **This is the checkout page, and it is where identity is settled** (ADR-0045, 18 September 2026). An unverified or anonymous guest is not turned away — they are offered sign-in or, where the site's `guestCheckout` is on, the one-time code. The cart stays intact either way; `checkoutCart` is what refuses. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 409 Extension cap reached (`extensionCapReached`), or a lease could not be extended because the capacity has gone (`noCapacity`, naming the lines in `lineIds`). (CartProblem); 409 Not enough capacity to increase (`noCapacity`). (CartProblem); 409 … |

#### Permissions

- `applyCartPromoCode` → no permission · guest, partner
- `getCart` → no permission · guest, partner, staff
- `checkoutCart` → no permission · guest, partner
- `abandonCart` → no permission · guest
- `claimCart` → no permission · guest
- `extendCart` → no permission · guest
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `removeCartLine` → no permission · guest, partner
- `updateCartLine` → no permission · guest, partner
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `getResourceHold` → `ORDER_VIEW` (read) · staff, guest
- `getPublishedBookingFlow` → no permission · guest

**A refused user sees:** **This is the checkout page, and it is where identity is settled** (ADR-0045, 18 September 2026). An unverified or anonymous guest is not turned away — they are offered sign-in or, where the site's `guestCheckout` is on, the one-time code. The cart stays intact either way; `checkoutCart` is what refuses.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.9.2 | The system should provide a service to enable the dynamic composition of the shop cart. The system must provide back all the information in real time, such as the performance availabilities of an … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.9.5 | The system should highlight conflicting times at different attractions when trying to purchase tickets in the same time-slot for one guest. For example, if a ticket for Golf 1 to 2 pm has been added … | Ticketing Sales | CONTRACTED | `getCart` |
| 19.2.10 | Ticket Purchase - System shall support ticket purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.23 | Membership Purchase - System shall support membership purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.24 | Membership Renewal - System shall support membership renewals. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.53 | Product Purchases - System shall support merchandise purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 1.1.98 | Membership renewals | Ticketing Catalogue | CONTRACTED | `checkoutCart` |
| 1.4.12 | System shall support dependencies between products, ensuring prerequisite products are purchased when required. | Ticketing Catalogue | CONTRACTED | `checkoutCart` |
| 2.1.10 | This system should provide a Self-service kiosk solution that enables the guests to skip the queues at POS and purchase all type of tickets defined in the system including multi-day, combo ticket … | Ticketing Sales | CONTRACTED | `checkoutCart` |
| 2.1.11 | The system should provide POS and Kiosk solution that allow the collection of tickets (free or not) booked on any portal. The kiosk should allow the collection of tickets using an identification … | Ticketing Sales | CONTRACTED | `checkoutCart` |
| 7.4.46 | Support mandatory, optional and conditional dependencies between products. Example: VIP package requires admission ticket; driving experience requires waiver and age validation. | F&B POS | CONTRACTED | `checkoutCart` |
| 2.1.31 | Guests shall be able to start a cart on one channel and complete it on another channel while retaining all cart contents and pricing rules. | Ticketing Sales | CONTRACTED | `claimCart` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest counters take their price from the chosen park ticket and produce one line, e.g. "2 park ticket · Adult × 3 = AED 1,425" (no separate Adult × 3 line). Child and senior prices scale from the chosen ticket; infants free. *(client request · design review 30 Sep 2026, 2. Multi-park ticket adds an extra adult line · DI-1106)*
- Checkout completes in 4 steps, supporting Apple Pay/card payment, and adds the resulting ticket to Apple Wallet or Google Wallet. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1096)*
- The mobile booking flow (date/day-pass selection, quantity, cross-sell, sign-in) is functionally identical to the web app. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1092)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- Each cart line shows the date of visit: the match date for the stadium, the reservation date for dining (mobile: in the cart bar). *(agreed · design review 29 Sep 2026, Cart 9. Show the date of visit in the cart · DI-1029)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Each picked seat goes into the cart with section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"); tapping the seat again removes it. *(client request · design review 23 Sep 2026, Seat map 15. Selected seats should be added to the cart · DI-982)*
- **Open question.** Qossai: a guest-checkout customer may not have opted into marketing the way a registered customer accepting full terms has; how marketing consent is captured at guest checkout is unresolved. *(open · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-940)*
- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

Also apply: 6 for P02 · Cart & Checkout, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| … 36 more | | | `WHITE-LABEL.md` |

Also set there, as content the tenant writes: venue overrides: settings.

*Booking flows: steps, their order and per-flow settings*, set in `CMS-102` Site Builder, `CMS-103` Booking Flows:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

Also set there, as content the tenant writes: settings.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-041` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match partial): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Cart (header basket, after a booking is added to the cart)*. Differences: Basket as a bottom bar on mobile.
- Flow F49 *A guest plans a day and follows it*, step 5: They check out. → Paid like any other basket; the tickets land on the Tickets tab.
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403, 404, 409, 410, 412, 422).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Apply code, Checkout cart, Abandon cart, Claim cart, Extend cart, Remove cart line, Save cart line.
- [ ] Every transition is wired: `GST-042`, `GST-001`, `GST-059`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 14 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | body text on the background |
| Dark mode (`theme.darkMode`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `CMS-003`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-007` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-007` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-007` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-007` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-007` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-007` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-007` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-007` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-007` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001` | — | — | — |
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
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Never configurable:** The *Powered by TICVAI* credit in the footer is fixed and never client-editable (MoM 3 Aug, DI-111; MoM 12 Aug, DI-250). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P02 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P02 as a whole** (30: 3 open, 27 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- … 16 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P02 Guest App

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)*
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- The revised mobile app design is approved in direction: Qossai liked the opening video and visual polish, Allam the UI/graphics quality. Its flow is deliberately different from the web application (after front-end team input), not a reused structure. Detailed feedback to follow. *(agreed · MoM 30 Sep 2026, 4.4 Guest Mobile App — Revised Design Walkthrough · DI-1086)*
- Every web product and flow stays bookable in the mobile app (incl. cabanas, surf, 2D/3D stadium, theatre plan, bus route map), each with its own step order; a toggle switches back to one decision per screen. *(agreed · design review 29 Sep 2026, Mobile app (v4) — All web products and flows available · DI-1084)*
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)*
- A persistent "Buy tickets" button appears on every screen of the mobile app. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1017)*
- Mobile tabs: Home, Explore, Plan, Tickets (Yas Island / Six Flags references). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1016)*
- The current mobile build goes straight into the booking journey and the client finds it unclear: redesign the UI. All web products and flows, including cabanas and surf, must remain available. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1015)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

### In P02 · Cart & Checkout

- A "save and finish later" option retains an in-progress order locally. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1094)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- Decision: season-pass/family-type products capture first and last name for each individual pass holder (not just the purchaser), via an "add guest name" step. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-429)*
- Decision: the B2C checkout shows a clear, visible step indicator — Ticket Selection → Add-ons → My Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-426)*
- Reference checkouts: Six Flags-style (product → quantity/name capture → cart summary → login/guest checkout with dual OTP validation) and Platinum List (event → date → colour-coded interactive seat map → seats → one-page checkout via Quick Order/Apple/Google, as few as four clicks, optional post-purchase profile prompt). *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-398)*

**41 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"abandonCart": {"method":"DELETE","path":"/carts/{cartId}","contract":"orders","summary":"Empty it deliberately","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"applyCartPromoCode": {"method":"POST","path":"/carts/{cartId}/promo-codes","contract":"orders","summary":"Apply a promo code to the cart","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApplyCartPromoCodeRequest","responds":"Cart"},
"checkoutCart": {"method":"POST","path":"/carts/{cartId}/checkout","contract":"orders","summary":"Turn the cart into an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"claimCart": {"method":"POST","path":"/carts/{cartId}/claim","contract":"orders","summary":"Attach an anonymous cart to a guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CartMergeResult"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createPayment": {"method":"POST","path":"/payments","contract":"orders","summary":"Take a payment against an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePaymentRequest","responds":"Payment"},
"extendCart": {"method":"POST","path":"/carts/{cartId}/extend","contract":"orders","summary":"Give the guest more time","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getPaymentLink": {"method":"GET","path":"/payment-links/{token}","contract":"orders","summary":"What a guest holding a link is being asked to pay for","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getPublishedBookingFlow": {"method":"GET","path":"/venues/{venueId}/booking-flow","contract":"white-label","summary":"The published booking flow a product or category books through","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"productCategoryId","in":"query","required":false},{"name":"flowTypeKey","in":"query","required":false}],"requestBody":null,"responds":"BookingFlow"},
"getResourceHold": {"method":"GET","path":"/resource-holds/{holdId}","contract":"resources","summary":"Read a resource hold","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceHold"},
"inquirePaymentStatus": {"method":"POST","path":"/payments/{paymentId}/inquiry","contract":"orders","summary":"Ask the provider what actually happened","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"payByLink": {"method":"POST","path":"/payment-links/{token}/pay","contract":"orders","summary":"Pay for a booking taken at a till","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"removeCartLine": {"method":"DELETE","path":"/carts/{cartId}/lines/{lineId}","contract":"orders","summary":"Take something out","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"transferOrderTickets": {"method":"POST","path":"/orders/{orderId}/transfer","contract":"orders","summary":"Transfer tickets to another guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateCartLine": {"method":"PATCH","path":"/carts/{cartId}/lines/{lineId}","contract":"orders","summary":"Change a quantity","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"ApplyCartPromoCodeRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["code"],"properties":{"code":{"type":"string","minLength":1,"maxLength":100,"description":"The code as the guest typed it."}}},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartMergeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["cart"],"properties":{"cart":{"$ref":"#/components/schemas/Cart"},"mergedLineCount":{"type":"integer"},"droppedLines":{"type":"array","description":"**Reported, never silent.** Lines that could not be re-leased on merge are named, so a guest signing in is told what they lost rather than discovering it at checkout.\n","items":{"type":"object","properties":{"productName":{"type":"string"},"reason":{"type":"string","enum":["noCapacity","expired","notSellableOnChannel","duplicate"]}}}}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"OrderLineDiscount": {"type":"object","description":"One discount applied to one order line (SD-008). Rows of `orders.order_line_discount`.","required":["id","amount","source"],"properties":{"id":{"type":"string","format":"uuid"},"promotionId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"promotions.promotion","description":"The promotion that gave it. Null for a manual discount."},"source":{"type":"string","enum":["promotion","promoCode","manual","bundle","member"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"A cashier's reason for a manual discount."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentLinkView": {"type":"object","x-ticvai-persistence":"none — projection of orders.payment_link for its holder","description":"What an anonymous holder of a payment link is shown about the link itself.","required":["status","expiresAt"],"properties":{"status":{"type":"string","enum":["issued","viewed","paid","expired","cancelled","superseded"]},"expiresAt":{"type":"string","format":"date-time"},"releaseHoldOnExpiry":{"type":"boolean"}}},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"ResourceHold": {"x-ticvai-persistence":"resources.resource_hold","type":"object","description":"**A guest's pick on the map, held while they pay** (decided 29 September, rev 3 REV3-15). The resource counterpart of `seating.SeatHold`: named resources, short-lived, converted by the order rather than released. States in `states/resource-hold.yaml`.\n","required":["id","mapId","resourceIds","from","to","status","createdAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"mapId":{"type":"string","format":"uuid"},"resourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"partySize":{"type":"integer","nullable":true},"status":{"type":"string","enum":["held","converted","released","expired"]},"totalPrice":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"heldByPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"Set when the order converts it."},"extensionCount":{"type":"integer","default":0},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `venue` scope."}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]}
}
```
