# WS191 — Wallet Configuration Backend Structure v1.0 board 6

**10 screens · 6 operations · 9 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PAYMENT_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1133` | Wallet Usage & Channel Command Center | B–D | 2 | 28 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1134` | Wallet Channel Configuration | B–D | 30 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1135` | Wallet Payment & Redemption Policy | B–D | 16 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-1136` | Wearable & Credential Type Configuration | B–D | 18 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1137` | Wearable Linking & Wallet Association Rules | B–D | 24 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-1138` | NFC, RFID & QR Interaction Rules | B–D | 11 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1139` | Digital Key & Wallet Authentication Policy | B–D | 15 | 0 | 6 | 1 | 0 | 6 | — | notStarted (—) |
| `BO-1140` | Offline Wallet & Degraded Mode Configuration | B–D | 20 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1141` | Device, Terminal & Acceptance Point Mapping | B–D | 14 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1142` | Wallet Transaction Simulator, Monitoring & Channel Audit | B–D | 0 | 0 | 6 | 3 | 1 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-1142 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1133` Wallet Usage & Channel Command Center

**Provide a real-time operational view of wallet usage across all TICVAI channels and venue touchpoints. Dashboard KPIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-usage-channel-command-center-bo-1133` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-025): A command centre declared only the channel-rules write (setWalletChannelRules), which its children BO-1134 to BO-1140 own; usage needs a read of transactions by … Contract gap recorded 2 October 2026 (CHG-WIR-027): A venue read of wallet usage and transactions aggregated by channel and touchpoint (listWalletTransactions is per wallet).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet usage across channels and touchpoints in real time.

**Fixed on main** (the package already carries these; draw what it says): A command centre declares only a configuration write (setWalletChannelRules). (CHG-WIR-025); No read operation: the screen declares only setWalletChannelRules and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search wallet usage channel | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, channel, outlet, device, wallet type and 5 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every wallet usage channel** (data table)

| Shows | Format | Notes |
|---|---|---|
| Wallet transactions today | text | not in the schema: `Wallet Transactions Today` |
| Wallet spend today | text | not in the schema: `Wallet Spend Today` |
| Online wallet spend | text | not in the schema: `Online Wallet Spend` |
| Onsite wallet spend | text | not in the schema: `Onsite Wallet Spend` |
| POS transactions | text | not in the schema: `POS Transactions` |
| Mobile app transactions | text | not in the schema: `Mobile App Transactions` |
| Wearable transactions | text | not in the schema: `Wearable Transactions` |
| QR transactions | text | not in the schema: `QR Transactions` |
| NFC transactions | text | not in the schema: `NFC Transactions` |
| RFID transactions | text | not in the schema: `RFID Transactions` |
| Declined wallet transactions | text | not in the schema: `Declined Wallet Transactions` |
| Offline transactions | text | not in the schema: `Offline Transactions` |
| Pending synchronizations | text | not in the schema: `Pending Synchronizations` |
| Usage by business area | text | not in the schema: `Usage by Business Area` |

**The selected wallet usage channel** (detail panel): The pack groups this record's detail under its own headings: “Break down by”, “Highlight”.

| Shows | Format | Notes |
|---|---|---|
| Wallet transactions today | text | not in the schema: `Wallet Transactions Today` |
| Wallet spend today | text | not in the schema: `Wallet Spend Today` |
| Online wallet spend | text | not in the schema: `Online Wallet Spend` |
| Onsite wallet spend | text | not in the schema: `Onsite Wallet Spend` |
| POS transactions | text | not in the schema: `POS Transactions` |
| Mobile app transactions | text | not in the schema: `Mobile App Transactions` |
| Wearable transactions | text | not in the schema: `Wearable Transactions` |
| QR transactions | text | not in the schema: `QR Transactions` |
| NFC transactions | text | not in the schema: `NFC Transactions` |
| RFID transactions | text | not in the schema: `RFID Transactions` |
| Declined wallet transactions | text | not in the schema: `Declined Wallet Transactions` |
| Offline transactions | text | not in the schema: `Offline Transactions` |
| Pending synchronizations | text | not in the schema: `Pending Synchronizations` |
| Usage by business area | text | not in the schema: `Usage by Business Area` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **usage**: Spend by channel and touchpoint. *(source: contracts/satellite/wallet.yaml#setWalletChannelRules)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1134` Wallet Channel Configuration: *Wallet Channel Configuration*
- → `BO-1135` Wallet Payment & Redemption Policy: *Wallet Payment & Redemption Policy*
- → `BO-1136` Wearable & Credential Type Configuration: *Wearable & Credential Type Configuration*
- → `BO-1137` Wearable Linking & Wallet Association Rules: *Wearable Linking & Wallet Association Rules*
- → `BO-1138` NFC, RFID & QR Interaction Rules: *NFC, RFID & QR Interaction Rules*
- → `BO-1139` Digital Key & Wallet Authentication Policy: *Digital Key & Wallet Authentication Policy*
- → `BO-1140` Offline Wallet & Degraded Mode Configuration: *Offline Wallet & Degraded Mode Configuration*
- → `BO-1141` Device, Terminal & Acceptance Point Mapping: *Device, Terminal & Acceptance Point Mapping*
- → `BO-1142` Wallet Transaction Simulator, Monitoring & Channel Audit: *Wallet Transaction Simulator, Monitoring & Channel Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet usage channel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet usage channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet usage channel yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet usage channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
today:
  wristband: AED 84,000.00
  app: AED 22,000.00
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1133` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1133`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 1: Opens Wallet Usage & Channel Command Center → Provide a real-time operational view of wallet usage across all TICVAI channels and venue touchpoints. Dashboard KPIs
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F298 branch at step 1 (expected): when Nothing has been set up on Wallet Usage & Channel Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F298 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1133?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1134`, `BO-1135`, `BO-1136`, `BO-1137`, `BO-1138`, `BO-1139`, `BO-1140`, `BO-1141`, `BO-1142`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1134` Wallet Channel Configuration

