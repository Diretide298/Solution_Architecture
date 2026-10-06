# P10-inventory-pricing-01 — P10 · Inventory & Pricing

**3 screens · 17 operations · 28 schemas · 5 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_REPRINT, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `PTR-005` | Inventory & Allocation View | C | 8 | 48 | 6 | 30 | 3 | 4 | — | notStarted (generated) |
| `PTR-006` | Product Catalog (B2B Pricing) | B | 3 | 48 | 6 | 24 | 2 | 0 | — | notStarted (generated) |
| `PTR-007` | Availability Search | B | 0 | 15 | 5 | 5 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-007 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-005` Inventory & Allocation View

**See inventory & allocation view for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Inventory & Pricing · wave 2 · needs the `partner` module |
| Block | Block C · task APP-PARTNER-PTR-005 |
| Who uses it | partner staff holding `CAPACITY_CONFIGURE`, `ORDER_REPRINT`, `ORDER_VIEW`, `PRODUCT_VIEW` (1 configure, 1 operate, 2 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `channelCapacityId` (deepLink), `orderId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/general/inventory-and-allocation-view` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Capacity writes removed 29 September** (M17-04); a partner no longer creates or amends a capacity envelope or sets channel allocations; it reads them and may still return its own unsold allocation (`relinquishChannelAllocation`).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-018): Order actions (create, discount, exchange, hold, modify, void) on an inventory view; booking is PTR-008 and this view reads and returns allocation (design-notes … Removed 2 October 2026 (CHG-WIR-018): Order actions (create, discount, exchange, hold, modify, void) on an inventory view; booking is PTR-008 and this view reads and returns allocation (design-notes … Removed 2 October 2026 (CHG-WIR-018): Order actions (create, discount, exchange, hold, modify, void) on an inventory view; booking is PTR-008 and this view reads and returns allocation (design-notes …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The partner's allocations: what is reserved for it per performance, sold and left; it may return unsold allocation. After Block A. Read only otherwise (M17-04).

**Fixed on main** (the package already carries these; draw what it says): Order actions (create, discount, exchange, hold, modify, void) on an inventory view. (CHG-WIR-018).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance id | picker: choose a performance (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?performanceId=` to `listChannelCapacities`. | `listChannelCapacities` ?performanceId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Principal | picker: choose a principal | — | — | `listOrders` ?principalId |
| Shift | picker: choose a shift | — | — | `listOrders` ?shiftId |
| Status | select | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | `listOrders` ?status |
| Created from | date and time picker | — | — | `listOrders` ?createdFrom |
| Created to | date and time picker | — | — | `listOrders` ?createdTo |
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Release channel allocation** (modal, opened by *Release channel allocation*; *Release channel allocation* calls `relinquishChannelAllocation`, *Cancel* sends nothing)

**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | multi-select chips | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre; at least 1 | — | — | `relinquishChannelAllocation` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `relinquishChannelAllocation` body |

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

