# WS188 — Wallet Configuration Backend Structure v1.0 board 3

**10 screens · 11 operations · 9 schemas · 3 permissions**

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
| `BO-1103` | Stored Value & Credit Command Center | C | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1104` | Credit Type Definition Studio | C | 24 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1105` | Credit Issuance Rule Configuration | C | 13 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1106` | Credit Usage & Eligibility Rules | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1107` | Consumption Priority Engine | C | 16 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-1108` | Expiry & Validity Policy Configuration | C | 11 | 14 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-1109` | FEFO & Credit Lot Management | C | 8 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1110` | Split Tender & Multi-Credit Consumption | C | 18 | 5 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1111` | Credit Expiry, Extension & Forfeiture Operations | A | 1 | 11 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1112` | Consumption Simulator, Validation & Rule Publication | C | 0 | 5 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1106, BO-1111 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1103` Stored Value & Credit Command Center

**Provide administrators with a centralized operational overview of all stored value and digital credits held across TICVAI wallets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1103 |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/stored-value-credit-command-center-bo-1103` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Stored value and credits across wallets: by credit type, outstanding, expiring.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCreditTypes, getWalletLiability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getWalletLiability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listCreditTypes / contracts/satellite/wallet.yaml#getWalletLiability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search stored value credit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, wallet type, credit type, customer/account type, currency and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

#### Outputs: what the screen shows and produces

**Shown**

**Total issued value** (metric tile)

**Current outstanding balance** (metric tile)

**Redeemed value** (metric tile)

**Expired value** (metric tile)

**Value expiring soon** (metric tile)

**Suspended/frozen value** (metric tile)

**Average wallet balance** (metric tile)

**Credits issued today** (metric tile)

**Credits consumed today** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **by credit type**: Outstanding and expiring next 30 days per type. *(source: contracts/satellite/wallet.yaml#getWalletLiability)*

**Data it reads**: `listCreditTypes` (onLoad, Credit types and their balances); `getWalletLiability` (onLoad, Outstanding by type)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1104` Credit Type Definition Studio: *Credit Type Definition Studio*; carries `creditTypeId`
- → `BO-1105` Credit Issuance Rule Configuration: *Credit Issuance Rule Configuration*; carries `creditTypeId`
- → `BO-1106` Credit Usage & Eligibility Rules: *Credit Usage & Eligibility Rules*; carries `creditTypeId`
- → `BO-1107` Consumption Priority Engine: *Consumption Priority Engine*
- → `BO-1108` Expiry & Validity Policy Configuration: *Expiry & Validity Policy Configuration*; carries `creditTypeId`
- → `BO-1109` FEFO & Credit Lot Management: *FEFO & Credit Lot Management*
- → `BO-1110` Split Tender & Multi-Credit Consumption: *Split Tender & Multi-Credit Consumption*
- → `BO-1111` Credit Expiry, Extension & Forfeiture Operations: *Credit Expiry, Extension & Forfeiture Operations*
- → `BO-1112` Consumption Simulator, Validation & Rule Publication: *Consumption Simulator, Validation & Rule Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stored value credit list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stored value credit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stored value credit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the stored value credit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  type: Bonus
  outstanding: AED 92,400.00
  expiring30d: AED 18,100.00
```

#### Permissions

- `listCreditTypes` → `WALLET_VIEW` (read) · staff
- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1103` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1103`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 1: Opens Stored Value & Credit Command Center → Provide administrators with a centralized operational overview of all stored value and digital credits held across TICVAI wallets.
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F295 branch at step 1 (expected): when Nothing has been set up on Stored Value & Credit Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F295 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1103?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1104`, `BO-1105`, `BO-1106`, `BO-1107`, `BO-1108`, `BO-1109`, `BO-1110`, `BO-1111`, `BO-1112`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1104` Credit Type Definition Studio

**Create and maintain the individual value buckets that can exist inside a TICVAI wallet. The source explicitly requires support for different digital wallet credit types such as Cash Credit, Bonus Credit, Redemption Tickets Credit and Rides Credit, with configurable usage criteria.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1104 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each credit type configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/orders-money/credit-type-definition-studio-bo-1104` |

