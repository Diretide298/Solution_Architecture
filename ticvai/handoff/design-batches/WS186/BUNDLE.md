# WS186 — Wallet Configuration Backend Structure v1.0 board 1

**10 screens · 13 operations · 9 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-1083` | Wallet Command Center | B–D | 26 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1084` | Wallet Type Library | B–D | 30 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1085` | Wallet Creation & Provisioning Rules | B–D | 17 | 20 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1086` | Wallet Ownership & Account Association | B–D | 6 | 0 | 6 | 16 | 1 | 6 | — | notStarted (—) |
| `BO-1087` | Wallet Currency & Monetary Configuration | B–D | 16 | 20 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1088` | Credit & Balance Type Configuration | B–D | 30 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1089` | Wallet Feature Profile | B–D | 0 | 20 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1090` | Wallet Lifecycle Configuration | B–D | 11 | 20 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1091` | Wallet Numbering, Identity & Digital Credentials | B–D | 17 | 20 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1092` | Wallet Configuration Preview, Validation & Publication | B–D | 18 | 10 | 6 | 0 | 1 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-1089 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1083` Wallet Command Center

**Provide administrators with the central operational and configuration overview of all wallet products across the TICVAI platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-command-center-bo-1083` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The overview of wallet products: wallet types and the outstanding liability and breakage the finance director asks for.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listWalletTypes, getWalletLiability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getWalletLiability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listWalletTypes / contracts/satellite/wallet.yaml#getWalletLiability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Active | select field | — | — | — | — | — | — |
| Pending Activation | select field | — | — | — | — | — | — |
| Suspended | select field | — | — | — | — | — | — |
| Blocked | select field | — | — | — | — | — | — |
| Expired | select field | — | — | — | — | — | — |
| Closed | select field | — | — | — | — | — | — |
| Cash value | select field | — | — | — | — | — | — |
| Bonus value | select field | — | — | — | — | — | — |
| Gift card value | select field | — | — | — | — | — | — |
| Promotional credits | select field | — | — | — | — | — | — |
| Ride credits | select field | — | — | — | — | — | — |
| Redemption credits | select field | — | — | — | — | — | — |
| Membership credits | select field | — | — | — | — | — | — |
| Top-ups | select field | — | — | — | — | — | — |
| Spending | select field | — | — | — | — | — | — |
| Refunds | select field | — | — | — | — | — | — |
| Transfers | select field | — | — | — | — | — | — |
| Adjustments | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Customer type | select field | — | — | — | — | — | — |
| Wallet status | select field | — | — | — | — | — | — |
| Balance range | select field | — | — | — | — | — | — |
| Date range | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **liability**: Outstanding by credit type, breakage recognised this period. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*

**Data it reads**: `listWalletTypes` (onLoad, Wallet types in use); `getWalletLiability` (onLoad, What is outstanding)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1084` Wallet Type Library: *Wallet Type Library*
- → `BO-1085` Wallet Creation & Provisioning Rules: *Wallet Creation & Provisioning Rules*; carries `walletTypeId`
- → `BO-1086` Wallet Ownership & Account Association: *Wallet Ownership & Account Association*; carries `walletTypeId`
- → `BO-1087` Wallet Currency & Monetary Configuration: *Wallet Currency & Monetary Configuration*; carries `walletTypeId`
- → `BO-1088` Credit & Balance Type Configuration: *Credit & Balance Type Configuration*
- → `BO-1089` Wallet Feature Profile: *Wallet Feature Profile*; carries `walletTypeId`
- → `BO-1090` Wallet Lifecycle Configuration: *Wallet Lifecycle Configuration*; carries `walletTypeId`
- → `BO-1091` Wallet Numbering, Identity & Digital Credentials: *Wallet Numbering, Identity & Digital Credentials*; carries `walletTypeId`
- → `BO-1092` Wallet Configuration Preview, Validation & Publication: *Wallet Configuration Preview, Validation & Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
liability:
  outstanding: AED 2,184,300.00
  breakageThisMonth: AED 41,320.00