**Every channel capacity** (data table, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Oversell basis | chip: Fixed count, Historic no show rate, Percentage | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The selected channel capacity** (detail panel, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Oversell basis | chip: Fixed count, Historic no show rate, Percentage | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Leased | 1,234 | Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023). |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |
| Has channel allocations | yes / no (icon or chip) | True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |

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

**The channel allocation set** (detail panel, from `getChannelAllocations`)

| Shows | Format | Notes |
|---|---|---|
| Channel capacity | the name it points at, never the id | — |
| Capacity | 1,234 | — |
| Allocations | list or chips (count when long) | — |
| General pool units | 1,234 | Unallocated remainder. Any channel may draw from it once its own allocation is exhausted. |
| Total sold | 1,234 | — |
| Total remaining | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Release channel allocation (secondary button) | `relinquishChannelAllocation` POST `/channel-capacities/{channelCapacityId}/channel-allocations/release` | inline | ChannelAllocationSet | — | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **allocation row**: Product, performance, allocated, sold, left, release date. *(source: DI-556; DI-930)*

**Data it reads**: `listChannelCapacities` (onLoad, List capacity envelopes); `listOrders` (onLoad, List orders)

**Where the user goes next**

- → `PTR-002` Partner Dashboard: *Partner Dashboard*; carries `orderId`
- → `PTR-003` Profile & Company Details: *Profile & Company Details*
- → `PTR-008` Booking Creation: *Receives vouchers*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory allocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory allocation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on performanceId and the inventory allocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `relinquishChannelAllocation` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row: Desert Nights · Sat 10 Oct · allocated 120 · sold 86 · left 34
```

#### Permissions

- `getChannelAllocations` → `PRODUCT_VIEW` (read) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `listChannelCapacities` → `PRODUCT_VIEW` (read) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `relinquishChannelAllocation` → `CAPACITY_CONFIGURE` (configure) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner, device

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `relinquishChannelAllocation` …

#### Requirements it meets

30 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 1.6.16 | System shall maintain immutable audit logs for listings, approvals, purchases, ownership transfers, cancellations, and administrative actions. | Ticketing Catalogue | CONTRACTED | `getOrderStatement` |
| 2.7.40 | The system should provide: - Management and display/communication of payments due and balance. - Management of the possibility to cancel or refund an order. - Alerts to B2B clients for credit limit … | Ticketing Sales | CONTRACTED | `getOrderStatement` |
| 2.12.32 | System shall maintain a complete audit history showing all order activities including creation, modifications, upgrades, refunds, cancellations, transfers, communications, redemptions, and user … | Ticketing Sales | CONTRACTED | `getOrderStatement` |
| 5.3.11 | The system should store all information related to a guest's purchase of any offering including purchased tickets, retail items and F&B offerings. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.3.12 | The system should store all information related to a guest's ticket usage and redemption. This should include information on all the attractions visited by the guest, with the corresponding number of … | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.3.27 | Provide complete visit history including dates, attractions visited, duration, purchases, and spending behavior. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.5.9 | Maintain a complete history of purchases, transfers, upgrades, refunds, reservations, validations, and consumption. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.5.18 | Maintain a complete audit trail for transfers, ownership changes, credit movements, and entitlement assignments. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| … 18 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner screens never create products, prices or performances: the product catalogue (B2B pricing) is read only and the inventory view keeps its reads; partners see assigned products and partner prices. *(agreed · Decisions Register 29 Sep 2026, Rev 3 prototype feedback — M17-04 (partner API scope) · DI-1079)*
- Partners never create products, prices or capacity: partner catalogue and inventory screens are read-only (a partner may still return its own unsold allocation). *(agreed · MoM 17 Sep 2026, M17-04 · DI-930)*
- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-005` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Release channel allocation, Reprint order.
- [ ] Every transition is wired: `PTR-002`, `PTR-003`, `PTR-008`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `ORDER_REPRINT`, `ORDER_VIEW`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-006` Product Catalog (B2B Pricing)

**See the products assigned to this partner and the partner prices, read only.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Inventory & Pricing · wave 2 · needs the `partner` module |
| Block | Block B · ticket #29935 (APP-PARTNER-PTR-006) |
| Who uses it | partner staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getPriceList` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `priceListId` (deepLink), `productId` (deepLink) · cold entry: **A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does. |
| Route | `/general/product-catalog-b2b-pricing` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Read only since 29 September** (decided 17 September, M17-04; applied 29 September). Partners never create products, prices or performances through the API or this portal; product configuration stays in the venue back office (BO-007, BO-008, BO-009), and a partner reads the products assigned to its channel (`listProducts`, `getProduct`, `listProductVariants`) and its partner price lists (`listPriceLists`, `getPriceList`, `listPrices`). The create, set, copy, transition and update actions were removed with the partner audience on those catalogue writes.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The products assigned to the partner with partner prices, read only. After Block A.

**Known correction pending (do not draw the wrong version)**

- **Filters "Venue id", "Kind", "Is sellable" typed as text.** Why: The list is the partner's assigned products. *(source: screens/P10-partner-reseller-portal.yaml#PTR-006 layout; Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listPriceLists` ?channel |

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Every alternative code** (data table, from `listAlternativeCodes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Partner | the name it points at, never the id | — |
| Partner name | text | — |
| Variant | the name it points at, never the id | — |
| Note | text | — |

**Every price list** (data table, from `listPriceLists`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Valid from | 1 Oct 2026, 14:30 | — |
| Priority | 1,234 | Where lists overlap, higher priority wins. |

**Every price** (data table, from `listPrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Price list | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax code | the name it points at, never the id | — |

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

**The selected product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |

**The price list** (detail panel, from `getPriceList`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Channels | list or chips (count when long) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Priority | 1,234 | Where lists overlap, higher priority wins. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Resolve product by code (primary button) | `resolveProductByCode` GET `/products/resolve` | — | ProductVariant | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **product row**: Product, guest types, public price and partner price (net), validity. *(source: DI-1079)*

**Data it reads**: `listProducts` (onLoad, from page inventory); `listPriceLists` (onLoad, List price lists)

**Where the user goes next**

- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product catalog (b2b list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product catalog (b2b untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product is assigned to this partner yet. **Offers no create action** — a partner never creates products or prices (M17-04); it says to ask the venue to assign products and a partner price list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the product catalog (b2b are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row: Summit Peaks Day Pass · Adult · public AED 325 · partner AED 260
```

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getPriceList` → `PRICE_VIEW` (read) · staff, partner
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listAlternativeCodes` → `PRODUCT_VIEW` (read) · staff, partner
- `listPriceLists` → `PRICE_VIEW` (read) · staff, partner
- `listPrices` → `PRICE_VIEW` (read) · staff, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `resolveProductByCode` → `PRODUCT_VIEW` (read) · staff, partner

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.22 | Dynamic Pricing Display - System shall display dynamic pricing. | Guest Mobile App & Branding | CONTRACTED | `listPrices` |
| 2.9.8 | The system should be able to regroup prices by category: Full price / reduced price / complimentary. | Ticketing Sales | CONTRACTED | `listPrices` |
| 1.1.13 | The system should allow combination of multiple properties for all type of tickets. For example, there can be a VIP child ticket and a normal adult ticket. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.32 | Ability to create and book dynamic performances based on the event start time. Dynamic performance to be chosen by customer 2 - 3 - 4 hour (for pods or Spaces) | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.33 | Book per time slot | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.34 | Book variable amount of minutes per individual 30 minute session. Can be at different times of the day and different times of the week / month. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.37 | As above, If individuals purchase X number of minutes, they want the ability to book varying time slots on varying dates | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.38 | For example: If a skydiver or first time flyer wishes to “just turn up”.. we need the ability to sell to that individual and enter them onto the system and create a “ There and then” booking. Can be … | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.39 | Pre purchased number of minutes with variable price based on time slots . Peak, Off Peak, Super Prime etc etc etc . We need the ability to change these periods easily ie , if I wanted to make Prime … | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner screens never create products, prices or performances: the product catalogue (B2B pricing) is read only and the inventory view keeps its reads; partners see assigned products and partner prices. *(agreed · Decisions Register 29 Sep 2026, Rev 3 prototype feedback — M17-04 (partner API scope) · DI-1079)*
- Partners never create products, prices or capacity: partner catalogue and inventory screens are read-only (a partner may still return its own unsold allocation). *(agreed · MoM 17 Sep 2026, M17-04 · DI-930)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-006` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Resolve product by code.
- [ ] Every transition is wired: `PTR-003`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-007` Availability Search

**See what is available to sell on the partner channel, by product and performance.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Inventory & Pricing · wave 2 · needs the `partner` module |
| Block | Block B · ticket #29936 (APP-PARTNER-PTR-007) |
| Who uses it | partner staff holding `PRODUCT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getAvailability` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/availability-search` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** **`getAvailability` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Availability search for the partner: date, product, how many, and what is left at partner price. After Block A.

**Fixed on main** (the package already carries these; draw what it says): Availability bound to an inline response with no schema; purpose copied from guest search. (CHG-WIR-020).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `getAvailability` ?performanceId |
| Channel capacity | picker: choose a channel capacity | — | — | `getAvailability` ?channelCapacityId |
| Event | picker: choose an event | — | — | `getAvailability` ?eventId |
| From | date and time picker | — | — | `getAvailability` ?from |
| To | date and time picker | — | Exclusive; at most 31 days after `from`. | `getAvailability` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **search**: Product, date (range), party size; results only for assigned products. *(source: F03 step 2)*

#### Outputs: what the screen shows and produces

**Shown**

**Availability** (data table, from `getAvailability`): Shows `channelCapacityId`, `performanceId`, `capacity`, `sold`, `leased`, `remaining`, `byChannel` from `getAvailability`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Channel capacity | the name it points at, never the id | — |
| Performance | the name it points at, never the id | The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart. |
| Starts at | 1 Oct 2026, 14:30 | The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's … |
| Capacity | 1,234 | — |
| Sold | 1,234 | — |
| Leased | 1,234 | Held by terminals but not yet sold. |
| Remaining | 1,234 | — |
| By channel | list or chips (count when long) | Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect. |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | — |
| Allocated | 1,234 | — |
| Sold | 1,234 | — |
| Remaining | 1,234 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Data it reads**: `getAvailability` (onLoad, Per-performance capacity on the B2B channel)

**Where the user goes next**

- → `PTR-008` Booking Creation: *Creates the booking*; calls `getAvailability`
- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The availability search list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the availability search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No availability search yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getAvailability` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result: Fri 2 Oct · Day Pass · 340 left · partner AED 260
```

#### Permissions

- `getAvailability` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getAvailability` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.74 | System shall support event-driven integrations. | Ticketing Catalogue | CONTRACTED | `getAvailability` |
| 2.1.4 | The system should ensure full integration of all internal sales channels. All associated information (capacity, sales, etc.) must be available to multiple operators simultaneously in real-time. | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.10 | - Event capacity updated in real-time | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.14 | - Remaining quantities | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.7.14 | - Capacity management in real time is expected | Ticketing Sales | CONTRACTED | `getAvailability` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-007` · status **notStarted** · provenance generated
- Flow F03 *Partner books on credit*, step 2: Searches availability → Sees the allocation reserved for the B2B channel, not the total
- Flow F03 branch at step 2 (recoverable): when The B2B channel allocation is exhausted, Shows sold out for this channel while other channels may still have capacity. Correct under channel allocation, and worth saying plainly in the portal.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-007?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-008`, `PTR-003`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P10 as a whole** (12: 0 open, 12 closed). Open first; a closed row says where it went on 30 September.

- **A89** Build corporate/B2B self-service onboarding (trade licence & VAT upload → approve/reject → rate setup → credential issuance) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker)*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker)*
- **A170** Build family and corporate wallets (parent-funded child wristbands, per-member allowances, parent-only top-up, guest self-service family setup, department-segregated corporate funds, bidirectional transfer as a venue … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A178** Build B2B partner management (configurable profiles, onboarding workflow, sub-agents, territory and distribution rights, venue association with per-venue pricing, document compliance repository, action permissions … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A179** Support all three B2B/OTA routes (direct portal · bidirectional API with external OTAs · bulk pre-generated QR CSV for non-integrating partners), with an existing OTA integration reusable by configuration *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A180** Build B2B agreements & payment models (tiered volume discounts, commission rates, credit limit vs. prepaid wallet vs. card, partner-reserved inventory, booking limits) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A181** Build B2B settlement & reconciliation (per-partner operations dashboard, statements of account, exception management for unsettled transfers, dispute handling, AI partner performance view) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A184** Build group, school and corporate sales (inquiry dashboard, configurable customer categories, package builder against live inventory and resources, versioned quotations with discount approval, conversion to confirmed … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A208** Check amendments and cancellations against policy before allowing refund, cancellation or reschedule, track booking financial status, and support deposits for school and corporate bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 1 Sep 2026 · workshop tracker)*
- **A231** Build the live operations dashboard and group/B2B admission profile (real-time attendance by venue and gate, gate status, turnstile mode reconfigurable through the day, entry stats by category) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker)*
- **C35** Share the wallet-configuration reference documentation (foundation, funding, stored value, family/corporate, gift cards, payments, fraud/risk, API) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 27 Aug 2026 · workshop tracker)*
- **C44** Confirm how B2B/reseller-issued tickets are handled under a fully-dynamic-QR event policy *(Qossai · Pending → 30 Sep: Closed, Moved to T10 · 2 Sep 2026 · workshop tracker)*

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

### Across P10 Partner Web

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAvailability": {"method":"GET","path":"/availability","contract":"catalogue","summary":"Live remaining capacity","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":"channelCapacityId","in":"query","required":null},{"name":"eventId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceAvailabilityPage"},
"getChannelAllocations": {"method":"GET","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Capacity allocated to each channel","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ChannelAllocationSet"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"getPriceList": {"method":"GET","path":"/price-lists/{priceListId}","contract":"catalogue","summary":"Read a price list","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PriceList"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"listAlternativeCodes": {"method":"GET","path":"/products/{productId}/alternative-codes","contract":"catalogue","summary":"External identifiers for a product","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AlternativeCode"},
"listChannelCapacities": {"method":"GET","path":"/channel-capacities","contract":"catalogue","summary":"List channel capacities","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceLists": {"method":"GET","path":"/price-lists","contract":"catalogue","summary":"List price lists","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrices": {"method":"GET","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"List prices in a list","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"relinquishChannelAllocation": {"method":"POST","path":"/channel-capacities/{channelCapacityId}/channel-allocations/release","contract":"catalogue","summary":"Return unsold channel allocation to the general pool","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"resolveProductByCode": {"method":"GET","path":"/products/resolve","contract":"catalogue","summary":"Resolve a partner code to a product","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"code","in":"query","required":true},{"name":"partnerId","in":"query","required":null}],"requestBody":null,"responds":"ProductVariant"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AlternativeCode": {"x-ticvai-persistence":"catalogue.alternative_code","type":"object","required":["code","partnerId"],"properties":{"code":{"type":"string","maxLength":128},"partnerId":{"type":"string","format":"uuid"},"partnerName":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":200}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelAllocation": {"x-ticvai-persistence":"catalogue.channel_allocation","type":"object","required":["channel","allocatedUnits"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"channel":{"$ref":"#/components/schemas/Channel"},"allocatedUnits":{"type":"integer","minimum":0},"soldUnits":{"type":"integer","readOnly":true},"leasedUnits":{"type":"integer","readOnly":true,"description":"Held by terminals on this channel but not yet sold."},"remainingUnits":{"type":"integer","readOnly":true},"releaseAt":{"type":"string","format":"date-time","nullable":true,"description":"Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"},"salesChannelId":{"type":"string","format":"uuid","nullable":true,"description":"The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3)."},"allocationType":{"type":"string","enum":["sharedPool","dedicated","percentage","dynamic"],"default":"dedicated","description":"How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row."},"minimumUnits":{"type":"integer","nullable":true,"minimum":0},"maximumUnits":{"type":"integer","nullable":true,"minimum":0},"replenishmentRule":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`."},"waitlistBehavior":{"type":"string","enum":["none","joinWaitlist","notifyOnRelease"],"default":"none"},"releaseThresholdUnits":{"type":"integer","nullable":true,"minimum":0},"releaseHoursBeforeEvent":{"type":"integer","nullable":true,"minimum":0,"description":"Alternative to `releaseAt`, relative to the performance start."},"contractualUnits":{"type":"integer","nullable":true,"minimum":0,"description":"Units a partner agreement guarantees; rebalancing never goes below it."},"minimumGuaranteedUnits":{"type":"integer","nullable":true,"minimum":0},"isFrozen":{"type":"boolean","default":false,"description":"Excluded from rebalancing."}}},
"ChannelAllocationSet": {"x-ticvai-persistence":"none — projection","type":"object","required":["channelCapacityId","capacity","allocations","generalPoolUnits"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"capacity":{"type":"integer"},"allocations":{"type":"array","items":{"$ref":"#/components/schemas/ChannelAllocation"}},"generalPoolUnits":{"type":"integer","description":"Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"},"totalSold":{"type":"integer"},"totalRemaining":{"type":"integer"}}},
"ChannelCapacity": {"x-ticvai-persistence":"catalogue.channel_capacity","type":"object","required":["id","performanceId","capacity","sold","leased","remaining","isSeated"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"},"seatCategoryId":{"type":"string","format":"uuid","nullable":true},"oversellAllowance":{"type":"integer","default":0,"description":"BL-046, 1.3.13. **The guard existed in one direction** — an envelope could be raised freely and refused reduction below what had sold.\n**Free events oversell deliberately because no-show rates are known.** An allowance on the envelope rather than an admission policy, because **the gate must still refuse when actual capacity is reached** — overselling is a sales decision and admission is a safety one, and they must not share a number.\n"},"oversellBasis":{"type":"string","nullable":true,"enum":["fixedCount","historicNoShowRate","percentage"]},"capacity":{"type":"integer","minimum":0},"sold":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units sold. **Maintained on write** (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by consumption a workstation reports on `renewInventoryHold` or `relinquishInventoryHold`, lowered when a refund or cancellation returns the units. Always `capacity + oversellAllowance = sold + leased + remaining`.\n"},"leased":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023)."},"remaining":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"What can still be held. **Decremented at the hold with a guarded statement** (`remaining >= n`) under the row lock, never at the sale, so two buyers cannot both take the last unit (SD-023, 29 September).\n"},"hasChannelAllocations":{"type":"boolean","description":"True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity.\n"},"isSeated":{"type":"boolean","description":"Seated envelopes cannot be leased and are blocked offline. A seat map is not a count.\n"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PerformanceAvailability": {"type":"object","x-ticvai-persistence":"none — computed on read from catalogue.channel_capacity and live leases","description":"Remaining capacity of one channel capacity of one performance (rev 3 REV3-1).","required":["channelCapacityId","performanceId","capacity","sold","leased","remaining"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid","description":"The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart."},"startsAt":{"type":"string","format":"date-time","readOnly":true,"description":"The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's `BookingFlowConfig.dayPartBoundaries`) come from this one call (rev 3 REV3-1)."},"capacity":{"type":"integer"},"sold":{"type":"integer"},"leased":{"type":"integer","description":"Held by terminals but not yet sold."},"remaining":{"type":"integer"},"byChannel":{"type":"array","description":"Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"allocated":{"type":"integer"},"sold":{"type":"integer"},"remaining":{"type":"integer"}}}}}},
"PerformanceAvailabilityPage": {"x-ticvai-persistence":"none — computed on read","description":"The `getAvailability` answer (named 29 September, rev 3 REV3-1).","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Page"},{"type":"object","properties":{"items":{"type":"array","items":{"$ref":"#/components/schemas/PerformanceAvailability"}}}}]},
"Price": {"x-ticvai-persistence":"catalogue.price","type":"object","required":["priceListId","variantId","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"priceListId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true}}},
"PriceList": {"x-ticvai-persistence":"catalogue.price_list","type":"object","required":["id","code","name","venueId","currency","currencyScale","channels"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire, removed from the table** — a client should not walk a hierarchy to read a figure, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else — storing it per row is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a client reading a figure should not walk a hierarchy to know what it means, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a workstation with its own currency is a misconfiguration.**\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"priority":{"type":"integer","description":"Where lists overlap, higher priority wins."},"description":{"type":"string","nullable":true,"description":"Price list master fields (29 September, data model DM3), set with `createPriceList` and `updatePriceList` since setPriceListMaster was retired in r2 (BC-008, CHG-CLN-001)."},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"default":"standardRetail"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"scopeLevel":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"default":"venue"},"defaultPriceCategoryId":{"type":"string","format":"uuid","nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"priceResolutionPolicyId":{"type":"string","format":"uuid","nullable":true},"allowOverrides":{"type":"boolean","default":false},"allowInheritance":{"type":"boolean","default":true},"allowMultipleCurrencies":{"type":"boolean","default":false},"allowProductSpecificRates":{"type":"boolean","default":true},"clonedFromPriceListId":{"type":"string","format":"uuid","nullable":true},"currentVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The active `catalogue.price_list_version`."}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"nameLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"**The product's name in each language the venue sells in** (6 October 2026, CHG-R4-011), keyed by ISO 639-1 code, e.g. `{\"en\": \"Aquarium entry\", \"ar\": \"دخول الأكواريوم\"}`. Every guest surface shows the entry for the guest's language and falls back to `name`, which stays the name staff search and reports print. Null, or a language missing from it, means `name` is shown. At most 200 characters per language, as `name`.\n"},"descriptionLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The product's description in each language, as `nameLocalised`; falls back to `description` (6 October 2026, CHG-R4-011).\n"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"description":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
