# P08-sell-03 — P08 · Sell (3 of 4)

**10 screens · 26 operations · 42 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AI_USE, MARKETING_MANAGE, MARKETING_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_CONFIGURE, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
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

### Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers)

Customer & marketing is how a venue knows its guests and talks to them. There is ONE guest profile per person across ticketing, F&B and retail, so a guest who books online and later dines is the same profile (DI-339). A profile needs at least an email or a mobile, never neither (DI-372). Profiles are created by registration, by guest checkout, or by staff at a till or desk. Repeat guest checkouts with the same verified email or phone attach to the same profile automatically (DI-941, R120 default). Two records that might be the same person are NEVER merged automatically: the guest is asked to confirm, and an admin review queue runs alongside (DI-377). Each candidate shows why it matched; the record that loses is superseded, not deleted; consent takes the narrower of the two positions (DI-808). Around the profile sit three things that must never be confused. CONSENT is what the law allows: per purpose and per channel, append-only, with the notice version and the source (recordConsent). It is Given, Withdrawn or Not asked. A SUBSCRIPTION is what the guest asked to receive, e.g. a newsletter list (MarketingSubscription). A PREFERENCE is what they like: table, dietary, accessibility (updateGuestPreferences). An anonymous visitor's cookie decision is recorded against a device key (recordDeviceConsent) and attaches to the guest when they sign in (claimDeviceConsent). Marketing consent at GUEST CHECKOUT is an open client question, and the design follows its default: an unticked opt-in beside the terms, one per channel and purpose. It is recorded with source "checkout" against the order and the verified contact, and nothing is sent without it. Whether that is sufficient consent under PDPL is the client DPO's call (M18-15 (audit R-M18-15), DI-954, DI-940). Marketing reads profiles through SEGMENTS (rules, evaluated when used) and static LISTS (imported). It reaches guests by CAMPAIGNS (one send to an audience) and JOURNEYS (automations started by an event, with waits and branches). Journeys may offer only pre-configured offers, never a free-typed discount (MoM 2026-08-20 4.6). Everything goes through ONE communications module that every other module uses (MoM 2026-08-31 4.6). Consent and suppression are applied at send time, and the number excluded, with the reasons, is reported before anything goes out (launchCampaign). Transactional messages (tickets, receipts, queue calls, case replies) do not need marketing consent and must never carry marketing. LOYALTY pays for spend: points, tiers, rewards and expiry. GAMIFICATION pays for behaviour: challenges, badges, streaks, referrals and leaderboards (createChallenge). A guest reads their own loyalty position (getLoyaltyPosition). A till, the back office or support reads a named guest's (getGuestLoyalty, or identifyGuest at a till). SERVICE: one Case object covers lost property, complaints, questions, accessibility and refund requests (CaseKind). A guest raises one with raiseMyCase, which needs the connection …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Guest | The person the venue serves, signed in or not. In body copy on every surface. | Customer, User, Subject, Contact, Patron | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestProfile |
| Guest profile | The CRM record of one person (details, consent, preferences, history). Distinct from the Account, which is how a guest signs in. | Customer record, Contact, Subject | contracts/satellite/marketing-crm.yaml#getGuestProfile |
| Consent - Given / Withdrawn / Not asked | What the law allows, per purpose (marketing, personalisation, profiling, third-party sharing, AI processing, transactional) and per channel. "Not asked" is not "Withdrawn" and must look different. | Opted in/out as a status, Accepted, Declined, Revoked, Unsubscribed (that is a subscription) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentDecision |
| Subscription | A list the guest asked to receive (a newsletter, event news), per channel. Unsubscribing from a list is not withdrawing consent. | Consent, Opt-in | contracts/satellite/marketing-crm.yaml#/components/schemas/MarketingSubscription |
| Preferences | What the guest likes or needs (seating, drinks, dietary, accessibility, contact channel). Never grants permission. | Consents, Settings | contracts/satellite/marketing-crm.yaml#updateGuestPreferences |
| Send me offers and news | The marketing opt-in label beside the terms at checkout, unticked, one per channel and purpose. | I agree to marketing, Pre-ticked boxes, Keep me updated ticked by default | DI-954 |
| Points / Tier / Points to next tier / Expiring points | The loyalty position. Points are a liability earned per programme; tiers are ranked (Bronze, Silver, Gold, Platinum in the meetings). | Credits, Coins, Balance alone (wallet money is "credit"), Level | DI-382 |
| Pending points | Points earned on a purchase still inside its refund window; shown apart from spendable points. | Available points for pending ones | contracts/satellite/marketing-crm.yaml#getLoyaltyPosition |
| Reward | What points can be turned into (rewards catalogue). | Prize (games redemption uses prize), Voucher unless it is one | contracts/satellite/marketing-crm.yaml#listRewards |
| Challenge / Badge / Streak / Referral | Gamification - rewards for behaviour, not spend. Status badges such as Explorer, Adventurer, Legend. | Mission and Quest used interchangeably on one screen, Loyalty tier for a badge | DI-392 |
| Case | One service record - lost property, complaint, question, accessibility, refund request or other - with a number (venue prefix plus sequence), a status and an SLA. | Ticket (a ticket is an admission product), Issue, Incident (that is maintenance and safety) | contracts/satellite/marketing-crm.yaml#/components/schemas/CaseKind |
| Reply to guest / Internal note | The two kinds of case message. The agent always chooses one explicitly; there is no default. | Comment, Message (ambiguous) | F05 step 2 |
| Conversation | A live chat session (web chat, in-app, WhatsApp, SMS, email, kiosk, voice). With the assistant, then queued, then with an agent. It is not a case. | Ticket, Case (until one is raised from it) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConversationState |
| Segment / List / Audience | A segment is rules evaluated when used. A list is static, imported or hand-picked. The audience is what a campaign or journey targets. | Group, Cohort, Target list for a segment | DI-381 |
| Campaign / Journey | A campaign is one send (one-off, scheduled, triggered or recurring) to an audience. A journey is an automation started by an event, with steps, waits and branches. | Flow (booking flows use it), Automation for a one-off send, Blast | R146 |
| Offer | A pre-configured, system-validated discount or benefit that a campaign or journey references. It is never typed into the builder. | Discount field, Coupon (unless the offer is a coupon code) | MoM 2026-08-20 4.6 |
| Reachable | How many guests in an audience can actually be sent to on a channel after consent and suppression. Always shown beside the matching count. | Audience size alone | contracts/satellite/marketing-crm.yaml#previewSegment |
| Possible duplicate / Merge | Two profiles that may be one person. Never called "Duplicate" as a verdict. Merging needs confirmation and stays reversible for 30 days. | Duplicate (as a status), Combine, Auto-merge | DI-808 |
| Data request | A guest's privacy request - a copy of my data, a correction, erasure, a restriction - with a legal clock. Statuses submitted, in progress, completed. | DSAR on guest screens, Subject data, Ticket | DI-379 |
| Waiver / Consent question | A waiver is a signed, versioned form. A consent question ("Are you able to swim?", "I accept the risk") is a single question asked per person or per booking and recorded as consent. | Contract, Disclaimer, Form for a waiver in guest copy | DI-1062 |
| Lost item / Found item / Possible match | The two directions of lost property and the suggested pairing between them. | Lost case, Claim before it is claimed | contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem |
| Wishlist | Products and dates a guest saved to buy later, including F&B and retail to buy on site. | Favourites (used for transport routes), Saved for later on one surface and Wishlist on another | DI-202 |
| Notification / Message | A notification is an item in the guest's in-app feed. A message is one send on a channel (email, SMS, WhatsApp, push, in-app). | Alert for marketing content, Inbox for the guest feed | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestNotification |
| Template | A reusable message body per channel and language with merge fields. Transactional and marketing templates are separate kinds. | Layout, Design | contracts/satellite/marketing-crm.yaml#createMessageTemplate |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-113` | Central Kitchen & Commissary Management | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (generated) |
| `BO-114` | Variants, Attributes, Barcode & RFID Management | B–D | 3 | 8 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-115` | Category, Brand & Merchandise Hierarchy | B–D | 14 | 15 | 6 | 0 | 2 | 6 | — | notStarted (generated) |
| `BO-116` | Merchandising & Product Presentation | B | 30 | 62 | 6 | 4 | 1 | 0 | — | notStarted (generated) |
| `BO-117` | Product Import, Governance & AI Configuration Assistant | A | 7 | 0 | 6 | 32 | 5 | 0 | — | notStarted (generated) |
| `BO-118` | Campaign & Audience Management | B–D | 47 | 45 | 6 | 14 | 0 | 6 | — | notStarted (generated) |
| `BO-119` | Cross-Sell, Upsell & Recommendation Rules | B–D | 1 | 24 | 5 | 54 | 4 | 0 | — | notStarted (generated) |
| `BO-120` | Omnichannel Commerce & Journey Configuration | B–D | 28 | 14 | 6 | 9 | 1 | 6 | — | notStarted (generated) |
| `BO-121` | Personalized Offers & Guest Engagement | B–D | 42 | 14 | 6 | 8 | 1 | 0 | — | notStarted (generated) |
| `BO-1190` | Donation Campaigns | B–D | 27 | 16 | 7 | 5 | 2 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-113, BO-117 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-113` Central Kitchen & Commissary Management

**Central Kitchen & Commissary Management — from the client design board, 20 August (merged into BO-112 Production Planning & Production Sheets).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`planProductionRun`, `completeProductionRun`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `runId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/central-kitchen-commissary-management` |

**What the spec says about it.** **Merged into BO-112** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). Commissary production is a tab of the one Production screen (design-note correction fnb-retail BO-112). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-112, and nothing on it is built separately. **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Food, Beverage & Retail process.** One central kitchen producing for many outlets: outlet demand rolled up per item, batches sized and costed once, and each outlet's share sent as a transfer (FNB-2N). A run is a stock movement in both directions - ingredients out when it starts, the made item in when it completes. The one thing to get right is the allocation of each batch to the outlets it is for, and the planned-against-made gap.

**Known correction pending (do not draw the wrong version)**