```

#### Permissions

- `listWalletTypes` → `WALLET_VIEW` (read) · staff
- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet dashboard gives an overview of all live wallet balances: total wallet value, total spend and total recharge activity. *(client request · MoM 27 Aug 2026, 4.1 Wallet Foundation & Dashboard · DI-507)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1083` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1083`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 1: Opens Wallet Command Center → Provide administrators with the central operational and configuration overview of all wallet products across the TICVAI platform.
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F293 branch at step 1 (expected): when Nothing has been set up on Wallet Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F293 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1083?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1084`, `BO-1085`, `BO-1086`, `BO-1087`, `BO-1088`, `BO-1089`, `BO-1090`, `BO-1091`, `BO-1092`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1084` Wallet Type Library

**Create and maintain reusable wallet types used throughout TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration; Each wallet type can configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-type-library-bo-1084` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Reusable wallet types: guest, registered, family, parent, child, corporate, school, employee.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listWalletTypes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listWalletTypes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Guest Wallet | select field | — | — | — | — | — | — |
| Registered Customer Wallet | select field | — | — | — | — | — | — |
| Family Wallet | select field | — | — | — | — | — | — |
| Parent Wallet | select field | — | — | — | — | — | — |
| Child Wallet | select field | — | — | — | — | — | — |
| Corporate Wallet | select field | — | — | — | — | — | — |
| School Wallet | select field | — | — | — | — | — | — |
| Employee Wallet | select field | — | — | — | — | — | — |
| Membership Wallet | select field | — | — | — | — | — | — |
| Event Wallet | select field | — | — | — | — | — | — |
| Resort Wallet | select field | — | — | — | — | — | — |
| Cashless Venue Wallet | select field | — | — | — | — | — | — |
| Closed-Loop Wallet | select field | — | — | — | — | — | — |
| Wallet name | select field | — | — | — | — | — | — |
| Internal wallet code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Wallet category | select field | — | — | — | — | — | — |
| Owning tenant | select field | — | — | — | — | — | — |
| Applicable venue | select field | — | — | — | — | — | — |
| Supported customer/account type | select field | — | — | — | — | — | — |
| Supported currencies | select field | — | — | — | — | — | — |
| Stored-value capability | select field | — | — | — | — | — | — |
| Transfer capability | select field | — | — | — | — | — | — |
| Top-up capability | select field | — | — | — | — | — | — |
| Refund capability | select field | — | — | — | — | — | — |
| Gift card support | select field | — | — | — | — | — | — |
| Voucher support | select field | — | — | — | — | — | — |
| Membership credit support | select field | — | — | — | — | — | — |
| Wearable support | select field | — | — | — | — | — | — |
| Online usage | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **wallet type**: Category decides ownership and access rules. *(source: contracts/satellite/wallet.yaml#createWalletType / TRACKER Actions row 102)*

#### Outputs: what the screen shows and produces

**Data it reads**: `listWalletTypes` (onLoad, The type library)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
type:
  name: Dune Park Family Wallet
  category: family
  currency: AED
```

#### Permissions

- `listWalletTypes` → `WALLET_VIEW` (read) · staff
- `createWalletType` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1084` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1084`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 2: Works in Wallet Type Library → Create and maintain reusable wallet types used throughout TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1084?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1085` Wallet Creation & Provisioning Rules

**Define how and when TICVAI automatically or manually creates a wallet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `walletTypeId` (navigation) |
| Route | `/orders-money/wallet-creation-provisioning-rules-bo-1085` |

**Known gaps.** **Wallet Creation & Provisioning Rules declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When a wallet is created automatically (at registration, first top-up, membership) or manually.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createWalletType, updateWalletType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Automatic vs manual creation | text field | — | — | — | — | — | — |
| Required customer information | select field | — | — | — | — | — | — |
| Anonymous wallet permission | select field | — | — | — | — | — | — |
| Account verification requirement | select field | — | — | — | — | — | — |
| Mobile verification | select field | — | — | — | — | — | — |
| Email verification | select field | — | — | — | — | — | — |
| Digital ID verification | select field | — | — | — | — | — | — |
| Default wallet type | select field | — | — | — | — | — | — |
| Default currency | select field | — | — | — | — | — | — |
| Default status | select field | — | — | — | — | — | — |
| Initial credit | select field | — | — | — | — | — | — |
| Initial promotional value | select field | — | — | — | — | — | — |
| Wallet validity | select field | — | — | — | — | — | — |
| Wallet activation rules | select field | — | — | — | — | — | — |
| Duplicate-wallet handling | select field | — | — | — | — | — | — |
| One wallet per customer vs multiple wallets | text field | — | — | — | — | — | — |
| Maximum wallets per account | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **provisioning triggers**: Triggers as checkboxes per wallet type. *(source: contracts/satellite/wallet.yaml#updateWalletType)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of wallet that may exist — who owns one** (data table, from `listWalletTypes`)

| Shows | Format | Notes |
|---|---|---|
| Auto reload allowed | yes / no (icon or chip) | Auto-reload is optional per wallet type (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Owner kind | chip: Guest, Registered customer, Family, Parent, Child, Corporate… | — |
| Stored value capability | yes / no (icon or chip) | Board 1.2. Whether this wallet holds a balance at all. |
| Top up capability | yes / no (icon or chip) | — |
| Transfer capability | yes / no (icon or chip) | — |
| Refund capability | yes / no (icon or chip) | — |
| Gift card support | yes / no (icon or chip) | — |
| Voucher support | yes / no (icon or chip) | — |
| Membership credit support | yes / no (icon or chip) | — |
| Wearable support | yes / no (icon or chip) | — |
| Usage channels | list or chips (count when long) | Where this wallet may be used, declared on the type itself. Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and … |
| Preset name | text | The client's own name for this composition — "Resort Wallet", "Cashless Venue Wallet", "Closed-Loop Wallet". |
| Holder may differ from owner | yes / no (icon or chip) | A child wallet's owner is the parent. Without this the model has to pretend a seven-year-old holds an account. |
| Requires identification | yes / no (icon or chip) | — |
| Maximum balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed credit types | list or chips (count when long) | — |
| Allow negative balance | yes / no (icon or chip) | — |

**Data it reads**: `listWalletTypes` (onLoad, The kinds of wallet that may exist — who owns one)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet creation provisioning configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet creation provisioning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet creation provisioning configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Live wallets exist that the change would invalidate |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
triggers:
- on registration
- on first wristband issue
```

#### Permissions

- `createWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `updateWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1085` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1085`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 4: Works in Wallet Creation & Provisioning Rules → Define how and when TICVAI automatically or manually creates a wallet.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1085?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1086` Wallet Ownership & Account Association

**Configure which customer, family or organization owns and controls a wallet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure roles such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `subjectId` (navigation), `walletTypeId` (navigation), `sharedWalletId` (navigation) |
| Route | `/orders-money/wallet-ownership-account-association-bo-1086` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Who owns and controls a wallet: individual, family, organisation; members and their allowances.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSharedWallets return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listSharedWallets; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet Owner | select field | — | — | — | — | — | — |
| Wallet Administrator | select field | — | — | — | — | — | — |
| Authorized User | select field | — | — | — | — | — | — |
| Dependant | select field | — | — | — | — | — | — |
| Viewer | select field | — | — | — | — | — | — |
| Finance Controller | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View balance, Top up, Spend, Transfer, Receive transfer, View transactions, Add payment instruments, Add/remove wearables, Configure spending limits, Freeze wallet, Receive notifications. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| One wallet → multiple users (primary button) | navigation or local | — | — | — | — |
| Primary wallet owner (secondary button) | navigation or local | — | — | — | — |
| Delegated wallet administration (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **structure**: Owner and members as a tree with each member's allowance. *(source: contracts/satellite/wallet.yaml#listSharedWallets / contracts/satellite/wallet.yaml#setSharedWalletMembers)*

**Data it reads**: `listSharedWallets` (onLoad, The shared wallets whose members are set)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet ownership account configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet ownership account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet ownership account configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Live wallets exist that the change would invalidate |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
family:
  owner: Fatima Al Nuaimi
  members:
  - name: Ali (9)
    allowance: AED 50.00 a day
```

#### Permissions

- `getWallet` → `WALLET_VIEW` (read) · staff, guest
- `updateWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| 4.3.7 | The system should allow guests to use their digital wallet to make online and in-app purchases (through API integrations), buy tickets of all type or purchase any service within venue such as retail … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.8 | The system should provide a digital wallet that allows: - multiple channels for payments, including but not limited to the Mobile app and wearable (which is linked to the digital wallet). - multiple … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.13 | The system should allow guests to make in-store and attraction payments using digital wallets via contactless methods as RFID, NFC and QR-code. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.20 | The system should enable usage of wallet by other systems through integration. All functionalities of the wallet such as credit redemption, balance check and wallet funding should be available … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.22 | Support cashless stored-value balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.23 | Support gift card balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1086` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1086`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 6: Works in Wallet Ownership & Account Association → Configure which customer, family or organization owns and controls a wallet.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1086?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: One wallet → multiple users, Primary wallet owner, Delegated wallet administration.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1087` Wallet Currency & Monetary Configuration

**Define currencies and monetary rules applicable to wallet balances.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `walletTypeId` (navigation) |
| Route | `/orders-money/wallet-currency-monetary-configuration-bo-1087` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Currencies and monetary rules of wallet balances: supported currencies, maximum balance, FX-converted top-up.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateWalletType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Base wallet currency | select field | — | — | — | — | — | — |
| Permitted currencies | select field | — | — | — | — | — | — |
| Multi-currency wallet enabled/disabled | select field | — | — | — | — | — | — |
| Venue currency | select field | — | — | — | — | — | — |
| Settlement currency | select field | — | — | — | — | — | — |
| Currency conversion permitted | select field | — | — | — | — | — | — |
| Exchange-rate source | select field | — | — | — | — | — | — |
| Conversion timing | select field | — | — | — | — | — | — |
| Exchange-rate markup | select field | — | — | — | — | — | — |
| Decimal precision | select field | — | — | — | — | — | — |
| Minimum wallet balance | select field | — | — | — | — | — | — |
| Maximum wallet balance | select field | — | — | — | — | — | — |
| Negative balance permission | select field | — | — | — | — | — | — |
| Zero-balance behavior | select field | — | — | — | — | — | — |
| Currency-specific limits | select field | — | — | — | — | — | — |
| Rounding policy | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **currencies**: Base currency from the region (PR-2); foreign top-up converted at the stored rate and shown both ways. *(source: contracts/satellite/wallet.yaml#updateWalletType / ADR-0018 / TRACKER Actions row 104)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of wallet that may exist — who owns one** (data table, from `listWalletTypes`)

| Shows | Format | Notes |
|---|---|---|
| Auto reload allowed | yes / no (icon or chip) | Auto-reload is optional per wallet type (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Owner kind | chip: Guest, Registered customer, Family, Parent, Child, Corporate… | — |
| Stored value capability | yes / no (icon or chip) | Board 1.2. Whether this wallet holds a balance at all. |
| Top up capability | yes / no (icon or chip) | — |
| Transfer capability | yes / no (icon or chip) | — |
| Refund capability | yes / no (icon or chip) | — |
| Gift card support | yes / no (icon or chip) | — |
| Voucher support | yes / no (icon or chip) | — |
| Membership credit support | yes / no (icon or chip) | — |
| Wearable support | yes / no (icon or chip) | — |
| Usage channels | list or chips (count when long) | Where this wallet may be used, declared on the type itself. Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and … |
| Preset name | text | The client's own name for this composition — "Resort Wallet", "Cashless Venue Wallet", "Closed-Loop Wallet". |
| Holder may differ from owner | yes / no (icon or chip) | A child wallet's owner is the parent. Without this the model has to pretend a seven-year-old holds an account. |
| Requires identification | yes / no (icon or chip) | — |
| Maximum balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed credit types | list or chips (count when long) | — |
| Allow negative balance | yes / no (icon or chip) | — |

**Data it reads**: `listWalletTypes` (onLoad, The kinds of wallet that may exist — who owns one)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet currency monetary configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet currency monetary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet currency monetary configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Live wallets exist that the change would invalidate |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
wallet:
  base: AED
  maxBalance: AED 5,000.00
  foreignTopUp: USD at feed rate + 2%
```

#### Permissions

- `updateWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Currency config sets supported currencies and maximum balance; foreign-currency top-up (e.g. USD) is converted at a configured exchange rate and credited in local currency. Credit types (cash, bonus, gift-card credit) are each classified monetary or non-monetary (e.g. a meal voucher redeemable only for a specific item). *(client request · MoM 27 Aug 2026, 4.3 Currency, Credit Types & Wallet Feature Profile · DI-510)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1087` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1087`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 8: Works in Wallet Currency & Monetary Configuration → Define currencies and monetary rules applicable to wallet balances.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1087?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1088` Credit & Balance Type Configuration

**Configure all value types that may be stored inside a TICVAI wallet. The attached requirements explicitly call for multiple wallet credit types including Cash Credit, Bonus Credit, Redemption Tickets Credit and Rides Credit.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators can define; For each balance type configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/orders-money/credit-balance-type-configuration-bo-1088` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** All value types a wallet may hold (cash, bonus, redemption tickets, gift, refund, promotional), monetary or not.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCreditTypes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listCreditTypes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Cash Credit | select field | — | — | — | — | — | — |
| Refund Credit | select field | — | — | — | — | — | — |
| Bonus Credit | select field | — | — | — | — | — | — |
| Promotional Credit | select field | — | — | — | — | — | — |
| Gift Card Credit | select field | — | — | — | — | — | — |
| Membership Credit | select field | — | — | — | — | — | — |
| Loyalty Credit | select field | — | — | — | — | — | — |
| Ride Credit | select field | — | — | — | — | — | — |
| Attraction Credit | select field | — | — | — | — | — | — |
| Redemption Ticket Credit | select field | — | — | — | — | — | — |
| Meal Credit | select field | — | — | — | — | — | — |
| Retail Credit | select field | — | — | — | — | — | — |
| Parking Credit | select field | — | — | — | — | — | — |
| Event Credit | select field | — | — | — | — | — | — |
| Custom Credit Type | select field | — | — | — | — | — | — |
| Balance code | select field | — | — | — | — | — | — |
| Display name | select field | — | — | — | — | — | — |
| Monetary/non-monetary | select field | — | — | — | — | — | — |
| Currency applicable | select field | — | — | — | — | — | — |
| Transferable | select field | — | — | — | — | — | — |
| Refundable | select field | — | — | — | — | — | — |
| Top-up allowed | select field | — | — | — | — | — | — |
| Promotional | select field | — | — | — | — | — | — |
| Expirable | select field | — | — | — | — | — | — |
| Redeemable channels | select field | — | — | — | — | — | — |
| Applicable products | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Accounting classification | select field | — | — | — | — | — | — |
| Liability classification | select field | — | — | — | — | — | — |
| Consumption priority | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listCreditTypes` (onLoad, The credit type library)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credit balance type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credit balance type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credit balance type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-415`: Same record and editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
type:
  name: Refund credit
  monetary: true
  refundable: true
```

#### Permissions

- `listCreditTypes` → `WALLET_VIEW` (read) · staff
- `createCreditType` → `WALLET_CONFIGURE` (configure) · staff
- `updateCreditType` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Currency config sets supported currencies and maximum balance; foreign-currency top-up (e.g. USD) is converted at a configured exchange rate and credited in local currency. Credit types (cash, bonus, gift-card credit) are each classified monetary or non-monetary (e.g. a meal voucher redeemable only for a specific item). *(client request · MoM 27 Aug 2026, 4.3 Currency, Credit Types & Wallet Feature Profile · DI-510)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1088` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1088`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 10: Works in Credit & Balance Type Configuration → Configure all value types that may be stored inside a TICVAI wallet. The attached requirements explicitly call for multiple wallet credit types including Cash Credit, Bonus Credit, Redemption Tickets …

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1088?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1089` Wallet Feature Profile

**Control which capabilities are available for each wallet type.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `walletTypeId` (navigation) |
| Route | `/orders-money/wallet-feature-profile-bo-1089` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which capabilities each wallet type has (top-up, transfer, unload, P2P, auto-reload).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateWalletType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **feature profile**: Switches per capability; transfers and unload are venue toggles, off by default. *(source: contracts/satellite/wallet.yaml#updateWalletType / DI-535 / TRACKER Actions row 115)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of wallet that may exist — who owns one** (data table, from `listWalletTypes`)

| Shows | Format | Notes |
|---|---|---|
| Auto reload allowed | yes / no (icon or chip) | Auto-reload is optional per wallet type (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Owner kind | chip: Guest, Registered customer, Family, Parent, Child, Corporate… | — |
| Stored value capability | yes / no (icon or chip) | Board 1.2. Whether this wallet holds a balance at all. |
| Top up capability | yes / no (icon or chip) | — |
| Transfer capability | yes / no (icon or chip) | — |
| Refund capability | yes / no (icon or chip) | — |
| Gift card support | yes / no (icon or chip) | — |
| Voucher support | yes / no (icon or chip) | — |
| Membership credit support | yes / no (icon or chip) | — |
| Wearable support | yes / no (icon or chip) | — |
| Usage channels | list or chips (count when long) | Where this wallet may be used, declared on the type itself. Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and … |
| Preset name | text | The client's own name for this composition — "Resort Wallet", "Cashless Venue Wallet", "Closed-Loop Wallet". |
| Holder may differ from owner | yes / no (icon or chip) | A child wallet's owner is the parent. Without this the model has to pretend a seven-year-old holds an account. |
| Requires identification | yes / no (icon or chip) | — |
| Maximum balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed credit types | list or chips (count when long) | — |
| Allow negative balance | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save wallet type (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listWalletTypes` (onLoad, The kinds of wallet that may exist — who owns one)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet feature profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet feature profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet feature profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet feature profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Live wallets exist that the change would invalidate |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  topUp: true
  p2p: false
  unloadAtExit: true
```

#### Permissions

- `updateWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet feature profile (global, optionally per wallet type) lists permitted actions such as top-up allowed, refund allowed. Example: a AED 100 membership-benefit voucher is spendable but not refundable/cashable-out. *(client request · MoM 27 Aug 2026, 4.3 Wallet Feature Profile · DI-511)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1089` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1089`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 12: Works in Wallet Feature Profile → Control which capabilities are available for each wallet type.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1089?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save wallet type, Cancel.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1090` Wallet Lifecycle Configuration

**Govern the complete wallet lifecycle from creation through closure.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `walletTypeId` (navigation) |
| Route | `/orders-money/wallet-lifecycle-configuration-bo-1090` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet lifecycle: active, suspended, blocked, closed; mandatory validity with the residual balance swept to a finance account.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateWalletType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Activation conditions | select field | — | — | — | — | — | — |
| Verification requirements | select field | — | — | — | — | — | — |
| Suspension reasons | select field | — | — | — | — | — | — |
| Block reasons | select field | — | — | — | — | — | — |
| Expiry behavior | select field | — | — | — | — | — | — |
| Dormancy rules | select field | — | — | — | — | — | — |
| Closure requirements | select field | — | — | — | — | — | — |
| Remaining balance handling | select field | — | — | — | — | — | — |
| Reactivation rules | select field | — | — | — | — | — | — |
| Archival period | select field | — | — | — | — | — | — |
| Data retention period | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **validity and sweep**: Validity required; sweep account picked from the chart of accounts. *(source: contracts/satellite/wallet.yaml#updateWalletType / TRACKER Actions row 106)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of wallet that may exist — who owns one** (data table, from `listWalletTypes`)

| Shows | Format | Notes |
|---|---|---|
| Auto reload allowed | yes / no (icon or chip) | Auto-reload is optional per wallet type (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Owner kind | chip: Guest, Registered customer, Family, Parent, Child, Corporate… | — |
| Stored value capability | yes / no (icon or chip) | Board 1.2. Whether this wallet holds a balance at all. |
| Top up capability | yes / no (icon or chip) | — |
| Transfer capability | yes / no (icon or chip) | — |
| Refund capability | yes / no (icon or chip) | — |
| Gift card support | yes / no (icon or chip) | — |
| Voucher support | yes / no (icon or chip) | — |
| Membership credit support | yes / no (icon or chip) | — |
| Wearable support | yes / no (icon or chip) | — |
| Usage channels | list or chips (count when long) | Where this wallet may be used, declared on the type itself. Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and … |
| Preset name | text | The client's own name for this composition — "Resort Wallet", "Cashless Venue Wallet", "Closed-Loop Wallet". |
| Holder may differ from owner | yes / no (icon or chip) | A child wallet's owner is the parent. Without this the model has to pretend a seven-year-old holds an account. |
| Requires identification | yes / no (icon or chip) | — |
| Maximum balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed credit types | list or chips (count when long) | — |
| Allow negative balance | yes / no (icon or chip) | — |

**Data it reads**: `listWalletTypes` (onLoad, The kinds of wallet that may exist — who owns one)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet lifecycle configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet lifecycle configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Live wallets exist that the change would invalidate |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
lifecycle:
  validity: 24 months of inactivity
  sweepTo: Breakage income 4810
```

#### Permissions

- `updateWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet statuses: active, suspended, blocked, closed. Every wallet must have a validity period (never open-ended); on lapse the remaining balance, monetary or non-monetary, is automatically swept to a finance-designated account. *(agreed · MoM 27 Aug 2026, 4.4 Wallet Lifecycle, Numbering & Publish Flow · DI-512)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1090` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1090`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 14: Works in Wallet Lifecycle Configuration → Govern the complete wallet lifecycle from creation through closure.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1090?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1091` Wallet Numbering, Identity & Digital Credentials

**Configure how wallets are uniquely identified across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `walletTypeId` (navigation) |
| Route | `/orders-money/wallet-numbering-identity-digital-credentials-bo-1091` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How wallets are identified (wallet code format) and which credentials (wristband, card, device) bind to them; a credential is not the wallet.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateWalletType, linkWalletCredential and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet ID structure | select field | — | — | — | — | — | — |
| Wallet number format | select field | — | — | — | — | — | — |
| Prefix/suffix | select field | — | — | — | — | — | — |
| Tenant code | select field | — | — | — | — | — | — |
| Venue code | select field | — | — | — | — | — | — |
| Sequential/random identifier | select field | — | — | — | — | — | — |
| Customer-facing wallet reference | select field | — | — | — | — | — | — |
| QR identifier | select field | — | — | — | — | — | — |
| NFC identifier | select field | — | — | — | — | — | — |
| RFID identifier | select field | — | — | — | — | — | — |
| Wearable token | select field | — | — | — | — | — | — |
| Mobile credential | select field | — | — | — | — | — | — |
| Digital Key / Digital ID | text field | — | — | — | — | — | — |
| Tokenization | select field | — | — | — | — | — | — |
| Credential expiry | select field | — | — | — | — | — | — |
| Credential replacement | select field | — | — | — | — | — | — |
| Lost/stolen credential handling | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of wallet that may exist — who owns one** (data table, from `listWalletTypes`)

| Shows | Format | Notes |
|---|---|---|
| Auto reload allowed | yes / no (icon or chip) | Auto-reload is optional per wallet type (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Owner kind | chip: Guest, Registered customer, Family, Parent, Child, Corporate… | — |
| Stored value capability | yes / no (icon or chip) | Board 1.2. Whether this wallet holds a balance at all. |
| Top up capability | yes / no (icon or chip) | — |
| Transfer capability | yes / no (icon or chip) | — |
| Refund capability | yes / no (icon or chip) | — |
| Gift card support | yes / no (icon or chip) | — |
| Voucher support | yes / no (icon or chip) | — |
| Membership credit support | yes / no (icon or chip) | — |
| Wearable support | yes / no (icon or chip) | — |
| Usage channels | list or chips (count when long) | Where this wallet may be used, declared on the type itself. Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and … |
| Preset name | text | The client's own name for this composition — "Resort Wallet", "Cashless Venue Wallet", "Closed-Loop Wallet". |
| Holder may differ from owner | yes / no (icon or chip) | A child wallet's owner is the parent. Without this the model has to pretend a seven-year-old holds an account. |
| Requires identification | yes / no (icon or chip) | — |
| Maximum balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed credit types | list or chips (count when long) | — |
| Allow negative balance | yes / no (icon or chip) | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Link credential**: Binds a wristband, card or device; a lost one is unlinked, the wallet stays. *(source: contracts/satellite/wallet.yaml#linkWalletCredential)*

**Data it reads**: `listWalletTypes` (onLoad, The kinds of wallet that may exist — who owns one)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet numbering identity configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet numbering identity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet numbering identity configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already bound to another wallet; 409 Live wallets exist that the change would invalidate |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
wallet:
  code: DW-0011-7741
  credentials:
  - Wristband WB-0098812
```

#### Permissions

- `updateWalletType` → `WALLET_CONFIGURE` (configure) · staff
- `linkWalletCredential` → `WALLET_OPERATE` (operate) · staff
- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each wallet gets a unique wallet code (like a ticket number) with configurable association to physical/digital media: QR code, RFID/wristband or other media types, usable across channels. *(client request · MoM 27 Aug 2026, 4.4 Wallet Numbering / 4.9 Wallet-to-media linking · DI-513)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1091` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1091`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 16: Works in Wallet Numbering, Identity & Digital Credentials → Configure how wallets are uniquely identified across TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1091?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1092` Wallet Configuration Preview, Validation & Publication

**Provide a governed final validation step before wallet configuration becomes operational. Configure how value enters a TICVAI wallet across digital and physical channels, including manual top-ups, payment-method funding, automatic reload, recurring funding, authorization controls, reversals, limits, and operational monitoring. This board directly covers the wallet requirements for multiple funding methods, auto-reload, recurring funding, configurable limits, security controls, and complete transaction auditing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Show configuration summary covering; Every configuration publication records) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-configuration-preview-validation-publication-bo-1092` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The final validation and publication of wallet configuration as a version.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only publishWalletConfiguration and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet type | select field | — | — | — | — | — | — |
| Ownership model | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Credit types | select field | — | — | — | — | — | — |
| Features | select field | — | — | — | — | — | — |
| Lifecycle | select field | — | — | — | — | — | — |
| Credentials | select field | — | — | — | — | — | — |
| Financial configuration | select field | — | — | — | — | — | — |
| Security profile | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Applicable channels | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Old value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Wallet configuration versions, newest first** (data table, from `listWalletConfigurationVersions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Note | text | — |
| Findings | list or chips (count when long) | — |
| Severity | chip: Blocking, Warning | — |
| Code | text | — |
| Message | text | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Publish**: Findings first (a credit type with no accounting mapping, a policy naming a retired type); publishes a version. *(source: contracts/satellite/wallet.yaml#publishWalletConfiguration)*

**Data it reads**: `listWalletConfigurationVersions` (onLoad, Wallet configuration versions, newest first)

**Where the user goes next**

- → `BO-1083` Wallet Command Center: *Back to Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet preview validation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet preview validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet preview validation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-1162`: Same versions and diff.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
publish:
  version: 15
  findings: 0 errors, 2 warnings
```

#### Permissions

- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff
- `listWalletConfigurationVersions` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A final review/publish screen summarises the completed wallet-type configuration (rules, applicable channels) before it goes live. *(client request · MoM 27 Aug 2026, 4.4 Wallet Lifecycle, Numbering & Publish Flow · DI-514)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1092` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1092`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 1
- Flow F293 *Wallet Configuration Backend Structure v1.0 board 1: Wallet Command Center*, step 18: Works in Wallet Configuration Preview, Validation & Publication → Provide a governed final validation step before wallet configuration becomes operational.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1092?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `BO-1083`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createCreditType": {"method":"POST","path":"/credit-types","contract":"wallet","summary":"Define a kind of credit, without a release","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreditType","responds":"CreditType"},
"createWalletType": {"method":"POST","path":"/wallet-types","contract":"wallet","summary":"Define a kind of wallet","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletType","responds":"WalletType"},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"getWalletLiability": {"method":"GET","path":"/wallet-liability","contract":"wallet","summary":"What is outstanding, and what is breakage","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"asOf","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletLiabilityRow"},
"linkWalletCredential": {"method":"POST","path":"/wallet-credentials","contract":"wallet","summary":"Bind a wristband, card or device to a wallet","permission":"WALLET_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletCredential","responds":"WalletCredential"},
"listCreditTypes": {"method":"GET","path":"/credit-types","contract":"wallet","summary":"The kinds of value that may sit in a wallet","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CreditType"},
"listSharedWallets": {"method":"GET","path":"/shared-wallets","contract":"wallet","summary":"Family, household and corporate structures","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"SharedWallet"},
"listWalletConfigurationVersions": {"method":"GET","path":"/wallet-configuration/versions","contract":"wallet","summary":"Wallet configuration versions, newest first","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletTypes": {"method":"GET","path":"/wallet-types","contract":"wallet","summary":"The kinds of wallet that may exist — who owns one","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WalletType"},
"publishWalletConfiguration": {"method":"POST","path":"/wallet-configuration/publish","contract":"wallet","summary":"Validate and publish the wallet configuration as a version","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletConfigurationVersion"},
"setSharedWalletMembers": {"method":"PUT","path":"/shared-wallets/{sharedWalletId}/members","contract":"wallet","summary":"Allowances, budgets and what each member may spend on","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SharedWalletMember"},
"updateCreditType": {"method":"PUT","path":"/credit-types/{creditTypeId}","contract":"wallet","summary":"Change a kind of credit","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreditType","responds":"CreditType"},
"updateWalletType": {"method":"PUT","path":"/wallet-types/{walletTypeId}","contract":"wallet","summary":"Change a kind of wallet","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletType","responds":"WalletType"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreditType": {"type":"object","x-ticvai-persistence":"wallet.credit_type","description":"Board 1.6. **What value sits inside a wallet** — the second vocabulary, and the one the acceptance condition requires to be a table.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"category":{"type":"string","enum":["cash","refund","bonus","promotional","giftCard","membership","loyalty","ride","attraction","redemption","fnb","retail","parking","event","other"]},"monetary":{"type":"boolean","default":true,"description":"**Loyalty points are not money.** A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency puts them on the balance sheet.\n"},"conversionRate":{"type":"number","nullable":true},"refundable":{"type":"boolean","default":false,"description":"**Promotional credit is not refundable and cash credit is.** A venue that refunds promotional credit to a card has converted marketing spend into cash.\n"},"transferable":{"type":"boolean","default":false},"expires":{"type":"boolean","default":false},"validityDays":{"type":"integer","nullable":true},"breakageEligible":{"type":"boolean","default":false},"ledgerAccountCode":{"type":"string","nullable":true},"priority":{"type":"integer","default":0},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SharedWallet": {"type":"object","x-ticvai-persistence":"wallet.shared_wallet","description":"Board 4. **One pot, distributed authority.**","required":["kind","walletId"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["family","household","corporate","school","group"]},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"members":{"type":"array","items":{"$ref":"#/components/schemas/SharedWalletMember"}},"totalBudget":{"x-ticvai-column":"budget_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"approvalAboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"SharedWalletMember": {"type":"object","x-ticvai-persistence":"wallet.shared_wallet_member","description":"Boards 4.5 and 4.6. **An allowance is a cap with a refresh, not a transfer.**","required":["subjectId"],"properties":{"subjectId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["owner","administrator","spender","viewer"]},"allowanceAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowanceCadence":{"type":"string","enum":["daily","weekly","monthly","none"],"default":"none"},"spendCapPerTransaction":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"blockedCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"activeFrom":{"type":"string","format":"date","nullable":true},"activeTo":{"type":"string","format":"date","nullable":true}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletConfigurationVersion": {"type":"object","x-ticvai-persistence":"wallet.configuration_version","description":"Boards 1.10 and 10.8. **Ten boards of configuration that interact.**","properties":{"version":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedBy":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"code":{"type":"string"},"message":{"type":"string"}}}},"scopePath":{"type":"string"}}},
"WalletCredential": {"type":"object","x-ticvai-persistence":"wallet.credential","description":"Boards 6.4 and 6.5. **A credential is not the wallet** — a lost wristband is relinked, not refunded.\n","required":["walletId","kind","identifier"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]},"identifier":{"type":"string"},"linkedAt":{"type":"string","format":"date-time"},"unlinkedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","lost","replaced","blocked","expired"]},"replacedByCredentialId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"WalletLiabilityRow": {"type":"object","description":"Boards 9.5 and 9.6. **The number the finance director asks for.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiringThisPeriod":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletCount":{"type":"integer"},"oldestLotAt":{"type":"string","format":"date","nullable":true}}},
"WalletType": {"type":"object","x-ticvai-persistence":"wallet.wallet_type","description":"Board 1.2. **Who owns a wallet** — the first of the two vocabularies.","required":["code","name"],"properties":{"autoReloadAllowed":{"type":"boolean","default":true,"description":"**Auto-reload is optional per wallet type** (Chinmay, 2 October, workbook Q105, default accepted; CHG-CSA-027). Where false, a holder of this type cannot set an auto top-up (`setWalletAutoReloadSetting` refuses it) whatever the venue's `WalletFundingRules.autoReload` says."},"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"ownerKind":{"type":"string","enum":["guest","registeredCustomer","family","parent","child","corporate","school","employee"]},"storedValueCapability":{"type":"boolean","default":true,"description":"Board 1.2. Whether this wallet holds a balance at all. A pure entitlement wallet — passes and vouchers, no money — does not.\n"},"topUpCapability":{"type":"boolean","default":false},"transferCapability":{"type":"boolean","default":false},"refundCapability":{"type":"boolean","default":false},"giftCardSupport":{"type":"boolean","default":false},"voucherSupport":{"type":"boolean","default":false},"membershipCreditSupport":{"type":"boolean","default":false},"wearableSupport":{"type":"boolean","default":false},"usageChannels":{"type":"array","description":"**Where this wallet may be used, declared on the type itself.** Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and this is what lets one `topUpWallet` serve every caller: the operation is shared and the type says which channel may reach it. `WalletChannelRules` still governs the per-credential detail — PIN thresholds, offline floor limits — and this governs whether the channel is open at all.\n","items":{"type":"string","enum":["online","pos","mobileApp","api","kiosk","reader"]}},"presetName":{"type":"string","description":"**The client's own name for this composition** — \"Resort Wallet\", \"Cashless Venue Wallet\", \"Closed-Loop Wallet\". Board 1.2 lists thirteen such names as examples, not as kinds: they are combinations of `ownerKind`, `allowedCreditTypeIds` and `scopePath`. Naming the preset keeps the client's vocabulary without hard-coding it into an enum.\n"},"holderMayDifferFromOwner":{"type":"boolean","default":false,"description":"**A child wallet's owner is the parent.** Without this the model has to pretend a seven-year-old holds an account.\n"},"requiresIdentification":{"type":"boolean","default":false},"maximumBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowNegativeBalance":{"type":"boolean","default":false},"sharedStructureAllowed":{"type":"boolean","default":false},"lifecycleStates":{"type":"array","items":{"type":"string"}},"numberingPattern":{"type":"string","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}}
}
```