**Known gaps.** **Credit Type Definition Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Create and maintain credit types (as BO-1088).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createCreditType, updateCreditType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Credit name | select field | — | — | — | — | — | — |
| Internal code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Credit category | select field | — | — | — | — | — | — |
| Monetary / non-monetary | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Unit of measure | select field | — | — | — | — | — | — |
| Decimal precision | select field | — | — | — | — | — | — |
| Transferable | select field | — | — | — | — | — | — |
| Refundable | select field | — | — | — | — | — | — |
| Reversible | select field | — | — | — | — | — | — |
| Top-up eligible | select field | — | — | — | — | — | — |
| Customer purchasable | select field | — | — | — | — | — | — |
| Promotional | select field | — | — | — | — | — | — |
| Membership related | select field | — | — | — | — | — | — |
| Gift related | select field | — | — | — | — | — | — |
| Expirable | select field | — | — | — | — | — | — |
| Shareable | select field | — | — | — | — | — | — |
| Family eligible | select field | — | — | — | — | — | — |
| Corporate eligible | select field | — | — | — | — | — | — |
| Offline usage permitted | select field | — | — | — | — | — | — |
| Customer-visible | select field | — | — | — | — | — | — |
| Accounting classification | select field | — | — | — | — | — | — |
| Liability classification | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of value that may sit in a wallet** (data table, from `listCreditTypes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Category | chip: Cash, Refund, Bonus, Promotional, Gift card, Membership… | — |
| Monetary | yes / no (icon or chip) | Loyalty points are not money. A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency … |
| Conversion rate | 12.5% | — |
| Refundable | yes / no (icon or chip) | Promotional credit is not refundable and cash credit is. A venue that refunds promotional credit to a card has converted marketing spend … |
| Transferable | yes / no (icon or chip) | — |
| Expires | yes / no (icon or chip) | — |
| Validity days | 1,234 | — |
| Breakage eligible | yes / no (icon or chip) | — |
| Ledger account code | text | — |
| Priority | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**Data it reads**: `listCreditTypes` (onLoad, The kinds of value that may sit in a wallet)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credit type definition configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credit type definition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credit type definition configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-1088`: Same editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
type:
  name: Free game
  monetary: false
```

#### Permissions

- `createCreditType` → `WALLET_CONFIGURE` (configure) · staff
- `updateCreditType` → `WALLET_CONFIGURE` (configure) · staff
- `listCreditTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A combo product can bundle admission with stored-value credit the guest draws down on F&B or retail purchases (wallet mechanics in a dedicated session). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-459)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1104` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1104`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 2: Works in Credit Type Definition Studio → Create and maintain the individual value buckets that can exist inside a TICVAI wallet. The source explicitly requires support for different digital wallet credit types such as Cash Credit, Bonus …

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1104?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1105` Credit Issuance Rule Configuration

**Define how credits enter a wallet after the wallet itself has already been funded or as the result of another TICVAI business process. This screen is deliberately different from Board 2: Board 2 controls funding/payment into a wallet; this screen controls the creation of individual credit buckets and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1105 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/orders-money/credit-issuance-rule-configuration-bo-1105` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A credit issuance rule record (trigger to credit) with its read and write; updateCreditType changes the credit type itself.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How credits are issued by other processes (purchase of a product, promotion, compensation) after funding.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Issuance rules are written through updateCreditType, which changes a credit type. (CHG-WIR-027)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateCreditType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Source event | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Fixed amount | select field | — | — | — | — | — | — |
| Percentage-based amount | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Maximum issuance | select field | — | — | — | — | — | — |
| Customer eligibility | select field | — | — | — | — | — | — |
| Applicable wallet | select field | — | — | — | — | — | — |
| Applicable venue | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Approval requirement | select field | — | — | — | — | — | — |
| Expiry policy | select field | — | — | — | — | — | — |
| Accounting treatment | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **issuance rule**: Trigger and credit type issued. *(source: contracts/satellite/wallet.yaml#updateCreditType)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of value that may sit in a wallet** (data table, from `listCreditTypes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Category | chip: Cash, Refund, Bonus, Promotional, Gift card, Membership… | — |
| Monetary | yes / no (icon or chip) | Loyalty points are not money. A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency … |
| Conversion rate | 12.5% | — |
| Refundable | yes / no (icon or chip) | Promotional credit is not refundable and cash credit is. A venue that refunds promotional credit to a card has converted marketing spend … |
| Transferable | yes / no (icon or chip) | — |
| Expires | yes / no (icon or chip) | — |
| Validity days | 1,234 | — |
| Breakage eligible | yes / no (icon or chip) | — |
| Ledger account code | text | — |
| Priority | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**Data it reads**: `listCreditTypes` (onLoad, The kinds of value that may sit in a wallet)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credit issuance rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credit issuance rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credit issuance rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: 'Buy Annual Pass Gold: issue AED 100.00 Bonus credit'
```

#### Permissions

- `updateCreditType` → `WALLET_CONFIGURE` (configure) · staff
- `listCreditTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Bonus credit tiers (e.g. AED 100 top-up earns AED 20 bonus; AED 200 earns AED 60). Bonus credit is consumed before base top-up credit and carries its own separate validity period. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-524)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1105` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1105`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 4: Works in Credit Issuance Rule Configuration → Define how credits enter a wallet after the wallet itself has already been funded or as the result of another TICVAI business process. This screen is deliberately different from Board 2: Board 2 …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1105?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1106` Credit Usage & Eligibility Rules

**Define exactly where and under what conditions each wallet credit may be consumed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1106 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/orders-money/credit-usage-eligibility-rules-bo-1106` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the credit eligibility (where a credit may be spent; CreditType does not carry it) that setCreditEligibilityRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where and when each credit may be consumed.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setCreditEligibilityRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credit usage eligibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credit usage eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credit usage eligibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credit usage eligibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-399`: Same eligibility editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  credit: Bonus
  allowed:
  - rides
  - games
```