- **Board frame mapped to Retail Board 2 ret-2d ("Category, Brand & Merchandise Hierarchy"); the client's frame is FnB Board 2 fnb-2n ("Central Kitchen & Commissary"), currently listed on BO-136.** Why: Wrong board; the designer would draw a merchandise tree. *(source: screens/P08-venue-back-office.yaml#BO-113; Food, Beverage & Retail)*
- **There is no operation to start or cancel a run - the state model gives planned to inProgress to planProductionRun and inProgress to cancelled to completeProductionRun.** Why: The screen cannot draw "Start batch" (the moment ingredients leave stock, R125 (8)) or "Cancel batch" with an honest call. *(source: R125; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): No read declared (listProductionRuns with location kind commissary), pattern configEditor, and a form of raw ProductionRun fields (id … (CHG-WIR-008); Each outlet's share "becomes a transfer" (FNB-2N), but no transfer operation (createStockTransfer) is wired. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the commissary a kind of outlet (DI-330 outlet-level model) or a kitchen shared by outlets as FNB-1H draws ("Main Kitchen linked to 3 outlets")?** → Drawn default stands (answer: "The commissary is an outlet that produces for others"): Treat the commissary as an outlet that produces for others (producing outlet plus for-outlets). *(decided by Chinmay, 2026-10-02; DEC-186 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Commissary and day**: The producing kitchen (Central Commissary) and the day; runs listed are those made at a commissary. *(source: contracts/satellite/fnb.yaml#listProductionRuns)*
- **Batch**: Recipe by name, planned quantity with unit, the outlets it is for (multi-select by name), scheduled start. *(source: contracts/satellite/fnb.yaml#planProductionRun)*
- **Complete batch**: Made quantity in the item's unit; a variance reason is asked for when made differs from planned (optional in the contract). The time is the device's own and is not asked for. *(source: contracts/satellite/fnb.yaml#completeProductionRun / designer default)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Consolidated demand**: Per item - outlets asking, total demand, batch size, number of batches, unit cost (FNB-2N). *(source: screens/P08-venue-back-office.yaml#BO-113)*
- **Yield**: Made over planned, as a percentage with one decimal, derived on read and never stored. *(source: contracts/satellite/fnb.yaml#getProductionRun)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Complete batch**: Moves the made quantity into stock; refused (409) if the batch is not running, with its current state named. Works offline and replays in order. *(source: contracts/satellite/fnb.yaml#completeProductionRun)*

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-112 while it opens. |
| Error (`?state=error`) | Could not open BO-112; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-112, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-112. |
| Permission denied (`?state=emptyNoAccess`) | As BO-112: shown when the caller lacks the access BO-112 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A batch abandoned halfway**: Its ingredients are already gone; it reads Cancelled with the variance kept, not as if it never happened. *(source: contracts/satellite/fnb.yaml#planProductionRun)*
- **An outlet's requisition arrives after the batch is planned**: Show it as unmet demand for the day rather than silently enlarging a running batch. *(source: designer default)*

#### Consistency with other screens

- Match `BO-112`: Same run card and units.
- Match `BO-138`: Batch execution and yield are the same view filtered to the commissary.
- Match `BO-078`: Outlet requisitions feed commissary demand (DI-341).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
commissary: Central Commissary - Mon 2 Nov 2026 - 14 outlets
demand:
- item: Burger Sauce (SUB-0071)
  outlets: 9
  demand: 42.0 kg
  batch: 12.0 kg
  batches: 4
  unitCost: AED 26.10
- item: Beef Patty 150g (ITM-1042)
  outlets: 6
  demand: 840 pc
  batch: 400 pc
  batches: 2
  unitCost: AED 6.10
allocation:
  item: Burger Sauce 12.0 kg
  to:
  - Bite & Go 4.0 kg
  - Oasis Bistro 6.0 kg
  - Beach Hut kiosk 2.0 kg
```

#### Permissions

**A refused user sees:** As BO-112: shown when the caller lacks the access BO-112 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'kitchen')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-113` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-113?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-102`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-114` Variants, Attributes, Barcode & RFID Management

**Variants, Attributes, Barcode & RFID Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSerialisedItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/variants-attributes-barcode-rfid-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.

**From the Food, Beverage & Retail process.** By its title this screen manages variants, attributes, barcodes and RFID for retail products. By its operations it is only a serialised-stock list with a barcode price check. The designer should draw the serialised-stock and barcode lookup it can actually do, and treat variants and attributes as living on Product Detail & Variants (BO-008). The one thing to get right is to trace an individual item by serial: where it is, its status and, if sold, on which sale.

**Known correction pending (do not draw the wrong version)**

- **The title promises variants, attributes, barcode and RFID management. The operations are only the serialised-item list and the barcode price check.** Why: Variant attributes (configurable per product type) and a distinct barcode per variant are agreed, but their operations (setProductAttributes, listProductVariants, updateProductVariant) are on BO-008. RFID has no operation (open item). Either bind the variant operations here or retitle this screen "Serialised Stock & Barcode Lookup" and merge it with EMP-069's back-office twin. *(source: DI-354 / DI-365 / DI-474 / DI-987 / contracts/spine/catalogue.yaml#setProductAttributes; Food, Beverage & Retail)*
- **Attributes are set per product (setProductAttributes). The decision says attributes are configured per product type and appear dynamically when a product is added.** Why: No per-product-type attribute template exists to drive "appear dynamically". *(source: DI-354 / contracts/spine/catalogue.yaml#setProductAttributes; Food, Beverage & Retail)*
- **The serial and status filters are text fields. The table is "Every serialised" with raw id columns.** Why: Plumbing. Use scan/search and status chips. *(source: screens/P08-venue-back-office.yaml#BO-114; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should BO-114 carry variant and attribute management, or is BO-008 the only place?** → Drawn default accepted: Draw serialised lookup and price check here, and link to BO-008 for variants. *(decided by Chinmay, 2026-10-02; DEC-296 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Serial | text field | optional | — | — | — | Sends `?serial=` to `listSerialisedItems`. | `listSerialisedItems` ?serial |
| Status | text field | optional | — | — | — | Sends `?status=` to `listSerialisedItems`. | `listSerialisedItems` ?status |
| Search variants, attributes, barcode | search field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Serial search**: Exact match, with scan support, first and prominent. A serial is unique within an item, not globally, so one serial can return several items. Show them all, with the item name. *(source: contracts/satellite/inventory.yaml#listSerialisedItems)*
- **Status filter**: Chips: In stock, Reserved, Sold, Returned, Damaged, Lost, In transit, Under warranty. *(source: contracts/satellite/inventory.yaml#/components/schemas/SerialisedItem)*
- **Barcode price check**: Scan or type a barcode or SKU. The result shows the price after any live promotion, stock at this outlet and stock at sibling outlets. *(source: R215 / contracts/satellite/retail.yaml#lookupMerchandise)*

#### Outputs: what the screen shows and produces

**Shown**

**Every serialised** (data table, from `listSerialisedItems`)

| Shows | Format | Notes |
|---|---|---|
| Serial | text | Unique within the item, not globally. Two manufacturers reuse serial numbers and a global constraint would refuse the second one. |
| Status | chip: In stock, Reserved, Sold, Returned, Damaged, Lost… | — |
| Warranty until | 1 Oct 2026 | — |
| Received at | 1 Oct 2026, 14:30 | — |

**The selected serialised** (detail panel, from `listSerialisedItems`)

| Shows | Format | Notes |
|---|---|---|
| Serial | text | Unique within the item, not globally. Two manufacturers reuse serial numbers and a global constraint would refuse the second one. |
| Status | chip: In stock, Reserved, Sold, Returned, Damaged, Lost… | — |
| Warranty until | 1 Oct 2026 | — |
| Received at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup merchandise (primary button) | `lookupMerchandise` GET `/merchandise/lookup` | — | PriceCheck | 400 Neither barcode nor SKU supplied, or a caller with no workstation sent no `outletId` (audit R215); 404 No active item with that barcode or SKU at the outlet. An inactive item is not found (audit R215). | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Serial record**: Item, serial, batch, location, status, received date, warranty until, and the sale it was sold on (as a sale number, linked). *(source: DI-406 / contracts/satellite/inventory.yaml#/components/schemas/SerialisedItem)*

**Data it reads**: `listSerialisedItems` (onLoad, listSerialisedItems)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The variants attributes barcode list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the variants attributes barcode untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No variants attributes barcode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on serial, status and the variants attributes barcode are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listSerialisedItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither barcode nor SKU supplied, or a caller with no workstation sent no `outletId` (audit R215) |

#### Consistency with other screens

- Match `EMP-069`: The same serial lookup and statuses on the handheld.
- Match `BO-008`: Size/colour attributes and the barcode per variant are set there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- item: Smartwatch kids GPS, pink
  serial: SW8K-2026-004417
  status: Sold
  location: Marina Bay Retail Floor
  soldOn: Sale MBR-20931
  warrantyUntil: '2027-10-12'
- item: Action camera 4K
  serial: AC4K-88213
  status: In stock
  location: Main Store
```

#### Permissions

- `listSerialisedItems` → `PRODUCT_VIEW` (read) · staff
- `lookupMerchandise` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listSerialisedItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product master holds price, stock and variant attributes (e.g. size/colour) with a distinct barcode per variant; stock is tracked per variant/size. Decision: size/variant attributes (small/medium/large) are configurable per product type in the admin panel and appear dynamically when products are added. *(agreed · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management; 5. Key Decisions · DI-354)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-114` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 4.dc.html#ret-4j`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-114?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup merchandise.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-115` Category, Brand & Merchandise Hierarchy

**Category, Brand & Merchandise Hierarchy — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProductCategories` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/category-brand-merchandise-hierarchy` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-4A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): Sale boards (POS layout, POS-4A), a report runner and a generic suggestion form sat on the category tree; the category tree (listProductCategories … Removed 2 October 2026 (CHG-WIR-025): Sale boards (POS layout, POS-4A), a report runner and a generic suggestion form sat on the category tree; the category tree (listProductCategories … Removed 2 October 2026 (CHG-WIR-025): Sale boards (POS layout, POS-4A), a report runner and a generic suggestion form sat on the category tree; the category tree (listProductCategories …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The category tree guests and tills browse by (Admission > General admission > Single day...; Retail > Apparel > T-shirts), in the order the guest sees it, with a short description per category shown under the option in the guest's "Choose your experience" list.

**Fixed on main** (the package already carries these; draw what it says): Sale boards, a report runner and a generic suggestion form are on this screen. (CHG-SBO-017); List operation(s) listProductCategories, listSaleBoards return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search category, brand | search field | — | — | — | — | — | — |
| Booking flow for this category | picker: choose a booking flow | optional | — | — | shows names, sends the id | **Every product filed here that names no flow of its own is sold through this one** (decided 29 September, W12). Empty means the venue's flow for each product's kind. Saved with … | `ProductCategory.bookingFlowId` |

**Form: Save product categories** (modal, opened by *Save product categories*; *Save product categories* calls `setProductCategories`, *Cancel* sends nothing)

**Collects what `setProductCategories` sends before it is called.** Required: `categories`. Each category may carry a `description` per language: the short text under the option in the guest's "Choose your experience" list (decided 29 September, rev 3 REV3-19). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Categories `categories` | repeatable rows | required | — | — | — | — | `setProductCategories` body |
| ID `categories[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setProductCategories` body |
| Name `categories[].name` | text field | required | — | — | — | — | `setProductCategories` body |
| Code `categories[].code` | text field | optional | — | max length 64 | — | Taken from their category tables, 20 September. Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to … | `setProductCategories` body |
| Name localised `categories[].nameLocalised` | key and value settings | optional | — | — | — | — | `setProductCategories` body |
| Kind `categories[].kind` | radio group | required | — | Category · Brand · Collection · Season · Department | — | — | `setProductCategories` body |
| Parent `categories[].parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them … | `setProductCategories` body |
| Display order `categories[].displayOrder` | number field | optional | 100 | — | — | — | `setProductCategories` body |
| Image `categories[].imageAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `setProductCategories` body |
| Description `categories[].description` | text, one per language | optional | — | Each language value at most 200 characters. | English and Arabic (Arabic right to left) | The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). | `setProductCategories` body |
| Booking flow `categories[].bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | The booking flow for every product filed here that names none of its own (decided 29 September, W12, BO-115). | `setProductCategories` body |
| Is active `categories[].isActive` | toggle | optional | on | — | — | Deactivated rather than deleted. A category with a season behind it still names the products sold under it, and removing it rewrites last year's report. | `setProductCategories` body |

Errors to draw in the form: 400 The body contains a cycle — a category that is its own ancestor — or a `parentId` that names no category in the body.; 409 The body leaves out a category that products name (send it with `isActive` false rather than deleting it), or a category `code` is already used in this tenant …; 422 A category `bookingFlowId` that is not a booking flow of the venue (W12, 29 September).

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **categories**: A drag-and-drop tree saved whole; each node has names and a description per language and an optional booking flow. *(source: contracts/spine/catalogue.yaml#setProductCategories / REV3-19 / DI-441 / DI-355)*

#### Outputs: what the screen shows and produces

**Shown**

**Every product category** (data table, from `listProductCategories`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Category, Brand, Collection, Season, Department | — |
| Display order | 1,234 | — |
| Description | in the reader's language | The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September … |
| Is active | yes / no (icon or chip) | Deactivated rather than deleted. A category with a season behind it still names the products sold under it, and removing it rewrites last … |

**The selected product category** (detail panel, from `listProductCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Name localised | grouped details | — |
| Kind | chip: Category, Brand, Collection, Season, Department | — |
| Parent | the name it points at, never the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each … |
| Scope path | text | Set by the server from the venue the caller acts at; not sent. |
| Display order | 1,234 | — |
| Image | the image or video | — |
| Description | in the reader's language | The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September … |
| Is active | yes / no (icon or chip) | Deactivated rather than deleted. A category with a season behind it still names the products sold under it, and removing it rewrites last … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product categories (primary button) | `setProductCategories` PUT `/product-categories` | inline | ProductCategory[] | 400 The body contains a cycle — a category that is its own ancestor — or a `parentId` that names no category in the body.; 409 The body leaves out a category that products name (send it with `isActive` false rather than … | opens modal first |

**Data it reads**: `listProductCategories` (onLoad, listProductCategories)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-116` Merchandising & Product Presentation: *Merchandising & Product Presentation*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The category brand merchandise list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the category brand merchandise untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No category brand merchandise yet. Offers no create action — this screen declares no operation that makes one. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listProductCategories` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProductCategories` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setProductCategories`; `TENANT_CONFIGURE` for `listBookingFlows`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The body contains a cycle — a category that is its own ancestor — or a `parentId` that names no category in the body.; 409 The body leaves out a category that products name (send it with `isActive` false rather than deleting it), or a category `code` is already used in this tenant …; 422 A category `bookingFlowId` that is not a booking flow of the venue (W12, 29 September). |

#### Edge cases to draw

- **Deleting a category that names products**: Refused; offer Deactivate, because last season's report still names it. *(source: contracts/spine/catalogue.yaml#setProductCategories)*
- **Moving a category under its own child**: Refused as a cycle. *(source: contracts/spine/catalogue.yaml#setProductCategories)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tree:
- Admission > Day passes > Day Pass
- Admission > Annual passes
- Experiences > Dive & snorkel
- Retail > Apparel > T-shirts
category:
  name: Dive & snorkel
  nameAr: الغوص والسنوركل
  description: Guided dives for certified divers and snorkel trips for everyone
```

#### Permissions

- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `setProductCategories` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProductCategories` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setProductCategories`; `TENANT_CONFIGURE` for `listBookingFlows`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Category, Brand & Hierarchy supports multi-level categorisation with subcategories (e.g. Apparel > Retail > Apparel > T-Shirt). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-355)*
- Products are grouped into categories for the tenant website (e.g. a diving operator's scuba diving, free diving, snorkelling, each listing its packages); package title, description, terms, age limits and images come from back-office fields and sync to the live site; choosing a package goes to checkout on the TICVAI booking platform. *(agreed · MoM 7 Aug 2026, 9. Statistical Groups & Website Content Integration · DI-161)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-115` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 4.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 4.dc.html#pos-4a`
- Flow F86 *A POS layout is designed, previewed and deployed*, step 1: Category, Brand & Merchandise Hierarchy. → **Drawn by the client as POS-4A.** 2 operations on this step.
- Flow F86 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-115?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product categories.
- [ ] Every transition is wired: `BO-102`, `BO-116`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-116` Merchandising & Product Presentation

**Arrange how merchandise is presented on the sale boards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `retail` module |
| Block | Block B · task APP-SETUP-BO-116 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | online only |
| Opens with | `venueId` (session), `merchandiseId` (deepLink), `saleBoardId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. A role opened from the directory. |
| Route | `/sell/merchandising-product-presentation` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-4B** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Save role permissions (setRolePermissions) and Save venue settings (setVenueSettings) were attached to a merchandising screen by board position; role permissions … Removed 2 October 2026 (CHG-WIR-021): Save role permissions (setRolePermissions) and Save venue settings (setVenueSettings) were attached to a merchandising screen by board position; role permissions …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Retail merchandising on the sale board: which merchandise shows on which board page, in what order, with what image, and whether it is returnable. Meant for a retail or outlet manager preparing the Wave Shop board. As wired it also edits role permissions and venue settings, which do not belong here.

**Fixed on main** (the package already carries these; draw what it says): Save role permissions (setRolePermissions) and Save venue settings (setVenueSettings) are actions on a merchandising screen. (CHG-WIR-021); Pattern commandCentre with tiles counting merchandise, sale boards and workstations. (CHG-WIR-023); formUpdateSaleBoard asks the person for id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every merchandise' drop id, outletId, categoryId, variantId, inventoryItemId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listMerchandise`. | `listMerchandise` ?outletId |
| Category id | picker: choose a category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?categoryId=` to `listMerchandise`. | `listMerchandise` ?categoryId |
| In stock only | toggle | optional | off | — | — | Sends `?inStockOnly=` to `listMerchandise`. | `listMerchandise` ?inStockOnly |
| Search | text field | optional | — | min length 1; max length 100 | — | Sends `?search=` to `listMerchandise`. | `listMerchandise` ?search |
| Search merchandising | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listSaleBoards` ?kind |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Form: Save merchandise** (modal, opened by *Save merchandise*; *Save merchandise* calls `updateMerchandise`, *Cancel* sends nothing)

**Collects what `updateMerchandise` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `barcode`, `categoryId`, `inventoryItemId`, `imageAssetRef`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateMerchandise` body |
| Description `description` | text area | optional | — | — | — | What the item is, in the guest's words. Null clears it. | `updateMerchandise` body |
| Barcode `barcode` | text field | optional | — | max length 128 | — | Must stay unique in the venue. Null clears it. | `updateMerchandise` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateMerchandise` body |
| Inventory item `inventoryItemId` | picker: choose an inventory item | optional | — | — | shows names, sends the id | Re-points the stock item a sale depletes. Sales already made keep the movements they wrote. | `updateMerchandise` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateMerchandise` body |
| Is returnable `isReturnable` | toggle | optional | — | — | — | — | `updateMerchandise` body |
| Return window days `returnWindowDays` | number field (days) | optional | — | min 0 | — | — | `updateMerchandise` body |
| Requires serial number `requiresSerialNumber` | toggle | optional | — | — | — | — | `updateMerchandise` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateMerchandise` body |

Errors to draw in the form: 409 The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem)

**Form: Save sale board** (modal, opened by *Save sale board*; *Save sale board* calls `updateSaleBoard`, *Cancel* sends nothing)

**Collects what `updateSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **Not asked:** is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `updateSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `updateSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `updateSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `updateSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `updateSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVenueSettings, updateSaleBoard: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setVenueSettings)*

#### Outputs: what the screen shows and produces

**Shown**

**Merchandise** (metric tile, from `listMerchandise`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Description | text | What the item is, in the guest's words. Indexed for guest-app search. |
| ID | the name it points at, never the id | — |
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Variant | the name it points at, never the id | The catalogue variant sold. Price and tax come from there. |
| Inventory item | the name it points at, never the id | The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error. |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| On hand | 1,234.5 | — |
| Is returnable | yes / no (icon or chip) | — |
| Return window days | 1,234 | — |
| Requires serial number | yes / no (icon or chip) | — |
| Image | the image or video | — |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Sale boards** (metric tile, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Name | text | — |
| Sort order | 1,234 | — |
| Tiles | list or chips (count when long) | — |
| Position | 1,234 | — |
| Kind | chip: Product, Category, Action, Spacer | — |
| Variant | the name it points at, never the id | — |
| Label | text | — |
| Colour | text | — |
| Image | the image or video | — |
| Is active | yes / no (icon or chip) | — |

**Workstations** (metric tile, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | The outlet this till stands in (CHG-CSP-006). Its board is the till's board unless the till overrides it. |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| ID | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Name | text | — |
| Sale board source | chip: Outlet, Workstation | Where `saleBoard` came from (decided 2 October 2026, Chinmay, BO-109: "Per outlet, with a till override"; DEC-183; CHG-CSP-006): `outlet` … |
| Cash drawer limit | AED 1,234.50 | This till's drawer limit, overriding the venue's (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point. |
| Devices | list or chips (count when long) | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously … |
| Identifier | text | Serial |
| Is required | yes / no (icon or chip) | When true, the workstation refuses to open a shift if the device is absent. |

**Every merchandise** (data table, from `listMerchandise`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| On hand | 1,234.5 | — |
| Is returnable | yes / no (icon or chip) | — |
| Return window days | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save merchandise (primary button) | `updateMerchandise` PATCH `/merchandise/{merchandiseId}` | inline | MerchandiseItem | 409 The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem) | opens modal first |
| Save sale board (secondary button) | `updateSaleBoard` PUT `/sale-boards/{saleBoardId}` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Merchandise list**: SKU, name, price with currency, on hand, returnable and return window; filter by outlet and category; in-stock-only toggle. *(source: contracts/satellite/retail.yaml#listMerchandise)*
- **Money columns (price)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listMerchandise` (onLoad, List merchandise); `listSaleBoards` (onLoad, List sale boards); `listWorkstations` (onLoad, List workstations)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-117` Product Import, Governance & AI Configuration Assistant: *Product Import, Governance & AI Configuration Assistant*; calls `updateMerchandise`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The merchandising product presentation figures; each tile loads on its own. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the merchandising product presentation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No merchandising product presentation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, categoryId, inStockOnly, search and the merchandising product presentation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listMerchandise` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `updateMerchandise`; `WORKSTATION_CONFIGURE` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tile references an unknown or unsellable variant; 409 The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PRODUCT_VIEW, SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PRODUCT_CONFIGURE for Save merchandise; ROLE_MANAGE for Save role permissions; TENANT_CONFIGURE for Save venue settings; WORKSTATION_CONFIGURE for Save sale board. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/retail.yaml#updateMerchandise)*
- **updateMerchandise answers 409**: Show it as something the person can act on, not a failure: The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. *(source: contracts/satellite/retail.yaml#updateMerchandise)*
- **setRolePermissions answers 409**: Show it as something the person can act on, not a failure: **Breaches a segregation rule.** Names the rule and both permissions. *(source: contracts/spine/tenancy.yaml#setRolePermissions)*
- **setVenueSettings answers 422**: Show it as something the person can act on, not a failure: **An enable the venue cannot evidence.** Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender verification where no device in the venue reports `genderClassification`. `errors[]` names each missing field or the missing capability. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

#### Consistency with other screens

- Match `BO-125`: Product & Category Button Configuration places the same items on the board; one board editor.
- Match `BO-124`: The sale board itself is defined there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
merchandise:
- sku: WS-TOWEL-01
  name: AquaCove beach towel
  price: AED 89.00
  onHand: 140
  returnable: true
  returnWindowDays: 14
- sku: WS-GOGG-02
  name: Kids swim goggles
  price: AED 35.00
  onHand: 12
  returnable: false
```

#### Permissions

- `listMerchandise` → `PRODUCT_VIEW` (read) · staff, guest
- `updateMerchandise` → `PRODUCT_CONFIGURE` (configure) · staff
- `listSaleBoards` → `SCOPE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `updateSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listMerchandise` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `updateMerchandise`; `WORKSTATION_CONFIGURE` …

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.51 | Merchandise Catalog - System shall provide merchandise browsing. | Guest Mobile App & Branding | CONTRACTED | `listMerchandise` |
| 13.3.10 | APIs shall support product catalogs, inventory availability, promotions, orders, exchanges and returns. | Developer & API Management | CONTRACTED | `listMerchandise` |
| 2.1.9 | The system should allow the interface of POS solution to be configurable: - Configurable hot keys on touch screen to link to a specific action. - Configuration of various sales screens (buttons … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.12.19 | Order Sales 1) The POS home page displays available products by category, for the current POS. 2) Staff can click a specific product to add it to the cart; quantity can be adjusted 3) The system … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Catalog Builder & Store Assortment maps which products sell on which channel (on-site, online, or restricted), managed at catalog level rather than per individual product. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-356)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-116` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 4.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 4.dc.html#pos-4b`
- Flow F86 *A POS layout is designed, previewed and deployed*, step 2: Merchandising & Product Presentation. → **Drawn by the client as POS-4B.** 2 operations on this step.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-116?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save merchandise, Save sale board.
- [ ] Every transition is wired: `BO-102`, `BO-117`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-117` Product Import, Governance & AI Configuration Assistant

**Product Import, Governance & AI Configuration Assistant — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block A · task APP-SETUP-BO-117 |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSaleBoards` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `jobId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/product-import-governance-ai-configuration-assistant` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-4C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): Sale boards are a POS layout concern (POS board 4C) unrelated to product import, and the assistant here is generateConfiguration, not a generic thirteen-kind … Removed 2 October 2026 (CHG-WIR-025): Sale boards are a POS layout concern (POS board 4C) unrelated to product import, and the assistant here is generateConfiguration, not a generic thirteen-kind … Removed 2 October 2026 (CHG-WIR-025): Sale boards are a POS layout concern (POS board 4C) unrelated to product import, and the assistant here is generateConfiguration, not a generic thirteen-kind …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Two ways to create a lot of catalogue quickly: import a file (preview, findings, then commit) and describe it to the configuration assistant, which asks follow-up questions and drafts a configuration for review. The thing to get right is that nothing the assistant or an import produces is live: everything arrives as a draft a person reviews.

**Fixed on main** (the package already carries these; draw what it says): The screen also carries listSaleBoards and updateSaleBoard (POS layout boards). (CHG-WIR-025); requestSuggestion (13 suggestion kinds) is offered as a generic form. (CHG-WIR-025); List operation(s) listSaleBoards return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product import, governance | search field | — | — | — | — | — | — |

**Form: Import product catalogue** (modal, opened by *Import product catalogue*; *Import product catalogue* calls `importProductCatalogue`, *Cancel* sends nothing)

**Collects what `importProductCatalogue` sends before it is called.** Required: `format`, `sourceRef`. Optional: `mode`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Format `format` | segmented control | required | — | Csv · Xlsx · Json | — | — | `importProductCatalogue` body |
| Source ref `sourceRef` | picker: choose a source ref | required | — | — | shows names, sends the id | The uploaded file, as the `MediaAsset.id` that `assets.completeUpload` returns after `assets.createUpload` — the reference every contract stores for a file. | `importProductCatalogue` body |
| Mode `mode` | segmented control | optional | Create only | Create only · Upsert · Replace category | — | `replaceCategory` is the dangerous one and is named so it can be refused. Replacing a category with live orders against it is not an import, it is a migration. | `importProductCatalogue` body |

Errors to draw in the form: 409 `mode` is `replaceCategory` and a category the file would replace has live orders against it — that is a migration, not an import.

**Form: Generate configuration** (modal, opened by *Generate configuration*; *Generate configuration* calls `generateConfiguration`, *Cancel* sends nothing)

**Collects what `generateConfiguration` sends before it is called.** Required: `kind`, `description`. Optional: `conversationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Product · Membership · Pass · Promotion · Discount rule · Pricing calendar · Seating zone · Operating hours · Campaign | — | — | `generateConfiguration` body |
| Description `description` | text area | required | — | min length 5; max length 4000 | — | — | `generateConfiguration` body |
| Conversation `conversationId` | picker: choose a conversation | optional | — | — | shows names, sends the id | Where the clarifying questions were asked and answered. | `generateConfiguration` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **import file**: Choose format, upload, map columns; the preview reports counts ("2,847 products, 14 with no price, 3 duplicate codes") before any commit. *(source: contracts/spine/catalogue.yaml#importProductCatalogue / DI-439)*
- **assistant prompt**: Conversational: on "I want to create a product" the assistant asks the type (admission, time slot, seat assignment), validity, dates and capacity and refuses to proceed while required information is missing; it accepts unstructured text and images (OCR). *(source: contracts/satellite/ai.yaml#generateConfiguration / DI-279 / DI-440 / DI-713 / DI-937)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import product catalogue (primary button) | `importProductCatalogue` POST `/products/import` | inline | CatalogueImportJob | 409 `mode` is `replaceCategory` and a category the file would replace has live orders against it — that is a migration, not an import. | opens modal first |
| Generate configuration (secondary button) | `generateConfiguration` POST `/generate/configuration` | inline | GeneratedConfiguration | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **assistant result**: A configuration blueprint showing what will be created, the assumptions it made (each editable), the clarifications still needed and its confidence; then "Create as draft". *(source: contracts/satellite/ai.yaml#generateConfiguration / DI-937)*
- **import findings**: Findings grouped by severity, each with the row number and field, filterable; errors block commit, warnings do not. *(source: contracts/spine/catalogue.yaml#importProductCatalogue)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Commit import**: Refused when nothing was found or the file was unreadable; otherwise creates or updates products as drafts and reports counts. *(source: contracts/spine/catalogue.yaml#commitCatalogueImport)*

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-118` Campaign & Audience Management: *Campaign & Audience Management*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product import governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product import governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product import governance yet. Offers Import product catalogue (`importProductCatalogue`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind and the product import governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_CONFIGURE`, which `importProductCatalogue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The job found nothing, or was already committed. Partial application is reported rather than rolled back — three thousand products half-created is a state …; 409 `mode` is `replaceCategory` and a category the file would replace has live orders against it — that is a migration, not an import. |

#### Edge cases to draw

- **Assistant proposal touches prices**: Shown with who suggested it; approval and publication follow the normal path and the history records it. *(source: DI-938)*

#### Consistency with other screens

- Match `ADM-121`: The P09 bulk import is the same two-phase job; same preview and findings layout.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
prompt: Create a twilight ticket for Coastal Aqua, Fridays 6 to 10 pm, AED 99 adults, AED 79 children
assumptions:
- 'Kind: timed admission'
- 'Channels: Website, App'
- 'Capacity per slot: missing, please confirm'
import:
  file: dune-retail-range-oct.xlsx
  parsed: 2847
  create: 2790
  update: 57
  findings:
    errors: 3
    warnings: 14
```

#### Permissions

- `importProductCatalogue` → `PRODUCT_CONFIGURE` (configure) · staff
- `generateConfiguration` → `AI_USE` (operate) · staff
- `commitCatalogueImport` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_CONFIGURE`, which `importProductCatalogue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

32 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.2 | The system should allow creation of product catalogue through bulk-file uploads. | Ticketing Catalogue | CONTRACTED | `importProductCatalogue` |
| 1.4.3 | The system should allow import and export of products in the catalogue between different environments. | Ticketing Catalogue | CONTRACTED | `importProductCatalogue` |
| 5.7.81 | Export COA data to CSV. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.7.82 | Export financial reports to Excel and CSV. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.7.83 | Bulk account import. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.7.84 | Bulk account updates. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.7.85 | Scheduled report exports. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.12.47 | Assign rules to product groups (Matrix Sheets). | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.12.48 | Assign rules to individual products (Matrix Cells). | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.12.50 | Support bulk product assignments. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 5.12.51 | Support mass updates to product mappings. | F&B & Guest Management | CONTRACTED | `importProductCatalogue` |
| 7.1.34 | The system shall support bulk import and export of users, roles, groups, and permissions with validation and audit logging. | F&B POS | CONTRACTED | `importProductCatalogue` |
| … 20 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI-prepared configuration keeps full version history, e.g. every price change shows who suggested it, who approved it and when it was published. *(client request · MoM 18 Sep 2026, 4.7 AI Configuration Assistant — Approval, Execution & Audit Trail · DI-938)*
- The AI configuration assistant is conversational and iterative: on "I want to create a product" it asks follow-ups (ticket type, validity, date/time) and, if required information such as capacity is missing, asks for it rather than proceeding, before showing a configuration blueprint and dependency map. *(agreed · MoM 18 Sep 2026, 4.5 AI Configuration Assistant — Conversational Requirement Gathering · DI-937)*
- AI-created product/ticket configuration likewise asks follow-ups before finalising (e.g. is the ticket admission, time-slot or seat-assignment type; which categories and discounts apply). *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-713)*
- AI-assisted draft: an AI wizard asks what ticket type to create and the relevant fields, then auto-configures a draft for review before approval/publish. Agreed extension (Chinmay): it also parses unstructured input (incl. OCR on images) and prompts the user for missing details. *(agreed · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-440)*
- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-117` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 4.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 4.dc.html#pos-4c`
- Flow F86 *A POS layout is designed, previewed and deployed*, step 3: Product Import, Governance & AI Configuration Assistant. → **Drawn by the client as POS-4C.** 2 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-117?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import product catalogue, Generate configuration.
- [ ] Every transition is wired: `BO-102`, `BO-118`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-118` Campaign & Audience Management

**Campaign & Audience Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | online only |
| Opens with | `venueId` (session), `reportId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/campaign-audience-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-4D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-005): A sale board is a workstation layout (WORKSTATION_CONFIGURE) with nothing to do with campaign and audience management (design-notes correction customer-marketing … Removed 2 October 2026 (CHG-WIR-005): A sale board is a workstation layout (WORKSTATION_CONFIGURE) with nothing to do with campaign and audience management (design-notes correction customer-marketing …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Campaign and audience management from the client's POS board (POS-4D): the list of campaigns and segments with headline counts, and creation. From this process's angle it is a lighter command centre than BO-764 and must show the same statuses and reach.

**Known correction pending (do not draw the wrong version)**

- **BO-118 and BO-764 overlap (campaign list plus create).** Why: Two campaign command centres will drift. Merge them or define BO-118 as the POS-context view. *(source: screens/P08-venue-back-office.yaml#BO-764; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

**Fixed on main** (the package already carries these; draw what it says): Sale boards (listSaleBoards, updateSaleBoard) - POS layouts - sit on a campaign screen. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · Scheduled · Sending · Paused · Completed · Stopped · Failed | — | Sends `?status=` to `listCampaigns`. | `listCampaigns` ?status |
| Search campaign | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | max length 200 | `listSegments` ?search |

**Form: Create campaign** (modal, opened by *Create campaign*; *Create campaign* calls `createCampaign`, *Cancel* sends nothing)

**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCampaign` body |
| Kind `kind` | radio group | required | — | One off · Scheduled · Triggered · Recurring | — | — | `createCampaign` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCampaign` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCampaign` body |
| Segment `segmentId` | picker: choose a segment | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Content `content` | group | required | — | — | — | — | `createCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `createCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `createCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `createCampaign` body |
| Trigger `trigger` | group | optional | — | — | — | — | `createCampaign` body |
| Event `trigger.event` | select | optional | — | Booking confirmed · Visit completed · Membership expiring · Birthday · Abandoned cart · First visit · Inactivity · Entitlement expiring | — | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's … | `createCampaign` body |
| Delay hours `trigger.delayHours` | number field (hours) | optional | — | — | — | — | `createCampaign` body |
| Conditions `trigger.conditions` | repeatable rows | optional | — | — | — | — | `createCampaign` body |
| Attribute `trigger.conditions[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createCampaign` body |
| Operator `trigger.conditions[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createCampaign` body |
| Value `trigger.conditions[].value` | field | optional | — | — | — | — | `createCampaign` body |
| Values `trigger.conditions[].values` | list of values (chips) | optional | — | — | — | — | `createCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCampaign` body |
| Consent purpose `consentPurpose` | select | optional | Marketing | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `createCampaign` body |
| Send window `sendWindow` | group | optional | — | — | — | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. | `createCampaign` body |
| Start time `sendWindow.startTime` | text field | optional | — | — | — | — | `createCampaign` body |
| End time `sendWindow.endTime` | text field | optional | — | — | — | — | `createCampaign` body |
| Time zone `sendWindow.timeZone` | text field | optional | — | — | — | — | `createCampaign` body |
| Send time mode `sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | `optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). | `createCampaign` body |
| Optimise channel `optimiseChannel` | toggle | optional | off | — | — | With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). | `createCampaign` body |
| Variants `variants` | repeatable rows | optional | — | at most 5 | — | A/B (or up to five-way) content and subject variants (29 September, build pass, group G2; 22.1.17, BO-772). | `createCampaign` body |
| Label `variants[].label` | text field | required | — | max length 20 | — | A, B, C... | `createCampaign` body |
| Subject override `variants[].subjectOverride` | key and value settings | optional | — | — | — | Subject line by locale. | `createCampaign` body |
| Template `variants[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | A different template for this variant; null uses the campaign's `content.templateId`. | `createCampaign` body |
| Split percent `variants[].splitPercent` | stepper or slider | optional | — | min 1; max 100 | — | Share of the test group; null splits evenly. | `createCampaign` body |
| Source `variants[].source` | segmented control | optional | Manual | Manual · AI draft | — | — | `createCampaign` body |
| AI decision record `variants[].aiDecisionRecordId` | text field | optional | — | — | — | The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`. | `createCampaign` body |
| Ab test `abTest` | group | optional | — | Required when `variants` has two or more. | — | How the variants are tested. Required when `variants` has two or more. | `createCampaign` body |
| Test percent `abTest.testPercent` | stepper or slider | optional | 20 | min 5; max 100 | — | Share of the audience the variants are tested on; 100 splits everyone and picks no winner. | `createCampaign` body |
| Success metric `abTest.successMetric` | radio group | optional | Click rate | Open rate · Click rate · Conversion rate · Attributed revenue | — | — | `createCampaign` body |
| Decide after hours `abTest.decideAfterHours` | number field (hours) | optional | 4 | min 1; max 168 | — | — | `createCampaign` body |
| Winner rule `abTest.winnerRule` | segmented control | optional | Automatic | Automatic · Manual | — | — | `createCampaign` body |
| Minimum sample per variant `abTest.minimumSamplePerVariant` | number field | optional | 500 | min 1 | — | Below this many sends per variant no winner is declared automatically; a person picks. | `createCampaign` body |
| Winning variant `abTest.winningVariantId` | picker: choose a winning variant | optional | — | — | shows names, sends the id | Set by the automatic rule, or by a person through `updateCampaign`. | `createCampaign` body |

Errors to draw in the form: 400 Validation failed

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Campaigns** (metric tile, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Venue | the name it points at, never the id | — |
| Segment | the name it points at, never the id | — |
| Content | grouped details | — |
| Template | the name it points at, never the id | — |
| Subject override | grouped details | — |
| Merge defaults | grouped details | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. |
| Promotion | the name it points at, never the id | Offer carried by the campaign. Coupon codes are issued from it. |
| Trigger | grouped details | — |
| Event | chip: Booking confirmed, Visit completed, Membership expiring, Birthday, Abandoned cart … | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still … |
| Delay hours | 1,234 | — |
| Conditions | list or chips (count when long) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Send window | grouped details | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. |
| Start time | text | — |
| End time | text | — |

**Segments** (metric tile, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Match | chip: All, Any | — |
| Criteria | list or chips (count when long) | — |
| Attribute | text | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. |
| Operator | chip: Equals, Not equals, Greater than, Less than, Between, In… | — |
| Value | text | — |
| Values | list or chips (count when long) | — |
| Exclude segments | list or chips (count when long) | — |
| Rule groups | list or chips (count when long) | Nested AND / OR / NOT groups (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by … |
| Operator | chip: And, Or, Not | — |
| Criteria | list or chips (count when long) | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). |
| Groups | list or chips (count when long) | — |
| Effective from | 1 Oct 2026, 14:30 | The segment is evaluated for sends only from this time. |
| Effective to | 1 Oct 2026, 14:30 | — |
| Owner principal | the name it points at, never the id | Who answers for the segment; defaults to its creator. |
| Requires approval | yes / no (icon or chip) | Where true, a campaign may use the segment only after an `approvals` request on it is approved. |
| ID | the name it points at, never the id | — |

**Every campaign** (data table, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create campaign (primary button) | `createCampaign` POST `/campaigns` | CreateCampaignRequest | Campaign | 400 Validation failed | opens modal first |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Headline tiles**: Campaigns by status, segments count, and reach (reachable guests) for the selected segment. *(source: contracts/satellite/marketing-crm.yaml#listCampaigns; contracts/satellite/marketing-crm.yaml#listSegments)*

**Data it reads**: `listCampaigns` (onLoad, List campaigns); `listSegments` (onLoad, List segments)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-126` Deployment, Preview & Audit: *Deployment, Preview & Audit*; calls `createCampaign`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign audience figures; each tile loads on its own. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign audience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign audience yet. Offers Create campaign (`createCampaign`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the campaign audience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_VIEW`, which `listCampaigns` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `createCampaign`; `REPORT_VIEW_VENUE` for `runReport`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Validation failed |

#### Consistency with other screens

- Match `BO-764`: Same campaign list and statuses; consider one screen.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaigns:
- Autumn comeback (scheduled 15 Oct)
- Kids Club half-term (sending, 61% delivered)
- Members' Night (completed)
```

#### Permissions

- `listCampaigns` → `MARKETING_VIEW` (read) · staff
- `createCampaign` → `MARKETING_MANAGE` (configure) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `MARKETING_VIEW`, which `listCampaigns` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `createCampaign`; `REPORT_VIEW_VENUE` for `runReport`.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.4.8 | Product & Event Integration | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.9.14 | Marketing Notifications | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-118` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 4.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 4.dc.html#pos-4d`
- Flow F86 *A POS layout is designed, previewed and deployed*, step 4: Campaign & Audience Management. → **Drawn by the client as POS-4D.** 1 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (45 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-118?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create campaign, Run report.
- [ ] Every transition is wired: `BO-102`, `BO-126`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-119` Cross-Sell, Upsell & Recommendation Rules

**Cross-Sell, Upsell & Recommendation Rules — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 operate, 1 configure, 1 read); in the flows as marketer |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getRecommendations` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `ruleId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/cross-sell-upsell-recommendation-rules` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Upsell rules are read-only here** (decided 28 September, audit R183): rules are created and deleted at region level, and this venue screen only shows what they suggest.

**Known gaps.** **`getRecommendations` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rules for what is suggested with what (cross-sell, upsell) at product page, cart, checkout, after purchase, at the gate and in venue, owned at region and read at venue; AI fills the slots within these limits.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createUpsellRule, deleteUpsellRule, decideRecommendations and nothing that returns the current … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search cross-sell, upsell | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Placement | select | — | Product detail · Cart · Checkout · Post purchase · At gate · In venue | `listUpsellRules` ?placement |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rule**: Trigger products or categories, suggested products or bundle, placement, channels (all by default), at most N suggestions (default 3). *(source: contracts/satellite/promotions.yaml#createUpsellRule / DI-959)*

#### Outputs: what the screen shows and produces

**Shown**

**Recommendations** (data table, from `getRecommendations`): Shows `productId`, `reason`, `confidence` from `getRecommendations`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | — |
| Reason | chip: Frequently bought together, Completes visit, Popular now, Previously purchased … | — |
| Confidence | 1,234.5 | — |

**The upsell suggestion** (detail panel, from `getUpsellSuggestions`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discounted price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Source | chip: Rule, Recommendation | A configured rule always outranks a model. |
| Rank | 1,234 | — |
| Rationale | text | — |

**List upsell and cross-sell rules** (data table, from `listUpsellRules`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Region | the name it points at, never the id | The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's … |
| Name | text | — |
| Placement | chip: Product detail, Cart, Checkout, Post purchase, At gate, In venue | — |
| Trigger variants | list or chips (count when long) | — |
| Trigger categorys | list or chips (count when long) | — |
| Suggested variants | list or chips (count when long) | — |
| Suggested bundle | the name it points at, never the id | — |
| Channels | list or chips (count when long) | Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience … |
| Priority | 1,234 | — |
| Max suggestions | 1,234 | — |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **guest preview**: How the suggestion looks at the chosen placement before publishing. *(source: DI-961)*
- **performance**: Shown, clicked, bought and conversion per rule, AI vs rule-based. *(source: DI-963)*

**Data it reads**: `listUpsellRules` (onLoad, List upsell and cross-sell rules)

**Where the user goes next**

- → `BO-010` Promotions & Coupons: *Promotions & Coupons*
- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-sell upsell recommendation, read by `getUpsellSuggestions`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-sell upsell recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-sell upsell recommendation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listUpsellRules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `decideRecommendations`; `PRODUCT_CONFIGURE` for `createUpsellRule`, `deleteUpsellRule`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Suggesting something the guest already owns**: Never offered; a member is offered add-ons, not another membership. *(source: DI-959 / DI-960)*
- **Deleting a rule from a venue**: Only at the owning region; at venue the rule is read-only with the region named. *(source: contracts/satellite/promotions.yaml#deleteUpsellRule / R183)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Fast track with day pass
  trigger: Day Pass
  suggest: Fast Track Express
  placement: cart
  max: 1
```

#### Permissions

- `createUpsellRule` → `PRODUCT_CONFIGURE` (configure) · staff
- `deleteUpsellRule` → `PRODUCT_CONFIGURE` (configure) · staff
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous
- `listUpsellRules` → `PRODUCT_VIEW` (read) · staff
- `getRecommendations` → `PRODUCT_VIEW` (read) · staff, guest
- `getUpsellSuggestions` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listUpsellRules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `decideRecommendations`; `PRODUCT_CONFIGURE` for `createUpsellRule`, `deleteUpsellRule`.

#### Requirements it meets

54 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.46 | Personalized Offers - System shall provide personalized offers. | Guest Mobile App & Branding | CONTRACTED | `decideRecommendations` |
| 1.1.33 | AI shall recommend suitable ticket products, upgrades, bundles and promotions based on guest profile, behavior and purchase history. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.34 | AI shall recommend upgrades, add-ons and premium experiences during the purchasing journey. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.35 | AI shall automatically recommend ticket bundles, packages and complementary products to maximize guest value and revenue. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 2.6.46 | AI shall recommend relevant tickets, memberships, packages, upgrades, add-ons, F&B, retail products, and experiences based on browsing behavior, purchase history, guest profile, selected products … | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 2.13.45 | AI Assisted Recommendations | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 2.14.18 | AI recommends upgrades, renewals and offers. | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 3.7.9 | System shall generate personalized recommendations for attractions, experiences, memberships, annual passes, F&B products, retail products, upgrades, and add-ons using AI and behavioral analytics. | Admission and Access | CONTRACTED | `decideRecommendations` |
| 4.1.14 | AI recommends higher-value products and add-ons. | Bundles and Promotions | CONTRACTED | `decideRecommendations` |
| 4.1.15 | AI recommends complementary products. | Bundles and Promotions | CONTRACTED | `decideRecommendations` |
| 4.4.30 | Provide AI-driven upsell and cross-sell recommendations based on customer profile, purchase history, loyalty status, seasonality, and basket contents. | Bundles and Promotions | CONTRACTED | `decideRecommendations` |
| 5.4.21 | Recommend rewards and offers. | F&B & Guest Management | CONTRACTED | `decideRecommendations` |
| … 42 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recommendation analytics show response rates, drop-offs, successful purchases and conversion per recommendation, broken down by strategy type (AI-based vs rule-based). *(client request · MoM 21 Sep 2026, 4.7 Recommendation Performance Analytics · DI-963)*
- Recommendation touchpoints are configurable (cart, checkout or post-purchase, per channel), and a presentation/experience preview visually simulates how a recommendation will look to the guest before it is published. *(client request · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-961)*
- What a guest is offered depends on context: a member is not offered another membership (F&B or retail add-ons instead); general admission is not offered once VIP/fast pass is selected; an expiring membership prompts a renewal rather than a new product; similar offers are not shown back-to-back (alternate F&B and experience upsells). *(client request · MoM 21 Sep 2026, 4.2 / 4.3 / 4.5 Recommendation Strategy and Decisioning · DI-960)*
- Recommendations stay within business limits, e.g. at most three recommendations shown at checkout and never a product the customer already owns; AI recommendations never override hard business rules or eligibility constraints. *(agreed · MoM 21 Sep 2026, 4.3 Recommendation Strategy — Business Priority, Conflict Suppression & Fallback · DI-959)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-119` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 5.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 5.dc.html#ret-5d`
- Flow F90 *An audience is built, offered to, and the result is judged*, step 1: Cross-Sell, Upsell & Recommendation Rules. → **Drawn by the client as RET-5D.**
- Flow F90 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.
- ADR-0052 *One recommendation engine; runtime in AI, configuration in Promotions* (`docs/adr/0052-one-recommendation-engine.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-119?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel.
- [ ] Every transition is wired: `BO-010`, `BO-102`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-120` Omnichannel Commerce & Journey Configuration

**Omnichannel Commerce & Journey Configuration — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listJourneys` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/omnichannel-commerce-journey-configuration` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `Retail Board 5.dc.html` frame `ret-5g`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Omnichannel Commerce &amp; Journey Configuration* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Configuration of automated guest journeys and recommendation touchpoints across channels (from the retail board, frame ret-5g). It lists journeys and starts new ones. A journey is created as a draft and activation is a separate act, because a half-drawn journey that starts sending is worse than one that never starts.

**Known correction pending (do not draw the wrong version)**

- **The "Create journey" modal asks for id, status and scopePath.** Why: System fields; a journey is created in draft from a template in the builder. *(source: screens/P08-venue-back-office.yaml#BO-120; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*
- **The client design input for this board is recommendation touchpoints (cart, checkout, post-purchase per channel) with a guest-view preview, which are recommendation strategy operations, not marketing journeys.** Why: The screen is wired to journeys only; recommendation strategies live on the ADM recommendation screens. *(source: DI-961; contracts/satellite/promotions.yaml#updateRecommendationStrategy; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is BO-120 a marketing-journey screen or the recommendation touchpoint configuration from the 21 September board?** → Drawn default accepted: Marketing journeys list; recommendation touchpoints stay on the ADM recommendation screens. *(decided by Chinmay, 2026-10-02; DEC-277 / CHG-NOTE-002)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search omnichannel commerce | search field | — | — | — | — | — | — |

**Form: Create journey** (modal, opened by *Create journey*; *Create journey* calls `createJourney`, *Cancel* sends nothing)

**Collects what `createJourney` sends before it is called.** Required: `name`, `entryEvent`, `steps`. Optional: `templateKind`, `entryConditions`, `maxDurationDays`, `reentryPolicy`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath`, `status` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | — | `createJourney` body |
| Template kind `templateKind` | select | optional | — | Abandoned cart · Membership lifecycle · Loyalty lifecycle · Wallet lifecycle · Birthday · Onboarding · Win back · Custom | — | Which named lifecycle this implements. Set for reporting and for the library, not for behaviour — the steps decide what happens. | `createJourney` body |
| Entry event `entryEvent` | text field | required | — | — | — | 22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes. | `createJourney` body |
| Entry conditions `entryConditions` | group | optional | — | — | — | Narrows entry — a segment, a tier, a venue. Evaluated once at entry, unlike step conditions. | `createJourney` body |
| Steps `steps` | repeatable rows | required | — | — | — | 22.3.1b. What the builder produces. | `createJourney` body |
| ID `steps[].id` | text field | required | — | — | — | — | `createJourney` body |
| Kind `steps[].kind` | radio group | required | — | Send · Wait · Branch · Exit · Goal | — | — | `createJourney` body |
| Template `steps[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | For `send`. Channel is resolved from the guest's preference at the moment of sending. | `createJourney` body |
| Send time mode `steps[].sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's suggested hour from `ai.requestSuggestion` … | `createJourney` body |
| Channel mode `steps[].channelMode` | segmented control | optional | Preference | Preference · Optimised | — | For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16). | `createJourney` body |
| Channel preference `steps[].channelPreference` | multi-select chips | optional | — | Email · SMS · Whatsapp · Push · In app | — | 22.3.3b. Ordered fallback — email, then SMS, then push. | `createJourney` body |
| Wait minutes `steps[].waitMinutes` | number field (minutes) | optional | — | — | — | — | `createJourney` body |
| Wait until `steps[].waitUntil` | group | optional | — | — | — | 22.3.5b. Business hours, time zone and blackout windows — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are venue configuration rather than a … | `createJourney` body |
| Business hours only `steps[].waitUntil.businessHoursOnly` | toggle | optional | off | — | — | — | `createJourney` body |
| Timezone `steps[].waitUntil.timezone` | text field | optional | — | — | — | — | `createJourney` body |
| Respect quiet hours `steps[].waitUntil.respectQuietHours` | toggle | optional | on | — | — | — | `createJourney` body |
| Not before `steps[].waitUntil.notBefore` | text field | optional | — | — | — | — | `createJourney` body |
| Condition `steps[].condition` | group | optional | — | — | — | 22.3.4b. IF/THEN over guest profile, behaviour and prior steps. | `createJourney` body |
| Field `steps[].condition.field` | text field | optional | — | — | — | — | `createJourney` body |
| Operator `steps[].condition.operator` | select | optional | — | Eq · Neq · Gt · Lt · Contains · Exists · Not exists | — | — | `createJourney` body |
| Value `steps[].condition.value` | text field | optional | — | — | — | — | `createJourney` body |
| On true `steps[].onTrue` | text field | optional | — | — | — | Next step id. | `createJourney` body |
| On false `steps[].onFalse` | text field | optional | — | — | — | — | `createJourney` body |
| Next `steps[].next` | text field | optional | — | — | — | — | `createJourney` body |
| Goal event `steps[].goalEvent` | text field | optional | — | — | — | For `goal`. The event that means this journey worked and the guest should leave it — a purchase for abandoned cart, a renewal for membership. | `createJourney` body |
| Max duration days `maxDurationDays` | number field (days) | optional | 30 | — | — | A journey with no end is a guest who never leaves it. After this, entrants exit wherever they are. | `createJourney` body |
| Reentry policy `reentryPolicy` | segmented control | optional | After completion | Never · After completion · Always | — | 22.3.6b. Abandoned cart is the case that needs this. | `createJourney` body |

Errors to draw in the form: 422 The graph does not terminate, or a step points at nothing. Refused at creation rather than discovered by a guest stuck in a loop.

#### Outputs: what the screen shows and produces

**Shown**

**Every journey** (data table, from `listJourneys`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Template kind | chip: Abandoned cart, Membership lifecycle, Loyalty lifecycle, Wallet lifecycle … | Which named lifecycle this implements. Set for reporting and for the library, not for behaviour — the steps decide what happens. |
| Entry event | text | 22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes. |
| Status | chip: Draft, Active, Paused, Archived | — |
| Max duration days | 1,234 | A journey with no end is a guest who never leaves it. After this, entrants exit wherever they are. |
| Reentry policy | chip: Never, After completion, Always | 22.3.6b. Abandoned cart is the case that needs this. |

**The selected journey** (detail panel, from `listJourneys`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Template kind | chip: Abandoned cart, Membership lifecycle, Loyalty lifecycle, Wallet lifecycle … | Which named lifecycle this implements. Set for reporting and for the library, not for behaviour — the steps decide what happens. |
| Entry event | text | 22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes. |
| Entry conditions | grouped details | Narrows entry — a segment, a tier, a venue. Evaluated once at entry, unlike step conditions. |
| Steps | list or chips (count when long) | 22.3.1b. What the builder produces. |
| Status | chip: Draft, Active, Paused, Archived | — |
| Max duration days | 1,234 | A journey with no end is a guest who never leaves it. After this, entrants exit wherever they are. |
| Reentry policy | chip: Never, After completion, Always | 22.3.6b. Abandoned cart is the case that needs this. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create journey (primary button) | `createJourney` POST `/journeys` | Journey | Journey | 422 The graph does not terminate, or a step points at nothing. Refused at creation rather than discovered by a guest stuck in a loop. | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Journey list**: Name, template (abandoned cart, membership, loyalty, wallet, birthday, onboarding, win-back, custom), entry event, status (draft, active, paused, archived), entrants this week. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/Journey)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Create journey**: Opens the visual builder (BO-775) with the template's steps; nothing sends until activated. *(source: contracts/satellite/marketing-crm.yaml#createJourney)*

**Data it reads**: `listJourneys` (onLoad, Automated journeys)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The omnichannel commerce journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the omnichannel commerce journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No omnichannel commerce journey yet. Offers Create journey (`createJourney`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listJourneys` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_VIEW`, which `listJourneys` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `createJourney`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The graph does not terminate, or a step points at nothing. Refused at creation rather than discovered by a guest stuck in a loop. |

#### Consistency with other screens

- Match `BO-774`: Journey automation centre shows the same list; one of them is redundant.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journeys:
- Abandoned cart - membership only (active)
- Birthday reward (active)
- Win-back 120 days (draft)
```

#### Permissions

- `listJourneys` → `MARKETING_VIEW` (read) · staff
- `createJourney` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `MARKETING_VIEW`, which `listJourneys` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `createJourney`.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.1 | Visual Journey Builder | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.6 | Abandoned Cart Recovery Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.7 | Membership Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.8 | Loyalty Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.9 | Wallet Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.10 | Birthday & Anniversary Campaigns | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.14 | Cross-Sell & Upsell Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.21 | Automation Analytics Dashboard | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.22 | Automation Audit Trail | Marketing & CRM | CONTRACTED | data `Journey` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recommendation touchpoints are configurable (cart, checkout or post-purchase, per channel), and a presentation/experience preview visually simulates how a recommendation will look to the guest before it is published. *(client request · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-961)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-120` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 5.dc.html`
- Client design-board frames: `Retail Board 5.dc.html#ret-5g`

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-120?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create journey.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-121` Personalized Offers & Guest Engagement

**Personalized Offers & Guest Engagement — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSegments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/personalized-offers-guest-engagement` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Personalised offers and guest engagement: pick a segment and reach it with an offer. From this process's angle the two rules are these. Never re-offer what a guest declined, whether on the same channel or another. And show response, conversion and drop-off by strategy (AI versus rule-based).

**Known correction pending (do not draw the wrong version)**

- **The screen's purpose is personalised offers, but it is wired only to listSegments and createCampaign.** Why: Offer performance (DI-963) and decline suppression (DI-962) need the recommendation analytics and decline store; add those reads or narrow the purpose. *(source: DI-963; DI-962; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | text field | optional | — | max length 200 | — | Sends `?search=` to `listSegments`. | `listSegments` ?search |
| Search personalized offers | search field | — | — | — | — | — | — |

**Form: Create campaign** (modal, opened by *Create campaign*; *Create campaign* calls `createCampaign`, *Cancel* sends nothing)

**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCampaign` body |
| Kind `kind` | radio group | required | — | One off · Scheduled · Triggered · Recurring | — | — | `createCampaign` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCampaign` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCampaign` body |
| Segment `segmentId` | picker: choose a segment | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Content `content` | group | required | — | — | — | — | `createCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `createCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `createCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `createCampaign` body |
| Trigger `trigger` | group | optional | — | — | — | — | `createCampaign` body |
| Event `trigger.event` | select | optional | — | Booking confirmed · Visit completed · Membership expiring · Birthday · Abandoned cart · First visit · Inactivity · Entitlement expiring | — | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's … | `createCampaign` body |
| Delay hours `trigger.delayHours` | number field (hours) | optional | — | — | — | — | `createCampaign` body |
| Conditions `trigger.conditions` | repeatable rows | optional | — | — | — | — | `createCampaign` body |
| Attribute `trigger.conditions[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createCampaign` body |
| Operator `trigger.conditions[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createCampaign` body |
| Value `trigger.conditions[].value` | field | optional | — | — | — | — | `createCampaign` body |
| Values `trigger.conditions[].values` | list of values (chips) | optional | — | — | — | — | `createCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCampaign` body |
| Consent purpose `consentPurpose` | select | optional | Marketing | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `createCampaign` body |
| Send window `sendWindow` | group | optional | — | — | — | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. | `createCampaign` body |
| Start time `sendWindow.startTime` | text field | optional | — | — | — | — | `createCampaign` body |
| End time `sendWindow.endTime` | text field | optional | — | — | — | — | `createCampaign` body |
| Time zone `sendWindow.timeZone` | text field | optional | — | — | — | — | `createCampaign` body |
| Send time mode `sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | `optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). | `createCampaign` body |
| Optimise channel `optimiseChannel` | toggle | optional | off | — | — | With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). | `createCampaign` body |
| Variants `variants` | repeatable rows | optional | — | at most 5 | — | A/B (or up to five-way) content and subject variants (29 September, build pass, group G2; 22.1.17, BO-772). | `createCampaign` body |
| Label `variants[].label` | text field | required | — | max length 20 | — | A, B, C... | `createCampaign` body |
| Subject override `variants[].subjectOverride` | key and value settings | optional | — | — | — | Subject line by locale. | `createCampaign` body |
| Template `variants[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | A different template for this variant; null uses the campaign's `content.templateId`. | `createCampaign` body |
| Split percent `variants[].splitPercent` | stepper or slider | optional | — | min 1; max 100 | — | Share of the test group; null splits evenly. | `createCampaign` body |
| Source `variants[].source` | segmented control | optional | Manual | Manual · AI draft | — | — | `createCampaign` body |
| AI decision record `variants[].aiDecisionRecordId` | text field | optional | — | — | — | The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`. | `createCampaign` body |
| Ab test `abTest` | group | optional | — | Required when `variants` has two or more. | — | How the variants are tested. Required when `variants` has two or more. | `createCampaign` body |
| Test percent `abTest.testPercent` | stepper or slider | optional | 20 | min 5; max 100 | — | Share of the audience the variants are tested on; 100 splits everyone and picks no winner. | `createCampaign` body |
| Success metric `abTest.successMetric` | radio group | optional | Click rate | Open rate · Click rate · Conversion rate · Attributed revenue | — | — | `createCampaign` body |
| Decide after hours `abTest.decideAfterHours` | number field (hours) | optional | 4 | min 1; max 168 | — | — | `createCampaign` body |
| Winner rule `abTest.winnerRule` | segmented control | optional | Automatic | Automatic · Manual | — | — | `createCampaign` body |
| Minimum sample per variant `abTest.minimumSamplePerVariant` | number field | optional | 500 | min 1 | — | Below this many sends per variant no winner is declared automatically; a person picks. | `createCampaign` body |
| Winning variant `abTest.winningVariantId` | picker: choose a winning variant | optional | — | — | shows names, sends the id | Set by the automatic rule, or by a person through `updateCampaign`. | `createCampaign` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**Every segment** (data table, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Match | chip: All, Any | — |
| Last evaluated size | 1,234 | — |
| Last evaluated at | 1 Oct 2026, 14:30 | — |

**The selected segment** (detail panel, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Match | chip: All, Any | — |
| Criteria | list or chips (count when long) | — |
| Exclude segments | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Last evaluated size | 1,234 | — |
| Last evaluated at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create campaign (primary button) | `createCampaign` POST `/campaigns` | CreateCampaignRequest | Campaign | 400 Validation failed | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Segments with reach**: Each segment with matching and reachable counts. *(source: contracts/satellite/marketing-crm.yaml#listSegments; contracts/satellite/marketing-crm.yaml#previewSegment)*
- **Offer performance**: Response rate, drop-off, purchases and conversion per offer, split by AI-based and rule-based. *(source: DI-963)*

**Data it reads**: `listSegments` (onLoad, List segments)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The personalized offers guest list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the personalized offers guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No personalized offers guest yet. Offers Create campaign (`createCampaign`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on search and the personalized offers guest are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_VIEW`, which `listSegments` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `createCampaign`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A guest declined the same offer three times or bought it elsewhere**: The guest is excluded from the offer on every channel; the exclusion count shows "declined before". *(source: DI-962; contracts/satellite/ai.yaml#recordRecommendationEvents)*

#### Consistency with other screens

- Match `BO-766`: Create campaign opens the builder with the segment preselected.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
segment: Gold members with no F&B spend in 60 days (matching 1,240; WhatsApp 980)
offer: Free karak with any meal (pre-configured)
```

#### Permissions

- `listSegments` → `MARKETING_VIEW` (read) · staff
- `createCampaign` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `MARKETING_VIEW`, which `listSegments` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `createCampaign`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.4.8 | Product & Event Integration | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.9.14 | Marketing Notifications | Marketing & CRM | CONTRACTED | `createCampaign` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recommendation analytics show response rates, drop-offs, successful purchases and conversion per recommendation, broken down by strategy type (AI-based vs rule-based). *(client request · MoM 21 Sep 2026, 4.7 Recommendation Performance Analytics · DI-963)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-121` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 5.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 5.dc.html#ret-5f`

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-121?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create campaign.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1190` Donation Campaigns

**Create, run and close the donation campaigns guests can give to at checkout.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listDonationCampaigns` reads the population and the panel edits one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `campaignId` (navigation) · cold entry: Resolves the tenant and venue from the session; a cold arrival is the ordinary case. |
| Route | `/sell/donation-campaigns` |

**What the spec says about it.** **Created 29 September (VM close-out)** because `listDonationCampaigns`, `createDonationCampaign` and `updateDonationCampaign` had no screen (matrix 1.1.128-1.1.133). **The amounts are configuration, not code**: fixed choices, a free amount or round-up. **Donations post to a liability account, not revenue** (1.1.132), so the liability account is required before a campaign goes live.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Donation campaigns guests can give to at checkout: fixed choices, a free amount or round-up, per channel and venue, posting to a liability account (not revenue). Several can run at once and one transaction may give to several.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listDonationCampaigns return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are donations taxable, and may a tax or service fee be enabled on them?** → Drawn default stands (answer: "No tax; optional fee switch"): No tax on donations; a switch for a tax or fee, off by default. *(decided by Chinmay, 2026-10-02; DEC-169 / CHG-NOTE-006)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Active only | toggle | — | — | — | — | Filters the loaded list on `isActive`. | — |

**Form: New campaign** (modal, opened by *New campaign*; *Create campaign* calls `createDonationCampaign`, *Cancel* sends nothing)

**Collects what `createDonationCampaign` sends.** Required: `name`, `amountMode`, `isActive`. With fixed choices, `fixedAmounts`; with a free amount, `minAmount` and `maxAmount`; always the `liabilityAccountId` before activation. Optional: `description`, `beneficiary`, `venueIds`, `channels`, `validFrom`, `validTo`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createDonationCampaign` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createDonationCampaign` body |
| Beneficiary `beneficiary` | text field | optional | — | — | — | Who the money is for. Shown to the guest, and it is the reason they give. | `createDonationCampaign` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `createDonationCampaign` body |
| Amount mode `amountMode` | segmented control | required | — | Fixed choices · Free amount · Round up | — | — | `createDonationCampaign` body |
| Fixed amounts `fixedAmounts` | repeatable rows | optional | — | — | — | 1.1.129. Predefined values, e.g. | `createDonationCampaign` body |
| Min amount `minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createDonationCampaign` body |
| Max amount `maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createDonationCampaign` body |
| Liability account `liabilityAccountId` | picker: choose a liability account | optional | — | — | shows names, sends the id | Donations post here, not to revenue (1.1.132). Money collected for a charity is not the venue's to recognise, and treating it as revenue is a restatement waiting to happen. | `createDonationCampaign` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | 1.1.133. Where it may be solicited — POS, kiosk, web, app. | `createDonationCampaign` body |
| Is active `isActive` | toggle | required | — | — | — | — | `createDonationCampaign` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createDonationCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createDonationCampaign` body |

**Sent by *Save campaign*** (`updateDonationCampaign`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `updateDonationCampaign` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateDonationCampaign` body |
| Beneficiary `beneficiary` | text field | optional | — | — | — | Who the money is for. Shown to the guest, and it is the reason they give. | `updateDonationCampaign` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `updateDonationCampaign` body |
| Amount mode `amountMode` | segmented control | required | — | Fixed choices · Free amount · Round up | — | — | `updateDonationCampaign` body |
| Fixed amounts `fixedAmounts` | repeatable rows | optional | — | — | — | 1.1.129. Predefined values, e.g. | `updateDonationCampaign` body |
| Min amount `minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateDonationCampaign` body |
| Max amount `maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateDonationCampaign` body |
| Liability account `liabilityAccountId` | picker: choose a liability account | optional | — | — | shows names, sends the id | Donations post here, not to revenue (1.1.132). Money collected for a charity is not the venue's to recognise, and treating it as revenue is a restatement waiting to happen. | `updateDonationCampaign` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | 1.1.133. Where it may be solicited — POS, kiosk, web, app. | `updateDonationCampaign` body |
| Is active `isActive` | toggle | required | — | — | — | — | `updateDonationCampaign` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateDonationCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateDonationCampaign` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **amountMode**: Fixed choices (up to a few amounts), free amount with minimum and maximum, or round-up; preview of how the guest sees it at checkout. *(source: contracts/spine/catalogue.yaml#createDonationCampaign / DI-471)*
- **liabilityAccountId**: Required to go live; picked from the chart of accounts. *(source: contracts/spine/catalogue.yaml#createDonationCampaign)*

#### Outputs: what the screen shows and produces

**Shown**

**Every donation campaign** (data table, from `listDonationCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Beneficiary | text | Who the money is for. Shown to the guest, and it is the reason they give. |
| Amount mode | chip: Fixed choices, Free amount, Round up | — |
| Channels | list or chips (count when long) | 1.1.133. Where it may be solicited — POS, kiosk, web, app. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Raised total | AED 1,234.50 | Not reversed when the campaign closes. The money is still owed. |

**The selected campaign** (detail panel, from `listDonationCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Amount mode | chip: Fixed choices, Free amount, Round up | — |
| Fixed amounts | list or chips (count when long) | 1.1.129. Predefined values, e.g. |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Raised total | AED 1,234.50 | Not reversed when the campaign closes. The money is still owed. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New campaign (primary button) | `createDonationCampaign` POST `/donation-campaigns` | DonationCampaign | DonationCampaign | — | opens modal first |
| Save campaign (secondary button) | `updateDonationCampaign` PATCH `/donation-campaigns/{campaignId}` | DonationCampaign | DonationCampaign | — | — |
| Close campaign (destructive button) | `updateDonationCampaign` PATCH `/donation-campaigns/{campaignId}` | DonationCampaign | DonationCampaign | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Close campaign**: Stops new donations; donations already given stay owed. *(source: contracts/spine/catalogue.yaml#updateDonationCampaign)*

**Data it reads**: `listDonationCampaigns` (onLoad, Every campaign with what it has raised)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant's donation campaigns, read by `listDonationCampaigns`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaigns untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No donation campaigns yet. Offers New campaign; checkout shows no donation prompt until one is active. |
| Empty, no results (`?state=emptyNoResults`) | The Active only filter matched nothing and the closed campaigns are still there. Offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission (`PRODUCT_VIEW` to see, `PRODUCT_CONFIGURE` to change). **Never an empty table.** |
| Validation (`?state=validation`) | `400` on a missing name or amount mode, fixed amounts missing when the mode is fixed choices, or a minimum above the maximum; marked on the field. A campaign without a liability account cannot be activated. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign:
  name: Ramadan Food Appeal
  nameAr: حملة رمضان للغذاء
  beneficiary: Emirates Red Crescent
  mode: fixedChoices
  amounts:
  - AED 5.00
  - AED 10.00
  - AED 25.00
  channels:
  - Website
  - App
  - Point of sale
  raised: AED 48,215.00
```

#### Permissions

- `listDonationCampaigns` → `PRODUCT_VIEW` (read) · staff
- `createDonationCampaign` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateDonationCampaign` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission (`PRODUCT_VIEW` to see, `PRODUCT_CONFIGURE` to change). **Never an empty table.**

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.131 | The system shall support multiple donation campaigns within a single transaction. Functional Requirements Multiple donation campaigns in one basket. Customer can select one or more campaigns. Ability … | Ticketing Catalogue | CONTRACTED | `listDonationCampaigns` |
| 1.1.133 | The solution shall support donation collection through all POS channels. Functional Requirements Counter POS. Self-service kiosk. Online sales portal. Mobile POS. Third-party sales channels. … | Ticketing Catalogue | CONTRACTED | `listDonationCampaigns` |
| 1.1.128 | Functional Requirements Create multiple donation campaigns. Configure campaign name and description. Define campaign validity dates. Configure campaign images and promotional messages. Configure … | Ticketing Catalogue | CONTRACTED | `createDonationCampaign` |
| 1.1.129 | Functional Requirements Fixed Donation Fixed donation amount. Multiple predefined donation values. Variable Donation Customer enters donation amount. Configurable minimum and maximum donation values. … | Ticketing Catalogue | CONTRACTED | `createDonationCampaign` |
| 1.1.132 | The system shall allow donation campaigns to be associated with specific products or product groups. Functional Requirements Apply donation campaign to all products. Apply donation campaign to … | Ticketing Catalogue | CONTRACTED | `updateDonationCampaign` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: whether donations are taxable. Allam believes they are typically not, but the system should allow enabling/disabling a tax or service fee on donations; Chinmay to confirm treatment. *(open · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 6. Open Items · DI-472)*
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1190` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1190?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, validation, offline.
- [ ] Every action is wired with its success and its failure: New campaign, Save campaign, Close campaign.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**17 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"commitCatalogueImport": {"method":"POST","path":"/products/import/{jobId}/commit","contract":"catalogue","summary":"Apply a parsed catalogue import","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CatalogueImportJob"},
"createCampaign": {"method":"POST","path":"/campaigns","contract":"marketing-crm","summary":"Create a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCampaignRequest","responds":"Campaign"},
"createDonationCampaign": {"method":"POST","path":"/donation-campaigns","contract":"catalogue","summary":"Create a campaign","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DonationCampaign","responds":"DonationCampaign"},
"createJourney": {"method":"POST","path":"/journeys","contract":"marketing-crm","summary":"Define an automated journey","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Journey","responds":"Journey"},
"createUpsellRule": {"method":"POST","path":"/upsell-rules","contract":"promotions","summary":"Create an upsell rule","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpsellRule","responds":"UpsellRule"},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"deleteUpsellRule": {"method":"DELETE","path":"/upsell-rules/{ruleId}","contract":"promotions","summary":"Remove an upsell rule","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"generateConfiguration": {"method":"POST","path":"/generate/configuration","contract":"ai","summary":"Draft a configuration from a description","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GeneratedConfiguration"},
"importProductCatalogue": {"method":"POST","path":"/products/import","contract":"catalogue","summary":"Parse a catalogue file into a preview","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listBookingFlows": {"method":"GET","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"A venue's booking flows, in the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"flowTypeKey","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCampaigns": {"method":"GET","path":"/campaigns","contract":"marketing-crm","summary":"List campaigns","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDonationCampaigns": {"method":"GET","path":"/donation-campaigns","contract":"catalogue","summary":"Campaigns a guest can give to","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DonationCampaign"},
"listJourneys": {"method":"GET","path":"/journeys","contract":"marketing-crm","summary":"Automated journeys","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMerchandise": {"method":"GET","path":"/merchandise","contract":"retail","summary":"List merchandise","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"inStockOnly","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listSaleBoards": {"method":"GET","path":"/sale-boards","contract":"tenancy","summary":"List sale boards","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"SaleBoard"},
"listSegments": {"method":"GET","path":"/segments","contract":"marketing-crm","summary":"List segments","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSerialisedItems": {"method":"GET","path":"/serialised-items","contract":"inventory","summary":"Where each individual item is","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"serial","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listUpsellRules": {"method":"GET","path":"/upsell-rules","contract":"promotions","summary":"List upsell and cross-sell rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"placement","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupMerchandise": {"method":"GET","path":"/merchandise/lookup","contract":"retail","summary":"Price and stock check by barcode","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"barcode","in":"query","required":null},{"name":"sku","in":"query","required":null},{"name":"includeSiblingOutlets","in":"query","required":null},{"name":"outletId","in":"query","required":null}],"requestBody":null,"responds":"PriceCheck"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"setProductCategories": {"method":"PUT","path":"/product-categories","contract":"catalogue","summary":"Define the hierarchy, in the order a guest sees it","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductCategory"},
"updateDonationCampaign": {"method":"PATCH","path":"/donation-campaigns/{campaignId}","contract":"catalogue","summary":"Amend or close a campaign","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DonationCampaign","responds":"DonationCampaign"},
"updateMerchandise": {"method":"PATCH","path":"/merchandise/{merchandiseId}","contract":"retail","summary":"Amend a merchandise item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MerchandiseItem"},
"updateSaleBoard": {"method":"PUT","path":"/sale-boards/{saleBoardId}","contract":"tenancy","summary":"Update a sale board","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SaleBoard","responds":"SaleBoard"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"Campaign": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/CreateCampaignRequest"},{"type":"object","required":["id","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetSpent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"},"status":{"$ref":"#/components/schemas/CampaignStatus"},"isPaused":{"type":"boolean"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"launchedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"sentCount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"}}}]},
"CampaignContent": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","required":["templateId"],"properties":{"templateId":{"type":"string","format":"uuid"},"subjectOverride":{"type":"object","additionalProperties":{"type":"string"}},"mergeDefaults":{"type":"object","description":"Fallback values for the template's `mergeFields`, by name, used where a guest has no value.","additionalProperties":{"type":"string"}},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Offer carried by the campaign. Coupon codes are issued from it."}}},
"CampaignKind": {"type":"string","enum":["oneOff","scheduled","triggered","recurring"]},
"CampaignStatus": {"type":"string","enum":["draft","scheduled","sending","paused","completed","stopped","failed"]},
"CampaignTrigger": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","properties":{"event":{"type":"string","enum":["bookingConfirmed","visitCompleted","membershipExpiring","birthday","abandonedCart","firstVisit","inactivity","entitlementExpiring"],"description":"`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."},"delayHours":{"type":"integer"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/SegmentCriterion"}}}},
"CatalogueImportJob": {"type":"object","x-ticvai-persistence":"catalogue.import_job","description":"1.4.2. **Two-phase, following `seating.ImportJob`** — and carrying the same lesson: a job that parses zero products is not a parsed job.\n","required":["id","status","parsedCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["parsing","previewReady","committing","committed","failed"]},"outcome":{"type":"string","enum":["parsed","parsedWithFindings","nothingFound","unreadable"]},"parsedCount":{"type":"integer"},"createCount":{"type":"integer"},"updateCount":{"type":"integer"},"findings":{"type":"array","description":"**What an operator sees before committing** — missing prices, duplicate codes, unknown categories, codes that do not match the tenant's schema.\n","items":{"type":"object","properties":{"row":{"type":"integer"},"severity":{"type":"string","enum":["error","warning"]},"message":{"type":"string"}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"},"jobKind":{"type":"string","enum":["productImport","environmentTransfer","pricingBulkUpdate","pricingImport"],"default":"productImport","description":"**One job table for every catalogue bulk operation** (29 September, data model DM3): product import (the original use), environment transfer (ADM-124) and bulk pricing update or import (ADM-080). A pricing job never writes prices; committing it creates a change request (`changeRequestId`)."},"direction":{"type":"string","enum":["export","import",null],"nullable":true},"sourceEnvironment":{"type":"string","enum":["development","sandbox","uat","staging","production",null],"nullable":true},"targetEnvironment":{"type":"string","enum":["development","sandbox","uat","staging","production",null],"nullable":true},"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"components":{"type":"array","items":{"type":"string"},"description":"Transfer components, per `ProductImportExportEnvironmentTransferView.components`."},"referenceMappings":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{kind, sourceRef, targetRef}]`."},"missingReferences":{"type":"array","items":{"type":"string"}},"fileId":{"type":"string","format":"uuid","nullable":true},"sourceFormat":{"type":"string","maxLength":40,"nullable":true},"columnMappings":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{sourceColumn, targetField, suggestedByAi, confirmed}]`."},"parameters":{"type":"object","additionalProperties":true,"nullable":true,"description":"Bulk pricing: `{selectBy, selectionValues, operation, adjustmentPercent, adjustmentAmount, targetCurrency, effectivePeriodFrom, effectivePeriodTo}`."},"warningCount":{"type":"integer","default":0},"errorCount":{"type":"integer","default":0},"changeRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"CreateCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","kind","channel","segmentId","content"],"properties":{"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/CampaignKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"content":{"$ref":"#/components/schemas/CampaignContent"},"trigger":{"$ref":"#/components/schemas/CampaignTrigger"},"scheduledFor":{"type":"string","format":"date-time"},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"default":"marketing"},"sendWindow":{"type":"object","description":"Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n","properties":{"startTime":{"type":"string"},"endTime":{"type":"string"},"timeZone":{"type":"string"}}},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."},"optimiseChannel":{"type":"boolean","default":false,"description":"With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."},"variants":{"type":"array","maxItems":5,"nullable":true,"description":"**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.","items":{"$ref":"#/components/schemas/MarketingCampaignVariant"}},"abTest":{"type":"object","nullable":true,"description":"How the variants are tested. Required when `variants` has two or more.","properties":{"testPercent":{"type":"integer","minimum":5,"maximum":100,"default":20,"description":"Share of the audience the variants are tested on; 100 splits everyone and picks no winner."},"successMetric":{"type":"string","enum":["openRate","clickRate","conversionRate","attributedRevenue"],"default":"clickRate"},"decideAfterHours":{"type":"integer","minimum":1,"maximum":168,"default":4},"winnerRule":{"type":"string","enum":["automatic","manual"],"default":"automatic"},"minimumSamplePerVariant":{"type":"integer","minimum":1,"default":500,"description":"Below this many sends per variant no winner is declared automatically; a person picks."},"winningVariantId":{"type":"string","format":"uuid","nullable":true,"description":"Set by the automatic rule, or by a person through `updateCampaign`."}}}}},
"CreateSegmentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","criteria"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"match":{"type":"string","enum":["all","any"],"default":"all"},"criteria":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/SegmentCriterion"}},"excludeSegmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ruleGroups":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**Nested AND / OR / NOT groups** (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by `match`) AND every group here. Absent keeps the flat list.","items":{"$ref":"#/components/schemas/SegmentRuleGroup"}},"effectiveFrom":{"type":"string","format":"date-time","nullable":true,"description":"The segment is evaluated for sends only from this time."},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who answers for the segment; defaults to its creator."},"requiresApproval":{"type":"boolean","default":false,"description":"Where true, a campaign may use the segment only after an `approvals` request on it is approved."}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"DonationAmountMode": {"type":"string","enum":["fixedChoices","freeAmount","roundUp"]},
"DonationCampaign": {"type":"object","x-ticvai-persistence":"catalogue.donation_campaign","required":["name","amountMode","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"beneficiary":{"type":"string","description":"Who the money is for. Shown to the guest, and it is the reason they give."},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"amountMode":{"$ref":"#/components/schemas/DonationAmountMode"},"fixedAmounts":{"type":"array","description":"1.1.129. Predefined values, e.g. 5, 10, 25.","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"liabilityAccountId":{"type":"string","format":"uuid","description":"**Donations post here, not to revenue** (1.1.132). Money collected for a charity is not the venue's to recognise, and treating it as revenue is a restatement waiting to happen.\n"},"channels":{"type":"array","description":"1.1.133. Where it may be solicited — POS, kiosk, web, app.","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","nullable":true},"raisedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Not reversed when the campaign closes.** The money is still owed.\n"}}},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"GeneratedConfiguration": {"type":"object","x-ticvai-persistence":"none — a draft, applied through the owning contract; the draft itself is the ai.proposed_action row named by proposedActionId","required":["proposedActionId","kind","targetContract","targetOperation","payload"],"properties":{"proposedActionId":{"type":"string","format":"uuid","description":"**The `ai.proposed_action` row this draft was written as**, and the id `decideProposedAction` takes. Without it a reviewer (BO-598) has a draft and no way to approve it.\n"},"kind":{"type":"string","enum":["product","membership","pass","promotion","discountRule","pricingCalendar","seatingZone","operatingHours","campaign"],"description":"The `kind` the request asked for."},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"**Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, validated against that operation before it is returned — this contract does not restate thirty other contracts' request schemas.\n"},"assumptions":{"type":"array","description":"**What it had to guess.** An admin reviewing a draft needs to know which fields came from what they said and which the assistant chose, or they approve a decision they did not make.\n","items":{"type":"object","properties":{"field":{"type":"string"},"value":{"type":"string"},"reason":{"type":"string"}}}},"clarificationsNeeded":{"type":"array","description":"What it could not resolve and should ask about.","items":{"type":"string"}},"confidence":{"type":"number","nullable":true},"traceId":{"type":"string"},"planId":{"type":"string","format":"uuid","description":"The one-step `ai.action_plan` the draft was written as (AI design 2.3), readable with `getActionPlan`."}}},
"GuestMerchandiseItem": {"x-ticvai-persistence":"none — guest projection of MerchandiseItem","type":"object","description":"**What a guest caller of `listMerchandise` receives.** The fields a shop screen shows and the ids a guest needs to reserve or buy, and nothing else: no inventory link, no catalogue variant, no stock count, no serial-number flag. `additionalProperties: false` is the guarantee: a staff field added to `MerchandiseItem` does not reach a guest by default.\n","additionalProperties":false,"required":["id","name","outletId","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"sku":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isAvailable":{"type":"boolean","description":"True when the item is active and in stock at its outlet. An item with no `inventoryItemId` never runs out, so it is available while active.\n"},"isReturnable":{"type":"boolean"},"returnWindowDays":{"type":"integer","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}},
"Journey": {"type":"object","x-ticvai-persistence":"marketing.journey + marketing.journey_step","description":"22.3.1b to 22.3.10b, CF-137. **A journey is a sequence with branches; a `MessageTrigger` is one step of it.** The trigger already handles *\"send this when that happens\"* — a journey is what you need when the next message depends on what the guest did about the last one.\nFive of the ten requirements are named lifecycles — abandoned cart, membership, loyalty, wallet, birthday. **They are not five features.** Each is a journey with a different entry event and a different set of steps, which is why this is one entity and a template library rather than five contracts.\n**Consent is checked at every send, not at entry.** A guest who opts out mid-journey stops receiving, and the journey does not need to know — the same rule `MessageTrigger` follows and the one PDPL Article 17(1) makes unconditional.\n","required":["id","name","entryEvent","status","steps"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"templateKind":{"type":"string","nullable":true,"enum":["abandonedCart","membershipLifecycle","loyaltyLifecycle","walletLifecycle","birthday","onboarding","winBack","custom"],"description":"Which named lifecycle this implements. **Set for reporting and for the library**, not for behaviour — the steps decide what happens.\n"},"entryEvent":{"type":"string","description":"22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes.\n"},"entryConditions":{"type":"object","nullable":true,"description":"Narrows entry — a segment, a tier, a venue. **Evaluated once at entry**, unlike step conditions.\n"},"steps":{"type":"array","description":"22.3.1b. What the builder produces. **The visual builder is a frontend over this** — the contract holds the graph and the canvas is a rendering of it.\n","items":{"$ref":"#/components/schemas/JourneyStep"}},"status":{"readOnly":true,"type":"string","enum":["draft","active","paused","archived"]},"maxDurationDays":{"type":"integer","default":30,"description":"**A journey with no end is a guest who never leaves it.** After this, entrants exit wherever they are.\n"},"reentryPolicy":{"type":"string","enum":["never","afterCompletion","always"],"default":"afterCompletion","description":"22.3.6b. **Abandoned cart is the case that needs this.** A guest who abandons three carts in an hour should not get three recovery sequences, and `never` is wrong too — they may genuinely abandon one next month.\n"},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"JourneyStep": {"type":"object","description":"One node. **A step either sends, waits, or branches** — three kinds rather than a general graph, because a marketing user drawing an arbitrary graph draws a loop.\n","required":["id","kind"],"properties":{"id":{"type":"string"},"kind":{"type":"string","x-ticvai-column":"type","enum":["send","wait","branch","exit","goal"]},"templateId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-column":"message_template_id","description":"For `send`. Channel is resolved from the guest's preference at the moment of sending."},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours and inside `waitUntil`; no suggestion or AI off sends at once, as `fixed`."},"channelMode":{"type":"string","enum":["preference","optimised"],"default":"preference","description":"For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16)."},"channelPreference":{"type":"array","nullable":true,"description":"22.3.3b. Ordered fallback — email, then SMS, then push. **A guest with no email address does not get an email step**, and the step does not fail, it moves down the list.\n","items":{"type":"string","enum":["email","sms","whatsapp","push","inApp"]}},"waitMinutes":{"type":"integer","nullable":true},"waitUntil":{"type":"object","nullable":true,"description":"22.3.5b. **Business hours, time zone and blackout windows** — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are venue configuration rather than a property of this step.\n","properties":{"businessHoursOnly":{"type":"boolean","default":false},"timezone":{"type":"string","nullable":true},"respectQuietHours":{"type":"boolean","default":true},"notBefore":{"type":"string","nullable":true}}},"condition":{"type":"object","nullable":true,"description":"22.3.4b. IF/THEN over guest profile, behaviour and prior steps. **The most common condition is whether the previous message worked** — a recovery sequence must stop when the guest buys.\n","properties":{"field":{"type":"string"},"operator":{"type":"string","enum":["eq","neq","gt","lt","contains","exists","notExists"]},"value":{"type":"string","nullable":true}}},"onTrue":{"type":"string","nullable":true,"description":"Next step id."},"onFalse":{"type":"string","nullable":true},"next":{"type":"string","nullable":true,"x-ticvai-column":"next_journey_step_id"},"goalEvent":{"type":"string","nullable":true,"description":"For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MarketingCampaignVariant": {"type":"object","x-ticvai-persistence":"marketing.campaign_variant","description":"One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.","required":["label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"marketing.campaign"},"label":{"type":"string","maxLength":20,"description":"A, B, C..."},"subjectOverride":{"type":"object","nullable":true,"description":"Subject line by locale.","additionalProperties":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true,"description":"A different template for this variant; null uses the campaign's `content.templateId`."},"splitPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Share of the test group; null splits evenly."},"source":{"type":"string","enum":["manual","aiDraft"],"default":"manual"},"aiDecisionRecordId":{"type":"string","nullable":true,"description":"The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."},"isWinner":{"type":"boolean","default":false,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), the campaign's."}}},
"MerchandiseItem": {"x-ticvai-persistence":"retail.merchandise","type":"object","required":["id","sku","name","outletId","variantId","price","onHand","isActive"],"properties":{"description":{"type":"string","description":"What the item is, in the guest's words. Indexed for guest-app search.\n"},"id":{"type":"string","format":"uuid"},"sku":{"type":"string"},"barcode":{"type":"string","nullable":true},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true},"variantId":{"type":"string","format":"uuid","description":"The catalogue variant sold. Price and tax come from there."},"inventoryItemId":{"type":"string","format":"uuid","nullable":true,"description":"The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error.\n"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"list_price"},"onHand":{"type":"number"},"isReturnable":{"type":"boolean","default":true},"returnWindowDays":{"type":"integer","nullable":true},"requiresSerialNumber":{"type":"boolean","default":false},"imageAssetRef":{"type":"string","nullable":true},"isActive":{"type":"boolean"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceCheck": {"x-ticvai-persistence":"none — computed","type":"object","required":["merchandiseId","name","listPrice","effectivePrice","onHand"],"properties":{"merchandiseId":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid","description":"The outlet whose price and stock this is: the asking workstation's outlet, or `outletId` for a caller with none (decided 28 September, audit R215).\n"},"sku":{"type":"string"},"name":{"type":"string"},"listPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"effectivePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"After any live promotion."},"appliedPromotionCode":{"type":"string","nullable":true},"onHand":{"type":"number"},"isAvailable":{"type":"boolean"},"siblingOutlets":{"type":"array","description":"Stock elsewhere in the venue, so a colleague can be sent.","items":{"type":"object","properties":{"outletId":{"type":"string","format":"uuid"},"outletName":{"type":"string"},"onHand":{"type":"number"}}}}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"SaleBoard": {"x-ticvai-persistence":"platform.sale_board","type":"object","required":["id","code","name","venueId","kind","pages"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"pages":{"type":"array","minItems":1,"items":{"type":"object","required":["name","sortOrder","tiles"],"properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"tiles":{"type":"array","items":{"type":"object","required":["position","kind"],"properties":{"position":{"type":"integer"},"kind":{"type":"string","enum":["product","category","action","spacer"]},"variantId":{"type":"string","format":"uuid","nullable":true},"label":{"type":"string"},"colour":{"type":"string","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}}}}}},"isActive":{"type":"boolean"}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"Segment": {"x-ticvai-persistence":"marketing.segment + marketing.segment_criterion","allOf":[{"$ref":"#/components/schemas/CreateSegmentRequest"},{"type":"object","required":["id","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"lastEvaluatedSize":{"type":"integer","nullable":true},"lastEvaluatedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"SerialisedItem": {"type":"object","x-ticvai-persistence":"inventory.serialised_item","description":"Retail Board 4 of the client's design set, 20 August. **`StockBatch` was added on 18 August with a lot number, and serialisation to the individual item is a step beyond it.**\nA lot answers *which delivery did this come from*. A serial answers *where is this exact one* — which is what a jewellery counter, a phone, a ticketed collectible or anything with a warranty needs.\n**Most stock is not serialised and should not be.** Turning it on for a 2 AED keyring creates a row per keyring, so it is a per-item decision rather than a policy.\n","required":["id","itemId","serial","status"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"description":"The batch it arrived in, where the item is both lotted and serialised."},"serial":{"type":"string","description":"**Unique within the item, not globally.** Two manufacturers reuse serial numbers and a global constraint would refuse the second one.\n"},"locationId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["inStock","reserved","sold","returned","damaged","lost","inTransit","warranty"]},"soldOnOrderLineId":{"type":"string","format":"uuid","nullable":true,"description":"**The link that makes serialisation worth having.** A warranty claim, a recall and a proof of purchase all start with *which sale was this exact item*.\n"},"warrantyUntil":{"type":"string","format":"date","nullable":true},"receivedAt":{"type":"string","format":"date-time"}}},
"UpsellPlacement": {"type":"string","enum":["productDetail","cart","checkout","postPurchase","atGate","inVenue"]},
"UpsellRule": {"x-ticvai-persistence":"promotions.upsell_rule","type":"object","required":["id","name","placement","triggerVariantIds","suggestedVariantIds"],"properties":{"id":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid","readOnly":true,"description":"The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's region scope on create.\n"},"name":{"type":"string","maxLength":200},"placement":{"$ref":"#/components/schemas/UpsellPlacement"},"triggerVariantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"triggerCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"suggestedVariantIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"suggestedBundleId":{"type":"string","format":"uuid","nullable":true},"channels":{"type":"array","description":"Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience inconsistency.\n","items":{"type":"string"}},"priority":{"type":"integer","default":0},"maxSuggestions":{"type":"integer","default":3},"isActive":{"type":"boolean"}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
