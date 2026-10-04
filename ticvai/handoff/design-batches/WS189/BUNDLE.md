# WS189 — Wallet Configuration Backend Structure v1.0 board 4

**10 screens · 8 operations · 10 schemas · 3 permissions**

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
  `APPROVAL_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1113` | Shared Wallet Command Center | C | 0 | 28 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1114` | Shared Wallet Model Configuration | C | 11 | 18 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1115` | Family & Household Structure Configuration | C | 11 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1116` | Parent–Child Stored Value Distribution | C | 14 | 24 | 6 | 4 | 2 | 6 | — | notStarted (—) |
| `BO-1117` | Allowance & Budget Allocation Engine | C | 12 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1118` | Member Spending Controls & Permissions | C | 23 | 18 | 6 | 0 | 1 | 5 | — | notStarted (—) |
| `BO-1119` | Corporate Wallet & Organizational Hierarchy | C | 11 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1120` | Corporate Budget, Policy & Approval Rules | C | 9 | 38 | 6 | 49 | 1 | 3 | — | notStarted (—) |
| `BO-1121` | Shared Wallet Transfers & Balance Reallocation | C | 11 | 6 | 6 | 4 | 1 | 6 | — | notStarted (—) |
| `BO-1122` | Shared Wallet Simulator, Monitoring & Audit | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-1122 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1113` Shared Wallet Command Center

**Provide administrators with a centralized operational view of all Family, Parent–Child and Corporate wallets. Backend Configuration & Monitoring**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1113 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `sharedWalletId` (navigation) |
| Route | `/orders-money/shared-wallet-command-center-bo-1113` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Family, parent-child and corporate wallets: structures, members, allowances.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSharedWallets return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listSharedWallets; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every shared wallet** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total shared wallets | text | not in the schema: `Total shared wallets` |
| Family wallets | text | not in the schema: `Family wallets` |
| Parent–child wallets | text | not in the schema: `Parent–child wallets` |
| Corporate wallets | text | not in the schema: `Corporate wallets` |
| School/group wallets | text | not in the schema: `School/group wallets` |
| Active linked users | text | not in the schema: `Active linked users` |
| Total shared balance | text | not in the schema: `Total shared balance` |
| Allocated balance | text | not in the schema: `Allocated balance` |
| Unallocated balance | text | not in the schema: `Unallocated balance` |
| Spending today | text | not in the schema: `Spending today` |
| Transfers today | text | not in the schema: `Transfers today` |
| Wallets approaching limits | text | not in the schema: `Wallets approaching limits` |
| Suspended child/member access | text | not in the schema: `Suspended child/member access` |
| Pending invitations/associations | text | not in the schema: `Pending invitations/associations` |

**The selected shared wallet** (detail panel): The pack groups this record's detail under its own headings: “Break down wallets by”.