#### Permissions

- `setCreditEligibilityRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Credit usage restrictions scope a credit to spend categories (e.g. usable for food & beverage, not retail), fully configurable; with no restriction the balance is spendable on anything offered. *(client request · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-522)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1106` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1106`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 6: Works in Credit Usage & Eligibility Rules → Define exactly where and under what conditions each wallet credit may be consumed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1106?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1107` Consumption Priority Engine

**Configure which wallet balance TICVAI should consume first when multiple eligible credits can pay for the same transaction. This directly addresses the source requirement that usage priority must be configurable—for example, consuming Cash Credit before Bonus Credit.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1107 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration; Configure priority by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/consumption-priority-engine-bo-1107` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which credit is drawn first when several can pay: nearest expiry first, bonus before base under its own validity; the guest sees the breakdown but cannot choose.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Expiring Promotional Credit | select field | — | — | — | — | — | — |
| Bonus Credit | select field | — | — | — | — | — | — |
| Gift Card Credit | select field | — | — | — | — | — | — |
| Membership Credit | select field | — | — | — | — | — | — |
| Cash Credit | select field | — | — | — | — | — | — |
| External Payment | select field | — | — | — | — | — | — |
| Membership Included Credit | select field | — | — | — | — | — | — |
| Ride Credit | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Customer type | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **order**: Drag-to-order list of credit types with FEFO within a type. *(source: contracts/satellite/wallet.yaml#setCreditConsumptionPolicy / TRACKER Actions row 110)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cash value last (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getCreditConsumptionPolicy` (onLoad, The order in force)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consumption priority configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consumption priority untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consumption priority configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
- Promotional (FEFO)
- Bonus (FEFO)
- Cash
```

#### Permissions

- `setCreditConsumptionPolicy` → `WALLET_CONFIGURE` (configure) · staff
- `getCreditConsumptionPolicy` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Bonus credit tiers (e.g. AED 100 top-up earns AED 20 bonus; AED 200 earns AED 60). Bonus credit is consumed before base top-up credit and carries its own separate validity period. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-524)*
- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1107` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1107`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 8: Works in Consumption Priority Engine → Configure which wallet balance TICVAI should consume first when multiple eligible credits can pay for the same transaction. This directly addresses the source requirement that usage priority must be …

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1107?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Cash value last.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1108` Expiry & Validity Policy Configuration

