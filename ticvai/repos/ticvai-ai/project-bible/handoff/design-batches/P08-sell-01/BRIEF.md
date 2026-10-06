# P08-sell-01 — P08 · Sell (1 of 4)

**10 screens · 97 operations · 104 schemas · 13 permissions**

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

- **Every control that can be refused must be gated.** 13 permissions apply here:
  `ASSET_LIBRARY_VIEW, CAPACITY_CONFIGURE, EVENT_CONFIGURE, GUEST_VIEW, PARTNER_MANAGE, PARTNER_VIEW, PERFORMANCE_CONFIGURE, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`…. A control nobody can use must say so,
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
| `BO-007` | Product Directory | A | 101 | 41 | 6 | 75 | 3 | 0 | — | notStarted (generated) |
| `BO-008` | Product Detail & Variants | A | 45 | 39 | 6 | 37 | 22 | 3 | — | notStarted (generated) |
| `BO-009` | Pricing Rules | A | 57 | 21 | 6 | 19 | 3 | 0 | — | notStarted (generated) |
| `BO-010` | Promotions & Coupons | A | 165 | 39 | 6 | 51 | 3 | 2 | — | notStarted (generated) |
| `BO-011` | Packages & Bundles | A | 69 | 56 | 6 | 11 | 4 | 0 | — | notStarted (generated) |
| `BO-012` | Membership Products | A | 119 | 36 | 6 | 112 | 0 | 0 | — | notStarted (generated) |
| `BO-013` | Channel & Distribution | A | 40 | 32 | 6 | 34 | 2 | 0 | — | notStarted (generated) |
| `BO-014` | Catalogue Publishing | B | 8 | 19 | 6 | 30 | 0 | 6 | — | notStarted (generated) |
| `BO-015` | Performance Calendar | A | 44 | 47 | 6 | 38 | 5 | 0 | — | notStarted (generated) |
| `BO-016` | Performance Template | B | 19 | 15 | 6 | 0 | 5 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-016 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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

### Screen by screen

**`BO-007` Product Directory**

- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Product lifecycle dashboard shows counts of products in draft, in approval and published, filterable by venue/department; every product must be authorised before publishing online or on-site. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-438)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*

**`BO-008` Product Detail & Variants**

- Decision: all policy types — reschedule, exchange, refund, cancellation, upgrade/downgrade, ownership transfer, membership-to-pass conversion — are managed centrally within the unified product configuration, not separate screens. Each product also maps pricing, GL account code, promotions and channel availability. *(agreed · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 5. Key Decisions · DI-466)*
- Decision: special product types — group (min/max size, single or multiple QR codes), family (min/max composition) and corporate/allocation tickets — are configured within the same unified product configuration screen, not separate screens. *(agreed · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships; 5. Key Decisions · DI-465)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*
- Validity types: fixed date range, rolling (e.g. 90 days from issue) and first-use activation (starts at first scan). Confirmed: first-use tickets need a fallback expiry (e.g. issue date + 30 days) if never scanned. *(agreed · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-451)*
- Products are classified by configurable components (e.g. resident/non-resident → standard/VIP tier → adult/child/youth), not a fixed structure; components can be added and a simple venue may use only guest category. Tickets can be anonymous or require captured guest details. *(client request · MoM 25 Aug 2026, 4.4 Product Combination Matrix & Ownership · DI-450)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Open-dated ticket: name, description, price and validity period (e.g. 1 day, 1 month, 6 months), with a configurable reservation rule controlling whether customer details (name, email, phone) are captured at point of sale. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-445)*
- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Content localisation: separate content (images, descriptions) per sales channel (POS vs. B2C/B2B) and per language (e.g. English/Arabic). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-442)*
- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- Six core ticket types: Open-Dated (no fixed date; GA and B2B/travel-agent QR resale), Group & Family (configurable group size, single-scan or multi-scan QR), Membership/Subscription (full details per member; renew/upgrade/cancel), Event (date/time selection, resources, capacity), Gift Voucher, Money Card. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-433)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*
- Product master holds price, stock and variant attributes (e.g. size/colour) with a distinct barcode per variant; stock is tracked per variant/size. Decision: size/variant attributes (small/medium/large) are configurable per product type in the admin panel and appear dynamically when products are added. *(agreed · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management; 5. Key Decisions · DI-354)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*
- Components/attributes model: a component (e.g. "ticket type") has attributes (adult, youth, senior, infant, child) each priced independently; adding an attribute creates a new sellable variant with no extra setup. Who may sell a product is restricted by site, operating area, workstation or role. *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-164)*
- Product record holds: price (tax inclusive/exclusive), linked print template, system product code, a toggle for capturing reservation details at sale, and entitlements (upgradeable, stored-value load, linked event, re-entry, linked performance). Multiple price lists per channel and season (winter/summer). *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-163)*

**`BO-009` Pricing Rules**

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*
- Product record holds: price (tax inclusive/exclusive), linked print template, system product code, a toggle for capturing reservation details at sale, and entitlements (upgradeable, stored-value load, linked event, re-entry, linked performance). Multiple price lists per channel and season (winter/summer). *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-163)*
- Prices are set per channel (web store, mobile app, kiosk, walk-up/POS) in one centralised "price matrix"; each channel picks up its price automatically once published. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-140)*

**`BO-010` Promotions & Coupons**

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Coupons as one shared promo code (e.g. for social media) or a batch of unique single-use codes, with configurable reuse rules. *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-173)*

**`BO-011` Packages & Bundles**

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)*
- Retail items (e.g. a t-shirt plus a cap) can be combined into a combo package with bundle-level pricing, presented both on-site and online with product images and descriptions. *(client request · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions · DI-358)*
- Bundle packages combine components within one attraction (ticket + meal + retail, or ticket + event ticket) at a discount — not a cross-attraction itinerary. *(agreed · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-220)*

**`BO-013` Channel & Distribution**

- Catalog Builder & Store Assortment maps which products sell on which channel (on-site, online, or restricted), managed at catalog level rather than per individual product. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-356)*
- Prices are set per channel (web store, mobile app, kiosk, walk-up/POS) in one centralised "price matrix"; each channel picks up its price automatically once published. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-140)*

**`BO-015` Performance Calendar**

- Time-slot creation asks for start and end date, first and last start time of the day, interval between starts (e.g. every 30 minutes), slot length, days of the week, language and format, and previews the slots before any is created. *(agreed · MoM 24 Sep 2026, M24-01 · DI-995)*
- Example the configuration screens must show concretely: how time slots are created, including start/end dates, times and interval parameters. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-986)*
- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*

**`BO-016` Performance Template**

- Example the configuration screens must show concretely: how time slots are created, including start/end dates, times and interval parameters. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-986)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*