| Shows | Format | Notes |
|---|---|---|
| Total shared wallets | text | not in the schema: `Total shared wallets` |
| Family wallets | text | not in the schema: `Family wallets` |
| Parent–child wallets | text | not in the schema: `Parent–child wallets` |
| Corporate wallets | text | not in the schema: `Corporate wallets` |
| School/group wallets | text | not in the schema: `School/group wallets` |
| Active linked users | text | not in the schema: `Active linked users` |
| Total shared balance | text | not in the schema: `Total shared balance` |
| Allocated balance | text | not in the schema: `Allocated balance` |
| Unallocated balance | text | not in the schema: `Unallocated balance` |
| Spending today | text | not in the schema: `Spending today` |
| Transfers today | text | not in the schema: `Transfers today` |
| Wallets approaching limits | text | not in the schema: `Wallets approaching limits` |
| Suspended child/member access | text | not in the schema: `Suspended child/member access` |
| Pending invitations/associations | text | not in the schema: `Pending invitations/associations` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Shared Wallet (primary button) | navigation or local | — | — | — | — |
| Add Member (secondary button) | navigation or local | — | — | — | — |
| Adjust Limits (secondary button) | navigation or local | — | — | — | — |
| Suspend Member (destructive button) | navigation or local | — | — | — | — |
| View Transactions (secondary button) | navigation or local | — | — | — | — |
| Investigate Exceptions (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **shared wallets**: Structure, owner, members, balance. *(source: contracts/satellite/wallet.yaml#listSharedWallets)*

**Data it reads**: `listSharedWallets` (onLoad, Family and corporate structures)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1114` Shared Wallet Model Configuration: *Shared Wallet Model Configuration*
- → `BO-1115` Family & Household Structure Configuration: *Family & Household Structure Configuration*; carries `sharedWalletId`
- → `BO-1116` Parent–Child Stored Value Distribution: *Parent–Child Stored Value Distribution*; carries `sharedWalletId`, `walletId`
- → `BO-1117` Allowance & Budget Allocation Engine: *Allowance & Budget Allocation Engine*; carries `sharedWalletId`
- → `BO-1118` Member Spending Controls & Permissions: *Member Spending Controls & Permissions*; carries `sharedWalletId`
- → `BO-1119` Corporate Wallet & Organizational Hierarchy: *Corporate Wallet & Organizational Hierarchy*
- → `BO-1120` Corporate Budget, Policy & Approval Rules: *Corporate Budget, Policy & Approval Rules*; carries `sharedWalletId`
- → `BO-1121` Shared Wallet Transfers & Balance Reallocation: *Shared Wallet Transfers & Balance Reallocation*; carries `walletId`
- → `BO-1122` Shared Wallet Simulator, Monitoring & Audit: *Shared Wallet Simulator, Monitoring & Audit*

**What opens over it**

- confirmDialog *Suspend Member*: **Suspend Member on a shared wallet is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shared wallet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shared wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shared wallet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the shared wallet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
wallet:
  type: family
  owner: Fatima Al Nuaimi
  members: 3
  balance: AED 640.00
```

#### Permissions

- `listSharedWallets` → `WALLET_VIEW` (read) · staff
- `createSharedWallet` → `WALLET_OPERATE` (operate) · staff
- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1113` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1113`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 1: Opens Shared Wallet Command Center → Provide administrators with a centralized operational view of all Family, Parent–Child and Corporate wallets. Backend Configuration & Monitoring
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F296 branch at step 1 (expected): when Nothing has been set up on Shared Wallet Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F296 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1113?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Shared Wallet, Add Member, Adjust Limits, Suspend Member, View Transactions, Investigate Exceptions.
- [ ] Every transition is wired: `BO-100`, `BO-1114`, `BO-1115`, `BO-1116`, `BO-1117`, `BO-1118`, `BO-1119`, `BO-1120`, `BO-1121`, `BO-1122`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1114` Shared Wallet Model Configuration

**Define reusable shared-wallet structures. Administrators can create models such as: Family Wallet Parent–Child Wallet Corporate Wallet Employee Wallet School Wallet Student Wallet Tour Group Wallet Event Group Wallet Hospitality Group Wallet Balance Models Model A — Fully Shared Balance Parent:**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1114 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/shared-wallet-model-configuration-bo-1114` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A reusable shared-wallet model record with its read and write; createSharedWallet creates a wallet, not a model.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Reusable shared-wallet models (family, parent-child, corporate, employee, school, tour group).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- createSharedWallet creates a wallet, not a reusable model. (CHG-WIR-027)

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only createSharedWallet and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet model | select field | — | — | — | — | — | — |
| Ownership type | select field | — | — | — | — | — | — |
| Maximum members | select field | — | — | — | — | — | — |
| Shared balance allowed | select field | — | — | — | — | — | — |
| Individual allocations allowed | select field | — | — | — | — | — | — |
| Hybrid mode | select field | — | — | — | — | — | — |
| Transfer capability | select field | — | — | — | — | — | — |
| Credit sharing | select field | — | — | — | — | — | — |
| Default permissions | select field | — | — | — | — | — | — |
| Default spending policy | select field | — | — | — | — | — | — |
| Applicable credit types | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **model**: Model type with its defaults. *(source: contracts/satellite/wallet.yaml#createSharedWallet)*

#### Outputs: what the screen shows and produces

**Shown**

**Family, household and corporate structures** (data table, from `listSharedWallets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Kind | chip: Family, Household, Corporate, School, Group | — |
| Owner principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Members | list or chips (count when long) | — |
| Subject | the name it points at, never the id | — |
| Role | chip: Owner, Administrator, Spender, Viewer | — |
| Allowance amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowance cadence | chip: Daily, Weekly, Monthly, None | — |
| Spend cap per transaction | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed categorys | list or chips (count when long) | — |
| Blocked categorys | list or chips (count when long) | — |
| Allowed venues | list or chips (count when long) | — |
| Active from | 1 Oct 2026 | — |
| Active to | 1 Oct 2026 | — |
| Total budget | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval above amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Data it reads**: `listSharedWallets` (onLoad, Family, household and corporate structures)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shared wallet model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shared wallet model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shared wallet model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
model:
  name: School trip wallet
  type: school
```

#### Permissions

- `createSharedWallet` → `WALLET_OPERATE` (operate) · staff
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1114` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1114`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 2: Works in Shared Wallet Model Configuration → Define reusable shared-wallet structures. Administrators can create models such as: Family Wallet Parent–Child Wallet Corporate Wallet Employee Wallet School Wallet Student Wallet Tour Group Wallet …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1114?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1115` Family & Household Structure Configuration

**Configure family relationships and wallet participation. The source requires customers to register individually or as a family/group, with a designated owner able to allocate budgets to linked accounts and monitor/cancel spending authorization. Supported Roles Family Owner Co-Owner Parent Guardian Adult Member Child Dependant Viewer**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1115 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sharedWalletId` (navigation) |
| Route | `/orders-money/family-household-structure-configuration-bo-1115` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Family relationships and who may spend from the family wallet.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSharedWalletMembers and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Primary account holder | select field | — | — | — | — | — | — |
| Secondary parent/guardian | select field | — | — | — | — | — | — |
| Dependants | select field | — | — | — | — | — | — |
| Relationship type | select field | — | — | — | — | — | — |
| Maximum family members | select field | — | — | — | — | — | — |
| Member invitation | select field | — | — | — | — | — | — |
| Member verification | select field | — | — | — | — | — | — |
| Approval required to join | text field | — | — | — | — | — | — |
| Removal rules | select field | — | — | — | — | — | — |
| Member status | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **members**: Members with role and allowance. *(source: contracts/satellite/wallet.yaml#setSharedWalletMembers)*

#### Outputs: what the screen shows and produces

**Shown**

**Family, household and corporate structures** (data table, from `listSharedWallets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Kind | chip: Family, Household, Corporate, School, Group | — |
| Owner principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Members | list or chips (count when long) | — |
| Subject | the name it points at, never the id | — |
| Role | chip: Owner, Administrator, Spender, Viewer | — |
| Allowance amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowance cadence | chip: Daily, Weekly, Monthly, None | — |
| Spend cap per transaction | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed categorys | list or chips (count when long) | — |
| Blocked categorys | list or chips (count when long) | — |
| Allowed venues | list or chips (count when long) | — |
| Active from | 1 Oct 2026 | — |
| Active to | 1 Oct 2026 | — |
| Total budget | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval above amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Data it reads**: `listSharedWallets` (onLoad, Family, household and corporate structures)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family household structure configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family household structure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family household structure configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
member:
  name: Ali
  role: child
  allowance: AED 50.00 a day
```

#### Permissions

- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1115` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1115`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 4: Works in Family & Household Structure Configuration → Configure family relationships and wallet participation. The source requires customers to register individually or as a family/group, with a designated owner able to allocate budgets to linked …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1115?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1116` Parent–Child Stored Value Distribution

**Configure the amusement-park style parent-card/child-card wallet model required specifically by 4.3.38. Example Parent Wallet Available Stored Value: AED 1,000**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1116 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sharedWalletId` (navigation), `walletId` (navigation) |
| Route | `/orders-money/parent-child-stored-value-distribution-bo-1116` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The parent-card and child-card model: the parent funds, children spend within allowances; an allowance is a cap, not a transfer.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSharedWalletMembers, transferWalletBalance and nothing that returns the current … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent wallet | select field | — | — | — | — | — | — |
| Child/dependant account | select field | — | — | — | — | — | — |
| Child card | select field | — | — | — | — | — | — |
| Child wristband | select field | — | — | — | — | — | — |
| Maximum linked children | select field | — | — | — | — | — | — |
| Shared-value access | select field | — | — | — | — | — | — |
| Allocated-value access | select field | — | — | — | — | — | — |
| Maximum spend | select field | — | — | — | — | — | — |
| Per-transaction limit | select field | — | — | — | — | — | — |
| Daily limit | select field | — | — | — | — | — | — |
| Venue restriction | select field | — | — | — | — | — | — |
| Product/category restriction | select field | — | — | — | — | — | — |
| Time restriction | select field | — | — | — | — | — | — |
| Credit-type restriction | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **allowance**: Cap with a refresh period; transfer offered separately where the venue allows. *(source: contracts/satellite/wallet.yaml#setSharedWalletMembers / contracts/satellite/wallet.yaml#transferWalletBalance)*

#### Outputs: what the screen shows and produces

**Shown**

**Family, household and corporate structures** (data table, from `listSharedWallets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Kind | chip: Family, Household, Corporate, School, Group | — |
| Owner principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Members | list or chips (count when long) | — |
| Subject | the name it points at, never the id | — |
| Role | chip: Owner, Administrator, Spender, Viewer | — |
| Allowance amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowance cadence | chip: Daily, Weekly, Monthly, None | — |
| Spend cap per transaction | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed categorys | list or chips (count when long) | — |
| Blocked categorys | list or chips (count when long) | — |
| Allowed venues | list or chips (count when long) | — |
| Active from | 1 Oct 2026 | — |
| Active to | 1 Oct 2026 | — |
| Total budget | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval above amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**A wallet's balance** (detail panel, from `getWalletBalance`)

| Shows | Format | Notes |
|---|---|---|
| Wallet balance | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Available balance | 1,234.5 | — |
| Hold balance | 1,234.5 | — |
| Total balance | 1,234.5 | — |
| Currency code | text | — |

**Data it reads**: `listSharedWallets` (onLoad, Family, household and corporate structures); `getWalletBalance` (onLoad, A wallet's balance)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The parent–child stored value configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the parent–child stored value untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No parent–child stored value configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
parent:
  balance: AED 1,000.00
  children:
  - name: Ali
    cap: AED 100.00 a day
  - name: Lina
    cap: AED 60.00 a day
```

#### Permissions

- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest
- `transferWalletBalance` → `WALLET_OPERATE` (operate) · staff, guest
- `listSharedWallets` → `WALLET_VIEW` (read) · staff
- `getWalletBalance` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.16 | The system should support peer to peer transaction for digital wallets using which a guests should be able to transfer money from their wallet to another guest's wallet. | Bundles and Promotions | CONTRACTED | `transferWalletBalance` |
| 5.5.3 | The system should provide the ability to move stored credit between portfolios linked to different accounts. For Example: each family member have their own portfolio with the possibility to transfer … | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 5.5.3 | Allow configurable transfer of stored value, wallet balances, promotional credits, and vouchers between linked portfolios with full audit tracking. | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 5.5.6 | Support shared family wallets while maintaining individual transaction tracking. | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*
- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1116` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1116`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 6: Works in Parent–Child Stored Value Distribution → Configure the amusement-park style parent-card/child-card wallet model required specifically by 4.3.38. Example Parent Wallet Available Stored Value: AED 1,000

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1116?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1117` Allowance & Budget Allocation Engine

**Configure how wallet owners distribute value to linked members. Allocation Types One-time allowance Daily allowance Weekly allowance Monthly allowance Event allowance Attraction allowance Meal allowance Ride allowance Shopping allowance Custom allocation**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1117 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sharedWalletId` (navigation) |
| Route | `/orders-money/allowance-budget-allocation-engine-bo-1117` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Allowance types (one-time, daily, weekly, monthly, event, attraction, meal) for linked members.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSharedWalletMembers and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Allocation amount | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Start date | select field | — | — | — | — | — | — |
| End date | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Auto-renewal | select field | — | — | — | — | — | — |
| Unused-balance behavior | select field | — | — | — | — | — | — |
| Carry-forward | select field | — | — | — | — | — | — |
| Return-to-parent | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Reallocation | select field | — | — | — | — | — | — |
| Funding priority | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **allowance type**: Type and amount per member. *(source: contracts/satellite/wallet.yaml#setSharedWalletMembers)*

#### Outputs: what the screen shows and produces

**Shown**

**Family, household and corporate structures** (data table, from `listSharedWallets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Kind | chip: Family, Household, Corporate, School, Group | — |
| Owner principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Members | list or chips (count when long) | — |
| Subject | the name it points at, never the id | — |
| Role | chip: Owner, Administrator, Spender, Viewer | — |
| Allowance amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowance cadence | chip: Daily, Weekly, Monthly, None | — |
| Spend cap per transaction | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed categorys | list or chips (count when long) | — |
| Blocked categorys | list or chips (count when long) | — |
| Allowed venues | list or chips (count when long) | — |
| Active from | 1 Oct 2026 | — |
| Active to | 1 Oct 2026 | — |
| Total budget | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval above amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Data it reads**: `listSharedWallets` (onLoad, Family, household and corporate structures)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The allowance budget allocation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the allowance budget allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No allowance budget allocation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
allowance:
  type: meal
  amount: AED 40.00 a day
```

#### Permissions

- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1117` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1117`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 8: Works in Allowance & Budget Allocation Engine → Configure how wallet owners distribute value to linked members. Allocation Types One-time allowance Daily allowance Weekly allowance Monthly allowance Event allowance Attraction allowance Meal …

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1117?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1118` Member Spending Controls & Permissions

**Give wallet owners granular control over what each linked member can do. The source explicitly requires family owners to cap expenses and cancel spending authorization at any time. Permission Controls**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1118 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each member configure; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sharedWalletId` (navigation) |
| Route | `/orders-money/member-spending-controls-permissions-bo-1118` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What each member may do: spend caps, categories, cancel authority at any time.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setSharedWalletMembers and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| View balance | select field | — | — | — | — | — | — |
| Spend | select field | — | — | — | — | — | — |
| Top up | select field | — | — | — | — | — | — |
| Receive funds | select field | — | — | — | — | — | — |
| Transfer funds | select field | — | — | — | — | — | — |
| Send funds | select field | — | — | — | — | — | — |
| Redeem vouchers | select field | — | — | — | — | — | — |
| Use gift cards | select field | — | — | — | — | — | — |
| Use membership benefits | select field | — | — | — | — | — | — |
| Add payment method | select field | — | — | — | — | — | — |
| Add/remove wearable | select field | — | — | — | — | — | — |
| View transaction history | select field | — | — | — | — | — | — |
| Spending Controls | select field | — | — | — | — | — | — |
| Maximum transaction amount | select field | — | — | — | — | — | — |
| Hourly limit | select field | — | — | — | — | — | — |
| Daily limit | select field | — | — | — | — | — | — |
| Weekly limit | select field | — | — | — | — | — | — |
| Monthly limit | select field | — | — | — | — | — | — |
| Number of transactions | select field | — | — | — | — | — | — |
| Product/category restrictions | select field | — | — | — | — | — | — |
| Venue restrictions | select field | — | — | — | — | — | — |
| Channel restrictions | select field | — | — | — | — | — | — |
| Time restrictions | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **permissions**: Per member switches and caps; owner can revoke instantly. *(source: contracts/satellite/wallet.yaml#setSharedWalletMembers)*

#### Outputs: what the screen shows and produces

**Shown**

**Family, household and corporate structures** (data table, from `listSharedWallets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Kind | chip: Family, Household, Corporate, School, Group | — |
| Owner principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Members | list or chips (count when long) | — |
| Subject | the name it points at, never the id | — |
| Role | chip: Owner, Administrator, Spender, Viewer | — |
| Allowance amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowance cadence | chip: Daily, Weekly, Monthly, None | — |
| Spend cap per transaction | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed categorys | list or chips (count when long) | — |
| Blocked categorys | list or chips (count when long) | — |
| Allowed venues | list or chips (count when long) | — |
| Active from | 1 Oct 2026 | — |
| Active to | 1 Oct 2026 | — |
| Total budget | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval above amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Data it reads**: `listSharedWallets` (onLoad, Family, household and corporate structures)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member spending controls configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member spending controls untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member spending controls configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
member:
  name: Ali
  categories:
  - games
  - F&B
  cap: AED 100.00
```

#### Permissions

- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1118` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1118`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 10: Works in Member Spending Controls & Permissions → Give wallet owners granular control over what each linked member can do. The source explicitly requires family owners to cap expenses and cancel spending authorization at any time. Permission Controls

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1118?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1119` Corporate Wallet & Organizational Hierarchy

**Configure wallets for companies, schools, partners and other organizations. Requirement 4.3.27 calls specifically for corporate wallets with spending limits, user-level permissions, departmental allocation and reporting. Organizational Structure**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1119 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/corporate-wallet-organizational-hierarchy-bo-1119` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Corporate wallets with departments, users and limits.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSharedWallets return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listSharedWallets; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Organization | select field | — | — | — | — | — | — |
| Business account | select field | — | — | — | — | — | — |
| Corporate wallet | select field | — | — | — | — | — | — |
| Cost center | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Team | select field | — | — | — | — | — | — |
| Employee/user | select field | — | — | — | — | — | — |
| Corporate hierarchy | select field | — | — | — | — | — | — |
| Budget owner | select field | — | — | — | — | — | — |
| Finance approver | select field | — | — | — | — | — | — |
| Wallet administrator | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **hierarchy**: Company, departments, users with limits. *(source: contracts/satellite/wallet.yaml#listSharedWallets)*

**Data it reads**: `listSharedWallets` (onLoad, Existing corporate wallets)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The corporate wallet organizational configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the corporate wallet organizational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No corporate wallet organizational configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
corporate:
  company: Gulf Engineering
  departments:
  - HR
  - Sales
  budget: AED 20,000.00
```

#### Permissions

- `createSharedWallet` → `WALLET_OPERATE` (operate) · staff
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Corporate/group wallets: funds loaded and segregated across departments (e.g. marketing, operations) for company accounts. *(client request · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-531)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1119` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1119`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 12: Works in Corporate Wallet & Organizational Hierarchy → Configure wallets for companies, schools, partners and other organizations. Requirement 4.3.27 calls specifically for corporate wallets with spending limits, user-level permissions, departmental …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1119?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1120` Corporate Budget, Policy & Approval Rules

**Control how organizational wallet funds may be spent. Budget Configuration**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1120 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sharedWalletId` (navigation) |
| Route | `/orders-money/corporate-budget-policy-approval-rules-bo-1120` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How organisational wallet funds may be spent: budgets per department and approval rules.

**Known correction pending (do not draw the wrong version)**

- **No read operation: the screen declares only setSharedWalletMembers, setApprovalMatrix and nothing that returns the current configuration.** Why: It opens as an empty form even where a configuration exists; it needs a get or list for the same record (PR-9). *(source: contracts/satellite/wallet.yaml#setSharedWalletMembers / contracts/spine/approvals.yaml#setApprovalMatrix / screens/P08-venue-back-office.yaml#BO-1120; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Corporate budget | select field | — | — | — | — | — | — |
| Department budget | select field | — | — | — | — | — | — |
| User budget | select field | — | — | — | — | — | — |
| Period | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Credit type | select field | — | — | — | — | — | — |
| Carry-forward | select field | — | — | — | — | — | — |
| Remaining-budget treatment | select field | — | — | — | — | — | — |
| Spending Policies | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **approval matrix**: Ordered rules, first match wins. *(source: contracts/spine/approvals.yaml#setApprovalMatrix)*

#### Outputs: what the screen shows and produces

**Shown**

**Family, household and corporate structures** (data table, from `listSharedWallets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Kind | chip: Family, Household, Corporate, School, Group | — |
| Owner principal | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Members | list or chips (count when long) | — |
| Subject | the name it points at, never the id | — |
| Role | chip: Owner, Administrator, Spender, Viewer | — |
| Allowance amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowance cadence | chip: Daily, Weekly, Monthly, None | — |
| Spend cap per transaction | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Allowed categorys | list or chips (count when long) | — |
| Blocked categorys | list or chips (count when long) | — |
| Allowed venues | list or chips (count when long) | — |
| Active from | 1 Oct 2026 | — |
| Active to | 1 Oct 2026 | — |
| Total budget | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval above amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**What requires approval here** (data table, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Post-spend review (primary button) | navigation or local | — | — | — | — |
| Single approval (secondary button) | navigation or local | — | — | — | — |
| Multi-level approval (secondary button) | navigation or local | — | — | — | — |
| Exception approval (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSharedWallets` (onLoad, Family, household and corporate structures); `listApprovalMatrices` (onLoad, What requires approval here)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The corporate budget policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the corporate budget policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No corporate budget policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: 'Spend over AED 500.00 by any employee: department head approves'
```

#### Permissions

- `setSharedWalletMembers` → `WALLET_OPERATE` (operate) · staff, guest
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff
- `listSharedWallets` → `WALLET_VIEW` (read) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Corporate/group wallets: funds loaded and segregated across departments (e.g. marketing, operations) for company accounts. *(client request · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-531)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1120` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1120`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 14: Works in Corporate Budget, Policy & Approval Rules → Control how organizational wallet funds may be spent. Budget Configuration
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 409, 412).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1120?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Post-spend review, Single approval, Multi-level approval, Exception approval.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1121` Shared Wallet Transfers & Balance Reallocation

**Manage movement of stored value within a family or corporate wallet structure. Supported Operations Family Parent → Child Child → Parent Parent → Parent Child → Child (if permitted) Corporate Corporate → Department Department → Employee Employee → Department Department → Corporate Department → Department**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1121 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `walletId` (navigation) |
| Route | `/orders-money/shared-wallet-transfers-balance-reallocation-bo-1121` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Moving value within a family or corporate structure (parent to child, department to department).

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only transferWalletBalance and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transfer permission | select field | — | — | — | — | — | — |
| Transferable credit types | select field | — | — | — | — | — | — |
| Minimum transfer | select field | — | — | — | — | — | — |
| Maximum transfer | select field | — | — | — | — | — | — |
| Daily transfer limit | select field | — | — | — | — | — | — |
| Approval requirement | select field | — | — | — | — | — | — |
| Transfer fees | select field | — | — | — | — | — | — |
| Expiry inheritance | select field | — | — | — | — | — | — |
| Source-credit preservation | select field | — | — | — | — | — | — |
| Return unused allocation | select field | — | — | — | — | — | — |
| Automatic reallocation | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**A wallet's balance** (detail panel, from `getWalletBalance`)

| Shows | Format | Notes |
|---|---|---|
| Wallet balance | the name it points at, never the id | — |
| Wallet | the name it points at, never the id | — |
| Available balance | 1,234.5 | — |
| Hold balance | 1,234.5 | — |
| Total balance | 1,234.5 | — |
| Currency code | text | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Transfer**: Amount and recipient; refused where the structure does not permit the direction. *(source: contracts/satellite/wallet.yaml#transferWalletBalance)*

**Data it reads**: `getWalletBalance` (onLoad, A wallet's balance)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shared wallet transfers configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shared wallet transfers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shared wallet transfers configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
transfer:
  from: Parent
  to: Lina
  amount: AED 50.00
```

#### Permissions

- `transferWalletBalance` → `WALLET_OPERATE` (operate) · staff, guest
- `getWalletBalance` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.16 | The system should support peer to peer transaction for digital wallets using which a guests should be able to transfer money from their wallet to another guest's wallet. | Bundles and Promotions | CONTRACTED | `transferWalletBalance` |
| 5.5.3 | The system should provide the ability to move stored credit between portfolios linked to different accounts. For Example: each family member have their own portfolio with the possibility to transfer … | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 5.5.3 | Allow configurable transfer of stored value, wallet balances, promotional credits, and vouchers between linked portfolios with full audit tracking. | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 5.5.6 | Support shared family wallets while maintaining individual transaction tracking. | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Balance can move between linked family/group wallets in either direction (parent to child, child to parent); a venue-controlled toggle, not always enabled. *(agreed · MoM 27 Aug 2026, 4.8 Shared wallet transfer · DI-532)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1121` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1121`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 16: Works in Shared Wallet Transfers & Balance Reallocation → Manage movement of stored value within a family or corporate wallet structure. Supported Operations Family Parent → Child Child → Parent Parent → Parent Child → Child (if permitted) Corporate …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1121?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1122` Shared Wallet Simulator, Monitoring & Audit

**Test complex family/corporate wallet policies before publication and provide complete traceability after activation. Simulation Example Family Wallet Balance: AED 1,500 Child A Daily Limit: AED 100 Used Today: AED 70 Requested Transaction: AED 50 Wallet Balance → PASS Member Permission → PASS Product Eligibility → PASS Daily Limit → FAIL Remaining allowance = AED 30 Result Transaction Declined Reason: Daily member spending limit exceeded. Corporate Simulation Configure the complete lifecycle of gift cards, digital vouchers, coupons, campaign rewards, complimentary credits and membership-related benefits stored or presented inside the TICVAI Wallet. This board covers the requirements to support gift-card balances, digital vouchers, membership-related credits and benefits, activation, partial redemption, expiry, balance inquiry, transaction history, gift-card liability, and integration with other TICVAI modules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1122 |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/shared-wallet-simulator-monitoring-audit-bo-1122` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test family and corporate policies before publication and trace them after.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listSharedWallets return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listSharedWallets; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | text field | — | — | `listSharedWallets` ?kind |

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

- **Simulate**: As BO-1110 with member limits applied. *(source: contracts/satellite/wallet.yaml#simulateCreditConsumption)*

**Data it reads**: `listSharedWallets` (onLoad, Monitor the structures)

**Where the user goes next**

- → `BO-1113` Shared Wallet Command Center: *Back to Shared Wallet Command Center*; carries `sharedWalletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shared wallet simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shared wallet simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shared wallet simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the shared wallet simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  wallet: Family AED 1,500.00
  child: daily limit AED 100.00
  purchase: AED 120.00
  result: 'refused: over daily limit'
```

#### Permissions

- `simulateCreditConsumption` → `WALLET_VIEW` (read) · staff
- `listSharedWallets` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1122` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1122`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 4
- Flow F296 *Wallet Configuration Backend Structure v1.0 board 4: Shared Wallet Command …*, step 18: Works in Shared Wallet Simulator, Monitoring & Audit → Test complex family/corporate wallet policies before publication and provide complete traceability after activation. Simulation Example Family Wallet Balance: AED 1,500 Child A Daily Limit: AED 100 …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1122?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1113`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createSharedWallet": {"method":"POST","path":"/shared-wallets","contract":"wallet","summary":"Set up a family, household or corporate wallet","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SharedWallet","responds":"SharedWallet"},
"getWalletBalance": {"method":"GET","path":"/wallets/{walletId}/balance","contract":"wallet","summary":"A wallet's balance","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"walletId","in":"path","required":true}],"requestBody":null,"responds":"WalletBalance"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listSharedWallets": {"method":"GET","path":"/shared-wallets","contract":"wallet","summary":"Family, household and corporate structures","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"SharedWallet"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setSharedWalletMembers": {"method":"PUT","path":"/shared-wallets/{sharedWalletId}/members","contract":"wallet","summary":"Allowances, budgets and what each member may spend on","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SharedWalletMember"},
"simulateCreditConsumption": {"method":"POST","path":"/credit-consumption/simulate","contract":"wallet","summary":"Which credit this purchase would actually use","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CreditAllocation"},
"transferWalletBalance": {"method":"POST","path":"/wallets/{walletId}/transfer","contract":"wallet","summary":"Send balance to another guest","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletTransaction"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"},"code":{"type":"string","maxLength":64,"nullable":true,"description":"**A stable code for the rule, unique within its matrix** (4 October 2026, CHG-FXC-005). The composite `approveMatrixMultiLevel` upserts a rule by it; `setApprovalMatrix` may leave it null."},"minimumApprovals":{"type":"integer","minimum":1,"nullable":true,"description":"N in N-of-M (CHG-FXC-005). Null means every approver the mode asks."},"requiredApproverRoleId":{"type":"string","format":"uuid","nullable":true,"description":"A role that must be among the approvals whatever N is (the CFO in an N-of-M group); it is also one of `approverRoleIds` (CHG-FXC-005)."},"rejectionBehavior":{"type":"string","nullable":true,"enum":["rejectRequest","returnToPreviousLevel","returnToRequester"],"description":"What a rejection at this rule does; null is `rejectRequest` (CHG-FXC-005)."},"allowRequestChanges":{"type":"boolean","default":false},"allowDelegate":{"type":"boolean","default":true},"allowReassign":{"type":"boolean","default":false},"minPercentage":{"type":"number","nullable":true,"description":"A percentage threshold (a discount or a margin impact) at or above which the rule applies, beside `minAmount` (CHG-FXC-005)."},"matchAttributes":{"type":"object","x-ticvai-persistence-column":"jsonb","nullable":true,"additionalProperties":{"type":"string"},"description":"**The request attributes a rule matches on** (CHG-FXC-005): keys `module`, `product`, `department`, `customerType`, `risk`, `exceptionType`, `legalEntity`, each an exact value the request's attributes must carry. Every key given must match; an absent key matches anything. Evaluated before `condition`."},"compositeMode":{"type":"string","nullable":true,"enum":["single","sequential","parallel","anyOne","allMustApprove","conditional","multiLevel"],"description":"The `approvalMode` the composite screen sent, kept so it reads back what it saved; `mode`, `levels` and `minimumApprovals` are what the engine runs (CHG-FXC-005)."}}},
"CreditAllocation": {"type":"object","description":"Board 3.10. **Which lots this purchase would draw on**, in order.","properties":{"requested":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"covered":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"shortfall":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","properties":{"lotId":{"type":"string","format":"uuid"},"creditTypeId":{"type":"string","format":"uuid"},"creditTypeName":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"reason":{"type":"string"}}}},"rejected":{"type":"array","items":{"type":"object","properties":{"creditTypeId":{"type":"string","format":"uuid"},"reason":{"type":"string","enum":["notEligibleHere","notEligibleForProduct","expired","basketCapReached","restricted"]}}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"SharedWallet": {"type":"object","x-ticvai-persistence":"wallet.shared_wallet","description":"Board 4. **One pot, distributed authority.**","required":["kind","walletId"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["family","household","corporate","school","group"]},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"members":{"type":"array","items":{"$ref":"#/components/schemas/SharedWalletMember"}},"totalBudget":{"x-ticvai-column":"budget_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"approvalAboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"SharedWalletMember": {"type":"object","x-ticvai-persistence":"wallet.shared_wallet_member","description":"Boards 4.5 and 4.6. **An allowance is a cap with a refresh, not a transfer.**","required":["subjectId"],"properties":{"subjectId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["owner","administrator","spender","viewer"]},"allowanceAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowanceCadence":{"type":"string","enum":["daily","weekly","monthly","none"],"default":"none"},"spendCapPerTransaction":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"blockedCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"activeFrom":{"type":"string","format":"date","nullable":true},"activeTo":{"type":"string","format":"date","nullable":true}}},
"WalletBalance": {"type":"object","x-ticvai-persistence":"wallet.balance","description":"**Taken from the backend workbook, 20 September.** Stores the current wallet balance for fast checkout: available amount, held amount, and total amount.","required":["walletBalanceId","walletId","availableBalance","holdBalance","totalBalance","currencyCode","version","updatedAt"],"properties":{"walletBalanceId":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"availableBalance":{"type":"number"},"holdBalance":{"type":"number"},"totalBalance":{"x-ticvai-column":"balance_amount","type":"number"},"currencyCode":{"type":"string","maxLength":10},"version":{"type":"integer"},"updatedAt":{"type":"string","format":"date-time"}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]}
}
```