**Configure how long each type of wallet value remains valid. The source requires configurable expiry periods for all credit types, including the ability to configure unlimited validity, particularly for cash credit.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1108 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/orders-money/expiry-validity-policy-configuration-bo-1108` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Validity per credit type, including unlimited.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only updateCreditType and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Valid-from date | select field | — | — | — | — | — | — |
| Expiry calculation | select field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Expiry timezone | select field | — | — | — | — | — | — |
| Extension allowed | select field | — | — | — | — | — | — |
| Manual extension permission | select field | — | — | — | — | — | — |
| Maximum extension | select field | — | — | — | — | — | — |
| Renewal behavior | select field | — | — | — | — | — | — |
| Remaining-value behavior | select field | — | — | — | — | — | — |
| Notification schedule | select field | — | — | — | — | — | — |
| Accounting treatment after expiry | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **expiry**: Unlimited allowed for cash where the law requires. *(source: contracts/satellite/wallet.yaml#updateCreditType)*

#### Outputs: what the screen shows and produces

**Shown**

**The kinds of value that may sit in a wallet** (data table, from `listCreditTypes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Category | chip: Cash, Refund, Bonus, Promotional, Gift card, Membership… | — |
| Monetary | yes / no (icon or chip) | Loyalty points are not money. A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency … |
| Conversion rate | 12.5% | — |
| Refundable | yes / no (icon or chip) | Promotional credit is not refundable and cash credit is. A venue that refunds promotional credit to a card has converted marketing spend … |
| Transferable | yes / no (icon or chip) | — |
| Expires | yes / no (icon or chip) | — |
| Validity days | 1,234 | — |
| Breakage eligible | yes / no (icon or chip) | — |
| Ledger account code | text | — |
| Priority | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**Data it reads**: `listCreditTypes` (onLoad, The kinds of value that may sit in a wallet)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiry validity policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiry validity policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiry validity policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
expiry:
  Cash: unlimited
  Bonus: 90 days