**Define which TICVAI channels can use Wallet as a payment or redemption method. Requirement 4.3.8 requires multiple wallet payment channels including mobile applications and wearables, with online, onsite POS and in-app payment modes. Supported Channels**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-channel-configuration-bo-1134` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet channel rules that setWalletChannelRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which channels may use the wallet to pay or redeem: app, wearables, online, on site.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletChannelRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| B2C Website | select field | — | — | — | — | — | — |
| Customer Mobile App | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Mobile POS | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| Self-Service Terminal | select field | — | — | — | — | — | — |
| F&B POS | select field | — | — | — | — | — | — |
| Retail POS | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Attraction Terminal | select field | — | — | — | — | — | — |
| Access Device | select field | — | — | — | — | — | — |
| Customer Service | select field | — | — | — | — | — | — |
| Corporate Portal | select field | — | — | — | — | — | — |
| B2B | select field | — | — | — | — | — | — |
| API | select field | — | — | — | — | — | — |
| Third-party system | select field | — | — | — | — | — | — |
| Per Channel Configure | select field | — | — | — | — | — | — |
| Wallet payment enabled | select field | — | — | — | — | — | — |
| Balance inquiry enabled | select field | — | — | — | — | — | — |
| Voucher redemption | select field | — | — | — | — | — | — |
| Gift card redemption | select field | — | — | — | — | — | — |
| Refund-to-wallet | select field | — | — | — | — | — | — |
| Split tender | select field | — | — | — | — | — | — |
| Top-up | select field | — | — | — | — | — | — |
| Transfer | select field | — | — | — | — | — | — |
| Offline wallet usage | select field | — | — | — | — | — | — |
| Supported currencies | select field | — | — | — | — | — | — |
| Supported credit types | select field | — | — | — | — | — | — |
| Maximum transaction | select field | — | — | — | — | — | — |
| Authentication requirement | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **allowedChannels**: Channel checkboxes using vocabulary labels. *(source: contracts/satellite/wallet.yaml#setWalletChannelRules)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet channel configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet channel configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-1141`: Same wallet channel rules record.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
channels:
- App
- Website
- Point of sale
- Kiosk
```

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1134` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1134`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 2: Works in Wallet Channel Configuration → Define which TICVAI channels can use Wallet as a payment or redemption method. Requirement 4.3.8 requires multiple wallet payment channels including mobile applications and wearables, with online …

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1134?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1135` Wallet Payment & Redemption Policy

