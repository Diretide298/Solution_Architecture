# WS176 — Seat Management Venue Mapping Reference v1.0 board 12

**10 screens · 32 operations · 31 schemas · 12 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `APPROVAL_CONFIGURE, CAPACITY_CONFIGURE, PERMISSION_GRANT, PERMISSION_MANAGE, PERMISSION_VIEW, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, SHIFT_OPEN, TENANT_CONFIGURE, TENANT_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
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

### Ticketing & Guest Commerce, as the venue and TICVAI configure and run it

WHAT THE PROCESS IS. Everything a guest can buy is set up, priced, promoted and serviced here, on Venue Management (P08, the venue's own back office, served inside the venue's cell) and on the TICVAI Console (P09, TICVAI's control plane, outside every cell). End to end: (1) CATALOGUE. A product has one of twelve kinds (admission, timedAdmission, datedAdmission, openDated, seated, membership, bundle, fnb, retail, rental, addOn, giftCard). Its ticket types (adult, child, senior, resident...) are not typed one by one: they are generated from the product's attributes (components) and each value combination becomes a sellable ticket type with no extra setup (DI-164). What a ticket grants (validity, entries, re-entry, days of week, blackout dates, expiry anchor, fast track, transfer) lives on a reusable entitlement template, not on the product. Who may take part (age, height, supervision, certification) is the eligibility rule; what the guest must answer is the data mask and the consent questions; how the guest sees it is guestListing (bookable, infoOnly, hidden), display tags (at most six), media and the booking flow. Group, family and corporate products and every after-sales policy (reschedule, exchange, refund, cancellation, upgrade, transfer) are configured inside the one product configuration, never on separate screens (DI-465, DI-466). (2) LIFECYCLE AND PUBLICATION. A product moves draft, inReview, approved, live, withdrawn, archived. Approval and publication are two acts with two permissions (PRODUCT_APPROVE, PRODUCT_PUBLISH, R091); every product is authorised before it sells online or on site (DI-438). Approved is still not on a till: a till sells only what is in the signed catalogue release it pulled (publishBundle, ADR-0013), so a saved price is a back-office fact until the venue publishes to tills. Changing something that has sold is preceded by an impact check (assessProductChange: orders affected, entitlements issued, future performances, open carts); restoring a version creates a new version, and sold tickets keep the price and terms they were sold under (restoreProductVersion, DI-938, TRACKER Actions row 145). (3) PRICE. Prices live in price lists: per venue, per channel set, with validity dates and a priority, copied for the next season with an uplift (copyPriceList) and repriced in bulk only after a dry run (bulkChangePrices). Currency and decimal scale are never chosen on a form: they resolve from the venue's region (ADR-0008, ADR-0018; AED 2 places, OMR and BHD 3). When several rules apply, the configured hierarchy decides; there is no "lowest price wins" default (DI-595). Tax on the pre-discount price and three-decimal rounding are regional settings (DI-598). Dynamic rules always show their minimum and maximum price guardrails beside the trigger (getDynamicPriceRule). (4) PROMOTE AND BUNDLE. A promotion is a rule (automatic, or gated by a code) created in draft, made live only by Publish, which first analyses stacking; a …
*(source: DI-164; DI-171; DI-438; DI-465; DI-466; DI-595; DI-598; DI-387; DI-039; DI-044; DI-474; DI-671; DI-987; DI-019; DI-080; ADR-0008; ADR-0013; ADR-0018; ADR-0019; ADR-0030; R091; R098; R101; R222; REV3-21; contracts/spine/catalogue.yaml#transitionProductLifecycle …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Product | Anything sellable, of one of the twelve kinds. The record that carries names, channels, listing, media and policies. | Item (except on F&B and retail screens), SKU (for tickets), Offering | contracts/spine/catalogue.yaml#/components/schemas/ProductKind |
| Ticket type | One sellable variant of an admission or event product (Adult, Child, Resident Adult), generated from the product's attributes. For retail and F&B the same record is labelled Variant. | Variant (on ticket screens), Sub-product, Rate (that is a price), Axis value | contracts/spine/catalogue.yaml#updateProductVariant / DI-164 / DI-437 |
| Attribute | A dimension that generates ticket types (Guest category, Residency, Tier, Length). Each has values; adding a value adds ticket types. | Axis, Component (the client's word; use it only in help text), Option | contracts/spine/catalogue.yaml#setProductAttributes / DI-164 / DI-450 |
| Entitlement | What a ticket lets the holder do (validity, entries, re-entry, days, blackout dates, expiry, fast track, transfer), defined once on an entitlement template and shared by several products. | Access rights, Ticket rules, Validity profile | contracts/spine/catalogue.yaml#createEntitlementTemplate / DI-171 / DI-451 |
| Eligibility rule | Who may take part in or buy a product (age, height, supervision, waiver, certification). Distinct from a promotion's eligibility, which decides who gets a discount. | Restriction, Access rule (that is access control) | contracts/spine/catalogue.yaml#setProductEligibilityRule / DI-463 |
| Price list | A set of prices for one venue and a set of channels, valid between two dates, with a priority. Several coexist (B2C, B2B, season). | Price book, Rate card, Tariff | contracts/spine/catalogue.yaml#createPriceList / DI-140 / DI-163 |
| Price category | A standard rate type (Adult, Child, Member) reused across lists so venues do not invent "Adult Standard" and "Normal Adult". | Price band (that is a seat-category band), Fare type (transport) | contracts/spine/catalogue.yaml#setPriceCategoryRateType / … |
| Price band | A priced band on a seat category (code, label, colour, amount, channel, from-date). | Price category, Zone price | contracts/satellite/seating.yaml#/components/schemas/SeatPriceBand |
| Promotion | A rule that changes a price automatically or when a code is entered; draft until published; declares how it stacks. | Offer (except in guest copy), Deal, Discount rule | contracts/satellite/promotions.yaml#createPromotion / DI-173 / DI-174 |
| Coupon code | A code issued from a coupon campaign that applies a promotion-style discount; one shared code or many single-use codes. | Voucher, Promo voucher | contracts/satellite/promotions.yaml#createCouponCampaign / DI-173 |
| Voucher | A code that carries money (face value, balance), sold or issued; a liability until redeemed or expired. | Coupon, Credit note | contracts/satellite/promotions.yaml#listVoucherBatches / … |
| Bundle | A product sold as one line whose price differs from the sum of its components, with a mandatory revenue allocation. "Package" is acceptable in guest copy. | Combo (that is an F&B meal deal), Catalogue bundle | contracts/satellite/promotions.yaml#createBundle / DI-220 / ADR-0019 |
| Catalogue release | The signed snapshot of a venue's catalogue, prices, promotions and sale boards that tills, kiosks and devices pull. Its action label is "Publish to tills". | Bundle, Catalogue bundle, Sync, Deploy | contracts/spine/catalogue.yaml#publishBundle / … |
| Approve / Publish / Save | Save keeps a draft; Approve records that it is authorised (PRODUCT_APPROVE); Publish makes it live for guests and channels (PRODUCT_PUBLISH). Three different buttons, never merged. | Submit, Go live, Activate (except CatalogueConfigStatus active), Deploy | R091 / contracts/spine/catalogue.yaml#transitionProductLifecycle / DI-438 |
| Product states | Draft, In review, Approved, Live, Withdrawn, Archived (ProductLifecycleState), always as coloured badges with these exact labels. | Published (for a product), Pending, Inactive (for a product) | contracts/spine/catalogue.yaml#/components/schemas/ProductLifecycleState |
| Channel | Where something is sold. Labels: pos Point of sale; kiosk Kiosk; web and guestWeb Website; mobile and guestApp App; b2b B2B partners; partner Partner; ota Travel agents (OTA); callCentre Call centre; api API; backOffice Back office. | Touchpoint, Outlet (an outlet is a business inside a venue), raw enum values | contracts/spine/catalogue.yaml#/components/schemas/Channel / … |
| Refund | Money returned after settlement, wholly or for some lines, under the venue's refund policy. | Return (that is retail goods), Reversal, Void | contracts/spine/orders.yaml#createRefund / DI-252 |
| Void | Cancelling a whole order before settlement, within the same shift, with a reason from the void list. After settlement it is a refund. | Cancel order, Delete | contracts/spine/orders.yaml#voidOrder / R222 |
| Exchange / Reschedule | Exchange swaps lines for other products or dates and settles only the difference; Reschedule is the same product moved to another date or time. | Rebook, Date change (acceptable only in guest copy), Refund and resell | contracts/spine/orders.yaml#exchangeOrderLines / … |
| Hold / Capture / Release | A deposit or stored-value amount is held, then partly or fully captured, and the rest released. A held deposit is not a payment. | Charge, Pre-auth (in staff copy), Block funds | contracts/spine/orders.yaml#authoriseStoredValue / … |
| Wallet (TICVAI wallet) | The guest's stored-value balance on TICVAI, spent by hold and capture. Distinct from the tender "Apple Pay / Google Pay", which the contract also calls wallet. | Digital wallet (for stored value), E-wallet, Credit (without a type) | contracts/spine/orders.yaml#/components/schemas/TenderKind / R080 |
| Credit lot | One amount of wallet credit of one credit type (cash, bonus, gift) with its own expiry; lots are spent nearest expiry first and the guest sees the breakdown but cannot choose. | Bucket, Batch, Top-up | TRACKER Actions row 171 / contracts/satellite/wallet.yaml#expireCreditLots |
| Venue map / Seat map | A venue map is the wayfinding map of a park or a floor (points, paths, bookable places); a seat map is the seating layout of an auditorium or stand. Never just "map" where both could be meant. | Layout (alone), Floor plan (unless it is a floor map), Map (alone) | contracts/satellite/venue-map.yaml#createVenueMap / … |
| Point / Bookable place | A point is a place on a venue map (toilet, ride, restaurant, exit). A bookable place is a cabana, lounger, table or pitch placed on the map and sold through its price band. | Pin, POI, Marker, Resource (in staff copy) | contracts/satellite/venue-map.yaml#setVenuePoint / … |
| Station / Route / Timetable / Departure / Fare table / Pass … | A route is an ordered list of stations with offsets; a timetable generates departures up to its release horizon; a fare table prices a route per passenger type; a pass type is a multi-trip or unlimited pass sold as a product. | Stop (except in the stop list), Line (except lineCode), Schedule, Trip (except a guest's journey) | contracts/satellite/transport.yaml / REV3-21 |
| Applies from | The effective date of a change. Every dated change shows it, and sold items keep their old terms. | Effective date (in labels), Start date (for a change) | contracts/satellite/seating.yaml#updateSeatCategory / TRACKER Actions row 194 |

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |

### Food, Beverage & Retail

Food & beverage, retail, rentals, inventory and procurement across the till (P04), the kitchen display (P15), the staff app (P06), Venue Management (P08), the guest web and app (P01/P02), the kiosk (P05) and the CMS (P13). COUNTER SERVICE (F108): the cashier takes the order on the Food & Drink board from the outlet's menu in force (sections in the outlet's order, option groups attached to the item), sends it to the kitchen, and only then charges — send to kitchen, then charge, for every POS F&B order (R261, upheld against the v2 frame by POSV2-4). The kitchen ticket is on the rail while the card is in the guest's hand; an unpaid sent order is cancelled while ordered or accepted and voided with a reason after (R125(3), R091(5)); the guest gets an order number, and the customer-facing status board (numbers only) is the kitchen display's KIT-007, mirrored on the till's queue (POSV2-7). TABLE SERVICE (F29, F80, F94): a party is seated with its covers, orders across the visit, courses are fired by the pass (DI-333, DI-407), the bill is printed and settled at the end and split by amount, covers, category, item or seat (DI-106); the client's table statuses are Available → Ordered → Table closed → Reserved with no cleaning status (DI-336); moving and merging tables stay on the staff app until after r2 (POSV2-8). GUEST ORDERING (F11, F48): a guest inside the venue orders in the app or web for pickup or delivery to a seat or a scanned location (DI-288, DI-291); F&B and retail are optional licensed modules completed inside TICVAI (DI-505), kept simple (DI-1091); no food without an admission ticket (DI-292); table reservations and the waitlist do not go through the cart and a dining deposit is a venue option, off by default (DI-1048, DI-1049, R077). KITCHEN (P15, F83, F88): TICVAI's own display on commodity screens (19 September, replacing the 31 July "integration point only", DI-077); one kitchen ticket per preparation station from the outlet's routing rules with a fallback display (DI-323); a fired timer counts up and resets per course, not shown for quick service (DI-334); displays are assigned to stations and filter by course, with no station-load tile in r1 (R277). 86 takes an item off sale on every till and guest menu immediately (R110(c)); guests always see "Sold out", never a missing dish. RETAIL (F17, F34, F51): scan and sell through the same cart, charge and payment as tickets and food (DI-795), one cart, one receipt and one QR per guest (DI-293); system stock per venue gates the sale (DI-294); returns by receipt or order number only in r1 (R139(c)), refund to the original tender with a reason code and note (DI-796, DI-797); Shop & Drop is paid online and collected on the way out (R236), a merchandise reservation lasts to the end of the visit day (R169, R215). TILL MONEY (F32, F73, F74, F87): the float is counted by denomination with note images and typed quantities (DI-775, DI-776, R229) while the hardware checks itself (DI-778); the close is a …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Send to kitchen | Put the order on the kitchen rail. On the till it always comes before Charge. | Fire, Fire order, Submit order, kitchen fires on payment | R261 / POSV2-4 / F108 step 3 |
| Charge | The till's single tender step (Payment, POS-005); the button reads "Charge AED 110.25". | Checkout (on staff screens), Pay now | F108 step 4 / screens/P04-point-of-sale.yaml#POS-021 |
| Fire / Hold (a course) | Kitchen-pass words for releasing or holding the next course of a table, and the "fired" timer. | using "fire" for sending an order from the till | DI-333 / DI-334 / DI-407 |
| Kitchen ticket | The slip on the kitchen display, one per preparation station. | Order (on the kitchen display), KOT | R210 |
| Ready · Served · Collected · Delivered | How an order reaches the guest; a server marks Served, a counter Collected, a runner Delivered (with the location). | Done, Complete, Bumped (as a status) | R125 / contracts/satellite/fnb.yaml#recordOrderHandover |
| Recall (kitchen) / Recall held sale (till) | Bring a mis-bumped kitchen ticket back to the rail; separately, bring a held cart back into a sale. Never "Recall" alone where both could apply. | Undo bump, Restore | contracts/satellite/fnb.yaml#recallKitchenTicket / POSV2-6 |
| Unavailable (86) / Sold out | Staff screens say "Unavailable" and may add "86"; guest screens say "Sold out". Immediate everywhere. | Out of stock (for food), Disabled, Hidden | R110 / contracts/satellite/fnb.yaml#getGuestMenu |
| Order type | Dine-in · Quick service · Takeaway · Delivery, chosen in the cart. | Service mode, Fulfilment source (on the till) | DI-789 / contracts/satellite/fnb.yaml#/components/schemas/ServiceMode |
| Covers | The number of guests at a table, entered when seating; drives split-by-covers. | Pax (except as a small suffix on the floor plan), Heads | DI-104 / contracts/satellite/fnb.yaml#openTableVisit |
| Vacant · Seated · Ordered · Bill requested · Table closed · … | Table statuses on every floor plan (till and staff app); "Table closed" is the client's word for after payment. | Cleaning, Needs clearing, Dirty | DI-336 / DI-792 |
| Till · Cash drawer | Staff copy may say "till" for the workstation; the cash drawer is the deposit box. | Terminal id as a heading, Deposit box (on staff screens) | R156 |
| Float · Count · Blind count · Variance | The opening float; the denomination count; the closing count made without seeing the expected cash; counted minus expected. | Expected in drawer, Discrepancy, Error | R080 / POSV2-3 |
| Cash out · Cash in · Safe drop | Taking cash out of the drawer mid-shift, adding change, and a supervisor moving cash to the safe with the cashier as witness. | Lift, Withdrawal (as button labels) | DI-274 / contracts/spine/shift.yaml#createCashMovement / … |
| Menu item · Merchandise item · Inventory item · SKU | The scoped product words; SKU is a variant's code, Product stays the sellable thing. | SKU as the item's name, Article | R131 |
| Stock on hand · Allocated · Available | Available is on hand minus allocated. | Inventory (as a number), Free stock | R171 / DI-361 |
| Requisition · Purchase order · Goods receipt · Transfer · … | The procurement and stock words, in that flow. | GRN as the only label, Indent | DI-341 / DI-348 / DI-362 / DI-363 |
| Shop & Drop | Bought and paid now, collected on the way out. | Click & collect | R236 |
| Check-out (rental) · Return (rental) | Handing equipment to the guest and taking it back. On the same screens payment is "Charge" or "Pay". | Checkout (for a handover), Check-in (for a return) | DI-758 / DI-765 |
| Deposit hold · Release · Capture | A refundable deposit held, given back in full, or partly kept for damage with the rest released. | Charge deposit, Refund deposit | DI-752 / R127 |
| Extension · Swap · Overdue · Late fee | The active-rental words; a quick swap restarts the clock, a late swap earns a free extension. | Renewal, Exchange (for a swap) | DI-761 / DI-762 / DI-764 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-1061` | Platform Command Center | C | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-1062` | Tenant & Brand Context | A | 82 | 11 | 6 | 28 | 0 | 6 | — | notStarted (—) |
| `BO-1063` | Venue-Specific Configuration | B | 85 | 0 | 6 | 17 | 0 | 0 | — | notStarted (—) |
| `BO-1064` | Naming, Numbering & Localization | C | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-1065` | Currency, Timezone & Channels | A | 47 | 17 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `BO-1066` | Roles, Permissions & Masking | B | 92 | 16 | 6 | 15 | 1 | 5 | — | notStarted (—) |
| `BO-1067` | Seat Approval Workflows | B | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1068` | Lifecycle & Environment Promotion | B | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (—) |
| `BO-1069` | Platform Health & Observability | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1070` | Setup, Clone & Inheritance | C | 0 | 30 | 6 | 3 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1061, BO-1064, BO-1067, BO-1068, BO-1069 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1061` Platform Command Center

**See the venue's maps and seat maps and their readiness, and open setup, cloning and integration from here.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block C · task VM-BO-1061 |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `VENUE_MAP_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/platform-command-center-bo-1061` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Readiness of the venue's maps (seat maps and venue maps) at a glance.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listVenueMaps return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/venue-map.yaml#listVenueMaps; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): The purpose is a platform-wide tenant and environment command centre, which belongs to the TICVAI Console. (CHG-WIR-026).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Validated · Published · Archived | `listSeatMaps` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **map readiness**: Seat maps and venue maps as two lists with status. *(source: contracts/satellite/venue-map.yaml#listVenueMaps / contracts/satellite/seating.yaml#listSeatMaps)*

**Data it reads**: `listVenueMaps` (onLoad, Venues and their maps); `listSeatMaps` (onLoad, Seat maps across them)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1062` Tenant & Brand Context: *Tenant & Brand Context*
- → `BO-1063` Venue-Specific Configuration: *Venue-Specific Configuration*
- → `BO-1064` Naming, Numbering & Localization: *Naming, Numbering & Localization*
- → `BO-1065` Currency, Timezone & Channels: *Currency, Timezone & Channels*
- → `BO-1066` Roles, Permissions & Masking: *Roles, Permissions & Masking*
- → `BO-1067` Seat Approval Workflows: *Seat Approval Workflows*
- → `BO-1068` Lifecycle & Environment Promotion: *Lifecycle & Environment Promotion*
- → `BO-1069` Platform Health & Observability: *Platform Health & Observability*
- → `BO-1070` Setup, Clone & Inheritance: *Setup, Clone & Inheritance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the platform are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
readiness:
  seatMaps: 3 published, 1 draft
  venueMaps: 2 published
