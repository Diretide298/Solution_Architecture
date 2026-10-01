# P06-operations-02 — P06 · Operations (2 of 5)

**10 screens · 37 operations · 55 schemas · 19 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 19 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, AI_USE, ATTENDANCE_RECORD, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **16 of these operations work offline**: applyManualDiscount, createOrder, getCurrentShift, getOrder, holdOrder, listCatalogueBundles, listOrderRefunds, listOrders
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-014` | Ticket lookup | B–D | 127 | 53 | 6 | 70 | 2 | 0 | — | notStarted (generated) |
| `EMP-015` | Group scan | B–D | 37 | 35 | 6 | 60 | 1 | 0 | — | notStarted (generated) |
| `EMP-017` | Sync & reconciliation | B–D | 74 | 40 | 6 | 62 | 2 | 0 | — | notStarted (generated) |
| `EMP-018` | Offline package | B–D | 3 | 26 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-019` | AI assistant — home | B–D | 4 | 16 | 6 | 16 | 1 | 0 | — | notStarted (generated) |
| `EMP-020` | AI assistant — answer | B–D | 4 | 16 | 6 | 16 | 1 | 0 | — | notStarted (generated) |
| `EMP-021` | Roster | B–D | 6 | 28 | 6 | 15 | 1 | 0 | — | notStarted (generated) |
| `EMP-022` | My rota | B–D | 6 | 44 | 6 | 16 | 2 | 0 | — | notStarted (generated) |
| `EMP-023` | Swap request | B–D | 6 | 36 | 6 | 15 | 2 | 0 | — | notStarted (generated) |
| `EMP-024` | Clock in / out | B–D | 11 | 31 | 6 | 5 | 3 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-014` Ticket lookup

**Answer a question without admitting anybody.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`… (8 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | Searches the bundle only. A ticket issued after the last sync will not be found, and the screen says so |
| Opens with | `orderId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/operations/ticket-lookup` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

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

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

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

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

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
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | works offline; opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | works offline; opens modal first |
| Create refund (secondary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | works offline; opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | works offline; opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | works offline |

**Data it reads**: `listOrders` (onLoad, List orders)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A ticket lookup this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket lookup list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket lookup untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket lookup yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the ticket lookup are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Searches the bundle only. A ticket issued after the last sync will not be found, and the screen says so |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Held order expired … |

#### Permissions

- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

70 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| … 58 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-014` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (127), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-015` Group scan

**Admit a party on one credential.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Fully offline. Admits what is valid and states the shortfall |
| Opens with | nothing: it opens on its own |
| Route | `/operations/group-scan` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `validateAccess` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `validateAccess` body |
| Group size `groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `validateAccess` body |
| Proximity token `proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `validateAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `validateAccess` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell

**Form: Validate group access** (modal, opened by *Validate group access*; *Validate group access* calls `validateGroupAccess`, *Cancel* sends nothing)

**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `validateGroupAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `validateGroupAccess` body |
| Admit count `admitCount` | number field | required | — | min 1 | — | — | `validateGroupAccess` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `validateGroupAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `validateGroupAccess` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance

**Sent by *Override access*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |

**The selected scan event** (detail panel, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |
| Override reason | text | The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`. |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Access point | the name it points at, never the id | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |
| Blacklist | list or chips (count when long) | Media codes to deny outright regardless of entitlement state. |
| Admission rules | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `listScans` (onLoad, List scan events); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A group scan this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group scan list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group scan untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group scan yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the group scan are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Fully offline. Admits what is valid and states the shortfall |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-015` · status **notStarted** · provenance generated
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Validate access, Validate group access.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-017` Sync & reconciliation

**Learn that the server disagreed with you.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_CREATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (5 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listSyncRejections` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Not applicable; this screen ends the offline period |
| Opens with | nothing: it opens on its own |
| Route | `/operations/sync-reconciliation` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listSyncRejections`. | `listSyncRejections` ?workstationId |
| Kind | radio group | optional | — | Order · Payment · Refund · Void · Scan | — | Sends `?kind=` to `listSyncRejections`. | `listSyncRejections` ?kind |
| Resolved | toggle | optional | — | — | — | Sends `?resolved=` to `listSyncRejections`. | `listSyncRejections` ?resolved |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |
| Access point | picker: choose an access point | — | — | `listScans` ?accessPointId |
| Ticket | picker: choose a ticket | — | — | `listScans` ?ticketId |
| Outcome | segmented control | — | Admitted · Denied · Overridden | `listScans` ?outcome |
| Recorded from | date and time picker | — | — | `listScans` ?recordedFrom |
| Recorded to | date and time picker | — | — | `listScans` ?recordedTo |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Sync orders** (modal, opened by *Sync orders*; *Sync orders* calls `syncOrders`, *Cancel* sends nothing)

**Collects what `syncOrders` sends before it is called.** Required: `deviceId`, `orders`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Orders `orders` | repeatable rows | required | — | at least 1; at most 200 | — | — | `syncOrders` body |
| ID `orders[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `syncOrders` body |
| Venue `orders[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Channel `orders[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `syncOrders` body |
| Shift `orders[].shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Subject `orders[].subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `syncOrders` body |
| Guest link `orders[].guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `syncOrders` body |
| Catalogue bundle version `orders[].catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `syncOrders` body |
| Lines `orders[].lines` | repeatable rows | required | — | at least 1 | — | — | `syncOrders` body |
| ID `orders[].lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `syncOrders` body |
| Variant `orders[].lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Recommendation `orders[].lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `syncOrders` body |
| Performance `orders[].lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Booked window `orders[].lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `syncOrders` body |
| Inventory hold `orders[].lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `syncOrders` body |
| Seats `orders[].lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `syncOrders` body |
| Resource hold `orders[].lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `syncOrders` body |
| Attributes `orders[].lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `syncOrders` body |
| Quantity `orders[].lines[].quantity` | number field | required | — | min 1 | — | — | `syncOrders` body |
| Eligibility declaration `orders[].lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `syncOrders` body |
| Quoted unit price `orders[].lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `syncOrders` body |
| Holder name `orders[].lines[].holderName` | text field | optional | — | — | — | — | `syncOrders` body |
| Data mask values `orders[].lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `syncOrders` body |
| Recorded at `orders[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |
| Sequence `orders[].sequence` | number field | required | — | min 1 | — | Monotonic per device. Processed in this order. | `syncOrders` body |
| Payments `orders[].payments` | repeatable rows | required | — | — | — | — | `syncOrders` body |
| ID `orders[].payments[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `syncOrders` body |
| Order `orders[].payments[].orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Tender `orders[].payments[].tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `syncOrders` body |
| Amount `orders[].payments[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `syncOrders` body |
| Tender currency `orders[].payments[].tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `syncOrders` body |
| Tender amount `orders[].payments[].tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `syncOrders` body |
| Wallet authorisation `orders[].payments[].walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `syncOrders` body |
| Wallet hold `orders[].payments[].walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `syncOrders` body |
| Return URL `orders[].payments[].returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `syncOrders` body |
| Terminal `orders[].payments[].terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `syncOrders` body |
| Device `orders[].payments[].deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Recorded at `orders[].payments[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `validateAccess` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `validateAccess` body |
| Group size `groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `validateAccess` body |
| Proximity token `proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `validateAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `validateAccess` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell

**Form: Validate group access** (modal, opened by *Validate group access*; *Validate group access* calls `validateGroupAccess`, *Cancel* sends nothing)

**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `validateGroupAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `validateGroupAccess` body |
| Admit count `admitCount` | number field | required | — | min 1 | — | — | `validateGroupAccess` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `validateGroupAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `validateGroupAccess` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance

**Sent by *Override access*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |
| Resolution | chip: Posted, Voided, Refunded | What `resolveSyncRejection` recorded. Null while the rejection waits. |
| Resolved record | the name it points at, never the id | The order, void or refund the resolution produced — what stops the entry being posted twice. |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Access point | the name it points at, never the id | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |
| Blacklist | list or chips (count when long) | Media codes to deny outright regardless of entitlement state. |
| Admission rules | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync orders (secondary button) | `syncOrders` POST `/sync/orders` | inline | OrderSyncResult | — | emits `order.paid`, `sync.rejectionRaised`; opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `listSyncRejections` (onLoad, Entries the server refused); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `EMP-009` End shift: *The supervisor closes it*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-018` Offline package: *Offline package*

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sync reconciliation this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sync reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sync reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sync reconciliation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind, resolved and the sync reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Not applicable; this screen ends the offline period |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncOrders` → `ORDER_CREATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

62 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| … 50 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-017` · status **notStarted** · provenance generated
- Flow F72 *A shift ends and the summary is read*, step 2: Anything unsynced is pushed first. → **Sync before close, always.** F33 exits at `openWithUnsynced` for exactly this.
- Flow F72 branch at step 2 (high): when Transactions are still rejected after sync., **The shift stays open.** F33 step 8 resolves them, and a shift closed over rejections has settled against a number that will change.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (74), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Sync orders, Validate access, Validate group access.
- [ ] Every transition is wired: `EMP-009`, `EMP-001`, `EMP-002`, `EMP-003`, `EMP-018`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_CREATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-018` Offline package

**Know which rules this device is enforcing.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act |
| Offline | Cannot refresh. The existing bundle continues and its age is shown |
| Opens with | `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/operations/offline-package` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: publishBundle. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | text field | — | — | `getLatestBundle` ?since |

**Form: Report bundle applied** (modal, opened by *Report bundle applied*; *Report bundle applied* calls `reportBundleApplied`, *Cancel* sends nothing)

**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Applied at `appliedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportBundleApplied` body |
| Outcome `outcome` | segmented control | required | — | Applied · Rolled back · Signature invalid | — | — | `reportBundleApplied` body |
| Error `error` | text field | optional | — | — | — | — | `reportBundleApplied` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle** (data table, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Content hash | text | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**The selected bundle** (detail panel, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Content hash | text | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**The catalogue bundle** (detail panel, from `getLatestBundle`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Is delta | yes / no (icon or chip) | — |
| Base version | text | Present when `isDelta`. The version this delta applies to. |
| Signature | text | Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never … |
| Signature key | text | — |
| Content hash | text | — |
| Stale after | 1 Oct 2026, 14:30 | — |
| Payload | grouped details | Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Report bundle applied (primary button) | `reportBundleApplied` POST `/catalogue/bundles/{version}/applied` | inline | — | — | opens modal first |

**Data it reads**: `listCatalogueBundles` (onLoad, List published bundles); `getLatestBundle` (onLoad, Pull the current bundle for this workstation's venue)

**Where the user goes next**

- → `EMP-049` Hand over the journal: *At the end of the session the journal is handed over*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline package list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline package untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline package yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cannot refresh. The existing bundle continues and its age is shown |

#### Permissions

- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `getLatestBundle` → `PRODUCT_VIEW` (read) · staff
- `reportBundleApplied` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-018` · status **notStarted** · provenance generated
- Flow F71 *A device is prepared, used and handed over*, step 2: It pulls its offline package. → **`reportBundleApplied` closes the loop.** A device that pulled a bundle and never confirmed it is a device the fleet view believes is current.
- Flow F71 branch at step 2 (high): when The bundle is stale and the network is gone., **The device is not issued.** ADR-0013 makes the till and the scanner local-first, and local-first with a stale catalogue is worse than no device.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Report bundle applied.
- [ ] Every transition is wired: `EMP-049`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-019` AI assistant — home

**The tab that is already in the shell.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAiConversations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Not available.** Retrieval needs the index |
| Opens with | `conversationId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/operations/ai-assistant-home` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. Pulled to Wave 1 (CF-101). CF-57: the client named AI configuration assistance as a Wave 1 priority, and F20 is Wave 1.

#### Inputs: what the user enters or picks

**Form: Create AI conversation** (modal, opened by *Create AI conversation*; *Create AI conversation* calls `createAiConversation`, *Cancel* sends nothing)

**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module `module` | select | required | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | Which part of the platform the conversation is about (8.4.1). | `createAiConversation` body |
| Locale `locale` | text field | optional | — | — | — | 8.4.3. Multilingual, and Arabic is not an afterthought here. | `createAiConversation` body |

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every AI conversation** (data table, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Scope path | text | — |
| Module | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**The selected AI conversation** (detail panel, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Scope path | text | — |
| Module | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create AI conversation (primary button) | `createAiConversation` POST `/conversations` | inline | AiConversation | — | opens modal first |
| Send AI message (secondary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | — | opens modal first |

**Data it reads**: `listAiConversations` (onLoad, A principal's conversation history)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-020` AI assistant — answer: *AI assistant — answer*; carries `conversationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The assistant home list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the assistant home untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No assistant home yet. Offers Create AI conversation (`createAiConversation`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAiConversations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `listAiConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available.** Retrieval needs the index |

#### Permissions

- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `sendAiMessage` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `listAiConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.29 | System shall expose AI services through APIs. | Unified Operations Dashboard | CONTRACTED | `listAiConversations` |
| 8.4.30 | System shall maintain AI interaction history. | Unified Operations Dashboard | CONTRACTED | `listAiConversations` |
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.2 | System shall support natural language interaction. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.3 | System shall support multilingual AI interactions. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-019` · status **notStarted** · provenance generated
- Flow F101 *A staff member asks the assistant and it answers from the venue*, step 1: AI assistant — home. → 2 operations, 2 of them previously unwalked.
- Flow F101 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create AI conversation, Send AI message.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-020`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-020` AI assistant — answer

**Answer with the operation behind it visible.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as supervisor, venue manager |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAiConversations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Not available |
| Opens with | `conversationId` (deepLink), `messageId` (navigation) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/operations/ai-assistant-answer` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. Pulled to Wave 1 (CF-101) with EMP-019 — **the question and the answer are one screen pair** and splitting them across waves ships half a feature. **Cross-platform navigation removed 24 August**: BO-058. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

**Form: Create AI conversation** (modal, opened by *Create AI conversation*; *Create AI conversation* calls `createAiConversation`, *Cancel* sends nothing)

**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module `module` | select | required | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | Which part of the platform the conversation is about (8.4.1). | `createAiConversation` body |
| Locale `locale` | text field | optional | — | — | — | 8.4.3. Multilingual, and Arabic is not an afterthought here. | `createAiConversation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every AI conversation** (data table, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Scope path | text | — |
| Module | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**The selected AI conversation** (detail panel, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Scope path | text | — |
| Module | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send AI message (primary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | — | opens modal first |
| Create AI conversation (secondary button) | `createAiConversation` POST `/conversations` | inline | AiConversation | — | opens modal first |

**Data it reads**: `listAiConversations` (onLoad, A principal's conversation history)

**Where the user goes next**

- → `EMP-040` Knowledge base: *Knowledge base*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `BO-058` Reporting Home: *Saves it as a report*; carries `conversationId`; calls `sendAiMessage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The assistant answer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the assistant answer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No assistant answer yet. Offers Create AI conversation (`createAiConversation`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAiConversations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `listAiConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Not available |

#### Permissions

- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `listAiConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-020` · status **notStarted** · provenance generated
- Flow F101 *A staff member asks the assistant and it answers from the venue*, step 2: AI assistant — answer. → 2 operations, 2 of them previously unwalked.
- Flow F20 *A manager asks a question and gets an answer*, step 2: The answer arrives with its sources → **An answer with no sources is a guess**, and the interface shows it as one
- Flow F20 branch at step 2 (recoverable): when Nothing relevant was retrieved, **Says so rather than answering from general knowledge.** A confident answer about a venue the model has never seen is the failure that stops people trusting it.
- Flow F20 branch at step 2 (requiresStaff): when The answer proposes a change, A `proposedAction`, not an applied one. Pricing and financial proposals need approval before execution.
- Flow F20 branch at step 2 (recoverable): when Every provider is unavailable, Reported rather than retried indefinitely. **An assistant that hangs is worse than one that says no.**

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send AI message, Create AI conversation.
- [ ] Every transition is wired: `EMP-040`, `EMP-001`, `EMP-002`, `EMP-003`, `BO-058`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-021` Roster

**See who is on, and where.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRotaAssignments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Cached roster with its age |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/roster` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRotaAssignment, updateRotaAssignment. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listRotaAssignments`. | `listRotaAssignments` ?principalId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listRotaAssignments`. | `listRotaAssignments` ?departmentId |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

#### Outputs: what the screen shows and produces

**Shown**

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request shift swap (primary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Data it reads**: `listRotaAssignments` (onLoad, The rota)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-022` My rota: *A steward reads their own shifts*; carries `assignmentId`; calls `listRotaAssignments`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No roster yet. Offers Request shift swap (`requestShiftSwap`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached roster with its age |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-021` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 1: The steward reads the published rota. → **Read, not authored.** `createRotaAssignment` and `updateRotaAssignment` were on this screen until 24 August — **a handheld that could write the rota it is showing.** The rota is published from the …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request shift swap.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-022`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-022` My rota

**Know when to turn up next.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SHIFT_OPEN`, `WORKFORCE_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRotaAssignments` reads the population and `getCurrentShift` reads one of them — list, select, act |
| Offline | Cached |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/my-rota` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRotaAssignment, updateRotaAssignment. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listRotaAssignments`. | `listRotaAssignments` ?principalId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listRotaAssignments`. | `listRotaAssignments` ?departmentId |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

#### Outputs: what the screen shows and produces

**Shown**

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**The shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request shift swap (primary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Data it reads**: `listRotaAssignments` (onLoad, The rota); `getCurrentShift` (onLoad, The shift this person is on now)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-023` Swap request: *They ask to swap one*; carries `assignmentId`; calls `listRotaAssignments`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rota list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rota untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rota yet. Offers Request shift swap (`requestShiftSwap`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the rota are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-022` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 2: A steward reads their own shifts. → **Read-only, deliberately.** `createRotaAssignment` was on this screen until 24 August — **a rota a steward can rewrite is not a rota.**

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request shift swap.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-023`.
- [ ] Every gated control is gated: `SHIFT_OPEN`, `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-023` Swap request

**Ask somebody to take a shift.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRotaAssignments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Queues locally |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/swap-request` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRotaAssignment, updateRotaAssignment. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listRotaAssignments`. | `listRotaAssignments` ?principalId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listRotaAssignments`. | `listRotaAssignments` ?departmentId |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. **The colleague picker lists only staff with the same role at the same venue**; anyone else is refused 409 `swap-role-mismatch` or `swap-venue-mismatch`. After the request the assignment shows `swapPending` until a supervisor approves (decided 28 September, audit R129 (6)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

#### Outputs: what the screen shows and produces

**Shown**

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |

**Every shift swap** (data table, from `listShiftSwapRequests`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Assignment | the name it points at, never the id | — |
| From principal | the name it points at, never the id | — |
| To principal | the name it points at, never the id | — |
| Status | chip: Awaiting peer, Awaiting approval, Approved, Rejected, Withdrawn | Both parties before the supervisor. A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift … |
| Approval request | text | Routed through `approvals` rather than a second mechanism here. |
| Reason | text | — |
| Requested at | 1 Oct 2026, 14:30 | — |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request shift swap (primary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Data it reads**: `listRotaAssignments` (onLoad, The rota); `listShiftSwapRequests` (onLoad, Swap requests and their state)

**Where the user goes next**

- → `EMP-024` Clock in / out: *On the day, they clock in*; calls `requestShiftSwap`
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The swap request list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the swap request untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No swap request yet. Offers Request shift swap (`requestShiftSwap`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the swap request are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Queues locally |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Permissions

- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `listShiftSwapRequests` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-023` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 3: They ask to swap one. → **A request, not a swap.** The other person has to agree and a supervisor has to allow it — two consents, and the approval path is the one mechanism CF-132 settled.
- Flow F68 branch at step 3 (high): when Nobody accepts the swap., **The original assignment stands.** An unaccepted swap that silently vacates a shift leaves a lane unstaffed.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request shift swap.
- [ ] Every transition is wired: `EMP-024`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-024` Clock in / out

**Record attendance from the device already in hand.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 operate, 1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAttendance` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Device time is recorded and both are kept.** A steward clocking in at a gate with no signal is not late because the sync was |
| Opens with | `recordId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/clock-in-out` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listAttendance`. | `listAttendance` ?date |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listAttendance`. | `listAttendance` ?principalId |
| Exceptions only | toggle | optional | — | — | — | Sends `?exceptionsOnly=` to `listAttendance`. | `listAttendance` ?exceptionsOnly |

**Form: Record attendance** (modal, opened by *Record attendance*; *Record attendance* calls `recordAttendance`, *Cancel* sends nothing)

**Collects what `recordAttendance` sends before it is called.** Required: `kind`, `occurredAt`. Optional: `assignmentId`, `accessPointId`, `latitude`, `longitude`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Clock in · Clock out · Break start · Break end | — | — | `recordAttendance` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time. The server records both this and when it arrived. | `recordAttendance` body |
| Assignment `assignmentId` | picker: choose an assignment | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Latitude `latitude` | number field | optional | — | — | — | — | `recordAttendance` body |
| Longitude `longitude` | number field | optional | — | — | — | — | `recordAttendance` body |

Errors to draw in the form: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected.

**Form: Amend attendance** (modal, opened by *Amend attendance*; *Amend attendance* calls `amendAttendance`, *Cancel* sends nothing)

**Collects what `amendAttendance` sends before it is called.** Required: `correctedAt`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Corrected at `correctedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `amendAttendance` body |
| Reason `reason` | text area | required | — | max length 300 | — | — | `amendAttendance` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance** (data table, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Assignment | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Access point | the name it points at, never the id | — |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Is amended | yes / no (icon or chip) | — |
| Amended by principal | the name it points at, never the id | Who made the latest amendment. The full history is `amendments` (audit R129 (7)). |

**The selected attendance** (detail panel, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Assignment | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Access point | the name it points at, never the id | — |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Is amended | yes / no (icon or chip) | — |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |
| Exception | chip: Late, Early leave, Missing clock out, No show, Out of geofence, Unscheduled | Computed against the rota. Null where the record matches what was expected. |

**Corrections** (timeline, from `listAttendance`): **Every correction, oldest first** — who, when, the time before and after, and why — rather than only the last amender and reason (decided 28 September, audit R129 (7)).

| Shows | Format | Notes |
|---|---|---|
| Amended at | 1 Oct 2026, 14:30 | — |
| Amended by principal | the name it points at, never the id | — |
| Occurred at before | 1 Oct 2026, 14:30 | The record's time before this correction. |
| Occurred at after | 1 Oct 2026, 14:30 | The time this correction set (`correctedAt` on the request). |
| Reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record attendance (primary button) | `recordAttendance` POST `/attendance/clock` | inline | AttendanceRecord | 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. | works offline; opens modal first |
| Amend attendance (secondary button) | `amendAttendance` POST `/attendance/{recordId}/amend` | inline | AttendanceRecord | — | opens modal first |

**Data it reads**: `listAttendance` (onLoad, Who was here)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-025` Break management: *They take a break and come back*; carries `recordId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The clock out list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the clock out untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No clock out yet. Offers Record attendance (`recordAttendance`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on date, principalId, exceptionsOnly and the clock out are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Device time is recorded and both are kept.** A steward clocking in at a gate with no signal is not late because the sync was |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Permissions

- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff
- `listAttendance` → `WORKFORCE_VIEW` (read) · staff
- `amendAttendance` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 8.9.7 | System shall display staffing levels, shift attendance, assignments, absences, overtime, and workforce utilization. | Unified Operations Dashboard | CONTRACTED | `listAttendance` |
| 1.2.75 | System shall maintain complete audit logs. | Ticketing Catalogue | CONTRACTED | `amendAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*
- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-024` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 4: On the day, they clock in. → **Attendance is not the shift.** A rota says who should be there; attendance says who was, and the gap is the number a venue manages.
- Flow F68 branch at step 4 (medium): when They clock in at the wrong venue., Refused against the rota. **A steward at the wrong site is a steward the right site is waiting for.**

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record attendance, Amend attendance.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-025`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

**16 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"amendAttendance": {"method":"POST","path":"/attendance/{recordId}/amend","contract":"workforce","summary":"A supervisor corrects a record","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"applyManualDiscount": {"method":"POST","path":"/orders/{orderId}/discounts","contract":"orders","summary":"Apply a discount a cashier chose","permission":"ORDER_DISCOUNT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ManualDiscountRequest","responds":"Order"},
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createRefund": {"method":"POST","path":"/orders/{orderId}/refunds","contract":"orders","summary":"Refund an order, wholly or in part","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRefundRequest","responds":null},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getCurrentShift": {"method":"GET","path":"/shifts/current","contract":"shift","summary":"The open or suspended shift on the session's workstation","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"getLatestBundle": {"method":"GET","path":"/catalogue/bundles/latest","contract":"catalogue","summary":"Pull the current bundle for this workstation's venue","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"since","in":"query","required":null},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"CatalogueBundle"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"holdOrder": {"method":"POST","path":"/orders/{orderId}/hold","contract":"orders","summary":"Park a sale and free the till","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"listAiConversations": {"method":"GET","path":"/conversations","contract":"ai","summary":"A principal's conversation history","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAttendance": {"method":"GET","path":"/attendance","contract":"workforce","summary":"Who was here","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShiftSwapRequests": {"method":"GET","path":"/shift-swaps","contract":"workforce","summary":"Swap requests and their state","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ShiftSwap"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"recordAnswerFeedback": {"method":"POST","path":"/messages/{messageId}/feedback","contract":"ai","summary":"Say whether an answer helped","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAnswerFeedback"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"reportBundleApplied": {"method":"POST","path":"/catalogue/bundles/{version}/applied","contract":"catalogue","summary":"Report that a workstation applied a bundle","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestShiftSwap": {"method":"POST","path":"/rota-assignments/{assignmentId}/swap","contract":"workforce","summary":"Ask someone to take your shift","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"resumeOrder": {"method":"POST","path":"/orders/{orderId}/resume","contract":"orders","summary":"Bring a parked sale back to a till","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderResumeResult"},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"syncOrders": {"method":"POST","path":"/sync/orders","contract":"orders","summary":"Replay orders recorded offline","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderSyncResult"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"validateAccess": {"method":"POST","path":"/access/validate","contract":"access","summary":"Validate media at an access point and admit or deny","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidateRequest","responds":"ValidationResult"},
"validateGroupAccess": {"method":"POST","path":"/access/group-validate","contract":"access","summary":"Admit a group on one read","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"voidOrder": {"method":"POST","path":"/orders/{orderId}/voids","contract":"orders","summary":"Void an order","permission":"ORDER_VOID","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiAnswerFeedback": {"type":"object","x-ticvai-persistence":"ai.answer_feedback","description":"**What a person thought of an answer** (AIC-062). One label per message per person; it feeds the golden sets and the knowledge-gap list, never an online update (design 3.5).","required":["messageId","rating"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"messageId":{"type":"string","format":"uuid","x-ticvai-references":"ai.message"},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"rating":{"type":"string","enum":["helpful","notHelpful"]},"reason":{"type":"string","enum":["wrong","outdated","incomplete","notGrounded","unsafe","other"],"nullable":true},"comment":{"type":"string","nullable":true,"maxLength":1000},"audience":{"type":"string","enum":["staff","guest"],"readOnly":true},"principalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest, where the audience is `guest`."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"CatalogueBundle": {"x-ticvai-persistence":"catalogue.published_bundle","type":"object","required":["version","venueId","isDelta","signature","signatureKeyId","contentHash","staleAfter","payload"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"isDelta":{"type":"boolean"},"baseVersion":{"type":"string","nullable":true,"description":"Present when `isDelta`. The version this delta applies to."},"signature":{"type":"string","description":"Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"},"signatureKeyId":{"type":"string"},"contentHash":{"type":"string"},"staleAfter":{"type":"string","format":"date-time"},"payload":{"type":"object","description":"Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n","additionalProperties":true,"properties":{"saleBoards":{"type":"array","description":"**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n","items":{"type":"object","additionalProperties":true}}}}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateRefundRequest": {"type":"object","required":["id","amount","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit to refund the whole order."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","minLength":3,"maxLength":500},"secondaryAuthorisation":{"type":"object","description":"Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid"},"credential":{"type":"string","maxLength":512,"description":"The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."}}},"refundToOriginalTender":{"type":"boolean","default":true},"alternateTender":{"$ref":"#/components/schemas/TenderKind"},"recordedAt":{"type":"string","format":"date-time"}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"ManualDiscountRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineId":{"type":"string","format":"uuid","nullable":true,"description":"Omit to discount the order rather than a line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","minimum":0,"maximum":100},"reason":{"type":"string","minLength":3,"maxLength":300,"description":"Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"},"reasonCode":{"type":"string","nullable":true,"description":"Optional alongside the free text, where the venue maintains a list."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required above the venue threshold. May not be the requester."},"recordedAt":{"type":"string","format":"date-time"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ModuleKey": {"type":"string","enum":["ticketsAndBooking","membership","events","attractions","virtualQueue","diningAndFnb","shop","parking","gamification","photoGallery","wallet","loyalty","lostAndFound","map","visitPlanner"],"description":"`visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown."},
"OfflineOrder": {"x-ticvai-persistence":"none — client-side journal, not server storage","allOf":[{"$ref":"#/components/schemas/CreateOrderRequest"},{"type":"object","required":["sequence","payments"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. Processed in this order."},"payments":{"type":"array","items":{"$ref":"#/components/schemas/CreatePaymentRequest"}}}}]},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderResumeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","hasChanged"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"hasChanged":{"type":"boolean","description":"True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"},"changes":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["priceChanged","promotionExpired","promotionNowApplies","soldOut","seatHoldExpired","productWithdrawn"]},"lineId":{"type":"string","format":"uuid"},"detail":{"type":"string"},"wasAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nowAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"OrderSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer"},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The `OfflineOrder.id` this result is about."},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","rejected","blockedByRejection"],"description":"`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."},"orderNumber":{"type":"string","nullable":true},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Posted to the variance account. Not surfaced to the cashier."},"varianceExceedsThreshold":{"type":"boolean","description":"True when review is required per the venue's variance threshold."},"rejectionId":{"type":"string","nullable":true,"description":"For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included."},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"ShiftSwap": {"type":"object","x-ticvai-persistence":"workforce.shift_swap","required":["id","assignmentId","fromPrincipalId","toPrincipalId","status"],"properties":{"id":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid"},"fromPrincipalId":{"type":"string","format":"uuid"},"toPrincipalId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["awaitingPeer","awaitingApproval","approved","rejected","withdrawn"],"description":"**Both parties before the supervisor.** A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift starts.\n"},"approvalRequestId":{"type":"string","nullable":true,"description":"Routed through `approvals` rather than a second mechanism here."},"reason":{"type":"string","nullable":true},"requestedAt":{"type":"string","format":"date-time"}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}},
"VoidReason": {"type":"string","description":"**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n","enum":["guestChangedMind","enteredInError","itemUnavailable","qualityIssue","duplicate","other"]}
}
```