**Configure the business rules applied when a customer selects Wallet at checkout.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Whereas another venue could configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-payment-redemption-policy-bo-1135` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet channel rules that setWalletChannelRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rules when a guest pays with the wallet: partial or full only, combination with other tenders, PIN.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletChannelRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet payment enabled | select field | — | — | — | — | — | — |
| Full wallet payment | select field | — | — | — | — | — | — |
| Partial wallet payment | select field | — | — | — | — | — | — |
| Split tender | select field | — | — | — | — | — | — |
| Minimum wallet contribution | select field | — | — | — | — | — | — |
| Maximum wallet contribution | select field | — | — | — | — | — | — |
| Maximum transaction value | select field | — | — | — | — | — | — |
| Minimum remaining balance | select field | — | — | — | — | — | — |
| Negative balance allowed/not allowed | text field | — | — | — | — | — | — |
| External tender fallback | select field | — | — | — | — | — | — |
| PIN requirement | select field | — | — | — | — | — | — |
| MFA requirement | select field | — | — | — | — | — | — |
| Customer confirmation | select field | — | — | — | — | — | — |
| Receipt requirement | select field | — | — | — | — | — | — |
| Transaction Types | select field | — | — | — | — | — | — |
| Partial wallet payment = Not Allowed | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **redemption policy**: Partial allowed or full only, split tender allowed. *(source: contracts/satellite/wallet.yaml#setWalletChannelRules / TRACKER Actions row 112)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet payment redemption configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet payment redemption untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet payment redemption configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  partial: true
  splitTender: true
  pinAbove: AED 200.00
```

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*
- Partial vs full redemption is configurable per wallet/gift-card type: some allow spending part and keeping the remainder, others require full redemption in a single transaction. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-526)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1135` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1135`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 4: Works in Wallet Payment & Redemption Policy → Configure the business rules applied when a customer selects Wallet at checkout.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1135?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1136` Wearable & Credential Type Configuration

**Define physical and digital credentials that can represent a wallet. The source requires venue-provided wearables to be linked to digital wallets and used to make payments. Credential Types**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wearable-credential-type-configuration-bo-1136` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet channel rules that setWalletChannelRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Credentials that can represent a wallet (wristband, card, NFC, RFID, QR, app, digital key).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletChannelRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Credential name | select field | — | — | — | — | — | — |
| Internal code | select field | — | — | — | — | — | — |
| Technology | select field | — | — | — | — | — | — |
| Identifier format | select field | — | — | — | — | — | — |
| Tokenization | select field | — | — | — | — | — | — |
| Encryption requirement | select field | — | — | — | — | — | — |
| Wallet linking allowed | select field | — | — | — | — | — | — |
| Multiple credentials per wallet | text field | — | — | — | — | — | — |
| Credential sharing permitted | select field | — | — | — | — | — | — |
| PIN required | select field | — | — | — | — | — | — |
| Customer verification | select field | — | — | — | — | — | — |
| Activation | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Replacement | select field | — | — | — | — | — | — |
| Lost/stolen handling | select field | — | — | — | — | — | — |
| Offline eligibility | select field | — | — | — | — | — | — |
| Applicable venue | select field | — | — | — | — | — | — |
| Applicable device types | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **credential kinds**: Chips; each with whether it works offline. *(source: contracts/satellite/wallet.yaml#setWalletChannelRules)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| RFID Card (primary button) | navigation or local | — | — | — | — |
| NFC Card (secondary button) | navigation or local | — | — | — | — |
| Mobile Wallet Credential (secondary button) | navigation or local | — | — | — | — |
| Digital Key (secondary button) | navigation or local | — | — | — | — |
| Hotel Key (secondary button) | navigation or local | — | — | — | — |
| Event Badge (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wearable credential type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wearable credential type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wearable credential type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kinds:
- wristband
- rfid
- qr
- mobileApp
```

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1136` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1136`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 6: Works in Wearable & Credential Type Configuration → Define physical and digital credentials that can represent a wallet. The source requires venue-provided wearables to be linked to digital wallets and used to make payments. Credential Types

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1136?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: RFID Card, NFC Card, Mobile Wallet Credential, Digital Key, Hotel Key, Event Badge.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1137` Wearable Linking & Wallet Association Rules

**Configure how wristbands, cards and other credentials are linked to wallet accounts. Requirement 4.3.12 specifically requires guests to link and remove venue-issued wearables from their wallet. Linking Methods Customer Mobile App B2C Portal POS Guest Services Kiosk Hotel Check-In Event Registration Administrative Backend API**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wearable-linking-wallet-association-rules-bo-1137` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the credentials linked to a wallet that linkWalletCredential writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How wristbands and cards are linked to and removed from a wallet; a lost credential is unlinked, the wallet stays.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only linkWalletCredential and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet type eligibility | select field | — | — | — | — | — | — |
| Credential type | select field | — | — | — | — | — | — |
| Customer verification | select field | — | — | — | — | — | — |
| Activation code | select field | — | — | — | — | — | — |
| PIN verification | select field | — | — | — | — | — | — |
| OTP verification | select field | — | — | — | — | — | — |
| Digital ID verification | select field | — | — | — | — | — | — |
| Maximum credentials per wallet | text field | — | — | — | — | — | — |
| Maximum wallets per credential | text field | — | — | — | — | — | — |
| Automatic activation | select field | — | — | — | — | — | — |
| Manual approval | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Credential Lifecycle | select field | — | — | — | — | — | — |
| Administrative Actions | select field | — | — | — | — | — | — |
| Link | select field | — | — | — | — | — | — |
| Unlink | select field | — | — | — | — | — | — |
| Suspend | select field | — | — | — | — | — | — |
| Reactivate | select field | — | — | — | — | — | — |
| Replace | select field | — | — | — | — | — | — |
| Transfer | select field | — | — | — | — | — | — |
| Mark Lost | select field | — | — | — | — | — | — |
| Mark Stolen | select field | — | — | — | — | — | — |
| View Usage | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Link**: Binds; the previous credential of the same kind can be revoked in the same step. *(source: contracts/satellite/wallet.yaml#linkWalletCredential)*

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wearable linking wallet configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wearable linking wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wearable linking wallet configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already bound to another wallet |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
link:
  wallet: DW-0011-7741
  credential: WB-0098844
  replaces: WB-0098812 (lost)
```

#### Permissions

- `linkWalletCredential` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The same wristband or enrolled face works as stored-value payment for F&B and retail: balance checked and deducted automatically at the point of sale; top-up via the same credential. *(client request · MoM 2 Sep 2026, 4.12 Media as a Payment Method · DI-643)*
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1137` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1137`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 8: Works in Wearable Linking & Wallet Association Rules → Configure how wristbands, cards and other credentials are linked to wallet accounts. Requirement 4.3.12 specifically requires guests to link and remove venue-issued wearables from their wallet. …

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1137?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_OPERATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1138` NFC, RFID & QR Interaction Rules

**Configure how different proximity/contactless technologies interact with TICVAI Wallet. Requirement 4.3.13 specifically requires wallet payments using RFID, NFC and QR code. Configure by Technology RFID Reader type Card/wristband format Identifier validation Offline support NFC Token validation Device authentication Tap behavior Secure token requirements QR Static QR Dynamic QR QR validity period Single-use token Refresh frequency Screenshot protection controls where supported Interaction Types**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/nfc-rfid-qr-interaction-rules-bo-1138` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet channel rules that setWalletChannelRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How NFC, RFID and QR interact with the wallet: limits, offline behaviour per technology.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletChannelRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tap to Pay | select field | — | — | — | — | — | — |
| Scan to Pay | select field | — | — | — | — | — | — |
| Tap to Redeem | select field | — | — | — | — | — | — |
| Scan to Redeem | select field | — | — | — | — | — | — |
| Balance Check | select field | — | — | — | — | — | — |
| Attraction Entry | select field | — | — | — | — | — | — |
| Ride Redemption | select field | — | — | — | — | — | — |
| F&B Purchase | select field | — | — | — | — | — | — |
| Retail Purchase | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Transaction Feedback | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **per technology**: Rows per technology with limits. *(source: contracts/satellite/wallet.yaml#setWalletChannelRules)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The nfc rfid interaction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the nfc rfid interaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No nfc rfid interaction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rfid:
  offline: true
  floor: AED 100.00
```

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1138` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1138`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 10: Works in NFC, RFID & QR Interaction Rules → Configure how different proximity/contactless technologies interact with TICVAI Wallet. Requirement 4.3.13 specifically requires wallet payments using RFID, NFC and QR code. Configure by Technology …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1138?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1139` Digital Key & Wallet Authentication Policy

**Configure authentication requirements based on transaction risk. Requirement 4.3.10 specifically calls for Digital Key/Digital ID authentication wherever possible to enhance security and credential management. Authentication Methods**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure based on) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/digital-key-wallet-authentication-policy-bo-1139` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet channel rules and authentication policy that setWalletChannelRules and setWalletAuthenticationPolicy writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What proof of identity a wallet spend needs, tiered by amount, channel and kind (none, PIN, biometric, digital key).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletChannelRules, setWalletAuthenticationPolicy and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transaction amount | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Risk score | select field | — | — | — | — | — | — |
| Transaction velocity | select field | — | — | — | — | — | — |

**Sent by *Save authentication policy*** (`setWalletAuthenticationPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tiers `tiers` | repeatable rows | required | — | at most 20 | — | — | `setWalletAuthenticationPolicy` body |
| Above amount `tiers[].aboveAmount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWalletAuthenticationPolicy` body |
| Channels `tiers[].channels` | list of values (chips) | optional | — | — | — | Empty means every channel in `WalletChannelRules.allowedChannels`. | `setWalletAuthenticationPolicy` body |
| Transaction kinds `tiers[].transactionKinds` | multi-select chips | optional | — | Top up · Spend · Refund · Adjustment · Bonus · Expiry · Transfer | — | Empty means every kind. | `setWalletAuthenticationPolicy` body |
| Methods `tiers[].methods` | multi-select chips | required | — | Wallet PIN · Device authentication · Digital key · Customer login · Membership credential; at least 1; no duplicates | — | Any one of these satisfies the tier. | `setWalletAuthenticationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setWalletAuthenticationPolicy` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **tiers**: Amount bands with the proof required. *(source: contracts/satellite/wallet.yaml#setWalletAuthenticationPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet PIN (primary button) | navigation or local | — | — | — | — |
| Device authentication (secondary button) | navigation or local | — | — | — | — |
| Digital Key (secondary button) | navigation or local | — | — | — | — |
| Customer login (secondary button) | navigation or local | — | — | — | — |
| Membership credential (secondary button) | navigation or local | — | — | — | — |
| Save authentication policy (primary button) | `setWalletAuthenticationPolicy` PUT `/wallet-authentication-policy` | WalletAuthenticationPolicy | WalletAuthenticationPolicy | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 Two tiers with the same `aboveAmount` overlap on a channel and a transaction kind, or a tier lists no method. | — |

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital key wallet configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital key wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital key wallet configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Two tiers with the same `aboveAmount` overlap on a channel and a transaction kind, or a tier lists no method. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiers:
- 'up to AED 50.00: none'
- 'AED 50-500: PIN'
- 'over AED 500.00: digital key'
```

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff
- `setWalletAuthenticationPolicy` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.10 | The system should provide a digital wallet that allows Digital Key (Digital ID) authentication wherever possible to enhance security, control, and management of credentials along with other methods … | Bundles and Promotions | CONTRACTED | `setWalletAuthenticationPolicy` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1139` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1139`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 12: Works in Digital Key & Wallet Authentication Policy → Configure authentication requirements based on transaction risk. Requirement 4.3.10 specifically calls for Digital Key/Digital ID authentication wherever possible to enhance security and credential …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1139?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Wallet PIN, Device authentication, Digital Key, Customer login, Membership credential, Save authentication policy.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1140` Offline Wallet & Degraded Mode Configuration

**Maintain controlled venue operations during temporary network or service interruptions. This is especially important for amusement parks, festivals, stadiums and large attractions where wristband transactions cannot simply stop because connectivity is temporarily unavailable. Offline Eligibility**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/offline-wallet-degraded-mode-configuration-bo-1140` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet channel rules that setWalletChannelRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet behaviour during network loss: offline allowed, floor limit, maximum age of offline data.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletChannelRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | — | — |
| Outlet | select field | — | — | — | — | — | — |
| Device | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Wallet type | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Transaction type | select field | — | — | — | — | — | — |
| Offline Controls | select field | — | — | — | — | — | — |
| Offline wallet enabled | select field | — | — | — | — | — | — |
| Maximum offline transaction | select field | — | — | — | — | — | — |
| Maximum cumulative offline spend | text field | — | — | — | — | — | — |
| Maximum transactions | select field | — | — | — | — | — | — |
| Offline duration | select field | — | — | — | — | — | — |
| Cached balance permitted | select field | — | — | — | — | — | — |
| Reserved offline allowance | select field | — | — | — | — | — | — |
| Credential whitelist | select field | — | — | — | — | — | — |
| Risk profile | select field | — | — | — | — | — | — |
| Expiry of cached data | text field | — | — | — | — | — | — |
| Device storage requirements | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **offline**: Allowed, floor limit and maximum minutes; consistent with the venue offline policy (BO-130). *(source: contracts/satellite/wallet.yaml#setWalletChannelRules)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline wallet degraded configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline wallet degraded untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline wallet degraded configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-130`: Wallet spend is one of the offline data classes there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offline:
  allowed: true
  floor: AED 100.00
  maxAgeMinutes: 120
```

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1140` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1140`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 14: Works in Offline Wallet & Degraded Mode Configuration → Maintain controlled venue operations during temporary network or service interruptions. This is especially important for amusement parks, festivals, stadiums and large attractions where wristband …

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1140?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1141` Device, Terminal & Acceptance Point Mapping

**Determine exactly which devices and locations are authorized to accept TICVAI Wallet. Hierarchy Tenant → Venue → Business Area → Outlet / Attraction → Terminal → Device Acceptance Points**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PAYMENT_VIEW`, `WALLET_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/device-terminal-acceptance-point-mapping-bo-1141` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which devices and acceptance points may take the TICVAI wallet, by tenant, venue, area, outlet and terminal, with credential kinds, PIN thresholds and offline limits.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listPaymentTerminals return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/payments.yaml#listPaymentTerminals; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Device ID | select field | — | — | — | — | — | — |
| Device type | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Outlet | select field | — | — | — | — | — | — |
| Business function | select field | — | — | — | — | — | — |
| Wallet enabled | select field | — | — | — | — | — | — |
| Supported credentials | select field | — | — | — | — | — | — |
| Supported credit types | select field | — | — | — | — | — | — |
| Maximum transaction | select field | — | — | — | — | — | — |
| Offline permission | select field | — | — | — | — | — | — |
| Device risk profile | select field | — | — | — | — | — | — |
| Authentication policy | select field | — | — | — | — | — | — |
| Operating hours | select field | — | — | — | — | — | — |
| Device status | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **wallet channel rules**: Credential kinds as chips; PIN above an amount; offline allowed with a floor limit. *(source: contracts/satellite/wallet.yaml#setWalletChannelRules)*

#### Outputs: what the screen shows and produces

**Data it reads**: `listPaymentTerminals` (onLoad, Terminals and acceptance points)

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device terminal acceptance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device terminal acceptance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device terminal acceptance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
  credentials:
  - wristband
  - nfc
  - qr
  pinAbove: AED 200.00
  offline: true
  floor: AED 100.00
```

#### Permissions

- `listPaymentTerminals` → `PAYMENT_VIEW` (read) · staff
- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1141` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1141`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 16: Works in Device, Terminal & Acceptance Point Mapping → Determine exactly which devices and locations are authorized to accept TICVAI Wallet. Hierarchy Tenant → Venue → Business Area → Outlet / Attraction → Terminal → Device Acceptance Points

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1141?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`, `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1142` Wallet Transaction Simulator, Monitoring & Channel Audit

**Test the complete channel-to-wallet transaction flow before configuration is published. Simulation Scenario Customer: Family Member / Child Wallet: Family Wallet Credential: RFID Wristband #CH-0045 Venue: Theme Park Device: F&B POS #12 Purchase: AED 85 TICVAI Evaluation Credential Active → PASS Credential Linked → PASS Device Authorized → PASS Channel Wallet Enabled → PASS F&B Credit Eligible → PASS Member Spending Permission → PASS Daily Limit → PASS Authentication Requirement → PASS Connectivity → ONLINE Consumption Meal Credit → AED 30 Bonus Credit → AED 20 Cash Credit → AED 35 Transaction Approved: AED 85 Remaining wallet balances displayed. Alternative Failure Scenario Configure the complete operational lifecycle of wallet value after it has been funded or issued— including peer-to-peer transfers, refund-to-wallet, reversals, balance adjustments, blocking/freezing, disputes, corrections, exception handling and governed administrative actions. This board directly addresses requirements 4.3.15, 4.3.16, 4.3.21 and 4.3.35, while complementing the family/corporate internal allocation capabilities already configured in Board 4.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/wallet-transaction-simulator-monitoring-channel-audit-bo-1142` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test the channel-to-wallet flow before publishing and audit transactions after.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate**: Credential, wallet, purchase in; lots used out. *(source: contracts/satellite/wallet.yaml#simulateCreditConsumption)*

**Where the user goes next**

- → `BO-1133` Wallet Usage & Channel Command Center: *Back to Wallet Usage & Channel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet transaction simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet transaction simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet transaction simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet transaction simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenario:
  credential: RFID wristband CH-0045
  wallet: Family
  purchase: Ice cream AED 15.00
```

#### Permissions

- `simulateCreditConsumption` → `WALLET_VIEW` (read) · staff
- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.112 | Transaction history | Ticketing Catalogue | CONTRACTED | `listWalletTransactions` |
| 5.3.17 | Maintain guest wallet balances, top-ups, spending history, refunds, transfers, expirations, and transaction history. | F&B & Guest Management | CONTRACTED | `listWalletTransactions` |
| 22.2.14 | Wallet History | Marketing & CRM | CONTRACTED | `listWalletTransactions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1142` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1142`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 6
- Flow F298 *Wallet Configuration Backend Structure v1.0 board 6: Wallet Usage & Channel …*, step 18: Works in Wallet Transaction Simulator, Monitoring & Channel Audit → Test the complete channel-to-wallet transaction flow before configuration is published. Simulation Scenario Customer: Family Member / Child Wallet: Family Wallet Credential: RFID Wristband #CH-0045 …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1142?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1133`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"linkWalletCredential": {"method":"POST","path":"/wallet-credentials","contract":"wallet","summary":"Bind a wristband, card or device to a wallet","permission":"WALLET_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletCredential","responds":"WalletCredential"},
"listPaymentTerminals": {"method":"GET","path":"/payment-terminals","contract":"payments","summary":"Terminals, and the payment configuration on each","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"PaymentTerminal"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setWalletAuthenticationPolicy": {"method":"PUT","path":"/wallet-authentication-policy","contract":"wallet","summary":"Which proof of identity a wallet spend needs, by amount, channel and kind","permission":"WALLET_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletAuthenticationPolicy","responds":"WalletAuthenticationPolicy"},
"setWalletChannelRules": {"method":"PUT","path":"/wallet-channel-rules","contract":"wallet","summary":"Where a wallet may be used, on what, and when it may not","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletChannelRules","responds":"WalletChannelRules"},
"simulateCreditConsumption": {"method":"POST","path":"/credit-consumption/simulate","contract":"wallet","summary":"Which credit this purchase would actually use","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CreditAllocation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreditAllocation": {"type":"object","description":"Board 3.10. **Which lots this purchase would draw on**, in order.","properties":{"requested":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"covered":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"shortfall":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","properties":{"lotId":{"type":"string","format":"uuid"},"creditTypeId":{"type":"string","format":"uuid"},"creditTypeName":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"reason":{"type":"string"}}}},"rejected":{"type":"array","items":{"type":"object","properties":{"creditTypeId":{"type":"string","format":"uuid"},"reason":{"type":"string","enum":["notEligibleHere","notEligibleForProduct","expired","basketCapReached","restricted"]}}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PaymentTerminal": {"type":"object","x-ticvai-persistence":"payments.terminal","description":"Board 3. **The payment layer on a `tenancy` device**, not a second device register.","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"The `tenancy.RegisteredDevice`. **Enrolment, credentials, firmware and tamper state live there.**"},"merchantAccountId":{"type":"string","format":"uuid","nullable":true},"acquirerConnectionId":{"type":"string","format":"uuid","nullable":true},"terminalIdentifier":{"type":"string","nullable":true},"emvConfigurationVersion":{"type":"string","nullable":true},"terminalModelCode":{"type":"string","nullable":true,"description":"4.3.1. The model whose EMV and PCI certification applies (`listPaymentTerminalCertifications`)."},"entryModes":{"type":"array","description":"4.3.2. The card entry modes this terminal accepts. **`magstripe` (swipe) is off unless listed**, since a swiped card carries no chip cryptogram; it stays available as a fallback where the acquirer allows it.","items":{"type":"string","enum":["chip","contactless","magstripe","manualEntry","mobileWallet"]}},"dccEnabled":{"type":"boolean","default":false,"description":"4.3.2. Offer Dynamic Currency Conversion on a foreign card at this terminal. The rate is the provider's and is recorded on the payment (`fxRateSource` `cardScheme`); the ledger still holds the base currency."},"dccProviderConnectionId":{"type":"string","format":"uuid","nullable":true},"contactlessLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"pinBypassAllowed":{"type":"boolean","default":false},"storeAndForward":{"type":"object","description":"**A risk decision, not a technical one.**","properties":{"enabled":{"type":"boolean","default":false},"floorLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumHeldTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAgeMinutes":{"type":"integer","nullable":true}}},"status":{"type":"string","enum":["unconfigured","active","offline","suspended"]},"scopePath":{"type":"string"}}},
"WalletAuthenticationPolicy": {"type":"object","x-ticvai-persistence":"wallet.authentication_policy","description":"Board 6, p.68. **Risk-tiered proof of identity for a wallet spend.** The highest matching tier wins; with no policy, `WalletChannelRules.requiresPin` applies.","required":["tiers"],"properties":{"tiers":{"type":"array","maxItems":20,"items":{"type":"object","required":["aboveAmount","methods"],"properties":{"aboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channels":{"type":"array","description":"Empty means every channel in `WalletChannelRules.allowedChannels`.","items":{"type":"string"}},"transactionKinds":{"type":"array","description":"Empty means every kind.","items":{"$ref":"#/components/schemas/WalletTransactionKind"}},"methods":{"type":"array","minItems":1,"uniqueItems":true,"description":"Any one of these satisfies the tier.","items":{"type":"string","enum":["walletPin","deviceAuthentication","digitalKey","customerLogin","membershipCredential"]}}}}},"scopePath":{"type":"string"}}},
"WalletChannelRules": {"type":"object","x-ticvai-persistence":"wallet.channel_rules","description":"Board 6. **The offline rule is stated once, not per device.**","properties":{"allowedChannels":{"type":"array","items":{"type":"string"}},"allowedCredentialKinds":{"type":"array","items":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]}},"requiresPin":{"type":"boolean","default":false},"pinAboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"offlineAllowed":{"type":"boolean","default":false},"offlineFloorLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"offlineMaximumAgeMinutes":{"type":"integer","nullable":true,"description":"**How stale a cached balance may be before the device refuses.** Without a ceiling an offline terminal spends a balance that ran out yesterday.\n"},"acceptancePointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}},
"WalletCredential": {"type":"object","x-ticvai-persistence":"wallet.credential","description":"Boards 6.4 and 6.5. **A credential is not the wallet** — a lost wristband is relinked, not refunded.\n","required":["walletId","kind","identifier"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]},"identifier":{"type":"string"},"linkedAt":{"type":"string","format":"date-time"},"unlinkedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","lost","replaced","blocked","expired"]},"replacedByCredentialId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]}
}
```