```

#### Permissions

- `listVenueMaps` → `VENUE_MAP_VIEW` (read) · staff
- `listSeatMaps` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.13.3 | Seat Management APIs | Seat Management & Venue Mapping | CONTRACTED | `listSeatMaps` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1061` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1061`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 1: Opens Platform Command Center → Provide a platform-wide view of tenant, venue and environment readiness. Show tenants, brands, venues, environments, active users, pending approvals, deployments and failed jobs. Display service …
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F285 branch at step 1 (expected): when Nothing has been set up on Platform Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F285 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1062`, `BO-1063`, `BO-1064`, `BO-1065`, `BO-1066`, `BO-1067`, `BO-1068`, `BO-1069`, `BO-1070`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `VENUE_MAP_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1062` Tenant & Brand Context

**See where this venue sits in the tenant's hierarchy (tenant, brand, region, venue) and set the defaults every venue inherits unless it overrides them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `core` module |
| Block | Block A · ticket #27942 (APP-SETUP-BO-1062) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): The organisation node in context, with the tenant's venue-setting defaults edited beside it (defined 4 October 2026, CHG-FXS-001). |
| Offline | online only |
| Opens with | `orgUnitId` (navigation) |
| Route | `/access-venue/tenant-brand-context-bo-1062` |

**What the spec says about it.** **Defined 4 October 2026 from OrgUnit (getOrgUnit) and the tenant's venue-setting defaults. Legal entity, isolation, encryption and residency are set on their own screens (finance, BO-1065)** (CHG-FXS-001)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Tenant and brand context and the defaults venues inherit (seat management). Tenant-level defaults set here apply to every venue unless overridden there.

**Fixed on main** (the package already carries these; draw what it says): requiresModule 'seating' on the tenant and brand context. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Cart hold (seconds) | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `VenueSettings.cartLeaseSeconds` |
| Display currencies | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `VenueSettings.displayCurrencies` |
| Calendar day starts at (hour) | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a … | `VenueSettings.calendarDayStartHour` |

**Form: Save venue setting defaults** (modal, opened by *Save venue setting defaults*; *Save venue setting defaults* calls `setVenueSettingsDefaults`, *Cancel* sends nothing)