```

#### Permissions

- `updateCreditType` → `WALLET_CONFIGURE` (configure) · staff
- `listCreditTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet statuses: active, suspended, blocked, closed. Every wallet must have a validity period (never open-ended); on lapse the remaining balance, monetary or non-monetary, is automatically swept to a finance-designated account. *(agreed · MoM 27 Aug 2026, 4.4 Wallet Lifecycle, Numbering & Publish Flow · DI-512)*
- Stored value configuration: minimum stored value, maximum top-up balance, expiry of stored balance, and refund destination (original payment method or back to wallet balance). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-468)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1108` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1108`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 10: Works in Expiry & Validity Policy Configuration → Configure how long each type of wallet value remains valid. The source requires configurable expiry periods for all credit types, including the ability to configure unlimited validity, particularly …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1108?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1109` FEFO & Credit Lot Management

**Control consumption when multiple lots of the same credit type have different expiry dates. Requirement 4.3.19 specifically requires TICVAI to support FEFO — First Expiry, First Out.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1109 |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/fefo-credit-lot-management-bo-1109` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Lots of the same credit type with different expiries, consumed first expiry first.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCreditLots return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listCreditLots; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Strategy per credit type | text field | — | — | — | — | — | — |
| Cross-lot consumption | select field | — | — | — | — | — | — |
| Partial lot consumption | select field | — | — | — | — | — | — |
| Lot locking | select field | — | — | — | — | — | — |
| Reserved balance handling | select field | — | — | — | — | — | — |
| Expired lot handling | select field | — | — | — | — | — | — |
| Reversal behavior | select field | — | — | — | — | — | — |
| Refund restoration behavior | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Wallet | picker: choose a wallet | — | — | `listCreditLots` ?walletId |
| Include exhausted | toggle | off | — | `listCreditLots` ?includeExhausted |
| Expiring within days | number field (days) | — | min 1 | `listCreditLots` ?expiringWithinDays |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **lots**: Lots per wallet in consumption order. *(source: contracts/satellite/wallet.yaml#listCreditLots)*

**Data it reads**: `listCreditLots` (onLoad, The lots behind a balance)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fefo credit lot configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fefo credit lot untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fefo credit lot configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
lots:
- Bonus AED 20.00 expires 2026-11-30
- Bonus AED 25.00 expires 2026-12-31
```

#### Permissions

- `listCreditLots` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1109` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1109`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 12: Works in FEFO & Credit Lot Management → Control consumption when multiple lots of the same credit type have different expiry dates. Requirement 4.3.19 specifically requires TICVAI to support FEFO — First Expiry, First Out.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1109?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1110` Split Tender & Multi-Credit Consumption

**Configure transactions where multiple wallet credits and external payment methods are combined.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1110 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Options when balance is insufficient) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/split-tender-multi-credit-consumption-bo-1110` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Combining several credits and an external payment in one transaction, with a simulation of what a purchase would use.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setCreditConsumptionPolicy, simulateCreditConsumption and nothing that returns the current … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Multi-credit usage allowed | select field | — | — | — | — | — | — |
| Maximum credit types per transaction | text field | — | — | — | — | — | — |
| Partial redemption | select field | — | — | — | — | — | — |
| Wallet + card | select field | — | — | — | — | — | — |
| Wallet + cash | select field | — | — | — | — | — | — |
| Wallet + voucher | select field | — | — | — | — | — | — |
| Wallet + loyalty | select field | — | — | — | — | — | — |
| Wallet + gift card | text field | — | — | — | — | — | — |
| Wallet + multiple payment methods | text field | — | — | — | — | — | — |
| Minimum external payment | select field | — | — | — | — | — | — |
| Rounding | select field | — | — | — | — | — | — |
| Insufficient-wallet behavior | select field | — | — | — | — | — | — |
| Request external payment | select field | — | — | — | — | — | — |
| Reject transaction | select field | — | — | — | — | — | — |
| Use next eligible wallet | text field | — | — | — | — | — | — |
| Ask customer | select field | — | — | — | — | — | — |
| Allow authorized negative balance | text field | — | — | — | — | — | — |
| Route to corporate wallet | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Which credit is spent first** (detail panel, from `getCreditConsumptionPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Strategy | chip: Expiring first, Type priority, Non refundable first, Manual | `expiringFirst` is the default because it is the one that does not quietly profit from the guest forgetting. |
| Type order | list or chips (count when long) | — |
| Within type order | chip: Fefo, Fifo, Lifo | — |
| Allow split tender | yes / no (icon or chip) | — |
| Allow guest choice | yes / no (icon or chip) | Whether a guest may override the order at the till. Rarely enabled, and the venues that want it want it badly. |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate**: A basket and wallet in; the lots and tender used out. *(source: contracts/satellite/wallet.yaml#simulateCreditConsumption)*

**Data it reads**: `getCreditConsumptionPolicy` (onLoad, Which credit is spent first)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The split tender multi-credit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the split tender multi-credit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No split tender multi-credit configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
simulation:
  basket: AED 120.00
  uses:
  - Bonus AED 36.50
  - Cash AED 83.50
```

#### Permissions

- `setCreditConsumptionPolicy` → `WALLET_CONFIGURE` (configure) · staff
- `simulateCreditConsumption` → `WALLET_VIEW` (read) · staff
- `getCreditConsumptionPolicy` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1110` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1110`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 14: Works in Split Tender & Multi-Credit Consumption → Configure transactions where multiple wallet credits and external payment methods are combined.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1110?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1111` Credit Expiry, Extension & Forfeiture Operations

**Provide governed administrative management of credits approaching or reaching expiry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · task VM-BO-1111 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/credit-expiry-extension-forfeiture-operations-bo-1111` |

**What the spec says about it.** **Credit lots are listed across the venue by expiry window (listCreditLots without walletId, expiringWithinDays), 4 October 2026; the pack-label tables left** (CHG-FXS-003)

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Credit approaching or reaching expiry: expire, extend or forfeit lots, with the accounting consequence stated, because expired credit stops being a liability and becomes breakage revenue on a date someone can defend. Extensions are recorded and never rewrite the original history.

**Fixed on main** (the package already carries these; draw what it says): No list of lots near expiry; the customer-level view of balances and expiry dates the client asked for has no read operation on this screen. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Expiring within | select field | — | — | — | — | Query expiringWithinDays: today, 7 or 30 days. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Wallet | picker: choose a wallet | — | — | `listCreditLots` ?walletId |
| Include exhausted | toggle | off | — | `listCreditLots` ?includeExhausted |
| Expiring within days | number field (days) | — | min 1 | `listCreditLots` ?expiringWithinDays |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **selection**: By expiry date range, credit type and wallet type; an "as of" date for the run. *(source: contracts/satellite/wallet.yaml#expireCreditLots / DI-527)*

#### Outputs: what the screen shows and produces

**Shown**

**Credit lots** (data table, from `listCreditLots`): Across the venue's wallets when no wallet is picked; selecting lots gives expireCreditLots its lots to expire, extend or forfeit.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Credit type | the name it points at, never the id | — |
| Issued amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Remaining amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Issued at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Source kind | chip: Top up, Refund, Promotion, Gift card, Membership benefit, Loyalty conversion… | — |
| Source reference | text | — |
| Terms snapshot | grouped details | The credit type's terms as they stood at issue. Changing a credit type must not retro-expire credit already given, so the lot carries its … |
| Status | chip: Active, Exhausted, Expired, Forfeited, Reversed | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **run preview**: Lots affected, wallets affected, total amount and breakage amount before applying. *(source: contracts/satellite/wallet.yaml#expireCreditLots)*

**Data it reads**: `listCreditLots` (onLoad, Every wallet's credit lots at this venue (no walletId) …)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credit expiry extension list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credit expiry extension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credit expiry extension yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credit expiry extension are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
run:
  asOf: '2026-12-31'
  creditType: Bonus
  lots: 1240
  wallets: 980
  total: AED 41,320.00
  breakage: AED 41,320.00
```

#### Permissions

- `expireCreditLots` → `WALLET_OPERATE` (operate) · staff
- `listCreditLots` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Credit expiry and extension operations give admins a customer-level view of all wallet balances and their expiry dates to manage upcoming expiries. *(client request · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-527)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1111` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1111`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 16: Works in Credit Expiry, Extension & Forfeiture Operations → Provide governed administrative management of credits approaching or reaching expiry.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1111?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1103`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1112` Consumption Simulator, Validation & Rule Publication

**Allow administrators to test the entire credit engine before publishing new rules. This is important because the interaction between eligibility, expiry, FEFO and priority can otherwise create unintended wallet behavior. Test Scenario Configure TICVAI's shared-wallet architecture for families, parents and children, groups, schools, companies, corporate clients and other organizations. This board covers the requirements for family wallets, designated wallet owners, budget distribution, spending caps, shared balances, corporate spending wallets, permissions, and parent-card/child-card stored-value distribution. The central concept is that TICVAI should support both: Shared Balance Model — multiple authorized users consume one central balance. and Allocated Balance Model — the wallet owner distributes allowances/budgets to linked users while retaining centralized control.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1112 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/consumption-simulator-validation-rule-publication-bo-1112` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test the credit engine (eligibility, expiry, FEFO, priority) before publishing rules.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only simulateCreditConsumption, publishWalletConfiguration and nothing that returns the current … (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Which credit is spent first** (detail panel, from `getCreditConsumptionPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Strategy | chip: Expiring first, Type priority, Non refundable first, Manual | `expiringFirst` is the default because it is the one that does not quietly profit from the guest forgetting. |
| Type order | list or chips (count when long) | — |
| Within type order | chip: Fefo, Fifo, Lifo | — |
| Allow split tender | yes / no (icon or chip) | — |
| Allow guest choice | yes / no (icon or chip) | Whether a guest may override the order at the till. Rarely enabled, and the venues that want it want it badly. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate then publish**: Simulation first; publish only with no errors. *(source: contracts/satellite/wallet.yaml#simulateCreditConsumption / contracts/satellite/wallet.yaml#publishWalletConfiguration)*

**Data it reads**: `getCreditConsumptionPolicy` (onLoad, Which credit is spent first)

**Where the user goes next**

- → `BO-1103` Stored Value & Credit Command Center: *Back to Stored Value & Credit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consumption simulator validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consumption simulator validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consumption simulator validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the consumption simulator validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  scenario: Child wristband buying ice cream with bonus only
  result: 'refused: bonus not valid for F&B'
```

#### Permissions

- `simulateCreditConsumption` → `WALLET_VIEW` (read) · staff
- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff
- `getCreditConsumptionPolicy` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1112` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1112`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 3
- Flow F295 *Wallet Configuration Backend Structure v1.0 board 3: Stored Value & Credit …*, step 18: Works in Consumption Simulator, Validation & Rule Publication → Allow administrators to test the entire credit engine before publishing new rules. This is important because the interaction between eligibility, expiry, FEFO and priority can otherwise create …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1112?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-1103`.
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

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createCreditType": {"method":"POST","path":"/credit-types","contract":"wallet","summary":"Define a kind of credit, without a release","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreditType","responds":"CreditType"},
"expireCreditLots": {"method":"POST","path":"/credit-lots/expire","contract":"wallet","summary":"Expire, extend or forfeit credit that has run out of time","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CreditExpiryResult"},
"getCreditConsumptionPolicy": {"method":"GET","path":"/credit-consumption-policy","contract":"wallet","summary":"Which credit is spent first","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CreditConsumptionPolicy"},
"getWalletLiability": {"method":"GET","path":"/wallet-liability","contract":"wallet","summary":"What is outstanding, and what is breakage","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"asOf","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletLiabilityRow"},
"listCreditLots": {"method":"GET","path":"/credit-lots","contract":"wallet","summary":"The tranches behind a balance, with their expiry","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"walletId","in":"query","required":false},{"name":"includeExhausted","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":false}],"requestBody":null,"responds":"CreditLot"},
"listCreditTypes": {"method":"GET","path":"/credit-types","contract":"wallet","summary":"The kinds of value that may sit in a wallet","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CreditType"},
"publishWalletConfiguration": {"method":"POST","path":"/wallet-configuration/publish","contract":"wallet","summary":"Validate and publish the wallet configuration as a version","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletConfigurationVersion"},
"setCreditConsumptionPolicy": {"method":"PUT","path":"/credit-consumption-policy","contract":"wallet","summary":"The order credit is drawn down in","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreditConsumptionPolicy","responds":"CreditConsumptionPolicy"},
"setCreditEligibilityRules": {"method":"PUT","path":"/credit-types/{creditTypeId}/eligibility","contract":"wallet","summary":"Where this credit may be spent, and on what","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreditEligibility","responds":"CreditEligibility"},
"simulateCreditConsumption": {"method":"POST","path":"/credit-consumption/simulate","contract":"wallet","summary":"Which credit this purchase would actually use","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CreditAllocation"},
"updateCreditType": {"method":"PUT","path":"/credit-types/{creditTypeId}","contract":"wallet","summary":"Change a kind of credit","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreditType","responds":"CreditType"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreditAllocation": {"type":"object","description":"Board 3.10. **Which lots this purchase would draw on**, in order.","properties":{"requested":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"covered":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"shortfall":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","properties":{"lotId":{"type":"string","format":"uuid"},"creditTypeId":{"type":"string","format":"uuid"},"creditTypeName":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"reason":{"type":"string"}}}},"rejected":{"type":"array","items":{"type":"object","properties":{"creditTypeId":{"type":"string","format":"uuid"},"reason":{"type":"string","enum":["notEligibleHere","notEligibleForProduct","expired","basketCapReached","restricted"]}}}}}},
"CreditConsumptionPolicy": {"type":"object","x-ticvai-persistence":"wallet.consumption_policy","description":"Boards 3.5 and 3.7. **There is no neutral default**, which is why this is configuration.\n","properties":{"strategy":{"type":"string","enum":["expiringFirst","typePriority","nonRefundableFirst","manual"],"default":"expiringFirst","description":"**`expiringFirst` is the default because it is the one that does not quietly profit from the guest forgetting.**\n"},"typeOrder":{"type":"array","items":{"type":"string","format":"uuid"}},"withinTypeOrder":{"type":"string","enum":["fefo","fifo","lifo"],"default":"fefo"},"allowSplitTender":{"type":"boolean","default":true},"allowGuestChoice":{"type":"boolean","default":false,"description":"**Whether a guest may override the order at the till.** Rarely enabled, and the venues that want it want it badly.\n"},"scopePath":{"type":"string"}}},
"CreditEligibility": {"type":"object","x-ticvai-persistence":"wallet.credit_eligibility","description":"Board 3.4. **Where credit may be spent** — acceptance, not funding.","properties":{"creditTypeId":{"type":"string","format":"uuid"},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedOutletKinds":{"type":"array","items":{"type":"string"}},"allowedProductCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"excludedProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedChannels":{"type":"array","items":{"type":"string"}},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumPercentOfBasket":{"type":"number","nullable":true,"description":"**Caps how much of a purchase one credit type may cover.** A venue that lets promotional credit pay for everything has run a free day it did not intend.\n"},"validDaysOfWeek":{"type":"array","items":{"type":"string"}},"scopePath":{"type":"string"}}},
"CreditExpiryResult": {"type":"object","description":"Board 3.9. **Expiry has an accounting consequence**, so the preview carries it.","properties":{"lotsAffected":{"type":"integer"},"totalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletsAffected":{"type":"integer"},"applied":{"type":"boolean"},"asOf":{"type":"string","format":"date"}}},
"CreditLot": {"type":"object","x-ticvai-persistence":"wallet.credit_lot","description":"Board 3.7. **The tranche behind a balance.** Expiry belongs here, not on the wallet.","required":["id","walletId","creditTypeId"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"creditTypeId":{"type":"string","format":"uuid"},"issuedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceKind":{"type":"string","enum":["topUp","refund","promotion","giftCard","membershipBenefit","loyaltyConversion","transfer","adjustment"]},"sourceReference":{"type":"string","nullable":true},"termsSnapshot":{"type":"object","additionalProperties":true,"description":"**The credit type's terms as they stood at issue.** Changing a credit type must not retro-expire credit already given, so the lot carries its own terms.\n**Open on purpose, and its shape lives in `CreditType`**: the snapshot is that credit type's properties copied at issue, so it follows `CreditType` as it stood then rather than as it stands now.\n"},"status":{"type":"string","enum":["active","exhausted","expired","forfeited","reversed"]},"scopePath":{"type":"string"}}},
"CreditType": {"type":"object","x-ticvai-persistence":"wallet.credit_type","description":"Board 1.6. **What value sits inside a wallet** — the second vocabulary, and the one the acceptance condition requires to be a table.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"category":{"type":"string","enum":["cash","refund","bonus","promotional","giftCard","membership","loyalty","ride","attraction","redemption","fnb","retail","parking","event","other"]},"monetary":{"type":"boolean","default":true,"description":"**Loyalty points are not money.** A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency puts them on the balance sheet.\n"},"conversionRate":{"type":"number","nullable":true},"refundable":{"type":"boolean","default":false,"description":"**Promotional credit is not refundable and cash credit is.** A venue that refunds promotional credit to a card has converted marketing spend into cash.\n"},"transferable":{"type":"boolean","default":false},"expires":{"type":"boolean","default":false},"validityDays":{"type":"integer","nullable":true},"breakageEligible":{"type":"boolean","default":false},"ledgerAccountCode":{"type":"string","nullable":true},"priority":{"type":"integer","default":0},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"WalletConfigurationVersion": {"type":"object","x-ticvai-persistence":"wallet.configuration_version","description":"Boards 1.10 and 10.8. **Ten boards of configuration that interact.**","properties":{"version":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedBy":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"code":{"type":"string"},"message":{"type":"string"}}}},"scopePath":{"type":"string"}}},
"WalletLiabilityRow": {"type":"object","description":"Boards 9.5 and 9.6. **The number the finance director asks for.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiringThisPeriod":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletCount":{"type":"integer"},"oldestLotAt":{"type":"string","format":"date","nullable":true}}}
}
```