**Collects what `setVenueSettingsDefaults` sends before it is called.** The body is a `VenueSettings`: every field is the default a venue inherits where it leaves the setting null (decided 28 September, audit R094). Tenant scope; needs `TENANT_CONFIGURE`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettingsDefaults` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettingsDefaults` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettingsDefaults` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettingsDefaults` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettingsDefaults` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettingsDefaults` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettingsDefaults` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettingsDefaults` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettingsDefaults` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettingsDefaults` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettingsDefaults` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettingsDefaults` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettingsDefaults` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettingsDefaults` body |
| Consent form `biometrics.consentFormId` | picker: choose a consent form | optional | — | Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access … | shows names, sends the id | The venue's own consent form, which every biometric capture is taken on (decided 2 October 2026, Chinmay, batch 4, BO-188: "Consent first, on the venue's consent form"; DEC-128 … | `setVenueSettingsDefaults` body |
| Allow minors `biometrics.allowMinors` | toggle | optional | on | Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method. | — | Whether this venue enrols minors at all (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: "Guardian consent on the venue's form; minor age per country; the … | `setVenueSettingsDefaults` body |
| Accreditation face matching `biometrics.accreditationFaceMatching` | group | optional | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables it, with applicant …; Enabling it is refused without `legalSignOffReference` … | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables … | `setVenueSettingsDefaults` body |
| Is enabled `biometrics.accreditationFaceMatching.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettingsDefaults` body |
| Legal sign off reference `biometrics.accreditationFaceMatching.legalSignOffReference` | text field | optional | — | max length 200 | — | The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when. | `setVenueSettingsDefaults` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettingsDefaults` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettingsDefaults` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettingsDefaults` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettingsDefaults` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettingsDefaults` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettingsDefaults` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettingsDefaults` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettingsDefaults` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettingsDefaults` body |
| Charge currencies `chargeCurrencies` | list of values (chips) | optional | — | presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. | — | Which currencies a guest may select and pay in (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). | `setVenueSettingsDefaults` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettingsDefaults` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettingsDefaults` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettingsDefaults` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettingsDefaults` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettingsDefaults` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| … 34 more | | | | | | the rest are in `schemas.json` | `setVenueSettingsDefaults` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Venue setting defaults**: Tenant scope; each value shows which venues override it. *(source: ADR-0018; contracts/spine/tenancy.yaml#setVenueSettingsDefaults)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVenueSettingsDefaults: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setVenueSettingsDefaults)*

#### Outputs: what the screen shows and produces

**Shown**

**Where this sits** (detail panel, from `getOrgUnit`): path is shown as tenant > brand > region > venue.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Code | text | — |
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Path | text | Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`. |
| Is active | yes / no (icon or chip) | False causes every permission query at or beneath this node to resolve to DENY. |
| Child count | 1,234 | — |

**Venue setting defaults** (detail panel, from `getVenueSettingsDefaults`)

| Shows | Format | Notes |
|---|---|---|
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |
| Display currencies | list or chips (count when long) | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). |
| Cart lease seconds | 1,234 | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue setting defaults (secondary button) | `setVenueSettingsDefaults` PUT `/venue-settings-defaults` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `TENANT_CONFIGURE`; opens modal first |

**Data it reads**: `getOrgUnit` (onLoad, The node opened (orgUnitId), or the venue in session, with …); `getVenueSettingsDefaults` (onLoad, The tenant's default for every venue setting — the …)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The node and the defaults. |
| Error (`?state=error`) | Could not load. Names the read that failed. |
| Empty, first run (`?state=emptyFirstRun`) | Never saved: the platform defaults show. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tenant brand context are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `getOrgUnit` requires to show this screen, and names that permission (the screen's other reads need `TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TENANT_CONFIGURE` for `setVenueSettingsDefaults`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds SCOPE_VIEW, TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Save venue setting defaults. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setVenueSettingsDefaults)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getOrgUnit (OrgUnit):
- code: AQC-AUH
  name: AquaCove Abu Dhabi
  isActive: true
  childCount: 12
- code: AQC-DXB
  name: Main Gate Till 3
  isActive: true
  childCount: 3
```

#### Permissions

- `getOrgUnit` → `SCOPE_VIEW` (read) · staff
- `getVenueSettingsDefaults` → `TENANT_VIEW` (read) · staff
- `setVenueSettingsDefaults` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `getOrgUnit` requires to show this screen, and names that permission (the screen's other reads need `TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TENANT_CONFIGURE` for `setVenueSettingsDefaults`.

#### Requirements it meets

28 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.14 | The system shall isolate users, permissions, configurations, and data between tenants. Users shall only access data belonging to their assigned tenant unless explicitly authorized. | F&B POS | CONTRACTED | `getOrgUnit` |
| 7.1.53 | Allow separate authorization policies for each tenant in a multi-tenant environment without impacting other tenants. | F&B POS | CONTRACTED | `getOrgUnit` |
| 7.3.1 | The sales system shall be able to manage the data transactions for Multi Tenants Sites | F&B POS | CONTRACTED | `getOrgUnit` |
| 13.1.46 | Multi-Tenant API Access - System shall support tenant-specific API access. | Developer & API Management | CONTRACTED | `getOrgUnit` |
| 13.2.11 | Data Isolation - Sandbox data shall be isolated from production. | Developer & API Management | CONTRACTED | `getOrgUnit` |
| 15.5.1 | Tenant-Specific Inventory - System shall support tenant-specific inventory. | Inventory Management | CONTRACTED | `getOrgUnit` |
| 15.5.2 | Venue-Specific Inventory - System shall support venue-specific inventory. | Inventory Management | CONTRACTED | `getOrgUnit` |
| 16.9.51 | Multi-Tenant Device Management - System shall support tenant-specific device management. | Device Management | CONTRACTED | `getOrgUnit` |
| 16.9.52 | Venue-Specific Device Management - System shall support venue-specific device management. | Device Management | CONTRACTED | `getOrgUnit` |
| 21.13.1 | Multi-Tenant Support | Seat Management & Venue Mapping | CONTRACTED | `getOrgUnit` |
| 21.13.2 | Venue-Specific Configuration | Seat Management & Venue Mapping | CONTRACTED | `getOrgUnit` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| … 16 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1062` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1062`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 2: Works in Tenant & Brand Context → Configure the hierarchy and isolation boundary for seat management. Maintain tenant, legal entity, brand, region, venue ownership, status and data-residency classification. Configure tenant …

#### Acceptance for the design

- [ ] Every input above is drawn (82), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue setting defaults.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1063` Venue-Specific Configuration

**Set this venue's seating and hold defaults without a separate seat system: how long a cart and a seat hold last, how often they extend, and how many seats a guest may book in one order.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29122 (VM-BO-1063) |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): One venue's seating defaults in one form (defined 4 October 2026 from VenueSettings.seating and the cart hold settings, CHG-FXS-001). |
| Offline | online only |
| Opens with | `venueId` (session) |
| Route | `/access-venue/venue-specific-configuration-bo-1063` |

**What the spec says about it.** **Defined 4 October 2026 from VenueSettings (cart lease and extensions, seat hold extensions, seats per order). Default map, naming, approvals and publishing policy are not venue settings in the contract and left the purpose** (CHG-FXS-001) **setVenueSettings replaces the whole settings row** (PUT; an omitted property returns to its default). The save sends the VenueSettings that getVenueSettings returned, with only this screen's group changed; nothing else is reset (CHG-FXS-003).

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Venue-specific overrides of the tenant defaults (map, hold duration, accessibility, channels). Each value shows the inherited default beside the override.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Cart hold (seconds) | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `VenueSettings.cartLeaseSeconds` |
| Cart extension (minutes) | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `VenueSettings.cartHoldExtensionMinutes` |
| Cart extensions allowed | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `VenueSettings.cartMaxExtensions` |
| Seat hold extension (seconds) | number field (seconds) | optional | 300 | min 60; max 1800 | — | What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). | `VenueSettings.seating.seatHoldExtensionSeconds` |
| Seat hold extensions allowed | stepper or slider | optional | 2 | min 0; max 5 | — | How many times a seat hold may be extended. Proposed, client to correct (audit R094). | `VenueSettings.seating.seatHoldMaxExtensions` |
| Seats per guest booking | stepper or slider | optional | 10 | min 1; max 50 | — | Seats one guest may take in one booking on a guest channel (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. | `VenueSettings.seating.maxSeatsPerGuestOrder` |

**Sent by *Save venue settings*** (`setVenueSettings`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettings` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettings` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettings` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettings` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettings` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettings` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettings` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettings` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettings` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettings` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettings` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettings` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettings` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettings` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettings` body |
| Consent form `biometrics.consentFormId` | picker: choose a consent form | optional | — | Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access … | shows names, sends the id | The venue's own consent form, which every biometric capture is taken on (decided 2 October 2026, Chinmay, batch 4, BO-188: "Consent first, on the venue's consent form"; DEC-128 … | `setVenueSettings` body |
| Allow minors `biometrics.allowMinors` | toggle | optional | on | Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method. | — | Whether this venue enrols minors at all (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: "Guardian consent on the venue's form; minor age per country; the … | `setVenueSettings` body |
| Accreditation face matching `biometrics.accreditationFaceMatching` | group | optional | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables it, with applicant …; Enabling it is refused without `legalSignOffReference` … | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables … | `setVenueSettings` body |
| Is enabled `biometrics.accreditationFaceMatching.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Legal sign off reference `biometrics.accreditationFaceMatching.legalSignOffReference` | text field | optional | — | max length 200 | — | The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when. | `setVenueSettings` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettings` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettings` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettings` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettings` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettings` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettings` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettings` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettings` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettings` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettings` body |
| Charge currencies `chargeCurrencies` | list of values (chips) | optional | — | presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. | — | Which currencies a guest may select and pay in (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). | `setVenueSettings` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettings` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettings` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettings` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettings` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettings` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| … 34 more | | | | | | the rest are in `schemas.json` | `setVenueSettings` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVenueSettings: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setVenueSettings)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue settings (primary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getVenueSettings` (onLoad, Venue configuration)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The form with the venue's saved values. |
| Error (`?state=error`) | Could not load. Names the read that failed; nothing is editable until it loads. |
| Empty, first run (`?state=emptyFirstRun`) | Never saved: the form shows the defaults getVenueSettings returns. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue-specific are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_VIEW`, which `getVenueSettings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TENANT_CONFIGURE` for `setVenueSettings`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for setVenueSettings. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*
- **setVenueSettings answers 422**: Show it as something the person can act on, not a failure: **An enable the venue cannot evidence.** Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender verification where no device in the venue reports `genderClassification`. `errors[]` names each missing field or the missing capability. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
overrides:
  holdDurationSeconds: 480 (tenant default 600)
  defaultMap: Wave Arena main
  accessibleSeatsHeld: true
```

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_VIEW`, which `getVenueSettings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TENANT_CONFIGURE` for `setVenueSettings`.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| 16.9.58 | Device Incident Management - System shall support device incident management. | Device Management | CONTRACTED | data `VenueSettings` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1063` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1063`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 4: Works in Venue-Specific Configuration → Set local defaults without creating separate seat systems. Configure default map, lock/hold duration, naming, accessibility, sales channels, approvals and publishing policy. Map local entrances …

#### Acceptance for the design

- [ ] Every input above is drawn (85), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1063?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue settings, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1064` Naming, Numbering & Localization

**Control how seat entities and values appear in each venue and language. Configure venue/section/row/seat code formats, numbering direction, padding, prefixes and reserved values. Maintain translated labels, supported languages, text direction, pluralization and fallback language. Validate uniqueness and preview labels on map, ticket, cart, POS, access device and report. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block C · task VM-BO-1064 |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `regionId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/naming-numbering-localization-bo-1064` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How seat codes appear: section, row and seat formats, numbering direction, prefixes, and translated labels.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **numbering**: Format and direction previewed on a row; Arabic labels for sections. *(source: contracts/satellite/seating.yaml#updateSeats / contracts/spine/tenancy.yaml#getRegionSettings / DI-019)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seats (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The naming numbering localization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the naming numbering localization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No naming numbering localization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the naming numbering localization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Map is published and the change is structural |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
format:
  section: L101
  row: A-Z
  seat: 1-30 left to right
  sectionAr: السفلي 101
```

#### Permissions

- `updateSeats` → `CAPACITY_CONFIGURE` (configure) · staff
- `getRegionSettings` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.30 | Bulk Configuration and Updates AI can: Apply seat categories to thousands of seats simultaneously. Update pricing zones across multiple venues. Clone and modify existing seat maps. Generate … | Ticketing Catalogue | CONTRACTED | `updateSeats` |
| 21.1.1 | Drag & Drop Venue Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.2 | Section Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.3 | Row Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.4 | Seat Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.2.15 | Manual Adjustment Layer | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1064` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1064`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 6: Works in Naming, Numbering & Localization → Control how seat entities and values appear in each venue and language. Configure venue/section/row/seat code formats, numbering direction, padding, prefixes and reserved values. Maintain translated …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seats, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1065` Currency, Timezone & Channels

**Set the region's currency, rounding, date and number formats, time zone and fiscal year, the notes and coins every till counts, and the AI residency class the AI engine routes this tenant's calls by (the residency section, drawn and built in Block A; Chinmay, 3 October 2026, r1 additions).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup · wave 1 · needs the `core` module |
| Block | Block A · ticket #28729 (APP-SETUP-BO-1065) |
| Who uses it | venue staff holding `REGION_CONFIGURE`, `SCOPE_VIEW`, `SHIFT_OPEN` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `regionId` (navigation) |
| Route | `/access-venue/currency-timezone-channels-bo-1065` |

**What the spec says about it.** **The generator's 'needs a person' gap removed 4 October 2026: the screen's content is defined (tables, panels and actions bound to its operations)** (CHG-FXS-005)

**From the Food, Beverage & Retail process.** Region settings: the trading currency and its decimals, time zone, date and number formats, fiscal year start, and the notes and coins every till in the region counts. Written at region scope by someone who holds region configuration, and inherited by every venue beneath. One thing to get right: currency and decimals freeze once the region has traded, and denominations are never deleted — a note taken out of circulation is deactivated so past cash-ups still read.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- "Channels" — enabling web, mobile, POS, box office, call centre, B2B, partner API and marketplace per venue — has no operation, and RegionSettings has no channels. (CHG-SBO-005)
- The purpose asks for week start and daylight-saving behaviour; RegionSettings has neither field. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Placement — the screen sits in the F&B process list, its module is "Access & Venue" with requiresModule seating (from the seat-mapping … (CHG-SBO-003); No read of the region's settings is declared (getRegionSettings), while updateRegionSettings replaces the whole record. (CHG-WIR-008); The layout has no content region (only Save/Cancel) because the pack page gave no fields. (CHG-SBO-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a week-start setting needed (Saturday/Sunday/Monday) for reports and calendars?** → Drawn default stands (answer: "Default / recommended accepted"): Not drawn. *(decided by Chinmay, 2026-10-02; DEC-042 / CHG-NOTE-004)*
- **The screen is wave 3 while Block A tills need denominations; is the R229 seed enough for the first release?** → Drawn default stands (answer: "Default / recommended accepted"): Seed covers r1; the screen is still drawn in full. *(decided by Chinmay, 2026-10-02; DEC-043 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| AI residency class | segmented control | optional | Uae only | Uae only · Global allowed · On prem; 5-122B, Falcon-H1 Arabic or Jais 2), only where the client asks for it (CHG-R1S-002).; Moving from `uaeOnly` to `globalAllowed` without `aiResidencyOptIn` is refused `422 residency-opt-in-required`; on a tenant … | — | UAE only, Global allowed, On-premises. Moving from UAE only to Global allowed without the opt-in evidence below is refused (`422 residency-opt-in-required`) and the form says which reference is … | `RegionSettings.aiResidencyClass` |
| Allowed AI residencies | list of values (chips) | optional | — | — | — | Narrows the class further where the region needs it; never widens it. Empty means the class alone decides. `ai.setAiProvider` refuses a provider outside it (`409 residency-refused`). | `RegionSettings.allowedAiResidencies` |
| Opt-in evidence (PDPL Article 23) | group | optional | — | — | — | Shown only for Global allowed: the vendor contract, DPIA and guest notice references (`vendorContractReference`, `dpiaReference`, `guestNoticeReference`, up to 200 characters each). Who confirmed it … | `RegionSettings.aiResidencyOptIn` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include inactive | toggle | on | — | `listDenominations` ?includeInactive |

**Form: Save region settings** (modal, opened by *Save region settings*; *Save region settings* calls `updateRegionSettings`, *Cancel* sends nothing)

**Collects what `updateRegionSettings` sends before it is called.** Required: `countryCode`, `currencyCode`, `currencyScale`, `timeZone`, `fiscalYearStartMonth`. Optional: `dateFormat`, `numberFormat`, `allowedAiResidencies`, `aiResidencyClass`, `aiResidencyOptIn`, `localLanguageNameLocales`, `requiredBillingDocuments`, `minorAgeThreshold`, `placement`. Currency, rounding (scale), date and number formats, time zone (IANA; daylight saving follows it) and fiscal year start. Week start and channels are logged gaps (CHG-SBO-005). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell. | `updateRegionSettings` body |
| Currency code `currencyCode` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `updateRegionSettings` body |
| Currency scale `currencyScale` | stepper or slider | required | — | min 0; max 4 | — | Decimal places for this region's currency. Varies by currency — some use 2, some use 3. | `updateRegionSettings` body |
| Time zone `timeZone` | text field | required | — | — | — | IANA zone, e.g. `Asia/Dubai`. | `updateRegionSettings` body |
| Date format `dateFormat` | text field | optional | dd/MM/yyyy | — | — | — | `updateRegionSettings` body |
| Number format `numberFormat` | text field | optional | #,##0.00 | — | — | — | `updateRegionSettings` body |
| Fiscal year start month `fiscalYearStartMonth` | stepper or slider | required | — | min 1; max 12 | — | Varies by country. | `updateRegionSettings` body |
| Allowed AI residencies `allowedAiResidencies` | list of values (chips) | optional | — | — | — | The region's compliance gate on AI providers (decided 28 September, audit R203; ADR-0009). | `updateRegionSettings` body |
| AI residency class `aiResidencyClass` | segmented control | optional | Uae only | Uae only · Global allowed · On prem; 5-122B, Falcon-H1 Arabic or Jais 2), only where the client asks for it (CHG-R1S-002).; Moving from `uaeOnly` to `globalAllowed` without `aiResidencyOptIn` is refused `422 residency-opt-in-required`; on a tenant … | — | The tenant's AI residency class (decided 2 October 2026, Chinmay, "AI residency: per-tenant residency class"; DEC-539; CHG-CSP-009; amends AI-D02 and ADR-0009 section 1). | `updateRegionSettings` body |
| AI residency opt in `aiResidencyOptIn` | group | optional | — | — | — | The evidence a `globalAllowed` opt-in needs under PDPL Article 23 (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract, its DPIA and the notice guests see. | `updateRegionSettings` body |
| Vendor contract reference `aiResidencyOptIn.vendorContractReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Dpia reference `aiResidencyOptIn.dpiaReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Guest notice reference `aiResidencyOptIn.guestNoticeReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Local language name locales `localLanguageNameLocales` | list of values (chips) | optional | — | — | — | The languages an outlet name must also be given in, in this country (decided 2 October 2026, Chinmay, batch 2 #26: "English plus the local language where the country needs it" … | `updateRegionSettings` body |
| Required billing documents `requiredBillingDocuments` | repeatable rows | optional | {'document type': 'trade licence', 'required when': 'always'}, {'document type': 'vat certificate', 'required when': 'trn entered'} | — | — | Which documents a TICVAI customer's billing entity must upload, in this country (decided 2 October 2026, Chinmay, batch 6 set 7, ADM-411: "Trade licence always; VAT certificate … | `updateRegionSettings` body |
| Document type `requiredBillingDocuments[].documentType` | text field | optional | — | max length 64 | — | The document kind, as the subscription contract's `PartnerDocument` names it (`tradeLicence`, `vatCertificate`, ...). | `updateRegionSettings` body |
| Required when `requiredBillingDocuments[].requiredWhen` | segmented control | optional | — | Always · Trn entered | — | — | `updateRegionSettings` body |
| Minor age threshold `minorAgeThreshold` | stepper or slider | optional | 18 | min 0; max 21 | — | The age below which a guest is a minor here, set per country (decided 2 October 2026, Chinmay, critical set 1, BO-187: "Guardian consent on the venue's form; minor age per … | `updateRegionSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Currency or scale change rejected because transactions exist in this region, or a change to `aiResidencyClass` on a tenant TICVAI locked to `uaeOnly` …; 422 `aiResidencyClass` `globalAllowed` without the three references of `aiResidencyOptIn` (`residency-opt-in-required`; PDPL Article 23; DEC-539; CHG-CSP-009).

**Form: Save AI residency** (modal, opened by *Save AI residency*; *Save AI residency* calls `updateRegionSettings`, *Cancel* sends nothing)

**Collects the residency section before `updateRegionSettings` is called** (3 October 2026, CHG-RONEC-004). Asks for `aiResidencyClass`, `allowedAiResidencies` and, for `globalAllowed`, the three `aiResidencyOptIn` references; every other field is sent as `getRegionSettings` returned it. A move to a wider class says what changes for guests (calls may leave the UAE) and asks the operator to confirm. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell. | `updateRegionSettings` body |
| Currency code `currencyCode` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `updateRegionSettings` body |
| Currency scale `currencyScale` | stepper or slider | required | — | min 0; max 4 | — | Decimal places for this region's currency. Varies by currency — some use 2, some use 3. | `updateRegionSettings` body |
| Time zone `timeZone` | text field | required | — | — | — | IANA zone, e.g. `Asia/Dubai`. | `updateRegionSettings` body |
| Date format `dateFormat` | text field | optional | dd/MM/yyyy | — | — | — | `updateRegionSettings` body |
| Number format `numberFormat` | text field | optional | #,##0.00 | — | — | — | `updateRegionSettings` body |
| Fiscal year start month `fiscalYearStartMonth` | stepper or slider | required | — | min 1; max 12 | — | Varies by country. | `updateRegionSettings` body |
| Allowed AI residencies `allowedAiResidencies` | list of values (chips) | optional | — | — | — | The region's compliance gate on AI providers (decided 28 September, audit R203; ADR-0009). | `updateRegionSettings` body |
| AI residency class `aiResidencyClass` | segmented control | optional | Uae only | Uae only · Global allowed · On prem; 5-122B, Falcon-H1 Arabic or Jais 2), only where the client asks for it (CHG-R1S-002).; Moving from `uaeOnly` to `globalAllowed` without `aiResidencyOptIn` is refused `422 residency-opt-in-required`; on a tenant … | — | The tenant's AI residency class (decided 2 October 2026, Chinmay, "AI residency: per-tenant residency class"; DEC-539; CHG-CSP-009; amends AI-D02 and ADR-0009 section 1). | `updateRegionSettings` body |
| AI residency opt in `aiResidencyOptIn` | group | optional | — | — | — | The evidence a `globalAllowed` opt-in needs under PDPL Article 23 (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract, its DPIA and the notice guests see. | `updateRegionSettings` body |
| Vendor contract reference `aiResidencyOptIn.vendorContractReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Dpia reference `aiResidencyOptIn.dpiaReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Guest notice reference `aiResidencyOptIn.guestNoticeReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Local language name locales `localLanguageNameLocales` | list of values (chips) | optional | — | — | — | The languages an outlet name must also be given in, in this country (decided 2 October 2026, Chinmay, batch 2 #26: "English plus the local language where the country needs it" … | `updateRegionSettings` body |
| Required billing documents `requiredBillingDocuments` | repeatable rows | optional | {'document type': 'trade licence', 'required when': 'always'}, {'document type': 'vat certificate', 'required when': 'trn entered'} | — | — | Which documents a TICVAI customer's billing entity must upload, in this country (decided 2 October 2026, Chinmay, batch 6 set 7, ADM-411: "Trade licence always; VAT certificate … | `updateRegionSettings` body |
| Document type `requiredBillingDocuments[].documentType` | text field | optional | — | max length 64 | — | The document kind, as the subscription contract's `PartnerDocument` names it (`tradeLicence`, `vatCertificate`, ...). | `updateRegionSettings` body |
| Required when `requiredBillingDocuments[].requiredWhen` | segmented control | optional | — | Always · Trn entered | — | — | `updateRegionSettings` body |
| Minor age threshold `minorAgeThreshold` | stepper or slider | optional | 18 | min 0; max 21 | — | The age below which a guest is a minor here, set per country (decided 2 October 2026, Chinmay, critical set 1, BO-187: "Guardian consent on the venue's form; minor age per … | `updateRegionSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Currency or scale change rejected because transactions exist in this region, or a change to `aiResidencyClass` on a tenant TICVAI locked to `uaeOnly` …; 422 `aiResidencyClass` `globalAllowed` without the three references of `aiResidencyOptIn` (`residency-opt-in-required`; PDPL Article 23; DEC-539; CHG-CSP-009).

**Form: Save notes and coins** (modal, opened by *Save notes and coins*; *Save notes and coins* calls `setDenominations`, *Cancel* sends nothing)

**Collects what `setDenominations` sends before it is called.** Required: `currencyCode`, `denominations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | — | — | The region the write is made at — the materialised path of a `region` scope node. | `setDenominations` body |
| Currency code `currencyCode` | text field | required | — | min length 3; max length 3 | — | — | `setDenominations` body |
| Denominations `denominations` | repeatable rows | required | — | at least 1 | — | — | `setDenominations` body |
| Display name `denominations[].displayName` | text field | required | — | max length 60 | — | — | `setDenominations` body |
| Kind `denominations[].kind` | segmented control | required | — | Note · Coin | — | — | `setDenominations` body |
| Value `denominations[].value` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setDenominations` body |
| Sort order `denominations[].sortOrder` | number field | required | — | min 0 | — | — | `setDenominations` body |
| Is active `denominations[].isActive` | toggle | optional | on | — | — | — | `setDenominations` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 A zero or negative value, or two entries with the same value and kind (problem type `denomination-invalid`).

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Region**: When the user configures several regions, pick one first; the save names that region. *(source: contracts/spine/shift.yaml#setDenominations)*
- **Currency and decimals**: ISO 4217 code with its decimals (AED 2; BHD, KWD, OMR 3), set together. Locked with the reason "This region has transactions" once it has traded (409). *(source: contracts/spine/tenancy.yaml#updateRegionSettings / ADR-0008 / DI-306)*
- **Time zone**: IANA zone picker (Asia/Dubai for the UAE). No separate daylight-saving setting — the zone carries it. *(source: contracts/spine/tenancy.yaml#/components/schemas/RegionSettings)*
- **Date and number format**: Defaults dd/MM/yyyy and *(source: contracts/spine/tenancy.yaml#/components/schemas/RegionSettings)*
- **Denominations**: Per currency: note or coin, face value above zero, unique per kind and value, display name (English and Arabic), counting order by drag (notes highest first, coins as they sit in the tray), active toggle. Removing a row deactivates it. UAE seed: notes 5, 10, 20, 50, 100, 200, 500, 1000 AED; coins 25 fils, 50 fils, 1 AED. *(source: R229 / contracts/spine/shift.yaml#setDenominations / contracts/spine/shift.yaml#/components/schemas/Denomination / DI-306)*

#### Outputs: what the screen shows and produces

**Shown**

**Region settings** (detail panel, from `getRegionSettings`)

| Shows | Format | Notes |
|---|---|---|
| Country code | text | ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell. |
| Currency code | text | — |
| Currency scale | 1,234 | Decimal places for this region's currency. Varies by currency — some use 2, some use 3. |
| Time zone | text | IANA zone, e.g. `Asia/Dubai`. |
| Date format | text | — |
| Number format | text | — |
| Fiscal year start month | 1,234 | Varies by country. |

**Notes and coins** (data table, from `listDenominations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Currency code | text | — |
| Display name | text | What the cashier reads — *AED 500*, *Coin*. Localised, because a count screen is read at speed. |
| Kind | chip: Note, Coin | — |
| Sort order | 1,234 | Counting order, not value order. Notes highest first, coins as they sit in the tray. |
| Is active | yes / no (icon or chip) | The field that makes this a table. A note withdrawn from circulation is deactivated and stays in the count history — a JSON blob cannot … |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**AI residency** (detail panel, from `getRegionSettings`): **The residency section, real since 3 October 2026** (Chinmay, r1 additions: "The residency section on BO-1065 is drawn and built in Block A"; CHG-RONEC-004). Where the AI engine may send this tenant's calls (ADR-0009 as amended 2 October; DEC-539): UAE only (the default, and mandatory for government, bank and health tenants), global allowed (a private venue's PDPL Article 23 opt-in) or …

| Shows | Format | Notes |
|---|---|---|
| AI residency class | chip: Uae only, Global allowed, On prem | The tenant's AI residency class (decided 2 October 2026, Chinmay, "AI residency: per-tenant residency class"; DEC-539; CHG-CSP-009; amends … |
| Allowed AI residencies | list or chips (count when long) | The region's compliance gate on AI providers (decided 28 September, audit R203; ADR-0009). |
| AI residency opt in | grouped details | The evidence a `globalAllowed` opt-in needs under PDPL Article 23 (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save region settings (primary button) | `updateRegionSettings` PUT `/regions/{regionId}/settings` | RegionSettings | RegionSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save notes and coins (secondary button) | `setDenominations` PUT `/denominations` | SetDenominationsRequest | Denomination[] | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 A zero or negative value, or two entries with the same value and kind (problem type `denomination-invalid`). | opens modal first |
| Save AI residency (secondary button) | `updateRegionSettings` PUT `/regions/{regionId}/settings` | RegionSettings | RegionSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Till count preview**: The denomination list as the till's count screen will show it, in counting order, with note and coin images. *(source: DI-775 / contracts/spine/shift.yaml#listDenominations)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save region settings**: Replaces the region's settings whole; 409 when a currency or decimals change is attempted after trading. *(source: contracts/spine/tenancy.yaml#updateRegionSettings)*
- **Save denominations**: Returns the full list including deactivated rows; 422 "zero or duplicate denomination" or "this currency is not traded in the region". *(source: contracts/spine/shift.yaml#setDenominations)*

**Data it reads**: `listDenominations` (onLoad, The notes and coins tills count); `getRegionSettings` (onLoad, The region's settings in force)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The currency timezone channels list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the currency timezone channels untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing saved yet.** The form opens on the region's values and Save region settings (`updateRegionSettings`) saves them; offers no other create action. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Currency or scale change rejected because transactions exist in this region, or a change to `aiResidencyClass` on a tenant TICVAI locked to `uaeOnly` …; 422 A zero or negative value, or two entries with the same value and kind (problem type `denomination-invalid`).; 422 `aiResidencyClass` `globalAllowed` without the three references of `aiResidencyOptIn` … |

#### Edge cases to draw

- **A note withdrawn from circulation**: Deactivated, still listed (marked) so a till that finds one can record it. *(source: contracts/spine/shift.yaml#listDenominations)*
- **A venue in the region trading in a second currency**: Its denominations are set here under that currency. *(source: contracts/spine/shift.yaml#setDenominations / ADR-0018)*

#### Consistency with other screens

- Match `POS-001`: Begin Shift's float count uses this list and order.
- Match `POS-007`: Close Shift's blind count uses the same list.
- Match `BO-065`: The venue shows the currency read-only and chooses guest display currencies there.
- Match `BO-077`: Exchange rates per region are there, not here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
region: United Arab Emirates
settings:
  currency: AED
  decimals: 2
  time_zone: Asia/Dubai
  date_format: dd/MM/yyyy
  number_format: '#,##0.00'
  fiscal_year_start: January
denominations:
- AED 1000 (note)
- AED 500
- AED 200
- AED 100
- AED 50
- AED 20
- AED 10
- AED 5
- AED 1 (coin)
- 50 fils
- 25 fils
bahrain_example:
  currency: BHD
  decimals: 3
  note: no 1000 note
```

#### Permissions

- `listDenominations` → `SHIFT_OPEN` (operate) · staff
- `setDenominations` → `REGION_CONFIGURE` (configure) · staff
- `updateRegionSettings` → `REGION_CONFIGURE` (configure) · staff
- `getRegionSettings` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1065` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1065`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 8: Works in Currency, Timezone & Channels → Configure regional display and channel availability. Set currency, rounding, date/time/number formats, timezone, week start and daylight-saving behavior. Enable web, mobile, POS, box office, call …
- ADR-0009 *AI Data Residency* (`docs/adr/0009-ai-data-residency.md`)
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1065?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save region settings, Save notes and coins, Save AI residency.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `REGION_CONFIGURE`, `SCOPE_VIEW`, `SHIFT_OPEN`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1066` Roles, Permissions & Masking

**Enforce least-privilege access to seat administration and operational data. Configure RBAC/PBAC for maps, layouts, inventory, locks, holds, pricing, reports, integrations and audit. Apply venue/region scope, field masking, temporary/delegated access, segregation of duties and emergency override. Preview effective access for a user/context and log sensitive read, export and administrative actions. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `core` module |
| Block | Block B · ticket #29053 (VM-BO-1066) |
| Who uses it | venue staff holding `PERMISSION_GRANT`, `PERMISSION_MANAGE`, `PERMISSION_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Access policies listed with the selected one edited, simulated and moved through its states, and the findings and reviews beside them (defined 4 October 2026, CHG-FXS-001). |
| Offline | online only |
| Opens with | `policyId` (navigation), `campaignId` (navigation), `itemId` (navigation) |
| Route | `/access-venue/roles-permissions-masking-bo-1066` |

**What the spec says about it.** **No default roles (DEC-007):** the access policy reads the role's per-module checklist; presets only fill it. **Defined 4 October 2026 from AuthorisationPolicy, IdentityPermissionFinding and IdentityAccessReviewCampaign with the screen's bound operations** (CHG-FXS-001)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Attribute-based access policies with field masking, temporary and emergency access, simulation and history. Every policy can be simulated for a person before it is enabled.

**Fixed on main** (the package already carries these; draw what it says): requiresModule 'seating' on the tenant's access-policy screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Policy name | text field | optional | — | — | — | — | `AuthorisationPolicy.name` |
| Policy code | text field | optional | — | — | — | — | `AuthorisationPolicy.code` |
| Effect | segmented control | optional | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake … | `AuthorisationPolicy.effect` |
| Permissions | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `AuthorisationPolicy.permissions` |
| Combine conditions | segmented control | optional | All must match | All must match · Any may match | — | — | `AuthorisationPolicy.combining` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |
| Principal | picker: choose a principal | — | — | `listPermissionFindings` ?principalId |
| Role | picker: choose a role | — | — | `listPermissionFindings` ?roleId |
| Scope path | text field | — | — | `listPermissionFindings` ?scopePath |
| Kind | segmented control | — | Excessive · Missing · Conflicting | `listPermissionFindings` ?kind |
| Lookback days | number field (days) | 90 | min 7; max 365 | `listPermissionFindings` ?lookbackDays |
| Denied threshold | number field | 3 | min 1 | `listPermissionFindings` ?deniedThreshold |
| Draft policy | picker: choose a draft policy | — | — | `listPermissionFindings` ?draftPolicyId |
| Status | segmented control | — | Open · Completed · Expired | `listAccessReviewCampaigns` ?status |

**Sent by *Create access policy*** (`createAuthorisationPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `createAuthorisationPolicy` body |
| Name `name` | text field | required | — | — | — | — | `createAuthorisationPolicy` body |
| Description `description` | text area | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Is template `isTemplate` | toggle | optional | off | — | — | — | `createAuthorisationPolicy` body |
| Permissions `permissions` | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `createAuthorisationPolicy` body |
| Conditions `conditions` | repeatable rows | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Attribute `conditions[].attribute` | select | required | — | User.attribute · Employee.attribute · Employee.on shift · Membership.tier · Membership.status · Accreditation.type · Accreditation.status · Customer.segment · Resource.classification · Venue.attribute · Venue.id · Attraction.attribute … | — | — | `createAuthorisationPolicy` body |
| Key `conditions[].key` | text field | optional | — | — | — | For the `*.attribute` forms — which attribute, by code. | `createAuthorisationPolicy` body |
| Operator `conditions[].operator` | select | required | — | Equals · Not equals · In · Not in · Greater than · Less than · Between · Contains · Starts with · Exists | — | — | `createAuthorisationPolicy` body |
| Value `conditions[].value` | field | optional | — | — | — | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. | `createAuthorisationPolicy` body |
| Values `conditions[].values` | list of values (chips) | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Combining `combining` | segmented control | optional | All must match | All must match · Any may match | — | — | `createAuthorisationPolicy` body |
| Effect `effect` | segmented control | required | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of … | `createAuthorisationPolicy` body |
| Priority `priority` | number field | optional | 0 | — | — | — | `createAuthorisationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance … | `createAuthorisationPolicy` body |
| Applies to roles `appliesToRoleIds` | multi-picker: choose applies to roles | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAuthorisationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAuthorisationPolicy` body |
| Delegated admin roles `delegatedAdminRoleIds` | multi-picker: choose delegated admin roles | optional | — | — | — | 3.3.35. Who may edit this policy without being a platform administrator. | `createAuthorisationPolicy` body |

**Sent by *Save as new version*** (`updateAuthorisationPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `updateAuthorisationPolicy` body |
| Name `name` | text field | required | — | — | — | — | `updateAuthorisationPolicy` body |
| Description `description` | text area | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Is template `isTemplate` | toggle | optional | off | — | — | — | `updateAuthorisationPolicy` body |
| Permissions `permissions` | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `updateAuthorisationPolicy` body |
| Conditions `conditions` | repeatable rows | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Attribute `conditions[].attribute` | select | required | — | User.attribute · Employee.attribute · Employee.on shift · Membership.tier · Membership.status · Accreditation.type · Accreditation.status · Customer.segment · Resource.classification · Venue.attribute · Venue.id · Attraction.attribute … | — | — | `updateAuthorisationPolicy` body |
| Key `conditions[].key` | text field | optional | — | — | — | For the `*.attribute` forms — which attribute, by code. | `updateAuthorisationPolicy` body |
| Operator `conditions[].operator` | select | required | — | Equals · Not equals · In · Not in · Greater than · Less than · Between · Contains · Starts with · Exists | — | — | `updateAuthorisationPolicy` body |
| Value `conditions[].value` | field | optional | — | — | — | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. | `updateAuthorisationPolicy` body |
| Values `conditions[].values` | list of values (chips) | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Combining `combining` | segmented control | optional | All must match | All must match · Any may match | — | — | `updateAuthorisationPolicy` body |
| Effect `effect` | segmented control | required | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of … | `updateAuthorisationPolicy` body |
| Priority `priority` | number field | optional | 0 | — | — | — | `updateAuthorisationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance … | `updateAuthorisationPolicy` body |
| Applies to roles `appliesToRoleIds` | multi-picker: choose applies to roles | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAuthorisationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAuthorisationPolicy` body |
| Delegated admin roles `delegatedAdminRoleIds` | multi-picker: choose delegated admin roles | optional | — | — | — | 3.3.35. Who may edit this policy without being a platform administrator. | `updateAuthorisationPolicy` body |

**Sent by *Simulate*** (`simulateAuthorisationPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| Policy `policy` | group | optional | — | — | — | 3.3. Conditions and an effect, evaluated by one engine. | `simulateAuthorisationPolicy` body |
| Code `policy.code` | text field | required | — | — | — | — | `simulateAuthorisationPolicy` body |
| Name `policy.name` | text field | required | — | — | — | — | `simulateAuthorisationPolicy` body |
| Description `policy.description` | text area | optional | — | — | — | — | `simulateAuthorisationPolicy` body |
| Is template `policy.isTemplate` | toggle | optional | off | — | — | — | `simulateAuthorisationPolicy` body |
| Permissions `policy.permissions` | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `simulateAuthorisationPolicy` body |
| Conditions `policy.conditions` | repeatable rows | optional | — | — | — | — | `simulateAuthorisationPolicy` body |
| Attribute `policy.conditions[].attribute` | select | required | — | User.attribute · Employee.attribute · Employee.on shift · Membership.tier · Membership.status · Accreditation.type · Accreditation.status · Customer.segment · Resource.classification · Venue.attribute · Venue.id · Attraction.attribute … | — | — | `simulateAuthorisationPolicy` body |
| Key `policy.conditions[].key` | text field | optional | — | — | — | For the `*.attribute` forms — which attribute, by code. | `simulateAuthorisationPolicy` body |
| Operator `policy.conditions[].operator` | select | required | — | Equals · Not equals · In · Not in · Greater than · Less than · Between · Contains · Starts with · Exists | — | — | `simulateAuthorisationPolicy` body |
| Value `policy.conditions[].value` | field | optional | — | — | — | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. | `simulateAuthorisationPolicy` body |
| Values `policy.conditions[].values` | list of values (chips) | optional | — | — | — | — | `simulateAuthorisationPolicy` body |
| Combining `policy.combining` | segmented control | optional | All must match | All must match · Any may match | — | — | `simulateAuthorisationPolicy` body |
| Effect `policy.effect` | segmented control | required | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of … | `simulateAuthorisationPolicy` body |
| Priority `policy.priority` | number field | optional | 0 | — | — | — | `simulateAuthorisationPolicy` body |
| Scope path `policy.scopePath` | text field | optional | — | — | — | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance … | `simulateAuthorisationPolicy` body |
| Applies to roles `policy.appliesToRoleIds` | multi-picker: choose applies to roles | optional | — | — | — | — | `simulateAuthorisationPolicy` body |
| Effective from `policy.effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `simulateAuthorisationPolicy` body |
| Effective to `policy.effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `simulateAuthorisationPolicy` body |
| Delegated admin roles `policy.delegatedAdminRoleIds` | multi-picker: choose delegated admin roles | optional | — | — | — | 3.3.35. Who may edit this policy without being a platform administrator. | `simulateAuthorisationPolicy` body |
| Contexts `contexts` | repeatable rows | required | — | — | — | — | `simulateAuthorisationPolicy` body |
| Principal `contexts[].principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| Subject `contexts[].subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| Permission `contexts[].permission` | text field | optional | — | — | — | — | `simulateAuthorisationPolicy` body |
| Scope path `contexts[].scopePath` | text field | optional | — | — | — | — | `simulateAuthorisationPolicy` body |
| Venue `contexts[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| Attraction `contexts[].attractionId` | picker: choose an attraction | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| Device `contexts[].deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| Event `contexts[].eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `simulateAuthorisationPolicy` body |
| At `contexts[].at` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `simulateAuthorisationPolicy` body |
| Attributes `contexts[].attributes` | key and value settings | optional | — | — | — | Deliberately an open map, keyed by attribute (the `AccessCondition.attribute` vocabulary, with `key` for the `*.attribute` forms), each value the one a condition compares against. | `simulateAuthorisationPolicy` body |

**Sent by *Submit / approve / activate / retire*** (`setAuthorisationPolicyState`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| State `state` | radio group | required | — | Draft · Pending approval · Active · Suspended · Retired | — | — | `setAuthorisationPolicyState` body |
| Reason `reason` | text area | optional | — | — | — | — | `setAuthorisationPolicyState` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setAuthorisationPolicyState` body |

**Sent by *Emergency override*** (`createEmergencyAccessOverride`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Principal `principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | — | `createEmergencyAccessOverride` body |
| Scope path `scopePath` | text field | required | — | — | — | — | `createEmergencyAccessOverride` body |
| Permissions `permissions` | list of values (chips) | optional | — | — | — | — | `createEmergencyAccessOverride` body |
| Reason `reason` | text area | required | — | — | — | — | `createEmergencyAccessOverride` body |
| Expires at `expiresAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createEmergencyAccessOverride` body |

**Sent by *Start access review*** (`createAccessReviewCampaign`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createAccessReviewCampaign` body |
| Scope path `scopePath` | text field | required | — | — | — | The partition key (ADR-0005), and what is reviewed: every grant at or below it. Inside the caller's own scope. | `createAccessReviewCampaign` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | Only grants of these roles; null reviews every grant in scope. | `createAccessReviewCampaign` body |
| Reviewer mode `reviewerMode` | segmented control | required | — | Line manager · Named | — | `lineManager`: each item goes to the holder's manager from their primary work assignment, falling back to the named reviewers where none is found. | `createAccessReviewCampaign` body |
| Reviewer principals `reviewerPrincipalIds` | multi-picker: choose reviewer principals | optional | — | — | — | — | `createAccessReviewCampaign` body |
| Due at `dueAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAccessReviewCampaign` body |
| Recurrence `recurrence` | radio group | optional | None | None · Quarterly · Semi annual · Annual | — | — | `createAccessReviewCampaign` body |
| Prefill from findings `prefillFromFindings` | toggle | optional | on | — | — | — | `createAccessReviewCampaign` body |
| Lookback days `lookbackDays` | number field (days) | optional | 90 | min 7; max 365 | — | — | `createAccessReviewCampaign` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: createAuthorisationPolicy, updateAuthorisationPolicy, setAuthorisationPolicyState, restoreAuthorisationPolicyVersion: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/identity.yaml#createAuthorisationPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Access policies** (data table, from `listAuthorisationPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Effect | chip: Permit, Deny | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not … |
| Permissions | list or chips (count when long) | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being … |
| Applies to roles | list or chips (count when long) | — |
| Priority | 1,234 | — |
| Effective to | 1 Oct 2026, 14:30 | — |

**Permission findings** (data table, from `listPermissionFindings`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Excessive, Missing, Conflicting | — |
| Principal | the name it points at, never the id | — |
| Permission | text | — |
| Recommendation | chip: Revoke, Grant, Review | — |
| Last used at | 1 Oct 2026, 14:30 | The last permit that used it; null when never used in the window. |

**Access reviews** (data table, from `listAccessReviewCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Due at | 1 Oct 2026, 14:30 | — |
| Status | chip: Open, Completed, Expired | — |
| Item count | 1,234 | — |
| Decided count | 1,234 | Kept by `decideAccessReviewItem` in the same write, so the campaign list needs no count query. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create access policy (primary button) | `createAuthorisationPolicy` POST `/authorisation-policies` | AuthorisationPolicy | AuthorisationPolicy | — | — |
| Save as new version (secondary button) | `updateAuthorisationPolicy` PUT `/authorisation-policies/{policyId}` | AuthorisationPolicy | AuthorisationPolicy | — | — |
| Simulate (secondary button) | `simulateAuthorisationPolicy` POST `/authorisation-policies/simulate` | inline | AccessDecision[] | — | — |
| Submit / approve / activate / retire (secondary button) | `setAuthorisationPolicyState` POST `/authorisation-policies/{policyId}/state` | inline | AuthorisationPolicy | — | — |
| Emergency override (destructive button) | `createEmergencyAccessOverride` POST `/access-overrides` | inline | EmergencyAccessOverride | — | — |
| Start access review (secondary button) | `createAccessReviewCampaign` POST `/access-review-campaigns` | IdentityAccessReviewCampaign | IdentityAccessReviewCampaign | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 `dueAt` not in the future, `reviewerMode` `named` with no `reviewerPrincipalIds`, a `scopePath` outside the caller's own, or no … | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Emergency access override**: Time-boxed, reason required, alerted and audited. *(source: contracts/spine/identity.yaml#createEmergencyAccessOverride)*

**Data it reads**: `listAuthorisationPolicies` (onLoad, Who may see and change what); `listPermissionFindings` (onLoad, Excessive, missing and conflicting permissions, or those a …); `listAccessReviewCampaigns` (onLoad, Access review campaigns and progress)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access policies yet: roles alone decide. Carries Create access policy. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the roles permissions masking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PERMISSION_VIEW`, which `listAuthorisationPolicies` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_GRANT` for `decideAccessReviewItem`; `PERMISSION_MANAGE` for `createAuthorisationPolicy`, `updateAuthorisationPolicy` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 `revoke` without a `reason`, or `certify` against a `revoke` recommendation without one.; 409 Already decided, or the campaign is no longer `open` (`campaign-closed`).; 409 The target version was never approved, is the current version, or the policy is retired |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PERMISSION_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PERMISSION_MANAGE for createAuthorisationPolicy, updateAuthorisationPolicy, setAuthorisationPolicyState; PERMISSION_GRANT for decideAccessReviewItem. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#createAuthorisationPolicy)*
- **restoreAuthorisationPolicyVersion answers 409**: Show it as something the person can act on, not a failure: The target version was never approved, is the current version, or the policy is retired *(source: contracts/spine/identity.yaml#restoreAuthorisationPolicyVersion)*
- **createAccessReviewCampaign answers 422**: Show it as something the person can act on, not a failure: `dueAt` not in the future, `reviewerMode` `named` with no `reviewerPrincipalIds`, a `scopePath` outside the caller's own, or no grant in scope to review (`nothing-to-review`). *(source: contracts/spine/identity.yaml#createAccessReviewCampaign)*
- **decideAccessReviewItem answers 403**: Show it as something the person can act on, not a failure: The item is for a grant the caller holds, or the caller lacks `PERMISSION_GRANT` at its scope. *(source: contracts/spine/identity.yaml#decideAccessReviewItem)*
- **decideAccessReviewItem answers 409**: Show it as something the person can act on, not a failure: Already decided, or the campaign is no longer `open` (`campaign-closed`). *(source: contracts/spine/identity.yaml#decideAccessReviewItem)*

#### Consistency with other screens

- Match `BO-054`: Roles there, policies here; one access model.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  name: Finance masks guest phone
  effect: mask
  fields:
  - mobile
  appliesTo: 'Role: Finance'
  state: active
```

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff
- `createAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `simulateAuthorisationPolicy` → `PERMISSION_VIEW` (read) · staff
- `updateAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `setAuthorisationPolicyState` → `PERMISSION_MANAGE` (configure) · staff
- `createEmergencyAccessOverride` → `PERMISSION_MANAGE` (configure) · staff
- `listAuthorisationPolicyHistory` → `PERMISSION_VIEW` (read) · staff
- `restoreAuthorisationPolicyVersion` → `PERMISSION_MANAGE` (configure) · staff
- `listAuthorisationPolicyEffectiveness` → `PERMISSION_VIEW` (read) · staff
- `listPermissionFindings` → `PERMISSION_VIEW` (read) · staff
- `listAccessReviewCampaigns` → `PERMISSION_VIEW` (read) · staff
- `createAccessReviewCampaign` → `PERMISSION_MANAGE` (configure) · staff
- `listAccessReviewItems` → `PERMISSION_VIEW` (read) · staff
- `decideAccessReviewItem` → `PERMISSION_GRANT` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PERMISSION_VIEW`, which `listAuthorisationPolicies` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_GRANT` for `decideAccessReviewItem`; `PERMISSION_MANAGE` for `createAuthorisationPolicy`, `updateAuthorisationPolicy` …

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.1 | Allows permissions to be granted dynamically based on attributes and context rather than fixed roles only. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.5 | Dynamic Rule Engine Administrators shall configure access policies without software development. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 7.1.44 | Provide a no-code visual interface for building access policies using conditions, rules, logic operators, approval requirements and reusable components. | F&B POS | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.25 | Policy Testing - System shall support simulation and testing of policies prior to deployment. | Admission and Access | CONTRACTED | `simulateAuthorisationPolicy` |
| 3.3.24 | Policy Versioning - System shall maintain versions of access policies. | Admission and Access | CONTRACTED | `updateAuthorisationPolicy` |
| 3.3.26 | Policy Approval Workflow - System shall support approval workflows for policy changes. | Admission and Access | CONTRACTED | `setAuthorisationPolicyState` |
| 3.3.6 | Emergency Override Authorized users may temporarily bypass restrictions with full audit logging | Admission and Access | CONTRACTED | `createEmergencyAccessOverride` |
| 7.1.40 | Allow supervisors to override access restrictions during emergencies. Require justification, approval workflow (optional), timestamp recording, audit logging and override expiration. | F&B POS | CONTRACTED | `createEmergencyAccessOverride` |
| 3.3.39 | Policy Change History - System shall maintain historical versions of policy changes. | Admission and Access | CONTRACTED | `listAuthorisationPolicyHistory` |
| 7.1.46 | Maintain historical versions of access policies, support comparison between versions and allow rollback to previous approved versions. | F&B POS | CONTRACTED | `restoreAuthorisationPolicyVersion` |
| 7.1.47 | Provide a sandbox environment to test authorization policies before deployment and identify conflicts, missing permissions and excessive permissions. | F&B POS | CONTRACTED | `listPermissionFindings` |
| 7.1.56 | Provide AI recommendations for role assignments, permission optimization, risk reduction, user provisioning and periodic access reviews. | F&B POS | CONTRACTED | `createAccessReviewCampaign` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1066` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1066`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 10: Works in Roles, Permissions & Masking → Enforce least-privilege access to seat administration and operational data. Configure RBAC/PBAC for maps, layouts, inventory, locks, holds, pricing, reports, integrations and audit. Apply …
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (92), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1066?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create access policy, Save as new version, Simulate, Submit / approve / activate / retire, Emergency override, Start access review.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `PERMISSION_GRANT`, `PERMISSION_MANAGE`, `PERMISSION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1067` Seat Approval Workflows

**Configure governance paths for high-impact seat changes. Define workflow by map/layout, capacity, seat kill, hold, accessibility, pricing, integration and override change type. Set stages, approver roles, thresholds, quorum, SLA, escalation, delegation, comments and evidence. Prevent requester self-approval where segregation rules apply and preserve decision history. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 51**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29426 (VM-BO-1067) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/seat-approval-workflows-bo-1067` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Approval paths for high-impact seat changes (map, capacity, kills, holds, pricing).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save visual workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat approval workflows list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat approval workflows untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat approval workflows yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat approval workflows are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
changeType: Seat kill
stages:
- Venue operations
- Ticketing
quorum: 2
sla: 4 h
```

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1067` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1067`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 12: Works in Seat Approval Workflows → Configure governance paths for high-impact seat changes. Define workflow by map/layout, capacity, seat kill, hold, accessibility, pricing, integration and override change type. Set stages, approver …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save visual workflow, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1068` Lifecycle & Environment Promotion

**Move approved configuration safely from draft to production. Provide Draft, Test, Staging and Production contexts with version, owner, status and dependency checks. Promote signed configuration packages through required gates, automated tests and approvals. Support comparison, rollback, failed-promotion recovery and prohibition of direct unapproved production edits. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29120 (VM-BO-1068) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/lifecycle-environment-promotion-bo-1068` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Move configuration from draft to production through test and staging with gates and approvals. Only profile deployment is wired.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Purpose promises draft/test/staging/production contexts; the contract has one deploy operation. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **deployConfigurationProfile**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/spine/tenancy.yaml#deployConfigurationProfile)*

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lifecycle environment promotion list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lifecycle environment promotion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lifecycle environment promotion yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the lifecycle environment promotion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. |

#### Edge cases to draw

- **deployConfigurationProfile answers 409**: Show it as something the person can act on, not a failure: **The named version is not deployable** — it is still a `draft`, or this profile has no such version. Names the version and its status. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
package: Wave Arena seating v12
from: Staging
to: Production
gates:
  tests: passed
  approval: pending
```

#### Permissions

- `deployConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1068` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1068`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 14: Works in Lifecycle & Environment Promotion → Move approved configuration safely from draft to production. Provide Draft, Test, Staging and Production contexts with version, owner, status and dependency checks. Promote signed configuration …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1069` Platform Health & Observability

**Monitor the technical services that protect seat-state correctness. Show API latency/error, event lag, lock service, inventory service, cache, database, queue and webhook health. Configure SLOs, thresholds, alerts, correlation, incident ownership and capacity forecasts by tenant/venue. Drill from a metric to traces, logs and affected performances without exposing restricted tenant data. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/platform-health-observability-bo-1069` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-021): The only read was getWorkstationHealth, a till's health score, labelled "Platform health"; API, cache and database health are TICVAI's and a workstation score is …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Technical health of the services behind seat state (latency, lag, locks). A tenant cannot see platform internals; only workstation health is wired.

**Fixed on main** (the package already carries these; draw what it says): Platform service health on a tenant screen. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform health observability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform health observability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform health observability yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the platform health observability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workstations:
  online: 41
  offline: 2
  pendingSync: 37
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1069` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1069`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 16: Works in Platform Health & Observability → Monitor the technical services that protect seat-state correctness. Show API latency/error, event lag, lock service, inventory service, cache, database, queue and webhook health. Configure SLOs …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1070` Setup, Clone & Inheritance

**Accelerate onboarding while keeping configuration lineage visible. Guide setup of tenant, brand, venue, locale, map, categories, locks/holds, channels, workflows and integrations. Clone an authorized source venue or template and choose which settings, maps and rules to copy or inherit. Show inherited, overridden, missing and conflicting settings and validate completeness before activation. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 52 Board 13 - Seat APIs, Webhooks & Audit Governance Figure 13. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 53**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block C · task VM-BO-1070 |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/setup-clone-inheritance-bo-1070` |

**Known gaps.** **Setup, Clone & Inheritance declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Set up a venue's seating by cloning an authorised configuration, keeping its lineage visible.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only cloneSeatMap, setConfigurationProfile and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Published · Deploying · Deployed · Superseded · Rolled back | `listConfigurationProfiles` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Read a seat map with its structure** (detail panel, from `getSeatMap`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Status | chip: Draft, Validated, Published, Archived | — |
| Seat count | 1,234 | — |
| Section count | 1,234 | — |
| Has geometry | yes / no (icon or chip) | False when only a manifest has been imported. Such a map can be sold from a list but not rendered. |
| Published at | 1 Oct 2026, 14:30 | — |
| Description | text | — |
| View box | grouped details | Coordinate space for rendering. Absent when there is no geometry. |
| Width | 1,234.5 | — |
| Height | 1,234.5 | — |
| Stage position | grouped details | — |
| X | 1,234.5 | — |
| Y | 1,234.5 | — |
| Sections | list or chips (count when long) | — |
| Code | text | — |
| Name | text | — |
| Row count | 1,234 | — |
| Seat count | 1,234 | — |

**Every configuration profile, at its current version** (data table, from `listConfigurationProfiles`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Venue kind scope | list or chips (count when long) | Which workstation types it applies to. A ticketing counter and a kitchen display do not share a profile, and a profile that claims to is a … |
| Settings | grouped details | — |
| Status | chip: Draft, Published, Deploying, Deployed, Superseded, Rolled back | On input only `draft` or `published`; sending `published` publishes this version. |
| Deployed count | 1,234 | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Clone map into venue**: The clone records where it came from. *(source: contracts/satellite/seating.yaml#cloneSeatMap)*

**Data it reads**: `getSeatMap` (onLoad, Read a seat map with its structure); `listConfigurationProfiles` (onLoad, Every configuration profile, at its current version)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The clone inheritance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the clone inheritance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No clone inheritance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the clone inheritance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
clone:
  from: Desert Amphitheatre end stage v4
  to: Pearl Museum courtyard
```

#### Permissions

- `cloneSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `setConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff
- `getSeatMap` → `PRODUCT_VIEW` (read) · staff
- `listConfigurationProfiles` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.3.2 | Event-Specific Layouts | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |
| 21.3.3 | Layout Cloning | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |
| 21.3.7 | Multi-Performance Layouts | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1070` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1070`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 18: Works in Setup, Clone & Inheritance → Accelerate onboarding while keeping configuration lineage visible. Guide setup of tenant, brand, venue, locale, map, categories, locks/holds, channels, workflows and integrations. Clone an authorized …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

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

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/clone","contract":"seating","summary":"Clone a map, optionally into another venue","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"createAccessReviewCampaign": {"method":"POST","path":"/access-review-campaigns","contract":"identity","summary":"Start an access review, one item per grant in scope","permission":"PERMISSION_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityAccessReviewCampaign","responds":"IdentityAccessReviewCampaign"},
"createAuthorisationPolicy": {"method":"POST","path":"/authorisation-policies","contract":"identity","summary":"Write a policy without writing code","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"},
"createEmergencyAccessOverride": {"method":"POST","path":"/access-overrides","contract":"identity","summary":"Bypass the policy, loudly","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EmergencyAccessOverride"},
"decideAccessReviewItem": {"method":"POST","path":"/access-review-items/{itemId}/decision","contract":"identity","summary":"Certify a grant, or revoke it","permission":"PERMISSION_GRANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IdentityAccessReviewItem"},
"deployConfigurationProfile": {"method":"POST","path":"/configuration-profiles/{profileId}/deploy","contract":"tenancy","summary":"Push a version to a fleet, in stages","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProfileDeployment","responds":null},
"getOrgUnit": {"method":"GET","path":"/org-units/{orgUnitId}","contract":"tenancy","summary":"Read a scope node","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrgUnit"},
"getRegionSettings": {"method":"GET","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Read region settings","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"RegionSettings"},
"getSeatMap": {"method":"GET","path":"/seat-maps/{seatMapId}","contract":"seating","summary":"Read a seat map with its structure","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatMap"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"getVenueSettingsDefaults": {"method":"GET","path":"/venue-settings-defaults","contract":"tenancy","summary":"The tenant's default for every venue setting","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listAccessReviewCampaigns": {"method":"GET","path":"/access-review-campaigns","contract":"identity","summary":"Access review campaigns, open first","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessReviewItems": {"method":"GET","path":"/access-review-campaigns/{campaignId}/items","contract":"identity","summary":"The grants a campaign asks somebody to certify or revoke","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToMe","in":"query","required":null},{"name":"findingKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listAuthorisationPolicyEffectiveness": {"method":"GET","path":"/authorisation-policy-effectiveness","contract":"identity","summary":"How each software-permission policy has behaved over a period","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"policyId","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicyHistory": {"method":"GET","path":"/authorisation-policies/{policyId}/history","contract":"identity","summary":"Every version, who changed it and why","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AuthorisationPolicyVersion"},
"listConfigurationProfiles": {"method":"GET","path":"/configuration-profiles","contract":"tenancy","summary":"Every configuration profile, at its current version","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDenominations": {"method":"GET","path":"/denominations","contract":"shift","summary":"The notes and coins a till counts","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"includeInactive","in":"query","required":null}],"requestBody":null,"responds":"Denomination"},
"listPermissionFindings": {"method":"GET","path":"/permission-findings","contract":"identity","summary":"Excessive, missing and conflicting permissions, per principal or role","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"principalId","in":"query","required":null},{"name":"roleId","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"lookbackDays","in":"query","required":null},{"name":"deniedThreshold","in":"query","required":null},{"name":"draftPolicyId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeatMaps": {"method":"GET","path":"/seat-maps","contract":"seating","summary":"List seat maps","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueMaps": {"method":"GET","path":"/venue-maps","contract":"venue-map","summary":"Maps for this venue","permission":"VENUE_MAP_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueMap"},
"restoreAuthorisationPolicyVersion": {"method":"POST","path":"/authorisation-policies/{policyId}/restore","contract":"identity","summary":"Put a previously approved policy version back, as a new version","permission":"PERMISSION_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"setAuthorisationPolicyState": {"method":"POST","path":"/authorisation-policies/{policyId}/state","contract":"identity","summary":"Submit, approve, activate or retire a policy","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"setConfigurationProfile": {"method":"PUT","path":"/configuration-profiles","contract":"tenancy","summary":"What a class of workstation is configured to be","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationProfile","responds":"ConfigurationProfile"},
"setDenominations": {"method":"PUT","path":"/denominations","contract":"shift","summary":"Set the notes and coins a region's tills count","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetDenominationsRequest","responds":"Denomination"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"setVenueSettingsDefaults": {"method":"PUT","path":"/venue-settings-defaults","contract":"tenancy","summary":"Set the tenant's default for every venue setting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"setVisualWorkflow": {"method":"PUT","path":"/visual-workflow","contract":"approvals","summary":"Visual Workflow Designer","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualWorkflowDesignerInput","responds":"VisualWorkflowDesignerView"},
"simulateAuthorisationPolicy": {"method":"POST","path":"/authorisation-policies/simulate","contract":"identity","summary":"What this policy would decide, before it decides anything","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessDecision"},
"updateAuthorisationPolicy": {"method":"PUT","path":"/authorisation-policies/{policyId}","contract":"identity","summary":"Change a policy, as a new version","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"},
"updateRegionSettings": {"method":"PUT","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Update region settings","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegionSettings","responds":"RegionSettings"},
"updateSeats": {"method":"PATCH","path":"/seat-maps/{seatMapId}/seats","contract":"seating","summary":"Bulk-amend seats","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"BulkUpdateSeatsRequest","responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"AccessContext": {"type":"object","description":"**Everything the decision is allowed to depend on.** Stated as one object so a simulation and a live decision see the same shape — a simulator that takes different inputs from the evaluator is testing something else.\n","properties":{"principalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string"},"scopePath":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"attractionId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"attributes":{"type":"object","additionalProperties":true,"description":"**Deliberately an open map**, keyed by attribute (the `AccessCondition.attribute` vocabulary, with `key` for the `*.attribute` forms), each value the one a condition compares against. **Supplied attributes are a fallback, not the source.** The evaluator resolves what it can itself; a caller that could assert its own membership tier could assert any membership tier.\n"}}},
"AccessDecision": {"type":"object","x-ticvai-persistence":"identity.access_decision","description":"3.3.37. **The decision, the policy version behind it, and the attribute values it actually saw.** The third is what separates *the policy is wrong* from *the data was stale*.\n","properties":{"id":{"type":"string","format":"uuid"},"effect":{"type":"string","enum":["permit","deny"]},"decidedAt":{"type":"string","format":"date-time"},"decidedBy":{"type":"string","enum":["central","deviceBundle"],"description":"3.3.29 against 3.3.30 — which evaluator answered."},"principalId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string"},"scopePath":{"type":"string"},"matchedPolicies":{"type":"array","items":{"type":"object","properties":{"policyId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"effect":{"type":"string"},"matched":{"type":"boolean"},"failedCondition":{"type":"string","nullable":true}}}},"observedAttributes":{"type":"object","additionalProperties":true,"description":"**Deliberately an open map**, the same keys as `AccessContext.attributes`: the value of every attribute the evaluator actually read, whichever source it came from.\n"},"overrideId":{"type":"string","format":"uuid","nullable":true},"latencyMs":{"type":"integer","nullable":true},"scopePathIndex":{"type":"string"}}},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","x-ticvai-persistence-column":"jsonb","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"AuthorisationPolicyEffectiveness": {"type":"object","x-ticvai-persistence":"none — computed from identity.access_decision and identity.access_override over the requested period","description":"One `AuthorisationPolicy` over a period (3.3.48; decided 29 September, build pass).","required":["policyId","evaluations"],"properties":{"policyId":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"type":"string","enum":["draft","pendingApproval","active","suspended","retired"]},"versionsInPeriod":{"type":"array","items":{"type":"integer"},"description":"The versions that decided anything in the period."},"evaluations":{"type":"integer","minimum":0,"description":"Decisions that evaluated this policy."},"matched":{"type":"integer","minimum":0,"description":"Evaluations in which every condition held (or one, for `anyMayMatch`)."},"decisivePermits":{"type":"integer","minimum":0,"description":"Permits this policy decided."},"decisiveDenies":{"type":"integer","minimum":0,"description":"Denies this policy decided, deny winning over any permit."},"overridesAtScope":{"type":"integer","minimum":0,"description":"Emergency overrides opened in the period at or beneath the policy's scope for a permission it speaks to - the times people had to go around it."},"lastMatchedAt":{"type":"string","format":"date-time","nullable":true},"neverMatched":{"type":"boolean","description":"True when the policy was evaluated and never matched in the period, the usual sign of a condition written backwards or a policy nobody needs."},"trend":{"type":"array","description":"One point per day in the period.","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"evaluations":{"type":"integer"},"decisiveDenies":{"type":"integer"}}}}}},
"AuthorisationPolicyVersion": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy_version","description":"3.3.36 and 3.3.39. **Who changed what, from what, and why.**","properties":{"policyId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"changedBy":{"type":"string","format":"uuid"},"changedAt":{"type":"string","format":"date-time"},"reason":{"type":"string","nullable":true},"approvedBy":{"type":"string","format":"uuid","nullable":true},"previous":{"$ref":"#/components/schemas/AuthorisationPolicy"},"current":{"$ref":"#/components/schemas/AuthorisationPolicy"},"scopePath":{"type":"string"}}},
"BulkUpdateSeatsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["selection"],"properties":{"selection":{"type":"object","description":"Seats to amend. Combine filters; an empty selection is rejected.","properties":{"seatIds":{"type":"array","items":{"type":"string"}},"sectionCodes":{"type":"array","items":{"type":"string"}},"rowLabels":{"type":"array","items":{"type":"string"}}}},"categoryId":{"type":"string","format":"uuid"},"attribute":{"$ref":"#/components/schemas/SeatAttribute"},"isActive":{"type":"boolean"}}},
"ConfigurationProfile": {"type":"object","x-ticvai-persistence":"platform.configuration_profile","description":"Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n","required":["id","name","venueKindScope","version","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"scopePath":{"type":"string"},"venueKindScope":{"type":"array","description":"Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n","items":{"type":"string"}},"version":{"type":"integer","readOnly":true,"description":"**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was. Assigned by the server: 1 on create, and one more each time a change lands on a published version (see `setConfigurationProfile`).\n"},"settings":{"type":"object","additionalProperties":true},"status":{"type":"string","enum":["draft","published","deploying","deployed","superseded","rolledBack"],"description":"On input only `draft` or `published`; sending `published` publishes this version. The other four are set by deployment and refused on input.\n"},"deployedCount":{"type":"integer","readOnly":true},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"Denomination": {"x-ticvai-persistence":"platform.denomination","description":"**Raised in review by Tanmay: denominations belong in a table, not in JSON.** He is right, and the reason is stronger than storage tidiness — **`orders.cash_movement.denominations` was a jsonb blob, so a note that stops circulating has nothing to deactivate.**\n**The seed is `docs/active/seed-data-proposal.md` section 1** (audit R229, proposed, client to correct): notes 5, 10, 20, 50, 100, 200, 500 and 1000 AED; coins 25 fils, 50 fils and 1 AED. The zero-valued coin in the list first supplied (`Coin, 0, COIN`) is a transcription slip rather than a denomination, is not seeded, and is the kind of row a table refuses and a JSON blob accepts silently.\n**Ordered for counting, not by value.** A cashier counts notes highest first and coins in the order they sit in the drawer, and `sortOrder` is what makes the count screen match the physical tray.\"\n","type":"object","required":["currencyCode","kind","value"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string"},"displayName":{"type":"string","description":"What the cashier reads — *AED 500*, *Coin*. Localised, because a count screen is read at speed."},"kind":{"type":"string","enum":["note","coin"]},"sortOrder":{"type":"integer","description":"**Counting order, not value order.** Notes highest first, coins as they sit in the tray.\n"},"isActive":{"type":"boolean","default":true,"description":"**The field that makes this a table.** A note withdrawn from circulation is deactivated and stays in the count history — **a JSON blob cannot deactivate anything**, and deleting the value would rewrite every past cash-up that used it.\n"},"value":{"x-ticvai-column":"face_value_amount","$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"EmergencyAccessOverride": {"type":"object","x-ticvai-persistence":"identity.access_override","description":"3.3.6. **Time-boxed at creation, alerted as well as logged.**","properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"permissions":{"type":"array","items":{"type":"string"}},"reason":{"type":"string"},"createdBy":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"revokedAt":{"type":"string","format":"date-time","nullable":true},"alertedTo":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"IdentityAccessReviewCampaign": {"type":"object","x-ticvai-persistence":"identity.access_review_campaign","description":"**A periodic access review** (7.1.35, 7.1.56; decided 29 September, build pass, group G2): which grants, reviewed by whom, by when. Its items are `identity.access_review_item`. Lifecycle in `states/access-review-campaign.yaml`.","required":["name","scopePath","reviewerMode","dueAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), and what is reviewed: every grant at or below it. Inside the caller's own scope. Operations write it at `venue` scope."},"roleIds":{"type":"array","nullable":true,"description":"Only grants of these roles; null reviews every grant in scope.","items":{"type":"string","format":"uuid"}},"reviewerMode":{"type":"string","enum":["lineManager","named"],"description":"`lineManager`: each item goes to the holder's manager from their primary work assignment, falling back to the named reviewers where none is found. `named`: the named reviewers share the items."},"reviewerPrincipalIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"}},"dueAt":{"type":"string","format":"date-time"},"recurrence":{"type":"string","enum":["none","quarterly","semiAnnual","annual"],"default":"none"},"prefillFromFindings":{"type":"boolean","default":true},"lookbackDays":{"type":"integer","minimum":7,"maximum":365,"default":90},"status":{"type":"string","enum":["open","completed","expired"],"readOnly":true},"itemCount":{"type":"integer","readOnly":true},"decidedCount":{"type":"integer","readOnly":true,"description":"Kept by `decideAccessReviewItem` in the same write, so the campaign list needs no count query."},"revokedCount":{"type":"integer","readOnly":true},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"IdentityAccessReviewItem": {"type":"object","x-ticvai-persistence":"identity.access_review_item","description":"One grant under review in a campaign, with the finding that pre-filled it and the reviewer's decision (decided 29 September, build pass, group G2). Lifecycle in `states/access-review-item.yaml`.","required":["campaignId","delegatedAccessId","principalId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","x-ticvai-references":"identity.access_review_campaign"},"delegatedAccessId":{"type":"string","format":"uuid","x-ticvai-references":"identity.delegated_access","description":"The grant under review."},"principalId":{"type":"string","format":"uuid","x-ticvai-references":"identity.principal"},"roleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.role"},"scopePath":{"type":"string","description":"The grant's scope. **The partition key** (ADR-0005)."},"reviewerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"findingKind":{"type":"string","enum":["none","excessive","conflicting"],"default":"none"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true},"recommendation":{"type":"string","enum":["certify","revoke","review"]},"status":{"type":"string","enum":["pending","certified","revoked","notReviewed"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","maxLength":1000,"nullable":true}}},
"IdentityPermissionFinding": {"type":"object","x-ticvai-persistence":"none — computed from grants (roles, delegations, policies) against identity.access_decision and identity.segregation_rule","description":"One excessive, missing or conflicting permission (7.1.47; decided 29 September, build pass).","required":["kind","principalId","permission"],"properties":{"kind":{"type":"string","enum":["excessive","missing","conflicting"]},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid","nullable":true,"description":"The role that grants it, for excessive and conflicting; the role whose peers hold it, for missing."},"permission":{"type":"string"},"conflictingPermission":{"type":"string","nullable":true,"description":"The other half of the pair, for conflicting."},"segregationRuleId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"grantedBy":{"type":"string","enum":["role","delegation","policy"],"nullable":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"description":"The last permit that used it; null when never used in the window."},"deniedCount":{"type":"integer","nullable":true,"description":"For missing, the denials in the window."},"peersHoldingPercent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"For missing, the share of the role's holders at the same scope who hold the permission."},"recommendation":{"type":"string","enum":["revoke","grant","review"]},"asDraft":{"type":"boolean","default":false,"description":"True when the finding exists only because of the `draftPolicyId` evaluated."}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Placement": {"x-ticvai-persistence":"none — embedded in region_settings","type":"object","description":"Read-only here. Set by the Control Plane at provisioning.\nEvery region is its own logical cell. Placement determines the infrastructure backing it, which is how cost is controlled without varying the split rule: `shared` puts several regions' databases on one cluster; `dedicated` and `isolated` give a region its own. Regions in different countries MUST have placements in their respective jurisdictions.\n","readOnly":true,"required":["mode"],"properties":{"mode":{"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},"cellName":{"type":"string"},"cloudRegion":{"type":"string"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"ProfileDeployment": {"type":"object","x-ticvai-persistence":"platform.profile_deployment","description":"**A deployment is an event with a date, a target and an outcome** — the client's board shows recent deployments with all three and the package had no record of any.\n**Staged rather than all-at-once by default.** Pushing a profile to 1,248 workstations simultaneously is how a venue discovers a bad profile at every till at the same moment.\n","required":["id","profileId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileId":{"type":"string","format":"uuid","readOnly":true,"description":"Taken from the path of `deployConfigurationProfile`."},"version":{"type":"integer","description":"The published version to deploy."},"targetWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"}},"targetFilter":{"type":"object","nullable":true,"description":"By department, type or venue, where the target is a set rather than a list.\n","properties":{"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"workstationTypes":{"type":"array","description":"The same workstation-type values `ConfigurationProfile.venueKindScope` holds.","items":{"type":"string"}}}},"strategy":{"type":"string","enum":["immediate","staged","onNextIdle"],"default":"onNextIdle"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"],"readOnly":true},"succeededCount":{"type":"integer","readOnly":true},"failedCount":{"type":"integer","readOnly":true},"failureReasons":{"type":"object","readOnly":true,"additionalProperties":{"type":"integer"},"description":"**Grouped, because 40 workstations failing for one reason is one problem** and a list of 40 rows is forty.\n"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"RegionSettings": {"x-ticvai-persistence":"platform.region_settings","type":"object","required":["countryCode","currencyCode","currencyScale","timeZone","fiscalYearStartMonth"],"properties":{"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","description":"ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell."},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"description":"Decimal places for this region's currency. Varies by currency — some use 2, some use 3. Money columns are numeric(18,4) and carry the scale explicitly, because a fixed 2-place type silently truncates 3-place currencies.\n"},"timeZone":{"type":"string","description":"IANA zone, e.g. `Asia/Dubai`."},"dateFormat":{"type":"string","default":"dd/MM/yyyy"},"numberFormat":{"type":"string","default":"#,##0.00"},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12,"description":"Varies by country."},"allowedAiResidencies":{"type":"array","description":"**The region's compliance gate on AI providers** (decided 28 September, audit R203; ADR-0009). The `AiProvider.residency` values a tenant in this region may use; empty means no restriction. `ai.setAiProvider` refuses any other residency with `409 residency-refused`. A prompt carrying guest data that reaches a provider hosted elsewhere is a cross-border transfer, and this is where a region says which it allows.\n**Derived from `aiResidencyClass` since 2 October 2026** (CHG-CSP-009): the class names the residencies, and this list narrows them further where a region needs it; it never widens them.\n","default":[],"items":{"type":"string"}},"aiResidencyClass":{"type":"string","enum":["uaeOnly","globalAllowed","onPrem"],"default":"uaeOnly","description":"**The tenant's AI residency class** (decided 2 October 2026, Chinmay, \"AI residency: per-tenant residency class\"; DEC-539; CHG-CSP-009; amends AI-D02 and ADR-0009 section 1). Which AI endpoints the AI engine may route this tenant's calls to:\n- `uaeOnly` (the default, and mandatory for government, bank and health tenants): the small tier\n  is Core42 Compass GPT-4.1 mini (or Seraj if it wins the Arabic golden set), the strong tier\n  Compass GPT-5, reached through `AiProviderKind` `openaiCompatible`; fallback OpenAI UAE (no\n  in-cell model: we host none unless a client asks, CHG-R1S-002). No call leaves the UAE.\n- `globalAllowed`: a private venue that opts in under PDPL Article 23, with a vendor contract, a\n  DPIA and a notice to guests (`aiResidencyOptIn`). Azure gpt-5-mini and gpt-6-sol Global, or\n  the tenant's BYOK provider; fallback the `uaeOnly` chain. The tenant is listed in ADR-0009's\n  transfer register.\n- `onPrem`: models in the tenant's own estate (Qwen3.5 or gpt-oss; strong tier Qwen3.5-122B,\n  Falcon-H1 Arabic or Jais 2), only where the client asks for it (CHG-R1S-002).\n\n**Every LLM call is scrubbed of personal data in-cell first, whatever the class** (DEC-542): the class decides where a call may go, never whether personal data may travel. Moving from `uaeOnly` to `globalAllowed` without `aiResidencyOptIn` is refused `422 residency-opt-in-required`; on a tenant `aiResidencyClassLocked` holds, any change is refused `409 residency-class-locked`. The model choice per class is the AI engine's (ai `AiProvider`, ai-system-design 3.3), not a setting here.\n"},"aiResidencyClassLocked":{"type":"boolean","readOnly":true,"default":false,"description":"**Set by TICVAI at onboarding for a government, bank or health tenant** (DEC-539), which must stay `uaeOnly`. Read-only to the tenant.\n"},"tenantCategory":{"type":"string","readOnly":true,"default":"private","enum":["private","semiGovernment","government","banking","payments","health","difc","adgm"],"description":"**What kind of organisation the tenant is, for AI residency** (3 October 2026, CHG-R1S-016; the legal research `docs/active/research/openai-key-uae-3-october.md`, item 2, and Chinmay's per-tenant residency class, DEC-539). Recorded by TICVAI staff at onboarding, read-only to the tenant. **Only `private` may take `globalAllowed`**: a government or semi-government entity (DESC, ADISS and TDRA scope), a bank or payments firm, a health provider, or a DIFC or ADGM entity stays `uaeOnly` (or `onPrem` where it asks), and `updateRegionSettings` refuses the change `409 residency-category-refused`, naming the category. `aiResidencyClassLocked` stays as the per-tenant override TICVAI can set on any category.\n"},"aiResidencyOptIn":{"type":"object","nullable":true,"description":"**The evidence a `globalAllowed` opt-in needs under PDPL Article 23** (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract, its DPIA and the notice guests see. The platform records that they were named, by whom and when; it does not hold or judge the documents. Null while the class is `uaeOnly` or `onPrem`.\n","properties":{"vendorContractReference":{"type":"string","maxLength":200},"dpiaReference":{"type":"string","maxLength":200},"guestNoticeReference":{"type":"string","maxLength":200},"confirmedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"confirmedAt":{"type":"string","format":"date-time","readOnly":true}}},"localLanguageNameLocales":{"type":"array","default":[],"description":"**The languages an outlet name must also be given in, in this country** (decided 2 October 2026, Chinmay, batch 2 #26: \"English plus the local language where the country needs it\"; DEC-031; CHG-CSP-005). ISO 639-1 codes; `[ar]` in the UAE. Empty asks for English only. `createOutlet` and `updateOutlet` refuse an outlet whose `nameTranslations` lacks one of them (`422 local-name-required`).\n","items":{"type":"string","pattern":"^[a-z]{2}$"}},"requiredBillingDocuments":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**Which documents a TICVAI customer's billing entity must upload, in this country** (decided 2 October 2026, Chinmay, batch 6 set 7, ADM-411: \"Trade licence always; VAT certificate when a TRN is entered; configurable per country\"; DEC-210; CHG-CSP-008). The default for every country is the two rows below; TICVAI staff change them per country. The subscription contract's billing entity and `PartnerDocument` read this list; a missing required document holds the entity in verification.\n","default":[{"documentType":"tradeLicence","requiredWhen":"always"},{"documentType":"vatCertificate","requiredWhen":"trnEntered"}],"items":{"type":"object","properties":{"documentType":{"type":"string","maxLength":64,"description":"The document kind, as the subscription contract's `PartnerDocument` names it (`tradeLicence`, `vatCertificate`, ...)."},"requiredWhen":{"type":"string","enum":["always","trnEntered"]}}}},"minorAgeThreshold":{"type":"integer","minimum":0,"maximum":21,"default":18,"description":"**The age below which a guest is a minor here, set per country** (decided 2 October 2026, Chinmay, critical set 1, BO-187: \"Guardian consent on the venue's form; minor age per country\"; DEC-237; CHG-CSP-019). A minor's biometric enrolment needs a guardian's consent on the venue's consent form (access `enrolFacePass`, `consent.guardianSubjectId`); a subject with no date of birth is treated as a minor (audit R126). The default 18 is the UAE's age of majority and is marked for counsel to confirm per country (R205); whether minors may enrol at all is the venue's switch (`VenueSettings.biometrics.allowMinors`).\n"},"placement":{"$ref":"#/components/schemas/Placement"},"cellName":{"type":"string","readOnly":true,"description":"The cell serving this region. One cell per tenant per region (ADR-0014).\n"}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SeatAttribute": {"type":"string","description":"BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n","enum":["standard","accessible","companion","obstructedView","restrictedLegroom","premium","houseSeat","buffer","aisle","endOfRow","extraLegroom","powerOutlet","tableService","shaded","covered","nearExit","nearAccessibleWc","wheelchairTransfer","limitedRecline","sofa","beanbag"]},
"SeatMap": {"x-ticvai-persistence":"seating.seat_map","allOf":[{"$ref":"#/components/schemas/SeatMapSummary"},{"type":"object","required":["sections"],"properties":{"description":{"type":"string","nullable":true},"viewBox":{"type":"object","description":"Coordinate space for rendering. Absent when there is no geometry.","nullable":true,"properties":{"width":{"type":"number"},"height":{"type":"number"}}},"stagePosition":{"$ref":"#/components/schemas/Point"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/Section"}},"isActive":{"type":"boolean"}}}]},
"SeatMapStatus": {"type":"string","enum":["draft","validated","published","archived"]},
"SeatMapSummary": {"x-ticvai-persistence":"seating.seat_map","type":"object","required":["id","name","venueId","status","seatCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/SeatMapStatus"},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean","description":"False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"},"publishedAt":{"type":"string","format":"date-time","nullable":true}}},
"Section": {"x-ticvai-persistence":"seating.section","type":"object","required":["code","name","rowCount","seatCount"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"rowCount":{"type":"integer"},"seatCount":{"type":"integer"},"boundary":{"type":"array","items":{"$ref":"#/components/schemas/Point"},"description":"Polygon for rendering. Absent without geometry."},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"assets.MediaAsset","description":"**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"},"rows":{"type":"array","items":{"type":"object","required":["label","seatCount"],"properties":{"label":{"type":"string"},"seatCount":{"type":"integer"},"numberingDirection":{"type":"string","enum":["leftToRight","rightToLeft"],"description":"Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SetDenominationsRequest": {"type":"object","description":"Request only. One currency's complete list; anything not in it is deactivated. Entries match existing rows on `kind` and `value` (see `setDenominations`).\n","required":["scopePath","currencyCode","denominations"],"properties":{"scopePath":{"type":"string","description":"The region the write is made at — the materialised path of a `region` scope node. The caller's `REGION_CONFIGURE` grant must cover it.\n"},"currencyCode":{"type":"string","minLength":3,"maxLength":3},"denominations":{"type":"array","minItems":1,"items":{"type":"object","required":["displayName","kind","value","sortOrder"],"properties":{"displayName":{"type":"string","maxLength":60},"kind":{"type":"string","enum":["note","coin"]},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer","minimum":0},"isActive":{"type":"boolean","default":true}}}}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"},"modelAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.MediaAsset","description":"**The 3D layer of the working draft** (ADR-0069, contract item closed 3 October 2026): the GLB (`model3d` asset) the last `glbModel` import brought in. Set by `importVenueGeometry`, never by sending a value. Null for a 2D-only map, which is the default and needs nothing. The 3D model is a rendering of the map, never the source of its truth: routes come from the graph.\n"},"navigationFileAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.MediaAsset","description":"The navigation file imported with the model, kept so the import can be re-run and audited."},"modelTransform":{"readOnly":true,"description":"**How the model's local frame sits on the earth** (ADR-0069 section 3): the navigation file's anchor, stored once and used both ways. Null without a model. It maps onto the plan's georeference as the ADR says, so a map with a model is georeferenced.\n","allOf":[{"$ref":"#/components/schemas/VenueModelTransform"}]},"model3dStatus":{"type":"string","readOnly":true,"enum":["none","publishable","blocked"],"description":"**Whether the next publish carries the 3D layer.** `none`: no model. `publishable`: the last model import had no `error` finding. `blocked`: it had one (over 300,000 triangles at LOD0, uncompressed textures, a control point more than 10 m out, an invalid navigation file), named in that job's `model.findings`; the 2D map still publishes and guests see 2D until a corrected model is imported (ADR-0069 sections 3 and 6).\n"}}},
"VenueModelTransform": {"type":"object","x-ticvai-persistence":"none — jsonb column","description":"ADR-0069 section 3: the navigation file's `anchor`. Local to WGS84: rotate (x, z) by `headingDegrees` into east/north metres, scale, offset from the origin on a local tangent plane; GPS to local is the inverse, done on the phone for every fix.\n","required":["originLat","originLng","headingDegrees"],"properties":{"originLat":{"type":"number","minimum":-90,"maximum":90},"originLng":{"type":"number","minimum":-180,"maximum":180},"originAltitudeMetres":{"type":"number","default":0},"headingDegrees":{"type":"number","minimum":0,"exclusiveMaximum":360,"description":"True-north bearing of the model's -Z axis, clockwise."},"scale":{"type":"number","default":1,"description":"Metres per model unit; 1 for a model in metres."},"controlPoints":{"type":"array","minItems":2,"maxItems":8,"description":"Surveyed checks, far apart. They verify the anchor; they do not define it.","items":{"type":"object","required":["label","x","z","lat","lng"],"properties":{"label":{"type":"string"},"x":{"type":"number"},"z":{"type":"number"},"lat":{"type":"number"},"lng":{"type":"number"},"residualMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Measured at import. Over 3 m is a warning; over 10 m blocks the 3D layer."}}}}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"VisualWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"VisualWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]}
}
```
